import discord
from discord.ext.commands import Bot

import os
import random

bot = Bot("=",intents=discord.Intents.all())

with open("bot_token.pyc","r") as file:
	BOT_TOKEN = file.read()

@bot.event
async def on_ready():
	print("ready")

@bot.command()
async def d(ctx):
	image = os.path.join("images", random.choice(os.listdir("images")))

	message = "{} Pick between these `3` by clicking their corresponding buttons.".format(ctx.author.mention)

	await ctx.reply(message,file=discord.File(image))

bot.run(BOT_TOKEN)