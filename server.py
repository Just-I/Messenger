from flask import Flask, abort, request
import time

app = Flask(__name__)

database = []

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/send", methods=['POST'])
def send_message():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)

    name = data['name']
    text = data['text']

    if not isinstance(name, str) or not isinstance(text, str):
        return abort(400)
    if name == '' or text == '':
        return abort(400)
    
    message = {
        'time': time.time(),
        'text': text,
        'name': name
    }
    database.append(message)
    return {'ok': True}

@app.route("/get")
def get_message():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    if not isinstance(after, float) and not isinstance(after, int):
        return abort(400)
    
    add = []
    for message in database:
        if message['time'] > after:
            add.append(message)
            if len(add) >= 50:
                break
    return {'messages': add}

app.run()
