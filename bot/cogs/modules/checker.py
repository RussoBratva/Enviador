from bot.cogs.modules.checker_cielo import *
from bot.cogs.modules.checker_erede import *
from bot.cogs.modules.checker_pagarme import *
from bot.cogs.modules.checker_getnet import *
from bot.cogs.modules.external_checker import *
from bot.cogs.modules.checker_mp import *
import json, random
from time import sleep


def checker(cc):
    with open('config/config_checker.json', 'r') as file:
        load = json.loads(file.read())
        gate = load['default']
        curl = load['external']
    
    sleep(6)

    if not random.randint(0, 5) == 45:
        if gate == 'pagarme':
            check = pagarme(cc)
            #check = [False, 'Transação negada']
        
        elif gate == 'mercadopago':
            check = mp(cc)

        elif gate == 'cielo':
            check = cielo(cc)

        elif gate == 'erede':
            check = erede(cc)

        elif gate == 'getnet':
            check = getnet(cc)
            
        elif gate == 'external':
            check = curl_request(curl, cc)
        
        else:
            check = ['Erro', 'Nenhum gate selecionado']

        return check
        
    else:
        return [True, 'Transação autorizada - Code: 0000 - R$1,{}'.format(str(random.randint(10, 99)))]



