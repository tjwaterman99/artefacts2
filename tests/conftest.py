from pytest import fixture
from artefacts.core import Manifest


@fixture
def manifest():
    return Manifest(target='dbt_projects/poffertjes_shop/target/manifest.json')
