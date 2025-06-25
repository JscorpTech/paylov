import base64
import urllib.parse


def generate_payment_link(base_url, merchant_id, amount, account_params, return_url):
    # Create query string
    query_params = {"merchant_id": merchant_id, "amount": amount, "return_url": return_url}

    # Add account-related fields
    for key, value in account_params.items():
        query_params[f"account.{key}"] = value

    query_string = urllib.parse.urlencode(query_params)

    # Encode query string to Base64
    encoded_query = base64.b64encode(query_string.encode()).decode()

    # Combine with base URL
    payment_link = f"{base_url}{encoded_query}"

    return payment_link


# Example usage
base_url = "https://my.paylov.uz/checkout/create/"
merchant_id = "ed364cd2-313c-4842-81e4-c9d74ccfb7b8"
amount = "1"
account_params = {"order_id": "1233"}
return_url = "https://atomcom.jscorp.uz/api/paylov/"

payment_link = generate_payment_link(base_url, merchant_id, amount, account_params, return_url)
print(payment_link)
