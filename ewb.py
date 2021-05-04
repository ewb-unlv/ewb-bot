import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='^')


@bot.event
async def on_ready():
    print("ewb will save the world")


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
