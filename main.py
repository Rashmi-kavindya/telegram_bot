# import os
# import telebot
# from dotenv import load_dotenv
# from groq import Groq

# load_dotenv()

# API_KEY = os.environ.get("TELEGRAM_API_KEY")

# def get_groq_response(content):
#     client = Groq(
#         api_key=os.environ.get("GROQ_API_KEY"),
#     )

#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": content,
#             }
#         ],
#         model="llama3-70b-8192",
#     )

#     return str(chat_completion.choices[0].message.content)


# bot = telebot.TeleBot(API_KEY)
# @bot.message_handler(commands=['start', 'help'])
# def send_start_help_message(message):
#     bot.reply_to(message, "Welcome! I'm here to assist you with HR-related queries. Type your question and I'll do my best to help you.")

# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def all_other_messages(message):
#     response = get_groq_response(message.text)
#     bot.send_message(message.chat.id, str(response))

# bot.infinity_polling()

# main.py

import os
import telebot
from dotenv import load_dotenv
from groq import Groq
from chatbot_rules import get_hr_response  # 🔁 Import rule-based logic

load_dotenv()

API_KEY = os.environ.get("TELEGRAM_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

bot = telebot.TeleBot(API_KEY)

def get_groq_response(content):
    client = Groq(api_key=GROQ_API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": content}
        ],
        model="llama3-70b-8192",
    )

    return str(chat_completion.choices[0].message.content)


@bot.message_handler(commands=['start', 'help'])
def send_start_help_message(message):
    bot.reply_to(message, "Welcome! I'm here to assist you with HR-related queries. Type your question and I'll do my best to help you.")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def all_other_messages(message):
    user_input = message.text
    response = get_hr_response(user_input)

    # Fallback to AI if no rule matches
    if response is None or response.startswith("I'm sorry"):
        response = get_groq_response(user_input)

    bot.send_message(message.chat.id, response)

bot.infinity_polling()
