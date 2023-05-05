KEY_WORDS = ["differentially", "privacy", "private", "differential"]

def contains_key_words(title: str) -> bool:
    return any([key_word in title.lower() for key_word in KEY_WORDS])
