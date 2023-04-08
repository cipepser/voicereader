
import openai
import os

# APIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")

CONTENT = """
English content to be translated to Japanese.
"""

def translate_text_to_japanese(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Translate the following English text to Japanese: '{text}'",
        temperature=0.7,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    translated_text = response.choices[0].text.strip()
    return translated_text

if __name__ == "__main__":
    english_text = CONTENT
    japanese_text = translate_text_to_japanese(english_text)

    print(japanese_text)
