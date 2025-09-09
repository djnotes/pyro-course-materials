import os
import configparser

conf = configparser.ConfigParser()

class AppConfig:
    def __init__(self):
        container = True if os.environ.get('api_id') else False
        if container:
            self.api_id = os.environ.get('api_id')
            self.api_hash = os.environ.get('api_hash')
            self.bot_token = os.environ.get('bot_token')
            self.proxy_on = os.environ.get('PROXY_ON')
            self.proxy_scheme = os.environ.get('PROXY_SCHEME')
            self.proxy_host = os.environ.get('PROXY_HOST')
            self.proxy_port = os.environ.get('PROXY_PORT')
            self.rabbitmq_user = os.environ.get('RABBITMQ_DEFAULT_USER')
            self.rabbitmq_password = os.environ.get('RABBITMQ_DEFAULT_PASSWORD')
            self.rabbitmq_host = os.environ.get('RABBITMQ_DEFAULT_HOST')
            self.rabbitmq_vhost = os.environ.get('RABBITMQ_DEFAULT_VHOST')
        else:
            conf.read('env.ini')
            self.api_id = conf['bot']['api_id']
            self.api_hash = conf['bot']['api_hash']
            self.bot_token = conf['bot']['bot_token']
            self.proxy_on = conf['proxy']['proxy_on']
            self.proxy_scheme = conf['proxy']['PROXY_SCHEME']
            self.proxy_host = conf['proxy']['PROXY_HOST']
            self.proxy_port = conf['proxy']['PROXY_PORT']
            self.rabbitmq_user = conf['rabbitmq']['RABBITMQ_DEFAULT_USER']
            self.rabbitmq_password = conf['rabbitmq']['RABBITMQ_DEFAULT_PASSWORD']
            self.rabbitmq_host = conf['rabbitmq']['RABBITMQ_DEFAULT_HOST']
            self.rabbitmq_vhost = conf['rabbitmq']['RABBITMQ_DEFAULT_VHOST']

            
    