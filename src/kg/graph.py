import networkx as nx

from src.models.schema import KnowledgeGraph


class KnowledgeGraphStore:
    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_knowledge_graph(self, kg: KnowledgeGraph):
        for entity in kg.entities:
            self.graph.add_node(
                entity.id,
                type=entity.type,
                name=entity.name,
            )

        for relation in kg.relations:
            self.graph.add_edge(
                relation.source,
                relation.target,
                relation=relation.relation,
            )

        for prop in kg.properties:
            self.graph.nodes[prop.entity_id][prop.key] = prop.value

    def get_neighbors(self, entity_id: str):
        return list(self.graph.successors(entity_id))

    def get_relation_targets(self, entity_id: str, relation: str):
        return [
            target
            for _, target, data in self.graph.out_edges(
                entity_id,
                data=True,
            )
            if data.get("relation") == relation
        ]

    def get_property(self, entity_id: str, key: str):
        return self.graph.nodes[entity_id].get(key)

    def get_related_property(
        self,
        entity_id: str,
        relation: str,
        property_key: str,
    ):
        targets = self.get_relation_targets(entity_id, relation)

        if not targets:
            return None

        return self.get_property(targets[0], property_key)