from validate_docbr import CPF, CNPJ
import re


def telefone(pix):
    pattern = re.compile(r'([1-9]{2})(9[1-9])([0-9]{3})([0-9]{4})')
    numero = pix.strip().replace(' ', '')
    
    if not re.match(pattern, numero):
        v = False
        
    else:
        v = True

    return v


def cpf(pix):
    pix = pix.strip().replace('.', '').replace('-', '')
    cpf_check = CPF()
    r = cpf_check.validate(pix)
    
    return r


def cnpj(pix):
    pix = pix.strip().replace('.', '').replace('-', '').replace('/', '')
    cnpj_check = CNPJ()
    r = cnpj_check.validate(pix)

    return r


def chave_aleatoria(pix):
    a = pix.strip()
    if a.count('-') == 4:
        if len(a) == 36:
            ac1 = len(a[:a.find('-')])
            bc1 = a[a.find('-')+1:]

            ac2 = len(bc1[:bc1.find('-')])
            bc2 = bc1[bc1.find('-')+1:]

            ac3 = len(bc2[:bc2.find('-')])
            bc3 = bc2[bc2.find('-')+1:]

            ac4 = len(bc3[:bc3.find('-')])
            bc4 = bc3[bc3.find('-')+1:]

            ac5 = len(bc4)

            if ac1 == 8 and ac2 == 4 and ac3 == 4 and ac4 == 4 and ac5 == 12:
                v = True

            else:
                v = False

        else:
            v = False

    else:
        v = False

    return v


def email(pix):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    email = pix.strip().replace(' ', '')
    
    if not re.match(pattern, email):
        v = False
        
    else:
        v = True

    return v


