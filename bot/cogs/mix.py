from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.modules.group_list import group_list
from bot.cogs.modules.database import *
from bot.cogs.modules.checker import *
import random, os, time
from time import sleep
import asyncio


def is_null(content):
    if content.strip() == '':
        return 'N/A'
    else:
        return content.strip()


def choose_ccs(quantidade, user_id):
    rows = asyncio.run(all_ccs())
    q = len(rows)
    ccs = []
    if q > int(quantidade):
        rows = random.sample(rows, int(quantidade))
        for row in rows:
            cc_id = row[0]
            numero = row[1]
            expiracao = row[2]
            cvv = row[3]
            bandeira = is_null(row[5])
            categoria = is_null(row[6])
            banco = is_null(row[7])
            hora = str(time.time())
            asyncio.run(update_cartao(cc_id, user_id, hora))
            credit_card = f"{numero}|{expiracao.replace('/', '|20')}|{cvv} - {categoria} | {banco} | {bandeira}"
            ccs.append(credit_card)
        
        return True, ccs

    else:
        return False, []


def choose_check_ccs(quantidade, user_id):
    repetidos = []
    ccs = []
    q = len(asyncio.run(all_ccs()))
    if q*2 > int(quantidade):
        while True:
            if not len(repetidos) == int(quantidade):
                rows = asyncio.run(all_ccs())
                q = len(rows)
                if not q < int(quantidade):
                    row = rows[random.randint(0, q-1)]
                    numero = row[1]
                    expiracao = row[2]
                    cvv = row[3]
                    bandeira = is_null(row[5])
                    categoria = is_null(row[6])
                    banco = is_null(row[7])
                    credit_card = f"{numero}|{expiracao.replace('/', '|20')}|{cvv} - {categoria} | {banco} | {bandeira}"
                    cc_checker = f"{numero}|{expiracao.replace('/', '|20')}|{cvv}"
                    if not credit_card in repetidos:
                        check = checker(cc_checker)
                        print(credit_card+str(check))
                        if check[0] == True:
                            ccs.append(row)
                            repetidos.append(credit_card)

                        else:
                            asyncio.run(remove_cc(numero, True))
                    
                        sleep(2)
                
                else:
                    break
            
            else:
                break
        
        if len(repetidos) == int(quantidade):
            for cc in ccs:
                cc_id = cc[0]
                hora = str(time.time())
                asyncio.run(update_cartao(cc_id, user_id, hora))
                
            return True, repetidos
        else:
            return False, []
    
    else:
        return False, []



def preco_mix(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message

    if query is None:
        query = update.callback_query
        user_info = query.from_user
        user_id = str(user_info['id'])

    else:
        user_info = query.from_user
        user_id = str(user_info['id'])

    if user_id in donos:
        rows = asyncio.run(all_mix())
        con = 0
        
        results1= []
        results2= []
        for row in rows:
            con += 1

            if (con%2) == 0:
                results2.append(row[0])
            
            else:
                results1.append(row[0])
                    

        buttons = []
        for var1, var2 in zip(results1, results2):
            buttons.append([InlineKeyboardButton(text=f'🔃 Mix {var1} CCs', callback_data='+'+var1), InlineKeyboardButton(text=f'🔃 Mix {var2} CCs', callback_data='+'+var2)])

        q1 = len(results1)+len(results2)
        if not (q1%2) == 0:
            var1 = results1[len(results1)-1]
            buttons.append([InlineKeyboardButton(text=f'🔃 Mix {var1} CCs', callback_data='+'+var1)])

        buttons.append([InlineKeyboardButton(text=f'◀︎ {button_back}', callback_data='editar_precos')])
        keyboard = InlineKeyboardMarkup(buttons)

        try:
            update.message.reply_text(text=price_mix_edit_text, parse_mode='Markdown', reply_markup=keyboard)

        except:
            query = update.callback_query
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_mix_edit_text, parse_mode='Markdown', reply_markup=keyboard)


def mix(update: Update, context: CallbackContext):
    mix_lista = asyncio.run(all_mix())
    lista = asyncio.run(all_ccs())
    
    q = len(lista)
    mixes = []
    buttons = []

    for item in sorted(mix_lista, key=lambda x: int(x[1])):
        quantidade = int(item[0])
        if q >= quantidade:
            mixes.append('💳 '+table_mix_text.format(quantidade, item[1]))
            buttons.append(quantidade)

    row1 = []
    row2 = []
    keyboard = []

    con = 0
    for c in buttons:
        con += 1
        level = c
        if (con%2) == 0:
            row2.append(level)
        
        else:
            row1.append(level)

    for var1, var2 in zip(row1, row2):
        var1 = str(var1)
        var2 = str(var2)
        keyboard.append([InlineKeyboardButton(text=f'💳 {var1} Mix', callback_data='>'+var1), InlineKeyboardButton(text=f'💳 {var2} Mix', callback_data='>'+var2)])

    q1 = len(row1)+len(row2)
    if not (q1%2) == 0:
        var1 = row1[len(row1)-1]
        var1 = str(var1)
        keyboard.append([InlineKeyboardButton(text=f'💳 {var1} Mix', callback_data='>'+var1)])

    keyboard.append([InlineKeyboardButton(f'◀︎ {button_back}', callback_data='m1')])

    qc = len(asyncio.run(all_ccs()))
    query = update.callback_query
    if not qc == 0:
        if not len(mixes) == 0:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=mix_text+str(mixes).replace("', ", "").replace("'", "").replace('[', '').replace(']', '').replace(r'\n', '\n'), parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=no_table, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=table_mix_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))



def criar_mix(update: Update, context: CallbackContext):
    query = update.message

    if query is None:
        query = update.callback_query
        user_info = query.from_user
        user_id = str(user_info['id'])

    else:
        user_info = query.from_user
        user_id = str(user_info['id'])

    try:
        table = update.message.text.split()[1]

        if not table.find('|') == -1:
            quantidade = table[:table.find('|')]
            preco = table[table.find('|')+1:]
            if quantidade.isnumeric() and preco.isnumeric():
                asyncio.run(registrar_mix(quantidade, preco))
                update.message.reply_text(text=table_created.format(quantidade, preco, button_edit_mix), parse_mode='Markdown')

            else:
                update.message.reply_text(text=table_create_error, parse_mode='Markdown')
        
        else:
            update.message.reply_text(text=table_create_error, parse_mode='Markdown')

    except:
        update.message.reply_text(text=table_create_error, parse_mode='Markdown')


def comprar_mix(update: Update, context: CallbackContext):
    query = update.callback_query

    user_info = query.from_user
    user_id = str(user_info['id'])
    
    quantidade = query.data.replace('>', '')

    keyboard = [[InlineKeyboardButton(text=f'✔️ Comprar', callback_data='comprarmix_'+str(quantidade))],
                [InlineKeyboardButton(text=f'❌ Cancelar', callback_data='mix')]]

    texto = f'🔃 | **Compra de MIX**\n\nVocê está prestes a comprar um lote com {quantidade} CCs, clique em "Comprar" para proceguir com a compra!\n\nMix acima de 10 CCs não são checadas por limitaçõe do checker, mas em breve vão ser! Mas damos a garantia de 70% na MIX!'
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


def confirmar_compra_mix(update: Update, context: CallbackContext):
    query = update.callback_query

    keyboard = [[InlineKeyboardButton(f'◀︎ {button_back}', callback_data='mix')]]

    user_info = query.from_user
    user_id = str(user_info['id'])
    saldo = asyncio.run(pesquisar_id(user_id))[1]
    grupos = group_list()
    
    quantidade = query.data.replace('comprarmix_', '')
    pesquisa = asyncio.run(pesquisar_mix(quantidade))
    if pesquisa is not None:
        if int(pesquisa[1]) <= int(saldo):
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='🔃 | **Criando Mix**\n\nEstamos criando sua MIX de CCs, aguarde!', parse_mode='Markdown')
    
            if int(quantidade) <= 11:
                asyncio.run(subtrair_saldo(user_id, pesquisa[1]))
                if asyncio.run(check_config('checker'))[1] == '1':
                    ccs = choose_check_ccs(quantidade, user_id)
                else:
                    ccs = choose_ccs(quantidade, user_id)
                filename = f'temp/mix{user_id}.txt'
                
                with open(filename, 'a', encoding='UTF-8') as file:
                    for cc in ccs[1]:
                        file.write(str(cc)+'\n')
                        
                if ccs[0]:
                    text = f'🔃 | *Mix pronta!*\n\nSua MIX de {quantidade} CCs está pronta e foi anexada a essa mensagem como um arquivo de texto, abra-o para mais informações!'
                    query.bot.send_document(chat_id=user_id, document=open(filename,'rb'), caption=text, parse_mode='Markdown')

                    nome = str(user_info['first_name'])
                    os.remove(filename)
                    for grupo in grupos:
                        try:
                            query.bot.send_message(chat_id=grupo, text=f'🔃 | *Mix comprada!*\n\nUma Mix de {quantidade} CCs foi comprada por: {nome}', parse_mode='Markdown')
                        except:
                            pass

                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='**🔃 | MIX criada!**\n\nEla vai ser enviada no chat!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

                else:
                    asyncio.run(add_saldo(user_id, pesquisa[1]))
                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='🔃 | **Ocorreu um Erro ao criar sua Mix**\n\nAs CCs podem estar em uma quantidade limitada no estoque!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

                
            else:
                ccs = choose_ccs(quantidade, user_id)
                if ccs[0]:
                    filename = f'temp/mix{user_id}.txt'
                    with open(filename, 'a', encoding='UTF-8') as file:
                        for cc in ccs[1]:
                            file.write(str(cc)+'\n')
                            
                    asyncio.run(subtrair_saldo(user_id, pesquisa[1]))
                    text = f'🔃 | *Mix pronta!*\n\nSua MIX de {quantidade} CCs está pronta e foi anexada a essa mensagem como um arquivo de texto, abra-o para mais informações!'
                    query.bot.send_document(chat_id=user_id, document=open(filename,'rb'), caption=text, parse_mode='Markdown')

                    os.remove(filename)

                    nome = str(user_info['first_name'])
                    for grupo in grupos:
                        try:
                            query.bot.send_message(chat_id=grupo, text=f'🔃 | *Mix comprada!*\n\nUma Mix de {quantidade} CCs foi comprada por: {nome}', parse_mode='Markdown')
                        except:
                            pass
                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='**🔃 | MIX criada!**\n\nEla vai ser enviada no chat!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

                else:
                    asyncio.run(add_saldo(user_id, pesquisa[1]))
                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='🔃 | **Ocorreu um Erro ao criar sua Mix**\n\nAs CCs podem estar em uma quantidade limitada no estoque!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            query.bot.answer_callback_query(update.callback_query.id,  text=f'❕ Saldo insuficiente para comprar essa MIX (R${pesquisa[1]},00). Você possui R${saldo},00', show_alert=True)

    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='🔃 | **Ocorreu um Erro ao criar sua Mix**\n\nEssa categoria de Mix foi deletada!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))





