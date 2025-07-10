import base64
import urllib.parse


def generate_payment_link(amount, order_id):
    # Create query string
    base_url = "https://my.paylov.uz/checkout/create/"
    merchant_id = "ed364cd2-313c-4842-81e4-c9d74ccfb7b8"
    return_url = "https://atomcom.framer.website/cart"

    query_params = {"merchant_id": merchant_id, "amount": amount, "return_url": return_url}
    query_params[f"account.order_id"] = order_id
    query_string = urllib.parse.urlencode(query_params)
    encoded_query = base64.b64encode(query_string.encode()).decode()
    payment_link = f"{base_url}{encoded_query}"

    return payment_link
