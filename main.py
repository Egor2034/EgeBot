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


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Jell")


@bot.message_handler(commands=[str(i) for i in range(1, 28)])
def goo(message):
    global task, rand, answer, solution

    rand = random.randint(1, 6)

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