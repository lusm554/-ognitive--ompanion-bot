import os
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import openai
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TELEGRAM_KEY", None)
chatgpt = os.getenv("CHAT_GPT_API_KEY", None)
openai.api_key = chatgpt

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def gen_response(prompt):
    model_engine = "text-davinci-003"
    prompt = (f"{prompt}")
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.8,
    )
    message = completions.choices[0].text
    return message.strip() 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Received command start")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_text = ' '.join(context.args)
    logging.info(f"Received command chat: {msg_text}")
    response = gen_response(msg_text)
    logging.info(f"Response command chat: {response}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    chat_handler = CommandHandler('chat', chat)
    application.add_handler(start_handler)
    application.add_handler(chat_handler)

    application.run_polling()
