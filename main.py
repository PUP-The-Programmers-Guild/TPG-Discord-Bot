import discord
from discord.ext import commands
import os
import sqlite3
import csv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from keep_alive import keep_alive

# sets up intent that will be requested
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

# initializes the bot
client = commands.Bot(command_prefix="+", intents=intents)

def scheduled_message(msg):
  print("updated:", datetime.now().strftime("%H:%M:%S"))

@client.event
async def on_ready():
    await load()
    await client.change_presence(activity=discord.CustomActivity(name='Welcome to the Guild'))
    print(f"logged on as {client.user}")
    channel = client.get_channel(1143347614532767835)
    scheduler = BackgroundScheduler()
    job_id = scheduler.add_job(scheduled_message, "interval", hours=8, args= ["Hello"])
    scheduler.start()
    await channel.send("Im up")

@client.command()
async def compute_streak(ctx):
    time_record = {}
    point_record = {}
    channel = client.get_channel(1045330081175842887)
    print(channel)

    async for text in channel.history(limit=1000):
        time_stamp = text.created_at.strftime("%m/%d/%Y")
        if time_stamp > "08/13/2023" and time_stamp[6:] != "2022":
            user_name = text.author.id
            if user_name in time_record:
                print(f'time stamp: {time_stamp[3:5]} == {int(time_record[user_name][3:5]) - 1}')
                if int(time_stamp[3:5]) == int(time_record[user_name][3:5]) - 1:
                    point_record[user_name] += 1
                    time_record[user_name] = time_stamp
                    print("point_added")
                elif int(time_stamp[3:5]) != int(time_record[user_name][3:5]) - 1 and not (int(time_stamp[3:5]) == int(time_record[user_name][3:5])):
                    point_record[user_name] = 0
                    time_record[user_name] = time_stamp
                    print("point_resetted")
            elif user_name not in time_record:
                point_record[user_name] = 1
                time_record[user_name] = time_stamp
                print("not in record")
            print(f"{user_name} has {point_record[user_name]} during {time_record[user_name]}")
            print("-" * 30)

    conn = sqlite3.connect("database/100DOC.db")
    c = conn.cursor()
    for name, points in point_record.items():
      print("*" * 40)
      print(name, points)
      c.execute(f"""
                UPDATE Logs
                SET Streak_Count = {points}
                WHERE Discord_ID = {name}""")
    conn.commit()

@client.command()
async def update_db(ctx):
    print("hello")
    conn = sqlite3.connect("database/100DOC.db")
    c = conn.cursor()
    with open(r"cogs/database/log.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            c.execute(f"""
                      UPDATE Logs
                      SET
                          Log_Count = {row['Days']},
                          Date = '{row['Date']}'
                      WHERE Discord_ID = {row['Discord ID']}""")

            c.execute(f"""
                      UPDATE Users
                      SET Discord_ID = {row["Discord ID"]},
                        Discord_Name = '{row["Username"]}'
                      WHERE Discord_ID = {row["Discord ID"]}""")
    conn.commit()
    conn.close()
    print("Worked")
    await ctx.channel.send("Done")

@client.command()
async def notify_me(ctx, sched):
    conn = sqlite3.connect("database/100DOC.db")
    c = conn.cursor()

    c.execute(f"""
              INSERT INTO Notifications (Discord_ID, Scheduled_Time)
              VALUES ({ctx.author.id},
                      '{sched}')""")
    conn.commit()
    await ctx.channel.send("Done")

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
