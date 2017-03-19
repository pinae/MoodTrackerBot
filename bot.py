#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import telepot
from apikey import API_KEY
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from time import sleep
from time import time as utc_time
from datetime import datetime, time
from draw_graph import plot_day, read_day
import re
import os


def write_users(user_list):
    with open("users.txt", 'w') as users_file:
        users_file.write("\n".join([str(uid) for uid in user_list]))


def get_users():
    user_list = []
    try:
        with open("users.txt", 'r') as users_file:
            for line in users_file.readlines():
                user_list.append(int(line))
    except FileNotFoundError:
        pass
    return user_list


def append_quality(number, user_id, timestamp):
    with open("mood_data.csv", 'r') as data_file:
        newest_line = data_file.readlines()[-1]
    if re.match(r'\d+, \d+, [^,]+, -?\d', newest_line):
        mood = re.match('\d+, \d+, ([^,]+), -?\d+', newest_line).groups()[0]
        with open("mood_data.csv", 'a') as data_file:
            data_file.write("\n" + ", ".join([str(user_id), str(timestamp), mood, str(number)]))
    else:
        with open("mood_data.csv", 'a') as data_file:
            data_file.write(", " + str(number))


def on_chat_message(msg):
    plot_regex = re.compile(r"^/(plot|graph|diagram) *(\d+)?$")
    try:
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
            user_id = msg['chat']['id']
            if msg['text'] in ["/start", "/start start", "Hallo", "Hi", "Start"]:
                if user_id not in users:
                    users.append(user_id)
                    write_users(users)
                bot.sendMessage(user_id, "In einem Wort: Wie fühlst du dich gerade?")
            elif msg['text'] in ["/stop", "Hör auf", "Stop", "Ende"]:
                users.remove(user_id)
                write_users(users)
                bot.sendMessage(user_id, "Ich frage dich ab jetzt nicht mehr.")
            elif plot_regex.match(msg['text']):
                matches = plot_regex.match(msg['text'])
                if len(matches.groups()) >= 2:
                    offset = int(matches.groups(1))
                else:
                    offset = 0
                times, mood_values = read_day(user_id, offset)
                plot_day(times, mood_values).savefig("tmp.png")
                bot.sendPhoto(chat_id, "tmp.png")
                os.remove("tmp.png")
            elif msg['text'].startswith("/"):
                bot.sendMessage(user_id, "Mit dem Befehl `" + msg['text'] + "` kann ich leider nichts anfangen.")
                bot.sendMessage(user_id, "Ich verstehe nur /start und /stop. Bei allen anderen Nachrichten gehe ich " +
                                "davon aus, dass es ein Gefühl ist.")
            else:  # It must be a mood
                with open("mood_data.csv", 'a') as data_file:
                    data_file.write("\n" + ", ".join([str(user_id), str(msg['date']), "".join(msg['text'].split(','))]))
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                               [InlineKeyboardButton(text='mies', callback_data='-2'),
                                InlineKeyboardButton(text='schlecht', callback_data='-1'),
                                InlineKeyboardButton(text='neutral', callback_data='0'),
                                InlineKeyboardButton(text='gut', callback_data='1'),
                                InlineKeyboardButton(text='super', callback_data='2')],
                           ])
                bot.sendMessage(chat_id, 'Wie gut fühlt sich das an?', reply_markup=keyboard)
    except telepot.exception.BotWasBlockedError:
        pass


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    append_quality(query_data, from_id, int(utc_time()))
    bot.answerCallbackQuery(query_id, text='OK, gespeichert.')


bot = telepot.Bot(API_KEY)
users = get_users()
try:
    bot.message_loop({'chat': on_chat_message,
                      'callback_query': on_callback_query})
    print("Bot started ...")
    while True:
        if time(23, 30) > datetime.now().time() > time(8, 30):
            for user in users:
                try:
                    bot.sendMessage(user, "In einem Wort: Wie fühlst du dich gerade?")
                except telepot.exception.BotWasBlockedError:
                    users.remove(user)
                    write_users(users)
        sleep(60*60)
except KeyboardInterrupt:
    pass
