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



secret_code = 'def50200dcb6863bcf9b1fadd7542067fcbed5e061e41d1755a2e47589eb49af004d17f214596d1775f995f8f7ef05d1400cd3a52568cce0c13dee4a429595f2eadf3aacc6021277b860ac27b765623c5c84b157c60a53d0a708da55a199d346a2f1b440f16ad88036c2dc53f4a1cdc924f43efb696aa022ac5a6f01a3187869c84a5e65fc1005ef7adbf067a66c268d7a0f68e484810f925796af40d11b24406cd58a0d3f96d85da3f70ab0d0b9b2dc2b1e8f83bc9826462507491b9008ee2d795cf02b223845c843ead42a33cdb83f91af6e994189d2e6cfff8ce35525081048a2decf472c17072ccc7d6ed33f4228fd73602723781ececed47d34ece602be4e857e083ec5a7b371b409afce1498e1dea90f4b6b1b30fb6a35baae5095bd69418e9ae5f0acc831e42ddc89f6fb38966ed4cf99a8252df73de382dbf63f122fcc44242ab79630da38bc8b74db8ec86f025ccd2e6591511492c5dd0ddf367b227e61b6c4478cc7e8f35b4aaecb7926bf0cb8c8f982d5cd6e523459a0574eb2b65c2df8f4c76de9ef61cb50a207deb57142d70b67ea8b2c577f569200cc0989e9ee2e20e02380b64ee8a48d35b8b0bfb4ad1cf4dc5dbc3211658c89636ff50343c98c80bd35374f6dec8b4e771b9a36eb27df68372109775c0751490504be6eb112f1f8b0f938f0370a34a735873d'



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



