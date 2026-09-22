from dataclasses import dataclass
from src.kg.graph import KnowledgeGraphStore


@dataclass
class Diagnosis:
    code: str
    message: str


def check_port_mapping(
    requested_port: int,
    listening_port: int,
) -> Diagnosis | None:
    if requested_port != listening_port:
        return Diagnosis(
            code="PORT_MAPPING_MISMATCH",
            message=(
                f"Requested port {requested_port} does not match "
                f"the service listening port {listening_port}."
            ),
        )

    return None

def diagnose_port_mapping(
    store: KnowledgeGraphStore,
    service_id: str,
    requested_port: int,
) -> Diagnosis | None:

    listening_port = store.get_related_property(
        service_id,
        "listens_on",
        "number",
    )

    if listening_port is None:
        return None

    return check_port_mapping(
        requested_port=requested_port,
        listening_port=int(listening_port),
    )