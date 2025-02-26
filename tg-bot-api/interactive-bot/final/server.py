from flask import Flask, request
import requests

app = Flask(__name__)

TG_API = "https://api.telegram.org/bot1594116514:AAGMbcOiPgC1dll5qxL6_RWYUDnFU2wG7aw/"


@app.route("/", methods = ["POST"])
def hook():
    if request.is_json:
        json = request.get_json()
        print(json)
        uid = json['message']['from']['id']
        text = json['message']['text']
        msgid = json['message']['message_id']
        match text:
            case "/audio":
                r = requests.post(TG_API + "sendAudio" , data = {"chat_id":uid, "reply_to_message_id": msgid}, files = {"audio": open("media/piano.mp3", "rb")})
                print(r)
            case "/text":
                requests.post(TG_API + "sendMessage", data = {"chat_id": uid, "reply_to_message_id": msgid, "text": "This is a text message from the bot"})
            case "/photo":
                requests.post(TG_API + "sendPhoto", data = {"chat_id": uid, "caption": "Photo caption"}, files = {"photo": open("media/piano.jpg", "rb")})
            case "/video":
                requests.post(TG_API + "sendVideo", data = {"chat_id": uid, "caption": "Video caption"}, files = {"video": open("media/piano.mp4", "rb")})
            case _:
                requests.post(TG_API + "sendMessage", data = {"chat_id": uid, "text": "Command not recognized"})                
            
        
    return "Everything OKay", 200
    


app.run(port = 8000)