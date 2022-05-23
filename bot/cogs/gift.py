from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.modules.database import *
from bot.cogs.modules.group_list import group_list
import urllib.parse
import asyncio


def gerar_gift(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message
    user_info = query.from_user
    user_id = str(user_info['id'])
    
    if user_id in donos:
        try:
            valor = update.message.text.split()
            
            if valor[1].isnumeric():
                gift = asyncio.run(gen_gift(valor[1]))
                text = gift_gen.format(valor[1], gift, gift)
                
                texto = urllib.parse.quote(text)
                keyboard = [[InlineKeyboardButton(f'🔗 {button_share_message}', url=f'https://t.me/share/url?url=%20&text={texto}')]]

                update.message.reply_text(text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

            else:
                update.message.reply_text(text=gift_error_2, parse_mode='Markdown')

        except:
            update.message.reply_text(text=gift_error_2, parse_mode='Markdown')


def adicionar_gift(update: Update, context: CallbackContext):
    grupos = group_list()
    query = update.message
    user_info = query.from_user
    user_id = str(user_info['id'])
    nome = str(user_info['first_name'])

    try:
        gift = update.message.text.split()[1]
        resgatar = asyncio.run(resgatar_gift(gift, user_id))
        gp = gift[18:]

        if resgatar[0] == True:
            valor = asyncio.run(pesquisar_gift(gift))[1]
            saldo = asyncio.run(pesquisar_id(user_id))[1]
            update.message.reply_text(text=gift_added.format(valor, saldo), parse_mode='Markdown')

            for grupo in grupos:
                try:
                    query.bot.send_message(chat_id=grupo, text=gift_group_alert.format(nome, user_id, gp, valor), parse_mode='Markdown')
                except Exception as e:
                    print(e)
                    pass
        else:
            if resgatar[1] == '2':
                update.message.reply_text(text=gift_error_1, parse_mode='Markdown')

            elif resgatar[1] == '1':
                gift = asyncio.run(pesquisar_gift(gift))[2]
                usuario = asyncio.run(pesquisar_id(gift))[2]
                update.message.reply_text(text=gift_error_3.format(usuario), parse_mode='Markdown')

    except Exception as e:
        print(e)
        gift = asyncio.run(pesquisar_gift(gift))[2]
        if gift == 'None':
            update.message.reply_text(text=gift_error_1, parse_mode='Markdown')





