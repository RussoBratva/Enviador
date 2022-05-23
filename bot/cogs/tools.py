from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from bot.cogs.modules.checker import checker
from bot.cogs.modules.card_validator import check_cc
from bot.cogs.modules.bin_checker import bin_checker
from bot.cogs.modules.functions import *
from bot.cogs.modules.separator import separator
from bot.cogs.modules.adm_list import *
import asyncio


def check_none(texto):
    if texto == '':
        return 'N/A'
    else:
        return texto


def ferramentas(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton(f'◀︎ {button_main}', callback_data='main')]]

    texto = '🧰 | *Ferramentas* `[Beta]`\n\n⊛ /chk `<cc>` - Checker de CCs, desconta 1 real a cada live!\n\n⊛ /separador `<lista>` - Organiza uma lista e extrai as CCs dessa lista em um formato mais limpo e organizado!'
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))



def chk(update: Update, context: CallbackContext):
    query = update.message
    user_info = query.from_user
    user_id = str(user_info['id'])
    donos = adm_list()

    if asyncio.run(check_config('checker_publico'))[1] == '1' or user_id in donos:
        try:
            content = update.message.text

            if int(asyncio.run(pesquisar_id(user_id))[1]) >= 1:
                ccs = separator(content)
                if len(ccs) > 0:
                    for cc in ccs:
                        check = check_cc(cc)
                        if check[0]:
                            numero = check[1]
                            mes, ano = check[2].split('/')
                            cvv = check[3]
                            numero_bin = numero[:6]
                            bandeira, tipo, level, banco, pais = bin_checker(numero_bin)
                            bandeira = check_none(bandeira)
                            tipo = check_none(tipo)
                            level = check_none(level)
                            banco = check_none(banco)
                            checker_getnet = checker(cc)
                            
                            if checker_getnet[0]:
                                result = '✅ ', 'Aprovado (Live)', ''
                                asyncio.run(subtrair_saldo(user_id, '1'))
                            else:
                                result = '❌', 'Rejeitado (Die)', ''
                            
                            texto2 = ''

                            texto = '💳 | *CHK*\n\n{} *Retorno*: `{}`\n🔄 *Status*: `{}`\n\nℹ️ | *Informações do cartão*:\n\n💳 *Numero*: `{}`\n📆 *Expiração*: `{}/{}`\n🔐 *cvv*: `{}`\n🏳️ *Bandeira*: `{}`\n⚜️ *Tipo*: `{}`\n💠 *Categoria*: `{}`\n🏛 *Banco*: `{}`'.format(result[0], result[1], checker_getnet[1], numero, mes, ano, cvv, bandeira, tipo, level, banco)+result[2]+texto2

                        else:
                            texto = '❌ | *Erro*\n\nO formato válido deve ser algo como: `/chk xxxxxxxxxxxxxxxx|xx|xx|xxx`'
                        
                        update.message.reply_text(text=texto, parse_mode='Markdown')
                else:
                    texto = '💳 | *CHK*\n\nInsira no mínimo uma CC pra começar a checagem!'
                    update.message.reply_text(text=texto, parse_mode='Markdown')
                        
            else:
                texto = '❌ | *Erro*\n\nVocê precisa ter no mínimo 1 real de saldo para usar esse recurso.'
                update.message.reply_text(text=texto, parse_mode='Markdown')

        except Exception as e:
            print(e)
            update.message.reply_text(text='❌ | *Erro*\n\nOcorreu um erro ao executar esse comando, pode ser que você ainda não esteja cadastrado no bot, se esse for o caso, me mande um "/start"', parse_mode='Markdown')

    else:
        update.message.reply_text(text='❌ | *Erro*\n\nO CHK foi desativado!', parse_mode='Markdown')


def separador(update: Update, context: CallbackContext):
    query = update.message

    try:
        content = update.message.text
        ccs = '\n'.join(separator(content))
        
        if ccs.strip() == '':
            update.message.reply_text(text='📑 | *Separador de CCs*\n\nEnvie uma ou mais listas de CCs para o bot organizar todo para você e colocar as ccs no formato ideal!', parse_mode='Markdown')

        else:
            update.message.reply_text(text=f'📑 | *Separador de CCs*\n\n{ccs}', parse_mode='Markdown')

    except:
        update.message.reply_text(text='❌ | *Erro*\n\nOcorreu um erro ao executar esse comando, pode ser que você ainda não esteja cadastrado no bot, entre em contato com o suporte o bot caso esse erro percista!', parse_mode='Markdown')



