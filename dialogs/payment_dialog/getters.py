import asyncio
from cachetools import TTLCache

from aiogram.types import CallbackQuery, User, Message, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from keyboards.admin import get_confirm_pay_keyboard
from utils.payments.create_payment import get_robokassa_url
from utils.payments.process_payment import wait_for_payment
from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, PaymentSG


config: Config = load_config()


async def payment_choose_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    prices = await session.get_prices()
    amount = prices.cost
    text = f'<blockquote> - Сумма к оплате: {amount}₽</blockquote>'
    return {
        'text': text,
    }


async def payment_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
        dialog_manager.start_data.clear()
    await dialog_manager.switch_to(PaymentSG.card_process_payment)
    return
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    prices = await session.get_prices()
    amount = prices.cost
    payment = clb.data.split('_')[0]
    if payment == 'card':
        payment = await get_robokassa_url(amount)
        task = asyncio.create_task(
            wait_for_payment(
                payment_id=payment.get('id'),
                user_id=clb.from_user.id,
                bot=clb.bot,
                session=session,
                amount=amount,
                data=dialog_manager.dialog_data,
                payment_type='card',
            )
        )
        for active_task in asyncio.all_tasks():
            if active_task.get_name() == f'process_payment_{clb.from_user.id}':
                active_task.cancel()
        task.set_name(f'process_payment_{clb.from_user.id}')
        dialog_manager.dialog_data['url'] = payment.get('url')
        await dialog_manager.switch_to(PaymentSG.process_payment)
        return


async def process_payment_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    prices = await session.get_prices()
    amount = prices.cost
    url = dialog_manager.dialog_data.get('url')
    text = f'<blockquote> - Сумма к оплате: {amount}₽</blockquote>'
    return {
        'text': text,
        'url': url
    }


async def card_process_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    prices = await session.get_prices()
    amount = prices.cost
    text = f'<blockquote> - Сумма к оплате: {amount}₽</blockquote>'
    return {
        'text': text
    }


async def get_pay_confirm(msg: Message, widget: MessageInput, dialog_manager: DialogManager):
    keyboard = await get_confirm_pay_keyboard(msg.from_user.id)
    form_storage: TTLCache = dialog_manager.middleware_data.get('form_storage')
    form_storage[msg.from_user.id] = dialog_manager.dialog_data
    for admin in config.bot.admin_ids:
        try:
            await msg.bot.copy_message(
                chat_id=admin,
                from_chat_id=msg.chat.id,
                message_id=msg.message_id
            )
            await msg.bot.send_message(
                chat_id=admin,
                text='Проверьте платеж по карте',
                reply_markup=keyboard
            )
        except Exception as err:
            print(err)
            continue
    await msg.answer('🕝Заявка на проверку оплаты была успешно отправлена, пожалуйста ожидайте')
    if dialog_manager.has_context():
        await dialog_manager.done()
        try:
            await msg.bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id - 1)
        except Exception:
            ...
        counter = 1
        while dialog_manager.has_context():
            await dialog_manager.done()
            try:
                await msg.bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id + counter)
            except Exception:
                ...
            counter += 1
    await dialog_manager.start(state=startSG.start, mode=StartMode.RESET_STACK)


async def close_payment(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    name = f'process_payment_{clb.from_user.id}'
    for task in asyncio.all_tasks():
        if task.get_name() == name:
            task.cancel()
    await dialog_manager.switch_to(PaymentSG.choose_payment)