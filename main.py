import json
import logging
from configparser import ConfigParser
from modules.extract_graph_elements import extract_entities_and_relationships
from modules.build_graph import consolidate_entities
from modules.util import validate_output_schema
from modules.display import visualize_relationships
from modules.text_preprocessing import preprocess_text

def main():
    # Load API key from configuration
    config = ConfigParser()
    config.read("config/config.properties")
    api_key = config.get("API", "key")

    # Load input report
    try:
        with open("threat_data/input.txt", "r") as file:
            report_text = file.read()
    except FileNotFoundError:
        logging.error("Input file not found. Please provide a valid input file.")
        return

    # Step 1: Preprocess the input text
    try:
        preprocessed_text = preprocess_text(report_text)
        logging.info("Input report preprocessed successfully.")
    except Exception as e:
        logging.error(f"Error during text preprocessing: {e}")
        return
    # Step 1: Extract entities and relationships
    try:
        raw_output = extract_entities_and_relationships(preprocessed_text, api_key)
    except Exception as e:
        logging.error(f"Error during entity extraction: {e}")
        return

    # Step 2: Process the extracted data
    try:
        processed_data = consolidate_entities(raw_output)
    except Exception as e:
        logging.error(f"Error during data processing: {e}")
        return

    # Step 3: Validate the data schema
    try:
        validate_output_schema(processed_data)
    except Exception as e:
        logging.error(f"Validation failed: {e}")
        return

    # Step 4: Save the results
    try:
        with open("threat_data/output.json", "w") as json_file:
            json.dump(processed_data, json_file, indent=4)
        logging.info("Processing completed. Results saved to threat_data/output.json.")
    except Exception as e:
        logging.error(f"Error saving output: {e}")
        return

    # Step 5: Visualize relationships
    try:
        visualize_relationships(processed_data)
    except Exception as e:
        logging.warning(f"Visualization failed: {e}")


if __name__ == "__main__":
    main()
