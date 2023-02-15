import requests
import json
from bs4 import BeautifulSoup

def scrape_pdfs(url):
    # Make request to URL and get page content
    try:
        response = requests.get(url)
    except:
        raise Exception("RequestFail")
    content = response.content

    # Parse page content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Find all links on the page, 'a' is a link html element
    links = soup.find_all('a')

    # Create list of links that end with ".pdf"
    pdf_links = []
    for link in links:
        href = link.get('href')
        if href is not None and href.startswith('http') and href.endswith('.pdf'):
            pdf_links.append(href)

    # Return list of PDF links
    return pdf_links



if __name__ == "__main__":
    # Config stuff
    try:
        with open('config.json', 'r') as cfg:
            config = json.load(cfg)
    except:
        print("Error parsing config file contents, repairing or creating config.json")
        settings = {"depth": 5, "start": "https://www.gamca.sk"}
        with open("config.json", 'w') as cfg:
            json.dump(settings, cfg)
            config = json.load(cfg)

    # Load configs from config variable
    depth = config['depth']
    urls = config['start']



    # This will append all already searched urls to an array, from a file, if file doesn't exist, it creates one
    indexed_urls = []

    try:
        with open("indexed.txt", "r") as indexed_urls_file:
            for line in indexed_urls_file:
                indexed_urls.append(line.strip())
    except FileNotFoundError:
        print("Indexed URLs database does not exist. Creating a new file...")
        with open("indexed.txt", 'a+') as indexed_urls_file:
            indexed_urls_file.seek(0)  # move the file pointer to the beginning
            for line in indexed_urls_file:
                indexed_urls.append(line.strip())

    # Load data from json



    # Main script, runs in depth of the depth variable
    for i in range(depth):
        # Looks for strings in urls variable
        for page in urls:
            # Checks if page is not in indexed urls, does nothing and skips the url if it already was scraped
            if page not in indexed_urls:
                #
                indexed_urls.append(page)
                # Runs runs scraper with 'page' url and assigns found sites to a variable new_links
                try:
                    new_links = scrape_pdfs(str(page))
                # Provides explanation on caught exceptions, may be an url rate limit, unknown site or anything that is the reason why you cannot access the site
                except Exception as error:
                    print("Error at page " + str(page) + ": \n" + error)
                    continue
                # Finally, appends new_links (scraped links) to an array of urls
                urls.append(new_links)