.PHONY: help install dev run test clean docker-up docker-down db-init etl

help:
	@echo "Comandos disponibles:"
	@echo "  make install    - Instalar dependencias"
	@echo "  make dev        - Ejecutar en modo desarrollo"
	@echo "  make run        - Ejecutar en modo producción"
	@echo "  make test       - Ejecutar tests"
	@echo "  make clean      - Limpiar archivos temporales"
	@echo "  make docker-up  - Levantar servicios con Docker"
	@echo "  make docker-down - Detener servicios Docker"
	@echo "  make db-init    - Inicializar base de datos"
	@echo "  make etl        - Ejecutar proceso ETL completo"

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --port 8000

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

test:
	python -m pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf data/raw/*.json

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

db-init:
	python -m app.cli init-db

etl:
	python -m app.cli etl

fetch:
	python -m app.cli fetch

load:
	python -m app.cli load

validate:
	python -m app.cli validate