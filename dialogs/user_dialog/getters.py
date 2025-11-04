from aiogram.types import CallbackQuery, User, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput

from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, SurveySG


config: Config = load_config()


async def start_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    admin = False
    admins = [*config.bot.admin_ids]
    admins.extend([admin.user_id for admin in await session.get_admins()])
    if event_from_user.id in admins:
        admin = True
    user = await session.get_user(event_from_user.id)
    print(user)
    if user.interviewed:
        text = '✅Анкета отправлена'
    else:
        text = '📝 Разместить анкету'
    return {
        'text': text,
        'admin': admin
    }


async def choose_male_switcher(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    user = await session.get_user(clb.from_user.id)
    if user.interviewed:
        await clb.answer('Вы уже заполняли анкету, пожалуйста ожидайте проверку')
        return
    await dialog_manager.switch_to(startSG.choose_male)


async def choose_male(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    male = clb.data.split('_')[0]
    await dialog_manager.start(SurveySG.get_age, data={'male': male})
