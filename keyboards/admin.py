from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_confirm_pay_keyboard(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='✅Успешно', callback_data=f'confirm_pay_{user_id}')],
            [InlineKeyboardButton(text='❌Оплата не прошла', callback_data=f'cancel_pay_{user_id}')]
        ]
    )
    return keyboard