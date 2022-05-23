from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.modules.database import *
from bot.cogs.ban import *
import asyncio


def unitaria(update: Update, context: CallbackContext):
    rows = asyncio.run(all_ccs())
    query = update.callback_query
    user_info = query.from_user
    user_id = str(user_info['id'])
    
    if check_status(user_id):
        buttons = []
        results = []
        for row in rows:
            categoria = row[6]
            results.append(categoria)

        if not len(results) == 0:
            checkados = []
            levels1 = []
            levels2 = []
            con = 0
            
            for c in results:
                if c not in checkados:
                    con += 1
                    contagem = results.count(c)
                    checkados.append(c)
                    price = asyncio.run(level_price(c))
                    if not price == no_price:
                        level = f'{c} ({contagem})'
                        levels1.append(level)

            aLista = iter(levels1)
            result = []
            result2 = []

            for i in aLista:
                try:
                    result.append(i)
                    result2.append(next(aLista))

                except Exception:
                    if i not in result:
                        result.append(i)
                        
                        
            for var1, var2 in zip(result, result2):
                buttons.append([InlineKeyboardButton(text=var1, callback_data='~'+var1.replace('({new})', '')), InlineKeyboardButton(text=var2, callback_data='~'+var2.replace('({new})', ''))])

            q1 = len(result)+len(result2)
            if q1 >= 3:
                if not (q1%2) == 0:
                    var1 = result[len(result)-1]
                    buttons.append([InlineKeyboardButton(text=var1, callback_data='~'+var1.replace('({new})', ''))])

            if q1 == 1:
                var1 = result[0]
                buttons.append([InlineKeyboardButton(text=var1, callback_data='~'+var1.replace('({new})', ''))])

            
            buttons.append([InlineKeyboardButton(f'◀︎ {button_back}', callback_data='m1')])
            keyboard = InlineKeyboardMarkup(buttons)
            results1 = []
            
            for categoria in checkados:
                row1 = asyncio.run(pesquisar_info_categoria(categoria))
                if row1 == None:
                    pass
                
                else:
                    preco = row1[1]
                    if not preco == 'None':
                        results1.append(f'- *{row1[0]}*: `R${row1[1]},00`\n')

            if asyncio.run(check_config('checker'))[1] == '1':
                text_check = '⚠️ *Avisos*:\n\n__- O checker está ativo, portanto ele irá checar as CCs antes da compra!__'
            else:
                text_check = ''


            if not len(results1) == 0:
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'{unitary}\n\n'+str(results1).replace(r'\n', '\n').replace('[', '').replace(']', '').replace("', ", '').replace("'", '')+'\n\n'+text_check, parse_mode='Markdown', reply_markup=keyboard)

            else:
                keyboard = [[InlineKeyboardButton(f'◀︎ {button_back}', callback_data='m1')]]
                keyboard2 = InlineKeyboardMarkup(keyboard)
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'{unitary}\n\n{stock_null}', parse_mode='Markdown', reply_markup=keyboard2)

        else:
            buttons.append([InlineKeyboardButton(f'◀︎ {button_back}', callback_data='m1')])
            keyboard = InlineKeyboardMarkup(buttons)
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'{unitary}\n\n{stock_null}', parse_mode='Markdown', reply_markup=keyboard)

    else:
        try:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=denied_text(user_id), parse_mode='Markdown')
        except:
            update.message.reply_text(text=denied_text(user_id), parse_mode='Markdown')


def preco_unitaria(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message

    if query is None:
        query = update.callback_query
        user_info = query.from_user

    else:
        user_info = query.from_user
    user_id = str(user_info['id'])
    if check_status(user_id):
        if query is None:
            query = update.callback_query
            user_info = query.from_user
            user_id = str(user_info['id'])

        else:
            user_info = query.from_user
            user_id = str(user_info['id'])

        if user_id in donos:
            rows = asyncio.run(all_precos())
            con = 0
            
            results1= []
            results2= []
            for row in rows:
                row1 = asyncio.run(pesquisar_info_categoria(row[0]))
                preco = row1[1]
                if not preco == 'None':
                    results1.append(row[0])
                else:
                    results1.append(row[0]+f' ({new})')
                
            aLista = iter(results1)
            result = []
            result2 = []

            for i in aLista:
                try:
                    result.append(i)
                    result2.append(next(aLista))

                except Exception:
                    if i not in result:
                        result.append(i)

            buttons = []
            for var1, var2 in zip(result, result2):
                buttons.append([InlineKeyboardButton(text=var1, callback_data='^'+var1.replace('({new})', '')), InlineKeyboardButton(text=var2, callback_data='^'+var2.replace('({new})', ''))])

            q1 = len(result)+len(result2)
            if q1 >= 3:
                if not (q1%2) == 0:
                    var1 = result[len(result)-1]
                    buttons.append([InlineKeyboardButton(text=var1, callback_data='^'+var1.replace('({new})', ''))])

            buttons.append([InlineKeyboardButton(text=f'◀︎ {button_back}', callback_data='editar_precos')])

            keyboard = InlineKeyboardMarkup(buttons)

            try:
                update.message.reply_text(text=price_edit_text.format(new), parse_mode='Markdown', reply_markup=keyboard)

            except:
                query = update.callback_query
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=price_edit_text.format(new), parse_mode='Markdown', reply_markup=keyboard)

    else:
        try:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=denied_text(user_id), parse_mode='Markdown')
        except:
            update.message.reply_text(text=denied_text(user_id), parse_mode='Markdown')

