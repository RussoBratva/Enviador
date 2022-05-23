from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from bot.cogs.modules.separator import *
from bot.cogs.modules.support import *
from bot.cogs.modules.checker import *
from bot.cogs.modules.functions import *
import asyncio, random, json


def is_null(content):
    if content.strip() == '' or content.strip() == 'None':
        return 'N/A'
    else:
        return content


def cc_usada(cc):
    if not os.path.isfile('temp/compradas'):
        with open('temp/compradas', 'w', encoding='UTF-8') as file:
            file.write('')
            
    with open('temp/compradas', 'a', encoding='UTF-8') as file:
        file.write(str(cc)+'\n')


with open('config/config.json', 'r', encoding='UTF-8') as file:
    try:
        tempo_de_troca = int(json.loads(file.read())['exchange_time_in_minutes'])
    except:
        tempo_de_troca = 7


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


def choose_cc(level):
    rows = asyncio.run(pesquisar_categoria(level))
    q = len(rows)
    if not q == 0:
        if q > 0:
            row = list(rows[random.randint(0, len(rows)-1)])

            if asyncio.run(check_comprada(row[1])):
                return True, row
            else:
                row = []
            
            if rows == []:
                return False, []

        else:
            return False, []

    else:
        return False, []


def troca(update: Update, context: CallbackContext):
    query = update.callback_query
    user_info = query.from_user
    user_id = str(user_info['id'])

    texto = query.message.text
    cc = separator(query.message.text)[0]

    call, tempo, level, cc_id = query.data.split('|')
    t = time_diference(tempo)

    if t[0] == True and int(t[1].split(':')[0]) <= tempo_de_troca:
        if asyncio.run(check_config('checker'))[1] == '1':
            a = query.bot.send_message(chat_id=query.message.chat.id, text=f"💳 | *Verificando disponibilidade de troca*\n\nEstamos verificando a possibilidade de troca...", parse_mode='Markdown')
            recheck = checker(cc)
            if recheck[0] == False:
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=a.message_id, text=f"💳 | *Trocando CC*\n\nA sua CC está sendo trocada, por favor, aguarde...", parse_mode='Markdown')
                while True:
                    contador_die = 0
                    contador_die += 1
                    repetidos = []
                    try:
                        if not contador_die >= 40:
                            cc = choose_cc(level)
                            if cc[0] == True and not cc[1] == []:
                                row = cc[1]
                                cc_id = cc[0]
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
                                    if check[0] == True and not a_cc_foi_usada(credit_card):
                                        cc_usada(credit_card)
 
                                        update_cc = asyncio.run(update_cartao(cc_id, user_id, hora))

                                        status = f'\n\n✅ *Status*: `#Aprovado - Retorno: {check[1]}`'

                                        query.bot.send_message(chat_id=query.message.chat.id, text=f"💳 | *Produto*:\n\n*Nota*: Sua CC foi trocada com sucesso!\n\nGARANTIMOS SOMENTE LIVE!\nNÃO GARANTIMOS A APROVAÇÃO\nNÃO GARANTIMOS SALDO\n\n*Card*: `{numero}|{expiracao.replace('/', '|')}|{cvv}`\n*Bandeira*: `{bandeira}`\n*Categoria*: `{categoria}`\n*Banco*:  `{banco}`\n\n*Nome*: `{nome}`\n*CPF*: `{cpf}`"+status, parse_mode='Markdown')
                                        query.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)

                                        break
                                        

                                    else:
                                        asyncio.run(remove_cc(numero))

                            else:
                                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=a.message_id, text='💳 | *CCs equivalentes acabaram!*\n\nNão foi possível realizar a troca, pois as ccs do nível especifico acabaram. Tente entrar em contato com o suporte caso seja necessário resolver o problema!', parse_mode='Markdown')
                                break

                        else:
                            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=a.message_id, text='💳 | *Limite de CCs escolhidas pela troca ultrapassado!*\n\nNão conseguimos escolher uma CC equivalente para troca, devido a limitações do checker, entre em contato com o suporte!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
                            break
                        
                    except Exception as e:
                        print(f'\n\n\nErro aqui: {e}\n\n\n')
                        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=a.message_id, text='💳 | *O Cartão não pode ser trocado!*\n\nTente escolher outra CC ou chame o suporte caso o problema percista!', parse_mode='Markdown')
                        break
            else:
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=a.message_id, text=f"❌ | *CC está live!*\n\nA troca não pode ser feita, devido ao fato da CC estar live!", parse_mode='Markdown')
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=texto, parse_mode='Markdown')
    else:
        if int(t[1].split(':')[0]) <= tempo_de_troca:
            text = f'❌ Para evitar abusos, você pode contratar a troca após 1 minuto! Se passou: {t[1]} desde a contratação...'
        else:
            text = f'❌ Se passou muito tempo desde a contratação de troca de {tempo_de_troca} minuto(s)'
        
        query.bot.answer_callback_query(update.callback_query.id, text=text, show_alert=True)










