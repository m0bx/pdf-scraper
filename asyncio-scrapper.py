import json, asyncio, aiohttp
from bs4 import BeautifulSoup


def load_json(filename, settings):
	try:
		file = open(str(filename) + '.json', 'r+')
	except FileNotFoundError:
		print("Error parsing " + str(filename) + ".json file contents, repairing or creating " + str(filename) + ".json.")
		file = open("config.json", 'w')
		json.dump(settings, file)
		file.close()
		file = open("config.json", 'r+')

	contents = json.load(file)
	return contents


def clear_indexed():
	boolean_indexed = input("Do you want to erase indexed before you start the process? y/n \n")
	if boolean_indexed == "y":
		try:
			open("indexed.json", "w").close()
		except FileNotFoundError:
			print("You dont even have indexed file setup yet ...")
	elif boolean_indexed != "n":
		exit()


if __name__ == "__main__":
	# Code to clear indexed file
	clear_indexed()
	# Code to handle config.json, and to load config files
	config_setup = {"depth": 2, "start": ['https://pdfix.net']}
	config = load_json("config", config_setup)

	depth = config["depth"]
	starter_urls, urls = config["start"]
	print("Loaded configs; depth:" + str(depth) + ", starting urls: " + str(starter_urls))
	# Code to handle indexed URLs database
	indexed_setup = {}
	indexed_urls = []
	indexed_json = load_json("indexed", indexed_setup)


	# PDFs file
	try:
		pdfs = open("pdfs.txt", "r+")
	except FileNotFoundError:
		print("PDFs database does not exist. Creating a new file...")
		pdfs = open("pdfs.txt", 'a+')
		pdfs.close()
		pdfs = open("pdfs.txt", 'r+')

	# Sets up headers for the request
	default_headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
