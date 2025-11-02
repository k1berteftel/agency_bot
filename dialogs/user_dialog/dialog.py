from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.user_dialog import getters

from states.state_groups import startSG, adminSG

user_dialog = Dialog(
    Window(
        Const('<b>Assalamu alaikum wa rahmatullahi wa barakatuh!</b>👋\n\nДобро пожаловать в бот '
              'мусульманского брачного агентства <b>Noor Nikah!</b>\n\n💡Наша цель — помочь вам найти свою '
              'вторую половинку для создания крепкой и счастливой семьи\nНу что, начнем?'),
        Column(
            SwitchTo(Format('{text}'), id='choose_male_switcher', state=startSG.choose_male),
            Url(Const('🕌Наш канал'), id='channel_url', url=Const("https://t.me/noor_nikah")),
            Url(Const('🆘Поддержка'), id='support_url', url=Const('https://t.me/Leggit_dev')),
            Url(Const('📃Оферта'), id='service_url', url=Const('https://telegra.ph/PUBLICHNAYA-OFERTA-10-21-5')),
            Start(Const('Админ панель'), id='admin', state=adminSG.start, when='admin')
        ),
        getter=getters.start_getter,
        state=startSG.start
    ),
    Window(
        Const('Какую анкету вы заполняете? <em>(Какого вы пола?)</em>'),
        Column(
            Button(Const('Мужская анкета'), id='men_form_start', on_click=getters.choose_male),
            Button(Const('Женская анкета'), id='women_form_start', on_click=getters.choose_male)
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        state=startSG.choose_male
    ),
)