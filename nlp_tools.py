import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy

# Ensure necessary NLTK data is downloaded
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load SpaCy model for named entity recognition
nlp = spacy.load("en_core_web_sm")

def remove_stopwords(text):
    """
    Removes stop words from the input text.

    Parameters:
    text (str): The input text from which stop words need to be removed.

    Returns:
    str: The text with stop words removed.
    """
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

def extract_named_entities(text):
    """
    Extracts named entities from the input text using SpaCy.

    Parameters:
    text (str): The input text for named entity recognition.

    Returns:
    list: A list of tuples where each tuple contains the entity text and its label.
          Example: [('Google', 'ORG'), ('California', 'GPE')]
    """
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def tokenize_text(text):
    """
    Tokenizes the input text into words using NLTK.

    Parameters:
    text (str): The input text to be tokenized.

    Returns:
    list: A list of words (tokens) extracted from the input text.
    """
    return word_tokenize(text)

def lemmatize_text(text):
    """
    Lemmatizes the input text using NLTK's WordNetLemmatizer.

    Parameters:
    text (str): The input text to be lemmatized.

    Returns:
    str: The lemmatized version of the input text.
    """
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)

if __name__ == "__main__":
    sample_text = "Google is a tech giant based in California. It was founded by Larry Page and Sergey Brin."
    print(f"\n\nOriginal text: {sample_text}\n")

    # Example usage of remove_stopwords
    print("Text after removing stopwords:")
    print(remove_stopwords(sample_text))

    # Example usage of extract_named_entities
    print("\nNamed entities extracted:")
    print(extract_named_entities(sample_text))

    # Example usage of tokenize_text
    print("\nTokenized text:")
    print(tokenize_text(sample_text))

    # Example usage of lemmatize_text
    print("\nLemmatized text:")
    print(lemmatize_text(sample_text))