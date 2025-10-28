from dialogs.user_dialog.dialog import user_dialog
from dialogs.admin_dialog.dialog import admin_dialog
from dialogs.payment_dialog.dialog import payment_dialog
from dialogs.survey_dialogs.dialog import survey_dialog


def get_dialogs():
    return [user_dialog, survey_dialog, payment_dialog, admin_dialog]