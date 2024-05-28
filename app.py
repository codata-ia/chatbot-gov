from flask import Flask, request, jsonify
from flask_cors import CORS

from chat import processMessage

from fileReader import getSystemMessage

app = Flask(__name__)
CORS(app)
messages_history = []

class MessageProcessor:
    def __init__(self):
        self.messages_history = [getSystemMessage()]

processor = MessageProcessor()

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response, processor.messages_history = processMessage(text, processor.messages_history)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
