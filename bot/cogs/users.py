from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from bot.cogs.modules.functions import data
from bot.cogs.modules.adm_list import *
import os
import asyncio


def baixar_usuarios(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message
    user_info = query.from_user
    user_id_author = str(user_info['id'])

    try:
        if user_id_author in donos:
            usuarios = asyncio.run(all_users())
            results = []

            for usuario in usuarios:
                user_id = usuario[0]
                saldo = usuario[1]
                nome = usuario[2]

                results.append(f'Nome: {nome}\nID: {user_id}\nSaldo: R${saldo},00')
                
            with open('temp/usuarios.txt', 'w', encoding="utf-8") as file:
                numero_usuarios = len(results)
                file.write(f'Lista de usuários do bot:\n\nTotal de usuários: {numero_usuarios}\n\n'+'\n\n'.join(results))

            context.bot.send_document(chat_id=user_id_author, document=open(f'temp/usuarios.txt','rb'), caption='Relatório gerado, baixe o relatório para visualizar os dados dos usuários existentes nas bases de dados!', parse_mode='Markdown')
            os.remove('temp/usuarios.txt')

    except Exception as e:
        print(e)
        update.message.reply_text(text='❌ | *Erro*\n\nOcorreu um erro na execução deste comando, contate o desenvolvedor do bot se esse problema percistir!', parse_mode='Markdown')


def resaldo(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message
    user_info = query.from_user
    user_id_author = str(user_info['id'])

    if user_id_author in donos:
        try:
            content = update.message.text.split()
            user_id = content[1]
            saldo = content[2]
            if saldo.isnumeric():
                pesquisa = asyncio.run(pesquisar_id(user_id))
                if pesquisa is not None:
                    if int(pesquisa[1]) >= int(saldo):
                        asyncio.run(subtrair_saldo(user_id, int(saldo)))
                        update.message.reply_text(text=f'Foram descontados R${saldo},00 de saldo do usuário {pesquisa[2]}, que agora possui: R${int(pesquisa[1])-int(saldo)},00', parse_mode='Markdown')

                    else:
                        update.message.reply_text(text='❌ | *Erro*\n\nNão é possível subtrair o saldo des usuário, pois o valor de subtração é maior que o saldo em conta.', parse_mode='Markdown')
                    
                else:
                    update.message.reply_text(text='❌ | *Erro*\n\nEsse ID de usuário não foi encontrado no banco de dados!', parse_mode='Markdown')

            else:
                update.message.reply_text(text='❌ | *Erro*\n\nDigite o saldo em números para subtrairmos!', parse_mode='Markdown')

        except Exception as e:
            print(e)
            update.message.reply_text(text='❌ | *Erro*\n\nOcorreu um erro na execução deste comando, contate o desenvolvedor do bot se esse problema percistir!', parse_mode='Markdown')


def usuario(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message

    tipo = 0

    if query is None:
        tipo = 1
        query = update.callback_query
        
    user_info = query.from_user
    user_id_author = str(user_info['id'])
    if user_id_author in donos:
        try:
            if tipo == 0:
                content = update.message.text.split()[1]
            else:
                content = str(query.data).replace('usuario_', '')

            user_id = content
            user = asyncio.run(pesquisar_id(user_id))
            if user is not None:
                saldo = user[1]
                registrado_em = data(user[3])
                nome = user[2]
                ccs = asyncio.run(ccs_comprados(user_id))
                qr = asyncio.run(recargas(user_id))
                gifts = len(asyncio.run(pesquisar_gifts_resgatados(user_id)))
                texto = f'👤 | *Perfil*\n\n- *Nome*: `{nome}`\n- *ID*: `{user_id}`\n- *Registrado em:* `{registrado_em}`\n\n💰 | *Carteira*\n\n- *Saldo*: `R${saldo},00`\n- *Compras*: `{ccs}`\n- *Recargas*: `{qr}`\n- *Gifts resgatados*: `{gifts}`'
                
                if not user_id == user_id_author:
                    if not user_id in donos:
                        keyboard = [
                            [InlineKeyboardButton(f'🌟 Promover para ADM', callback_data='add_admin_'+user_id),
                            InlineKeyboardButton(f'⬇️ Baixar histórico', callback_data='baixar_historico'+user_id)],]
                    
                    else:
                        keyboard = [
                            [InlineKeyboardButton(f'🌟 Remover ADM', callback_data='rm_admin_'+user_id),
                            InlineKeyboardButton(f'⬇️ Baixar histórico', callback_data='baixar_historico'+user_id)],]

                    if asyncio.run(pesquisar_ban(user_id)) is None:
                        keyboard.append([InlineKeyboardButton(f'🚫 Banir usuário', callback_data='ban_'+user_id),
                        InlineKeyboardButton(f'⚠️ Deletar conta', callback_data='encerrar_conta'+user_id)],)
                    
                    else:
                        keyboard.append([InlineKeyboardButton(f'🚫 Desbanir usuário', callback_data='unban_'+user_id),
                        InlineKeyboardButton(f'⚠️ Deletar conta', callback_data='encerrar_conta'+user_id)],)

                else:
                    keyboard = [[InlineKeyboardButton(f'⬇️ Baixar histórico', callback_data='baixar_historico'+user_id)],]

                keyboard.append([InlineKeyboardButton(f'🔎 Pesquisar por outro Usuário', switch_inline_query_current_chat='usuario ')])
            
                if tipo == 0:
                    update.message.reply_text(text=texto, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

                else:
                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
                
            else:
                update.message.reply_text(text='❌ | *Erro*\n\nEsse ID de usuário não foi encontrado no banco de dados!', parse_mode='Markdown')

        except Exception as e:
            print(e)
            update.message.reply_text(text='❌ | *Erro*\n\nOcorreu um erro na execução deste comando, contate o desenvolvedor do bot se esse problema percistir!', parse_mode='Markdown')



def pesquisarusuario(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message
    user_info = query.from_user
    user_id = str(user_info['id'])

    if user_id in donos:
        keyboard = [[InlineKeyboardButton(f'🔎 Pesquisar por usuários', switch_inline_query_current_chat='usuario ')]]
        
        texto = '🔎 *Grenciamento de usuários*\n\nPesquise por usuários, selecione o usuário em questão e defina uma ação para o mesmo, como: banir, baixar informações, excluir conta, etc...'
        update.message.reply_text(text=texto, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))




