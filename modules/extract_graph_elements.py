import openai
import json
import re
import logging
from modules.util import validate_with_llm


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
    Analyze the following cybersecurity threat intelligence report. If the data is unstructured, first organize it into a structured format that highlights key details. Then, extract the key entities and their relationships.

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

    Example Input:
    "The threat actor 'ShadowBear' used the malware 'MalNet' in a targeted attack on the healthcare industry in Europe. 
    The malware was delivered through phishing emails. ShadowBear has been linked to Eastern Europe and has previously targeted government institutions."

    Example Output:
    {{
      "entities": [
        {{ "id": "1", "name": "ShadowBear", "type": "Threat Actor", "additional_info": {{ "Region": "Eastern Europe" }} }},
        {{ "id": "2", "name": "MalNet", "type": "Malware", "additional_info": {{ "Delivery Method": "Phishing emails" }} }},
        {{ "id": "3", "name": "Healthcare Industry", "type": "Industry", "additional_info": {{ "Region": "Europe" }} }},
        {{ "id": "4", "name": "Government Institutions", "type": "Industry", "additional_info": {{}} }}
      ],
      "relationships": [
        {{ "source": "1", "target": "2", "type": "uses" }},
        {{ "source": "1", "target": "3", "type": "targets" }},
        {{ "source": "1", "target": "4", "type": "previously targeted" }}
      ]
    }}

    Cybersecurity Report:
    {report_text}
    """
    try:
        # Call LLM for extraction
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a cybersecurity analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        content = response.choices[0].message.content.strip()
        logging.debug(f"Raw response from OpenAI: {content}")

        try:
            # Extract the JSON portion using regex
            json_match = re.search(r"\{.*\}", content, re.S)
            if not json_match:
                raise ValueError("JSON data not found in the response.")

            json_content = json_match.group(0)
            data = json.loads(json_content)

            # Validate output with LLM itself
            if not validate_with_llm(data, api_key):
                raise ValueError("LLM validation of its output failed.")

            logging.info("Entity and relationship extraction successful.")
            return data
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON: {e}")
            raise ValueError(f"Response is not valid JSON: {e}")
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        raise RuntimeError(f"OpenAI API error received: {e}")

