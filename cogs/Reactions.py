from discord.ext import commands
import reactions
import sys

sys.path.insert(0, "../")


class Reactions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.channel.id in [1140322273753047070, 1025693891065827338]:
            await reactions.add_reactions(ctx)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if reaction.channel_id in [1140322273753047070, 1025693891065827338]:
            channel = self.client.get_channel(reaction.channel_id)
            user = reaction.member
            message = await channel.fetch_message(reaction.message_id)
            emoji = str(reaction.emoji)
            await reactions.assign_role(emoji, user, message)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        if reaction.channel_id in [1140322273753047070, 1025693891065827338]:
            channel = self.client.get_channel(reaction.channel_id)
            message = await channel.fetch_message(reaction.message_id)
            guild = self.client.get_guild(reaction.guild_id)
            user = await guild.fetch_member(reaction.user_id)
            emoji = str(reaction.emoji)

            await reactions.remove_role(emoji, user, message)


async def setup(client):
    await client.add_cog(Reactions(client))
