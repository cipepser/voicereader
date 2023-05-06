from typing import Protocol, List

class UntranslatedTransaction:
    def __init__(
        self,
        title: str,
        article_text_en: str,
        tag: str,
    ):
        self.title = title
        self.article_text_en = article_text_en
        self.tag = tag

    def get_title(self) -> str:
        return self.title

    def get_article_text_jp(self) -> str:
        return self.article_text_en

    def get_tag(self) -> str:
        return self.tag

class ContentExtractor(Protocol):
    def extract(self) -> List[UntranslatedTransaction]:
        pass
