import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load SpaCy model for named entity recognition
nlp = spacy.load("en_core_web_sm")

def remove_stopwords(text):
    """
    Removes stop words from the input text.
    """
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

def extract_named_entities(text):
    """
    Extracts named entities from the input text.
    """
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def tokenize_text(text):
    """
    Tokenizes the input text into words.
    """
    return word_tokenize(text)

def lemmatize_text(text):
    """
    Lemmatizes the input text.
    """
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)

if __name__ == "__main__":
    # ...existing code...
    pass
