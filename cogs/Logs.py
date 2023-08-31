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
        channels = ['1045330081175842887', '1139959499193598002']

        right_channel = str(ctx.channel.id) in channels
        right_prefix = ctx.content.lower().startswith("day")
        bolded_prefix = ctx.content.lower().startswith("**day")
        if right_channel and (right_prefix or bolded_prefix):
            author = ctx.author
            user_id = author.id
            time = datetime.now().strftime("%m/%d/%Y")

            conn = sqlite3.connect("database/100DOC.db")
            c = conn.cursor()

            c.execute(f"""
              SELECT Discord_Name, Date, Streak_Count
              FROM Logs l INNER JOIN Users u
                ON l.Discord_ID = u.Discord_ID
              WHERE Discord_Name = '{author}'
              """)
            user = c.fetchall()
            print(user)

            yesterday = (datetime.now() - timedelta(1)).strftime("%m/%d/%Y")
            streak = user[0][2] + 1 if user[0][1] == yesterday else 1
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
                        INSERT INTO Users
                        VALUES (
                            {user_id},
                            '{author}')""")
                conn.commit()
                c.execute(f"""
                INSERT INTO Logs (Discord_ID, Log_Count, Date, Streak, Streak_Count)
                VALUES (
                    {user_id},
                    0,
                    '{time}',
                    0,
                    1)""")
                conn.commit()
                await ctx.add_reaction("💚")
            print("it works")

    @commands.command()
    async def see_log(self, ctx):
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
        else:
            await channel.send(f"{ctx.author.display_name} is still not in the records")

async def setup(client):
    await client.add_cog(Logs(client))
