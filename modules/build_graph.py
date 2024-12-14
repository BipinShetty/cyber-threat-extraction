import uuid
import logging

def consolidate_entities(data):
    """
    Consolidates entities by removing duplicates and normalizing relationships.

    Parameters:
        data (dict): Input dictionary containing entities and relationships.

    Returns:
        dict: A dictionary with consolidated entities and relationships as a graph.
    """
    logging.info("Starting entity consolidation process.")
    seen_entities = {}
    seen_relationship ={}

    # Consolidate entities
    for entity in data.get("entities", []):
        if "id" not in entity:
            # Assign unique ID if missing
            entity["id"] = str(uuid.uuid4())
            logging.debug(f"Assigned new ID to entity: {entity}")
            # Use name and type as unique identifiers
        key = (entity["name"], entity["type"])
        if key not in seen_entities:
            # Store the entity if it's not already seen, avoid duplicate entity names
            seen_entities[key] = entity
            logging.debug(f"Added entity to seen_entities: {entity}")
        else:
            logging.debug(f"Duplicate entity detected and skipped: {entity}")

    logging.info("Entity consolidation completed.")

    # Map entity IDs to their names for look-up later
    entity_name_map = {e["id"]: e["name"] for e in seen_entities.values()}

    #  Map relationships with entity names as source and target, type is the edge of relationship between 2.
    relationships = []
    for relationship in data.get("relationships", []):
        key = (relationship["source"],relationship["target"],relationship["type"])
        if key not in seen_relationship:
            relationship["source"] = entity_name_map.get(relationship["source"])
            relationship["target"] = entity_name_map.get(relationship["target"])
            relationships.append(relationship)
            seen_relationship[key] = relationship
            logging.debug(f"Processed relationship: {relationship}")

    logging.info("Relationship normalization completed.")

    # Return graph for visualization
    graph_data = {
        "entities": list(seen_entities.values()),
        "relationships": relationships
    }
    logging.info("Consolidated data ready for output.")
    return graph_data