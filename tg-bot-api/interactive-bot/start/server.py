from flask import Flask, request

app = Flask(__name__)

@app.route("/hook", methods = ["POST"])
def hook():
    if request.is_json:
        print(request.get_json())
    return "Everything OKay", 200
    


app.run(port = 8000)