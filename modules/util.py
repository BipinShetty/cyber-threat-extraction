from jsonschema import validate

import openai
import json
import logging


def validate_with_llm(data, api_key):
    """
    Ask the LLM to validate its own output and critique it if invalid.

    Parameters:
        data (dict): The JSON data to validate.
        api_key (str): API key for OpenAI.

    Returns:
        bool: True if the LLM validates the output as correct, False otherwise.
    """
    logging.info("Asking LLM to critique its output.")
    openai.api_key = api_key

    prompt = f"""
    The following JSON was generated based on a cybersecurity report. Please validate the JSON against the expected schema mentioned next.
    
    Output the results as a JSON object with the following structure:
      {{
        "entities": [
          {{ "id": "unique_id", "name": "entity_name", "type": "entity_type", "additional_info": {{...}} }}
        ],
        "relationships": [
          {{ "source": "source_entity_id", "target": "target_entity_id", "type": "relationship_type" }}
        ]
      }}


    If valid, respond with 'VALID'. If invalid, specify the issues in detail.

    JSON:
    {json.dumps(data, indent=4)}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a cybersecurity validation assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        critique = response.choices[0].message.content.strip()
        logging.debug(f"LLM critique: {critique}")

        if "VALID" in critique.upper():
            logging.info("LLM validated its output as correct.")
            return True
        else:
            logging.warning(f"LLM found issues: {critique}")
            return False
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error during validation: {e}")
        return False


def validate_output_schema(data):
    schema = {
        "type": "object",
        "properties": {
            "entities": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                    },
                    "required": ["id", "name", "type"],
                },
            },
            "relationships": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string"},
                        "target": {"type": "string"},
                        "type": {"type": "string"},
                    },
                    "required": ["source", "target", "type"],
                },
            },
        },
        "required": ["entities", "relationships"],
    }
    validate(instance=data, schema=schema)
