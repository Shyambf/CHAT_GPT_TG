#!/usr/bin/env python
import os
import openai
from background import keep_alive

import logging

from telegram import __version__ as TG_VER

try:
  from telegram import __version_info__
except ImportError:
  __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
  raise RuntimeError(
    f"This example is not compatible with your current PTB version {TG_VER}. To view the "
    f"{TG_VER} version of this example, "
    f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html")
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  level=logging.INFO)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.delete()
  await update.message.reply_text(
    f'Приветствуем Вас в боте\nФункционал нашего бота доступен только зарегестрированным пользователям, для регистрации пишите в лс \n@Shyam134\nВаш ID: `{update.message.chat_id}`'
  )


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.delete()
  await update.message.reply_text('Просто напишите ваш вопрос в чат')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  # await update.message.delete()
  if str(update.message.chat_id) in os.environ['users']:
    #mess = ProgressMsg(update.message, 'Генерация сообщения')
    openai.api_key = os.environ['open_ai_token']
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=[{
                                                "role":
                                                "user",
                                                "content":
                                                update.message.text
                                              }])
    #mess.finish()
    await update.message.reply_text(completion.choices[0].message.content)
  else:
    await update.message.reply_text('Вас нет в базе данных')


def main() -> None:
  """Start the bot."""
  keep_alive()
  # Create the Application and pass it your bot's token.
  application = Application.builder().token(os.environ['Bot_token']).build()

  # on different commands - answer in Telegram
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("help", help_command))

  # on non command i.e message - echo the message on Telegram
  application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                                         echo))

  # Run the bot until the user presses Ctrl-C
  application.run_polling()


if __name__ == "__main__":
  main()
