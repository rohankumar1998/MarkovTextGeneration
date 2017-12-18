import string

def preprocess_text(text):
    table = text.maketrans('', '', string.punctuation)
    new_text = text.translate(table)
    return new_text
