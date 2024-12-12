import openai
import json
import re
import logging


def extract_entities_and_relationships(report_text, api_key):
    """
    Extracts entities and relationships from a cybersecurity report using OpenAI's GPT model.

    Parameters:
        report_text (str): The cybersecurity report text to analyze.
        api_key (str): API key for OpenAI.

    Returns:
        dict: Extracted entities and relationships in JSON format.
    """
    logging.info("Starting entity and relationship extraction.")
    openai.api_key = api_key
    # I have used prompt directly in here for better readability and this is present in /prompts/entity_relationship_prompt.json too for better structure later...
    prompt = f"""
    Analyze the following cybersecurity threat intelligence report and extract the key entities and their relationships. 

    Requirements:
    - Extract entities and classify them into the following types:
      - Threat Actor
      - Malware
      - TTPs (Tactics, Techniques, Procedures)
      - Indicators (IP addresses, file hashes, URLs, domains, etc.)
      - Industry
      - Location
    - Identify relationships between entities, such as:
      - Uses: (e.g., threat actor uses malware or TTPs)
      - Targets: (e.g., malware targets industry or location)
      - Communicates With: (e.g., threat actors collaborating or interacting)
    - Output the results as a JSON object with the following structure:
      {{
        "entities": [
          {{ "id": "unique_id", "name": "entity_name", "type": "entity_type", "additional_info": {{...}} }}
        ],
        "relationships": [
          {{ "source": "source_entity_id", "target": "target_entity_id", "type": "relationship_type" }}
        ]
      }}

    Cybersecurity Report:
    {report_text}
    """
    # Call open-ai for getting the relationship and entity info. I used my open-ai key for same
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a cybersecurity analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )

        if response and response.choices:
            content = response.choices[0].message.content.strip()
            logging.debug(f"Raw response from OpenAI: {content}")
            try:
                # Extract the JSON portion using regex
                json_match = re.search(r"\{.*\}", content, re.S)
                if not json_match:
                    raise ValueError("JSON data not found in the response.")

                json_content = json_match.group(0)
                data = json.loads(json_content)

                # Validate the JSON structure for entities and relationships info as per prompt and json schema
                if not isinstance(data, dict) or "entities" not in data or "relationships" not in data:
                    raise ValueError("Invalid JSON structure: missing 'entities' or 'relationships'")
                if not all(isinstance(entity, dict) for entity in data.get("entities", [])):
                    raise ValueError("Invalid entity format detected")
                if not all(isinstance(relationship, dict) for relationship in data.get("relationships", [])):
                    raise ValueError("Invalid relationship format detected")

                logging.info("Entity and relationship extraction successful.")
                return data
            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse JSON: {e}")
                raise ValueError(f"Response is not valid JSON: {e}")
        raise ValueError("No valid response from the API.")
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        raise RuntimeError(f"OpenAI API error received: {e}")