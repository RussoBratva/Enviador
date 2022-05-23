from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from bot.cogs.modules.functions import data
from bot.cogs.ban import *
import asyncio


def informacoes(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(f'💵 {button_add_credits}', callback_data='adicionar_saldo'),
        InlineKeyboardButton(f'⚠️ {button_delete_account}', callback_data='encerrar_conta')]]
    query = update.callback_query
    
    if asyncio.run(check_config('afiliado'))[1] == '1':
        keyboard.append([InlineKeyboardButton(f'👥 {button_affliates}', callback_data='afiliados')])
    
    keyboard.append([InlineKeyboardButton(f'◀︎ {button_main}', callback_data='main')])
    user_info = query.from_user
    nome = str(user_info['first_name'])
    user_id = str(user_info['id'])
    nome = str(user_info['first_name'])
    
    if check_status(user_id):
        query.answer()

        asyncio.run(registrar_usuario(user_id, nome))
        asyncio.run(name_update(user_id, nome))
        user = asyncio.run(pesquisar_id(str(user_id)))
        saldo = user[1]
        registrado_em = data(user[3])
        ccs = asyncio.run(ccs_comprados(user_id))
        qr = asyncio.run(recargas(user_id))
        gifts = len(asyncio.run(pesquisar_gifts_resgatados(user_id)))
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=profile_info.format(nome, user_id, registrado_em, saldo, ccs, qr, gifts), parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=denied_text(user_id), parse_mode='Markdown')



