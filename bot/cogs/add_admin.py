from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.database import *
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.adm_list import adm_list
import asyncio
import logging


def add_admin(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message
    try:
        user_id_add = update.message.text.split()[1]
        user_info = query.from_user
        user_id = str(user_info['id'])
        if user_id in donos:
            pesquisar = asyncio.run(pesquisar_adm(user_id_add))
            if pesquisar is None:
                asyncio.run(registrar_adm(user_id_add))
                user = asyncio.run(pesquisar_id(user_id_add))
                
                if user is not None:
                    nome = user[2]
                else:
                    nome = 'Não registrado'
                    
                if not nome == 'Não registrado':
                    try:
                        query.bot.send_message(chat_id=user_id_add, text='🌟 | *Administraçao*\n\nVocê foi adicionado como administrador nesse bot!')
                    except:
                        pass
                
                update.message.reply_text(text=f'🌟 | *Administraçao*\n\nNovo usuário registrado com sucesso como administrador!\n\n*Nome*: `{nome}`\n*ID*: `{user_id_add}`', parse_mode='Markdown')

            else:
                update.message.reply_text(text=f'🌟 | *Administraçao*\n\nEsse usuário já está registrado como administrador!', parse_mode='Markdown')

    except:
        user_info = query.from_user
        user_id = str(user_info['id'])
        if user_id in donos:
            update.message.reply_text(text=f'🌟 | *Administraçao*\n\nDigite um id de usuário válido para poder adicionar esse ID ao banco de dados!', parse_mode='Markdown')




def remove_admin(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message
    try:
        user_id_add = update.message.text.split()[1]
        user_info = query.from_user
        user_id = str(user_info['id'])
        if user_id in donos:
            pesquisar = asyncio.run(pesquisar_adm(user_id_add))
            if pesquisar is not None:
                remove = asyncio.run(remove_adm(user_id_add))
                user = asyncio.run(pesquisar_id(user_id_add))
                
                if user is not None:
                    nome = user[2]
                else:
                    nome = 'Não registrado'
                
                if remove:
                    if not nome == 'Não registrado':
                        try:
                            query.bot.send_message(chat_id=user_id_add, text='🌟 | *Administraçao*\n\nVocê foi removido como administrador nesse bot!', parse_mode='Markdown')
                        except:
                            pass
                    
                    update.message.reply_text(text=f'🌟 | *Administraçao*\n\nUsuário removido com sucesso como administrador!\n\n*Nome*: `{nome}`\n*ID*: `{user_id_add}`', parse_mode='Markdown')

                else:
                    update.message.reply_text(text=f'🌟 | *Administraçao*\n\nOcorreu um erro ao remover esse usuário como administrador!', parse_mode='Markdown')

            else:
                update.message.reply_text(text=f'🌟 | *Administraçao*\n\nEsse usuário não está registrado como administrador!', parse_mode='Markdown')

    except:
        user_info = query.from_user
        user_id = str(user_info['id'])
        if user_id in donos:
            update.message.reply_text(text=f'🌟 | *Administraçao*\n\nDigite um id de usuário válido para poder adicionar esse ID ao banco de dados!', parse_mode='Markdown')


def add_admin_button(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.callback_query
    user_id_add = query.data.replace('add_admin_', '')
    user_info = query.from_user
    user_id = str(user_info['id'])
    keyboard = [[InlineKeyboardButton(f'◀︎ {button_back}', callback_data='usuario_'+user_id_add)],]
    
    if user_id in donos:
        pesquisar = asyncio.run(pesquisar_adm(user_id_add))
        if pesquisar is None:
            asyncio.run(registrar_adm(user_id_add))
            user = asyncio.run(pesquisar_id(user_id_add))
            nome = user[2]
            
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'🌟 | *Administraçao*\n\nNovo usuário registrado com sucesso como administrador!\n\n*Nome*: `{nome}`\n*ID*: `{user_id_add}`', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'🌟 | *Administraçao*\n\nEsse usuário já está registrado como administrador!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


def remove_admin_button(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.callback_query

    user_id_add = query.data.replace('rm_admin_', '')
    user_info = query.from_user
    user_id = str(user_info['id'])
    if user_id in donos:
        pesquisar = asyncio.run(pesquisar_adm(user_id_add))
        keyboard = [[InlineKeyboardButton(f'◀︎ {button_back}', callback_data='usuario_'+user_id_add)],]
        if not pesquisar is None:
            remove = asyncio.run(remove_adm(user_id_add))
            user = asyncio.run(pesquisar_id(user_id_add))
            nome = user[2]
            
            if remove:
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'🌟 | *Administraçao*\n\nUsuário removido com sucesso como administrador!\n\n*Nome*: `{nome}`\n*ID*: `{user_id_add}`', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

            else:
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'🌟 | *Administraçao*\n\nOcorreu um erro ao remover esse usuário como administrador!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'🌟 | *Administraçao*\n\nEsse usuário não está registrado como administrador!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))



