from .settings import *
from dotenv import load_dotenv
import os 

DEBUG = False
load_dotenv()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'reading_wrapped',
        'USER': 'postgres',
        'PASSWORD': os.getenv('DB_ENV'),
        'HOST' : 'localhost',
        'PORT': '5432'
    }
}
