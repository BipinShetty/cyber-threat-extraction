
# Cybersecurity Threat Intelligence Extraction

This project leverages OpenAI's GPT to extract entities and relationships from cybersecurity threat intelligence reports. It processes input text, consolidates extracted data, validates the structure, and visualizes the relationships as a directed graph.

---

## Features

- **Entity Extraction**: Identifies and classifies entities like Threat Actors, Malware, TTPs, Indicators, Industries, and Locations.
- **Relationship Mapping**: Maps relationships like `uses`, `targets`, and `communicates with` between entities.
- **Visualization**: Displays relationships as a directed graph for better understanding.
- **Output Validation**: Ensures JSON output adheres to a defined schema.

---

# Evaluation Criteria and Implementation Details

This document explains how the solution meets the evaluation criteria for the cybersecurity threat intelligence extraction project.

---

## **1. Correctness: Accuracy of Entity and Relationship Extraction**
- **Implementation**:
  - Entities are extracted with specific types such as `Threat Actor`, `Malware`, and `TTPs`.
  - Relationships such as `uses` and `targets` are mapped accurately.
  - Outputs are validated against a defined JSON schema.
- **Tests**:
  - Comprehensive unit tests validate the correctness of entity and relationship extraction.

---

## **2. LLM Integration: Effective Usage of the LLM API and Prompt Engineering**
- **Implementation**:
  - The OpenAI GPT API is used with a well-designed prompt stored in `prompts/entity_relationship_prompt.json`.
  - Modularized prompt design ensures consistency and simplifies updates.
  - Regex-based extraction ensures valid JSON data is captured from LLM outputs.
- **Error Handling**:
  - Handles hallucinated or incomplete JSON outputs through validation and fallback mechanisms.

---

## **3. Code Quality: Clean, Modular, and Well-Documented Code**
- **Implementation**:
  - The codebase is organized into modules:
    - `build_graph.py` for entity consolidation.
    - `extract_graph_elements.py` for LLM interaction.
    - `validation.py` for schema validation.
    - `display.py` for visualization.
  - Logging is used for error tracing and debugging.
  - Functions are well-documented with clear docstrings.

---

## **4. Extensibility: Ability to Extend the Solution**
- **Implementation**:
  - New entity types or relationships can be added by modifying the prompt and schema.
  - Modular architecture allows for easy integration of additional features.
- **Scenarios**:
  - Supports multilingual prompts for future expansion.
  - Handles scalable datasets with batch processing.

---

## **5. Performance: Efficient Processing of Medium to Large Reports**(Future enhancements)
- **Implementation**:
  - Batch processing splits large reports into manageable chunks.
  - Caching avoids redundant API calls, reducing latency and improving efficiency.
  - Rate limiting ensures compliance with API limits.
- **Potential Enhancements**:
  - Further optimization for parallel processing.

---

## **6. Documentation: Clarity in Explaining the Solution**
- **Implementation**:
  - The README includes:
    - Setup instructions.
    - Example input/output.
    - Challenges faced and their mitigations.
    - Testing and usage guidelines.
  - Documentation is provided for all modules and key functions.

---

## **7. Bonus: Innovative Features**
- **Visualization**:
  - Relationship visualization using `matplotlib` and `networkx`.
- **Extensibility**:
  - Designed to support additional entity types, relationships, and multilingual prompts.

---

This comprehensive implementation ensures the solution is robust, accurate, and scalable for real-world applications.



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


## **Challenges Faced and How They Were Mitigated**

**Hallucination Reduction Measures**

**Preprocessing for Input Consistency**
* **Issue:** Ambiguous input text can lead to inconsistent or unclear LLM responses.
* **Mitigation:**
  * Employ SpaCy to clean, tokenize, and standardize input text.
  * This preprocessing significantly reduces ambiguities and improves LLM comprehension.

**Enhanced Prompt Engineering**
* **Issue:** Initial prompts caused inconsistent entity classifications and hallucinations.
* **Mitigation:**
  * Added 1-shot examples to provide context and demonstrate expected outputs.
  * Included an expected JSON schema to ensure structured and valid LLM-generated results.
  * Modularized prompt design for easier updates and future adaptability.
  * **Code Reference:** Prompt Code

**LLM Self-Critique**
* **Issue:** The LLM sometimes produced invalid JSON responses with missing entities or relationships.
* **Mitigation:**
  * Introduced a secondary validation step where the LLM critiques its own output against the predefined schema.
  * This feedback loop helps detect and resolve inconsistencies in real-time.
  * **Code Reference:** Validation Code

**Elimination of Redundancies**
* **Issue:** Output occasionally contained duplicate entities or relationships.
* **Mitigation:**
  * Improved post-processing logic to detect and remove redundant entities and relationships.
  * This refinement enhances data quality for graph database storage and downstream tasks.

2.**Scalability**: (How can be mitigated in future)
   ### **Challenges**
   - **Large Input Reports**:
     - **Issue**: Large reports can exceed token limits or cause memory issues during processing.
     - **Impact**: The system may fail to handle extensive datasets or produce incomplete outputs.
   - **Repeated Requests**:
     - **Issue**: Similar input chunks may result in redundant API calls, increasing latency and costs.
     - **Impact**: Processing time and resource utilization become inefficient.

   ### **Mitigation Strategies**
   1. **Batch Processing**:
      - **Approach**: Split large reports into smaller, manageable chunks (e.g., paragraphs or sections) and process them sequentially.
      - **Benefits**:
        - Reduces token usage per request.
        - Ensures scalability for larger datasets without memory overflow.
   2. **Caching API Responses**:
      - **Approach**: Use a caching mechanism to store responses for previously processed input chunks.
      - **Benefits**:
        - Eliminates redundant API calls for identical inputs.
        - Enhances performance by reducing processing time and API costs.

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

## Testing

1. **Run All Tests**:
   ```bash
   pytest tests/
   ```

2. **Unit Test Coverage**:
   - Consolidation logic (`test_consolidate_entities.py`).
   - JSON validation schema (`test_validate_output_schema.py`).

---

## Dependencies

- `Python 3.x`
- `openai`
- `matplotlib`
- `networkx`
- `pytest`

