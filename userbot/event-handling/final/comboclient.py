from pyrogram import Client

class ComboClient(Client):
    def __init__(self, name: str, api_id: int, api_hash: str, bot_token: str, userbot: Client):
        super().__init__(name, api_id, api_hash, bot_token)
        self.userbot = userbot
