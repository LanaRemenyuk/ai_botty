import os

import openai
import asyncio
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot, types

load_dotenv()

openai.api_key = os.getenv('API_KEY')
bot = AsyncTeleBot(os.getenv('BOT_TOKEN'))


@bot.message_handler(commands=['start'])
async def say_hi(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    start_button = types.InlineKeyboardButton('hey, Botty!', callback_data='start')
    markup.add(start_button)
    await bot.reply_to(message, """\
Hey 👋, what's up, duuude\
""", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'start')
async def process_start_callback(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    gpt_botty = types.InlineKeyboardButton('start asking', callback_data='gpt_botty')
    markup.add(gpt_botty)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='🐱', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
async def callback_handler(call):
    if call.data == 'gpt_botty':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(call.message.chat.id, "Ask me something ❤")
        if call.data != None:
            await answer_back(call.message)


@bot.message_handler(func=lambda message: True)
async def answer_back(message):
    response = openai.Completion.create(model="text-davinci-003", prompt=message.text, temperature=0, max_tokens=1000)
    await bot.reply_to(message, response['choices'][0]['text'])


asyncio.run(bot.polling())


