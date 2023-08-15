import discord
import csv
import os
from datetime import datetime
from discord.utils import get
from keep_alive import keep_alive
from help import help

# sets up intent that will be requested
intents = discord.Intents.default()
intents.message_content = True

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

    # checks if its the right time then add it to the csv
    with open(path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if user_id == row["Discord ID"]:
                new = False
                current = datetime.now().strftime("%m/%d/%Y")
                if int(current[3:5]) != int(row["Date"][3:5]):
                    is_time = True
                    row["Date"] = datetime.now().strftime("%m/%d/%Y")
                    row["Days"] = int(row["Days"]) + 1
                    await message.add_reaction("💚")
                updated_row.append(row)
        print(updated_row)

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




keep_alive()
client.run(os.environ['TOKEN'])
