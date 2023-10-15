from plyer import notification

from scripts.button import Buttoner

class Dev:
	GUILD_ID = 859700213962768405
	CHANNEL_ID = 859700214411427841
	BOT_ID = 364598887824097280

class Main:
	GUILD_ID = 1069900680229289994
	CHANNEL_ID = 1143706578541887488
	BOT_ID = 999736048596816014

settings = Dev

def check_message(bot,m):
	if m['guild_id'] != str(settings.GUILD_ID):
		return 1

	if m['channel_id'] != str(settings.CHANNEL_ID):
		return 2

	if m['author']['id'] != str(settings.BOT_ID):
		return 3

	if "A wild countryball appeared!" not in m['content']:
		return 4

	notification.notify(title="Balls Bot", message="New Countryball Dropped!", app_icon=None, timeout=5)

	if len(m["components"]) < 1:
		return 5

	buttons = Buttoner(m["components"])

	button = buttons.getButton(label="Catch me!")

	bot.click(
		m["author"]["id"],
		channelID=m["channel_id"],
		guildID=m["guild_id"],
		messageID=m["id"],
		messageFlags=m["flags"],
		data=button,
	)