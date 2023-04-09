
import openai

class OpenAIError(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(f"An error occurred in the other library: {original_exception}")

# 生成されるtokenとpromptのtoken数が合計したカウントがmax_tokensになる。
# https://platform.openai.com/docs/api-reference/completions/create
# サンプル的に日本語と英語でtoken数は3:1くらいになるので、text-davinci-002のmax_tokensは4097に対して、3072を設定

def translate_text_to_japanese(text: str, api_key: str) -> str:
    openai.api_key = api_key

    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Translate the following English text to Japanese: '{text}'",
            temperature=0.7,
            max_tokens=4097,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
    except Exception as e:
        raise OpenAIError(e)

    translated_text = response.choices[0].text.strip()
    return translated_text
