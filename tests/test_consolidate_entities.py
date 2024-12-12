import pytest
from modules.build_graph import consolidate_entities

def test_consolidate_entities():
    # Test normal input with duplicates
    input_data = {
        "entities": [
            {"id": "1", "name": "ShadowBear", "type": "Threat Actor"},
            {"name": "ShadowBear", "type": "Threat Actor"},
            {"id": "2", "name": "MalNet", "type": "Malware"}
        ],
        "relationships": [
            {"source": "1", "target": "2", "relationship": "uses"}
        ]
    }

    expected_output = {
        "entities": [
            {"id": "1", "name": "ShadowBear", "type": "Threat Actor"},
            {"id": "2", "name": "MalNet", "type": "Malware"}
        ],
         'relationships': [{'relationship': 'uses',
                    'source': 'ShadowBear',
                    'target': 'MalNet'}]
    }

    result = consolidate_entities(input_data)
    assert result == expected_output

def test_consolidate_entities_empty_input():
    # Test empty entities and relationships
    input_data = {
        "entities": [],
        "relationships": []
    }

    expected_output = {
        "entities": [],
        "relationships": []
    }

    result = consolidate_entities(input_data)
    assert result == expected_output

def test_consolidate_entities_missing_ids():
    # Test missing IDs in entities
    input_data = {
        "entities": [
            {"name": "ShadowBear", "type": "Threat Actor"},
            {"id": "2", "name": "MalNet", "type": "Malware"}
        ],
        "relationships": [
            {"source": "ShadowBear", "target": "MalNet", "relationship": "uses"}
        ]
    }

    result = consolidate_entities(input_data)

    # Verify that a unique ID is assigned to the first entity
    assert len(result["entities"]) == 2
    assert result["entities"][0]["id"] is not None
    assert result["entities"][1]["id"] == "2"

def test_consolidate_entities_duplicate_relationships():
    # Test duplicate relationships
    input_data = {'entities': [{'id': '1', 'name': 'ShadowBear', 'type': 'Threat Actor'},
              {'id': '2', 'name': 'MalNet', 'type': 'Malware'}],
 'relationships': [{'relationship': 'uses',
                    'source': 'ShadowBear',
                    'target': 'MalNet'},
                   {'relationship': 'uses',
                    'source': 'ShadowBear',
                    'target': 'MalNet'}]}

    expected_output = {'entities': [{'id': '1', 'name': 'ShadowBear', 'type': 'Threat Actor'},
              {'id': '2', 'name': 'MalNet', 'type': 'Malware'}],
 'relationships': [{'relationship': 'uses', 'source': None, 'target': None},
                   {'relationship': 'uses', 'source': None, 'target': None}]}

    result = consolidate_entities(input_data)
    assert result == expected_output


def test_consolidate_entities_invalid_relationships():
    # Test relationships with missing source or target
    input_data = {
        "entities": [
            {"id": "1", "name": "ShadowBear", "type": "Threat Actor"},
            {"id": "2", "name": "MalNet", "type": "Malware"}
        ],
        "relationships": [
            {"source": "1", "target": "2", "relationship": "uses"},
            {"source": "", "target": "2", "relationship": "uses"},
            {"source": "1", "target": "", "relationship": "uses"}
        ]
    }

    expected_output = {'entities': [{'id': '1', 'name': 'ShadowBear', 'type': 'Threat Actor'},
              {'id': '2', 'name': 'MalNet', 'type': 'Malware'}],
 'relationships': [{'relationship': 'uses',
                    'source': 'ShadowBear',
                    'target': 'MalNet'},
                   {'relationship': 'uses', 'source': None, 'target': 'MalNet'},
                   {'relationship': 'uses',
                    'source': 'ShadowBear',
                    'target': None}]}

    result = consolidate_entities(input_data)
    assert result == expected_output
