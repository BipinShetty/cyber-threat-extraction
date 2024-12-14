import logging
import spacy.cli
import spacy

# Load the model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(report_text):
    """
    Preprocess text using spaCy for tokenization.

    Parameters:
        report_text (str): The input text to preprocess.

    Returns:
        str: Preprocessed text.
    """
    try:
        logging.info("Initializing spaCy model.")
        nlp = spacy.load("en_core_web_sm")

        logging.info("Tokenizing the input text.")
        doc = nlp(report_text)

        # Join tokens back into a single string
        preprocessed_text = " ".join(token.text for token in doc)

        logging.info("Text preprocessing completed successfully.")
        return preprocessed_text

    except Exception as e:
        logging.error(f"Error during text preprocessing: {e}")
        raise
