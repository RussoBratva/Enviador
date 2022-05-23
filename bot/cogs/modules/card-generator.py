from random import randint
import time
from datetime import datetime

def generate_card():
    card_types = ["americanexpress", "visa16","mastercard","discover"]
    type = card_types[randint(0, len(card_types)-1)]
    print(type)
    def prefill(t):
        def_length = 16

        if t == card_types[0]:
            return [3, randint(4,7)], 13
            
        elif t == card_types[1] or t == card_types[2]:
            return [4], def_length 

        elif t == card_types[3]:
            return [5, randint(1,5)], def_length
            
        elif t == card_types[4]:
            return [6, 0, 1, 1], def_length
            
        else:
            return [], def_length
        
    def expiration():
        mes = str(randint(1, 12))
        if len(mes) == 1:
            mes = '0'+mes
    
        t = datetime.utcfromtimestamp(float(time.time()))
        ano = str(t.year + randint(1, 8))
    
        return mes, ano
    
    
    def finalize(nums):
        check_sum = 0

        check_offset = (len(nums) + 1) % 2
        
        for i, n in enumerate(nums):
            if (i + check_offset) % 2 == 0:
                n_ = n*2
                check_sum += n_ -9 if n_ > 9 else n_
            else:
                check_sum += n
        return nums + [10 - (check_sum % 10) ]

    t = type.lower()
    if t not in card_types:
        return False
    
    initial, rem = prefill(t)
    so_far = initial + [randint(1,9) for x in range(rem - 1)]
    
    expiracao = expiration()
    
    cvv = str(randint(111, 999))
    
    if type == 'americanexpress':
        cvv = str(randint(1111, 9999))
    
    return "".join(map(str,finalize(so_far)))+'|'+expiracao[0]+'|'+expiracao[1]+'|'+cvv


print(generate_card())