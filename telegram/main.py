import logging

from aiogram import Bot, Dispatcher, executor, types
import json
from keep_alive import keep_alive

with open("card_price.json", "r") as read_file:
    data_prices = json.load(read_file)
with open("card_image1.json", "r") as read_file:
    data_images = json.load(read_file)
with open("card_oracle1.json", "r") as read_file:
    data_oracles = json.load(read_file)
with open("card_legalities.json", "r") as read_file:
    data_legalities = json.load(read_file)

API_TOKEN = 'TOKEN'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ бот для поиска карт)\n Команды:\n 1) (название карты) - фото карты \n 2) {название карты} - оракл карты \n 3) [название карты] - цены карты \n 4) *название карты* - легальность карты \n !!!названия карт писать только на английском!!!")

@dp.message_handler()
async def find(message: types.Message):
    context = message['text'].split()
    a = ''
    k1 = 0
    k2 = 0
    k3 = 0
    k4 = 0
    for i in range(len(context)):
            if context[i][-1] == ')' and context[i][0] == '(':
              card_name = context[i].replace('(','').replace(')','')
              for i in data_images:
                    if i['name'] == card_name or i['name'].lower() == card_name or (
                            card_name.lower() in i['name'].lower() and card_name.lower()[0:3] == i['name'].lower()[
                                                                                                 0:3]):
                        if 'image_first_side' not in i:
                            card_image = i['image']
                            await bot.send_photo(chat_id=message.chat.id, photo=card_image)
                            break
                        else:
                            card_image_1 = i['image_first_side']
                            card_image_2 = i['image_second_side']
                            await bot.send_photo(chat_id=message.chat.id, photo=card_image_1)
                            await bot.send_photo(chat_id=message.chat.id, photo=card_image_2)
                            break
            elif context[i][-1] == '}' and context[i][0] == '{':
                  card_name = context[i].replace('{','').replace('}','').strip(' ')
                  for i in data_oracles:
                    if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i[
                        'name'].lower():
                        if 'oracle_first_side' not in i and 'oracle_second_side' not in i:
                            card_oracle = 'Оракл карты: ' + i['name'] + '\n' + i['oracle_text']
                            await message.answer(card_oracle)
                            break
                        else:
                            card_oracle_1 = 'Оракл верхней стороны карты: ' + i['name'] + '\n' + i['oracle_first_side']
                            card_oracle_2 = 'Оракл нижней стороны карты: ' + i['name'] + '\n' + i['oracle_second_side']
                            await message.answer(card_oracle_1)
                            await message.answer(card_oracle_2)
                            break
            elif context[i][-1] == ']' and context[i][0] == '[':
                  card_name = context[i].replace('[','').replace(']','').strip(' ')
                  output = ''
                  for i in data_prices:
                      if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i[
                          'name'].lower():
                          for j in i['prices'].items():
                              if j[1] != None:
                                  output += str(j[0]) + ' ' + ':' + ' ' + str(j[1]) + '\n'
                                  card_name_original = i['name']
                          break
                  if output != '':
                      output = 'Цена карты: ' + card_name_original + '\n' + output
                      await message.answer(output)
            elif context[i][-1] == '*' and context[i][0] == '*':
                  card_name = context[i].replace('*','').replace('*','').strip(' ')
                  output = ''
                  for i in data_legalities:
                      if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i['name'].lower():
                          card_name_original = i['name']
                          for j in i['legalities'].items():
                              if j[1] != None:
                                  output += str(j[0]) + ' ' + ':' + ' ' + str(j[1]) + '\n'
                          break
                  if output != '':
                      output = 'Легальность карты: ' + card_name_original + '\n' + output
                      await message.answer(output)
            elif context[i][-1] == ')' and k1 == 1:
                  k1 = 0
                  a += context[i]
                  card_name = a.replace('(','').replace(')','').strip(' ')
                  for i in data_images:
                    if i['name'] == card_name or i['name'].lower() == card_name or (
                            card_name.lower() in i['name'].lower() and card_name.lower()[0:3] == i['name'].lower()[
                                                                                                 0:3]):
                        if 'image_first_side' not in i:
                            card_image = i['image']
                            await bot.send_photo(chat_id=message.chat.id, photo=card_image)
                            break
                        else:
                            card_image_1 = i['image_first_side']
                            card_image_2 = i['image_second_side']
                            await bot.send_photo(chat_id=message.chat.id, photo=card_image_1)
                            await bot.send_photo(chat_id=message.chat.id, photo=card_image_2)
                            break
                  a = ''
            elif context[i][0] == '(' or k1 == 1:
                k1 = 1
                a += context[i] + ' '
            elif context[i][-1] == '}' and k2 == 1:
                  k2 = 0
                  a += context[i]
                  card_name = a.replace('{','').replace('}','').strip(' ')
                  for i in data_oracles:
                    if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i[
                        'name'].lower():
                        if 'oracle_first_side' not in i and 'oracle_second_side' not in i:
                            card_oracle = 'Оракл карты: ' + i['name'] + '\n' + i['oracle_text']
                            await message.answer(card_oracle)
                            break
                        else:
                            card_oracle_1 = 'Оракл верхней стороны карты: ' + i['name'] + '\n' + i['oracle_first_side']
                            card_oracle_2 = 'Оракл нижней стороны карты: ' + i['name'] + '\n' + i['oracle_second_side']
                            await message.answer(card_oracle_1)
                            await message.answer(card_oracle_2)
                            break
                  a = ''
            elif context[i][0] == '{' or k2 == 1:
                k2 = 1
                a += context[i] + ' '
            elif context[i][-1] == ']' and k3 == 1:
                  k3 = 0
                  a += context[i]
                  card_name = a.replace('[','').replace(']','').strip(' ')
                  output = ''
                  for i in data_prices:
                      if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i[
                          'name'].lower():
                          for j in i['prices'].items():
                              if j[1] != None:
                                  output += str(j[0]) + ' ' + ':' + ' ' + str(j[1]) + '\n'
                                  card_name_original = i['name']
                          break
                  if output != '':
                      output = 'Цена карты: ' + card_name_original + '\n' + output
                      await message.answer(output)
                  a = ''
            elif context[i][0] == '[' or k3 == 1:
                k3 = 1
                a += context[i] + ' '
            elif context[i][-1] == '*' and k4 == 1:
                  k4 = 0
                  a += context[i]
                  card_name = a.replace('*','').replace('*','').strip(' ')
                  output = ''
                  for i in data_legalities:
                      if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i['name'].lower():
                          card_name_original = i['name']
                          for j in i['legalities'].items():
                              if j[1] != None:
                                  output += str(j[0]) + ' ' + ':' + ' ' + str(j[1]) + '\n'
                          break
                  if output != '':
                      output = 'Легальность карты: ' + card_name_original + '\n' + output
                      await message.answer(output)
                  a = ''
            elif context[i][0] == '*' or k4 == 1:
                k4 = 1
                a += context[i] + ' '

if __name__ == '__main__':
    keep_alive()
    executor.start_polling(dp, skip_updates=True)
