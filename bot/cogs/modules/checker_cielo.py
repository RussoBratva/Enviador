import requests, json
from unidecode import unidecode
from fordev.generators import people
import random, time


with open('config/config_checker.json', 'r') as file:
    cielo_c = json.loads(file.read())['cielo']
    cieloMerchantId = cielo_c['cieloMerchantId']
    cieloMerchantKey = cielo_c['cieloMerchantKey']


def get_brand(cc):
    try:
        info_cc = requests.get("http://140.82.31.167/search/bin="+cc[:6]).json()
        band = info_cc.get('bandeira').lower().capitalize().replace('card','')

        if 'American express' in band:
            band ="AMEX"

        if info_cc.get('bin')[:2] == "65":
            band = 'discover'

        if "ELO" in band or "Hiper" in band:
            band = "Elo"
    except:
        band = 'Master'
    
    return band


def cielo(cc):
    if len(cc.split("|")) == 4:
        numero, mes, ano, cvv = cc.split('|')
        if len(ano) == 2:
            ano = '20'+ano
        
        headers = {
            'MerchantId':cieloMerchantId,
            'MerchantKey': cieloMerchantKey,
            'Content-Type': 'application/json'
            }

        payload = {
            "MerchantOrderId": str(random.randint(1111111111, 9999999999)),
            "Customer":{
                "Name": unidecode(people()['nome'])
            },
            "Payment":{
                "Type":"CreditCard",
                "Amount": str(random.randint(100,200)),
                "Installments":1,
                "SoftDescriptor": "123456789ABCD",
                "CreditCard":{
                    "CardNumber": str(numero),
                    "Holder": unidecode(people()['nome']),
                    "ExpirationDate": f'{mes}/{ano}',
                    "SecurityCode": str(cvv),
                    "Brand": get_brand(numero),
                    "CardOnFile":{ 
                        "Usage": "Used", 
                        "Reason":"Unscheduled" }},
                    "IsCryptoCurrencyNegotiation": False
                }
            }


        try:
            response = requests.post('https://api.cieloecommerce.cielo.com.br/1/sales', headers=headers, json=payload)

            print(response.text)

            load = json.loads(response.text)
            valor = load['Payment']['Amount']
            status = load['Payment']['ReturnCode']
            msg = load['Payment']['ReturnMessage']
            
            if load['Payment']['ReturnMessage'] == "Transacao autorizada":
                result = True
            else:
                result = False
            
            valor =str(valor)
            valor = f'R${valor[0]},{valor[1]}{valor[2]}'
            
            return result, f'{msg} - Code: {status} - {valor}'

        except:
            return False, 'Request inválido ao Gateway'

    else:
        return False, 'Parâmetros insuficientes'



