# 🧪 Guia: Ambiente de Laboratório Local (Docker)

Siga este guia para rodar o **GlowStudio AI** e o **n8n** juntos no seu computador. Isso permite que você desenvolva a integração com IA sem custos de hospedagem.

## 🛠️ Pré-requisitos
1. **Docker Desktop:** Deve estar instalado e rodando. [Baixar aqui](https://www.docker.com/products/docker-desktop/).
2. **Terminal:** Ter o terminal aberto na pasta raiz do projeto.

---

## 🚀 Como Inicializar

Para subir o aplicativo e o orquestrador, execute o comando abaixo:

```bash
docker-compose up -d
```

### O que este comando faz?
- Sobe o **Streamlit** em `http://localhost:8501`
- Sobe o **n8n** em `http://localhost:5678`
- Configura um **Nginx** local (opcional)

---

## ⚙️ Configurando o n8n pela primeira vez

1. Acesse `http://localhost:5678`.
2. Siga os passos na tela para criar sua conta de administrador local.
3. Clique em **"Workflows"** -> **"Add Workflow"**.
4. Crie seus nós de **Webhook** seguindo os contratos definidos em `docs/api_contracts.md`.

### Dica Skill 5 (Persistência):
Seus dados do n8n (workflows e credenciais) ficam salvos na pasta `./n8n_data` no seu computador. Se você apagar o container, os dados **não** serão perdidos.

---

## 🛑 Como Parar

Para desligar o laboratório:

```bash
docker-compose down
```

---

## 🔍 Troubleshooting (Resolução de Problemas)

- **Porta ocupada:** Se o erro disser que a porta 5678 está em uso, verifique se você não tem outra instância do n8n rodando.
- **Erro de Memória:** Certifique-se de que o Docker Desktop tem pelo menos 4GB de RAM alocados nas configurações.
