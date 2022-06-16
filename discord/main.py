import discord
from discord.ext import commands
from datetime import datetime
import json
from keep_alive import keep_alive

with open("card_artist.json", "r") as read_file:
    data_artists = json.load(read_file)
with open("card_price.json", "r") as read_file:
    data_prices = json.load(read_file)
with open("card_legalities.json", "r") as read_file:
    data_legalities = json.load(read_file)
with open("card_image1.json", "r") as read_file:
    data_images = json.load(read_file)
with open("card_oracle1.json", "r") as read_file:
    data_oracles = json.load(read_file)

prefix = "*"
bot = commands.Bot(command_prefix=prefix, help_command=None)

@bot.command()
async def help(context):
    help = '*find {имя карты} - найти фото карты \n ' \
           '*findfull {имя карты} - найти полную информацию о карте \n' \
           '*findoracle {имя карты} - найти оракл карты \n' \
           '*findprice {имя карты} - найти цену \n' \
           '*findlegal {имя карты} - легальность карты в разных форматах \n' \
           'Также вы можете получить информацию о карте во время общения: \n' \
           '(название карты) - фото карты \n{название карты} - оракл карты \n[название карты] - цены карты \n*название карты* - легальность карты \n!!!названия карт писать только на английском!!! '
    embed_commands = discord.Embed(title="Команды бота", description=help, colour=0x87CEEB, timestamp=datetime.utcnow())
    embed_commands.set_author(name="MTGSearcher",
                              icon_url="https://sun9-69.userapi.com/impg/MpeCkG6cKBmcQoirZmi0EvNgKdnwlB5A6k7aHA/J74wfRfqfE8.jpg?size=720x720&quality=96&sign=a34757aa8ad78dbf4b71ca7aa0b73dd7&type=album")
    await context.send(embed=embed_commands)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} серверов!"))

@bot.command()
async def findfull(ctx, *, content: str):
    card_image = 'Не найдено!'
    prices = 'Не найдено!'
    legality = 'Не найдено!'
    card_name = content
    flag = 0
    flag1 = 0
    for i in data_images:
        if i['name'] == card_name or i['name'].lower() == card_name or (card_name.lower() in i['name'].lower() and card_name.lower()[0:3] == i['name'].lower()[0:3]):
            if 'image_first_side' not in i:
                card_image = i['image']
                break
            else:
                flag = 1
                card_image_1 = i['image_first_side']
                card_image_2 = i['image_second_side']
                break
    for i in data_oracles:
        if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i['name'].lower():
            if 'oracle_first_side' not in i and 'oracle_second_side' not in i:
                card_oracle = i['oracle_text']
                break
            else:
                flag = 1
                card_oracle_1 = i['oracle_first_side']
                card_oracle_2 = i['oracle_second_side']
                break
    if flag == 0:
        embed_oracle = discord.Embed(title="Оракл карты", description=card_oracle, colour=0x87CEEB,
                                     timestamp=datetime.utcnow())
        embed_oracle.set_author(name="MTGSearcher",
                                icon_url="https://sun9-69.userapi.com/impg/MpeCkG6cKBmcQoirZmi0EvNgKdnwlB5A6k7aHA/J74wfRfqfE8.jpg?size=720x720&quality=96&sign=a34757aa8ad78dbf4b71ca7aa0b73dd7&type=album")
        await ctx.send(embed=embed_oracle)
    else:
        embed_oracle = discord.Embed(title="Оракл карты", colour=0x87CEEB,
                                     timestamp=datetime.utcnow())
        embed_oracle.set_author(name="MTGSearcher",
                                icon_url="https://sun9-69.userapi.com/impg/MpeCkG6cKBmcQoirZmi0EvNgKdnwlB5A6k7aHA/J74wfRfqfE8.jpg?size=720x720&quality=96&sign=a34757aa8ad78dbf4b71ca7aa0b73dd7&type=album")
        embed_oracle.add_field(name="Оракл верхний стороны", value=card_oracle_1, inline=False)
        embed_oracle.add_field(name="Оракл нижней стороны", value=card_oracle_2, inline=False)
        await ctx.send(embed=embed_oracle)
    for i in data_prices:
        if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i['name'].lower():
            for j in i['prices'].items():
                if j[1] != None:
                    prices += str(j[0]) + ' ' + ':' + ' ' + str(j[1]) + '\n'
            break
    for i in data_legalities:
        if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i['name'].lower():
            for j in i['legalities'].items():
                if j[1] != None:
                    legality += str(j[0]) + ' ' + ':' + ' ' + str(j[1]) + '\n'
            break
    card_stats = 'Данная карта не имеет стат!'
    for i in data_artists:
        if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i['name'].lower():
            card_artist = i['artist']
            break

    embed_full = discord.Embed(title="Полная информация о карте", colour=0x87CEEB, timestamp=datetime.utcnow())
    embed_full.set_author(name="MTGSearcher",
                          icon_url="https://sun9-69.userapi.com/impg/MpeCkG6cKBmcQoirZmi0EvNgKdnwlB5A6k7aHA/J74wfRfqfE8.jpg?size=720x720&quality=96&sign=a34757aa8ad78dbf4b71ca7aa0b73dd7&type=album")
    embed_full.add_field(name="Цены", value=prices, inline=False)
    embed_full.add_field(name="Легальность", value=legality, inline=False)
    embed_full.add_field(name="Художник", value=card_artist, inline=False)
    await ctx.send(embed=embed_full)
    if flag == 0:
        await ctx.send(card_image)
    else:
        await ctx.send(card_image_1)
        await ctx.send(card_image_2)


@bot.command()
async def find(ctx, *, content: str):
    card_image = 'Не найдено!'
    card_name = content
    flag = 0
    for i in data_images:
        if i['name'] == card_name or i['name'].lower() == card_name or (card_name.lower() in i['name'].lower() and card_name.lower()[0:3] == i['name'].lower()[0:3]):
            if 'image_first_side' not in i:
                card_image = i['image']
                break
            else:
                flag = 1
                card_image_1 = i['image_first_side']
                card_image_2 = i['image_second_side']
                break
    if flag == 0:
        await ctx.send(card_image)
    else:
        await ctx.send(card_image_1)
        await ctx.send(card_image_2)


@bot.command()
async def findoracle(ctx, *, content: str):
    card_name = content
    card_oracle = 'Не найдено!'
    flag = 0
    for i in data_oracles:
        if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i['name'].lower():
            if 'oracle_first_side' not in i and 'oracle_second_side' not in i:
                card_oracle = i['oracle_text']
                break
            else:
                flag = 1
                card_oracle_1 = i['oracle_first_side']
                card_oracle_2 = i['oracle_second_side']
                break
    if flag == 0:
        embed_oracle = discord.Embed(title="Оракл карты", description=card_oracle, colour=0x87CEEB,
                                     timestamp=datetime.utcnow())
        embed_oracle.set_author(name="MTGSearcher",
                                icon_url="https://sun9-69.userapi.com/impg/MpeCkG6cKBmcQoirZmi0EvNgKdnwlB5A6k7aHA/J74wfRfqfE8.jpg?size=720x720&quality=96&sign=a34757aa8ad78dbf4b71ca7aa0b73dd7&type=album")
        await ctx.send(embed=embed_oracle)
    else:
        embed_oracle = discord.Embed(title="Оракл карты", colour=0x87CEEB,
                                     timestamp=datetime.utcnow())
        embed_oracle.set_author(name="MTGSearcher",
                                icon_url="https://sun9-69.userapi.com/impg/MpeCkG6cKBmcQoirZmi0EvNgKdnwlB5A6k7aHA/J74wfRfqfE8.jpg?size=720x720&quality=96&sign=a34757aa8ad78dbf4b71ca7aa0b73dd7&type=album")
        embed_oracle.add_field(name="Оракл верхний стороны", value=card_oracle_1, inline=False)
        embed_oracle.add_field(name="Оракл нижней стороны", value=card_oracle_2, inline=False)
        await ctx.send(embed=embed_oracle)


@bot.command()
async def findprice(ctx, *, content: str):
    card_name = content
    output = ''
    for i in data_prices:
        if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i['name'].lower():
            for j in i['prices'].items():
                if j[1] != None:
                    output += str(j[0]) + ' ' + ':' + ' ' + str(j[1]) + '\n'
            break
    embed_price = discord.Embed(title="Цены карты", description=output, colour=0x87CEEB,
                                timestamp=datetime.utcnow())
    embed_price.set_author(name="MTGSearcher",
                           icon_url="https://sun9-69.userapi.com/impg/MpeCkG6cKBmcQoirZmi0EvNgKdnwlB5A6k7aHA/J74wfRfqfE8.jpg?size=720x720&quality=96&sign=a34757aa8ad78dbf4b71ca7aa0b73dd7&type=album")
    await ctx.send(embed=embed_price)


@bot.command()
async def findlegal(ctx, *, content: str):
    legality = ''
    card_name = content
    for i in data_legalities:
        if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i['name'].lower():
            for j in i['legalities'].items():
                if j[1] != None:
                    legality += str(j[0]) + ' ' + ':' + ' ' + str(j[1]) + '\n'
            break
    embed_legal = discord.Embed(title="Легальность карты", description=legality, colour=0x87CEEB,
                                timestamp=datetime.utcnow())
    embed_legal.set_author(name="MTGSearcher",
                           icon_url="https://sun9-69.userapi.com/impg/MpeCkG6cKBmcQoirZmi0EvNgKdnwlB5A6k7aHA/J74wfRfqfE8.jpg?size=720x720&quality=96&sign=a34757aa8ad78dbf4b71ca7aa0b73dd7&type=album")
    await ctx.send(embed=embed_legal)

@bot.command()
async def findartist(ctx, *, content: str):
    card_name = content
    for i in data_artists:
        if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i['name'].lower():
            card_artist = i['artist']
            break
    await ctx.send(card_artist)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    context = message.content.split()
    a = ''
    k1 = 0
    k2 = 0
    k3 = 0
    for i in range(len(context)):
            if context[i][-1] == ')' and context[i][0] == '(':
              card_name = context[i].replace('(','').replace(')','')
              for i in data_images:
                    if i['name'] == card_name or i['name'].lower() == card_name or (
                            card_name.lower() in i['name'].lower() and card_name.lower()[0:3] == i['name'].lower()[
                                                                                                 0:3]):
                        if 'image_first_side' not in i:
                            card_image = i['image']
                            await message.channel.send(card_image)
                            break
                        else:
                            card_image_1 = i['image_first_side']
                            card_image_2 = i['image_second_side']
                            await message.channel.send(card_image_1)
                            await message.channel.send(card_image_2)
                            break
            elif context[i][-1] == '}' and context[i][0] == '{':
                  card_name = context[i].replace('{','').replace('}','').strip(' ')
                  for i in data_oracles:
                    if i['name'] == card_name or i['name'].lower() == card_name or card_name.lower() in i[
                        'name'].lower():
                        if 'oracle_first_side' not in i and 'oracle_second_side' not in i:
                            card_oracle = 'Оракл карты: ' + i['name'] + '\n' + i['oracle_text']
                            await message.channel.send(card_oracle)
                            break
                        else:
                            card_oracle_1 = 'Оракл верхней стороны карты: ' + i['name'] + '\n' + i['oracle_first_side']
                            card_oracle_2 = 'Оракл нижней стороны карты: ' + i['name'] + '\n' + i['oracle_second_side']
                            await message.channel.send(card_oracle_1)
                            await message.channel.send(card_oracle_2)
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
                      await message.channel.send(output)
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
                            await message.channel.send(card_image)
                            break
                        else:
                            card_image_1 = i['image_first_side']
                            card_image_2 = i['image_second_side']
                            await message.channel.send(card_image_1)
                            await message.channel.send(card_image_2)
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
                            await message.channel.send(card_oracle)
                            break
                        else:
                            card_oracle_1 = 'Оракл верхней стороны карты: ' + i['name'] + '\n' + i['oracle_first_side']
                            card_oracle_2 = 'Оракл нижней стороны карты: ' + i['name'] + '\n' + i['oracle_second_side']
                            await message.channel.send(card_oracle_1)
                            await message.channel.send(card_oracle_2)
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
                      await message.channel.send(output)
                  a = ''
            elif context[i][0] == '[' or k3 == 1:
                k3 = 1
                a += context[i] + ' '
                
    
keep_alive()
bot.run('TOKEN')
