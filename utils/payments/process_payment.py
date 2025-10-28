import datetime
import random
from typing import Literal
import asyncio
from asyncio import TimeoutError

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from nats.js import JetStreamContext

from utils.text_utils import get_form_text
from utils.payments.create_payment import check_robokassa_url
from database.action_data_class import DataInteraction
from config_data.config import Config, load_config


config: Config = load_config()


async def wait_for_payment(
        payment_id,
        user_id: int,
        bot: Bot,
        session: DataInteraction,
        amount: int,
        data: dict,
        payment_type: Literal['card'],
        timeout: int = 60 * 15,
        check_interval: int = 6
):
    """
    Ожидает оплаты в фоне. Завершается при оплате или по таймауту.
    """
    try:
        await asyncio.wait_for(_poll_payment(payment_id, user_id, amount, data, bot, session, payment_type, check_interval),
                                             timeout=timeout)

    except TimeoutError:
        print(f"Платёж {payment_id} истёк (таймаут)")

    except Exception as e:
        print(f"Ошибка в фоновом ожидании платежа {payment_id}: {e}")


async def _poll_payment(payment_id, user_id: int, amount: int, data: dict, bot: Bot, session: DataInteraction, payment_type: str, interval: int):
    """
    Цикл опроса статуса платежа.
    Завершается, когда платёж оплачен.
    """
    while True:
        #if payment_type == 'card':
        status = await check_robokassa_url(payment_id)
        if status:
            await bot.send_message(
                chat_id=user_id,
                text='✅Оплата прошла успешно'
            )
            await execute_rate(user_id, bot, amount, data, session)
            break
        await asyncio.sleep(interval)


async def execute_rate(user_id: int, bot: Bot, amount: int, data: dict,
                       session: DataInteraction):
    user = await session.get_user(user_id)
    text = get_form_text("@" + user.username if user.username else '-', data)
    await bot.send_photo(
        chat_id=config.bot.channel,
        photo=data.get("photo"),
        caption=text
    )
    try:
        await bot.send_message(
            chat_id=user_id,
            text='✅Ваша анкета была успешно отправлена на модерацию, '
                 'в скором времени мы выложим ее в наш канал'
        )
    except Exception:
        ...
    await session.add_income(amount)


