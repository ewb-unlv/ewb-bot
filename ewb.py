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

@bot.command(aliases = ['hello', 'hey you', 'hey', 'oi'])
async def hi(ctx):
    await ctx.channel.send("henlo")

@bot.command()
async def bri(ctx):
    await ctx.channel.send(rtx.author.mention + " frick")

# admin commands
async def verify(ctx, roleName):
	role = get(ctx.message.guild.roles, name = roleName)

	if (role in ctx.author.roles):
		return True
	else:
		await ctx.channel.send("You do not have proper permissions to use that command!")
	return False

@bot.command()
async def create(ctx, message, message2, message3):
	if (await verify(ctx, "ewb bot")):
		await ctx.channel.send(message + " " + message2 + " " + message3)

bot.run(TOKEN)