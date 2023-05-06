import os
import sys
from pathlib import Path
import logging

root_path = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root_path))

from voicereader.implementations.destination.qiita_pocket import QiitaPocketDestinator
from voicereader.implementations.translator.openai import OpenAITranslator, OpenAIError
from voicereader.implementations.source.hacker_news import HackerNewsExtractor

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s',
    level=logging.INFO
)

if __name__ == "__main__":
    translator = OpenAITranslator(api_key=os.getenv("API_KEY_OPENAI"))
    destinator = QiitaPocketDestinator(
        qiita_access_token=os.getenv("ACCESS_TOKEN_QIITA"),
        pocket_consumer_key=os.getenv("CONSUMER_KEY_POCKET"),
        pocket_access_token=os.getenv("ACCESS_TOKEN_POCKET")
    )

    try:
        untranslated_transactions = HackerNewsExtractor().extract()
    except Exception as e:
        logging.error(e)
        sys.exit(1)

    logging.info(f"{len(untranslated_transactions)} articles has found")
    for untx in untranslated_transactions:
        try:
            logging.info(f"start translation: {untx.get_title()}")
            tx = translator.translate(untx)
            logging.info(f"translated: {tx.get_title()}")
        except OpenAIError as e:
            logging.warning(e)
            continue
        except Exception as e:
            logging.error(e)
            sys.exit(1)

        try:
            url = destinator.create_private_article(tx)
            logging.info(f"created Qiita article, url: {url}")
        except Exception as e:
            logging.error(e)
            sys.exit(1)

        try:
            if url:
                destinator.send_to_reader(str(url))
                logging.info(f"sent to Pocket")
        except Exception as e:
            logging.error(e)
            sys.exit(1)
