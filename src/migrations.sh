#!/usr/bin/env bash

if [ ! -d "/short-url/src/migrations" ]; then
    flask db init
else
    # Check if dir of versions is empty
    if [ $(ls -A  /short-url/src/migrations/versions | wc -l) -ne 0 ]; then
        echo "Dir of versions is not empty applying stamp head..."
        flask db stamp head
    else
        echo "Dir of versions is empty..."
    fi
    # Run Scan of migrations and apply migrations if then exist
    flask db migrate
    flask db upgrade
fi
