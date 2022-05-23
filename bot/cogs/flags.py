from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.modules.database import *
import asyncio


def keyboard_flags():
    manutencao = check_flag_status(asyncio.run(check_config('manutencao'))[1])
    checker = check_flag_status(asyncio.run(check_config('checker'))[1])
    pix = check_flag_status(asyncio.run(check_config('pix'))[1])
    afiliado = check_flag_status(asyncio.run(check_config('afiliado'))[1])
    pesquisar_bandeira = check_flag_status(asyncio.run(check_config('pesquisar_bandeira'))[1])
    pesquisar_banco = check_flag_status(asyncio.run(check_config('pesquisar_banco'))[1])
    pesquisar_bin = check_flag_status(asyncio.run(check_config('pesquisar_bin'))[1])
    checker_publico = check_flag_status(asyncio.run(check_config('checker_publico'))[1])
    auto_live = check_flag_status(asyncio.run(check_config('auto_live'))[1])
    qrcode = check_flag_status(asyncio.run(check_config('qrcode'))[1])
    troca = check_flag_status(asyncio.run(check_config('troca'))[1])
    
    keyboard = [
        [InlineKeyboardButton(f'{manutencao[1]} M. Manutenção - {manutencao[0]}', callback_data='flag_manutencao'),
        InlineKeyboardButton(f'{checker[1]} Checker - {checker[0]}', callback_data='flag_checker')],
        [InlineKeyboardButton(f'{pix[1]} PIX - {pix[0]}', callback_data='flag_pix'),
        InlineKeyboardButton(f'{afiliado[1]} M. Afiliado - {afiliado[0]}', callback_data='flag_afiliado')],
        [InlineKeyboardButton(f'{pesquisar_bandeira[1]} P. por bandeira - {pesquisar_bandeira[0]}', callback_data='flag_pesquisar_bandeira'),
        InlineKeyboardButton(f'{pesquisar_banco[1]} P. por banco - {pesquisar_banco[0]}', callback_data='flag_pesquisar_banco')],
        [InlineKeyboardButton(f'{pesquisar_bin[1]} P. por bin - {pesquisar_bin[0]}', callback_data='flag_pesquisar_bin'),
        InlineKeyboardButton(f'{checker_publico[1]} CHK Público - {checker_publico[0]}', callback_data='flag_checker_publico')],
        [InlineKeyboardButton(f'{auto_live[1]} Escolha de live - {auto_live[0]}', callback_data='flag_auto_live'),
        InlineKeyboardButton(f'{qrcode[1]} Geração de QRcode - {qrcode[0]}', callback_data='flag_qrcode')],
        [InlineKeyboardButton(f'{troca[1]} Troca de CCs - {troca[0]}', callback_data='flag_troca')]
        ]

    return keyboard


def check_flag_status(status):
    if status == '1':
        return 'ON', '🟢'
    
    elif status == '0':
        return 'OFF', '🔴'
    
    else:
        return '', '❌'


def flags(update: Update, context: CallbackContext):
    query = update.message

    if query is None:
        query = update.callback_query
        user_info = query.from_user

    else:
        user_info = query.from_user
        
    try:
        query_data = query.data
    except:
        query_data = None
    
    nome = str(user_info['first_name'])
    user_id = str(user_info['id'])
    donos = adm_list()
    
    if user_id in donos:
        text = '⚙️ | *Configurações do bot*\n\nLigue ou desligue recursos do bot interagindo com os botões!'
        if query_data is None:
            keyboard = keyboard_flags()
            update.message.reply_text(text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            data = str(query_data).replace('flag_', '')
            check = asyncio.run(check_config(data))
            if check is not None:
                condicao_atual = check[1]
                if condicao_atual == '1':
                    condicao = '0'
                    asyncio.run(config_change(data, condicao))
                elif condicao_atual == '0':
                    condicao = '1'
                    asyncio.run(config_change(data, condicao))
                
                keyboard = keyboard_flags()
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

            

