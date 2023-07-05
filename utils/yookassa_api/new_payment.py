import asyncio
import json
import uuid

from yookassa import Payment

from logs.log_all import log_all


async def create_new_payment(price, subscription_name, email):
    new_payment = Payment.create({
            "amount": {
                "value": f"{price}.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/chatgpt_davinci_aibot"
            },
            "capture": True,
            "description": subscription_name,
            "receipt": {
                "customer": {
                    "email": email
                },
                "items": [
                    {
                        "description": subscription_name,
                        "quantity": "1",
                        "amount": {
                            "value": f"{price}.00",
                            "currency": "RUB"
                        },
                        "vat_code": "1"
                    }
                ]
            }
        }, uuid.uuid4())
    payment_data = json.loads(new_payment.json())
    return payment_data


async def check_payment_status(payment_data, user):
    try:
        payment = json.loads((Payment.find_one(payment_data["id"])).json())
        while payment["status"] == "pending":
            payment = json.loads((Payment.find_one(payment_data["id"])).json())
            await asyncio.sleep(1)
        if payment["status"] == "succeeded":
            return True
        return False
    except Exception as error:
        await log_all('check_payment_status', 'error', user.user_id, user.firstname, error)
