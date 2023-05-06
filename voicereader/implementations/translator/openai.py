
import openai
import logging
from voicereader.protocols.source import UntranslatedTransaction
from voicereader.protocols.translator import Translator, TranslatedTransaction

class OpenAIError(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(f"An error occurred in the other library: {original_exception}")

class OpenAITranslator(Translator):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def translate(self, transaction: UntranslatedTransaction) -> TranslatedTransaction:
        return TranslatedTransaction(
            title=transaction.get_title(),
            article_text_jp=translate_to_japanese(transaction.get_article_text_jp(), self.api_key),
            tag=transaction.get_tag()
        )

# 生成されるtokenとpromptのtoken数が合計したカウントがmax_tokensになる。
# https://platform.openai.com/docs/api-reference/completions/create
# サンプル的に日本語と英語でtoken数は3:1くらいになるので、text-davinci-003のmax_tokensは4097に対して、3072を設定
def translate_to_japanese(text: str, api_key: str) -> str:
    openai.api_key = api_key

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Translate the following English text to Japanese: '{text}'",
            temperature=0.7,
            max_tokens=3072,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
    except Exception as e:
        raise OpenAIError(e)

    translated_text = response.choices[0].text.strip()
    return translated_text
