from cachetools import TTLCache

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from config_data.config import Config, load_config
from utils.text_utils import get_form_text
from database.action_data_class import DataInteraction
from states.state_groups import startSG

config: Config = load_config()

admin_handlers = Router()


@admin_handlers.callback_query(F.data.startswith("confirm_pay"))
async def confirm_user_pay(clb: CallbackQuery, session: DataInteraction, form_storage: TTLCache):
    user_id = int(clb.data.split('_')[-1])
    prices = await session.get_prices()
    amount = prices.cost
    user = await session.get_user(user_id)
    data = form_storage.get(user_id)
    text = get_form_text("@" + user.username if user.username else '-', data)
    await clb.bot.send_photo(
        chat_id=config.bot.channel,
        photo=data.get("photo"),
        caption=text
    )
    try:
        await clb.bot.send_message(
            chat_id=user_id,
            text='✅Ваша анкета была успешно отправлена на модерацию, '
                 'в скором времени мы выложим ее в наш канал'
        )
    except Exception:
        ...
    await session.add_income(amount)
    try:
        await clb.message.delete()
        await clb.bot.delete_message(chat_id=clb.from_user.id, message_id=clb.message.message_id - 1)
    except Exception:
        ...
    del form_storage[user_id]


@admin_handlers.callback_query(F.data.startswith("cancel_pay"))
async def del_message(clb: CallbackQuery, session: DataInteraction, form_storage: TTLCache):
    user_id = int(clb.data.split('_')[-1])
    del form_storage[user_id]
    try:
        await clb.bot.send_message(
            chat_id=user_id,
            text='🚨Ваша оплата по карте не прошла, пожалуйста обратитесь в поддержку'
        )
    except Exception:
        ...
    try:
        await clb.message.delete()
        await clb.bot.delete_message(chat_id=clb.from_user.id, message_id=clb.message.message_id - 1)
    except Exception:
        ...
