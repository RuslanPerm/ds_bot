import discord
import requests
from googletrans import Translator
import asyncio

TOKEN = 'ODMwMzkzNzIxMzk2MjY0OTkw.YHGCaw.9pbGlP5MsNURXPFXAkRjQwcMKLc'


class QuakeReq():
    def __init__(self, name):
        qc_req = requests.get(f'https://quake-stats.bethesda.net/api/v2/Player/Stats?name={name}')
        if qc_req.status_code == 500:
            self.status_code = 500
        else:
            self.status_code = 200
            self.name = qc_req.json()['name']

            self.duel = qc_req.json()["playerRatings"]["duel"]
            self.duel_rating = self.duel['rating']
            self.duel_deviation = self.duel["deviation"]
            self.duel_gamescount = self.duel["gamesCount"]
            self.duel_last_update = self.duel['lastChange']

            self.tdm = qc_req.json()["playerRatings"]["tdm"]
            self.tdm_rating = self.tdm['rating']
            self.tdm_deviation = self.tdm["deviation"]
            self.tdm_gamescount = self.tdm["gamesCount"]
            self.tdm_last_update = self.tdm['lastChange']

    def full_info(self):
        if self.status_code == 500:
            print('Неверный ник, попробуй')
        else:
            return (f'Name: {self.name}\n \n'
                    f'Duel: {self.duel_rating}±{self.duel_deviation} (Games: {self.duel_gamescount})\n')


class WeatherReq():
    def __init__(self, city):
        self.API = '2c6c62ecc0d20abf473f5b3274545e06'
        self.req = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API}')

    def m_info(self):
        if self.req.status_code == 500:
            return 'Не могу найти это место'
        else:
            wth = self.req.json()
            print(wth)
            return (f'{wth["name"]}, {wth["sys"]["country"]}: '
                    f'{wth["main"]["temp"]}*F, {wth["weather"][0]["main"]}')


class DisBot(discord.Client):
    async def on_ready(self):
        print(f"{self.user} в Discord'е!")
        for guild in client.guilds:
            print(
                f'{client.user} зашёл в хату:\n'
                f'{guild.name} (id: {guild.id})'
            )
        self.ln_src = 'ru'
        self.ln_dest = 'en'

    async def on_message(self, message):
        if message.content.lower() == '!help':
            await message.channel.send('''*!help* - помощь по командам
                                            *!wth {city}* - погода сейчас
                                            *!trans/!text* - перевести из {src} языка в {dest} язык
                                            *!set_timer {time in hours} часов {time in minutes} минут* - таймер''')
        elif message.content.startswith('!trans'):
            needtotr = message.content[6:]
            translator = Translator()
            translated_one = translator.translate(needtotr, dest='ru').text
            await message.channel.send(translated_one)

        elif message.content.startswith('!change'):
            self.ln_src = message.content[8:10]
            self.ln_dest = message.content[11:13]
            await message.channel.send(f'{self.ln_src}-{self.ln_dest} выбраны')

        elif message.content.startswith('!text'):
            needtotr = message.content[5:]
            translator = Translator()
            translated_one = translator.translate(needtotr, src=self.ln_src, dest=self.ln_dest).text
            await message.channel.send(translated_one)

        elif message.content.lower().startswith('!set_timer'):
            hours, minutes = int(message.content.split()[2]), int(message.content.split()[4])
            await message.channel.send(f'Таймер задаведён {hours} часов {minutes} минут')
            await asyncio.sleep(hours * 3600 + minutes * 60)
            await message.channel.send('Время вышло :alarm_clock:')

        elif message.content.lower().startswith('!qcs'):
            qcs = QuakeReq(message.content[5:])
            await message.channel.send(qcs.full_info())

        elif message.content.lower().startswith('!wth'):
            wth = WeatherReq(message.content[5:])
            await message.channel.send(wth.m_info())


client = DisBot()
client.run(TOKEN)