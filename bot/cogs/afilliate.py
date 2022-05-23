from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
import urllib.parse
import asyncio


def afiliados(update: Update, context: CallbackContext):
    query = update.callback_query
    bot_info = query.message.bot
    bot_username = str(bot_info.username).replace('_', '\_')
    user_info = query.from_user
    user_id = str(user_info['id'])
    if asyncio.run(check_config('manutencao'))[1] == '0':
        if asyncio.run(check_config('afiliado'))[1] == '1':
            q = asyncio.run(lista_indicados(user_id))
            texto = urllib.parse.quote(afiliate_invite_text.format(bot_username, user_id))

            keyboard = [
                [InlineKeyboardButton(f'🔗 {button_share}', url='https://t.me/share/url?url=%20&text={}'.format(texto, bot_username.replace('\_', '_'), user_id))],
                [InlineKeyboardButton(f'◀︎ {button_back}', callback_data='main')],]

            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=affliate_text.format(bot_username, user_id, q), parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            keyboard = [[InlineKeyboardButton(f'◀︎ {button_main}', callback_data='main')],]
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='❌ | *Erro*\n\no sistema de afiliados foi desativado!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=maintenance, parse_mode='Markdown')

