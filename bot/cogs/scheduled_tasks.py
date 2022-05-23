from bot.cogs.modules.import_text_variables import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
#from bot.cogs.modules.relatorio import relatorio
from bot.cogs.modules.adm_list import *
from bot.cogs.modules.mp_pix import pix as pix_mp_1, status as status_mp
from bot.cogs.modules.gn_pix import pix as pix_gn_1, status as status_gn
from bot.cogs.modules.qr import remove, qrimg
from bot.cogs.modules.pix_authentication import *
from bot.cogs.modules.group_list import group_list
from bot.cogs.modules.database import *
from datetime import datetime, timedelta
import os, asyncio


def time_diference(start_time):
    try:
        start_time = float(start_time)
        elapsed_time_secs = time.time() - start_time

        msg = str(timedelta(seconds=round(elapsed_time_secs))).split(':')

        hora = msg[0]
        

        if int(hora) <= 1:
            return True
        else:
            print('false')
            return False
    except: 
        return False


def scheduled_tasks(context):
    path = 'temp'
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    text2 = 'Não é mais possível deletar essa mensagem devido a limitações do Telegram!'

    for file in files:
        if 'send-' in file:
            file_path = str(path)+'/'+str(file)
            date_creation = os.path.getmtime(file_path)
            diff = relativedelta(datetime.now(), datetime.utcfromtimestamp(float(date_creation)))
            if diff.hours >= 48:
                with open(file_path, 'r') as f:
                    load = json.loads(f.read())
                    text = load['text']
                    user_id = load['chat_id']
                    message_id = load['message_id']

                try:
                    context.bot.edit_message_text(chat_id=user_id, message_id=message_id, text=text+'\n\n'+text2)
                except:
                    pass

                os.remove(file_path)


def backup_task(context):
    donos = adm_list()
    for dono in donos:
        context.bot.send_document(chat_id=dono, document=open('database.db','rb'), caption='| *Backup diário*\n\nBackup do banco de dados nas Ultimas 12 horas!', parse_mode='Markdown')


def payment_checker(context):
    print('\n\nOi filho da puta\n\n')
    path = 'temp'
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    pix = []
    for file in files:
        if 'pix-' in file:
            pix.append(str(path)+'/'+str(file))
    
    for c in range(0, len(pix)):
        file_path = pix[c]
        with open(file_path, 'r') as file:
            load = json.loads(file.read())
        
        tipo = load['tipo']
        preco = str(load['preco'])
        id_user = load['usuario']
        pesquisa = asyncio.run(pesquisar_id(str(id_user)))
        user_nome = pesquisa[2]
        criado_em = load['criado_em']
        id_p = load['id_p']

        if time_diference(str(criado_em)) == True:
            try:
                if tipo == 'mp':
                    status_order = status_mp(str(id_p))
                    print('Status da ordem:', status_order, 'User:', user_nome)

                    if status_order == True:
                        if asyncio.run(pesquisar_recarga(id_p)) is None:
                            print('Preparando pra adiconar saldo para:', user_nome)
                            asyncio.run(add_saldo(str(id_user), str(preco)))
                            print('Saldo adicionado para:', user_nome)
                            asyncio.run(registrar_recarga(id_user, preco, str(id_p)))
                            context.bot.send_message(chat_id=id_user, text=payed_profile_alert.format(preco, id_p, pesquisa[1]), parse_mode='Markdown')
                            
                            if asyncio.run(check_config('afiliado'))[1] == '1':
                                comitado = asyncio.run(comissao(id_user, preco))
                                pesquisar_afiliado = asyncio.run(check_afiliado(id_user))

                                if comitado:
                                    if pesquisar_afiliado is not None:
                                        calculo = int(preco) - int(int(preco) * (1 - 10 / 100))
                                        try:
                                            context.bot.send_message(chat_id=pesquisar_afiliado, text=afiliate_added_credit_alert.format(user_nome, preco, calculo), parse_mode='Markdown')

                                        except:
                                            pass
                            
                            grupos = group_list()

                            for grupo in grupos:
                                try:
                                    context.bot.send_message(chat_id=grupo, text=payed_group_alert.format(user_nome, id_user, preco), parse_mode='Markdown')
                                except:
                                    pass
                            
                        os.remove(file_path)
                            

                elif tipo == 'gn':
                    status_order = status_gn(str(id_p))

                    if status_order == True:
                        if asyncio.run(pesquisar_recarga(id_p)) is None:
                            asyncio.run(add_saldo(str(id_user), str(preco)))
                            pesquisa = asyncio.run(pesquisar_id(str(id_user)))
                            user_nome = pesquisa[2]
                            asyncio.run(registrar_recarga(id_user, preco, str(id_p)))
                            context.bot.send_message(chat_id=id_user, text=payed_profile_alert.format(preco, id_p, pesquisa[1]), parse_mode='Markdown')
                            
                            if asyncio.run(check_config('afiliado'))[1] == '1':
                                comitado = asyncio.run(comissao(id_user, preco))
                                pesquisar_afiliado = asyncio.run(check_afiliado(id_user))

                                if comitado:
                                    if pesquisar_afiliado is not None:
                                        calculo = int(preco) - int(int(preco) * (1 - 10 / 100))
                                        try:
                                            context.bot.send_message(chat_id=pesquisar_afiliado, text=afiliate_added_credit_alert.format(user_nome, preco, calculo), parse_mode='Markdown')

                                        except:
                                            pass
                            
                            grupos = group_list()

                            for grupo in grupos:
                                try:
                                    context.bot.send_message(chat_id=grupo, text=payed_group_alert.format(user_nome, id_user, preco), parse_mode='Markdown')
                                except:
                                    pass
                            
                        os.remove(file_path)

                else:
                    context.bot.send_message(chat_id=id_user, text=expired_pay.format(preco), parse_mode='Markdown')
                    os.remove(file_path)

            except Exception as e:
                print(f'Erro ao adicionar saldo: {e}')

        else:
            os.remove(file_path)


