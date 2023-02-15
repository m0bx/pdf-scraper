import requests
import json
from bs4 import BeautifulSoup

def scrape_link(url, headers):
    # Make request to URL and get page content
    try:
        response = requests.get(str(url))
        print("success at page:" + str(url))
    except:
        raise Exception("RequestFail")
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
    try:
        with open('config.json', 'r') as cfg:
            config = json.load(cfg)
    except:
        print("Error parsing config file contents, repairing or creating config.json")
        cfg_setup = {"depth": 5, "start": "https://www.gamca.sk"}
        with open("config.json", 'w') as cfg:
            json.dump(cfg_setup, cfg)
            config = json.load(cfg)

    # This will append all already searched urls to an array, from a file, if file doesn't exist, it creates one


    # Fun statistics
    try:
        with open('stats.json', 'r') as stats:
            overall_stats = json.load(stats)
    except:
        print("Error parsing config file contents, repairing or creating config.json")
        settings = {"Total requests": 0, "Found pdfs": 0}
        with open("stats.json", 'w') as stats:
            json.dump(settings, stats)
            overall_stats = json.load(stats)

    # Indexed urls
    try:
        indexed_urls = []
        with open("indexed.txt", "r") as indexed_urls_file:
            for line in indexed_urls_file:
                indexed_urls.append(line.strip())
    except FileNotFoundError:
        print("Indexed URLs database does not exist. Creating a new file...")
        with open("indexed.txt", 'a+') as indexed_urls_file:
            indexed_urls_file.seek(0)  # move the file pointer to the beginning
            for line in indexed_urls_file:
                indexed_urls.append(line.strip())

    try:
        open("pdfs.txt", "r")
    except FileNotFoundError:
        print("PDFs database does not exist. Creating a new file...")
        with open("indexed.txt", 'a+') as pdfs:
            pdfs.seek(0)
    # Load stuff
    depth = config["depth"]
    urls = config["start"]
    # Sets up headers for the request
    default_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    total_pdfs_count = overall_stats["Found pdfs"]
    total_url_count = overall_stats["Total requests"]

    # Main script
    for i in range(depth):
        # Looks for strings in urls variable
        for page in urls:
            # Checks if page is not in indexed urls, does nothing and skips the url if it already was scraped
            if str(page).endswith('.pdf') and page not in indexed_urls:
                pdfs.append(page + "\n")
                total_pdfs_count += 1
                settings = {"Total requests": total_url_count, "Found pdfs": total_pdfs_count}
                json.dump(settings)
            if page not in indexed_urls:
                # Adds page to indexed
                indexed_urls.append(page)
                # Runs runs scraper with 'page' url and assigns found sites to a variable new_links
                try:
                    new_links = scrape_link(str(page), headers=default_headers)
                # Provides explanation on caught exceptions, may be an url rate limit, unknown site or anything that is the reason why you cannot access the site
                except Exception as error:
                    print("Error at page " + str(page) + ": \n" + str(error))
                    continue
                # Finally, appends new_links (scraped links) to an array of urls
                for a in new_links:
                    urls.append(str(a))
            # here goes the pdf code
    print("Finished")
