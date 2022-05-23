from OpenSSL import crypto
import json, os


with open('config/config.json', 'r') as file:
    config = json.loads(file.read())
    path = 'temp/cert_gn.p12'


def create_cert_gerencianet():
    try:
        if os.path.isfile('config/cert/cert-gn.pem') == False:
            if os.path.isfile(path):
                p12 = crypto.load_pkcs12(open(path, 'rb').read())

                a = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
                b = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())

                cert = f'{a}\n{b}'.replace(r'\n', '\n').replace("b'", '').replace("'", '')

                with open('config/cert/cert-gn.pem', 'w') as file:
                    file.write(cert)
                
                return True

            else:
                return False

        else:
            return False

    except:
        return False

