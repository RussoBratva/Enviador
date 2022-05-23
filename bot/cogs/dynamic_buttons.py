from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.modules.group_list import group_list
from bot.cogs.modules.database import *
from bot.cogs.modules.checker import *
import random, os
from bot.cogs.ban import *
import asyncio, time



def cc_usada(cc):
    if not os.path.isfile('temp/compradas'):
        with open('temp/compradas', 'w', encoding='UTF-8') as file:
            file.write('')
            
    with open('temp/compradas', 'a', encoding='UTF-8') as file:
        file.write(str(cc)+'\n')


def a_cc_foi_usada(cc):
    if not os.path.isfile('temp/compradas'):
        with open('temp/compradas', 'w', encoding='UTF-8') as file:
            file.write('')

    with open('temp/compradas', 'r', encoding='UTF-8') as file:
        data = file.read()
        if cc in data:
            return True
        else:
            return False

with open('config/config.json', 'r', encoding='UTF-8') as file:
    try:
        tempo_de_troca = int(json.loads(file.read())['exchange_time_in_minutes'])
    except:
        tempo_de_troca = 7
    segundos = tempo_de_troca*60


def choose_cc(level):
    while True:
        rows = asyncio.run(pesquisar_categoria(level))
        q = len(rows)
        if not q == 0:
            if q > 0:
                row = list(rows[random.randint(0, len(rows)-1)])
                numero = row[1]
                expiracao = is_null(row[2])
                cvv = is_null(row[3])
                credit_card = f"{numero}|{expiracao.replace('/', '|')}|{cvv}"

                if a_cc_foi_usada(credit_card) ==  False:
                    if asyncio.run(check_comprada(row[1])):
                        return True, row
                    else:
                        row = []
                    
                    if rows == []:
                        print(rows)
                        return False, []
                    
                else:
                    pass

            else:
                return False, []

        else:
            return False, []


def choose_cc_especific(conteudo, tipo):
    rows = asyncio.run(all_ccs())
    rows2 = []
    q = len(rows)
    
    if tipo == 'banco':
        for row in rows:
            if row[7] == conteudo:
                rows2.append(row)
    
    elif tipo == 'bin':
        for row in rows:
            if row[1][:6] == conteudo:
                rows2.append(row)
    
    elif tipo == 'bandeira':
        for row in rows:
            if row[5] == conteudo:
                rows2.append(row)
    
    if not len(rows2) == 0:
        if len(rows2) >= 1:
            row = []
            row = list(rows2[0])

            if asyncio.run(check_comprada(row[1])):
                print(row)
                return True, row

            if row == []:
                return False, []

        else:
            return False, []

    else:
        return False, []


def is_null(content):
    if content.strip() == '' or content.strip() == 'None':
        return 'N/A'
    else:
        return content



def editar_precos(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message

    if query is None:
        query = update.callback_query
        user_info = query.from_user
        user_id = str(user_info['id'])

    else:
        user_info = query.from_user
        user_id = str(user_info['id'])

    keyboard = [[InlineKeyboardButton(f'🔃 {button_edit_mix}', callback_data='editar_mix')],
            [InlineKeyboardButton(f'💳 {button_edit_unitary}', callback_data='editar_unitaria')],]

    if user_id in donos:
        try:
            update.message.reply_text(text=price_edit, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        except:
            query = update.callback_query
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


def dynamic_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    donos = adm_list()
    user_info = query.from_user
    user_id = str(user_info['id'])
    retorno = str(query.data)
    query_data_clear = retorno.replace('^', '')
    

    lista = ['aplicar', 'zerar', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o0']
    lista2 = ['aplicar2', 'zerar2', 'deletar2', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a0']

    if retorno[0] == '^' or retorno in lista:
        query_data = retorno.replace('^', '').replace('o', '')

        numpad = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='1', callback_data= 'o1'),
            InlineKeyboardButton(text='2', callback_data= 'o2'),
            InlineKeyboardButton(text='3', callback_data= 'o3')],
            [InlineKeyboardButton(text='4', callback_data= 'o4'),
            InlineKeyboardButton(text='5', callback_data= 'o5'),
            InlineKeyboardButton(text='6', callback_data= 'o6')],
            [InlineKeyboardButton(text='7', callback_data= 'o7'),
            InlineKeyboardButton(text='8', callback_data= 'o8'),
            InlineKeyboardButton(text='9', callback_data='o9')],
            [InlineKeyboardButton(text='0', callback_data='o0'),
            InlineKeyboardButton(text=button_reset, callback_data='zerar')],
            [InlineKeyboardButton(text=f'✔️ {button_done}', callback_data='aplicar'),
            InlineKeyboardButton(text=f'❌ {button_cancel}', callback_data='cancelar_edicao1')],])

        numpad2 = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=button_reset, callback_data='zerar')],
            [InlineKeyboardButton(text=f'✔️ {button_done}', callback_data='aplicar'),
            InlineKeyboardButton(text=f'❌ {button_cancel}', callback_data='cancelar_edicao1')]])

        numpad3 = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='1', callback_data= 'o1'),
            InlineKeyboardButton(text='2', callback_data= 'o2'),
            InlineKeyboardButton(text='3', callback_data= 'o3')],
            [InlineKeyboardButton(text='4', callback_data= 'o4'),
            InlineKeyboardButton(text='5', callback_data= 'o5'),
            InlineKeyboardButton(text='6', callback_data= 'o6')],
            [InlineKeyboardButton(text='7', callback_data= 'o7'),
            InlineKeyboardButton(text='8', callback_data= 'o8'),
            InlineKeyboardButton(text='9', callback_data='o9')],
            [InlineKeyboardButton(text='0', callback_data='o0')],
            [InlineKeyboardButton(text=f'❌ {button_cancel}', callback_data='cancelar_edicao1')],])

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f'◀︎ {button_back_edit_menu}', callback_data='cancelar_edicao1')],])

        categoria = query_data_clear.replace('({new})', '').strip()

        if retorno[0] == '^':
            if retorno[0] == '^':
                price = asyncio.run(level_price(categoria))
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_1.format(category, categoria, new_price, price)+'\n\n'+'-='*20+f'\n\n{price_edit_info_2}: {price_edit_info_null}', parse_mode='Markdown', reply_markup=numpad3)

            else:
                text = query.message.text
                categoria1 = text.strip().replace('`', '')[text.find(category)+len(category)+2:].strip()
                categoria2 = categoria1[:categoria1.find('\n')]
                price = asyncio.run(level_price(categoria2))
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_1.format(category, categoria, new_price, price)+'\n\n'+'-='*20+f'\n\n{price_edit_info_2}: {price_edit_info_null}', parse_mode='Markdown', reply_markup=numpad3)

        elif query.data == 'aplicar':
            text = query.message.text
            categoria1 = text.strip().replace('`', '')[text.find(category)+len(category)+2:].strip()
            categoria2 = categoria1[:categoria1.find('\n')].replace(f'({new})', '').strip()
            q = text.replace(price_edit_info_null, '').strip().replace('`', '')[text.find(price_edit_info_2.replace('*', ''))+len(price_edit_info_2):]
            preco_antigo = price = asyncio.run(level_price(categoria2))
            asyncio.run(price_change(categoria2, q))
            preco_novo = asyncio.run(level_price(categoria2))
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_changed.format(category, categoria2, preco_antigo, preco_novo), parse_mode='Markdown', reply_markup=keyboard)

        elif query_data == 'zerar':
            text = query.message.text
            categoria1 = text.strip().replace('`', '')[text.find(category)+len(category)+2:].strip()
            categoria2 = categoria1[:categoria1.find('\n')].replace(f'({new})', '').strip()
            price = asyncio.run(level_price(categoria2))
            q = text.replace(price_edit_info_null, '').strip().replace('`', '')[text.find(price_edit_info_2.replace('*', ''))+len(price_edit_info_2):]
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_1.format(category, categoria2, new_price, price)+'\n\n'+'-='*20+f'\n\n{price_edit_info_2}: {price_edit_info_null}', parse_mode='Markdown', reply_markup=numpad3)

        else:
            try:
                query_data = query_data_clear.replace(price_edit_info_null, '').replace('o', '')
                text = query.message.text
                q = text.replace(price_edit_info_null, '').strip().replace('`', '')[text.find(price_edit_info_2.replace('*', ''))+len(price_edit_info_2):]
                categoria1 = text.strip().replace('`', '')[text.find(category)+len(category)+2:].strip()
                categoria2 = categoria1[:categoria1.find('\n')].replace(f'({new})', '').strip()
                price = asyncio.run(level_price(categoria2))
                q_add = q.replace(price_edit_info_null, '') + query_data.replace(price_edit_info_null, '')

                if int(q_add) < 201:
                    if int(q_add) < 21:
                        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_1.format(category, categoria2, new_price, price)+f'\n\n{price_edit_info_2}: {q_add}', parse_mode='Markdown', reply_markup=numpad)

                    else:
                        q_add = q_add.lstrip('0')
                        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_1.format(category, categoria2, new_price, price)+f'\n\n{price_edit_info_2}: {q_add}', parse_mode='Markdown', reply_markup=numpad2)

                else:
                    q_add = q_add.lstrip('0')
                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_1.format(category, categoria2, new_price, price)+f'\n\n{price_edit_info_2}: {q_add}', parse_mode='Markdown', reply_markup=numpad2)

            except Exception as e:
                print('Erro interno:', str(e))
                pass

    elif retorno[0] == '+' or retorno in lista2:
        query_data = retorno.replace('^', '').replace('a', '')

        numpad = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='1', callback_data= 'a1'),
            InlineKeyboardButton(text='2', callback_data= 'a2'),
            InlineKeyboardButton(text='3', callback_data= 'a3')],
            [InlineKeyboardButton(text='4', callback_data= 'a4'),
            InlineKeyboardButton(text='5', callback_data= 'a5'),
            InlineKeyboardButton(text='6', callback_data= 'a6')],
            [InlineKeyboardButton(text='7', callback_data= 'a7'),
            InlineKeyboardButton(text='8', callback_data= 'a8'),
            InlineKeyboardButton(text='9', callback_data='a9')],
            [InlineKeyboardButton(text='0', callback_data='a0'),
            InlineKeyboardButton(text=button_reset, callback_data='zerar2')],
            [InlineKeyboardButton(text=f'✔️ {button_done}', callback_data='aplicar2')],
            [InlineKeyboardButton(text=f'🗑️ {button_delete_mix_table}', callback_data='deletar2')],
            [InlineKeyboardButton(text=f'❌ {button_cancel}', callback_data='cancelar_edicao2')],])

        numpad2 = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'✔️ {button_done}', callback_data='aplicar2')],
            [InlineKeyboardButton(text=f'🗑️ {button_delete_mix_table}', callback_data='deletar2')],
            [InlineKeyboardButton(text=f'❌ {button_cancel}', callback_data='cancelar_edicao2')],])

        numpad3 = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='1', callback_data= 'a1'),
            InlineKeyboardButton(text='2', callback_data= 'a2'),
            InlineKeyboardButton(text='3', callback_data= 'a3')],
            [InlineKeyboardButton(text='4', callback_data= 'a4'),
            InlineKeyboardButton(text='5', callback_data= 'a5'),
            InlineKeyboardButton(text='6', callback_data= 'a6')],
            [InlineKeyboardButton(text='7', callback_data= 'a7'),
            InlineKeyboardButton(text='8', callback_data= 'a8'),
            InlineKeyboardButton(text='9', callback_data='a9')],
            [InlineKeyboardButton(text='0', callback_data='a0')],
            [InlineKeyboardButton(text=f'🗑️ {button_delete_mix_table}', callback_data='deletar2')],
            [InlineKeyboardButton(text=f'❌ {button_cancel}', callback_data='cancelar_edicao2')]])

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f'◀︎ {button_back_edit_menu}', callback_data='cancelar_edicao1')],])
        keyboard2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f'◀︎ {button_back_edit_menu}', callback_data='cancelar_edicao2')],])

        quantidade = query_data.replace('+', '')

        if retorno[0] == '+':
            if retorno[0] == '+':
                price = asyncio.run(pesquisar_mix(quantidade.replace('+', '')))[1]
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_1.format(amount, quantidade, new_price, price)+'\n\n'+'-='*20+f'\n\n{price_edit_info_2}: {price_edit_info_null}', parse_mode='Markdown', reply_markup=numpad3)

            else:
                text = query.message.text
                quantidade1 = text.strip().replace('`', '')[text.find(amount)+len(amount)+2:].strip()
                quantidade2 = quantidade1[:quantidade1.find('\n')]
                price = asyncio.run(pesquisar_mix(quantidade.replace('+', '')))[1]
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_1.format(amount, quantidade2, new_price, price)+'\n\n'+'-='*20+f'\n\n{price_edit_info_2}: {price_edit_info_null}', parse_mode='Markdown', reply_markup=numpad3)

        elif query_data == 'zerar2':
            text = query.message.text
            quantidade1 = text.strip().replace('`', '')[text.find(amount)+len(amount)+2:].strip()
            quantidade2 = quantidade1[:quantidade1.find('\n')].strip()
            q = text.replace(price_edit_info_null, '').strip().replace('`', '')[text.find(price_edit_info_2.replace('*', ''))+len(price_edit_info_2):]
            price = asyncio.run(pesquisar_mix(quantidade2.replace('+', '')))[1]
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_1.format(amount, quantidade, new_price, price)+'\n\n'+'-='*20+f'\n\n{price_edit_info_2}: {price_edit_info_null}', parse_mode='Markdown', reply_markup=numpad3)

        elif query.data == 'aplicar2':
            text = query.message.text
            quantidade1 = text.strip().replace('`', '')[text.find(amount)+len(amount)+2:].strip()
            quantidade2 = quantidade1[:quantidade1.find('\n')].strip()
            q = text.replace(price_edit_info_null, '').strip().replace('`', '')[text.find(price_edit_info_2.replace('*', ''))+len(price_edit_info_2):]
            preco_antigo = asyncio.run(pesquisar_mix(quantidade2.replace('+', '')))[1]
            asyncio.run(editar_valor_mix(quantidade2, q))
            preco_novo = asyncio.run(pesquisar_mix(quantidade2.replace('+', '')))[1]
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_changed.format(amount, quantidade2, preco_antigo, preco_novo), parse_mode='Markdown', reply_markup=keyboard2)

        elif query.data == 'deletar2':
            text = query.message.text
            quantidade1 = text.strip().replace('`', '')[text.find(amount)+len(amount)+2:].strip()
            quantidade2 = quantidade1[:quantidade1.find('\n')].strip()
            asyncio.run(deletar_mix(quantidade2))
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_mix_deleted.format(amount, quantidade2), parse_mode='Markdown', reply_markup=keyboard2)

        else:
            try:
                query_data = query_data.replace(price_edit_info_null, '').replace('a', '')
                text = query.message.text
                q = text.replace(price_edit_info_null, '').strip().replace('`', '')[text.find(price_edit_info_2.replace('*', ''))+len(price_edit_info_2):]
                quantidade1 = text.strip().replace('`', '')[text.find(amount)+len(amount)+2:].strip()
                quantidade2 = quantidade1[:quantidade1.find('\n')].strip()
                price = asyncio.run(pesquisar_mix(quantidade2))[1]
                q_add = q.replace(price_edit_info_null, '') + query_data.replace(price_edit_info_null, '')

                if int(q_add) < 2001:
                    if int(q_add) < 201:
                        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_1.format(amount, quantidade2, new_price, price)+f'\n\n{price_edit_info_2}: {q_add}', parse_mode='Markdown', reply_markup=numpad)

                    else:
                        q_add = q_add.lstrip('0')
                        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_1.format(amount, quantidade2, new_price, price)+f'\n\n{price_edit_info_2}: {q_add}', parse_mode='Markdown', reply_markup=numpad2)

                else:
                    q_add = q_add.lstrip('0')
                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_info_1.format(amount, quantidade2, new_price, price)+f'\n\n{price_edit_info_2}: {q_add}', parse_mode='Markdown', reply_markup=numpad2)

            except Exception as e:
                print('Erro interno:', str(e))
                pass

    if check_status(user_id):
        if retorno[0] == '~':
            query_data = query.data.replace('~', '')[:query.data.find('(')-1].strip()

            rows = asyncio.run(pesquisar_categoria(query_data))
            contador = 0
            q = len(rows)
            if q > 2:
                rows = rows[random.randint(0, q-1)]
            
            else:
                rows = rows[0]

            row = tuple(rows)
            contador += 1
            if contador == 1:
                cc_id = row[0]
                numero = row[1][:6]
                expiracao = is_null(row[2])
                cvv = is_null(row[3])
                tipo = is_null(row[4])
                bandeira = is_null(row[5])
                categoria = is_null(row[6])
                banco = is_null(row[7])
                preco_cc = is_null(asyncio.run(level_price(categoria)))

                keyboard = [
                    [InlineKeyboardButton(f'✅ {button_buy}', callback_data='`'+str(cc_id))],]
                
                if user_id in donos:
                    keyboard.append([InlineKeyboardButton(f'🗑️ Deletar CC', callback_data=f'remove_{cc_id}')])
                
                keyboard.append([InlineKeyboardButton(f'◀︎ {button_back}', callback_data='unitaria')])
                
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=cc_info_buy.format(numero, expiracao, bandeira, tipo, categoria, banco, preco_cc), parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        elif retorno[0] == '`':
            user_info = query.from_user
            user_id = str(user_info['id'])
            usernome = str(user_info['first_name'])

    
            if 'bin' in retorno:
                tipo_p = 'bin'
                retorno = retorno.replace('bin', '')
            
            elif 'banco' in retorno:
                tipo_p = 'banco'
                retorno = retorno.replace('banco', '')
            
            elif 'bandeira' in retorno:
                tipo_p = 'bandeira'
                retorno = retorno.replace('bandeira', '')
            
            else:
                tipo_p = ''

            asyncio.run(registrar_usuario(user_id, usernome))
            asyncio.run(name_update(user_id, usernome))
            saldo = asyncio.run(pesquisar_id(user_id))[1]
            cc_id = retorno.replace('`', '')
            
            row = asyncio.run(pesquisar_cc_id(cc_id))
            
            if row is not None:
                numero = row[1]
                bin_cc = row[1][:6]
                expiracao = is_null(row[2])
                cvv = is_null(row[3])
                tipo = is_null(row[4])
                bandeira = is_null(row[5])
                categoria = is_null(row[6])
                banco = is_null(row[7])
                cpf = is_null(row[9])
                nome = is_null(row[10])
                comprador = row[11]
                hora = row[12]
                preco_cc = is_null(asyncio.run(precos(categoria)))

                if not int(preco_cc) <= int(saldo):
                    query.bot.answer_callback_query(update.callback_query.id, text=no_credits_alert.format(preco_cc, saldo), show_alert=True)
                
                else:
                    keyboard = [[InlineKeyboardButton(f'💳 {button_cc_main}', callback_data='unitaria')],]

                    expiracao = expiracao.replace('/', '|')
                    credit_card = f'{numero}|{expiracao}|{cvv}'

                    if asyncio.run(check_comprada(numero)):
                        
                        hora = str(time.time())
                        
                        if asyncio.run(check_config('checker'))[1] == '1' and asyncio.run(check_config('auto_live'))[1] == '0':
                            check = checker(credit_card)
                            if check[0]:
                                cc_usada(credit_card)

                                keyboard2 = [[InlineKeyboardButton(f'🔄 Não Upou? Tente trocar aqui!', callback_data=f'troca|{t}|{categoria}|{cc_id}'),]]

                                status = f'\n\n✅ *Status*: `#Aprovado - Retorno: {check[1]}`'

                                update_cc = asyncio.run(update_cartao(cc_id, user_id, hora))
                                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=cc_buy_warning, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
                                if asyncio.run(check_config('troca'))[1] == '1':
                                    a = query.bot.send_message(chat_id=query.message.chat.id, text=f"💳 | *Produto*:\n\nGARANTIMOS SOMENTE LIVE!\nNÃO GARANTIMOS A APROVAÇÃO\nNÃO GARANTIMOS SALDO\n\n*Card*: `{numero}|{expiracao.replace('/', '|')}|{cvv}`\n*Bandeira*: `{bandeira}`\n*Categoria*: `{categoria}`\n*Banco*:  `{banco}`\n\n*Nome*: `{nome}`\n*CPF*: `{cpf}`"+status, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard2))
                                else:
                                    a = query.bot.send_message(chat_id=query.message.chat.id, text=f"💳 | *Produto*:\n\nGARANTIMOS SOMENTE LIVE!\nNÃO GARANTIMOS A APROVAÇÃO\nNÃO GARANTIMOS SALDO\n\n*Card*: `{numero}|{expiracao.replace('/', '|')}|{cvv}`\n*Bandeira*: `{bandeira}`\n*Categoria*: `{categoria}`\n*Banco*:  `{banco}`\n\n*Nome*: `{nome}`\n*CPF*: `{cpf}`"+status, parse_mode='Markdown')

                                asyncio.run(subtrair_saldo(user_id, preco_cc))
                                asyncio.run(remove_cc(numero, False))
                                grupos = group_list()
                                for grupo in grupos:
                                    try:
                                        query.bot.send_message(chat_id=grupo, text=f'💳 | *Cartão comprado!*\n\n*Level*: `{categoria}`\n*Comprador*: `{usernome}`', parse_mode='Markdown')
                                    except:
                                        pass

                            else:
                                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="💳 | *Cartão recusado!*\n\nCartão recusado! Escolha um outro cartão para comprar!", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

                        
                        if asyncio.run(check_config('checker'))[1] == '1' and asyncio.run(check_config('auto_live'))[1] == '1':
                            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='Estamos efetuando a verificação desse cartão, por favor aguarde!',parse_mode='Markdown')
                            check = checker(credit_card)
                            if check[0]:
                                cc_usada(credit_card)
                                saldo = asyncio.run(pesquisar_id(user_id))[1]
                                if int(preco_cc) <= int(saldo):
                                    update_cc = asyncio.run(update_cartao(cc_id, user_id, hora))
                                    t = str(time.time())
                                    keyboard2 = [[InlineKeyboardButton(f'🔄 Não Upou? Tente trocar aqui!', callback_data=f'troca|{t}|{categoria}|{cc_id}'),]]
                                    
                                    status = f'\n\n✅ *Status*: `#Aprovado - Retorno: {check[1]}`'
                                    
                                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=cc_buy_warning, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
                                    if asyncio.run(check_config('troca'))[1] == '1':
                                        a = query.bot.send_message(chat_id=query.message.chat.id, text=f"💳 | *Produto*:\n\nGARANTIMOS SOMENTE LIVE!\nNÃO GARANTIMOS A APROVAÇÃO\nNÃO GARANTIMOS SALDO\n\n*Card*: `{numero}|{expiracao.replace('/', '|')}|{cvv}`\n*Bandeira*: `{bandeira}`\n*Categoria*: `{categoria}`\n*Banco*:  `{banco}`\n\n*Nome*: `{nome}`\n*CPF*: `{cpf}`"+status, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard2))
                                    else:
                                        a = query.bot.send_message(chat_id=query.message.chat.id, text=f"💳 | *Produto*:\n\nGARANTIMOS SOMENTE LIVE!\nNÃO GARANTIMOS A APROVAÇÃO\nNÃO GARANTIMOS SALDO\n\n*Card*: `{numero}|{expiracao.replace('/', '|')}|{cvv}`\n*Bandeira*: `{bandeira}`\n*Categoria*: `{categoria}`\n*Banco*:  `{banco}`\n\n*Nome*: `{nome}`\n*CPF*: `{cpf}`"+status, parse_mode='Markdown')

                                    asyncio.run(subtrair_saldo(user_id, preco_cc))
                                    grupos = group_list()
                                    for grupo in grupos:
                                        try:
                                            query.bot.send_message(chat_id=grupo, text=f'💳 | *Cartão comprado!*\n\n*Level*: `{categoria}`\n*Comprador*: `{usernome}`', parse_mode='Markdown')
                                        except:
                                            pass
                                    
                                    asyncio.run(remove_cc(numero, False))

                                else:
                                    query.bot.send_message(chat_id=user_id, text=f'💳 | *O cartão não pode ser comprado por saldo insuficiente!*\n\nO cartão não foi comprado por você já não ter mais o saldo na carteira para isso, provavelmente porque o saldo da sua carteira foi usado para compra de outra CC nesse meio tempo. Contate o suporte caso esse seja um mal entendido!', parse_mode='Markdown')


                            else:
                                contador_die = 0
                                repetidos = []
                                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='💳 |  *Escolhendo outro cartão...*\n\nPedimos que aguarde, pois esse cartão foi recusado, mas estamos escolhendo um outro cartão equivalente para você, por favor aguarde! Isso pode levar um tempo...', parse_mode='Markdown')
                                while True:
                                    print(tipo_p)
                                    if tipo_p.strip() == '':
                                        cc = choose_cc(categoria)
                                    else:
                                        conteudo = ''
                                        if tipo_p == 'bin':
                                            conteudo = bin_cc
                                        elif tipo_p == 'banco':
                                            conteudo = banco
                                        elif tipo_p == 'bandeira':
                                            conteudo = bandeira

                                        cc = choose_cc_especific(conteudo, tipo_p)
                                        
                                    contador_die += 1
                                    try:
                                        if not contador_die >= 20:

                                            if cc[0]:
                                                row = cc[1]
                                                cc_id = row[0]
                                                numero = row[1]
                                                expiracao = is_null(row[2])
                                                cvv = is_null(row[3])
                                                tipo = is_null(row[4])
                                                bandeira = is_null(row[5])
                                                categoria = is_null(row[6])
                                                banco = is_null(row[7])
                                                cpf = is_null(row[9])
                                                nome = is_null(row[10])
                                                comprador = row[11]
                                                hora = row[12]
                                                preco_cc = is_null(asyncio.run(precos(categoria)))
                                            
                                                credit_card = f"{numero}|{expiracao.replace('/', '|')}|{cvv}"
                                                if not credit_card in repetidos:
                                                    repetidos.append(credit_card)
                                                    check = checker(credit_card)
                                                    print(check)
                                                    if check[0] == True:
                                                        cc_usada(credit_card)
                                                        saldo = asyncio.run(pesquisar_id(user_id))[1]
                                                        if int(preco_cc) <= int(saldo):
                                                            update_cc = asyncio.run(update_cartao(cc_id, user_id, hora))
                                                            t = str(time.time())
                                                            keyboard2 = [[InlineKeyboardButton(f'🔄 Não Upou? Tente trocar aqui!', callback_data=f'troca|{t}|{categoria}|{cc_id}'),]]
                                                            
                                                            status = f'\n\n✅ *Status*: `#Aprovado - Retorno: {check[1]}`'

                                                            
                                                            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=cc_buy_warning, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
                                                            if asyncio.run(check_config('troca'))[1] == '1':
                                                                a = query.bot.send_message(chat_id=query.message.chat.id, text=f"💳 | *Produto*:\n\nGARANTIMOS SOMENTE LIVE!\nNÃO GARANTIMOS A APROVAÇÃO\nNÃO GARANTIMOS SALDO\n\n*Card*: `{numero}|{expiracao.replace('/', '|')}|{cvv}`\n*Bandeira*: `{bandeira}`\n*Categoria*: `{categoria}`\n*Banco*:  `{banco}`\n\n*Nome*: `{nome}`\n*CPF*: `{cpf}`"+status, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard2))
                                                            else:
                                                                a = query.bot.send_message(chat_id=query.message.chat.id, text=f"💳 | *Produto*:\n\nGARANTIMOS SOMENTE LIVE!\nNÃO GARANTIMOS A APROVAÇÃO\nNÃO GARANTIMOS SALDO\n\n*Card*: `{numero}|{expiracao.replace('/', '|')}|{cvv}`\n*Bandeira*: `{bandeira}`\n*Categoria*: `{categoria}`\n*Banco*:  `{banco}`\n\n*Nome*: `{nome}`\n*CPF*: `{cpf}`"+status, parse_mode='Markdown')

                                                            asyncio.run(subtrair_saldo(user_id, preco_cc))
                                                            grupos = group_list()
                                                            for grupo in grupos:
                                                                try:
                                                                    query.bot.send_message(chat_id=grupo, text=f'💳 | *Cartão comprado!*\n\n*Level*: `{categoria}`\n*Comprador*: `{usernome}`', parse_mode='Markdown')
                                                                except:
                                                                    pass
                                                            
                                                            asyncio.run(remove_cc(numero, False))

                                                        else:
                                                            query.bot.send_message(chat_id=user_id, text=f'💳 | *O cartão não pode ser comprado por saldo insuficiente!*\n\nO cartão não foi comprado por você já não ter mais o saldo na carteira para isso, provavelmente porque o saldo da sua carteira foi usado para compra de outra CC nesse meio tempo. Contate o suporte caso esse seja um mal entendido!', parse_mode='Markdown')

                                                        break
                                                        

                                                    else:
                                                        asyncio.run(remove_cc(numero, True))
                                                
                                            else:
                                                if tipo_p.strip() == '':
                                                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='💳 | *Sem cartões para a categoria escolhida!*\n\nO estoque da categoria do cartão comprado acabou, e não podemos pegar uma CC equivalente, tente escolher outra CC ou chame o suporte caso o problema percista!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

                                                else:
                                                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'💳 | *Cartões com {tipo_p} especifico(a) acabaram*\n\nO estoque com o(a) {tipo_p} especifico(a) acabou, pesquise por outro cartão ou relecione outro cartão!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
                                                
                                                break
                                        
                                        else:
                                            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='💳 | *Limite ultrrapassado!*\n\nDemorou muito tempo desde a sua compra, por favor, escolha outro level para continuar a comprar CCs ou chame o suporte caso o problema percista!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
                                            break
                                        
                                    except Exception as e:
                                        print(e)
                                        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='💳 | *Cartão não comprado!*\n\nTente escolher outra CC ou chame o suporte caso o problema percista!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
                                        break


                        elif asyncio.run(check_config('checker'))[1] == '0' and asyncio.run(check_config('auto_live'))[1] == '0':
                            update_cc = asyncio.run(update_cartao(cc_id, user_id, hora))
                            
                            if update_cc:
                                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=cc_buy_warning, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
                                context.bot.send_message(chat_id=query.message.chat_id, text=cc_info.format(numero, expiracao, cvv, bandeira, tipo, categoria, banco, cpf, nome, preco_cc), parse_mode='Markdown')
                                asyncio.run(subtrair_saldo(user_id, preco_cc))

                                grupos = group_list()
                                for grupo in grupos:
                                    try:
                                        query.bot.send_message(chat_id=grupo, text=f'💳 | *Cartão comprado!*\n\n*Level*: `{categoria}`\n*Comprador*: `{usernome}`', parse_mode='Markdown')
                                    except:
                                        pass

                            else:
                                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'❌ | {cc_buy_error_2}', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


                    else:
                        query.bot.answer_callback_query(update.callback_query.id, text=f'❕ {cc_buy_error_1}', show_alert=True)

            else:
                query.bot.answer_callback_query(update.callback_query.id, text=f'❕ {cc_buy_error_2}', show_alert=True)

    else:
        try:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=denied_text(user_id), parse_mode='Markdown')
        except:
            update.message.reply_text(text=denied_text(user_id), parse_mode='Markdown')





