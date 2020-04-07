import os
from dotenv import load_dotenv


load_dotenv('.env')

# DATABASE
DB_URI      = os.getenv('DB_URI')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# AUTH
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')