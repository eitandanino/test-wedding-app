import requests
import urllib.parse
import pandas as pd


# Read API token from file
with open("api_token.txt", "r") as file:
    token = file.read().strip()

# Define the API endpoint for SMS
sms_url = "https://019sms.co.il/api/test"
# sms_url = "https://019sms.co.il/api"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}


# Read guest list from Excel file
def read_guest_list(filename):
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(filename, dtype={"phone": str})

    # Ensure that the columns "name" and "phone" exist
    if "name" in df.columns and "phone" in df.columns:
        return df[["name", "phone"]].to_dict(orient="records")
    else:
        raise ValueError("The Excel file must contain 'name' and 'phone' columns")


# Your base URL for the form submission
base_url = "https://invite2you.com/החתונה_של_איתי_זלצמן_ושקד_רויז/"


def send_sms(phone_number, message, invite_url):
    # Define the data payload including the link to shorten
    data = {
        "sms": {
            "user": {
                "username": "2you"  # Replace with your username
            },
            "source": "invite2you",
            "destinations": {
                "phone": [
                    {"_": phone_number}
                ]
            },
            "message": message.replace("[link-id]", "[link-a1]"),  # Placeholder for the shortened link
            "links": {
                "link": [
                    {"$": {
                        "id": "a1",
                    },
                        "_": invite_url   # The actual invite link to be shortened
                    }
                ]
            }
        }
    }

    # Send the POST request
    response = requests.post(sms_url, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        sms_data = response.json()
        print("SMS Sent to", phone_number, ":", sms_data)
        # Print out the response to check for shortened link details
        # print("API Response:", sms_data)
    else:
        print(f"Failed to send SMS to {phone_number}:", response.status_code, response.text)


# Generate URLs and send SMS for each guest
def process_guests(guest_list):
    for guest in guest_list:
        # Ensure phone number starts with 0
        phone_number = guest["phone"]
        if not phone_number.startswith("0"):
            phone_number = "0" + phone_number

        # Encode the name and phone for the URL
        params = {
            "Name": guest["name"],
            "Phone Number": phone_number,
        }

        # Construct the full URL with query parameters
        invite_url = base_url + "?" + urllib.parse.urlencode(params)

        # Replace '+' with '%20' for proper encoding of "Phone Number"
        invite_url = invite_url.replace("+", "%20")

        # Prepare the SMS message with a placeholder for the shortened link
        message = f"שלום {guest['name']}, הנך מוזמן לחתונה! הכנס ללינק לצפייה בפרטים נוספים: [link-id] "

        # Send SMS with shortened link
        send_sms(phone_number, message, invite_url)

        # Print the generated URL for each guest
        # print(f"Invitation for {guest['name']}: {invite_url}")


# Main flow
if __name__ == "__main__":
    # Replace with the path to your Excel file
    excel_file = "guest_list.xlsx"

    # Read the guest list from the Excel file
    guests = read_guest_list(excel_file)

    # Process each guest in the list
    process_guests(guests)
