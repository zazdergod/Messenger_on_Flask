import requests

name = input("Your name:")
message = input("Your message:")


def send_message(author, text):
    response = requests.post(
        'http://127.0.0.1:5000/send_message',
        json={'text': text, 'author': author}
    )
    print(response.status_code)
    print(response.text)


send_message(name, message)
