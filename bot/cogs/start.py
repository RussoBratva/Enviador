from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from bot.cogs.modules.support import *
from bot.cogs.ban import *
import asyncio


with open('config/config.json', 'r', encoding='UTF-8') as file_config:
    load = json.loads(file_config.read())
    footer_text = load['footer_text']



def start(update: Update, context: CallbackContext):
    query = update.message
    bot_info = query.bot
    bot_first_name = str(bot_info['first_name'])
    user_info = query.from_user
    nome = str(user_info['first_name'])
    user_id = str(user_info['id'])

    if check_status(user_id):
        
        try:
            asyncio.run(name_update(user_id, nome))
        except:
            pass
        
        texto = update.message.text.split()
        try:
            if asyncio.run(check_config('afiliado'))[1] == '1':
                afiliado = texto[1]
                if afiliado.isnumeric():
                    asyncio.run(add_afiliado(afiliado, user_id))

        except:
            pass

        keyboard = [[
            InlineKeyboardButton(f'💳 {button_buy}', callback_data='m1'), 
            InlineKeyboardButton(f'💵 {button_add_credits}', callback_data='adicionar_saldo')],
            [InlineKeyboardButton(f'📃 {button_history}', callback_data='m3'),
            InlineKeyboardButton(f'👤 {button_info}', callback_data='m2')],]
        
        if asyncio.run(check_config('afiliado'))[1] == '1':
            keyboard.append([InlineKeyboardButton(f'🧰 Ferramentas', callback_data='ferramentas'), InlineKeyboardButton(f'👥 {button_affliates}', callback_data='afiliados')])
            keyboard.append([InlineKeyboardButton(f'🔧 Suporte', url='https://t.me/{}'.format(str(support().replace('@', ''))))])
        
        else:
            keyboard.append([InlineKeyboardButton(f'🧰 Ferramentas', callback_data='ferramentas'), InlineKeyboardButton(f'🔧 Suporte', url='https://t.me/{}'.format(str(support().replace('@', ''))))])


        keyboard2 = [[InlineKeyboardButton(f'✔️ {button_accept_terms}', callback_data='termos'),]]

        if not asyncio.run(pesquisar_id(user_id)) == None:
            update.message.reply_text(text=main_text.format(bot_first_name, nome, support().replace('_', '\_'), footer_text), parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            update.message.reply_text(text=terms, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard2))

    else:
        update.message.reply_text(text=denied_text(user_id), parse_mode='Markdown')


def menu(update: Update, context: CallbackContext):
        
    keyboard = [[
        InlineKeyboardButton(f'💳 {button_buy}', callback_data='m1'), 
        InlineKeyboardButton(f'💵 {button_add_credits}', callback_data='adicionar_saldo')],
        [InlineKeyboardButton(f'📃 {button_history}', callback_data='m3'),
        InlineKeyboardButton(f'👤 {button_info}', callback_data='m2')],]
    
    if asyncio.run(check_config('afiliado'))[1] == '1':
        keyboard.append([InlineKeyboardButton(f'🧰 Ferramentas', callback_data='ferramentas'), InlineKeyboardButton(f'👥 {button_affliates}', callback_data='afiliados')])
        keyboard.append([InlineKeyboardButton(f'🔧 Suporte', url='https://t.me/{}'.format(str(support().replace('@', ''))))])
    
    else:
        keyboard.append([InlineKeyboardButton(f'🧰 Ferramentas', callback_data='ferramentas'), InlineKeyboardButton(f'🔧 Suporte', url='https://t.me/{}'.format(str(support().replace('@', ''))))])


    query = update.callback_query
    bot_info = query.message.bot
    bot_first_name = str(bot_info.first_name)
    user_info = query.from_user
    nome = str(user_info['first_name'])
    user_id = str(user_info['id'])
        
    if check_status(user_id):
        
        if query.data == 'termos':
            asyncio.run(registrar_usuario(user_id, nome))
            asyncio.run(name_update(user_id, nome))
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=main_text.format(bot_first_name, nome, support().replace('_', '\_'), footer_text), parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=main_text.format(bot_first_name, nome, support().replace('_', '\_'), footer_text), parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=denied_text(user_id), parse_mode='Markdown')




