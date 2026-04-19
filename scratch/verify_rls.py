import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Adiciona o caminho raiz
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Carrega chaves
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

print("🛡️ [VERIFICAÇÃO DE RLS - PRIVACIDADE]")

# 1. Login com Usuário A
email_a = "usuario_a@glow.com"
pass_a = "senha123456"

try:
    print(f"\n1. Criando/Logando Usuário A ({email_a})...")
    supabase.auth.sign_up({"email": email_a, "password": pass_a})
    res_a = supabase.auth.sign_in_with_password({"email": email_a, "password": pass_a})
    user_a_id = res_a.user.id
    print(f"✅ Usuário A autenticado: {user_a_id}")

    # 2. Usuário A insere um segredo
    data_a = {
        "user_id": user_a_id,
        "type": "image",
        "caption": "SEGREDO DO USUARIO A",
        "prompt": "Joia de Luxo A"
    }
    print("2. Usuário A inserindo dados...")
    supabase.table("generations").insert(data_a).execute()
    print("✅ Dados inseridos com sucesso.")

    # 3. Logout de A e Login com Usuário B
    supabase.auth.sign_out()
    email_b = "usuario_b@glow.com"
    pass_b = "senha123456"
    print(f"\n3. Criando/Logando Usuário B ({email_b})...")
    supabase.auth.sign_up({"email": email_b, "password": pass_b})
    res_b = supabase.auth.sign_in_with_password({"email": email_b, "password": pass_b})
    user_b_id = res_b.user.id
    print(f"✅ Usuário B autenticado: {user_b_id}")

    # 4. Usuário B tenta ler TODOS os dados
    print("4. Usuário B tentando ler dados da tabela 'generations'...")
    res_query = supabase.table("generations").select("*").execute()
    
    found_a = any(item['caption'] == "SEGREDO DO USUARIO A" for item in res_query.data)
    
    if not found_a:
        print("\n🔒 [SUCESSO] RLS ESTÁ ATIVO!")
        print("   O Usuário B não conseguiu enxergar os dados do Usuário A.")
    else:
        print("\n⚠️ [ALERTA] RLS FALHOU!")
        print("   O Usuário B conseguiu ler dados privados do Usuário A.")

except Exception as e:
    print(f"❌ Erro durante o teste: {e}")
finally:
    supabase.auth.sign_out()
