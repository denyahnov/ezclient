




#####################################
### EDIT THESE TO CHANGE SETTINGS ###

NOTIFICATIONS = { 			# Send desktop notification when cooldown ends
	"Claim": 		False,
	"Daily": 		False,
	"Drop": 		False,
	"Vote": 		False,
	"Challenge": 	False,
}

AUTOMATE = {				# Automatically respond to the command
	"Claim": 		True,
	"Daily": 		True,
	"Drop": 		False,
	"Vote": 		False,
	"Challenge": 	False,
}

DROP_PRIORITIES = [ 		# What card rarity you want picked in descending order
	"One of a Kind",
	"Future Star",
	"Champion",
	"Exclusive",
	"Historic",
	"Special",
	"Rare",
	"Uncommon",
	"Common",
	"Very Common",
]

#####################################
#####################################










# from scripts.button import Buttoner

from plyer import notification

from threading import Thread

import os
import io
import random
import requests
from PIL import Image, ImageDraw
from string import ascii_uppercase
from time import sleep, gmtime, strftime

# import pytesseract

# pytesseract.pytesseract.tesseract_cmd = os.path.join(os.getenv("PROGRAMFILES"),"Tesseract-OCR","tesseract")

class settings:
	GUILD_ID = 1146260269643862059
	CHANNEL_ID = 1158523905162625075
	BOT_ID = 785719830640328704
	# BOT_ID = 976067627711606784 # Test
	USER_ID = 364598887824097280

class Variables:
	WaitDelay = 5
	UpdateDelay = 200
	CommandDelay = 0.2

	BOT = None
	LISTENING = False
	UPDATE_MESSAGE = None
	LAST_UPDATE = None

class Command:
	bDrop = "=d"
	bVote = "=vote"
	bClaim = "=claim"
	bDaily = "=daily"
	bCooldown = "=cd"

	LISTEN = "=listen"

def Notify(message):
	notification.notify(
		title="Basketball Bot", 
		message=message, 
		app_icon="favicon.ico", 
		timeout=3
	)

def ThrowError(title,error):
	print("[!] <{}> -> {}".format(title,error))

def DropPick(m):
	return 69

	if not AUTOMATE["Drop"]:
		return 1

	if len(m["attachments"]) == 0:
		return 2

	def strip_name(string):
		return " ".join(a for a in ["".join([w for w in word if w in ascii_uppercase]) for word in string.split(" ") if len(word) > 0] if a != "")

	def round_color(rgba):
		return [15 * ((value - 1) // 15) for value in rgba[:-1]]

	def get_rarity(color):
		try:
			return {

				"[120, 105, -15]": 	"Champion",
				"[120, 105, 0]": 	"Champion",
				"[225, 90, 240]": 	"Future Star",
				"[225, 105, 240]": 	"Future Star",
				"[-15, 105, 120]": 	"Historic",
				"[0, 105, 120]": 	"Historic",
				"[180, 75, 180]": 	"Exclusive",
				"[150, -15, 105]": 	"Special",
				"[135, -15, 105]": 	"Special",
				"[135, -15, 90]": 	"Special",
				"[135, 0, 105]": 	"Special",
				"[150, 0, 105]": 	"Special",
				"[15, 60, 240]": 	"Rare",
				"[30, 75, 240]": 	"Rare",
				"[30, 90, 240]": 	"Rare",
				"[15, 90, 0]": 		"Uncommon",
				"[60, 120, 30]": 	"Common",
				"[75, 120, 30]": 	"Common",
				"[60, 60, 60]": 	"Very Common",

			}[str(round_color(color))] 
		except KeyError:
			raise Exception("Unknown Color -> {}".format(round_color(color)))

	response = requests.get(m["attachments"][0]["url"])

	image = Image.open(io.BytesIO(response.content))

	tx,ty,w,h = image.getbbox()

	cards = [image.crop(box=[30 + i * (w // 3), 9, (i + 1) * (w // 3), 46]) for i in range(3)]

	card_names = [strip_name(pytesseract.image_to_string(card)) for card in cards]

	x,y = 15,10

	rarities = [get_rarity(card.getdata()[x + (y * card.getbbox()[2])]) for card in cards]

	priorities = sorted([(DROP_PRIORITIES.index(rarity),i) for i,rarity in enumerate(rarities)],key=lambda x: x[0])

	priority,chosen = priorities[0]

	print("[+] Detected Drop:\n" + "\n".join(["\t{}.\t{} - {}".format(i+1,rarities[i],card.title()) for i,card in enumerate(card_names)]))

	buts = Buttoner(m["components"])

	emojis = [":one:", ":two:", ":three:"]

	# Variables.BOT.click(
	# 	m["author"]["id"],
	# 	channelID=m["channel_id"],
	# 	guildID=m["guild_id"],
	# 	messageID=m["id"],
	# 	messageFlags=m["flags"],
	# 	data=buts.getButton(emojiName=emojis[chosen]),
	# )

	print("todo: add bot click button")

	print("[>] Grabbed Player {} -> {} - {} (Priority {})".format(chosen+1,rarities[chosen],card_names[chosen].title(),priority + 1))

	return 0

def DecodeUpdateMessage(string):
	emojis = [":closed_lock_with_key:", ":lock:"]

	remove = [" ", "`"]

	key_split = "·"

	ready = "ready"

	for item in emojis + remove:
		string = string.replace(item,'')

	return {line.split(key_split)[0]: line.split(key_split)[-1] == ready for line in string.split("\n")}

def __main_thread__():
	while Variables.LISTENING:
		try:

			Variables.BOT.sendMessage(str(settings.CHANNEL_ID),Command.bCooldown)

			sleep(random.uniform(Variables.WaitDelay * 0.9, Variables.WaitDelay * 1.1))

			cooldowns = DecodeUpdateMessage(Variables.UPDATE_MESSAGE["embeds"][0]["description"])

			if Variables.LAST_UPDATE == None:
				Variables.LAST_UPDATE = {key: False for key in cooldowns}

			if cooldowns["Claim"] and not Variables.LAST_UPDATE["Claim"]:
				if AUTOMATE["Claim"]: Variables.BOT.sendMessage(str(settings.CHANNEL_ID),Command.bClaim)
				
				if NOTIFICATIONS["Claim"]: Notify("Claimed Free Coins!")

			sleep(random.uniform(Variables.CommandDelay * 0.9, Variables.CommandDelay * 1.1))

			if cooldowns["DropPick"] and not Variables.LAST_UPDATE["DropPick"]:
				if AUTOMATE["Drop"]: Variables.BOT.sendMessage(str(settings.CHANNEL_ID),Command.bDrop)

				if NOTIFICATIONS["Drop"]: Notify("New Drop Available!")

			sleep(random.uniform(Variables.CommandDelay * 0.9, Variables.CommandDelay * 1.1))
			
			if cooldowns["Challenge"] and not Variables.LAST_UPDATE["Challenge"]:
				if NOTIFICATIONS["Challenge"]: Notify("Play Challenge Available!")

			sleep(random.uniform(Variables.CommandDelay * 0.9, Variables.CommandDelay * 1.1))
			
			if cooldowns["Daily"] and not Variables.LAST_UPDATE["Daily"]:
				if AUTOMATE["Daily"]: Variables.BOT.sendMessage(str(settings.CHANNEL_ID),Command.bDaily)
				
				if NOTIFICATIONS["Daily"]: Notify("Claimed Daily Rewards!")

			sleep(random.uniform(Variables.CommandDelay * 0.9, Variables.CommandDelay * 1.1))
			
			if cooldowns["Top.ggvote"] and not Variables.LAST_UPDATE["Top.ggvote"]:
				if NOTIFICATIONS["Vote"]: Notify("Top.GG Vote Available!")

			sleep(random.uniform(Variables.CommandDelay * 0.9, Variables.CommandDelay * 1.1))
			
			if cooldowns["Diffcordvote"] and not Variables.LAST_UPDATE["Diffcordvote"]:
				if NOTIFICATIONS["Vote"]: Notify("Diffcord Vote Available!")

			sleep(random.uniform(Variables.CommandDelay * 0.9, Variables.CommandDelay * 1.1))

			if AUTOMATE["Vote"] and ((cooldowns["Top.ggvote"] and not Variables.LAST_UPDATE["Top.ggvote"])\
			or cooldowns["Diffcordvote"] and not Variables.LAST_UPDATE["Diffcordvote"]):
				Variables.BOT.sendMessage(str(settings.CHANNEL_ID),Command.bVote)

			Variables.LAST_UPDATE = cooldowns

			sleep(random.uniform(Variables.UpdateDelay * 0.9, Variables.UpdateDelay * 1.1))

		except Exception as error:
			ThrowError("scripts.basketball.Listen", error)
			sleep(5)

def Start():
	thread = Thread(target=__main_thread__)
	thread.daemon = True
	thread.start()

def ToggleListen(bot,m):
	Variables.LISTENING = not Variables.LISTENING

	Notify("Basketball Dropper {}!".format("Listening" if Variables.LISTENING else "Stopped"))

	if Variables.LISTENING:
		Start()

def check_message(bot,m):
	if Variables.BOT == None: Variables.BOT = bot

	# if 'guild_id' not in m:
	# 	return 0

	# if m['guild_id'] != str(settings.GUILD_ID):
	# 	return 1

	# if m['channel_id'] != str(settings.CHANNEL_ID):
	# 	return 2

	if "author" not in m:
		return 0

	### BOT HANDLER ###
	if m['author']['id'] == str(settings.BOT_ID):
		if "message_reference" in m: 						# Message is a reply
			if bot.user_data['id'] in m["content"]:			# Author is mentioned
				if "pick between" in m["content"].lower():	# Drop pick response
					DropPick(m)

		if len(m["embeds"]) == 1:
			if "title" in m["embeds"][0] and "Cooldowns" in m["embeds"][0]["title"] and bot.user_data['username'] in m["embeds"][0]["title"]:
				Variables.UPDATE_MESSAGE = m

				print(strftime("[%H:%M:%S] Updated Cooldowns", gmtime()))

	### USER HANDLER ###
	elif m['author']['id'] == bot.user_data['id']:

		if m['content'].startswith(Command.LISTEN):
			settings.CHANNEL_ID = int(m["channel_id"])

			ToggleListen(bot,m)

	

	else:
		return 3