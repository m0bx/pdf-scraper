import json, asyncio, aiohttp, os
from bs4 import BeautifulSoup


########################################################################################################################

def load_json(filename, settings):
	try:
		file = open(str(filename) + '.json', 'r+')
	except FileNotFoundError:
		print(
			"Error parsing " + str(filename) + ".json file contents, repairing or creating " + str(filename) + ".json.")
		file = open("config.json", 'w')
		json.dump(settings, file)
		file.close()
		file = open("config.json", 'r+')

	contents = json.load(file)
	return contents


def update_json_value(file_path, key, new_values):
	with open(file_path, 'r') as f:
		data = json.load(f)
	data[key].append(values for values in new_values)
	with open(file_path, 'w') as f:
		if data is not None:
			json.dump(data, f)


########################################################################################################################

# Fetches and returns the whole response text with the aiohttp.ClientSession() session.
async def fetch(session, url):
	try:
		async with session.get(url, headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}) as response:
			return await response.text()
	except Exception:
		print("Error " + response.status + "  ...  " + str(url))


# Part of the fetch code, gathers html data as a response from the fun above.
async def fetch_and_extract_links(url):
	async with aiohttp.ClientSession() as session:
		html = await fetch(session, url)
		soup = BeautifulSoup(html, 'html.parser')
		links = [link.get('href') for link in soup.find_all('a')]
		return links


# Main module that controls the whole requests part. urls should probably be an array for guaranteed functionality,
# since json file formatting can be tricky at times.
async def fetch_and_extract_links_multiple(urls):
	async with aiohttp.ClientSession() as session:
		tasks = []
		for url in urls:
			# This is the task that async will run asynchronously
			task = asyncio.ensure_future(fetch_and_extract_links(url))
			# Appends fetch_and_extract_links's response, which in this case is links array. The array becomes 2 dimensional
			tasks.append(task)
		print("success  ...  " + str(url))
		await asyncio.sleep(0.1)  # Timeout between requests. Higher this if you are expecting rate limiting.
		responses = await asyncio.gather(*tasks)  # Gather all (*) tasks when tasks are "released"
		# Since responses is 2d array, we need to make 2 for cycles to gather 2nd layer data:
		links = [link for sublist in responses for link in sublist]
		return links  # Returns links (damn), it is an array of all gathered links from all the urls given


# Now using asyncio.run(fetch_and_extract_links_multiple(urls)) the process will start for given urls (should)

if __name__ == "__main__":
	# Code to clear indexed file


	# Code to handle config.json, and to load config files
	depth = 2
	urls = [""]
	print("Starting with depth:" + str(depth))

	# PDFs file
	pdfs_txt = open("pdfs.txt", "a+")  # a+ is for appending at the end, file will be created if it doesn't exist
	pdfs_temp = []
	# Code to handle indexed URLs database
	indexed_urls = []
	indexed_database = open("indexed.txt", "r")
	# Loads data from indexed_database if not empty
	if int(os.stat(indexed_database).st_size) != 0:
		for line in indexed_database:
			indexed_urls.append(line.strip())
	indexed_database.close()
	indexed_database = open("indexed.txt", "r")

	# Main script
	for i in range(depth):
		for page in urls:
			if str(page).lower().endswith('.pdf') and page not in indexed_urls:
				pdfs_temp.append(str(page))
				indexed_urls.append(str(page))
				urls.pop(page)
			if page in indexed_urls:
				urls.pop(page)

		new_urls = asyncio.run(fetch_and_extract_links_multiple(urls))
		urls = new_urls

		# Updating PDFs and new indexed URLs database
		if len(pdfs_temp) != 0:
			for url in pdfs_temp:
				pdfs_txt.append()
			print("Something updated in the pdfs.txt file.")
			pdfs_temp = []
		data = dict(indexed_urls)
		with open("indexed.json", 'w') as f:
			json.dump(data, f)


	print("\n\n### Finished ###")
