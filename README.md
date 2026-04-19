# 💎 GlowStudio AI

> Plataforma SaaS para semijoias — Transforme fotos de peças reais em conteúdo profissional com Inteligência Artificial.

## 🚀 O que é

O **GlowStudio AI** permite que lojistas de semijoias:

1. 📸 Façam upload de fotos das suas peças
2. 🤖 Gerem modelos virtuais fotorrealistas vestindo as peças
3. ✍️ Recebam legendas estratégicas de vendas
4. 🎬 Criem vídeos animados para redes sociais

## 📋 Documentação

O documento oficial do projeto está em [`GlowStudio_AI_Master.md`](./GlowStudio_AI_Master.md) — PRD completo com Skills, Stack Técnica, Roadmap e Design Tokens.

## 🛠️ Como Rodar Localmente

### Pré-requisitos

- Python 3.12+
- pip

### Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd "GlowStudio AI"

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas chaves de API

# 5. Rode o aplicativo
streamlit run src/app.py
```

O app estará disponível em `http://localhost:8501`.

### Com Docker

```bash
# Build e run
docker compose up --build

# Acessar em http://localhost (porta 80 via Nginx)
```

## 📁 Estrutura do Projeto

```
GlowStudio AI/
├── src/
│   ├── app.py                  # Entry point
│   ├── pages/                  # Telas do Streamlit
│   │   ├── 01_configuracao.py  # Upload + Estratégia
│   │   ├── 02_edicao.py        # Edição de textos
│   │   └── 03_estudio.py       # Galeria + Downloads
│   ├── services/               # Lógica de negócio
│   ├── config/                 # Settings e theme
│   ├── utils/                  # Logger, validators
│   └── components/             # UI reutilizável
├── assets/css/                 # Estilos customizados
├── .streamlit/config.toml      # Tema Streamlit
├── Dockerfile                  # Build Docker
├── docker-compose.yml          # Orquestração
├── nginx.conf                  # Proxy reverso
├── requirements.txt            # Dependências Python
└── GlowStudio_AI_Master.md     # PRD oficial
```

## 🔒 Segurança

- Somente bibliotecas aprovadas no Documento Mestre
- Container Docker com non-root user
- Nginx com rate limiting e security headers
- API keys em `.env` (nunca versionadas)

## 📄 Licença

Proprietário — Todos os direitos reservados.
