def test_node_parents(manifest):
    for model in manifest.models.values():
        assert model.parents is not None
        for node in model.parents:
            assert node is not None, f"{model} has an undefined parent"
            assert str(node) == node.unique_id


def test_node_children(manifest):
    for model in manifest.models.values():
        assert model.children is not None
        for node in model.children:
            assert node is not None, f"{model} has an undefined child"
            assert str(node) == node.unique_id


def test_node_str(manifest):
    for model in manifest.models.values():
        assert str(model) == model.unique_id


def test_node_repr(manifest):
    for model in manifest.models.values():
        assert repr(model) is not None
