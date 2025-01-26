#!/bin/sh

# Apply migrations if the alembic directory exists
if [ -d alembic ]; then
    reflex db migrate
fi

# Start Caddy server
caddy start &

# Start Reflex backend
reflex run --env prod --backend-only --loglevel debug
