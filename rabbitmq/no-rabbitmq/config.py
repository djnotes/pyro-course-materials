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
            self.bot_admin = os.environ.get('bot_admin')
            self.proxy_on = os.environ.get('PROXY_ON')
            self.proxy_scheme = os.environ.get('PROXY_SCHEME')
            self.proxy_host = os.environ.get('PROXY_HOST')
            self.proxy_port = os.environ.get('PROXY_PORT')
            self.rabbitmq_user = os.environ.get('RABBITMQ_DEFAULT_USER')
            self.rabbitmq_password = os.environ.get('RABBITMQ_DEFAULT_PASS')
            self.rabbitmq_host = os.environ.get('RABBITMQ_DEFAULT_HOST')
            self.rabbitmq_vhost = os.environ.get('RABBITMQ_DEFAULT_VHOST')

        else:
            conf.read('env.ini')
            self.api_id = conf['bot']['api_id']
            self.api_hash = conf['bot']['api_hash']
            self.bot_token = conf['bot']['bot_token']
            self.bot_admin = conf['bot']['bot_admin']
            self.proxy_on = conf['proxy']['proxy_on']
            self.proxy_scheme = conf['proxy']['PROXY_SCHEME']
            self.proxy_host = conf['proxy']['PROXY_HOST']
            self.proxy_port = conf['proxy']['PROXY_PORT']
            self.rabbitmq_user = conf['rabbitmq']['RABBITMQ_DEFAULT_USER']
            self.rabbitmq_password = conf['rabbitmq']['RABBITMQ_DEFAULT_PASS']
            self.rabbitmq_host = conf['rabbitmq']['RABBITMQ_DEFAULT_HOST']
            self.rabbitmq_vhost = conf['rabbitmq']['RABBITMQ_DEFAULT_VHOST']
        
    def __repr__(self):
        return (f"api_id: {self.api_id}\n"
                f"api_hash: {self.api_hash}\n"
                f"bot_token: {self.bot_token[::4]}\n"
                f"bot_admin: {self.bot_admin} \n"
                f"proxy_on: {self.proxy_on}\n"
                f"proxy_scheme: {self.proxy_scheme}\n"
                f"proxy_host: {self.proxy_host}\n"
                f"proxy_port: {self.proxy_port}\n"
             f"rabbitmq_user: {self.rabbitmq_user}\n"
             f"rabbitmq_password: {self.rabbitmq_password}\n"
             f"rabbitmq_host: {self.rabbitmq_password}\n"
             f"rabbitmq_vhost: {self.rabbitmq_vhost}"
              )
    
    def __str__(self):
        return (
            f" Configuration Status:\n"
            f" API ID: {self.api_id}\n"
            f" Bot Token: '{self.bot_token[:4]}...'\n"
            f" Bot Admin: {self.bot_admin}\n"
            f" Proxy Host: {self.proxy_scheme}:{self.proxy_host}:{self.proxy_port} ({'ON' if self.proxy_on else 'OFF'})\n"
            f" RabbitMQ Host: {self.rabbitmq_host}\n"
            f" RabbitMQ VHost: {self.rabbitmq_vhost}\n"
            f" RabbitMQ User: {self.rabbitmq_user}\n"
            f" RabbitMQ Password: {self.rabbitmq_password}"
        )

            

            
    