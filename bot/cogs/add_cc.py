from telegram.ext import  CallbackContext
from telegram import  Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.functions import people
from random import sample, randint
from bot.cogs.modules.adm_list import adm_list
from bot.cogs.modules.bin_checker import bin_checker
from bot.cogs.modules.card_validator import check_cc
from bot.cogs.modules.database import *
from bot.cogs.modules.separator import separator
from cardvalidator import luhn
import string, os
import asyncio


def bulk_ccs(update, context):
    donos = adm_list()
    name = ''.join(sample(string.ascii_lowercase, 3))
    query = update.message
    user_info = query.from_user
    user_id = str(user_info['id'])
    primeiro_nome = str(user_info['first_name'])
    if not user_id not in donos:
        with open(f"temp/{name}.txt", 'wb') as f:
            context.bot.get_file(update.message.document).download(out=f)

        with open(f"temp/{name}.txt", 'r') as f:
            ccs = str(f.read())

        contagem_erro = 0
        contagem_add = 0
        contagem_nao_add = 0
        cartoes_add = []
        cartoes_nao_add = []

        if not len(ccs) == 0:
            update.message.reply_text(text=bulk_message_accept, parse_mode='Markdown')

            with open(f"temp/{name}.txt", 'r', encoding="utf8") as f:
                ccs = f.read()
                ccs = separator(str(ccs))

                for cc in ccs:
                    cc = cc.strip()
                    check = check_cc(cc)

                    if check[0]:
                        numero = check[1]
                        expiracao = check[2]
                        cvv = check[3]

                        if asyncio.run(check_cc_database(numero)) == None:
                            #teste
                            if luhn.is_valid(numero):
                                b = numero[:6]
                                r = bin_checker(b)
                                pessoa = people()
                                cpf = pessoa[0]
                                cpf_format = cpf[0]+cpf[1]+cpf[2]+'.'+cpf[3]+cpf[4]+cpf[5]+'.'+cpf[6]+cpf[7]+cpf[8]+'-'+cpf[9]+cpf[10]
                                nome = pessoa[1]
                                bandeira = r[0]
                                tipo = r[1]
                                categoria = r[2]
                                banco = r[3]
                                pais = r[4]
                                cc_id = str("{}{}{}{}{}{}{}{}{}{}").format(randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9))
                                comprador = 'None'
                                data = 'None'

                                if categoria.strip() == '':
                                    categoria = 'INDEFINIDO'
                                asyncio.run(add_level(categoria))
                                asyncio.run(cadastrar_cartao(cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome, comprador, data))
                                contagem_add += 1
                                cartoes_add.append(bulk_cc_info_log.format(numero, expiracao, cvv, bandeira, tipo, categoria, banco, cpf_format, nome))

                            else:
                                contagem_nao_add += 1
                                cartoes_nao_add.append(cc+' - '+bulk_error_2+'\n')

                        else:
                            contagem_nao_add += 1
                            cartoes_nao_add.append(cc+' - '+bulk_error_3+'\n')

                    else:
                        contagem_erro += 1

                with open(f'temp/relatorio-{user_id}.txt', 'w', encoding="utf8") as relatorio:
                    lista1 = str(cartoes_add).replace("', ", "").replace("'", "").replace('[', '').replace(']', '').replace(r'\n', '\n')
                    lista2 = str(cartoes_nao_add).replace("', ", "").replace("'", "").replace('[', '').replace(']', '').replace(r'\n', '\n')

                    if lista1.strip() == '':
                        lista1 = null_fields
                        
                    if lista2.strip() == '':
                        lista2 = null_fields
                        
                    relatorio.write(bulk_log.format(primeiro_nome, contagem_erro, contagem_add, contagem_nao_add, lista1, lista2))
                
                context.bot.send_document(chat_id=user_id, document=open(f'temp/relatorio-{user_id}.txt','rb'), caption=bulk_added_cards.format(contagem_erro, contagem_add, contagem_nao_add), parse_mode='Markdown')
                os.remove(f'temp/relatorio-{user_id}.txt')
                check = check_level()
                if not check == 0:
                    query.bot.send_message(chat_id=user_id, text=new_categories.format(check), parse_mode='Markdown')

            os.remove(f"temp/{name}.txt")

        else:
            os.remove(f'temp/{name}.txt')
            update.message.reply_text(text=bulk_message_recuse, parse_mode='Markdown')


def adicionar_cc(update: Update, context: CallbackContext):
    donos = adm_list()
    query = update.message
    user_info = query.from_user
    user_id = str(user_info['id'])

    try:
        if not user_id not in donos:
            ccs = update.message.text
            lista_ccs = separator(ccs)
            if not len(lista_ccs) == 0:
                for cc in lista_ccs:
                    check = check_cc(cc)
                    if check[0]:
                        numero = check[1]
                        expiracao = check[2]
                        cvv = check[3]
                        if asyncio.run(check_cc_database(numero)) == None:
                            if luhn.is_valid(numero) == True:
                                b = numero[:6]
                                r = bin_checker(b)
                                pessoa = people()
                                cpf = pessoa[0]
                                nome = pessoa[1]
                                bandeira = r[0]
                                tipo = r[1]
                                categoria = r[2]
                                banco = r[3]
                                pais = r[4]
                                
                                cc_id = str("{}{}{}{}{}{}{}{}{}{}").format(randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9))
                                comprador = 'None'
                                data = 'None'
                                if categoria == '':
                                    categoria = 'INDEFINIDO'
                                asyncio.run(add_level(categoria))
                                asyncio.run(cadastrar_cartao(cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome, comprador, data))
                                update.message.reply_text(text=added_cc_info.format(b, expiracao, bandeira, tipo, categoria, banco), parse_mode='Markdown')
                            
                                check = asyncio.run(check_level())
                                if not check == 0:
                                    query.bot.send_message(chat_id=user_id, text=new_categorie, parse_mode='Markdown')

                            else:
                                update.message.reply_text(text=added_cc_error_2.format(cc), parse_mode='Markdown')

                        else:
                            update.message.reply_text(text=added_cc_error_3.format(cc), parse_mode='Markdown')

                    else:
                        update.message.reply_text(text=added_cc_error_4.format(cc), parse_mode='Markdown')

            else:
                update.message.reply_text(text=added_cc_error_6, parse_mode='Markdown')

    except Exception as e:
        print('Erro interno: ',e)
        update.message.reply_text(text=added_cc_error_7, parse_mode='Markdown')



