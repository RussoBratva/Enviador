from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from bot.cogs.modules.functions import data
import os
from bot.cogs.ban import *
import asyncio


def historico(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(f'⬇️ {button_download_history}', callback_data='baixar_historico')],
        [InlineKeyboardButton(f'◀︎ {button_main}', callback_data='main')],]
    
    query = update.callback_query
    user_info = query.from_user
    user_id = str(user_info['id'])
    if check_status(user_id):
        query.answer()
        user_info = query.from_user
        user_id = str(user_info['id'])
        user = asyncio.run(pesquisar_id(str(user_id)))
        saldo = user[1]
        qr = asyncio.run(recargas(user_id))
        ccs = asyncio.run(ccs_comprados(user_id))
        gifts = len(asyncio.run(pesquisar_gifts_resgatados(user_id)))
        
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=history_text.format(ccs, saldo, qr, gifts), parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=denied_text(user_id), parse_mode='Markdown')


def gerar_historico(user_id):
    user = asyncio.run(pesquisar_id(str(user_id)))
    saldo = user[1]
    qr = asyncio.run(recargas(user_id))
    ccs = asyncio.run(ccs_comprados(user_id))
    registrado_em = data(user[3])
    
    rows = asyncio.run(pesquisar_comprador(user_id))
    cartoes = []
    
    try:
        for row in rows:
            try:
                numero = row[1]
                expiracao = row[2]
                cvv = row[3]
                tipo = row[4]
                bandeira = row[5]
                categoria = row[6]
                banco = row[7]
                pais = row[8]
                cpf = row[9]
                nome = row[10]
                comprado_em = data(row[12])
                cartoes.append(history_cc_info_log.format(numero, expiracao, cvv, bandeira, tipo, categoria, banco, pais, cpf, nome, comprado_em))
            except: pass

    except: pass

    rows = asyncio.run(pesquisar_recargas(user_id))
    recargas1 = []
    
    rows2 = asyncio.run(pesquisar_gifts_resgatados(user_id))
    
    try:
        for row in rows2:
            tipo = 'Gift'
            recarga_de = row[1]
            recarregado_em = data(row[3])
            recargas1.append(history_gift_info_log.format(recarga_de, recarregado_em))
    except: pass

    try:
        for row in rows:
            recarga_de = row[1]
            order_id = row[2]
            recarregado_em = data(row[3])

            recargas1.append(history_pay_info_log.format(order_id, recarga_de, recarregado_em))

    except: pass

    if len(cartoes) == 0:
        lista_cartoes = f'\n{null_fields}\n'

    else:
        lista_cartoes = str(cartoes).replace("', ", "").replace("'", "").replace('[', '').replace(']', '').replace(r'\n', '\n')

    if len(recargas1) == 0:
        lista_recargas = f'\n{null_fields}\n'

    else:
        lista_recargas = str(recargas1).replace("', ", "").replace("'", "").replace('[', '').replace(']', '').replace(r'\n', '\n')

    qg = len(rows2)

    conteudo = history_log.format(registrado_em, ccs, saldo, qr, qg, lista_cartoes, lista_recargas)
    with open(f'temp/{user_id}.txt','w', encoding="utf8") as f:
        f.write(f'{conteudo}')
    
    return f'temp/{user_id}.txt'


def baixar_historico(update: Update, context: CallbackContext):
    query = update.callback_query
    user_info = query.from_user
    user_id = str(user_info['id'])
    data = str(query.data).replace('baixar_historico', '')
    
    if data == '':
        user_id_h = str(user_info['id'])
    else:
        user_id_h = data

    if check_status(user_id):
        try:
            caminho = gerar_historico(user_id_h)
            query.bot.send_document(chat_id=user_id, document=open(caminho,'rb'), caption=fixed_history_message_1, parse_mode='Markdown')
            query.bot.answer_callback_query(update.callback_query.id, text=download_history_alert, show_alert=True)

            try:
                os.remove(caminho)

            except:
                pass

        except Exception as e:
            print('Erro interno:', e)
            query.bot.send_message(chat_id=user_id, text=download_history_error, parse_mode='Markdown')

    else:
        try:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=denied_text(user_id), parse_mode='Markdown')
        except:
            update.message.reply_text(text=denied_text(user_id), parse_mode='Markdown')


