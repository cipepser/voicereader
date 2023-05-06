from typing import Protocol, Optional
from voicereader.protocols.translator import TranslatedTransaction

class Destinator(Protocol):
    # return url
    def create_private_article(self ,transaction: TranslatedTransaction) -> Optional[str]:
        pass

    def send_to_reader(self, url: str) -> None:
        pass
