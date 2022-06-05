## artefacts

A set of python utilities to help write scripts that build on top of dbt's artifacts.

### Install

```
pip install artefacts
```

### Development Set Up

Install with poetry

```
poetry install
```

Build the dbt example project.

```
poetry run dbt build --project-dir dbt_projects/poffertjes_shop --profiles-dir dbt_projects
```

Run the test suite.

```
poetry run pytest
```