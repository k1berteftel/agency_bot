from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Cancel, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.payment_dialog import getters

from states.state_groups import PaymentSG


payment_dialog = Dialog(
    Window(
        Const('🏦<b>Выберите способ оплаты</b>\n'),
        Format('{text}'),
        Column(
            Button(Const('💳Карта'), id='card_payment_choose', on_click=getters.payment_choose),
        ),
        Cancel(Const('⬅️Назад'), id='close_dialog'),
        getter=getters.payment_choose_getter,
        state=PaymentSG.choose_payment
    ),
    Window(
        Const('⌛️Проведите оплату по указанному номеру карты:\n - <code>2200702064408250</code>\n'
              'После оплаты нажмите ниже "✅Оплатил"'),
        Column(
            SwitchTo(Const('✅Оплатил'), id='get_pay_confirm_switcher', state=PaymentSG.get_pay_confirm),
        ),
        Back(Const('⬅️Назад'), id='back_choose_payment'),
        getter=getters.card_process_getter,
        state=PaymentSG.card_process_payment
    ),
    Window(
        Const('Отправьте фото подтверждающее перевод средств👇'),
        MessageInput(
            func=getters.get_pay_confirm,
            content_types=ContentType.ANY
        ),
        Back(Const('⬅️Назад'), id='back_card_process'),
        state=PaymentSG.get_pay_confirm
    ),
    Window(
        Const('<b>⌛️Ожидание оплаты</b>'),
        Format('{text}'),
        Column(
            Url(Const('🔗Оплатить'), id='url', url=Format('{url}')),
        ),
        Button(Const('⬅️Назад'), id='back_choose_payment', on_click=getters.close_payment),
        getter=getters.process_payment_getter,
        state=PaymentSG.process_payment
    ),
)
