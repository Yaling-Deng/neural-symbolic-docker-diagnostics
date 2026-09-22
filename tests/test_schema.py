from src.models.schema import Entity, Property, Relation, KnowledgeGraph


def test_knowledge_graph_schema():
    flask = Entity(
        id="service_flask",
        type="Service",
        name="flask",
    )

    postgres = Entity(
        id="service_postgres",
        type="Service",
        name="postgres",
    )

    connection = Relation(
        source="service_flask",
        relation="connects_to",
        target="service_postgres",
    )

    status = Property(
        entity_id="service_postgres",
        key="ready",
        value="true",
    )

    graph = KnowledgeGraph(
        entities=[flask, postgres],
        relations=[connection],
        properties=[status],
    )

    assert len(graph.entities) == 2
    assert len(graph.relations) == 1
    assert len(graph.properties) == 1