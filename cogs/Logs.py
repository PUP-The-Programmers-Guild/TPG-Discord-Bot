from discord.ext import commands
import csv
import os
from datetime import datetime, timedelta
import csv
import sqlite3

from discord.utils import time_snowflake

class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        async def log(author, user_id, time, message):
            fieldnames = ["Discord ID", "Username", "Date", "Days"]
            PATH = r"cogs/database/log.csv"
            is_time = False
            new = True
            updated_row = []

            # creates the PATH
            if not os.path.exists(PATH):
                with open(PATH, "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()

            worked = False
            # checks if its the right time then add it to the csv
            with open(PATH, "r", newline='') as file:
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
                # await message.add_reaction("💚")
                print("added emoji")
            if is_time:
                with open(PATH, "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(updated_row)
            if new:
                with open(PATH, "a", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writerow({
                        "Discord ID": str(user_id),
                        "Username": str(author),
                        "Date": str(time),
                        "Days": 1
                    })
                # await message.add_reaction("💚")
                print("new added emoji")

        channels = ['1045330081175842887', '1139959499193598002']

        right_channel = str(ctx.channel.id) in channels
        right_prefix = ctx.content.lower().startswith("day")
        bolded_prefix = ctx.content.lower().startswith("**day")
        if right_channel and (right_prefix or bolded_prefix):
            author = ctx.author
            user_id = author.id
            time = datetime.now().strftime("%m/%d/%Y")
            # message_id = ctx.id
            await log(str(author), str(user_id), str(time), ctx)

            # sql implementation
            conn = sqlite3.connect("database/100DOC.db")
            c = conn.cursor()

            c.execute(f"""
              SELECT Discord_Name, Date, Streak_Count
              FROM Logs l INNER JOIN Users u
                ON l.Discord_ID = u.Discord_ID
              WHERE Discord_Name = '{author}'
              """)
            user = c.fetchall()
            streak = 0
            print(user)

            yesterday = (datetime.now() - timedelta(1)).strftime("%m/%d/%Y")
            if user[0][1] == yesterday:
                streak = user[0][2] + 1
            if user and user[0][1] != time:
                c.execute(f"""
                        UPDATE Logs
                        SET Log_Count = Log_Count + 1,
                        Date = '{time}',
                        Streak_Count = {streak}
                        WHERE Discord_ID = {user_id}""")
                conn.commit()
                await ctx.add_reaction("💚")
            elif not user:
                c.execute(f"""
                INSERT INTO Logs (Discord_ID, Log_Count, Date, Streak, Streak_Count)
                VALUES (
                    {user_id},
                    0,
                    '{time}',
                    0,
                    1)""")
                conn.commit()
                c.execute(f"""
                        INSERT INTO Users
                        VALUES (
                            {user_id},
                            '{author}')""")
                conn.commit()
                await ctx.add_reaction("💚")
            print("it works")

    @commands.command()
    async def see_log(self, ctx):
        # in_records = False
        # days = 0
        # with open(r"cogs/database/log.csv", "r") as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         print(row["Username"])
        #         if str(ctx.author.id) == row["Discord ID"]:
        #             in_records = True
        #             days = row['Days']
        #             await ctx.channel.send(
        #                 f"{ctx.author.display_name} logged in: {days} days out of 100")
        #             break
        # if not in_records:
        #     await ctx.channel.send(f"{ctx.author.display_name} is still not in the records")

        # sql implementation
        channel = self.client.get_channel(1139959499193598002)
        conn = sqlite3.connect("database/100DOC.db")
        c = conn.cursor()
        c.execute(f"""
                  SELECT Log_Count
                  FROM Logs
                  WHERE Discord_ID = {ctx.author.id}""")
        log_amount = c.fetchone()

        if log_amount is not None:
            await ctx.channel.send(f"{ctx.author.display_name} logged in: {log_amount[0]} days out of 100")
        else:
            await ctx.channel.send(f"{ctx.author.display_name} is still not in the records")

    @commands.command()
    async def db_see_log(self, ctx):
      channel = self.client.get_channel(1045330081175842887)
      conn = sqlite3.connect("database/100DOC.db")
      c = conn.cursor()
      c.execute(f"""
                SELECT Log_Count
                FROM Logs
                WHERE Discord_ID = {ctx.author.id}""")
      log_amount = c.fetchone()

      if log_amount is not None:
        await channel.send(f"{ctx.author.display_name} logged in: {days} days out of 100")
      elif log_amount is None:
        await channel.send(f"{ctx.author.display_name} is still not in the records")

async def setup(client):
    await client.add_cog(Logs(client))
