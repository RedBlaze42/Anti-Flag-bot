import discord

bot=discord.Client()
with open("flag_list.txt","r") as flag_file:
    flag_database=list()
    for line in flag_file.read().split("\n"):
        if len(line)>=2:
            flag_database.append(line[0:2])

@bot.event
async def on_ready():
    print("The bot is ready !")

def is_flag(emoji):
    if isinstance(emoji, str):
        emoji_name=emoji
    else:
        emoji_name=emoji.name
    return emoji_name in flag_database

async def remove_flags(message):    
    reactions=message.reactions
    for reaction in reactions:
        if is_flag(reaction.emoji):
            users = await reaction.users().flatten()
            for user in users:
                await reaction.remove(user)

@bot.event
async def on_raw_reaction_add(payload):
    guild, emoji = bot.get_guild(payload.guild_id), payload.emoji
    message=await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if guild is not None:
        await remove_flags(message)  
            

bot.run("some secret token")
