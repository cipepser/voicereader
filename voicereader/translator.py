
import openai

# 生成されるtokenとpromptのtoken数が合計したカウントがmax_tokensになる。
# https://platform.openai.com/docs/api-reference/completions/create
# サンプル的に日本語と英語でtoken数は3:1くらいになるので、text-davinci-002のmax_tokensは4097に対して、3072を設定

def translate_text_to_japanese(text: str, api_key: str) -> str:
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Translate the following English text to Japanese: '{text}'",
        temperature=0.7,
        max_tokens=3072,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    translated_text = response.choices[0].text.strip()
    return translated_text
