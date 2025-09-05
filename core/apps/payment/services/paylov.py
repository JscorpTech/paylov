import base64
import urllib.parse
from core.apps.shared.utils import get_exchange_rate
from config.env import env


def generate_payment_link(amount, order_id, currency="uzs"):
    # Create query string
    base_url = "https://my.paylov.uz/checkout/create/"
    merchant_id = env.str("PAYLOV_ID")
    return_url = "https://atomcom.framer.website/cart"

    if currency == "usd":
        amount = uzs_to_usd(amount)

    query_params = {
        "merchant_id": merchant_id,
        "amount": amount_to_tiny(amount),
        "return_url": return_url,
        "amount_in_tiyin": True,
        "currency_id": get_currency_code(currency),
    }
    query_params[f"account.order_id"] = order_id
    query_string = urllib.parse.urlencode(query_params)
    encoded_query = base64.b64encode(query_string.encode()).decode()
    payment_link = f"{base_url}{encoded_query}"

    return payment_link


def get_currency_code(currency: str) -> int:
    if currency == "uzs":
        return 860
    elif currency == "usd":
        return 840
    raise Exception("Invalid currency")


def usd_to_uzs(amount):
    return amount * get_exchange_rate()


def uzs_to_usd(amount):
    return round(amount / get_exchange_rate(), 2)


def amount_to_tiny(amount):
    return int(amount * 100)


def tiny_to_amount(tiny: int) -> float:
    return float(tiny / 100)
