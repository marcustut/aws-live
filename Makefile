DB_MIGRATIONS_DIR="./db/migrations"
DB_SCHEMA_FILE="./db/schema.sql"

# Load env from .env
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Connect to db through mycli
mycli:
	mycli $(DATABASE_URL)

# Create a new migration
migrate-new:
	dbmate -u $(DATABASE_URL) -d $(DB_MIGRATIONS_DIR) -s $(DB_SCHEMA_FILE) new $(NAME)

# Apply latest migration
migrate-up:
	dbmate -u $(DATABASE_URL) -d $(DB_MIGRATIONS_DIR) -s $(DB_SCHEMA_FILE) up

# Rollback latest migration
migrate-down:
	dbmate -u $(DATABASE_URL) -d $(DB_MIGRATIONS_DIR) -s $(DB_SCHEMA_FILE) down

# Check migration status
migrate-status:
	dbmate -u $(DATABASE_URL) -d $(DB_MIGRATIONS_DIR) -s $(DB_SCHEMA_FILE) status

dev:
	python app.py

prod:
	APP_ENV=production python app.py