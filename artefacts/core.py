from dbt.contracts.graph.manifest import WritableManifest
from artefacts import cache


class NodeId:
    def __init__(self, node_id):
        self.node_id = node_id

    def __str__(self):
        return self.node_id

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))


# TODO: tests for the dunder methods
class Node:
    def __init__(self, node, target="./target"):
        self._node = node
        if "manifest" not in cache.local:
            cache.local["manifest"] = Manifest(target=target)
        self.manifest = cache.local["manifest"]

    def __str__(self):
        return self.unique_id

    def __repr__(self):
        return f"<{self.__class__.__name__.capitalize()} {str(self)}>"

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    @property
    def unique_id(self):
        return self._node.unique_id

    @property
    def parents(self):
        return self.manifest.parent_map.get(self.unique_id, list())

    @property
    def children(self):
        return self.manifest.child_map.get(self.unique_id, list())


class Model(Node):
    pass


class Test(Node):
    pass


class Source(Node):
    pass


class Macro(Node):
    pass


class Exposure(Node):
    pass


class Metric(Node):
    pass


class Operation(Node):
    pass


class Seed(Node):
    pass


class Analysis(Node):
    pass


class Manifest:

    node_types = {
        'model': Model,
        'test': Test,
        'source': Source,
        'macro': Macro,
        'exposure': Exposure,
        'metric': Metric,
        'operation': Operation,
        'seed': Seed,
        'analysis': Analysis,
    }

    def __init__(self, target):
        self.target = target
        self._manifest = WritableManifest.read(self.target)
        self._cache = dict()
        cache.local["manifest"] = self

    def _get_all_nodes(self):
        return {
            **self._manifest.nodes,
            **self._manifest.sources,
            **self._manifest.macros,
            **self._manifest.exposures,
            **self._manifest.metrics,
            # **self._manifest.disabled,
        }

    @property
    def _nodes(self):
        if "_nodes" in self._cache:
            return self._cache["_nodes"]

        result = {}
        for node_id, node in self._get_all_nodes().items():
            ResourceType = self.node_types.get(node.resource_type)
            if ResourceType is not None:
                result[node_id] = ResourceType(node)
        self._cache["_nodes"] = result
        return self._cache["_nodes"]

    # todo: cache
    @property
    def models(self):
        return {k: v for k, v in self._nodes.items() if type(v) == Model}

    # todo: cache
    @property
    def tests(self):
        return {k: v for k, v in self._nodes.items() if type(v) == Test}

    @property
    def sources(self):
        return {k: v for k, v in self._nodes.items() if type(v) == Source}

    @property
    def macros(self):
        return {k: v for k, v in self._nodes.items() if type(v) == Macro}

    @property
    def exposures(self):
        return {k: v for k, v in self._nodes.items() if type(v) == Exposure}

    @property
    def metrics(self):
        return {k: v for k, v in self._nodes.items() if type(v) == Metric}

    @property
    def parent_map(self):
        if "parent_map" in self._cache:
            return self._cache["parent_map"]

        result = dict()

        for _node_id, _nodes in self._manifest.parent_map.items():
            node_id = NodeId(node_id=_node_id)
            nodes = [self._nodes.get(n) for n in _nodes]
            result.update({node_id: nodes})
        self._cache.update(parent_map=result)

        return result

    # todo: DRY up the child_map and parent_map attributes
    @property
    def child_map(self):
        if "child_map" in self._cache:
            return self._cache["child_map"]

        result = dict()

        for _node_id, _nodes in self._manifest.child_map.items():
            node_id = NodeId(node_id=_node_id)
            nodes = [self._nodes.get(n) for n in _nodes]
            result.update({node_id: nodes})
        self._cache.update(child_map=result)

        return result
