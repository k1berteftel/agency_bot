from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Cancel, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory

from dialogs.survey_dialogs import getters

from states.state_groups import SurveySG


survey_dialog = Dialog(
    Window(
        Const('Укажите свой возраст (от 18 до 60 лет)\nОтправляя возраст, вы подтверждаете, что вам уже есть 18 лет.'),
        TextInput(
            id='get_age',
            on_success=getters.get_age
        ),
        Cancel(Const('⬅️Назад'), id='close_dialog'),
        state=SurveySG.get_age
    ),
    Window(
        Const('Укажите ваше семейное положение'),
        Group(
            Button(Const('Женат'), id='marry_married_choose', on_click=getters.married_choose),
            Button(Const('Женат не более 1-й'), id='one_married_choose', on_click=getters.married_choose),
            Button(Const('В разводе'), id='divorce_married_choose', on_click=getters.married_choose),
            Button(Const('Вдова/Вдовец'), id='widow_married_choose', on_click=getters.married_choose),
            Button(Const('Не был(-а) в браке'), id='no_married_choose', on_click=getters.married_choose),
            width=3
        ),
        Back(Const('⬅️Назад'), id='back_get_age'),
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
        ),
        state=SurveySG.get_married
    ),
    Window(
        Const('Укажите наличие детей (можно выбрать вариант или ввести текст):'),
        TextInput(
            id='get_children',
            on_success=getters.get_children
        ),
        Group(
            Button(Const('Детей нет'), id='no_children_choose',  on_click=getters.children_choose),
            Button(Const('1 ребенок'), id='one_children_choose',  on_click=getters.children_choose),
            Button(Const('Двое детей'), id='two_children_choose',  on_click=getters.children_choose),
            Button(Const('3+ детей'), id='three_children_choose',  on_click=getters.children_choose),
            width=1
        ),
        Back(Const('⬅️Назад'), id='back_get_married'),
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
        ),
        state=SurveySG.get_children
    ),
    Window(
        Const('Ваше место проживания:\n\nВведите название города или региона:\n💡 Например: Дагестан, Москва, '
              'Ташкент, Стамбул\n🌍 Или название страны: Россия, Казахстан, Узбекистан'),
        TextInput(
            id='get_city',
            on_success=getters.get_city
        ),
        Back(Const('⬅️Назад'), id='back_get_children'),
        state=SurveySG.get_city
    ),
    Window(
        Const('Укажите вашу национальность'),
        TextInput(
            id='get_origin',
            on_success=getters.get_origin
        ),
        Back(Const('⬅️Назад'), id='back_get_city'),
        state=SurveySG.get_origin
    ),
    Window(
        Const('Введите ваше имя или ник'),
        TextInput(
            id='get_name',
            on_success=getters.get_name
        ),
        Back(Const('⬅️Назад'), id='back_get_origin'),
        state=SurveySG.get_name
    ),
    Window(
        Const('Расскажите подробно о себе и опишите будущего кандидата. Добавьте информацию о хобби, работе, '
              'ценностях и пожеланиях к будущему партнёру'),
        TextInput(
            id='get_about',
            on_success=getters.get_about
        ),
        Back(Const('⬅️Назад'), id='back_get_name'),
        state=SurveySG.get_about
    ),
    Window(
        Const('Укажите ваши контактные контактные данные, чтобы мы могли с вами связаться'),
        TextInput(
            id='get_contact',
            on_success=getters.get_contact
        ),
        Back(Const('⬅️Назад'), id='back_get_about'),
        state=SurveySG.get_contact
    ),
    Window(
        Const('Отправьте одно фото для анкеты'),
        MessageInput(
            func=getters.get_photo,
            content_types=ContentType.PHOTO
        ),
        Back(Const('⬅️Назад'), id='back_get_contact'),
        state=SurveySG.get_photo
    ),
)