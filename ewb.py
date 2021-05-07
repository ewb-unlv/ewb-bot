import discord
import os
import json
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
    await ctx.channel.send(ctx.author.mention + " frick")

# admin commands
async def verify(ctx, roleName):
	role = get(ctx.message.guild.roles, name = roleName)

	if (role in ctx.author.roles):
		return True
	else:
		await ctx.channel.send("You do not have proper permissions to use that command!")
	return False

async def warn(ctx, msg):
	await ctx.channel.send(ctx.author.mention + " " + msg)

@bot.command()
async def create(ctx, *, json_message):
	if (await verify(ctx, "ewb bot")):
		try:
			json_object = json.loads(json_message)
		except:
			await warn(ctx, "Incorrect JSON format!")
			await warn(ctx, json_message)
			return

		# json object created
		try:
			heading = json_object["heading"]
		except:
			await warn(ctx, "No 'heading' provided!")
			return

		description = ""
		color = 0xABCDEF # did this as joke but it actually look good lol

		if "description" in json_object:
			description = json_object["description"]

		if "color" in json_object:
			color = int(json_object["color"], 16)

		hasRole = False
		hasReaction = False

		if "roles" in json_object:
			hasRole = True
		
		if "reactions" in json_object:
			hasReaction = True

		if (hasRole and not hasReaction) or (hasReaction and not hasRole):
			await warn(ctx, "Roles and reactions must be equal!")
			return
		elif (hasRole and hasReaction):
			if (len(json_object["roles"]) != len(json_object["reactions"])):
				await warn(ctx, "Roles and reactions must be equal!")
				return

			# check that all roles exist
			roleCount = 0
			for roleName in json_object["roles"]:
				role = get(ctx.message.guild.roles, name = roleName)

				if not role:
					await warn(ctx, "Role '" + roleName + "' does not exist in this server!")
					return

				description = description + "\n" + json_object["reactions"][roleCount] + " = " + roleName

				roleCount = roleCount + 1
		# put roles in description

		# add reactions

		embed_object = discord.Embed(
			title = heading,
			description = description,
			color = color,
		)

		ref = await ctx.send(embed = embed_object)

		if (ref):
			await ctx.message.delete()

		for emoji in json_object["reactions"]:
			try:
				await ref.add_reaction(emoji)
			except:
				try:
					#emoji_token = get(ctx.guild.emojis, name = emoji)
					emoji_token = bot.get_emoji(id = emoji)
					await ref.add_reaction(emoji_token)
				except:
					await warn(ctx, "Some of those emojis are not allowed!")
					return
bot.run(TOKEN)