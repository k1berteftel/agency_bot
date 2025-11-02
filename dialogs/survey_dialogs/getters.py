from aiogram.types import CallbackQuery, User, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput

from utils.text_utils import get_form_text
from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, SurveySG, PaymentSG


config: Config = load_config()


async def get_age(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
        dialog_manager.start_data.clear()
    try:
        age = int(text)
    except Exception:
        await msg.answer('❗️Возраст должен быть числом, пожалуйста попробуйте еще раз'),
        return
    if age < 18:
        await msg.answer('❗️Вам должно быть больше 18')
        return
    dialog_manager.dialog_data['age'] = age
    await dialog_manager.switch_to(SurveySG.get_married)


async def married_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    choose = clb.data.split('_')[0]
    male = dialog_manager.dialog_data.get('male')
    if choose == 'marry':
        marry = 'Женат'
    elif choose == 'one':
        marry = 'Женат не более 1-й'
    elif choose == 'divorce':
        marry = 'В разводе'
    elif choose == 'widow':
        if male == 'men':
            marry = 'Вдовец'
        else:
            marry = 'Вдова'
    else:
        if male == 'men':
            marry = 'Не был в браке'
        else:
            marry = 'Не была в браке'
    dialog_manager.dialog_data['married'] = marry
    await dialog_manager.switch_to(SurveySG.get_children)


async def get_children(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['children'] = text
    await dialog_manager.switch_to(SurveySG.get_city)


async def children_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    choose = clb.data.split('_')[0]
    if choose == 'no':
        children = 'Детей нет'
    elif choose == 'one':
        children = '1 ребенок'
    elif choose == 'two':
        children = 'Двое детей'
    else:
        children = '3+ детей'
    dialog_manager.dialog_data['children'] = children
    await dialog_manager.switch_to(SurveySG.get_city)


async def get_city(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['city'] = text
    await dialog_manager.switch_to(SurveySG.get_origin)


async def get_origin(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['origin'] = text
    await dialog_manager.switch_to(SurveySG.get_name)


async def get_name(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['name'] = text
    await dialog_manager.switch_to(SurveySG.get_about)


async def get_about(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['about'] = text
    await dialog_manager.switch_to(SurveySG.get_contact)


async def get_contact(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['contact'] = text
    await dialog_manager.switch_to(SurveySG.get_photo)


async def get_photo(msg: Message, widget: MessageInput, dialog_manager: DialogManager):
    male = dialog_manager.dialog_data.get('male')
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    photo = msg.photo[-1].file_id
    dialog_manager.dialog_data['photo'] = photo
    if True:  # male == 'women':
        text = get_form_text(
            '@' + msg.from_user.username if msg.from_user.username else '-',
            dialog_manager.dialog_data
        )
        await msg.bot.send_photo(
            chat_id=config.bot.channel,
            photo=photo,
            caption=text
        )
        await msg.answer('✅Ваша анкета была успешно отправлена на модерацию, '
                         'в скором времени мы выложим ее в наш канал')
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
        await msg.delete()
        await session.set_interviewed(msg.from_user.id)
        return
    await dialog_manager.start(PaymentSG.choose_payment, data=dialog_manager.dialog_data)