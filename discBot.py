import discord
import os 
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv('.env')

BOT_TOKEN = os.getenv('token')
BOT_CHANNEL = 1126831550294675526
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix = '!', intents = intents)

mygroup = app_commands.Group(name='greetings', description='Welcomes users')
bot.tree.add_command(mygroup)

@mygroup.command(description='Pings user')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'ping {interaction.user.mention}! ')

@mygroup.command(description='Pongs user')
async def pong(interaction: discord.Interaction):
    await interaction.response.send_message(f'pong {interaction.user.mention}! ')

@bot.command()
async def cmdhelp(ctx):
    await ctx.send('Command List\n------------------------------\n/greetings ping: pong\n/greetings pong: ping\n!ping: pong\n!pong: ping\n!delete @(username): deletes last message of mentioned user')

@bot.command()
async def ping(ctx):
    mention = await ctx.send('pong')
    await ctx.message.add_reaction("🏓")

@bot.command()
async def pong(ctx):
    mention = await ctx.send('ping')
    await ctx.message.add_reaction("🏓")

@bot.command()
async def hello(lol):
    a = await lol.send()

@bot.command()
async def delete(ctx, user: discord.User    ):
    async for message in ctx.channel.history(limit=None):
        if message.author == user and message.id != ctx.message.id:
            await message.delete()
            break

@bot.tree.command(description='Greets User')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! ")

@bot.tree.command(description='Lists commands')
async def cmdhelp(interaction: discord.Interaction):
    await interaction.response.send_message("Command List\n------------------------------\n/greetings ping: pong\n/greetings pong: ping\n!ping: pong\n!pong: ping\n!delete @(username): deletes last message of mentioned user")

@bot.event
async def on_ready():
    channel = bot.get_channel(BOT_CHANNEL)
    #await channel.send("Hi! This is KoriBot! Type !cmdhelp for more info!")
    print("Bot is ready for use!")
    print("---------------------")
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} Command(s)')
    except Exception as e:
        print(e)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(BOT_CHANNEL)
    name = member.display_name
    pfp = member.display_avatar
    embed = discord.Embed(title='Welcome to this channel', description='This is really cool',colour=discord.Colour.random())
    embed.set_author(name='{}'.format(name))
    embed.set_thumbnail(url='{}'.format(pfp))
    embed.add_field(name='hi',value='bye')
    embed.set_footer(text='Hope you enjoy your time in this server!')
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(BOT_CHANNEL)
    await channel.send("Goodbye {}".format(member))

@bot.event
async def on_message(message):
    author = message.author
    content = message.content
    await bot.process_commands(message)
    print("{}: {}".format(author, content))

@bot.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    await channel.send("{} has deleted message: {}".format(author,content))

@bot.event
async def on_message_edit(before,after):
    if before.author == bot.user:
        return;
    author = before.author
    pfp = author.display_avatar
    channel = before.channel
    before_content = before.content
    after_content = after.content
    embed = discord.Embed(title='EDITED MESSAGE',colour = discord.Colour.random())
    embed.set_author(name="{}".format(author))
    embed.set_thumbnail(url='{}'.format(pfp))
    embed.add_field(name = 'Before:',value='{}'.format(before_content),inline=False)
    embed.add_field(name='After:', value='{}'.format(after_content))
    await channel.send(embed=embed)

@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    name = user.name
    emoji = reaction.emoji
    content = reaction.message.content
    await channel.send('{} has added {} to the message: {}'.format(name,emoji,content))

@bot.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    name = user.name
    emoji = reaction.emoji
    content = reaction.message.content
    await channel.send('{} has removed {} from the message: {}'.format(name,emoji,content))

bot.run(BOT_TOKEN)