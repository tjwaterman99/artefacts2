from pytest import fixture
from pytest import mark
from artefacts.core import Manifest


@fixture
def manifest():
    return Manifest(target='dbt_projects/poffertjes_shop/target/manifest.json')


def test_manifest_init_cache(manifest):
    assert manifest._cache == {}


def test_manifest_nodes(manifest):
    assert len(manifest._nodes) > 0
    assert '_nodes' in manifest._cache


def test_manifest_models(manifest):
    assert len(manifest.models) > 0


def test_manifest_tests(manifest):
    assert len(manifest.tests) > 0


def test_manifest_sources(manifest):
    assert len(manifest.sources) > 0


def test_manifest_sources(manifest):
    assert len(manifest.sources) > 0


def test_manifest_macros(manifest):
    assert len(manifest.macros) > 0


def test_manifest_exposures(manifest):
    assert len(manifest.exposures) > 0


def test_manifest_metrics(manifest):
    assert len(manifest.metrics) > 0


def test_model_parent_map(manifest):
    models_with_parents = [m for m in manifest.models.values() if len(m.parents) > 0]
    assert len(models_with_parents) > 0


def test_model_child_map(manifest):
    models_with_children = [m for m in manifest.models.values() if len(m.children) > 0]
    assert len(models_with_children) > 0
