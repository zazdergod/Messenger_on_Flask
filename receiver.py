import time
import requests
from datetime import datetime
from skillbot import SkillBot

after = 0

bot = SkillBot('http://127.0.0.1:5000/')

while True:
    response = requests.get(
        'http://127.0.0.1:5000/get_messages',
        params={'after': after}
    )
    if response.status_code == 200:
        messages = response.json()['messages']

        for message in messages:
            after = message['time']
            ftime = datetime.fromtimestamp(message['time']).strftime('%Y/%m/%d %H:%M:%S')
            print(ftime, message['author'])
            print(message['text'])
            print()
            bot.validateMessage(message)

    time.sleep(1)
