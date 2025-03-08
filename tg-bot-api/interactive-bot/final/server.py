from flask import Flask, request
import requests
import json
import configparser

parser = configparser.ConfigParser()

parser.read('conf.ini')

BOT_TOKEN = parser['bot']['BOT_TOKEN']

BOT_API = 'https://api.telegram.org/bot' + BOT_TOKEN + "/"


app = Flask(__name__)

@app.route("/", methods = ["POST"])
def hook():
    if request.is_json:
        json_r = request.get_json()
        print(json.dumps(json_r))
        uid = json_r['message']['from']['id']
        msgid = json_r['message']['message_id']
        text = json_r['message']['text']
        
        match text:
            case '/text':
                requests.post(BOT_API + "sendMessage", data = {"chat_id": uid, "text": "This is a test message"})
            case '/audio':
                requests.post(BOT_API + "sendAudio", data = {"chat_id": uid, "caption": "Audio Caption"}, files = {"audio": open("media/piano.mp3", "rb")})                
            case '/photo':
                requests.post(BOT_API + "sendPhoto", data = {"chat_id": uid, "caption": "Photo Caption"}, files = {"photo": open("media/piano.jpg", "rb")})                
            case '/animation':
                requests.post(BOT_API + "sendAnimation", data = {"chat_id": uid}, files = {"animation": open("media/blink.tgs", "rb")})                
            case '/video':
                requests.post(BOT_API + "sendVideo", data = {"chat_id": uid, "caption": "Video Caption"}, files = {"video": open("media/piano.mp4", "rb")})                
            case _:
                pass   
        
    return "Everything OKay", 200
    


app.run(port = 8000)