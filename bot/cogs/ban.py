from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from bot.cogs.modules.adm_list import adm_list
import asyncio



def ban(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.callback_query
    user_id_add = query.data.replace('ban_', '')
    user_info = query.from_user
    user_id = str(user_info['id'])
    keyboard = [[InlineKeyboardButton(f'◀︎ {button_back}', callback_data='usuario_'+user_id_add)],]
    
    if user_id in donos:
        pesquisar = asyncio.run(pesquisar_ban(user_id_add))
        if pesquisar is None:
            asyncio.run(registrar_ban(user_id_add))
            user = asyncio.run(pesquisar_id(user_id_add))
            nome = user[2]
            
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'🚫 | *Restrição*\n\nUsuário banido!\n\n*Nome*: `{nome}`\n*ID*: `{user_id_add}`', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'🚫 | *Restrição*\n\nEsse usuário já está banido!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


def unban(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.callback_query

    user_id_add = query.data.replace('unban_', '')
    user_info = query.from_user
    user_id = str(user_info['id'])
    if user_id in donos:
        pesquisar = asyncio.run(pesquisar_ban(user_id_add))
        keyboard = [[InlineKeyboardButton(f'◀︎ {button_back}', callback_data='usuario_'+user_id_add)],]
        if not pesquisar is None:
            remove = asyncio.run(remove_ban(user_id_add))
            user = asyncio.run(pesquisar_id(user_id_add))
            nome = user[2]
            
            if remove:
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'🚫 | *Restrição*\n\nUsuário desbanido com sucesso!\n\n*Nome*: `{nome}`\n*ID*: `{user_id_add}`', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

            else:
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'🚫 | *Restrição*\n\nOcorreu um erro ao desbanir esse usuário!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'🚫 | *Restrição*\n\nEsse usuário não está banido!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))



def check_status(user_id):
    if asyncio.run(pesquisar_ban(user_id)) is not None:
        return False
    elif not asyncio.run(check_config('manutencao'))[1] == '0':
        return False
    else:
        return True


def denied_text(user_id):
    donos = adm_list()
    if asyncio.run(pesquisar_ban(user_id)) is not None and not user_id in donos:
        return '🚫 | *Você foi restringido de usar o bot*\n\nUm administrador restringiu você por tempo indeterminado de poder usar esse bot!'
    elif not asyncio.run(check_config('manutencao'))[1] == '0':
        return maintenance
    else:
        return 'Ocorreu um erro temporario ao executar esse comando, refaça-o!'


