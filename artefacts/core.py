from dbt.contracts.graph.manifest import WritableManifest
from artefacts import cache


class NodeId:
    def __init__(self, node_id):
        self.node_id = node_id


class Node:
    def __init__(self, node, target='./target'):
        self._node = node
        if 'manifest' not in cache.local:
            cache.local['manifest'] = Manifest(target=target)
        self.manifest = cache.local['manifest']

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


class Manifest:

    node_types = {
        'model': Model,
        'test': Test,
        'source': Source,
        'macro': Macro,
        'exposure': Exposure,
        'metric': Metric,
    }

    def __init__(self, target):
        self.target = target
        self._manifest = WritableManifest.read(self.target)
        self._cache = dict()
        cache.local['manifest'] = self

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
        if '_nodes' in self._cache:
            return self._cache['_nodes']

        result = {}
        for node_id, node in self._get_all_nodes().items():
            ResourceType = self.node_types.get(node.resource_type)
            if ResourceType is not None:
                result[node_id] = ResourceType(node)
        self._cache['_nodes'] = result
        return self._cache['_nodes']

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

    # todo: cache, convert ids and nodes into their resource types
    @property
    def parent_map(self):
        return self._manifest.parent_map

    # todo: cache, convert ids and nodes into their resource types
    @property
    def child_map(self):
        return self._manifest.child_map
