import requests, json
from base64 import b64encode


class GetNet():
    URL = "https://api.getnet.com.br"

    with open('config/config_checker.json', 'r', encoding='UTF-8') as file:
        getnet = json.loads(file.read())['getnet']

        CLIENT_ID = getnet['client_id']
        CLIENT_SECRET = getnet['client_secret']
        SELLER_ID = getnet['seller_id']

    AUTHORIZATION = None
    ACCESS_TOKEN = None
    NUMBER_TOKEN = None

    ERROR = ""


    def __init__(self):
        data = f"{self.CLIENT_ID}:{self.CLIENT_SECRET}"
        encodedBytes = b64encode(data.encode("utf-8"))
        self.AUTHORIZATION = str(encodedBytes, "utf-8")


    def get_error(self):
        return self.ERROR


    def authentication(self):
        with requests.Session() as s:
            authentication = s.post(
                url=self.URL + "/auth/oauth/v2/token",
                headers={
                    'Accept': 'application/json, text/plain, */*',
                    'Authorization': 'Basic ' + self.AUTHORIZATION,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data="scope=oob&grant_type=client_credentials"
            )

        if authentication.status_code == 200:
            self.ACCESS_TOKEN = authentication.json()['access_token']
            authentication.close()
            return True

        elif 'error' in authentication.json():
            self.ERROR = authentication.json()['error']

        return False


    def tokenization(self, card_number):
        if not self.authentication():
            return False

        with requests.Session() as s:
            tokenization = s.post(
                url=self.URL + "/v1/tokens/card",
                headers={
                    'content-type': 'application/json; charset=utf-8 ',
                    'Accept': 'application/json, text/plain, */*',
                    'Authorization': f'Bearer ' + self.ACCESS_TOKEN
                },
                json={
                    'card_number': card_number,
                    "customer_id": "customer_3242"
                }
            )
            
            tokenization.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'})

        if tokenization.status_code == 201:
            self.NUMBER_TOKEN = tokenization.json()['number_token']
            tokenization.close()

            return True

        return False


    def verification(self, card_number, card_month, card_year, card_cvv):
        if not self.tokenization(card_number):
            return False

        if len(card_year) == 4:
            card_year = card_year[2:]

        with requests.Session() as s:
            verification = s.post(
                url=self.URL + "/v1/cards/verification",
                headers={
                    'content-type': 'application/json; charset=utf-8 ',
                    'Authorization': 'Bearer ' + self.ACCESS_TOKEN,
                    'seller_id': self.SELLER_ID
                },
                json={
                    "number_token": self.NUMBER_TOKEN,
                    "cardholder_name": "JOAO DA SILVA",
                    "expiration_month": card_month,
                    "expiration_year": card_year,
                    "security_code": card_cvv
                }
            )
            
            verification.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'})

        result = verification.json()

        if verification.status_code == 200:
            return result

        try:
            details = result['details'][0]
        except Exception as e:
            self.ERROR = str(e)
            return False

        return details


def checker(creditCard):
    try:
        card_number, card_month, card_year, card_cvv = creditCard.split("|")
    except Exception as e:
        return print(f"Erro | {creditCard} | Retorno: Cartão inválido")

    get_net = GetNet()
    result = get_net.verification(card_number, card_month, card_year.replace('20', ''), card_cvv)

    if not result or not 'status' in result:
        return False, get_net.get_error()
    
    elif result['status'] == "VERIFIED":
        return True, result['status']
    
    else:
        return False, result['status']

