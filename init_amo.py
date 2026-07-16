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



secret_code = 'def502005d440854ad9310cb4fe7a56edf7a1a9f3086f5730df2b464b41f88460006c5a7209345bbc53ba663898c11d0b81ba3f2cf2f601e2a97728bb7b185f4756eb1149db35a369b06304dbbf8c2861ad1770ee69a2ea114af65b378642d8ec9bf063758005e1a53f61f3d7e66c5ab661d71672210ff721db1944490a70693a5c26d2357f5bd3fabcd295d564598a9f3092ec11bfb8ac88f3a76e6203157ff9164fe06d484c3e82681aa52c33f5dffb33555e6dd64fe7b99a52da68230a471b722d8b730c428cc81c44910761aade5d0d8ec89928a08d319d00447d5f035a65fec938ea37196ed907bc7ed540059e745ab7a8126a3d49dd385d95b859af18f339a14cbad9685c990991de4a344f95893d5f3438078cba6e9d02ca25584b7e7f321d8436afa9bc7d0e39c729af66ba499bfeda6645ab443e8e20dc8b68dcd5021136be3561a66e3d68f1454cad435fa17e5baf0a538c325e871d49252a99930f92edb7fd4d786b585f19a60679e6b5a00ed37d63fe7715f875507e95256930d6d2a55bf3149e268be193fcabed351b41056988e9c74c9393bed7dd0eacdc2c5f1f41ab459b93d4709dc29547a287594b3a336928869628db3a8acd264fbd12856dbd076130fc4ed5d5c703396162259d717950674669b29951a542c1e62ca4a881b684d61feb9cbb70edeed74b0'



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


amo_wrapper = AmoCRMWrapper()
amo_wrapper.init_oauth2()



