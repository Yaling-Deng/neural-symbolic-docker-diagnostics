from src.models.schema import (
    Entity,
    KnowledgeGraph,
    Property,
    Relation,
)
from src.models.semantic import SemanticFacts


def make_id(prefix: str, name: str) -> str:
    normalized = name.lower().replace(" ", "_")
    return f"{prefix}_{normalized}"


def semantic_facts_to_kg(facts: SemanticFacts) -> KnowledgeGraph:
    entities = []
    relations = []
    properties = []

    entity_ids = set()

    def add_entity(entity: Entity):
        if entity.id not in entity_ids:
            entities.append(entity)
            entity_ids.add(entity.id)

    # Services
    for service in facts.services:
        service_id = make_id("service", service.name)

        add_entity(
            Entity(
                id=service_id,
                type="Service",
                name=service.name,
            )
        )

    # Connections
    for connection in facts.connections:
        source_id = make_id("application", connection.source)
        target_id = make_id("service", connection.target)

        add_entity(
            Entity(
                id=source_id,
                type="Application",
                name=connection.source,
            )
        )

        add_entity(
            Entity(
                id=target_id,
                type="Service",
                name=connection.target,
            )
        )

        relations.append(
            Relation(
                source=source_id,
                relation="connects_to",
                target=target_id,
            )
        )

        if connection.requested_port is not None:
            request_id = "request"

            add_entity(
                Entity(
                    id=request_id,
                    type="Configuration",
                    name="connection_request",
                )
            )

            properties.append(
                Property(
                    entity_id=request_id,
                    key="requested_port",
                    value=str(connection.requested_port),
                )
            )

    # Listening ports
    for listener in facts.listeners:
        service_id = make_id("service", listener.service)
        port_id = make_id(
            "port",
            f"{listener.service}_{listener.port}",
        )

        add_entity(
            Entity(
                id=port_id,
                type="Port",
                name=str(listener.port),
            )
        )

        relations.append(
            Relation(
                source=service_id,
                relation="listens_on",
                target=port_id,
            )
        )

        properties.append(
            Property(
                entity_id=port_id,
                key="number",
                value=str(listener.port),
            )
        )

    return KnowledgeGraph(
        entities=entities,
        relations=relations,
        properties=properties,
    )