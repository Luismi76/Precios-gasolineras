# API Precio Gasolineras España 🚗⛽

API REST para consultar precios actuales e históricos de combustibles en estaciones de servicio de España.

## 🚀 Características

- ✅ Búsqueda de estaciones por provincia y tipo de combustible
- ✅ Ranking de precios más baratos (nacional/provincial)
- ✅ Histórico de precios por estación
- ✅ ETL automático desde API del Ministerio
- ✅ Base de datos PostgreSQL optimizada
- ✅ API REST con FastAPI
- ✅ Documentación automática (Swagger/OpenAPI)

## 📋 Requisitos

- Python 3.11+
- PostgreSQL 15+
- Docker y Docker Compose (opcional)

## 🔧 Instalación

### Opción 1: Con Docker (Recomendado)

1. Clonar el repositorio:
```bash
git clone https://github.com/tuusuario/precio-gasolineras.git
cd precio-gasolineras
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus valores
```

3. Levantar servicios:
```bash
make docker-up
# o directamente:
docker-compose up -d
```

4. Inicializar base de datos y cargar datos:
```bash
# Inicializar esquema
docker exec gasolineras-api python -m app.cli init-db

# Ejecutar ETL completo
docker exec gasolineras-api python -m app.cli etl
```

### Opción 2: Instalación Local

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
make install
# o directamente:
pip install -r requirements.txt
```

3. Configurar PostgreSQL y variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus valores de conexión a PostgreSQL
```

4. Inicializar base de datos:
```bash
make db-init
```

5. Cargar datos:
```bash
make etl
```

6. Ejecutar API:
```bash
make dev  # Modo desarrollo con recarga automática
# o
make run  # Modo producción
```

## 📡 Uso de la API

La API estará disponible en `http://localhost:8000`

### Documentación interactiva
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints principales

#### Buscar estaciones
```bash
GET /api/search?fuel_type=GOA&provincia=Madrid&limit=10
```

#### Obtener detalle de estación
```bash
GET /api/station/12345
```

#### Ranking de precios
```bash
GET /api/ranking?scope=nacional&fuel_type=G95_E5&limit=20
GET /api/ranking?scope=provincia:Barcelona&fuel_type=GOA
```

#### Histórico de precios
```bash
GET /api/history/station/12345?fuel_type=GOA&desde=2024-01-01
```

#### Listas de referencia
```bash
GET /api/products     # Lista de combustibles
GET /api/provinces    # Lista de provincias
```

## 🔄 Proceso ETL

El CLI incluye comandos para gestionar el proceso ETL:

```bash
# ETL completo (descarga + carga + validación)
python -m app.cli etl

# Comandos individuales
python -m app.cli fetch     # Descargar datos
python -m app.cli load      # Cargar en BD
python -m app.cli validate  # Validar datos
```

### Automatización con Cron

Para actualizar datos diariamente, añadir a crontab:

```bash
# Ejecutar ETL todos los días a las 6:00 AM
0 6 * * * cd /ruta/al/proyecto && /usr/local/bin/python -m app.cli etl >> /var/log/gasolineras-etl.log 2>&1
```

## 🗄️ Estructura de la Base de Datos

### Tablas principales

- `stations`: Información de estaciones de servicio
- `prices_daily`: Precios diarios por estación y combustible
- `ref_producto`: Catálogo de tipos de combustible
- `ref_provincia`: Catálogo de provincias

## 🧪 Tests

```bash
# Ejecutar todos los tests
make test

# Con coverage
pytest --cov=app tests/
```

## 📊 Monitoreo

### Health checks
- `GET /healthz` - Check básico
- `GET /health/detailed` - Check detallado con estado de BD

## 🚀 Despliegue en Producción

### Con Docker

1. Ajustar `docker-compose.yml` para producción:
   - Quitar volumen de código en el servicio API
   - Configurar variables de entorno seguras
   - Añadir reverse proxy (nginx)

2. Usar Docker Swarm o Kubernetes para orquestación

### Sin Docker

1. Instalar como servicio systemd
2. Configurar Nginx/Apache como reverse proxy
3. Usar Gunicorn como servidor WSGI

## 📝 Licencia

MIT

## 👥 Contribuir

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📧 Contacto

Tu Nombre - [@tutwitter](https://twitter.com/tutwitter) - email@ejemplo.com

Proyecto: [https://github.com/tuusuario/precio-gasolineras](https://github.com/tuusuario/precio-gasolineras)
