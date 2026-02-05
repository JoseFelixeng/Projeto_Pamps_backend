#!/usr/bin/bash
set -e

PAMPS_DB=pamps_test docker-compose up -d

echo "Waiting postgres..."
until docker-compose exec -T db pg_isready -U postgres; do
  sleep 1
done

echo "Creating test database..."
docker-compose exec -T db psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname='pamps_test'" | grep -q 1 || \
docker-compose exec -T db psql -U postgres -c "CREATE DATABASE pamps_test;"

docker-compose exec api pamps reset-db -f
docker-compose exec api alembic stamp base
docker-compose exec api alembic upgrade head

docker-compose exec api pytest -v -l --tb=short --maxfail=1 tests/

docker-compose down
