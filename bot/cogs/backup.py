from telegram.ext import ConversationHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.modules.functions import *
from bot.cogs.modules.save_backup import *
from time import time
import os


def download_backup(update: Update, context: CallbackContext):
    query = update.message
    user_info = query.from_user
    user_id = str(user_info['id'])
    
    text = '💾 | *Backup baixado*\n\nO arquivo de backup do bot foi anexado a essa mensagem!\n\n*Data do backup*: `{}`\n\nCaso seja necessário envie esse arquivo ao bot para restaurar o backup!'
    text2 = '💾 | *Arquivo não encontrado!*\n\nNão foi possível baixar um backup, pois o arquivo de backup não foi encontrado!\n\nEntre em contato com o suporte do bot para resolver o problema!'
    text3 = '💾 | *Erro ao executar comando de backup*\n\nOcorreu um erro interno ao baixar o backup, entre em contato com o suporte para resolver o problema caso ele percista!\n\n*Log do erro*: `{}`'
    
    try:
        if user_id in adm_list():
            tempo = str(time())
            hora = data(tempo)
            
            caminho = 'database.db'
            if os.path.isfile(caminho):
                query.bot.send_document(chat_id=user_id, document=open(caminho,'rb'), caption=text.format(hora), parse_mode='Markdown')

            else:
                update.message.reply_text(text=text2, parse_mode='Markdown')

    except Exception as e:
        update.message.reply_text(text=text3.format(e), parse_mode='Markdown')


def upload_backup(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message
    user_info = query.from_user
    user_id = str(user_info['id'])

    if user_id in donos:
        path = f"temp/backup-{user_id}.db"
        with open(path, 'wb') as f:
            context.bot.get_file(update.message.document).download(out=f)

        backup = install_backup(path)

        ccs = backup[1]
        usuarios = backup[2]
        recarga = backup[3]
        precos = backup[4]
        afiliados = backup[5]
        mix = backup[6]
        administrador = backup[7]
        gifts = backup[8]
        grupos = backup[9]
        erros = backup[11]

        update.message.reply_text(text=f'💾 | *Backup instalado!*\n\nVeja abaixo as tabelas no banco de dados que foram adicionadas a DB\n\n*CCs*: `{ccs}`\n*usuários*: `{usuarios}`\n*Recargas*: `{recarga}`\n*Preços CCs*: `{precos}`\n*Afiliados*: `{afiliados}`\n*MIX*: `{mix}`\n*Administradores*: `{administrador}`\n*Gifts*: `{gifts}`\n*Grupos*: `{grupos}`\n\n*Erros na instalação*: `{erros}`', parse_mode='Markdown')



