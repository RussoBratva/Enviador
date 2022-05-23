import json, os
from bot.cogs.modules.mp_pix import pix as mercadopago
from bot.cogs.modules.gn_pix import pix as gerencianet


path = 'config/config_pix.json'


def template(mp_token, gn_pix, gn_client_id, gn_client_secret, pix_key, pix_type, pix_default):
    body = {
        "mp": {
            "token": mp_token
        },
        "gn": {
            "pix": gn_pix,
            "client_id": gn_client_id,
            "client_secret": gn_client_secret
        },
        "pix_key": pix_key,
        "pix_type": pix_type,
        "pix_default": pix_default
    }
    
    return body


def verify_file_exists():
    a = os.path.isfile(path)
    if a is False:
        with open(path, 'w') as file:
            t = template('', '', '', '', '', '', '')
            j = json.dumps(t, indent=4)
            file.write(j)


def mp_authentication():
    mp = mercadopago('Teste', '1')

    if mp[0] == 'Erro':
        register_mp_pix('', True)
        return False

    else:
        return True


def gn_authentication():
    gn = gerencianet('Teste', '1')

    if gn[0] == 'Erro':
        register_gn_pix('', '', '', True)
        return False

    else:
        return True


def register_default_pix(default):
    verify_file_exists()
    with open(path, 'r') as file:
        f = json.loads(file.read())
        pix_key = f['pix_key']
        pix_type = f['pix_type']
        
        mp_token = f['mp']['token']
        
        gn_pix = f['gn']['pix']
        gn_client_id = f['gn']['client_id']
        gn_client_secret = f['gn']['client_secret']
        
        pix_default = default
        
    t = template(mp_token, gn_pix, gn_client_id, gn_client_secret, pix_key, pix_type, pix_default)
    j = json.dumps(t, indent=4)

    with open(path, 'w') as file:
        file.write(j)


def verify_gn():
    verify_file_exists()
    with open(path, 'r') as file:
        f = json.loads(file.read())
        gn_pix = f['gn']['pix']
        gn_client_id = f['gn']['client_id']
        gn_client_secret = f['gn']['client_secret']

        if gn_pix == '' and gn_client_id == '' and gn_client_secret == '':
            return True

        else:
            return False


def verify_mp():
    verify_file_exists()
    with open(path, 'r') as file:
        f = json.loads(file.read())
        mp_token = f['mp']['token']
        
        if mp_token == '':
            return True
        
        else:
            return False


def verify_key():
    verify_file_exists()
    with open(path, 'r') as file:
        f = json.loads(file.read())
        pix_key = f['pix_key']
        pix_type = f['pix_type']
        
        if pix_key == '' and pix_type == '':
            return True

        else:
            return False


def verify_default():
    verify_file_exists()
    with open(path, 'r') as file:
        f = json.loads(file.read())
        pix_default = f['pix_default']
        
        return pix_default


def reset_default(pix_deletado):
    atual = verify_default()

    if pix_deletado == atual:
        mp = verify_mp()
        gn = verify_gn()
        key = verify_key()
        
        if atual == 'mp':
            if key == False:
                register_default_pix('key')
            
            elif gn == False:
                register_default_pix('gn')
            
            else:
                register_default_pix('')

        elif atual == 'gn':
            if mp == False:
                register_default_pix('mp')
            
            elif key == False:
                register_default_pix('key')
            
            else:
                register_default_pix('')
        
        elif atual == 'key':
            if mp == False:
                register_default_pix('mp')
            
            elif gn == False:
                register_default_pix('gn')
            
            else:
                register_default_pix('')

        else:
            register_default_pix('')


def register_mp_pix(token, apagar=False):
    verify_file_exists()
    
    if apagar:
        reset_default('mp')
        
    with open(path, 'r') as file:
        f = json.loads(file.read())
        pix_key = f['pix_key']
        pix_type = f['pix_type']
        
        mp_token = f['mp']['token']
        
        if not token == '' or apagar == True:
            mp_token = token
        
        gn_pix = f['gn']['pix']
        gn_client_id = f['gn']['client_id']
        gn_client_secret = f['gn']['client_secret']
        
        pix_default = "mp"
        
    t = template(mp_token, gn_pix, gn_client_id, gn_client_secret, pix_key, pix_type, pix_default)
    j = json.dumps(t, indent=4)

    with open(path, 'w') as file:
        file.write(j)


def register_gn_pix(pix, client_id, client_secret, apagar=False):
    verify_file_exists()
    
    if apagar:
        reset_default('gn')
    
    with open(path, 'r') as file:
        f = json.loads(file.read())
        pix_key = f['pix_key']
        pix_type = f['pix_type']
        
        mp_token = f['mp']['token']
        
        gn_pix = f['gn']['pix']
        gn_client_id = f['gn']['client_id']
        gn_client_secret = f['gn']['client_secret']
        
        if not pix == '' or apagar == True:
            gn_pix = pix
        
        if not client_id == '' or apagar == True:
            gn_client_id = client_id
        
        if not client_secret == '' or apagar == True:
            gn_client_secret = client_secret
        
        pix_default = "gn"
        
    t = template(mp_token, gn_pix, gn_client_id, gn_client_secret, pix_key, pix_type, pix_default)
    j = json.dumps(t, indent=4)

    with open(path, 'w') as file:
        file.write(j)


def register_pix_key(pix, pix_type1, apagar=False):
    verify_file_exists()
    
    if apagar:
        reset_default('key')
    
    with open(path, 'r') as file:
        f = json.loads(file.read())
        pix_key = f['pix_key']
        pix_type = f['pix_type']
        
        if not pix == '' or apagar == True:
            pix_key = pix
        
        if not pix == '' or apagar == True:
            pix_type = pix_type1
        
        mp_token = f['mp']['token']
        
        gn_pix = f['gn']['pix']
        gn_client_id = f['gn']['client_id']
        gn_client_secret = f['gn']['client_secret']
        pix_default = f['pix_default']
    
    if pix_default == "":
        pix_default = "key"
        
    t = template(mp_token, gn_pix, gn_client_id, gn_client_secret, pix_key, pix_type, pix_default)
    j = json.dumps(t, indent=4)

    with open(path, 'w') as file:
        file.write(j)

