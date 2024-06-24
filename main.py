import discord
from discord.ext import commands

import config as config


intents = discord.Intents().all()
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    for i in config.extensions:
        await client.load_extension(i)
        print(f'{i} - успешно загружен')
    print(f'\n\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}\n')
 


client.run(config.TOKEN, reconnect=True)