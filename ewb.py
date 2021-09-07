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

async def attempt_add_reaction(ref, reactions_object, ctx):
	for emoji in reactions_object:
		try:
			await ref.add_reaction(emoji)
		except:
			try:
				emoji_token = bot.get_emoji(id = emoji)
				await ref.add_reaction(emoji_token)
			except:
				await warn(ctx, "Some of those emojis are not allowed!")
				return

# TODO(dillon): If this bot scales larger, this command should also search through a "guild" list
# so we can avoid searching through all active_messages in every server each time we run this event.
# This could also be used to potentially throttle servers with too many reaction listeners if necessary.

# Messages with active listeners for emoji reactions
active_messages = []

# Keyed by message_id = []
reaction_list = {}
role_list = {}

async def validate_reaction(message_to_check, user):
	for message in active_messages:
		if (message_to_check == message):
			if (bot.user == user):
				return True
	return False

@bot.event
async def on_raw_reaction_add(payload):
	roleIndex = 0
	for message in active_messages:
 		if (payload.message_id == message.id):
 			for reaction_emoji in reaction_list[payload.message_id]:
 				if ((bot.user.id != payload.user_id) and (payload.emoji.name == reaction_emoji)):
 					role = get(payload.member.guild.roles, name=role_list[payload.message_id][roleIndex])
 					await payload.member.add_roles(role)

 				roleIndex += 1

@bot.event
async def on_raw_reaction_remove(payload):
	roleIndex = 0
	for message in active_messages:
 		if (payload.message_id == message.id):
 			for reaction_emoji in reaction_list[payload.message_id]:
 				if ((bot.user.id != payload.user_id) and (payload.emoji.name == reaction_emoji)):
 					curr_guild = bot.get_guild(payload.guild_id)
 					member = curr_guild.get_member(payload.user_id)
 					role = get(member.guild.roles, name=role_list[payload.message_id][roleIndex])
 					await member.remove_roles(role)

 				roleIndex += 1

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

				# put roles in description
				description = description + "\n" + json_object["reactions"][roleCount] + " = " + roleName

				roleCount = roleCount + 1

		embed_object = discord.Embed(
			title = heading,
			description = description,
			color = color,
		)

		ref = await ctx.send(embed = embed_object)

		if (ref):
			await ctx.message.delete()

		# No need to listen if the message isn't meant for reacting
		if (hasRole and hasReaction):
			active_messages.append(ref)

			reaction_emoji_list = []

			for reaction_emoji in json_object["reactions"]:
				reaction_emoji_list.append(reaction_emoji)

			reaction_list[ref.id] = reaction_emoji_list

			raw_role_list = []

			for role in json_object["roles"]:
				raw_role_list.append(role)

			role_list[ref.id] = raw_role_list

			# adds reactions to message (aka ref)
			await attempt_add_reaction(ref, json_object["reactions"], ctx)
		
bot.run(TOKEN)