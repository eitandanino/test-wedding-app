import requests

with open("api_token.txt", "r") as file:
    token = file.read().strip()

# Define the API endpoint
url = "https://019sms.co.il/api"
# url = "https://019sms.co.il/api/test"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# Define the payload
data = {
    "sms": {
        "user": {
            "username": "2you"  # Replace with your username
        },
        # "source": "0584442400",
        "source": "0505446626",
        # "source": "invite2you",
        "destinations": {
            "phone": [
                # {"_": "585903528"},
                {"_": "584442400"},
            ]
        },
        "message": "אני אוהב אותך יפה קטנה שלי ❤️",
    }
}

# Send the POST request
response = requests.post(url, json=data, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    sms_data = response.json()
    print("SMS Sent:", sms_data)
else:
    print("Failed to retrieve balance:", response.status_code, response.text)
