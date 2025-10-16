#!/usr/bin/env bash
set -euo pipefail

timestamp=$(date +%Y%m%d%H%M)
backup_dir="backup_${timestamp}"

echo "🗃️  Creando copia de seguridad en: $backup_dir"
mkdir -p "$backup_dir"
rsync -a . "$backup_dir" --exclude "$backup_dir"

echo "✅ Copia de seguridad completa."

# ==============================
# 1. Consolidar paquete 'app'
# ==============================

echo "📦 Consolidando estructura del paquete app/ ..."

# Si existe backend/app/, fusionar routers útiles
if [ -d "backend/app/routers" ]; then
  mkdir -p app/routers
  rsync -a backend/app/routers/ app/routers/ --ignore-existing
  echo "   → Routers de backend/app/ fusionados en app/routers/"
fi

# Fusionar posibles services
if [ -d "backend/app/services" ]; then
  mkdir -p app/services
  rsync -a backend/app/services/ app/services/ --ignore-existing
  echo "   → Services de backend/app/ fusionados en app/services/"
fi

# Fusionar posibles core
if [ -d "backend/app/core" ]; then
  mkdir -p app/core
  rsync -a backend/app/core/ app/core/ --ignore-existing
  echo "   → Core de backend/app/ fusionado en app/core/"
fi

# Fusionar posibles SQL o utils
if [ -d "backend/app/sql" ]; then
  mkdir -p app/sql
  rsync -a backend/app/sql/ app/sql/ --ignore-existing
  echo "   → SQL de backend/app/ fusionado en app/sql/"
fi

# Eliminar carpeta fantasma app/app/
if [ -d "app/app" ]; then
  echo "🧹 Eliminando duplicado app/app/"
  rsync -a app/app/ app/ --ignore-existing
  rm -rf app/app
fi

# ==============================
# 2. Eliminar duplicados obvios (solo si ya se han copiado)
# ==============================
echo "🧩 Eliminando duplicados residuales en backend/"
if [ -d "backend" ]; then
  rm -rf backend
fi

# ==============================
# 3. Crear subcarpetas básicas si faltan
# ==============================
mkdir -p app/{routers,services,core,data}
touch app/__init__.py app/routers/__init__.py app/services/__init__.py app/core/__init__.py

# ==============================
# 4. Limpiar artefactos no versionables
# ==============================
echo "🧹 Añadiendo reglas básicas a .gitignore"
cat > .gitignore <<'EOF'
# Entornos y dependencias
.venv/
__pycache__/
*.pyc
*.pyo
*.egg-info/
node_modules/

# Datos y salidas
data/raw/
*.log
*.sqlite
.env
EOF

# ==============================
# 5. Recordatorio final
# ==============================
echo "✅ Reorganización completada."
echo "📁 Estructura esperada:"
echo "
app/
├── core/
├── routers/
├── services/
├── db.py
├── main.py
└── models.py
"
echo "Se creó una copia de seguridad completa en: $backup_dir"
