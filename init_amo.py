from config import *
import requests
import os
from datetime import datetime
import time
from requests.exceptions import JSONDecodeError
import jwt
import dotenv
from dotenv import load_dotenv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app.models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_path = os.path.join(BASE_DIR, ".env")


CHOOSED_SESSIONFIELD_ID = 1897827
RESPONSIBLE_USER_ID = 33083426
PIPLINE_ID = 10970430
STATUS_ID = 86247706



secret_code = 'def5020019505a1ee4505e8c0369f3e3f4de6f11c08d110a5bb746bf0fa5187b290df4346695e84102c756890ac90b2210350d0b5d3045c34ecdc3c145d35638d79919c157627209d8cc168e090abb38bdd7b35086afbe079341eb9f548b92e80e153421e6934df3e78b4fe188ec8b65b45e09a885eab5b9b3ea1a19e1481487ab8ddf04c4821886663d8d19c0f89d520124df3e4c03c6ef67e21e96fcf0e2481adfcdb3e3583bfe3ed24daa071830b0296928abf95d415de23813795a49e71bda8833377a242424285fe0499e5c49fe15717ad0cd1ccd572fdb2c6f7ad7ccef1550343cf6a640a8f77a706b6407ce03bcadd958dcabbc293e301e1c8a38087613db426cf1b8653451581e9ce3256f1b6b05e07ffa1417afaca599874b9ae2bb8869cec5989c5177191cbbaca5377985d6991406728168a97fff4bf43a3225ca98c593223e0dcafbdcc8620aceea879cdaf2d6ea3b479e82b08d2b89c61f680788467fa82a3e8aa5c19efaf1bf99a24e2c06452abb91324aedd9e6d418a2e612f17ec49ca5ec79cf28de3e4ec4f5a886de1e991e868a63c8ba15cadf2efd4c23356012b3e5cc020e5491f42de8c39d2ec36e4505cd0b33651f0c4eb5e2a998b2f4a73da89cf7429aaaa9cbe8bdffda6bd25326e480e24729a567b726506761705545955b36a0a0758f21165ab9ed'



def _is_expire(token):
    if isinstance(token, str):
        token = token.encode('utf-8')
    token_data = jwt.decode(token, options={"verify_signature": False})
    exp = datetime.utcfromtimestamp(token_data['exp'])
    now = datetime.utcnow()

    return now >= exp


def save_tokens(access_token, refresh_token):
    try:
        Access_token.objects.update_or_create(id=1, defaults={'access_token': access_token})
        Refresh_token.objects.update_or_create(id=1, defaults={'refresh_token': refresh_token})
        return True
    except Exception as e:
        return e





def get_access_token():
    return Access_token.objects.get(id=1).access_token


def get_refresh_token():
    return Refresh_token.objects.get(id=1).refresh_token


def get_new_tokens():
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': get_refresh_token(),
        'redirect_uri': REDIRECT_URI,

    }
    response = requests.post('https://{}.amocrm.ru/oauth2/access_token'.format(SUBDOMAIN),
                             json=data).json()
    print(response)
    access_token = response['access_token']
    refresh_token = response['refresh_token']

    save_tokens(access_token, refresh_token)


class AmoCRMWrapper:
    def init_oauth2(self):
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': "authorization_code",
            'code': secret_code,
            'redirect_uri': REDIRECT_URI
        }
        response = requests.post('https://{}.amocrm.ru/oauth2/access_token'.format(SUBDOMAIN),
                                 json=data).json()

        print(response)
        access_token = response['access_token']
        refresh_token = response['refresh_token']

        result = save_tokens(access_token, refresh_token)

        print(f'РЕЗУЛЬТАТ: {result}, {type(result)}')




    def base_request(self, **kwargs):
        if _is_expire(get_access_token()):
            get_new_tokens()
        access_token = f"Bearer {get_access_token()}"

        headers = {
            "Authorization": access_token
        }
        req_type = kwargs.get('type')
        response = ""
        if req_type == "get":
            try:
                response = requests.get("https://{}.amocrm.ru{}".format(
                    SUBDOMAIN, kwargs.get("endpoint")), headers=headers).json()
            except JSONDecodeError as e:
                return e

        elif req_type == "get_param":
            url = "https://{}.amocrm.ru{}?{}".format(
                SUBDOMAIN,
                kwargs.get("endpoint"), kwargs.get("parameters"))
            response = requests.get(str(url), headers=headers).json()
        elif req_type == "post":
            response = requests.post("https://{}.amocrm.ru{}".format(
                SUBDOMAIN,
                kwargs.get("endpoint")), headers=headers, json=kwargs.get("data")).json()
        return response



def add_complex_lead(name, phone_number, session):
    data = [
        {
            "source_name": "Сайт Flex Camp",
            "source_uid": "Форма запипси flex camp",
            "metadata": {
                "ip": "82.115.50.124",
                "form_id": "new lead",
                "form_sent_at": int(time.time()),
                "form_name": "Форма записи в лагерь",
                "form_page": "https://flexcamp.uz",
                "referer": "https://flexcamp.uz"
            },
            "_embedded": {
                "leads": [{

                    "name": 'Новая сделка с сайта',
                }

                          ],
                "contacts": [
                    {
                        "name": name,
                        "updated_by": 0,
                        "custom_fields_values": [
                            {
                                "field_id": CHOOSED_SESSIONFIELD_ID,
                                "values": [
                                    {
                                        "value": session
                                    }
                                ]
                            },
                            {
                                "field_code": "PHONE",
                                "values": [
                                    {
                                        "enum_code": "WORK",
                                        "value": phone_number
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    ]
    amocrm_wrapper = AmoCRMWrapper()
    response = amocrm_wrapper.base_request(endpoint='/api/v4/leads/unsorted/forms', type='post', data=data)

    lead_id = response['_embedded']['unsorted'][0]['_embedded']['leads'][0]['id']
    return lead_id





