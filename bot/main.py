from model.example_model import ChatBotModel
from view.example_view import ChatBotView
from controller.example_controller import ChatBotController
import logging

#model = ChatBotModel()
#print(model)
#
#view = ChatBotView()
#print(view)
#
#controller = ChatBotController()
#print(controller)

try:
  bot = ChatBotController()
  bot.handle_message("hello")
  bot.handle_message("start")
  bot.handle_message("end")
  bot.handle_message("help")
except Exception as e:
  logging.exception(e)
