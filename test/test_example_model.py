import pytest, logging
from bot.model.example_model import ChatBotModel

@pytest.fixture
def chat_bot_model():
  model = ChatBotModel()
  return model

def test_recognize_command(chat_bot_model):
  assert chat_bot_model.recognize_command("start") == "start"
  assert chat_bot_model.recognize_command("help") == "help"
  assert chat_bot_model.recognize_command("end") == "end"
  assert chat_bot_model.recognize_command("this_cmd_does_not_exist") == None
  assert chat_bot_model.recognize_command("/end") == None # input should be only command name

def test_ask_question(chat_bot_model):
  assert chat_bot_model.ask_question() == "What would you like to know? Type '/help' for the list of available commands."

def test_process_message(chat_bot_model):
  # Test default vars
  assert chat_bot_model.state == "inactive"
  assert chat_bot_model.command_prefix == "/"
  assert chat_bot_model.commands == ("start", "help", "end")
  # Test when bot inactive (command /start not running first)
  assert chat_bot_model.process_message("hello") == "Please start the conversation using the /start command."
  assert chat_bot_model.process_message("/hello") == "Please start the conversation using the /start command."
  assert chat_bot_model.process_message("staart") == "Please start the conversation using the /start command."
  assert chat_bot_model.process_message("start/") == "Please start the conversation using the /start command."
  assert chat_bot_model.state == "inactive"
  # Test when bot active
  assert chat_bot_model.process_message("start") == "Hello! How can I help you?" # yeah, there some problems with prefix
  assert chat_bot_model.state == "active"
  assert chat_bot_model.process_message("not_found_command") == "What would you like to know? Type '/help' for the list of available commands." 
  assert chat_bot_model.process_message("/not_found_command") == "What would you like to know? Type '/help' for the list of available commands." 
  assert chat_bot_model.process_message("start") == "Grats, u run start command!"
  assert chat_bot_model.process_message("help") == "Grats, u run help command!"
  assert chat_bot_model.process_message("end") == "Grats, u run end command!"

