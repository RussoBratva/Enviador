from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.modules.relatorio import stats


def set_button(tipo):
    def if_selected(tipo, button):
        if str(tipo) == str(button):
            return '✅'
        else:
            return '□'

    keyboard = [
            [InlineKeyboardButton(f'{if_selected(tipo, "1")} Hoje', callback_data='stats_1'),
            InlineKeyboardButton(f'{if_selected(tipo, "2")} Em 2 dias', callback_data='stats_2'),
            InlineKeyboardButton(f'{if_selected(tipo, "3")} Em 3 dias', callback_data='stats_3')],
            [InlineKeyboardButton(f'{if_selected(tipo, "4")} Em 4 dias', callback_data='stats_4'),
            InlineKeyboardButton(f'{if_selected(tipo, "5")} Em 5 dias', callback_data='stats_5'),
            InlineKeyboardButton(f'{if_selected(tipo, "6")} Em 6 dias', callback_data='stats_6')],
            [InlineKeyboardButton(f'{if_selected(tipo, "7")} Em 7 dias', callback_data='stats_7'),
            InlineKeyboardButton(f'{if_selected(tipo, "15")} Em 15 dias', callback_data='stats_15'),
            InlineKeyboardButton(f'{if_selected(tipo, "30")} Em 30 dias', callback_data='stats_30')]
            ]

    return keyboard


def estatisticas(update: Update, context: CallbackContext):
    query = update.message
    tipo_msg = 1

    if query is None:
        query = update.callback_query
        tipo_msg = 2

    user_info = query.from_user
        
    try:
        tipo = str(query.data).replace('stats_', '')
    except:
        tipo = '1'
    
    user_info = query.from_user
    user_id = str(user_info['id'])
    donos = adm_list()
    
    if user_id in donos:
        keyboard = set_button(tipo)
        data = stats()
        lista_tipos = ['1', '2', '3', '4', '5', '6', '7', '15', '30']

        if str(tipo) in lista_tipos:
            usuarios = data['relatorio']['usuarios']['quantidade'][tipo]
            ccsquantidade =  data['relatorio']['ccs']['quantidade'][tipo]
            ccsganho = data['relatorio']['ccs']['ganho'][tipo]
            recargasquantidade =  data['relatorio']['recargas']['quantidade'][tipo]
            recargasganho = data['relatorio']['recargas']['ganho'][tipo]
            giftsquantidade =  data['relatorio']['gifts']['quantidade'][tipo]
            giftsganho = data['relatorio']['gifts']['ganho'][tipo]

            if tipo == '1':
                periodo = 'hoje'
            else:
                periodo = f'nos ultímos {tipo} dias'

            text = f'📊 | *Estatistícas*:\n\n🗣️ *Novos usuários* ({periodo}): `{usuarios}`\n\n💳 *CCs vendidas* ({periodo}):\n\n*Quantidade de ccs vendidas*: `{ccsquantidade}`\n*Total ganho em CCs*: `{ccsganho}`\n\n💸 *Recargas via PIX* ({periodo}):\n\n*Total de recargas feitas*: `{recargasquantidade}`\n*Total em recargas*: `{recargasganho}`\n\n🎟️ *Gifts resgatados* ({periodo}):\n\n*Total de gifts resgatados*: `{giftsquantidade}`\n*Total em gifts*: `{giftsganho}`'

        else:
            text = '❌ | *Erro*\n\nErro ao gerar estatísticas!'
        
        if tipo_msg == 1:
            query.bot.send_message(chat_id=user_id, text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
        
        else:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))




