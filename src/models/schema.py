from pydantic import BaseModel
from typing import Literal


class Entity(BaseModel):
    id: str
    type: Literal["Application", "Container", "Service", "Port", "Network", "Configuration"]
    name: str


class Property(BaseModel):
    entity_id: str
    key: str
    value: str


class Relation(BaseModel):
    source: str
    relation: Literal[
        "runs_in",
        "depends_on",
        "connects_to",
        "listens_on",
        "exposes",
        "configured_with",
    ]
    target: str


class KnowledgeGraph(BaseModel):
    entities: list[Entity]
    relations: list[Relation]
    properties: list[Property]