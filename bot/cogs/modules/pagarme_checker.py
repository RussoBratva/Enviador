import requests
from random import randint
from bot.cogs.modules.functions import *


api_key = 'ek_live_JDAIMbzsoD0dajq0f6oJgzIP7YCmB1'


#rotas
base_url_domain = 'https://api.pagar.me/1'

route_card = base_url_domain+'/cards'
route_balance_operation = base_url_domain+'/balance/operations'
route_balance = base_url_domain+'/balance'
route_bank_accounts = base_url_domain+'/bank_accounts'
route_company = base_url_domain+'/company'
route_customers = base_url_domain+'/customers'
route_payables = base_url_domain+'/payables'
route_plans = base_url_domain+'/plans'
refunds = base_url_domain+'/refunds'
route_subscriptions = base_url_domain+'/subscriptions'
route_transactions = base_url_domain+'/transactions'
route_transfers = base_url_domain+'/transfers'


def checker(cc):
    try:
        numero_cc, exp_mes, exp_ano, cvv = cc.split("|")

        infos = generate_infos()
        data = {
        'encryption_key': api_key,
        "card_number": numero_cc,
        "card_cvv": cvv,
        "card_holder_name": infos[0],
        "card_expiration_date": str(exp_mes+exp_ano).replace('20', '').replace('/', '').replace('|', '').replace(' ', ''),
        "customer":{
            "email":f"{infos[1].replace(' ', '.').lower()}@gmail.com",
            "name":infos[0],
            "document_number":infos[1],
            "address":{
            "zipcode":infos[6],
            "neighborhood":infos[4],
            "street":infos[2],
            "street_number":infos[3]
            },
            "phone": {
            "number":infos[9],
            "ddd":infos[8]
            }
        } ,
        "capture": True,
        "async": False,
        "installments": 1,
        "payment_method":"credit_card",
        "amount": randint(100, 201),
                }
        pagarme_response = requests.post(route_transactions, json=data)
        
        return pagarme_response.json()

    except Exception as e:
        return 'Erro no checker!\n\n'+(str(e))
        

