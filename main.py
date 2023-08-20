import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

# sets up intent that will be requested
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

# initializes the bot
client = commands.Bot(command_prefix="+", intents=intents)


@client.event
async def on_ready():
    await load()
    await client.change_presence(activity=discord.CustomActivity(name='Welcome to the Guild'))
    print(f"logged on as {client.user}")

initial_extensions = [
    f"cogs.{filename[:-3]}"
    for filename in os.listdir("./cogs")
    if filename.endswith(".py")
]


async def load():
    for extension in initial_extensions:
        print(extension)
        await client.load_extension(extension)

keep_alive()
client.run(os.environ['TOKEN'])
