# Fila Certa — imagem única: builda o PWA e serve tudo pelo FastAPI.
# Alvo: Hugging Face Spaces (SDK docker, porta 7860).

# --- estágio 1: build do frontend ---
FROM node:22-slim AS frontend
WORKDIR /build
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build          # gera /build/dist

# --- estágio 2: runtime ---
FROM python:3.11-slim

# HF Spaces roda com uid 1000; criar o usuário antes de qualquer COPY evita
# problema de permissão e o chown recursivo que incha a imagem.
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1
WORKDIR $HOME/app

COPY --chown=user backend/pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .

COPY --chown=user backend/src ./src
COPY --chown=user --from=frontend /build/dist ./static

# Storage do Space é efêmero: o banco da demo é semeado a cada boot.
ENV FILA_CERTA_DB_PATH=/tmp/fila_certa.duckdb \
    FILA_CERTA_STATIC_DIR=/home/user/app/static

EXPOSE 7860
CMD ["uvicorn", "fila_certa.main:app", "--host", "0.0.0.0", "--port", "7860"]
