import requests


with open("api_token.txt", "r") as file:
    token = file.read().strip()

# Define the API endpoint
url = "https://019sms.co.il/api"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# Define the payload
data = {
    "balance": {
        "user": {
            "username": "2you"  # Replace with your username
        },
        "type": "sms"  # Optional: Replace with "sms" if you want SMS balance, or omit if not needed
    }
}

# Send the POST request
response = requests.post(url, json=data, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    balance_data = response.json()
    print("SMS Balance:", balance_data["balance"])
else:
    print("Failed to retrieve balance:", response.status_code, response.text)
