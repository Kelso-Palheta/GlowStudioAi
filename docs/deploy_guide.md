# GlowStudio AI — Guia de Deploy na Hetzner

> **Skill 5: Infraestrutura e DevOps**  
> Este guia cobre o deploy completo do GlowStudio AI na Hetzner com Docker, Nginx e SSL.

---

## 1. Pré-Requisitos

- Conta na [Hetzner Cloud](https://hetzner.cloud)
- Domínio apontando para o IP da VPS (ex: `glowstudio.seudominio.com`)
- SSH key configurada

## 2. Criação da VPS

```bash
# Recomendação mínima: CPX31 (4 vCPU, 8GB RAM)
# Sistema: Ubuntu 22.04
# Datacenter: Nuremberg (nbg1) ou Falkenstein (fsn1)
```

## 3. Setup Inicial do Servidor

```bash
# Conectar via SSH
ssh root@SEU_IP_HETZNER

# Atualizar sistema
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com | sh

# Instalar Docker Compose
apt install docker-compose-plugin -y

# Verificar
docker --version
docker compose version
```

## 4. Deploy do Projeto

```bash
# Clonar o repositório (ou enviar via rsync)
git clone https://seu-repositorio/glowstudio-ai.git /opt/glowstudio
cd /opt/glowstudio

# Criar arquivo .env a partir do template
cp .env.example .env
nano .env   # Preencher com as chaves reais
```

### 4.1 Configuração do `.env` (Produção)

```env
APP_ENV=production
APP_DEBUG=false
APP_SECRET_KEY=<gerar com: python -c "import secrets; print(secrets.token_hex(32))">

N8N_BASE_URL=http://seu-n8n:5678
N8N_WEBHOOK_TEXT=https://seu-n8n.com/webhook/maritaca
N8N_WEBHOOK_IMAGE=https://seu-n8n.com/webhook/fal-ai
N8N_WEBHOOK_VIDEO=https://seu-n8n.com/webhook/kling
N8N_API_KEY=sua_chave

MARITACA_API_KEY=sua_chave_maritaca
FAL_API_KEY=sua_chave_fal
```

## 5. Build e Start

```bash
# Build e iniciar em modo detached
docker compose up --build -d

# Verificar logs
docker compose logs -f app

# Verificar health
docker compose ps
```

## 6. Ativação do SSL (Certbot)

```bash
# O docker-compose.yml já inclui o Certbot.
# Substitua o domínio no nginx.conf:
sed -i 's/glowstudio.seudominio.com/SEU_DOMINIO_REAL/g' nginx.conf

# Executar certbot manualmente na primeira vez:
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    -d SEU_DOMINIO_REAL \
    --email seu@email.com \
    --agree-tos \
    --no-eff-email

# Reiniciar nginx para carregar o certificado
docker compose restart nginx
```

## 7. Manutenção

### Renovação automática do SSL
```bash
# Adicionar ao crontab (root):
0 0 1 * * docker compose -f /opt/glowstudio/docker-compose.yml run --rm certbot renew && docker compose -f /opt/glowstudio/docker-compose.yml restart nginx
```

### Atualização do app
```bash
cd /opt/glowstudio
git pull
docker compose up --build -d
```

### Backup
```bash
# Backup das configurações
tar -czf /backup/glowstudio-$(date +%Y%m%d).tar.gz /opt/glowstudio/.env /opt/glowstudio/nginx.conf
```

## 8. Troubleshooting

| Sintoma | Causa Provável | Solução |
|---------|---------------|---------|
| Erro 502 Bad Gateway | App não subiu | `docker compose logs app` |
| Timeout na geração | n8n lento | Aumentar `N8N_TIMEOUT_SECONDS` no `.env` |
| SSL não funciona | Certificado não gerado | Re-executar certbot (passo 6) |
| Porta bloqueada | Firewall | `ufw allow 80,443/tcp` |

---

*Documento Skill 5 — GlowStudio AI, Abril 2026.*
