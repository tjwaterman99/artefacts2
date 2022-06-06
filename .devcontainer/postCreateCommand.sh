#!/bin/bash

# This command is ran during the devcontainer's `postCreateCommand` step
# every time the container is built.

# Set up postgres db
sudo service postgresql start
sudo -u postgres psql -c "create user $PGUSER with password '$PGPASSWORD'"
sudo -u postgres createdb $PGDATABASE -O $PGUSER

# Install dependencies
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry install

# Build dbt test project
git submodule update --init --recursive
poetry run dbt deps --project-dir dbt_projects/poffertjes_shop
poetry run dbt build --project-dir dbt_projects/poffertjes_shop
poetry run dbt docs generate --project-dir dbt_projects/poffertjes_shop
poetry run dbt source freshness --project-dir dbt_projects/poffertjes_shop
