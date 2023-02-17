import aiohttp
import asyncio
import os

from bs4 import BeautifulSoup


########################################################################################################################

# Fetches and returns the whole response text with the aiohttp.ClientSession() session.
async def fetch(session, url):
	try:
		async with session.get(url, headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}) as response:
			return await response.text()
	except:
		async with session.get(url, headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}) as response:
			await response.text()
			print("Error " + response.status + "  ...  " + str(url))
			return await response.status


# Part of the fetch code, gathers html data as a response from the fun above.
async def fetch_and_extract_links(url):
	async with aiohttp.ClientSession() as session:
		try:
			html = await fetch(session, url)
			soup = BeautifulSoup(html, 'html.parser')
			links = [link.get('href') for link in soup.find_all('a')]
			return links
		except:
			return


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
		#print("responses: " + str(responses))
		# Since responses is 2d array, we need to make 2 for cycles to gather 2nd layer data:
		links = [link for sublist in responses for link in sublist]
		print("links: " + str(links))
		return links  # Returns links (damn), it is an array of all gathered links from all the urls given


# Now using asyncio.run(fetch_and_extract_links_multiple(urls)) the process will start for given urls (should)

if __name__ == "__main__":

	# Config
	depth = 2  # Setup depth
	urls = ["https://www.pdfa.org"]  # Setup starting urls, they need to have a protocol (http/s) set
	print("Starting with depth:" + str(depth))

	# PDFs file
	pdfs_txt = open("pdfs.txt", "a+")  # a+ is for appending at the end, file will be created if it doesn't exist
	pdfs_temp = []

	# Code to handle indexed URLs database
	indexed_urls = []
	open("indexed.txt", "a+").close()
	with open("indexed.txt", "r+") as f:
		# Loads data from indexed_database if not empty
		if 0 != int(os.stat("indexed.txt").st_size):
			for line in f:
				indexed_urls.append(line.strip())

	# Main script
	for i in range(depth):
		for page in urls:
			if str(page).lower().endswith('.pdf') and page not in indexed_urls:
				pdfs_temp.append(str(page))
				indexed_urls.append(str(page))
				#urls.pop(urls.index(page))
			#elif page in indexed_urls:
				#urls.pop(urls.index(page))

		new_urls = asyncio.run(fetch_and_extract_links_multiple(urls))
		urls = new_urls

		# Updating PDFs file
		if len(pdfs_temp) != 0:
			for url in pdfs_temp:
				pdfs_txt.write("\n" + str(url))
			print("Something updated in the pdfs.txt file.")
			pdfs_temp = []
		# Replace contents of indexed.txt with indexed_urls
		with open("indexed.txt", "w") as f:
			for url in indexed_urls:
				f.write(str(url) + "\n")

	print("\n\n### Finished ###")
