import requests


# Load the token from the file
def load_token(filename="api_token.txt"):
    with open(filename, "r") as file:
        return file.read().strip()


# Verify phone numbers
def verify_phones():
    token = load_token()

    url = "https://019sms.co.il/api"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "verify_phone": {
            "user": {"username": "2you"},  # Replace with your username
            "phone": [
                "584442400",  # Replace with the phone number you want to verify
                "559744633"  # Replace with another phone number you want to verify
            ]
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Phone numbers verified successfully")
    else:
        print("Failed to verify phone numbers:", response.status_code, response.text)


verify_phones()
