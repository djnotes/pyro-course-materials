from pyrogram import Client


app = Client(
    name = "helloworld",
    api_id = 712345, # Replace with your own api_id
    api_hash = "9123453fb6014f0b74fbea1781412345" # Replace with your own api_hash
)

app.start()


try:
    app.send_message(chat_id = "@dev2000x", text = "Hello World from Pyrogram")
except Exception as e:
    print(f"An error occurred: {e}")
