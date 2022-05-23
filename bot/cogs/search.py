from telegram.ext import CallbackContext
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from bot.cogs.modules.prices import preco_img
from uuid import uuid4
from random import randint
import json
from bot.cogs.ban import *
import asyncio

def search(update: Update, context: CallbackContext):
    results = asyncio.run(all_ccs())

    q = len(results)
    query = update.callback_query
    user_info = query.from_user
    user_id = str(user_info['id'])
    if check_status(user_id):

        if not q == 0:
            if q > 2:
                r = randint(0, q-1)
            else:
                r = 0
                
            bandeira = results[r][5]
            bin_num = results[r][1][:6]
            banco = results[r][7]

            if bandeira.strip() == '':
                bandeira = scheme_search_default

            if bin_num.strip() == '':
                bin_num = bin_search_default

            if banco.strip() == '':
                banco = bank_search_default

        else:
            bandeira = scheme_search_default
            bin_num = bin_search_default
            banco = bank_search_default
            
        keyboard = []
        
        keyboard_search = []

        if asyncio.run(check_config('pesquisar_banco'))[1] == '1':
            keyboard_search.append('item 1')

        if asyncio.run(check_config('pesquisar_bandeira'))[1] == '1':
            keyboard_search.append('item 2')

        if asyncio.run(check_config('pesquisar_bin'))[1] == '1':
            keyboard_search.append('item 3')

        if len(keyboard_search) == 1:
            keyboard.append([InlineKeyboardButton(f'🏦 {button_search_bank}', switch_inline_query_current_chat='banco '+banco)])
            
        elif len(keyboard_search) == 2:
            keyboard.append([InlineKeyboardButton(f'🏦 {button_search_bank}', switch_inline_query_current_chat='banco '+banco), InlineKeyboardButton(f'💳 {button_search_scheme}', switch_inline_query_current_chat='bandeira '+bandeira)])

        elif len(keyboard_search) == 3:
            keyboard.append([InlineKeyboardButton(f'🏦 {button_search_bank}', switch_inline_query_current_chat='banco '+banco), InlineKeyboardButton(f'💳 {button_search_scheme}', switch_inline_query_current_chat='bandeira '+bandeira)])
            keyboard.append([InlineKeyboardButton(f'🔍 {button_search_bin}', switch_inline_query_current_chat='bin '+bin_num)])

        keyboard.append([InlineKeyboardButton(f'◀︎ {button_back}', callback_data='m1')])
    
    query = update.callback_query
    if check_status(user_id):
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='🔎 | *Filtros de Pesquisa*\n\nEscolha um tipo de pesquisa para começar a pesquisar pelos cartões que você deseja!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=denied_text(user_id), parse_mode='Markdown')



def buscar(item, pesquisa):
    l = []
    for c in pesquisa.replace(' ', ''):
        if c in item:
            item2 = item.index(c)
            item = item[:item2] + item[item2+1:]
            l.append(item)

        else:
            l.append(False)
            break

    q = len(l) - 1
    u = l[q]
    if u == False:
        return False
    
    else:
        return True


def query_result(frase):
    q = frase.upper().strip().split()
    quantidade = len(q)
    t1 = []

    for c in range(1, quantidade):
        palavra = str(q[c])
        t1.append(palavra)

    retorno = str(t1).replace("'", '').replace(",", '').replace("[", '').replace("]", '')
    
    return retorno


def buscar_preco(categoria, lista):
    def corte_preco(c):
        contador = -1
        n = 0
        for l in c:
            contador += 1
            if l.isnumeric():
                n = contador
                break
            
        return n

    for c in lista:
        if not c.find(categoria.upper().strip()) == -1:
            corte = corte_preco(c)
            return c[corte:]


def inlinequery(update: Update, context: CallbackContext):
    query = update.inline_query.query
    lista = list(asyncio.run(precos_inline()))
    user_id = update.inline_query.from_user.id

    donos = adm_list()

    if check_status(user_id):
        try:
            results= []
            if query.lower().split()[0] == 'bin':
                if asyncio.run(check_config('pesquisar_bin'))[1] == '1':
                    query = query_result(query)
                    results2= []
                    rows = asyncio.run(all_ccs())

                    for row in rows:
                        id_cc = row[0]
                        numero = row[1][:6]
                        expiracao = row[2].replace('/', '|20')
                        bandeira = row[5]
                        categoria = row[6]
                        banco = row[7]
                        p = buscar_preco(categoria, lista)
                        if not p == None:
                            pi = preco_img(p)
                            
                            if buscar(numero, query):
                                if len(results2) < 49:
                                    results2.append(InlineQueryResultArticle(type='article', thumb_url=pi, id=str(uuid4()),title=f'{numero}xxxxxxxxxx|{expiracao}|xxx',description=inline_cc_info.format(categoria, bandeira, banco, p),input_message_content=InputTextMessageContent(f"/cartao {id_cc}|bin"),))

                                else:
                                    break

                    if len(results2) >= 1:
                        q = len(results2)
                        results.append(InlineQueryResultArticle(type='article', thumb_url='https://creazilla-store.fra1.digitaloceanspaces.com/emojis/42989/magnifying-glass-tilted-right-emoji-clipart-md.png', id=str(uuid4()),title=cards_found.format(q),description=see_cards,input_message_content=InputTextMessageContent(f"{q} {found_for_bin}: {query}"),))
                        for r in results2:
                            results.append(r)
                            
                        update.inline_query.answer(results)

                    elif len(results2) == 0:
                        results.append(InlineQueryResultArticle(type='article', thumb_url='https://i.imgur.com/BBnidae.png', id=str(uuid4()),title=bin_not_found,description=try_search_other_bin,input_message_content=InputTextMessageContent(bin_not_found),))

                else:
                    results.append(InlineQueryResultArticle(thumb_url='https://i.imgur.com/BBnidae.png', id=str(uuid4()),title='Metodo de busca desativado',description='A o método de busca selcionado foi desativado!',input_message_content=InputTextMessageContent(scheme_not_found)))
                    update.inline_query.answer(results)

            elif query.lower().split()[0] == 'banco':
                if asyncio.run(check_config('pesquisar_banco'))[1] == '1':
                    query = query_result(query)
                    
                    results2= []
                    rows = asyncio.run(all_ccs())

                    for row in rows:
                        id_cc = row[0]
                        numero = row[1][:6]
                        expiracao = row[2].replace('/', '|20')
                        bandeira = row[5]
                        categoria = row[6]
                        banco = row[7]
                        p = buscar_preco(categoria, lista)
                        if not p == None:
                            pi = preco_img(p)
                            
                            if buscar(banco, query):
                                if len(results2) < 49:
                                    results2.append(InlineQueryResultArticle(type='article', thumb_url=pi, id=str(uuid4()),title=f'{numero}xxxxxxxxxx|{expiracao}|xxx',description=inline_cc_info.format(categoria, bandeira, banco, p),input_message_content=InputTextMessageContent(f"/cartao {id_cc}|banco"),))

                                else:
                                    break

                    if len(results2) >= 1:
                        q = len(results2)
                        results.append(InlineQueryResultArticle(type='article', thumb_url='https://creazilla-store.fra1.digitaloceanspaces.com/emojis/42989/magnifying-glass-tilted-right-emoji-clipart-md.png', id=str(uuid4()),title=cards_found.format(q),description=see_cards,input_message_content=InputTextMessageContent(f"{q} {found_for_bank}: {query}"),))
                        for r in results2:
                            results.append(r)
                            
                        update.inline_query.answer(results)

                    elif len(results2) == 0:
                        results.append(InlineQueryResultArticle(type='article', thumb_url='https://i.imgur.com/BBnidae.png', id=str(uuid4()),title=bank_not_found,description=try_search_other_bank,input_message_content=InputTextMessageContent(bank_not_found),))

                        update.inline_query.answer(results)

                else:
                    results.append(InlineQueryResultArticle(thumb_url='https://i.imgur.com/BBnidae.png', id=str(uuid4()),title='Metodo de busca desativado',description='A o método de busca selcionado foi desativado!',input_message_content=InputTextMessageContent(scheme_not_found)))
                    update.inline_query.answer(results)


            elif query.lower().split()[0] == 'bandeira':
                if asyncio.run(check_config('pesquisar_bandeira'))[1] == '1':
                    query = query_result(query)
                    
                    results2= []
                    rows = asyncio.run(all_ccs())

                    for row in rows:
                        id_cc = row[0]
                        numero = row[1][:6]
                        expiracao = row[2].replace('/', '|20')
                        bandeira = row[5]
                        categoria = row[6]
                        banco = row[7]
                        p = buscar_preco(categoria, lista)
                        if not p == None:
                            pi = preco_img(p)
                            
                            if buscar(bandeira, query):
                                if len(results2) < 49:
                                    results2.append(InlineQueryResultArticle(type='article', thumb_url=pi, id=str(uuid4()),title=f'{numero}xxxxxxxxxx|{expiracao}|xxx',description=inline_cc_info.format(categoria, bandeira, banco, p),input_message_content=InputTextMessageContent(f"/cartao {id_cc}|bandeira"),))

                                else:
                                    break

                    if len(results2) >= 1:
                        q = len(results2)
                        results.append(InlineQueryResultArticle(type='article', thumb_url='https://creazilla-store.fra1.digitaloceanspaces.com/emojis/42989/magnifying-glass-tilted-right-emoji-clipart-md.png', id=str(uuid4()),title=cards_found.format(q),description=see_cards,input_message_content=InputTextMessageContent(f"{q} {found_for_scheme}: {query}"),))
                        for r in results2:
                            results.append(r)
                            
                        update.inline_query.answer(results)

                    elif len(results2) == 0:
                        results.append(InlineQueryResultArticle(type='article', thumb_url='https://i.imgur.com/BBnidae.png', id=str(uuid4()),title=scheme_not_found,description=try_search_other_scheme,input_message_content=InputTextMessageContent(scheme_not_found),))

                        update.inline_query.answer(results)

                else:
                    results.append(InlineQueryResultArticle(thumb_url='https://i.imgur.com/BBnidae.png', id=str(uuid4()),title='Metodo de busca desativado',description='A o método de busca selcionado foi desativado!',input_message_content=InputTextMessageContent(scheme_not_found)))
                    update.inline_query.answer(results)


            elif query.lower().split()[0] == 'usuario' or query.lower().split()[0] == 'user':
                if str(user_id) in donos:
                    query = query.lower().replace('usuario', '').replace('user', '').strip()
                    if query == '':
                        query = 'a'
                        
                    rows = asyncio.run(all_users())
                    repetidos = []
                    for row in rows:
                        uid = row[0]
                        saldo = row[1]
                        nome = row[2].lower()
                        if buscar(nome, query) or buscar(uid, query):
                            if not uid in repetidos:
                                repetidos.append(uid)

                                if len(results) < 49:
                                    results.append(InlineQueryResultArticle(type='article', id=str(uuid4()),title=nome, description=f'ID: {uid} - Saldo: R${saldo},00',input_message_content=InputTextMessageContent(f"/usuario {uid}"),))

                                else:
                                    break
                    
                    r2 = []
                    if len(results) >= 1:
                        q = len(results)
                        r2.append(InlineQueryResultArticle(type='article', thumb_url='https://creazilla-store.fra1.digitaloceanspaces.com/emojis/42989/magnifying-glass-tilted-right-emoji-clipart-md.png', id=str(uuid4()),title=f'{len(results)} usuários encontrados',description='Veja-os abaixo!',input_message_content=InputTextMessageContent(f"{len(results)} usuários encontrados para: {query}"),))
                        for r in results:
                            r2.append(r)
                            
                        update.inline_query.answer(r2)

                    elif len(results) == 0:
                        r2.append(InlineQueryResultArticle(type='article', thumb_url='https://i.imgur.com/BBnidae.png', id=str(uuid4()),title='Usuário não encontrado!',description=f'Nada encontrado para: {query}',input_message_content=InputTextMessageContent(f'Nenhum usuário encontrado para: {query}'),))

                        update.inline_query.answer(r2)


            elif query.lower().split()[0] == 'gift':
                query = query.replace('gift', '').strip()
                if str(user_id) in donos:
                    if not query == '' and query.isnumeric():
                        gift = asyncio.run(gen_gift(query))
            
                        result = [InlineQueryResultArticle(type='article', id=str(uuid4()),title=f'Gift de {query} gerado!',description=f'Clique para enviar no chat!',input_message_content=InputTextMessageContent(gift_gen.format(query, gift, gift), parse_mode='Markdown'))]

                    else:
                        result = [InlineQueryResultArticle(type='article', id=str(uuid4()),title=f'Digite um valor para gerar um gift!',description=f'Ex: gift 10',input_message_content=InputTextMessageContent('Use: @arroobadobot gift <valor>, para gerar um gift, e clique para enviar no chat', parse_mode='Markdown'))]

                    update.inline_query.answer(result)


        except Exception as e:
            print(e)
            results = []
            results2= []
            rows = asyncio.run(all_ccs())

            for row in rows:
                id_cc = row[0]
                numero = row[1][:6]
                expiracao = row[2]
                bandeira = row[5]
                categoria = row[6]
                banco = row[7]
                p = buscar_preco(categoria, lista)
                if not p == None:
                    pi = preco_img(p)
                    
                    if len(results2) < 49:
                        results2.append(InlineQueryResultArticle(type='article', thumb_url=pi, id=str(uuid4()),title=f'{numero}xxxxxxxxxx|{expiracao}|xxx',description=inline_cc_info.format(categoria, bandeira, banco, p),input_message_content=InputTextMessageContent(f"/cartao {id_cc}"),))

                    else:
                        break

            if len(results2) >= 1:
                q = len(results2)
                results.append(InlineQueryResultArticle(type='article', thumb_url='https://creazilla-store.fra1.digitaloceanspaces.com/emojis/42989/magnifying-glass-tilted-right-emoji-clipart-md.png', id=str(uuid4()),title=cards_found.format(q),description=see_cards,input_message_content=InputTextMessageContent(cards_found.format('0')),))
                for r in results2:
                    results.append(r)
                    
                update.inline_query.answer(results)

            elif len(results2) == 0:
                results.append(InlineQueryResultArticle(type='article', thumb_url='https://i.imgur.com/BBnidae.png', id=str(uuid4()),title=inline_stock_null_title,description=inline_stock_null,input_message_content=InputTextMessageContent(inline_stock_null),))

                update.inline_query.answer(results)



