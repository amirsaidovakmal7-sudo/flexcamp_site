from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SUBDOMAIN = os.getenv('SUBDOMAIN')
REDIRECT_URI = os.getenv('REDIRECT_URI')
AMO_ACCESS_TOKEN = os.getenv('AMO_ACCESS_TOKEN')
AMO_REFRESH_TOKEN = os.getenv('AMO_REFRESH_TOKEN')
