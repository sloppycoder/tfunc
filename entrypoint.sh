#!/bin/sh

cd "$(dirname "$0")"

if [ "$DATABASE_URL" = "" && -f [ "/secrets/database_url" ] ]; then
    export DATABASE_URL=$(cat /secrets/database_url)
fi

if [ "$DATABASE_URL" = "" ]; then
    echo DATABASE_URL not set, aborting.
    exit 1
fi

if [ "$RUN_MIGRATE" = "Y" ]; then
    # Check for pending migrations
    current_migration=$(alembic current | awk '{print $1}')
    latest_migration=$(alembic heads | awk '{print $1}')

    if [ "$current_migration" != "$latest_migration" ]; then
        echo "Running migrations before starting app"
        alembic upgrade head
    fi
fi
uvicorn main:app --host 0.0.0.0 --port 8000 --workers ${WORKERS:-1}
