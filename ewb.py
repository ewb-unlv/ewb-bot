import discord
import os
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='^', intents = intents)

@bot.event
async def on_ready():
    print("EWB Client has connected :D")

@bot.event
async def on_member_join(member):
	role = get(member.guild.roles, name="EWB Members")
	await member.add_roles(role)

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
