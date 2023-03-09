#!/usr/bin/env python3
import os
import openai

chatgpt = os.getenv("CHAT_GPT_API_KEY", None)
openai.api_key = chatgpt

def gen_response(prompt, model_engine="text-davinci-003"):
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
    ADA_MODEL = "text-davinci-002"
    with open("traning-data.txt", "r") as training_data_f:
        training_data = training_data_f.read()
        prompt = training_data + "\n\n" + input("Input: ")
        completion = gen_response(prompt, model_engine=ADA_MODEL)

        print_block = lambda title, body: print(f"{title}\n{'*' * 40}\n{body}\n{'*'*40}")
        print_block("Input", prompt)
        print()
        print_block("Response", repr(completion))

