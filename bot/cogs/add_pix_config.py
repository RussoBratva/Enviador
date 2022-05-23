from telegram.ext import ConversationHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.modules.pix_authentication import *
from bot.cogs.modules.pix_key_check import *
from bot.cogs.modules.create_cert import *
import os


STEP1, STEP2, STEP3, STEP4, STEP5 = range(5)


def delete_files(lista):
    for item in list(lista):
        try:
            os.remove(item)
        except:
            pass


def menu_pix(update: Update, context: CallbackContext):
    donos = adm_list()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'➕ {button_add_pix}', callback_data='menu_pix')],
        [InlineKeyboardButton(f'📄 {button_added_pix}', callback_data='menu_pix_criados')],])
    query = update.message

    if query is None:
        query = update.callback_query
        
    user_info = query.from_user
    user_id = str(user_info['id'])
    
    if user_id in donos:
        try:
            update.message.reply_text(text=pix_created_list, parse_mode='Markdown', reply_markup=keyboard)

        except:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=pix_created_list, parse_mode='Markdown', reply_markup=keyboard)


def menu_pix_criados(update: Update, context: CallbackContext):
    a = verify_mp()
    b = verify_gn()
    c = verify_key()
    button_list = []
    donos = adm_list()
    
    if a == False:
        padrao = ''
        if verify_default() == 'mp':
            padrao = ' (padrão)'
        button_list.append([InlineKeyboardButton('💲 '+button_mp+padrao, callback_data='edit_mp')])
    if b == False:
        padrao = ''
        if verify_default() == 'gn':
            padrao = ' (padrão)'
        button_list.append([InlineKeyboardButton('💲 '+button_gn+padrao, callback_data='edit_gn')])
    if c == False:
        padrao = ''
        if verify_default() == 'key':
            padrao = ' (padrão)'
        button_list.append([InlineKeyboardButton('💲 '+button_pix_key+padrao, callback_data='edit_key')])

    button_list.append([InlineKeyboardButton('◀︎ '+button_back, callback_data='main_pix')])
    keyboard = InlineKeyboardMarkup(button_list)
    query = update.message

    if query is None:
        query = update.callback_query

    user_info = query.from_user
    user_id = str(user_info['id'])
    
    if user_id in donos:                
        try:
            update.message.reply_text(text=pix_list, parse_mode='Markdown', reply_markup=keyboard)

        except:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=pix_list, parse_mode='Markdown', reply_markup=keyboard)


def edit_mp(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'✅ {button_default_pix}', callback_data='default_mp')],
        [InlineKeyboardButton(f'🗑️ {button_delete_pix}', callback_data='delete_mp')],
        [InlineKeyboardButton(f'◀︎ {button_back}', callback_data='menu_pix_criados')]])

    keyboard2 = InlineKeyboardMarkup([[InlineKeyboardButton(f'◀︎ {button_back}', callback_data='menu_pix_criados')]])
    
    query = update.message

    if query is None:
        query = update.callback_query
    
    q_data = query.data
    lista = ['edit_mp', 'default_mp', 'delete_mp']
    if q_data in lista:
        if not verify_mp():
            if q_data == 'edit_mp':
                padrao = button_no
                if verify_default() == 'mp':
                    padrao = button_yes
                
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=pix_item.format(button_mp, automatic, padrao), parse_mode='Markdown', reply_markup=keyboard)

            elif q_data == 'default_mp':
                register_default_pix('mp')
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=register_default.format(button_mp), parse_mode='Markdown', reply_markup=keyboard2)

            elif q_data == 'delete_mp':
                register_mp_pix('', True)
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=deleted_pix.format(button_mp), parse_mode='Markdown', reply_markup=keyboard2)

        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=error_pix_edit, parse_mode='Markdown', reply_markup=keyboard2)



def edit_gn(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'✅ {button_default_pix}', callback_data='default_gn')],
        [InlineKeyboardButton(f'🗑️ {button_delete_pix}', callback_data='delete_gn')],
        [InlineKeyboardButton(f'◀︎ {button_back}', callback_data='menu_pix_criados')]])


    keyboard2 = InlineKeyboardMarkup([[InlineKeyboardButton(f'◀︎ {button_back}', callback_data='menu_pix_criados')]])
    
    query = update.message

    if query is None:
        query = update.callback_query
    
    q_data = query.data
    lista = ['edit_gn', 'default_gn', 'delete_gn']
    if q_data in lista:
        if not verify_gn():
            if q_data == 'edit_gn':
                padrao = button_no
                if verify_default() == 'gn':
                    padrao = button_yes
                
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=pix_item.format(button_gn, automatic, padrao), parse_mode='Markdown', reply_markup=keyboard)

            elif q_data == 'default_gn':
                register_default_pix('gn')
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=register_default.format(button_gn), parse_mode='Markdown', reply_markup=keyboard2)

            elif q_data == 'delete_gn':
                register_gn_pix('', '', '', True)
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=deleted_pix.format(button_gn), parse_mode='Markdown', reply_markup=keyboard2)

        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=error_pix_edit, parse_mode='Markdown', reply_markup=keyboard2)



def edit_key(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f'✅ {button_default_pix}', callback_data='default_key')],
        [InlineKeyboardButton(f'🗑️ {button_delete_pix}', callback_data='delete_key')],
        [InlineKeyboardButton(f'◀︎ {button_back}', callback_data='menu_pix_criados')]])


    keyboard2 = InlineKeyboardMarkup([[InlineKeyboardButton(f'◀︎ {button_back}', callback_data='menu_pix_criados')]])
    
    query = update.message

    if query is None:
        query = update.callback_query
    
    q_data = query.data
    lista = ['edit_key', 'default_key', 'delete_key']
    if q_data in lista:
        if not verify_key():
            if q_data == 'edit_key':
                padrao = button_no
                if verify_default() == 'key':
                    padrao = button_yes
                
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=pix_item.format(button_pix_key, automatic, padrao), parse_mode='Markdown', reply_markup=keyboard)

            elif q_data == 'default_key':
                register_default_pix('key')
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=register_default.format(button_pix_key), parse_mode='Markdown', reply_markup=keyboard2)

            elif q_data == 'delete_key':
                register_pix_key('', '', True)
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=deleted_pix.format(button_pix_key), parse_mode='Markdown', reply_markup=keyboard2)

        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=error_pix_edit, parse_mode='Markdown', reply_markup=keyboard2)


def add_pix(update: Update, context: CallbackContext):
    donos = adm_list()
    a = verify_mp()
    b = verify_gn()
    c = verify_key()
    button_list = []

    if a:
        button_list.append([InlineKeyboardButton('📋 '+button_register_mp, callback_data='mp_menu_pix')])
    if b:
        button_list.append([InlineKeyboardButton('📋 '+button_register_gn, callback_data='gn_menu_pix')])
    if c:
        button_list.append([InlineKeyboardButton('📋 '+button_register_key, callback_data='key_menu_pix')])

    button_list.append([InlineKeyboardButton('◀︎ '+button_back, callback_data='main_pix')])
    keyboard = InlineKeyboardMarkup(button_list)
    query = update.message
    if query is None:
        query = update.callback_query
    user_info = query.from_user
    user_id = str(user_info['id'])
    
    if user_id in donos:    
            
        try:
            update.message.reply_text(text=pix_not_created_list, parse_mode='Markdown', reply_markup=keyboard)

        except:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=pix_not_created_list, parse_mode='Markdown', reply_markup=keyboard)


def add_gn_pix_start(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('📋 '+button_register_gn, callback_data='criar_pix_gn')],
                                [InlineKeyboardButton('◀︎ '+button_back, callback_data='menu_pix')]])
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,text=pix_gn, parse_mode='Markdown', reply_markup=keyboard)


def add_gn_pix(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('❌ '+button_cancel, callback_data='cancelar_criacao_pix_gn')]])
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=add_gn_pix_1, parse_mode='Markdown', reply_markup=keyboard)

    with open('temp/cache_message_gn.json', 'w') as file:
        a = {"message_id": str(query.message.message_id)}
        w = json.dumps(a, indent=4)
        file.write(w)


    return STEP1


def add_gn_pix2(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('❌ '+button_cancel, callback_data='cancelar_criacao_pix_gn')]])
    keyboard2 = InlineKeyboardMarkup([[InlineKeyboardButton('◀︎ '+button_back, callback_data='menu_pix')]])
    
    with open('temp/cache_message_gn.json', 'r') as file:
        a = json.loads(file.read())
        m_id = a['message_id']

    with open("temp/cert_gn.p12", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
    
    verify_cert = create_cert_gerencianet()
    
    update.message.delete()
    
    if verify_cert == False:
        context.bot.edit_message_text(chat_id=update.message.from_user['id'], message_id=m_id, text=error_pix_gn_1, parse_mode='Markdown', reply_markup=keyboard2)
        os.remove("temp/cert_gn.p12")
        os.remove('temp/cache_message_gn.json')
        os.remove('config/cert/cert-gn.pem')

        return ConversationHandler.END

    else:
        os.remove("temp/cert_gn.p12")
        context.bot.edit_message_text(chat_id=update.message.from_user['id'], message_id=m_id, text=add_gn_pix_2, parse_mode='Markdown', reply_markup=keyboard)

        return STEP2


def add_gn_pix3(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('❌ '+button_cancel, callback_data='cancelar_criacao_pix_gn')]])
    keyboard2 = InlineKeyboardMarkup([[InlineKeyboardButton('◀︎ '+button_back, callback_data='menu_pix')]])
    
    texto = update.message.text
    
    update.message.delete()

    with open('temp/cache_message_gn.json', 'r') as file:
        a = json.loads(file.read())
        m_id = a['message_id']

    if len(texto.strip()) == 50:
        register_gn_pix('', texto, '')
        context.bot.edit_message_text(chat_id=update.message.from_user['id'], message_id=m_id,text=add_gn_pix_3.format(texto), parse_mode='Markdown', reply_markup=keyboard)
        return STEP3

    else:
        register_gn_pix('', '', '', True)
        context.bot.edit_message_text(chat_id=update.message.from_user['id'], message_id=m_id,text=error_pix_gn_2, parse_mode='Markdown', reply_markup=keyboard2)
        os.remove('temp/cache_message_gn.json')
        os.remove('config/cert/cert-gn.pem')
        return ConversationHandler.END


def add_gn_pix4(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('❌ '+button_cancel, callback_data='cancelar_criacao_pix_gn')]])
    keyboard2 = InlineKeyboardMarkup([[InlineKeyboardButton('◀︎ '+button_back, callback_data='menu_pix')]])
    
    texto = update.message.text
    update.message.delete()

    with open('temp/cache_message_gn.json', 'r') as file:
        a = json.loads(file.read())
        m_id = a['message_id']

    with open('config/config_pix.json', 'r') as file:
        f = json.loads(file.read())
        gn_client_id = f['gn']['client_id']

    if len(texto.strip()) == 54:
        register_gn_pix('', '', texto)
        context.bot.edit_message_text(chat_id=update.message.from_user['id'], message_id=m_id,text=add_gn_pix_4.format(gn_client_id, texto), parse_mode='Markdown', reply_markup=keyboard)
        return STEP4

    else:
        register_gn_pix('', '', '', True)
        context.bot.edit_message_text(chat_id=update.message.from_user['id'], message_id=m_id,text=error_pix_gn_3, parse_mode='Markdown', reply_markup=keyboard2)
        os.remove('temp/cache_message_gn.json')
        os.remove('config/cert/cert-gn.pem')
        return ConversationHandler.END


def add_gn_pix5(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('◀︎ '+button_back, callback_data='menu_pix')]])
    
    texto = update.message.text
    update.message.delete()
    
    with open('temp/cache_message_gn.json', 'r') as file:
        a = json.loads(file.read())
        m_id = a['message_id']
    
    register_gn_pix(texto, '', '')
    
    check = gn_authentication()
    
    if check == True:
        context.bot.edit_message_text(chat_id=update.message.from_user['id'], message_id=m_id,text=add_gn_pix_5, parse_mode='Markdown', reply_markup=keyboard)
        os.remove('temp/cache_message_gn.json')
        return ConversationHandler.END

    else:
        context.bot.edit_message_text(chat_id=update.message.from_user['id'], message_id=m_id,text=error_pix_gn_4, parse_mode='Markdown', reply_markup=keyboard)
        os.remove('temp/cache_message_gn.json')
        os.remove('config/cert/cert-gn.pem')
        return ConversationHandler.END


def add_mp_pix_start(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('📋 '+button_register_mp, callback_data='criar_pix_mp')],
                                [InlineKeyboardButton('◀︎ '+button_back, callback_data='menu_pix')]])
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,text=pix_mp, parse_mode='Markdown', reply_markup=keyboard)


def add_mp_pix(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('❌ '+button_cancel, callback_data='cancelar_criacao_pix_mp')]])
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=add_mp_pix_1, parse_mode='Markdown', reply_markup=keyboard)

    with open('temp/cache_message_mp.json', 'w') as file:
        a = {"message_id": str(query.message.message_id)}
        w = json.dumps(a, indent=4)
        file.write(w)

    return STEP1


def add_mp_pix2(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('◀︎ '+button_back, callback_data='menu_pix')]])
    texto = update.message.text
    
    with open('temp/cache_message_mp.json', 'r') as file:
        a = json.loads(file.read())
        m_id = a['message_id']
    
    register_mp_pix(texto)
    check = mp_authentication()
    update.message.delete()
    
    if check == True:
        context.bot.edit_message_text(chat_id=update.message.from_user['id'], message_id=m_id,text=add_mp_pix_2, parse_mode='Markdown', reply_markup=keyboard)
        os.remove('temp/cache_message_mp.json')
        return ConversationHandler.END

    else:
        context.bot.edit_message_text(chat_id=update.message.from_user['id'], message_id=m_id,text=error_pix_mp, parse_mode='Markdown', reply_markup=keyboard)
        os.remove('temp/cache_message_mp.json')
        return ConversationHandler.END


def add_key_pix_start(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('📋 '+button_register_key, callback_data='criar_pix_key')],
                                [InlineKeyboardButton('◀︎ '+button_back, callback_data='menu_pix')]])
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,text=pix_key, parse_mode='Markdown', reply_markup=keyboard)


def add_key_pix0(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(button_cpf, callback_data='pix_cpf'),
        InlineKeyboardButton(button_cnpj, callback_data='pix_cnpj')],
        [InlineKeyboardButton(button_telefone, callback_data='pix_telefone'),
        InlineKeyboardButton(button_email, callback_data='pix_email')],
        [InlineKeyboardButton(button_key, callback_data='pix_aleatoria')],
        [InlineKeyboardButton('❌ '+button_cancel, callback_data='cancelar_criacao_pix_mp')]])
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="💲 | *Adcionar chave PIX (1/4)*\n\nDigite o tipo de chave PIX que você tem e deseja inserir no bot!", parse_mode='Markdown', reply_markup=keyboard)


def add_key_pix1(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('◀︎ '+button_back, callback_data='cancelar_criacao_pix_key')]])
    q_data = query.data
    
    if q_data == 'pix_cpf':
        tipo = 'CPF'

    elif q_data == 'pix_cnpj':
        tipo = 'CNPJ'
        
    elif q_data == 'pix_telefone':
        tipo = 'telefone'
        
    elif q_data == 'pix_email':
        tipo = 'e-mail'
        
    elif q_data == 'pix_aleatoria':
        tipo = 'aleatoria'
    
    else:
        tipo = ''
    
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=add_pix_key_1.format(tipo), parse_mode='Markdown', reply_markup=keyboard)

    with open('temp/cache_message_key.json', 'w') as file:
        a = {"message_id": str(query.message.message_id), "tipo": tipo}
        w = json.dumps(a, indent=4)
        file.write(w)

    return STEP1


def add_key_pix2(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('📋 '+button_register_key, callback_data='menu_pix')]])

    update.message.delete()
    texto = str(update.message.text).strip().replace(' ', '')
    
    with open('temp/cache_message_key.json', 'r') as file:
        a = json.loads(file.read())
        m_id = a['message_id']
        tipo = a['tipo']
    
    check = False
    
    if tipo == 'CPF':
        r = cpf(texto)
        texto = texto.replace('.', '').replace('-', '')
        if r == True:
            check = True
    
    elif tipo == 'CNPJ':
        r = cnpj(texto)
        texto = texto.replace('.', '').replace('-', '').replace('/', '')
        if r == True:
            check = True
    
    elif tipo == 'telefone':
        r = telefone(texto)
        texto = texto.replace('(', '').replace(')', '').replace('-', '')
        if r == True:
            check = True
    
    elif tipo == 'e-mail':
        r = email(texto)
        if r == True:
            check = True

    elif tipo == 'aleatoria':
        r = chave_aleatoria(texto)
        if r == True:
            check = True
    
    if check == True:
        register_pix_key(texto, tipo)
        os.remove('temp/cache_message_key.json')
        context.bot.edit_message_text(chat_id=update.message.from_user['id'], message_id=m_id,text=add_pix_key_2, parse_mode='Markdown', reply_markup=keyboard)
        return ConversationHandler.END

    else:
        context.bot.edit_message_text(chat_id=update.message.from_user['id'], message_id=m_id,text=error_pix_key, parse_mode='Markdown', reply_markup=keyboard)
        os.remove('temp/cache_message_key.json')
        return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('◀︎ '+button_back, callback_data='menu_pix')]])
    query = update.callback_query

    d = ['temp/cache_message_gn.json', 'temp/cache_message_mp.json', 'temp/cache_message_key.json']

    if query.data == 'cancelar_criacao_pix_mp':
        register_mp_pix('', True)
        p = 'temp/cache_message_mp.json'
    
    elif query.data == 'cancelar_criacao_pix_gn':
        register_gn_pix('', '', '', True)
        p = 'temp/cache_message_gn.json'
        d.append('config/cert/cert-gn.pem')
        
    elif query.data == 'cancelar_criacao_pix_key':
        register_pix_key('', '', True)
        p = 'temp/cache_message_key.json'
    
    else:
        p = ''
    
    try:
        with open(p, 'r') as file:
            a = json.loads(file.read())
            m_id = a['message_id']

        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, message_id=m_id,text='*Cadastro PIX cancelado*', parse_mode='Markdown', reply_markup=keyboard)

    except:
        update.message.reply_text(text='*Cadastro PIX cancelado*', parse_mode='Markdown', reply_markup=keyboard)

    
    delete_files(d)

    return ConversationHandler.END

