import os
import dotenv

from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')
valid_number = os.getenv('valid_number')