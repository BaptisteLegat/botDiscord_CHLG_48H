import discord
from discord.ext import commands
import asyncio
import openai
import requests
import icalendar
import pytz
from datetime import datetime, timedelta
import sqlite3
import re

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
openai.api_key = "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"
kolok_role_name = "Kolok"

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Commande inconnue.')
    else:
        raise error

@bot.command()
async def send(ctx):
    message = ctx.message.content
    channel = ctx.message.channel
    text_to_send = message.split('!send ')[1]
    await channel.send(text_to_send)
    await ctx.message.delete()

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 1096024112687759371:
        if payload.emoji.name == '👍':
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, name="SOS")
            await member.add_roles(role)
            print(f"Attribuer le rôle {role.name} à {member.display_name}")
        if payload.emoji.name == '👽':
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, name="Pédagogie")
            await member.add_roles(role)
            print(f"Attribuer le rôle {role.name} à {member.display_name}")
        if payload.emoji.name == '🍹':
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, name="Kolok")
            await member.add_roles(role)
            print(f"Attribuer le rôle {role.name} à {member.display_name}")
        if payload.emoji.name == '🔔':
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, name="Yrappel")
            await member.add_roles(role)
            print(f"Attribuer le rôle {role.name} à {member.display_name}")
            message = "Vous vous êtes bien inscrit au Yrappel\nVeuillez m'envoyer votre lien privé Hyperplanning précédé de la commande !verify\n\nPour obtenir ce lien veuillez vous rendre sur votre emplois du temps Hyperplanning et cliquer sur le petit logo ical en haut à droite\nExemple : !verify https://hp22.ynov.com/LYO/Telechargements/ical/Edt_YOURNAME"
            await member.send(message)

@bot.command()
async def sondage(ctx, question, *options):
    message = f"{question}\n\nRépondez avec les réactions ci-dessous :\n"
    for option in options:
        message += f"{options.index(option)+1}: {option}\n"
    reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    message = await ctx.send("**{}**\n\n{}".format(question, "\n".join("{} {}".format(reactions[i], option) for i, option in enumerate(options))))
    for i in range(len(options)):
        await message.add_reaction(reactions[i])
    await ctx.message.delete()

@bot.command()
async def afterwork(ctx):
    guild = ctx.guild
    kolok_role = discord.utils.get(guild.roles, name=kolok_role_name)
    general_channel = discord.utils.get(guild.channels, name="général")
    sent_message = await general_channel.send(f"{kolok_role.mention} Un afterwork est prévu à la Kolok ce soir, réagissez si vous venez !")
    await sent_message.add_reaction('👍')

pedagogie_emoji = "🎓"  # définir un emoji pour le rôle Pédagogie
sos_emoji = "🆘"  # définir un emoji pour le rôle SOS



# Connexion à la base de données SQLite
conn = sqlite3.connect('calendriers.db')
c = conn.cursor()

# Création de la table pour stocker les iCals
c.execute('''CREATE TABLE IF NOT EXISTS icals
             (discord_id TEXT, ical_url TEXT)''')


@bot.command()
async def verify(ctx, url):
    if not isinstance(ctx.message.channel, discord.abc.PrivateChannel):
        await ctx.send("Cette commande est réservée aux messages privés.")
    # Vérification de la validité de l'URL
    regex = re.compile(
        r'^https?://'  # http:// ou https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domaine
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # adresse IP
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if not regex.match(url):
        await ctx.send("URL invalide.")
        return

    # Récupération de l'ID de l'utilisateur sur Discord
    discord_id = str(ctx.author.id)

    # Ajout de l'iCal dans la base de données
    c.execute("INSERT INTO icals VALUES (?, ?)", (discord_id, url))
    conn.commit()

    await ctx.send("iCal stocké avec succès !")
# Commande pour récupérer l'iCal d'un utilisateur

@bot.command()
async def time(ctx):
  date_start_str = '20220915T070000Z'
  date_start_obj = datetime.strptime(date_start_str, '%Y%m%dT%H%M%SZ')

  date_end_str = '20220915T110000Z'
  date_end_obj = datetime.strptime(date_end_str, '%Y%m%dT%H%M%SZ')

  # Définir le fuseau horaire UTC
  timezone_utc = pytz.timezone('UTC')

  # Convertir la date en heure locale
  timezone_local = pytz.timezone('Europe/Paris') # Remplacez "Europe/Paris" par votre fuseau horaire local
  date_start_local = timezone_utc.localize(date_start_obj).astimezone(timezone_local)
  date_end_local = timezone_utc.localize(date_end_obj).astimezone(timezone_local)

  # Afficher la date locale
  await ctx.send(date_start_local.strftime('%Y-%m-%d %H:%M:%S'))
  await ctx.send(date_end_local.strftime('%Y-%m-%d %H:%M:%S'))

@bot.command()
async def get_ical(ctx):
    if not isinstance(ctx.message.channel, discord.abc.PrivateChannel):
        await ctx.send("Cette commande est réservée aux messages privés.")
    # Récupération de l'ID de l'utilisateur sur Discord
    discord_id = str(ctx.author.id)

    # Récupération de l'iCal dans la base de données
    c.execute("SELECT ical_url FROM icals WHERE discord_id=?", (discord_id,))
    row = c.fetchone()
    if row is not None:
        # Envoi de l'iCal à l'utilisateur
        ical_url = row[0]
        await ctx.send(f"Voici votre iCal: {ical_url}")
    else:
        await ctx.send("Aucun iCal n'a été stocké pour cet utilisateur.")


@bot.command()
async def bonjour(ctx):
    if ctx.author.guild_permissions.manage_roles:
        await ctx.send("Bonjour, vous avez les permissions pour gérer les rôles.")
    else:
        await ctx.send("Bonjour!")


@bot.command()
async def rappel(ctx, date_str, heure_str, *, message):
    """Crée un rappel à une date et une heure spécifiques."""
    # Convertir la date et l'heure en objets datetime
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    heure_obj = datetime.strptime(heure_str, '%H:%M').time()
    rappel_datetime = datetime.combine(date_obj, heure_obj)

    # Calculer le temps d'attente avant le rappel
    maintenant = datetime.now()
    temps_attente = (rappel_datetime - maintenant).total_seconds()

    # Vérifier que le temps d'attente est positif
    if temps_attente < 0:
        await ctx.send("La date et l'heure spécifiées sont déjà passées.")
        return

    # Attendre le temps nécessaire avant d'envoyer le rappel
    await asyncio.sleep(temps_attente)

    # Envoyer le rappel
    await ctx.send(f"{ctx.author.mention}, voici votre rappel : {message}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Commande inconnue.')
    else:
        raise error


@bot.command()
async def gpt(ctx, *, message):
    # Envoyer la requête à l'API de ChatGPT
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Récupérer la réponse de l'API
    reply = response.choices[0].text.strip()

    # Envoyer la réponse en message privé
    await ctx.author.send(f"Voici la réponse de ChatGPT :\n{reply}")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command()
async def ajrd(ctx):
  discord_id = str(ctx.author.id)
  c.execute("SELECT ical_url FROM icals WHERE discord_id=?", (discord_id,))
  row = c.fetchone()
  if row is not None:
    ical_url = row[0]
  else:
      await ctx.send("Aucun iCal n'a été stocké pour cet utilisateur.")

  response = requests.get(ical_url)
  today = datetime.today().date()
  if response.status_code == 200:
    calendar = icalendar.Calendar.from_ical(response.content)
  for event in calendar.walk("VEVENT"):
      if event["DTSTART"].dt.date() == today:
        dtstart = event["DTSTART"].dt
        dtend = event["DTEND"].dt
        timezone = pytz.timezone("Europe/Paris")
        dtstart_paris = dtstart.astimezone(timezone)
        dtend_paris = dtend.astimezone(timezone)
        await ctx.send(f"{event['SUMMARY']}")
        await ctx.send(f"{event['LOCATION']}")
        await ctx.send(f"{dtstart_paris.strftime('%H:%M')} - {dtend_paris.strftime('%H:%M')}")
  else:
      await ctx.send("Impossible de télécharger le fichier .ical")


@bot.command()
async def demain(ctx):
    discord_id = str(ctx.author.id)
    c.execute("SELECT ical_url FROM icals WHERE discord_id=?", (discord_id,))
    row = c.fetchone()
    if row is not None:
        ical_url = row[0]
    else:
        await ctx.send("Aucun iCal n'a été stocké pour cet utilisateur.")
        return

    response = requests.get(ical_url)
    tomorrow = datetime.today().date() + timedelta(days=1)
    if response.status_code == 200:
        calendar = icalendar.Calendar.from_ical(response.content)
        for event in calendar.walk("VEVENT"):
            if event["DTSTART"].dt.date() == tomorrow:
                dtstart = event["DTSTART"].dt
                dtend = event["DTEND"].dt
                timezone = pytz.timezone("Europe/Paris")
                dtstart_paris = dtstart.astimezone(timezone)
                dtend_paris = dtend.astimezone(timezone)
                await ctx.send(f"{event['SUMMARY']}")
                await ctx.send(f"{event['LOCATION']}")
                await ctx.send(f"{dtstart_paris.strftime('%H:%M')} - {dtend_paris.strftime('%H:%M')}")
        else:
            await ctx.send("Aucun événement trouvé pour demain.")
    else:
        await ctx.send("Impossible de télécharger le fichier .ical")


@bot.command()
async def semaine(ctx):
    discord_id = str(ctx.author.id)
    c.execute("SELECT ical_url FROM icals WHERE discord_id=?", (discord_id,))
    row = c.fetchone()
    if row is not None:
        ical_url = row[0]
    else:
        await ctx.send("Aucun iCal n'a été stocké pour cet utilisateur.")
        return

    response = requests.get(ical_url)
    today = datetime.today().date()
    monday = today - timedelta(days=today.weekday())
    friday = monday + timedelta(days=4)
    if response.status_code == 200:
        calendar = icalendar.Calendar.from_ical(response.content)
        for event in calendar.walk("VEVENT"):
            if monday <= event["DTSTART"].dt.date() <= friday:
                dtstart = event["DTSTART"].dt
                dtend = event["DTEND"].dt
                timezone = pytz.timezone("Europe/Paris")
                dtstart_paris = dtstart.astimezone(timezone)
                dtend_paris = dtend.astimezone(timezone)
                await ctx.send(f"{event['SUMMARY']}")
                await ctx.send(f"{event['LOCATION']}")
                await ctx.send(f"{dtstart_paris.strftime('%a %d/%m %H:%M')} - {dtend_paris.strftime('%H:%M')}")
                await ctx.send("------------------------------")
        else:
            await ctx.send("Aucun événement trouvé pour cette semaine.")
    else:
        await ctx.send("Impossible de télécharger le fichier .ical")


@bot.command()
async def ticket(ctx):
    guild = ctx.guild
    ticket_category = discord.utils.get(guild.categories, name='Tickets')
    if not ticket_category:
        ticket_category = await guild.create_category(name='Tickets')
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(
            read_messages=True, send_messages=True)
    }
    ticket_channel = await ticket_category.create_text_channel(name=f'ticket-{ctx.author.name}', overwrites=overwrites)
    message = await ticket_channel.send(f"{ctx.author.mention} Merci d'avoir ouvert un ticket. Veuillez choisir le rôle que vous souhaitez contacter en réagissant avec l'emoji correspondant.")
    await message.add_reaction(pedagogie_emoji)
    await message.add_reaction(sos_emoji)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in [pedagogie_emoji, sos_emoji]

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        pass
    else:
        if str(reaction.emoji) == pedagogie_emoji:
            role = discord.utils.get(guild.roles, name='Pédagogie')
        elif str(reaction.emoji) == sos_emoji:
            role = discord.utils.get(guild.roles, name='SOS')
        overwrites[role] = discord.PermissionOverwrite(
            read_messages=True, send_messages=True)
        await ticket_channel.edit(overwrites=overwrites)
        await ticket_channel.send(f"Vous avez contacté {role.mention} pour vous aider. Pour fermer le ticket, cliquez sur la réaction ci-dessous.")
        await message.add_reaction('🔒')

        def check(reaction, user):
            return str(reaction.emoji) == '🔒'

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            pass
        else:
            await ticket_channel.delete()
            await ticket_channel.send(f"{ctx.author.mention} Votre ticket a été fermé.")

bot.run('MTA5NTk4NzQyMDU1NTY0NDk3OA.GqQbFs.5XPaVhvE4XAGdZQyQh76UlqtlL-uKRKnJywGvY')
