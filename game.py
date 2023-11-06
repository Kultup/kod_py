import json
import telebot
from telebot import types

TOKEN = '6642577626:AAEI7Tg8yVA3oZflxyKq75pl-xS-gI72gew'
bot = telebot.TeleBot(TOKEN)


def load_questions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        questions = json.load(file)
    return questions


user_data = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(
        message.chat.id, 'Привіт! Ласкаво просимо до гри у вікторину. Я задам вам кілька питань. Почнемо!')
    questions = load_questions('questions.json')
    user_data[message.chat.id] = {'questions': questions, 'score': 0}
    ask_question(message.chat.id)


def ask_question(chat_id):
    user = user_data.get(chat_id)
    if user and user['questions']:
        question = user['questions'][0]
        options = question['options']
        correct_answer = question['correct_answer']
        user_data[chat_id]['correct_answer'] = correct_answer

        markup = types.InlineKeyboardMarkup()
        for option in options:
            button = types.InlineKeyboardButton(
                text=option, callback_data=option)
            markup.add(button)

        bot.send_message(
            chat_id, f"{question['question']}", reply_markup=markup)
    else:
        bot.send_message(
            chat_id, 'Гра завершена. Ваш рахунок: {}'.format(user['score']))
        del user_data[chat_id]


@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    chat_id = call.message.chat.id
    user = user_data.get(chat_id)
    if user and user['questions']:
        user_answer = call.data
        correct_answer = user['correct_answer']
        if user_answer == correct_answer:
            user_data[chat_id]['score'] += 1
        user_data[chat_id]['questions'].pop(0)
        ask_question(chat_id)


if __name__ == "__main__":
    bot.polling(none_stop=True)
