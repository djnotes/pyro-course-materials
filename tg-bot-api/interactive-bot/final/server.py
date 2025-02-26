from flask import Flask, request
import requests
import configparser

app = Flask(__name__)

confParser = configparser.ConfigParser()
confParser.read('conf.ini')
BOT_TOKEN = confParser['bot']['token']
BOT_API = "https://api.telegram.org/bot" + BOT_TOKEN + "/"


@app.route("/", methods = ["POST"])
def hook():
    if request.is_json:
        json = request.get_json()
        print(json)
        uid = json['message']['from']['id']
        msgid = json['message']['message_id']
        text = json['message']['text']
        
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
                
    return "Everything OKay", 200
    


app.run(port = 8000)