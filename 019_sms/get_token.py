import requests

# Define the API endpoint
url = "https://019sms.co.il/api"

# Define the headers
headers = {
    "Content-Type": "application/json"
}

# Define the payload
data = {
    "getApiToken": {
        "user": {
            "username": "2you",  # Replace with your admin username
            "password": "Tantan123@"   # Replace with your admin password
        },
        "username": "2you",   # Replace with the username for which you want to generate a token
        # "action": "new"  # Use "current" if you want the existing token
        "action": "current"  # Use "current" if you want the existing token
    }
}

# Send the POST request
response = requests.post(url, json=data, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    token_data = response.json()

    # # Save the token to a file
    # with open("api_token.txt", "w") as file:  # You can also use .json or other file formats
    #     file.write(token_data["message"])

    print("API Token:", token_data["message"])
    print("Expiration Date:", token_data["expiration_date"])
else:
    print("Failed to generate token:", response.status_code, response.text)


# eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJmaXJzdF9rZXkiOiI2NzUxOSIsInNlY29uZF9rZXkiOiIzNjk0Njc1IiwiaXNzdWVkQXQiOiIxOC0wOC0yMDI0IDA4OjI3OjM2IiwidHRsIjo2MzA3MjAwMH0.6liDDCDA52aOcxB-OGfOj8U_KWWjkc83zlBMbuIrkoU