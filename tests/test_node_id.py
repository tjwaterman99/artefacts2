from artefacts.core import NodeId


def test_node_id_str():
    name = "test"
    node_id = NodeId(node_id=name)
    assert str(node_id) == name


def test_node_id_repr():
    name = "test"
    node_id = NodeId(node_id=name)
    assert repr(node_id) == name


def test_node_id_eq():
    name = "test"
    node_id = NodeId(node_id=name)
    assert node_id == name

    other_node_id = NodeId(node_id=name)
    assert node_id == other_node_id


def test_node_id_hash():
    name = "test"
    node_id = NodeId(node_id=name)
    assert hash(node_id) == hash(node_id.node_id)

    d = {node_id: "value"}
    assert name in d
