from .settings import *

DATABASES = {
    'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': str(os.getenv('NAME', 'test_' + os.getenv('NAME'))),
                'USER': str(os.getenv('USERTESTE')),
                'PASSWORD': str(os.getenv('PASSWORD')),
                'HOST': str(os.getenv('HOSTTESTE')),
                'PORT': '5432'
            }
        }

DEBUG = True