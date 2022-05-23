from random import randint
import json, requests, random
from datetime import datetime, timedelta
import json, time


def contador(start_time):
    with open('config/config.json', 'r', encoding='UTF-8') as file:
        default = json.loads(file.read())['default_api']

    time_sms = 3
    
    try:
        start_time = float(start_time)
        elapsed_time_secs = time.time() - start_time

        msg = str(timedelta(seconds=round(elapsed_time_secs))).split(':')

        minuto = str(int(msg[1])+1)
        segundo = str(60-int(msg[2]))
        if int(segundo) == 60:
            segundo = '59'
        hora = int(msg[0])*60
        
        a = hora+time_sms - int(minuto)
        
        print(minuto)
        if int(minuto) >= time_sms:
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
        
        if int(minuto) >= 1:
            return True, f'{minuto}:{segundo}'
        else:
            return False, f'{minuto}:{segundo}'

    except Exception as e:
        print(e)
        return False, '00:00'


def random_user_agent():
    agent = {}
    def get_os():
        if agent['platform'] == 'Machintosh':
            agent['os'] = random.choice(['68K', 'PPC'])
        elif agent['platform'] == 'Windows':
            agent['os'] = random.choice(['Win3.11', 'WinNT3.51', 'WinNT4.0', 'Windows NT 5.0', 'Windows NT 5.1', 'Windows NT 5.2', 'Windows NT 6.0', 'Windows NT 6.1', 'Windows NT 6.2', 'Win95', 'Win98', 'Win 9x 4.90', 'WindowsCE'])
        elif agent['platform'] == 'X11':
            agent['os'] = random.choice(['Linux i686', 'Linux x86_64'])
            
    def get_browser():
        agent['browser'] = random.choice(['Chrome', 'Firefox', 'IE'])
        
    def get_platform():
        agent['platform'] = random.choice(['Machintosh', 'Windows', 'X11'])
        
    get_platform()
    get_os()
    get_browser()
    
    if agent['browser'] == 'Chrome':
        webkit = str(random.randint(500, 599))
        version = "%s.0%s.%s"%(str(random.randint(0, 24)), str(random.randint(0, 1500)), str(random.randint(0, 999)))
        return "Mozilla/5.0 (%s) AppleWebKit/%s.0 (KHTML, live Gecko) Chrome/%s Safari/%s"%(agent['os'], webkit, version, webkit)
    
    elif agent['browser'] == 'Firefox':
        year = str(random.randint(2000, 2015))
        month = str(random.randint(1, 12)).zfill(2)
        day = str(random.randint(1, 28)).zfill(2)
        gecko = "%s%s%s"%(year, month, day)
        version = "%s.0"%(str(random.randint(1, 15)))
        return "Mozillia/5.0 (%s; rv:%s) Gecko/%s Firefox/%s"%(agent['os'], version, gecko, version)
    
    elif agent['browser'] == 'IE':
        version = "%s.0"%(str(random.randint(1, 10)))
        engine = "%s.0"%(str(random.randint(1, 5)))
        option = random.choice([True, False])
        if option:
            token = "%s;"%(random.choice(['.NET CLR', 'SV1', 'Tablet PC', 'Win64; IA64', 'Win64; x64', 'WOW64']))
        else:
            token = ''
        return "Mozilla/5.0 (compatible; MSIE %s; %s; %sTrident/%s)"%(version, agent['os'], token, engine)


def data(ts):
    t = datetime.utcfromtimestamp(float(ts))

    ano = t.year
    mes = t.month
    dia = t.day
    hora = t.hour
    minutos = t.minute

    return f'{mes:02}/{dia:02}/{ano:02}, {hora:02}:{minutos:02}'


def people():
    with open("assets/pessoas.json", "r", encoding="utf8") as f:
        r = json.load(f)
        pessoas = r['pessoa']
        q = len(pessoas)
        pessoa = pessoas[randint(0, q-1)]

        cpf = pessoa['cpf']
        nome = pessoa['nome']

        return cpf, nome

