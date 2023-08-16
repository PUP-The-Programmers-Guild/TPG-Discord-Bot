import discord
import csv
import os
from datetime import datetime
from discord.utils import get
from keep_alive import keep_alive
from help import help
import reactions

# sets up intent that will be requested
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

# initializes the bot
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f"logged on as {client.user}")


@client.event
async def on_message(message):
  async def log(author, user_id, time, message):
    fieldnames = ["Discord ID", "Username", "Date", "Days"]
    path = r"database/log.csv"
    is_time = False
    new = True
    updated_row = []

    # creates the path
    if not os.path.exists(path):
      with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

    worked = False
    # checks if its the right time then add it to the csv
    with open(path, "r", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if user_id == row["Discord ID"]:
                new = False
                current = datetime.now().strftime("%m/%d/%Y")
                if int(current[3:5]) != int(row["Date"][3:5]):
                    is_time = True
                    row["Date"] = datetime.now().strftime("%m/%d/%Y")
                    row["Days"] = int(row["Days"]) + 1
                    worked = True  
            updated_row.append(row)
        print(updated_row)

    if worked:
      await message.add_reaction("💚")
      print("added emoji")
    if is_time:
      with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_row)
    if new:
      with open(path, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({
            "Discord ID": str(user_id),
            "Username": str(author),
            "Date": str(time),
            "Days": 1
        })
        await message.add_reaction("💚")

  if message.author == client.user:
    return

  print(
      f"Message from {message.author}: {message.content} in {message.channel}")

  channels = ['1045330081175842887', '1139959499193598002']

  right_channel = str(message.channel.id) in channels
  right_prefix = message.content.lower().startswith("day")
  bolded_prefix = message.content.lower().startswith("**day")
  if right_channel and (right_prefix or bolded_prefix):
    author = message.author
    user_id = author.id
    now = datetime.now().strftime("%m/%d/%Y")
    message_id = message.id
    await log(str(author), str(user_id), str(now), message)
    print("it works")

  if message.channel.id in [1140322273753047070, 1025693891065827338]:
    contents = reactions.get_message_reactions(message)
    for emoji, equivalent in contents.items():
      print(f"emoji: {emoji}\nequivalent: {equivalent}")
    await reactions.add_reactions(message)

  # list of commands
  if message.content.startswith("+"):
    if message.content[1:] == "see_roles":
      options = ["participant"]
      for role in message.author.roles:
        role = str(role)
        if role in options:
          await message.channel.send(f"roles: {role}")
    elif message.content[1:] == "see_log":
      in_records = False
      with open(r"database/log.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
          print(row)
          if str(message.author.id) == row["Discord ID"]:
            in_records = True
            await message.channel.send(
                f"{message.author} logged in: {row['Days']} days out of 100")
      if not in_records:
        await message.channel.send(
                f"{message.author} is still not in the records")
    elif message.content[1:] == "help":
        await message.channel.send(help())
    elif message.content[1:] == "reactions":
      channel = client.get_channel(1025693891065827338)
      reacted = await channel.fetch_message(1026515967330750464)
      contents = reacted.content.split("\n")
      for content in contents[1:]:
        print(content[0:5])
        print(content[6:])
    elif message.content[1:] == "see_emoji":
      await message.add_reaction("💚")
      await message.add_reaction("💚")

@client.event
async def on_raw_reaction_add(reaction):
  if reaction.channel_id in [1140322273753047070, 1025693891065827338]:
    channel = client.get_channel(reaction.channel_id)
    user = reaction.member
    message = await channel.fetch_message(reaction.message_id)
    emoji = str(reaction.emoji)
    print("emoji name", reaction.emoji.name)
    print(emoji)
    print(user)
    print(message)
    await reactions.assign_role(emoji, user, message)

@client.event
async def on_raw_reaction_remove(reaction):
  if reaction.channel_id in [1140322273753047070, 1025693891065827338]:
    channel = client.get_channel(reaction.channel_id)
    print(channel)
    message = await channel.fetch_message(reaction.message_id)
    print(message)
    guild = client.get_guild(reaction.guild_id) 
    print(guild)
    user = await guild.fetch_member(reaction.user_id)
    emoji = str(reaction.emoji)
    print("emoji name", reaction.emoji.name)
    print(emoji)
    print(user)
    print(reaction.user_id)
    print(message)
    await reactions.remove_role(emoji, user, message)


keep_alive()
client.run(os.environ['TOKEN'])
