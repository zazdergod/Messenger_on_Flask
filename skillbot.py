from random import randint
import requests


# File with bot

class SkillBot:
    def __init__(self, url):
        self.name = "SkillBot"
        self.url = url
        self.jokes = [
            "Сольфеджио для программистов: интервьюер читает тебе вслух код, а ты должен сказать, что этот код делает.",
            "- Доктор, я себя чувствую, как C++.\n-Это как?\n-Меня никто не понимает, все боятся, и говорят, "
            "что я больше не нужен...",
            "Зачем к устройству с \"интуитивно-понятным интерфейсом\" инструкция на 100+ страниц?"
        ]
        self.greetings = [
            "Добрый день, ",
            "Рад тебя видеть, ",
            "И вот вы снова здесь, "
        ]
        self.answer = [
            "Можно и пропустить",
            "Верояность успеха крайне мала",
            "Омар Хаям сказал, что все по силам!",
            "ДА ДА И ЕЩЕ РАЗ ДА"
        ]

    # Method witch send bot message to server
    def send_message(self, message):
        try:
            response = requests.post(
                self.url + 'send_message',
                json={'text': message, 'author': self.name}
            )
        except:
            print(response.status_code)
            return

    # Method witch check user's message and create answer to it
    def validateMessage(self, message):
        response = requests.get(
            self.url + 'get_members'
        )

        number_of_members = response.json()['number_of_members']
        members = response.json()['members']
        text = message["text"]
        author = message["author"]
        text = list(text)
        if text[0] == "!":
            if ''.join(text[1:]) == "online":
                self.send_message('На сервере сейчас ' + str(number_of_members) + ' человек')
            elif ''.join(text[1:]) == "members":
                response = "Члены чата:\n"
                for member in members:
                    response += member + "\n"
                self.send_message(response)
            elif ''.join(text[1:]) == "joke":
                self.send_message(self.jokes[randint(0, len(self.jokes) - 1)])
            elif ''.join(text[1:]) == "roll":
                self.send_message("И на барабане выпадает: " + str(randint(0, 100)))
            elif ''.join(text[1:]) == "flip":
                coin = randint(0, 1)
                if coin == 1:
                    message = "Орел"
                else:
                    message = "Решка"
                self.send_message("Подбрасываю монетку и выпадает:\n\n\n" + message)
            elif ''.join(text[1:]) == "ask":
                self.send_message(self.answer[randint(0, len(self.answer) - 1)])
            elif ''.join(text[1:]) == "hello":
                self.send_message(self.greetings[randint(0, len(self.greetings) - 1)] + author)
            elif ''.join(text[1:]) == "help":
                self.send_message("Список команд:\n"
                                  "!hello - поздороваться с ботом\n"
                                  "!ask - спросить жизненно важный вопрос у бота\n"
                                  "!online - количество участников на сервере\n"
                                  "!roll - прокрутить барабан\n"
                                  "!flip - подбросить монету\n"
                                  "!joke - послушать шутку от бота")
