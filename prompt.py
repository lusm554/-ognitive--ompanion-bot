#!/usr/bin/env python3
import os
import openai
import sys
from dotenv import load_dotenv

load_dotenv()
chatgpt = os.getenv("CHAT_GPT_API_KEY", None)
openai.api_key = chatgpt


def gen_response(prompt):
    model_engine = "text-davinci-003"
    prompt = (f"{prompt}")
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0,
    )
    message = completions.choices[0].text
    return message.strip() 

if __name__ == '__main__':
    input_text = sys.argv[1]
    resp = gen_response(input_text)
    print(f"Input: {input_text}")
    print(f"Response: {resp}")

