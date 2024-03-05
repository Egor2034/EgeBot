import telebot
from telebot import types
import os
import random

token='6595906182:AAE4s5uKoA7aXdOkQdyJNhox6InguFtgBd8'

bot=telebot.TeleBot(token)

solution = ""
rand = 0
task = ""
answer = ""
file = ""
numb = ""

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello")


@bot.message_handler(commands=["3", "9", "10", "17", "18", "22", "24", "25", "26", "27"])
def file_tasks(message):
    global task, rand, answer, solution, file, numb

    rand = random.randint(1, 6)
    numb = message.text[1:]

    if message.text in ("/3", "/22", "/18"):
        file = open(f"Задания для бота Телеграм/{message.text}/Задания/{rand}/{rand}.xlsx", "rb")
    elif message.text == "/10":
        file = open(f"Задания для бота Телеграм/{message.text}/Задания/{rand}/{rand}.docx", "rb")
    else:
        file = open(f"Задания для бота Телеграм/{message.text}/Задания/{rand}/{rand}.txt", "rb")

    try:
        solution = sorted(os.listdir(f"Задания для бота Телеграм/{message.text}/Задания/{rand}/Решение/"))
    except:
        solution = sorted(os.listdir(f"Задания для бота Телеграм/{message.text}/Задания/{rand}/"))

    task = open(f"Задания для бота Телеграм/{message.text}/Задания/{rand}/{rand}.txt", "r", encoding='utf-8').read()
    answer = open(f"Задания для бота Телеграм/{message.text}/Задания/{rand}/Ответ.txt", 'r', encoding='utf-8').read()

    bot.send_message(message.chat.id, task)
    bot.send_document(message.chat.id, file)
    bot.register_next_step_handler(message, process_text)


@bot.message_handler(commands=[str(i) for i in range(1, 28)])
def simple_tasks(message):
    global task, rand, answer, solution, numb

    rand = random.randint(1, 6)
    numb = message.text[1:]

    solution = open(f"Задания для бота Телеграм/{message.text}/Задания/{rand}/Решение.txt", "r", encoding='utf-8').read()
    photo = open(f"Задания для бота Телеграм/{message.text}/Задания/{rand}/{rand}.png", "rb")
    task = open(f"Задания для бота Телеграм/{message.text}/Задания/{rand}/{rand}.txt", "r", encoding='utf-8').read()
    answer = open(f"Задания для бота Телеграм/{message.text}/Задания/{rand}/Ответ.txt", 'r', encoding='utf-8').read()

    bot.send_photo(message.chat.id, photo, task)
    bot.register_next_step_handler(message, process_text)


@bot.message_handler(commands=[f"Задание{str(i)}" for i in range(1, 28)])
def info_sol(message):
    t = ""

    for i in message.text:
        if i.isdigit():
            t += i

    solution = open(f"Задания для бота Телеграм/{t}/Как делать.txt", "r",
             encoding='utf-8').readlines()
    info = open(f"Задания для бота Телеграм/{t}/О задании.txt", "r",
             encoding='utf-8').read()

    bot.send_message(message.chat.id, info)

    bot.send_message(message.chat.id, solution[0].replace("\n", ""))
    bot.send_message(message.chat.id, solution[1].replace("\n", ""))

    bot.send_message(message.chat.id, solution[2].replace("\n", ""))
    bot.send_message(message.chat.id, solution[3].replace("\n", ""))

    bot.send_message(message.chat.id, solution[4].replace("\n", ""))
    bot.send_message(message.chat.id, solution[5].replace("\n", ""))


def process_text(message):
    model = message.text

    if model.lower() == "/назад":
        bot.send_message(message.chat.id, "Введите номер следующего задания")

    elif model.lower() == "/решение":
        if numb in ("3", "9", "10", "17", "18", "22", "24", "25", "26", "27"):
            if numb == "3":
                for i in range(1, 7):
                    if i == 6:
                        text = open(f"Задания для бота Телеграм/{numb}/Задания/{rand}/Решение/Решение{i}.txt", "r",
                                    encoding='utf-8').read()
                        bot.send_message(message.chat.id, text)
                    else:
                        ph = open(f"Задания для бота Телеграм/{numb}/Задания/{rand}/Решение/Решение{i}.png", "rb")
                        text = open(f"Задания для бота Телеграм/{numb}/Задания/{rand}/Решение/Решение{i}.txt", "r",
                                    encoding='utf-8').read()
                        bot.send_photo(message.chat.id, ph, text)
            else:
                text = open(f"Задания для бота Телеграм/{numb}/Задания/{rand}/Решение.txt", "r",
                            encoding='utf-8').read()
                bot.send_message(message.chat.id, text)

        else:
            bot.send_message(message.chat.id, solution)

    elif model.lower() == "/ответ":
        bot.send_message(message.chat.id, answer)

    elif model != answer:
        bot.send_message(message.chat.id, "Ответ неверный!")
        bot.register_next_step_handler(message, process_text)

    else:
        bot.send_message(message.chat.id, "Молодец! Это верный ответ")


@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_message(message.chat.id, "Извините, я Вас не понимаю")


bot.polling()