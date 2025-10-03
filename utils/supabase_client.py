import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_supabase_client() -> Client:
    url = os.getenv('VITE_SUPABASE_URL')
    key = os.getenv('VITE_SUPABASE_SUPABASE_ANON_KEY')

    if not url or not key:
        raise ValueError('Supabase credentials not found in environment variables')

    return create_client(url, key)

supabase = get_supabase_client()
