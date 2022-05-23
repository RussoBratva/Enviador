from gerencianet import Gerencianet
from bot.cogs.modules.create_cert import create_cert_gerencianet
from random import sample
import string, json
from time import sleep


create_cert_gerencianet()


def pix(descricao, valor):
    try:
        with open('config/config.json', 'r') as file:
            config = json.loads(file.read())
            expiration_payment = config['expiration_payment_in_minutes']


        with open('config/config_pix.json', 'r') as file:
            config = json.loads(file.read())
            chave_pix = config['gn']['pix']
            client_id = config['gn']['client_id']
            client_secret = config['gn']['client_secret']

        CREDENTIALS = {
            "client_id": client_id,
            "client_secret": client_secret,
            "sandbox": False,
            "pix_cert": "config/cert/cert-gn.pem"
        }

        c_list = string.ascii_uppercase + string.digits + string.ascii_lowercase
        tid = "".join(sample(c_list, 26))
        
        valor = str(valor)+'.00'
        gn = Gerencianet(CREDENTIALS)

        params = {"txid": f"{tid}"}

        body = {
            "calendario": {
                "expiracao": int(expiration_payment)*60
            },
            "valor": {
                "original": valor
            },
            "chave": chave_pix,
            "solicitacaoPagador": descricao
        }

        response =  gn.pix_create_charge(params=params,body=body)
        loc = response['loc']['id']
        params = {'id': loc}

        response =  gn.pix_generate_QRCode(params=params)
        return tid, response['qrcode']

    except Exception as e:
        print(e)
        return 'Erro', ''


def status(id_a):
    try:
        with open('config/config.json', 'r') as file:
            config = json.loads(file.read())
            expiration_payment = config['expiration_payment_in_minutes']


        with open('config/config_pix.json', 'r') as file:
            config = json.loads(file.read())
            client_id = config['gn']['client_id']
            client_secret = config['gn']['client_secret']

        CREDENTIALS = {
            "client_id": client_id,
            "client_secret": client_secret,
            "sandbox": False,
            "pix_cert": "config/cert/cert-gn.pem"
        }

        
        gn = Gerencianet(CREDENTIALS)
        response =  gn.pix_detail_charge(params={'txid': id_a})
        status = response['status'].lower()
        
        if status == 'ativa':
            return False
            
        elif status == 'concluida':
            return True
    
        else:
            return False

    except:
        return 'Erro'


