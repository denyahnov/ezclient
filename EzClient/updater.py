import os
import requests

github_url = r"https://raw.githubusercontent.com/denyahnov/ezclient/main/EzClient/"

def ReadDirectory(path="."):
	files = {}
	
	for file in os.listdir(path):
		tmp = os.path.join(path,file).replace(".\\","")

		if os.path.isdir(tmp):
			files[tmp] = ReadDirectory(tmp)
		elif tmp.endswith(".py"):
			with open(tmp,"rb") as f:
				files[tmp] = f.read().decode("utf-8").replace("\r\n","\n")

	return files

def CompareData(directory):
	for path, data in directory.items(): 
		
		if type(data) != str:
			CompareData(data)

			continue

		file_url = github_url + path.replace("\\","/")

		response = requests.get(file_url)

		if response.status_code != 200:
			print("[!] < FileNotFoundError > -> {}".format(file_url))

			continue

		file_content = response.text.replace("\r\n","\n")

		if data != file_content:

			with open(path,"w") as file:
				file.write(file_content)

			print("[+] '{}' Updated!".format(path))

CompareData(ReadDirectory())