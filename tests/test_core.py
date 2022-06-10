from pytest import fixture
from pytest import mark
from artefacts.core import Manifest, NodeId


@fixture
def manifest():
    return Manifest(target='dbt_projects/poffertjes_shop/target/manifest.json')


def test_node_id_str():
    name = 'test'
    node_id = NodeId(node_id=name)
    assert str(node_id) == name


def test_node_id_repr():
    name = 'test'
    node_id = NodeId(node_id=name)
    assert repr(node_id) == name


def test_node_id_eq():
    name = 'test'
    node_id = NodeId(node_id=name)
    assert node_id == name
    
    other_node_id = NodeId(node_id=name)
    assert node_id == other_node_id


def test_node_id_hash():
    name = 'test'
    node_id = NodeId(node_id=name)
    assert hash(node_id) == hash(node_id.node_id)

    d = {node_id: 'value'}
    assert name in d


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


def test_manifest_parent_map(manifest):
    assert len(manifest.parent_map) > 0
    
    for model_id, model in manifest.models.items():
        assert model.unique_id in manifest.parent_map
        assert model_id in manifest.parent_map
        assert manifest.parent_map[model_id] is not None

    for model_id in manifest.models:
        if len(manifest.parent_map[model_id]) > 0:
            break
    else:
        raise Exception("No models with parents found.")


def test_manifest_child_map(manifest):
    assert len(manifest.child_map) > 0
    
    for model_id, model in manifest.models.items():
        assert model.unique_id in manifest.child_map
        assert model_id in manifest.child_map
        assert manifest.child_map[model_id] is not None

    for model_id in manifest.models:
        if len(manifest.child_map[model_id]) > 0:
            break
    else:
        raise Exception("No models with children found.")
