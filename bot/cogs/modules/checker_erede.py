import requests, random, json, time, base64
from requests.structures import CaseInsensitiveDict
from deep_translator import GoogleTranslator


with open('config/config_checker.json', 'r', encoding='UTF-8') as file:
    erede_c = json.loads(file.read())['erede']
    pv = erede_c['pv']
    token = erede_c['token']
    auth = f'{pv}:{token}'
    token = str(base64.b64encode(auth.encode())).replace("b'", '').replace("'", '')


def erede(cc):
    if len(cc.split("|")) == 4:
        url = "https://api.userede.com.br/erede/v1/transactions"

        debitar = random.randint(100, 200)

        numero, mes, ano, cvv = cc.split('|')
        
        if len(ano) == 2:
            ano = '20'+ano

        try:
            headers = CaseInsensitiveDict()
            headers["authorization"] = f"Basic {token}"
            headers["Content-Type"] = "application/json"
            reference = str(random.randint(1111111, 9999999))

            data = f'"Capture":true,"Kind":"credit","Reference":"{reference}","Amount":"{debitar}","Installments":1,"CardHolderName":"joao da silva","CardNumber":"{numero}","ExpirationMonth":"{mes}","ExpirationYear":"{ano}","SecurityCode":"{cvv}","Subscription":false'

            resp = requests.post(url, headers=headers, data='{'+data+'}').text

            load = json.loads(resp)
            retorno = load['returnMessage']
            code = load['returnCode']
            
            if code == '00':
                result = True
            else:
                result = False
            
            debitar = str(debitar)
            preco = f'R${debitar[0]},{debitar[1]}{debitar[2]}'
            retorno = GoogleTranslator(source='auto', target='pt').translate(retorno)
        
            return result, f'{retorno} - Code: {code} - {preco}'

        except:
            return False, 'Request inválido ao Gateway'

    else:
        return False, 'Parâmetros insuficientes'

