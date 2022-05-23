import requests, json, base64



api_key = 'A8087555425E35ACD585A01022F2B2B6FA725A7533FED3967CB19D89C69D4378'


def get_iugu_info(api_key):
    token = str(base64.b64encode(api_key.encode())).replace("b'", '').replace("'", '')

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Basic {token}',
    }

    try:
        response = requests.get('https://api.iugu.com/v1/customers', headers=headers).json()

        return response
    
    except:
        return {}

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

print(requests.post('https://api.iugu.com/v1/account?api_token=A8087555425E35ACD585A01022F2B2B6FA725A7533FED3967CB19D89C69D4378', headers=headers).text)