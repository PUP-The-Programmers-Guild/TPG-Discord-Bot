import discord


def get_message_reactions(message):
    contents = message.content.split("\n")
    return {content[:3]: content[6:] for content in contents[1:]}


async def add_reactions(message):
    emojis = get_message_reactions(message).keys()

    for emoji in emojis:
        await message.add_reaction(emoji)


async def assign_role(emoji, user, message):
    contents = message.content.split("\n")
    print(contents)
    emojis = [content[:3] for content in contents[1:]]
    msg_roles = [content[7:] for content in contents[1:]]

    role_index = 0

    for index, msg_emoji in enumerate(emojis):
        print(msg_emoji)
        print(emoji)
        print(msg_emoji == emoji)
        if msg_emoji == emoji:
            role_index = index
    print(msg_roles[role_index])
    print(msg_roles[role_index] == 'Software Development')
    Role = discord.utils.get(user.guild.roles, name=msg_roles[role_index])
    print(Role)
    await user.add_roles(Role)


async def remove_role(emoji, user, message):
    contents = message.content.split("\n")
    print(contents)
    emojis = [content[:3] for content in contents[1:]]
    msg_roles = [content[7:] for content in contents[1:]]

    role_index = 0

    for index, msg_emoji in enumerate(emojis):
        print(msg_emoji)
        print(emoji)
        print(msg_emoji == emoji)
        if msg_emoji == emoji:
            role_index = index
    print(msg_roles[role_index])
    print(user)
    print(msg_roles[role_index] == 'Software Development')
    Role = discord.utils.get(user.guild.roles, name=msg_roles[role_index])
    await user.remove_roles(Role)
    print("role removed")
