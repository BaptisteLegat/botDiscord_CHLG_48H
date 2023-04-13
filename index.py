import discord
from discord.ext import commands
import asyncio
import requests
import icalendar
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

url = "https://hp22.ynov.com/LYO/Telechargements/ical/Edt_ARIAS.ics?version=2022.0.4.3&idICal=11DE48A32C815F96F9F4835844A54A22&param=643d5b312e2e36325d2666683d3126663d31"



response = requests.get(url)
today = datetime.today().date()
tomorrow = datetime.today().date() + timedelta(days=1)



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    
@bot.command()
async def ajrd(ctx):
        if response.status_code == 200:
            calendar = icalendar.Calendar.from_ical(response.content)
        for event in calendar.walk("VEVENT"):
            if event["DTSTART"].dt.date() == today:
                await ctx.send(event["description"])
        else:
            ("Impossible de télécharger le fichier .ical")


@bot.command()
async def demain(ctx):
        if response.status_code == 200:
            calendar = icalendar.Calendar.from_ical(response.content)
        for event in calendar.walk("VEVENT"):
            if event["DTSTART"].dt.date() == tomorrow:
                await ctx.send(event["description"])
        else:
            ("Impossible de télécharger le fichier .ical")



bot.run('MTA5NTk4NzQyMDU1NTY0NDk3OA.GDVohy.GFl4x5RPFzmaD-RoNP8dlFvGKPhSaXyGS32K84')