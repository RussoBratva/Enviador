from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.database import *
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.group_list import group_list
from bot.cogs.modules.adm_list import adm_list
import asyncio


def add_groups(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message
    chat = str(update.message.chat['type'])
    
    if chat == 'group' or chat == 'supergroup':
        user_info = update.message.from_user
        user_id = str(user_info['id'])
        if user_id in donos:
            id_group = str(update.message.chat['id'])
            asyncio.run(add_group(str(id_group)))
            update.message.reply_text(text='Esse grupo será notificado!', parse_mode='Markdown')

        else:
            update.message.reply_text(text='Você não tem permissão para usar esse comando!', parse_mode='Markdown')





