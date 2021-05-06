import discord
import os
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents = intents)

bot = commands.Bot(command_prefix='^')


@bot.event
async def on_ready():
    print("ewb will save the world")
    print(get(bot.guilds[0].roles, name="EWB Members"))
    print(intents.members)

@client.event
async def on_member_join(member):
	print("SOMEONE JOINED")
	#print(get(member.guild.roles, name = "EWB Members"))
	#role = get(member.guild.roles, name="EWB Members")
	#await member.add_roles(role)
	await member.channel.send("test")

@bot.command()
async def hi(ctx):
    await ctx.channel.send("henlo")


@bot.command()
async def ping(reallylongvariablename):
    await reallylongvariablename.channel.send("pong")


@bot.command()
async def bri(rtx):
    await rtx.channel.send(rtx.author.mention + " frick")

bot.run(TOKEN)
