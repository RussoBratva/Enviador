from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.history import gerar_historico
import os
import asyncio


def encerrar_conta(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.callback_query
    user_info = query.from_user
    data = str(query.data).replace('encerrar_conta', '').replace('_sim', '').strip()
    tipo = 0
    
    if data == '':
        user_id = str(user_info['id'])
        user_nome = str(query.from_user['first_name'])
    else:
        user_id = data

        tipo = 1
        user_nome = asyncio.run(pesquisar_id(user_id))[2]


    if asyncio.run(check_config('manutencao'))[1] == '0':
        if 'encerrar_conta' in query.data and not '_sim' in query.data:
            keyboard = [
            [InlineKeyboardButton(f'✔️ {button_yes}', callback_data='encerrar_conta_sim'+user_id)],
            [InlineKeyboardButton(f'◀︎ {button_main}', callback_data='main')]]
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=delete_account_warning, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        elif 'encerrar_conta_sim' in query.data:

            try:
                if tipo == 0:
                    caminho = gerar_historico(user_id)
                    query.bot.send_document(chat_id=user_id, document=open(caminho,'rb'), caption=fixed_history_message_2, parse_mode='Markdown')
                    for dono in donos:
                        query.bot.send_document(chat_id=dono, document=open(caminho,'rb'), caption=fixed_history_message_3.format(user_nome, user_id), parse_mode='Markdown')
                    
                    try:
                        os.remove(caminho)
                    except:
                        pass
                
                asyncio.run(excluir_conta(user_id))
                keyboard = [[InlineKeyboardButton(f'🔎 Pesquisar por outro Usuário', switch_inline_query_current_chat='usuario ')]]
    
                if tipo == 0:
                    query.bot.send_message(chat_id=user_id, text=deleted_account, parse_mode='Markdown')

                else:
                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=deleted_account.replace('Sua', 'A')+f'\n\n*ID*: `{user_id}`\n*Nome*: `{user_nome}`', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

            except Exception as e:
                print('Erro interno:', e)
                query.bot.send_message(chat_id=user_id, text=delete_account_error, parse_mode='Markdown')

    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=maintenance, parse_mode='Markdown')

