import pytest
from jsonschema import ValidationError
from modules.validation import validate_output_schema

def test_validate_output_schema_valid():
    # Valid input data
    valid_data = {
        "entities": [
            {"id": "1", "name": "ShadowBear", "type": "Threat Actor"}
        ],
        "relationships": [
            {"source": "1", "target": "2", "type": "uses"}
        ]
    }

    # Should pass validation without raising exceptions
    try:
        validate_output_schema(valid_data)
    except ValidationError as e:
        pytest.fail(f"ValidationError raised unexpectedly: {e}")


def test_validate_output_schema_missing_required_fields():
    # Invalid input data (missing required fields)
    invalid_data = {
        "entities": [
            {"id": "1", "type": "Threat Actor"}  # Missing "name"
        ],
        "relationships": [
            {"source": "1", "target": "2"}  # Missing "type"
        ]
    }

    # Expect the validation to raise a ValidationError
    with pytest.raises(ValidationError):
        validate_output_schema(invalid_data)
