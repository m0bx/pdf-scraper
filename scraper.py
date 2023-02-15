import requests
import json
from bs4 import BeautifulSoup


def scrape_link(url, headers):
	# Make request to URL and get page content
	try:
		print("trying request at page:" + str(url))

		response = requests.get(str(url), headers=headers, timeout=3)
		print("success at page:" + str(url))
	except Exception as error3:
		raise Exception(str(error3))
	content = response.content

	# Parse page content using BeautifulSoup
	soup = BeautifulSoup(content, 'html.parser')

	# Find all links on the page, 'a' is a link html element
	links = soup.find_all('a')

	# Create list of links that are links
	found_links = []
	for link in links:
		href = link.get('href')
		if href is not None and href.startswith('http'):
			found_links.append(href)

	# Return list of PDF links
	return found_links


if __name__ == "__main__":
	# Config stuff
	clear_indexed = input("Do you want to erase indexed before you start the process? y/n \n")
	if clear_indexed == "y":
		try:
			open("indexed.txt", "w").close()
		except FileNotFoundError:
			print("You dont even have indexed file setup yet ...")
	elif clear_indexed != "n":
		exit()
	try:
		with open('config.json', 'r') as cfg:
			config = json.load(cfg)
	except Exception as e:
		print("Error parsing config file contents, repairing or creating config.json")
		cfg_setup = {"depth": 2, "start": ['https://pdfix.net']}
		cfg = open("config.json", 'w')
		json.dump(cfg_setup, cfg)
		cfg.close()
		cfg = open("config.json", 'r+')
		config = json.load(cfg)

	# Load stuff from cfg
	depth = config["depth"]
	starter_urls = config["start"]
	urls = config["start"]
	print("Loaded configs; depth:" + str(depth) + ", urls: " + str(urls))

	"""
	# Fun statistics
	try:
		stats = open('stats.json', 'r+')
		overall_stats = json.load(stats)
	except Exception as err:
		print("Error parsing stats file contents, repairing or creating stats.json. If something goes wrong remove the stats.json file completely.\nError: " + str(err))
		settings = {"Total": 0, "Found": 0}
		stats = open('stats.json', 'w')
		json.dump(settings, stats)
		overall_stats = settings
		stats = open('stats.json', 'r+')
	"""
	# Indexed urls
	try:
		indexed_urls = []
		indexed_urls_file = open("indexed.txt", "r+")
		for line in indexed_urls_file:
			indexed_urls.append(line.strip())
	except FileNotFoundError:
		indexed_urls = []
		print("Indexed URLs database does not exist. Creating a new file...")
		indexed_urls_file = open("indexed.txt", 'a+')
		indexed_urls_file.close()
		indexed_urls_file = open("indexed.txt", "r+")

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
	"""
	# Loads up statistics from stats.json file
	total_pdfs_count = overall_stats["Found"]
	total_url_count = overall_stats["Total"]
	"""
	# Main script
	for i in range(depth):
		# Looks for strings in urls variable
		for page in urls:
			# Checks if page is not in indexed urls, does nothing and skips the url if it already was scraped
			if str(page).endswith('.pdf') and page not in indexed_urls:
				# Appends pdf destination URL to a file
				print("\nFound PDF file\n")
				pdfs.write(str(page) + "\n")
				# Stats
				# total_pdfs_count += 1
				# total_url_count += 1
			elif page not in indexed_urls:  # or page in starter_urls
				# Stats
				# total_url_count += 1
				# Adds page to indexed
				indexed_urls.append(page)
				indexed_urls_file.write(str(page) + "\n")
				# Runs runs scraper with 'page' url and assigns found sites to a variable new_links
				try:
					new_links = scrape_link(str(page), headers=default_headers)
				# Provides explanation on caught exceptions, may be an url rate limit, unknown site or anything else
				except Exception as error:
					print("Error at page " + str(page) + ": \n" + str(error))
					continue
				# Finally, appends new_links (scraped links) to an array of urls
				for a in new_links:
					urls.append(str(a))

		# Stats
		# stats_upload = {"Total": total_url_count, "Found": total_pdfs_count}
		# json.dump(stats_upload, stats)
	print("\n\n### Finished ###")
