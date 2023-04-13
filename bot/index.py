import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

pedagogie_emoji = "🎓" # définir un emoji pour le rôle Pédagogie
sos_emoji = "🆘" # définir un emoji pour le rôle SOS

@bot.command()
async def bonjour(ctx):
    if ctx.author.guild_permissions.manage_roles:
        await ctx.send("Bonjour, vous avez les permissions pour gérer les rôles.")
    else:
        await ctx.send("Bonjour!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Commande inconnue.')
    else:
        raise error
        
@bot.command()
async def ticket(ctx):
    guild = ctx.guild
    ticket_category = discord.utils.get(guild.categories, name='Tickets')
    if not ticket_category:
        ticket_category = await guild.create_category(name='Tickets')
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
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
        overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
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

bot.run('MTA5NTk4NzQyMDU1NTY0NDk3OA.G5tyUZ.a8IqT23mOsad3oO31BNPGdYGka41WBVesub0Qg')
