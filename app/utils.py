import secrets
import string
import requests
import os
from config import Config


def generate_random_link(length=9):
    # Define the characters to use for the link
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    # Generate a random string of the specified length
    return ''.join(secrets.choice(characters) for _ in range(length))


def send_sms(phone_number, message, sender_name=None):
    """
    Send an SMS message using the 019 SMS API
    
    Args:
        phone_number (str): The recipient's phone number
        message (str): The message content
        sender_name (str, optional): The sender name. Defaults to Config.SMS_SENDER_NAME.
    
    Returns:
        dict: The API response
    """
    if not sender_name:
        sender_name = Config.SMS_SENDER_NAME
        
    # Normalize phone number (remove leading 0 and add country code if needed)
    if phone_number.startswith('0'):
        phone_number = '972' + phone_number[1:]
    elif not phone_number.startswith('972'):
        phone_number = '972' + phone_number
        
    # API endpoint
    url = "https://019sms.co.il/api"
    
    # Request payload
    payload = {
        "token": Config.SMS_API_TOKEN,
        "msg": message,
        "to": phone_number,
        "from": sender_name
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e), "success": False}
