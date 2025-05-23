import os
import telebot
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.environ.get("TELEGRAM_API_KEY")

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama3-70b-8192",
)

print(chat_completion.choices[0].message.content)