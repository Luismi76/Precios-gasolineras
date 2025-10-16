# ========= Base común =========
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PATH="/home/appuser/.local/bin:${PATH}"
WORKDIR /app

# Paquetes de sistema mínimos (builder y/o runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gcc libpq-dev curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ========= Builder: genera la wheel del proyecto =========
FROM base AS builder
# Copiamos sólo metadata primero para cachear deps cuando no cambian
COPY pyproject.toml /app/
# Copiamos el código del paquete
COPY app /app/app

# Construye wheels del proyecto **y** de sus dependencias
RUN python -m pip install --upgrade pip \
 && pip wheel --wheel-dir=/wheels /app

# ========= Runtime: imagen final ligera =========
FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PORT=8000

WORKDIR /app

# Usuario no root
RUN useradd -m -u 10001 appuser
USER appuser

# Traemos sólo las wheels
COPY --from=builder /wheels /wheels
RUN pip install --no-index --find-links=/wheels /wheels/*

# (Opcional) copiar ejemplo de entorno para referencia
COPY .env.example /app/.env.example

# Puerto lógico (recuerda: con --network host no es necesario EXPOSE, pero no molesta)
EXPOSE 8000

# Healthcheck contra tu endpoint /healthz
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD \
  python -c "import urllib.request,urllib.error,sys; \
url='http://127.0.0.1:8000/healthz'; \
try: \
    r=urllib.request.urlopen(url,timeout=2); \
    sys.exit(0 if r.status==200 else 1); \
except Exception: \
    sys.exit(1)"
# Comando por defecto: uvicorn
# (si tu main se llama app/main.py y expone FastAPI en `app`)
CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
