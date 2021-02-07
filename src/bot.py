import os
import discord

from dotenv import load_dotenv
from datetime import datetime
from discord.ext import commands

#
# bot.py
#
# Author: Nigel Davis
# 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix='>')
client.remove_command('help')

#
# Events
#

@client.event 
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=None)
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} has connected to {guild.name} ({guild.id})')

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')    

#
# Commands
#

# ping command
@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')

# help command
@client.command(aliases=['h'])
async def help(ctx):
    em = discord.Embed(title='List of Commands')
    em.add_field(name='!help', value='shows a list of commands')
    await ctx.send(embed=em)

# purge command
@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount:int):
    if amount < 1:
        await ctx.send('Please specify an amount greater then zero.')
    else:
        await ctx.channel.purge(limit=amount+1)

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArguments):
        date = datetime.now().strftime('%d/%m/%Y %H:%M')
        print(f'{date}\tpurge error: not enough arguments.')

# echo command
@client.command()
@commands.has_permissions(manage_messages=True)
async def echo(ctx, *, message):
    await ctx.send(message)

@echo.error
async def echo_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        date = datetime.now().strftime('%d/%m/%Y %H:%M')
        print(f'{date}\techo error: not enough arguments.')

client.run(TOKEN)