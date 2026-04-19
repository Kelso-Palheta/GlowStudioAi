import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

print("Tentando criar um usuário de teste direto na API...")
try:
    res = supabase.auth.sign_up({"email": "testando_agora@glow.com", "password": "senha123456"})
    print("Sign up response:", res)
except Exception as e:
    print("Erro no Sign Up:", e)

print("\nTentando fazer login...")
try:
    res_login = supabase.auth.sign_in_with_password({"email": "testando_agora@glow.com", "password": "senha123456"})
    print("Sign in response:", res_login is not None)
    print("Logado com sucesso! Token obtido.")
except Exception as e:
    print("Erro no Sign In:", e)
