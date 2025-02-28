import requests
import configparser
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import json

confParser = configparser.ConfigParser()
confParser.read('conf.ini')
BOT_TOKEN = confParser['bot']['token']
BOT_API = "https://api.telegram.org/bot" + BOT_TOKEN + "/"


# match text:
#     case '/text':
#         requests.post(BOT_API + "sendMessage", data = {"chat_id": uid, "text": "This is a text message"})
#     case '/audio':
#         requests.post(BOT_API + "sendAudio", data = {"chat_id": uid, "caption": "Audio Caption"}, files = {"audio": open("media/piano.mp3", "rb")})
#     case '/photo':
#         requests.post(BOT_API + "sendPhoto", data = {"chat_id": uid, "caption": "Photo Caption"}, files = {"photo": open("media/piano.jpg", "rb")})               
#     case '/video':
#         requests.post(BOT_API + "sendVideo", data = {"chat_id": uid, "caption": "Video Caption"}, files = {"video": open("media/piano.mp4", "rb")})               
#     case _:
#         requests.post(BOT_API + "sendMessage", data = {"chat_id": uid, "text": "Unrecognized command"})

update_id = -1

def tick():
    global update_id
    r = requests.post(BOT_API + "getUpdates", data = {"offset": update_id})
    json_r = r.json()
    print(json.dumps(json_r, indent = 2))
    updates = json_r['result']
    if len(updates):
        update = updates[-1]

        # for update in updates:
        uid = update['message']['from']['id']
        text = update['message']['text']
        msgid = update['message']['message_id']
        if update_id != update['update_id']:
            update_id = update['update_id']
        else:
            update_id += 1
            
        match text:
            case '/text':
                requests.post(BOT_API + "sendMessage", data = {"chat_id": uid, "text": "This is a text message"})
            case '/audio':
                requests.post(BOT_API + "sendAudio", data = {"chat_id": uid, "caption": "Audio Caption"}, files = {"audio": open("media/piano.mp3", "rb")})
            case '/photo':
                requests.post(BOT_API + "sendPhoto", data = {"chat_id": uid, "caption": "Photo Caption"}, files = {"photo": open("media/piano.jpg", "rb")})               
            case '/video':
                requests.post(BOT_API + "sendVideo", data = {"chat_id": uid, "caption": "Video Caption"}, files = {"video": open("media/piano.mp4", "rb")})               
            case _:
                requests.post(BOT_API + "sendMessage", data = {"chat_id": uid, "text": "Unrecognized command"})
    


async def main():
    s = AsyncIOScheduler()
    s.add_job(tick, "interval", seconds = 1)
    s.start()

    while True:
        await asyncio.sleep(1000)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass



