import requests
import pandas as pd


# Read API token from file
with open("api_token.txt", "r") as file:
    token = file.read().strip()

# Define the API endpoint for SMS
sms_url = "https://019sms.co.il/api"

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
    if "Name" in df.columns and "Phone Number" in df.columns:
        return df[["Name", "Phone Number"]].to_dict(orient="records")
    else:
        raise ValueError("The Excel file must contain 'name' and 'phone' columns")


def send_sms(phone_number, message):
    data = {
        "sms": {
            "user": {
                "username": "2you"  # Replace with your username
            },
            "source": "0505446626",
            # "source": "invite2you",
            "destinations": {
                "phone": [
                    {"_": phone_number}
                ]
            },
            "message": message,
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
        phone_number = guest["Phone Number"]
        phone_number = str(phone_number)
        if not phone_number.startswith("0"):
            phone_number = "0" + phone_number
            # print(phone_number)

        message = """
        מתרגשים ושמחים להזמינכם לחתונה של יובל מור ועדי מרוקו.\nנודה אם תאשרו את ההזמנה בקישור הזה👇\nhttps://invite2you.com/החתונה_של_יובל_מור_ועדי_מרוקו/
        """
        message = ""
        # Send SMS with shortened link
        send_sms(phone_number, message)

        # Print the generated URL for each guest
        # print(f"Invitation for {guest['name']}: {invite_url}")


# Main flow
if __name__ == "__main__":
    # Replace with the path to your Excel file
    # excel_file = "guest_list.xlsx"
    excel_file = "didn't_answer_יובל מור ועדי מרוקו.xlsx"

    # Read the guest list from the Excel file
    guests = read_guest_list(excel_file)

    # Process each guest in the list
    process_guests(guests)
