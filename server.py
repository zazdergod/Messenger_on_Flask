import time
from datetime import datetime

from flask import Flask, Response, request

app = Flask(__name__)
db = [
    {'text': 'Привет', 'author': 'Jack', 'time': time.time()},
    {'text': 'Приве!', 'author': 'Mary', 'time': time.time()},
]


# Function witch get unique users
def get_members():
    members_set = {user["author"] for user in db}
    members_list = list()
    for member in members_set:
        members_list.append(member)
    return members_list


# Function witch get number of unique users
def get_number_of_members():
    return len(get_members())


# Function witch return status of server
@app.route("/status")
def status():
    numOfUsers = get_number_of_members()
    dn = datetime.now()
    return {
        'status': True,
        'name': 'SkillMessenger',
        'time': dn.strftime('%Y-%m-%d %H:%M:%S'),
        'Number of users': numOfUsers
    }


# Default server page
@app.route("/")
def hello():
    return "Hello, World!<br><a href='/status'>Статус</a>"


# Function witch return JSON with information about unique users on server
@app.route("/get_members")
def members():
    return {
        'members': get_members(),
        'number_of_members': get_number_of_members()
    }


# Function witch send message to server and append it to database on server
@app.route("/send_message", methods=['POST'])
def send_message():
    data = request.json
    if not isinstance(data, dict):
        return Response('not json', 400)

    text = data.get('text')
    author = data.get('author')

    if isinstance(text, str) and isinstance(author, str):
        db.append({
            'text': text,
            'author': author,
            'time': time.time()
        })
        return Response('ok')
    else:
        return Response('wrong format', 400)


# Function witch return all messages from server
@app.route("/get_messages")
def get_messages():
    after = request.args.get('after', '0')
    try:
        after = float(after)
    except:
        return Response('wrong format', 400)

    new_messages = [m for m in db if m['time'] > after]
    return {'messages': new_messages}


app.run()
