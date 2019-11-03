import requests
from bs4 import BeautifulSoup

url = "http://www.football-data.co.uk/englandm.php"
response = requests.get(url)

soup = BeautifulSoup(response.text, “html.parser”)


## APPENDIX ##
'''
url = 'http://www.football-data.co.uk/mmz4281/1920/E0.csv'
r = requests.get(url, allow_redirects=True)
with open('E0.csv', 'wb') as f:
    f.write(r.content)
'''
