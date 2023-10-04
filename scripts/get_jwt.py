import os

import supabase_py
from dotenv import load_dotenv

load_dotenv()

# Load email and password from environment variables
email = os.environ["SUPABASE_TEST_EMAIL"]
password = os.environ["SUPABASE_TEST_PW"]

# Initialize the Supabase client
url = os.environ["SUPABASE_URL"]
supabase_key = os.environ["SUPABASE_KEY"]
supabase = supabase_py.create_client(url, supabase_key)


def get_jwt():
    # Authenticate the user
    result = supabase.auth.sign_in(email=email, password=password)

    # Check for an error
    if result.get("error"):
        print(f'Error: {result.get("error", {}).get("message", "")}')
    else:
        # Print the JWT to the terminal
        print(result.get("access_token", ""))


# Run the async function


get_jwt()
