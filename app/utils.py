import secrets
import string


def generate_random_link(length=9):
    # Define the characters to use for the link
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    # Generate a random string of the specified length
    return ''.join(secrets.choice(characters) for _ in range(length))
