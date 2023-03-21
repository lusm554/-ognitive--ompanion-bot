from controller.cli_controller import ChatBotControllerCLI
import logging

try:
  bot = ChatBotControllerCLI()
  bot.handle_message("/selectusers")
except Exception as e:
  logging.exception(e)
