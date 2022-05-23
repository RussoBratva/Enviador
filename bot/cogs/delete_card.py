from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from bot.cogs.modules.adm_list import adm_list
import asyncio


def delete_card(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.callback_query
    user_info = query.from_user
    user_id = str(user_info['id'])
    cc_id = str(query.data).replace('remove_', '')
    
    if user_id in donos:
        row = asyncio.run(pesquisar_cc_id(cc_id))
        if row is not None:
            numero = row[1]
            expiracao = row[2]
            cvv = row[3]
            cartao = f'{numero}|{expiracao}|{cvv}'.replace('/', '|')
            delete = asyncio.run(remove_cc(numero))
            if delete:
                keyboard = [[InlineKeyboardButton(f'◀︎ Menu de unitárias', callback_data='unitaria')]]
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'Cartão excluído!\n\n*Cartão*: `{cartao}`', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
            
            else:
                query.bot.answer_callback_query(update.callback_query.id, text=f'❕ Ocorreu um erro ao deletar esse cartão!', show_alert=True)

        else:
            query.bot.answer_callback_query(update.callback_query.id, text=f'❕ Cartão não encontrado na base de dados!', show_alert=True)

    else:
        query.bot.answer_callback_query(update.callback_query.id, text=f'❕ Só administradores podem usar esse botão!', show_alert=True)


def delete_all_cards(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(f'✔️ Deletar todo o estoque!', callback_data='delete_cards_yes')],
        [InlineKeyboardButton(f'◀︎ {button_main}', callback_data='main')]]

    query = update.message
    query_data = ''
    
    if query is None:
        query = update.callback_query
        query_data = query.data
        
    user_info = query.from_user
    user_id = str(user_info['id'])
    donos = adm_list()

    if user_id in donos:
            
        if query_data == '':
            update.message.reply_text(text='⚠️ | *Deletar cartões!*\n\nTem certeza que deseja apagar todos os cartões do estoque do bot?\n\nPS: Os cartões já comprados não serão deletados!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        if query_data == 'delete_cards_yes':
            cartoes = asyncio.run(all_ccs())

            contador_erros = 0
            contador = 0
            
            for cartao in cartoes:
                numero = cartao[1]
                delete = asyncio.run(remove_cc(numero))
                
                if delete:
                    contador += 1
                else:
                    contador_erros += 1
                
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'🗑️ | *Cartões excluídos!*\n\n*Cartões deletados*: `{contador}`\n*Erros*: `{contador_erros}`', parse_mode='Markdown')

