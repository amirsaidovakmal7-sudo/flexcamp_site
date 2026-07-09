from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')
AMO_CLIENT_ID = os.getenv('AMO_CLIENT_ID')
AMO_CLIENT_SECRET = os.getenv('AMO_CLIENT_SECRET')