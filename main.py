import os
import logging
import asyncio
import random

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from fastapi import FastAPI, Request

from telegram import Update, ForceReply, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BotToken = os.getenv("TOKEN")

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def roll(update: Update, context: CallbackContext) -> None:
    """Roll dice. /roll 6"""
    if not context.args:
        number = 6
    elif not context.args[0].isdecimal():
        number = 6
    else:
        number = int(context.args[0])
    result_number = random.randint(1, number)
    await update.message.reply_text(f'Roll dice from 1 to {number}\nResult = {result_number}')

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

async def inline_button_ex(update: Update, context: CallbackContext) -> None:
    show_list = []
    show_list.append(InlineKeyboardButton("50", callback_data="50"))
    show_list.append(InlineKeyboardButton("100", callback_data="100"))
    show_list.append(InlineKeyboardButton("200", callback_data="200"))
    show_list.append(InlineKeyboardButton("300", callback_data="300"))
    show_list.append(InlineKeyboardButton("400", callback_data="400"))
    show_list.append(InlineKeyboardButton("cancel", callback_data="cancel"))
    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup
    
    await update.message.reply_text("Select Input", reply_markup=show_markup)

async def callback_inline_button_ex(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.edit_message_text(text=f"Selected option: {query.data}")

def get_application():
    application = Application.builder().token(BotToken).build()
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("roll", roll))
    application.add_handler(CommandHandler("button", inline_button_ex))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # on UI callback
    application.add_handler(CallbackQueryHandler(callback_inline_button_ex, pattern=r"(\d+|cancel)"))
    return application

application = get_application()

app = FastAPI()

@app.post("/webhook")
async def webhook_handler(req: Request):
    data = await req.json()
    async with application:
        # set bot commands menu
        ## BotCommand("command", "description")
        await application.bot.set_my_commands(
            [
                BotCommand("start", "Start the bot"),
                BotCommand("help", "Help message"),
                BotCommand("roll", "Roll dice. /roll [int=6]"),
                BotCommand("button", "InlineButton example. /button")
            ]
        )
        await application.start()
        await application.process_update(Update.de_json(data=data, bot=application.bot))
        await application.stop()
