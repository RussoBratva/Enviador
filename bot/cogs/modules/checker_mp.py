from fordev import generators
from random import randint
import mercadopago, json, random, requests


with open('config/config_checker.json', 'r') as file:
    try:
        mercadopago_c = json.loads(file.read())['mercadopago']
        token = mercadopago_c['token']
    except:
        token = ''

sdk = mercadopago.SDK(token)

def refund(payment_id):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {}

    try:
        r = requests.post(f'https://api.mercadopago.com/v1/payments/{payment_id}/refunds', headers=headers, data=data).text
        return True
    except Exception as e:
        print(e)
        return False


def return_description(content):
    return_list = {
        "accredited": "O pagamento foi aprovado!",
        "ending_contingency": "Aprovado, porém, estamos processando o pagamento.",
        "pending_review_manual": "Aprovado, porém, estamos processando seu pagamento.",
        "cc_rejected_bad_filled_card_number": "Por favor, revise o número do cartão.",
        "cc_rejected_bad_filled_date": "O cartão está espirado.",
        "cc_rejected_bad_filled_other": "Por favor, revise os dados.",
        "cc_rejected_bad_filled_security_code": "Código de segurança do cartao inválido!.",
        "cc_rejected_blacklist": "Não pudemos processar o pagamento.",
        "cc_rejected_call_for_authorize": "Erro de autorização do cartão!",
        "cc_rejected_card_disabled": "Cartão não ativo, contate o emissor!",
        "cc_rejected_card_error": "Não foi possível processar o pagamento.",
        "cc_rejected_duplicated_payment": "Erro de pagamento duplicado!",
        "cc_rejected_high_risk": "Seu pagamento foi recusado.",
        "cc_rejected_insufficient_amount": "O cartão possui saldo insuficiente.",
        "cc_rejected_invalid_installments": "O cartão não aceita pagamento parcelado.",
        "cc_rejected_max_attempts": "Você atingiu o limite de tentativas permitido.",
        "cc_rejected_other_reason": "Não foi possível processar o pagamento."
    }

    try:
        return return_list[content.strip()]
    except:
        return 'A cc foi recusada ou ouve um erro de comunicação com o gateway!'



def people():
    with open("assets/pessoas.json", "r", encoding="utf8") as f:
        r = json.load(f)
        pessoas = r['pessoa']
        q = len(pessoas)
        pessoa = pessoas[randint(0, q-1)]
        cpf = pessoa['cpf']
        nome = pessoa['nome']
        
        return cpf, nome


def mp(cc):
    if len(cc.split("|")) == 4:
        numero, exp_mes, exp_ano, cvv = cc.split('|')
        if len(exp_ano) == 2:
            exp_ano = '20'+exp_ano

        endereco = generators.people(
            uf_code=generators.uf()[0],
            data_only=True)
        
        with open('assets/db_emails.json', 'r') as file2:
            load = json.loads(file2.read())
            emails = load['emails']
            email = random.choice(emails)
        
        gen_pay = float('1'+'.'+str(randint(0,99)))

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

        try:
            card_token_created = sdk.card_token().create(card_token_object)
            
            payment_object = {
                "token": card_token_created["response"]["id"],
                "installments":1,
                "transaction_amount": gen_pay,
                "description":"Check-in Demo",
                "payer":{
                    "email": email,
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
                        "title":"Check-in Demo",
                        "description": "Check-in Demo",
                        "picture_url":"",
                        "category_id": "",
                        "quantity":1,
                        "unit_price": gen_pay
                    }
                    ],
                    "shipments":{
                        "receiver_address":{
                            "street_name": endereco["endereco"],
                            "street_number": int(endereco["numero"]),
                            "zip_code": endereco["cep"].replace("-", ""),
                            "city_name": endereco["cidade"],
                            "state_name": endereco["estado"]
                        }
                    }
                }
            }

            payment_created = sdk.payment().create(payment_object)

            detalhes = payment_created['response']['status_detail']
            retorno = payment_created['response']['status']
            payment_id = payment_created['response']['id']

            if len(str(gen_pay)) == 3:
                gen_pay = str(gen_pay)+'0'

            description_status = return_description(detalhes)
            
            if retorno == 'approved':
                a = refund(payment_id)
                return True, description_status+f' - R${gen_pay}'

            elif retorno == 'in_process':
                return True, description_status+f' - R${gen_pay}'
                
            else:
                return False, description_status+f' - R${gen_pay}'

        except Exception as e:
            print(e)
            return False, 'Ocorreu algum erro no checker!'


    else:
        return False, 'Parâmetros insuficientes'


