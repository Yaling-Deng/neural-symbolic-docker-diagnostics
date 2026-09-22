from src.neural.deepseek import parse_with_deepseek
from src.kg.builder import semantic_facts_to_kg
from src.kg.graph import KnowledgeGraphStore
from src.reasoning.rules import diagnose_port_mapping


def diagnose(text: str):
    # 1. Natural language → SemanticFacts
    facts = parse_with_deepseek(text)

    # 2. SemanticFacts → KnowledgeGraph
    kg = semantic_facts_to_kg(facts)

    # 3. KnowledgeGraph → graph store
    store = KnowledgeGraphStore()
    store.add_knowledge_graph(kg)

    # 4. Find the requested port
    requested_port = store.get_property(
        "request",
        "requested_port",
    )

    if requested_port is None:
        return "Could not identify the requested port."

    # 5. Find the target service through the KG
    service_ids = store.get_relation_targets(
        "application_application",
        "connects_to",
    )

    if not service_ids:
        return "Could not identify the target service."

    service_id = service_ids[0]

    # 6. Knowledge Graph → symbolic reasoning
    diagnosis = diagnose_port_mapping(
        store=store,
        service_id=service_id,
        requested_port=int(requested_port),
    )

    if diagnosis is None:
        return "No port mapping mismatch was detected."

    return (
        f"Diagnosis: {diagnosis.code}\n\n"
        f"{diagnosis.message}"
    )


def main():
    print("Docker Diagnostic System")
    print("------------------------")
    print("Describe the problem in natural language.")
    print()

    text = input("> ")

    result = diagnose(text)

    print()
    print(result)


if __name__ == "__main__":
    main()