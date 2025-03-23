import urllib.parse

# Guest list data
guests = [
    {"name": "נעם גמל", "phone": "545326558"},
    {"name": "חן אסתר", "phone": "585903528"},
    {"name": "רפאל", "phone": "549981836"},
    {"name": "משה גמל", "phone": "585903528"},
    {"name": "אמא", "phone": "542400166"}
]

# Your base URL for the form submission
base_url = "https://invite2you.com/החתונה_של_איתי_זלצמן_ושקד_רויז/"

# Generate URLs for each guest
urls = []

for guest in guests:
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
    url = base_url + "?" + urllib.parse.urlencode(params)

    # Replace '+' with '%20' for proper encoding of "Phone Number"
    url = url.replace("+", "%20")

    urls.append({"name": guest["name"], "url": url})

# Display generated URLs for each guest
for url in urls:
    print(f"Invitation for {url['name']}: {url['url']}")
