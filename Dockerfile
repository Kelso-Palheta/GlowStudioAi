# ============================================
# GlowStudio AI - Dockerfile
# ============================================
# Multi-stage build | Python 3.12 | Non-root user
# Segue Skill 5 (DevOps) do Documento Mestre

# --- Stage 1: Builder ---
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Stage 2: Runtime ---
FROM python:3.12-slim AS runtime

# Metadados
LABEL maintainer="GlowStudio AI Team"
LABEL description="GlowStudio AI - Plataforma SaaS para semijoias com IA"
LABEL version="1.0.0"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Criar usuário não-root (segurança)
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Copiar dependências instaladas do builder
COPY --from=builder /install /usr/local

# Diretório da aplicação
WORKDIR /app

# Copiar código-fonte
COPY --chown=appuser:appuser .streamlit/ .streamlit/
COPY --chown=appuser:appuser src/ src/
COPY --chown=appuser:appuser assets/ assets/

# Trocar para usuário não-root
USER appuser

# Expor porta do Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# Iniciar aplicação
ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.address=0.0.0.0", \
    "--server.port=8501"]
