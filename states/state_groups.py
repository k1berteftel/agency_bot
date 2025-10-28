from aiogram.fsm.state import State, StatesGroup

# Обычная группа состояний


class startSG(StatesGroup):
    start = State()

    choose_male = State()


class SurveySG(StatesGroup):
    get_age = State()
    get_married = State()
    get_children = State()
    get_city = State()
    get_origin = State()
    get_name = State()
    get_about = State()
    get_contact = State()
    get_photo = State()


class adminSG(StatesGroup):
    start = State()
    get_mail = State()
    get_time = State()
    get_keyboard = State()
    confirm_mail = State()

    deeplink_menu = State()
    deeplink_del = State()

    admin_menu = State()
    admin_del = State()
    admin_add = State()

    cost_menu = State()


class PaymentSG(StatesGroup):
    choose_payment = State()
    process_payment = State()

    card_process_payment = State()

    get_pay_confirm = State()
