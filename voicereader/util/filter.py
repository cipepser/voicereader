from typing import List

def contains_key_words(title: str, key_words: List[str]) -> bool:
    return any([key_word in title.lower() for key_word in key_words])
