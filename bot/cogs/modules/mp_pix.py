import mercadopago, pytz, datetime, json, requests, time


def expiration():
    with open('config/config.json', 'r') as file:
        config = json.loads(file.read())
        expiration_payment = config['expiration_payment_in_minutes']
    
    time_change = datetime.timedelta(minutes=int(expiration_payment))
    new_time = datetime.datetime.now() + time_change

    tz = pytz.timezone("America/Bahia")
    aware_dt = tz.localize(new_time)

    a = aware_dt.isoformat()
    
    return a[:23]+a[26:]


def pix(descricao, valor):
    try:
        with open('config/config_pix.json', 'r') as file:
            config = json.loads(file.read())
            token = config['mp']['token']
        
        sdk = mercadopago.SDK(token)

        payment_data = {
            "transaction_amount": float(str(valor)+'.00'),
            "description": descricao,
            "payment_method_id": "pix",
            "date_of_expiration": expiration(),
            "payer": {
                "email": 'anakinpix@gmail.com',
                "first_name": '',
                "last_name": '',
                "identification": {
                    "type": "CPF",
                    "number": ''
                },
                "address": {
                    "zip_code": '',
                    "street_name": '',
                    "street_number": '',
                    "neighborhood": '',
                    "city": '',
                    "federal_unit": ''
                }
            }
        }

        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]

        id_p = str(payment['id'])
        pix = payment['point_of_interaction']['transaction_data']['qr_code']

        return id_p, pix

    except:
        return 'Erro', ''


def status(id_a):
    try:
        with open('config/config.json', 'r') as file:
            config = json.loads(file.read())
            expiration_payment = config['expiration_payment_in_minutes']

        with open('config/config_pix.json', 'r') as file:
            config = json.loads(file.read())
            token = config['mp']['token']
            
        headers = {"Authorization": f"Bearer {token}"}
        contador = 0

        contador += 1
        
        request = requests.get(f'https://api.mercadopago.com/v1/payments/{id_a}', headers=headers).json()
        
        status = str(request['status']).strip()
        print(status)

        if not contador > int(expiration_payment):
            if status == 'pending':
                return False
                
            elif status == 'approved':
                return True
            
            else:
                return False
            
        else:
            return False

    except:
        return 'Erro'

