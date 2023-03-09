#!/usr/bin/env python3
import os
import openai
import webbrowser

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
	prompt = input("Input: ")
	response = openai.Image.create(
	  prompt=prompt,
	  n=1,
	  size="1024x1024"
	)
	image_url = response['data'][0]['url']
	print(prompt)
	print(image_url)
	webbrowser.open(image_url, new=0, autoraise=True)
