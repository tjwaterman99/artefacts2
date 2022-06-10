#!/bin/bash

# This command is ran during the devcontainer's `postCreateCommand` step
# every time the container is built.

# Set up postgres db
sudo service postgresql start
sudo -u postgres psql -c "create user $PGUSER with password '$PGPASSWORD'"
sudo -u postgres createdb $PGDATABASE -O $PGUSER

# Install dependencies
pip install -r requirements.txt

# Build dbt test project
git submodule update --init --recursive
dbt deps --project-dir dbt_projects/poffertjes_shop
dbt build --project-dir dbt_projects/poffertjes_shop
dbt docs generate --project-dir dbt_projects/poffertjes_shop
dbt source freshness --project-dir dbt_projects/poffertjes_shop
