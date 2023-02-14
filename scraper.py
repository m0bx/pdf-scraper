import requests
from bs4 import BeautifulSoup

# Read initial URL from text file
with open('start_urls.txt', 'r') as f:
    url = f.read().strip()

response = requests.get(url)
content = response.content

# parse page content
soup = BeautifulSoup(content, 'html.parser')

# find all links on the page
links = soup.find_all('a')

with open('links.txt', 'a') as f:
    for link in links:
        href = link.get('href')
        if href is not None and href.startswith('http') and href.endswith('.pdf'):
            f.write(href + '\n')
