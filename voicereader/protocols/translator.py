from typing import Protocol
from voicereader.protocols.source import UntranslatedTransaction

class TranslatedTransaction:
    def __init__(
        self,
        title: str,
        article_text_jp: str,
        tag: str,
    ):
        self.title = title
        self.article_text_jp = article_text_jp
        self.tag = tag

    def __repr__(self):
        return f"TranslatedTransaction(\n\ttitle={self.title}\n\tarticle_text_jp={self.article_text_jp[:60]}...\n\ttag={self.tag}\n)"

    def get_title(self) -> str:
        return self.title

    def get_article_text_jp(self) -> str:
        return self.article_text_jp

    def get_tag(self) -> str:
        return self.tag

class Translator(Protocol):
    def translate(self, transaction: UntranslatedTransaction) -> TranslatedTransaction:
        pass
