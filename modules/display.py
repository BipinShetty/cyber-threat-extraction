import matplotlib.pyplot as plt
import networkx as nx
import logging


def visualize_relationships(data):
    """
    Visualizes the relationships between entities using a directed graph.

    Parameters:
        data (dict): Input dictionary containing entities and relationships.

    Returns:
        None
    """
    logging.info("Starting visualization of relationships.")
    graph = nx.DiGraph()

    # Add nodes for entities
    for entity in data["entities"]:
        graph.add_node(entity["name"], label=entity["name"])
        logging.debug(f"Added node for entity: {entity["name"]}")

    # Add edges for relationships, source and target are 2 nodes, connected by relation type returned by llm
    for relationship in data["relationships"]:
        graph.add_edge(relationship["source"], relationship["target"], label=relationship["type"])
        logging.debug(f"Added edge from {relationship["source"]} to {relationship["target"]} with label {relationship["type"]}")

    # Generate layout and draw graph
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=3000, font_size=10)
    labels = nx.get_edge_attributes(graph, "label")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()
    logging.info("Visualization completed.")
