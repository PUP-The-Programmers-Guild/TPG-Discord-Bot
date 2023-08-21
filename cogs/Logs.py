from discord.ext import commands
import csv
import os
from datetime import datetime


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
                await message.add_reaction("💚")
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
                await message.add_reaction("💚")
                print("new added emoji")

        channels = ['1045330081175842887', '1139959499193598002']

        right_channel = str(ctx.channel.id) in channels
        right_prefix = ctx.content.lower().startswith("day")
        bolded_prefix = ctx.content.lower().startswith("**day")
        if right_channel and (right_prefix or bolded_prefix):
            author = ctx.author
            user_id = author.id
            now = datetime.now().strftime("%m/%d/%Y")
            # message_id = ctx.id
            await log(str(author), str(user_id), str(now), ctx)
            print("it works")

    @commands.command()
    async def see_log(self, ctx):
        in_records = False
        days = 0
        with open(r"cogs/database/log.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row["Username"])
                if str(ctx.author.id) == row["Discord ID"]:
                    in_records = True
                    days = row['Days']
                    await ctx.channel.send(
                        f"{ctx.author.display_name} logged in: {days} days out of 100")
                    break
        if not in_records:
            await ctx.channel.send(
                    f"{ctx.author.display_name} is still not in the records")


async def setup(client):
    await client.add_cog(Logs(client))
