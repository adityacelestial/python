import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def sign_up(email: str, password: str):
    """Create a new user in Supabase Auth."""
    response = supabase.auth.sign_up({"email": email, "password": password})
    return response


def sign_in(email: str, password: str):
    """Authenticate a user and return session/token info."""
    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
    return response


def get_user(access_token: str):
    """Get current user from Supabase using access token."""
    response = supabase.auth.get_user(access_token)
    return response
