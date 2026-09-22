from pydantic import BaseModel, Field


class ApplicationFact(BaseModel):
    name: str

class ServiceFact(BaseModel):
    name: str


class ConnectionFact(BaseModel):
    source: str
    target: str
    requested_port: int | None = None


class ListenerFact(BaseModel):
    service: str
    port: int


class SemanticFacts(BaseModel):
    applications: list[ApplicationFact] = Field(default_factory=list)
    services: list[ServiceFact] = Field(default_factory=list)
    connections: list[ConnectionFact] = Field(default_factory=list)
    listeners: list[ListenerFact] = Field(default_factory=list)