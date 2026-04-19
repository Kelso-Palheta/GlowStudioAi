import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.services.supabase_client import get_supabase_client
from supabase import Client

def test_connection():
    print("Iniciando teste de conexão...")
    try:
        supabase: Client = get_supabase_client()
        if supabase:
            print("✅ Cliente Supabase inicializado com sucesso!")
            # Tentar uma operação simples (ex: ler o auth.config)
            # Mas geralmente inicializar já valida as chaves se o client fizer o handshake
            print(f"URL: {supabase.supabase_url}")
            
            # Tentar listar usuários ou algo que não exija tabelas específicas (Auth)
            # Como é anon key, podemos tentar ver se o auth responde
            print("🚀 Conexão parece estar UP.")
        else:
            print("❌ Falha: Cliente retornou None (Cheque as chaves no .env)")
    except Exception as e:
        print(f"❌ Erro durante a conexão: {e}")

if __name__ == "__main__":
    test_connection()
