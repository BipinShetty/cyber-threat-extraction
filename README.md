Cybersecurity Threat Intelligence Extraction
This project leverages OpenAI's GPT to extract entities and relationships from cybersecurity threat intelligence reports. It processes input text, consolidates extracted data, validates the structure, and visualizes the relationships as a directed graph.

Features
Entity Extraction: Identifies and classifies entities like Threat Actors, Malware, TTPs, Indicators, Industries, and Locations.
Relationship Mapping: Maps relationships like uses, targets, and communicates with between entities.
Visualization: Displays relationships as a directed graph for better understanding.
Output Validation: Ensures JSON output adheres to a defined schema.
Project Structure
plaintext
Copy code
cyber-threat-extraction/
├── config/
│   └── config.properties         # Configuration file for API key
├── prompts/
│   └── entity_relationship_prompt.json  # Prompt for LLM
├── threat_data/
│   ├── input.txt                 # Example input report
│   ├── output.json               # Example output
│   └── relationship_graph.png    # Graph visualization (optional)
├── modules/
│   ├── build_graph.py            # Consolidation and processing logic
│   ├── extract_graph_elements.py # LLM interaction
│   ├── validation.py             # JSON schema validation
│   ├── display.py                # Visualization of relationships
├── tests/
│   ├── test_consolidate_entities.py  # Unit tests for entity consolidation
│   ├── test_validate_output_schema.py  # Unit tests for validation schema
├── requirements.txt              # Python dependencies
├── main.py                       # Main execution script
├── README.md                     # Project documentation
Installation
Clone the repository:

bash
Copy code
git clone <repository_url>
cd cyber-threat-extraction
Set up a virtual environment (optional but recommended):

bash
Copy code
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\\Scripts\\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configure the OpenAI API key:

Add your API key in config/config.properties:
csharp
Copy code
[API]
key=YOUR_API_KEY
Usage
Input Report:

Place your input report in threat_data/input.txt.
Run the Script:

bash
Copy code
python main.py
Output:

Extracted entities and relationships will be saved to threat_data/output.json.
A directed graph visualization (optional) will be saved as threat_data/relationship_graph.png.
Example Input and Output
Input (input.txt)
plaintext
Copy code
The threat actor "ShadowBear" has been identified using the malware "MalNet" in a targeted campaign against the healthcare industry in Europe. The campaign involved phishing emails to deliver the malware. ShadowBear is suspected of being linked to the region of Eastern Europe and has previously targeted government institutions.
Output (output.json)
json
Copy code
{
    "entities": [
        {"id": "1", "name": "ShadowBear", "type": "Threat Actor"},
        {"id": "2", "name": "MalNet", "type": "Malware"}
    ],
    "relationships": [
        {"source": "ShadowBear", "target": "MalNet", "type": "uses"}
    ]
}
Features and Highlights
Scalability:
Modular design allows easy addition of new entity types or relationship categories.
Visualization:
Graphical representation of relationships for quick insights.
Error Handling:
Comprehensive logging and schema validation for robust error detection.
Testing
Run All Tests:

bash
Copy code
pytest tests/
Unit Test Coverage:

Consolidation logic (test_consolidate_entities.py).
JSON validation schema (test_validate_output_schema.py).
Challenges Faced
Prompt Design:

Fine-tuning the prompt to ensure consistent entity and relationship extraction.
Modularized prompts for flexibility.
Handling Flaky Responses:

Added logic to handle invalid or partial JSON responses from the LLM.
Performance:

Optimized for smaller reports; scalability for large datasets is a potential enhancement.
Future Enhancements
Scalability:
Batch processing for large reports to handle high volumes of data.
Interactive Visualization:
Use tools like pyvis for interactive graph visualizations.
Multilingual Support:
Expand prompt and validation to support reports in multiple languages.
Dependencies
Python 3.x
openai
matplotlib
networkx
pytest
