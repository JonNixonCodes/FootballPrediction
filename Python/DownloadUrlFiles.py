import re
import requests
from bs4 import BeautifulSoup

# Constants
MAIN_URL = "http://www.football-data.co.uk/englandm.php"
URL_REGEX = re.compile(r"mmz4281.*\.csv")

# Helper Functions
filterUrl = lambda x: URL_REGEX.search(x) != None
prependUrl = lambda x: "http://www.football-data.co.uk/"+x
getUrl = lambda x: x.attrs['href']
getFileName = lambda x: "_".join(re.split(r"[/.]",x)[-3:-1])+".csv"

# Main
response = requests.get(MAIN_URL)
soup = BeautifulSoup(response.text, "html.parser")
anchor_tags = soup.findAll('a')
urls = list(map(getUrl, anchor_tags))
urls = list(filter(filterUrl, urls))
urls = list(map(prependUrl, urls))
for ind,url in enumerate(urls):
    r = requests.get(url, allow_redirects=True)
    fname = getFileName(url)
    print(f"\tSaving file {ind+1}/{len(urls)}",end='\r', flush=True)
    with open(fname, 'wb') as f:
        f.write(r.content)
print("\tFinished",end="\n" flush=False)

