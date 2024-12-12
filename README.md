
# Cybersecurity Threat Intelligence Extraction

This project leverages OpenAI's GPT to extract entities and relationships from cybersecurity threat intelligence reports. It processes input text, consolidates extracted data, validates the structure, and visualizes the relationships as a directed graph.

---

## Features

- **Entity Extraction**: Identifies and classifies entities like Threat Actors, Malware, TTPs, Indicators, Industries, and Locations.
- **Relationship Mapping**: Maps relationships like `uses`, `targets`, and `communicates with` between entities.
- **Visualization**: Displays relationships as a directed graph for better understanding.
- **Output Validation**: Ensures JSON output adheres to a defined schema.

---

## Project Structure

```plaintext
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
```

---

## Approach to Solving the Problem Using LLMs

This solution leverages a Large Language Model (LLM), specifically OpenAI's GPT, to analyze cybersecurity threat intelligence reports. The LLM is prompted to identify and classify key entities such as Threat Actors, Malware, and TTPs, and extract relationships between them (e.g., "uses", "targets"). These outputs are normalized into a structured JSON format.

### How the LLM Was Integrated into the Solution
1. **Prompt Design**:
   - A carefully crafted prompt is stored in a JSON file (`prompts/entity_relationship_prompt.json`) to ensure consistency and clarity in the LLM's response.
   - The prompt specifies the requirements for entity extraction, relationship identification, and the expected JSON output structure.

2. **Workflow**:
   - The main script (`main.py`) reads the input report (`threat_data/input.txt`) and passes it along with the prompt to the OpenAI GPT API.
   - The LLM's output is then parsed, validated, and consolidated to remove duplicates or incomplete entries.

3. **Error Handling**:
   - To handle flaky or hallucinated responses, the code validates the JSON structure and falls back to error messages if invalid responses are encountered.

---

## Challenges Faced and How They Were Mitigated

1. **Hallucinated JSON Responses**:
   - Issue: The LLM occasionally returned incomplete or invalid JSON outputs.
   - Mitigation: Added regex-based extraction to identify valid JSON portions, followed by schema validation to ensure the output adheres to the required structure.

2. **Prompt Tuning**:
   - Issue: Initial prompts resulted in inconsistent entity classifications.
   - Mitigation: Iterative refinement of the prompt and modularization into a separate JSON file for easier updates.

3. **Scalability**:
   Challenges
Large Input Reports:
-Issue: Large reports can exceed token limits or cause memory issues during processing.
Impact: The system may fail to handle extensive datasets or produce incomplete outputs.
Repeated Requests:
-Issue: Similar input chunks may result in redundant API calls, increasing latency and costs.
Impact: Processing time and resource utilization become inefficient.
Mitigation Strategies
Batch Processing:
Approach: Split large reports into smaller, manageable chunks (e.g., paragraphs or sections) and process them sequentially.
Benefits:
Reduces token usage per request.
Ensures scalability for larger datasets without memory overflow.
-Caching API Responses:
Approach: Use a caching mechanism to store responses for previously processed input chunks.
Benefits:
Eliminates redundant API calls for identical inputs.
Enhances performance by reducing processing time and API costs.

Solution
Break the report into smaller batches (e.g., paragraphs or sections) and process them sequentially or concurrently.
---

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd cyber-threat-extraction
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the OpenAI API key**:
   - Add your API key in `config/config.properties`:
     ```
     [API]
     key=YOUR_API_KEY
     ```

---

## Usage

1. **Input Report**:
   - Place your input report in `threat_data/input.txt`.

2. **Run the Script**:
   ```bash
   python main.py
   ```

3. **Output**:
   - Extracted entities and relationships will be saved to `threat_data/output.json`.
   - A directed graph visualization (optional) will be saved as `threat_data/relationship_graph.png`.

---

## Example Input and Output

### Input (`input.txt`)
```plaintext
Report Summary:
A cybersecurity threat has been identified involving the threat actor "ShadowBear."

Key Findings:
1. The threat actor "ShadowBear" is linked to Eastern Europe.
2. "ShadowBear" used the malware "MalNet" in a targeted campaign.
3. The target of the campaign was the healthcare industry in Europe.
4. The attack was delivered through phishing emails.
5. "ShadowBear" has a history of targeting government institutions.

Details:
- Threat Actor: "ShadowBear"
  - Region: Eastern Europe
  - Known Activity: Previous attacks on government institutions

- Malware: "MalNet"
  - Usage: Deployed by "ShadowBear" in recent campaigns
  - Delivery Method: Phishing emails

- Target: Healthcare Industry
  - Region: Europe

```

### Output (`output.json`)
```json
{
    "entities": [
        {
            "id": "1",
            "name": "ShadowBear",
            "type": "Threat Actor",
            "additional_info": {
                "Region": "Eastern Europe",
                "Known Activity": "Previous attacks on government institutions"
            }
        },
        {
            "id": "2",
            "name": "MalNet",
            "type": "Malware",
            "additional_info": {
                "Usage": "Deployed by ShadowBear in recent campaigns",
                "Delivery Method": "Phishing emails"
            }
        },
        {
            "id": "3",
            "name": "Healthcare industry",
            "type": "Industry",
            "additional_info": {
                "Region": "Europe"
            }
        },
        {
            "id": "4",
            "name": "Phishing emails",
            "type": "TTPs"
        },
        {
            "id": "5",
            "name": "Eastern Europe",
            "type": "Location"
        },
        {
            "id": "6",
            "name": "Europe",
            "type": "Location"
        }
    ],
    "relationships": [
        {
            "source": "ShadowBear",
            "target": "MalNet",
            "type": "uses"
        },
        {
            "source": "ShadowBear",
            "target": "Healthcare industry",
            "type": "targets"
        },
        {
            "source": "ShadowBear",
            "target": "Eastern Europe",
            "type": "located"
        },
        {
            "source": "MalNet",
            "target": "Healthcare industry",
            "type": "targets"
        },
        {
            "source": "MalNet",
            "target": "Phishing emails",
            "type": "delivered using"
        }
    ]
}
```

![graph](https://github.com/user-attachments/assets/71abfefc-aeba-44b3-8eef-50f4f4580995)

---

## Features and Highlights

- **Scalability**:
  - Modular design allows easy addition of new entity types or relationship categories.
- **Visualization**:
  - Graphical representation of relationships for quick insights.
- **Error Handling**:
  - Comprehensive logging and schema validation for robust error detection.

---

## Testing

1. **Run All Tests**:
   ```bash
   pytest tests/
   ```

2. **Unit Test Coverage**:
   - Consolidation logic (`test_consolidate_entities.py`).
   - JSON validation schema (`test_validate_output_schema.py`).

---

## Challenges Faced

1. **Prompt Design**:
   - Fine-tuning the prompt to ensure consistent entity and relationship extraction.
   - Modularized prompts for flexibility.

2. **Handling Flaky Responses**:
   - Added logic to handle invalid or partial JSON responses from the LLM.

3. **Performance**:
   - Optimized for smaller reports; scalability for large datasets is a potential enhancement.

---

## Future Enhancements

1. **Scalability**:
   - Batch processing for large reports to handle high volumes of data.
2. **Interactive Visualization**:
   - Use tools like `pyvis` for interactive graph visualizations.
3. **Multilingual Support**:
   - Expand prompt and validation to support reports in multiple languages.

---

## Dependencies

- `Python 3.x`
- `openai`
- `matplotlib`
- `networkx`
- `pytest`

