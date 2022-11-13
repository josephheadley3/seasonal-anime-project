# Imports
from bs4 import BeautifulSoup as bs
import requests
import psycopg2

# Web Scraper
response = requests.get('https://myanimelist.net/anime/season').text
soup = bs(response, 'lxml')

# Initializing empty lists to hold separate anime info
# anime_html = []
titles = []
scores = []
epnums = []
eplens = []
memnums = []
startdates = []
synopses = []
gnr_placeholder = []
genres = []
studios = []
sources = []
urls = []
imagelinks = []

info = soup.find('div', class_='js-seasonal-anime')
print(info.find('a', class_='link-title')['href']) # How to get an anime's url
print(info.find('img')['src']) # How to get an anime's image link

# Miscellaneous Test Code Snippets

# Parsing through html info
# for match in soup.find_all('div', class_='js-seasonal-anime'):
#     anime_html.append(match)

# print(len(anime_html))

# info = soup.find('div', class_='js-seasonal-anime')
# print(info)


# gnr1 = [genre.text.strip() for genre in info.find_all('span', class_='genre')]
# gnr1.extend([info.find('div', class_='properties').find_all('div', class_='property')[2].find('span', class_='item').text])
# gnr1.extend([info.find('div', class_='properties').find_all('div', class_='property')[3].find('span', class_='item').text])
# print(gnr1)
# print(info.find('div', class_='properties').find_all('div', class_='property')[2].find('span', class_='item').text, info.find('div', class_='properties').find_all('div', class_='property')[3].find('span', class_='item').text)


# for match in soup.find_all('div', class_='js-seasonal-anime'):
#     try:
#         print(match.find('div', class_='properties').find_all('div', class_='property')[2])
#     except:
#         print("N/A")
    # demographics.append(match.find('div', class_='properties').find_all('div', class_='property')[3])#.find('span', class_='item').text) # How to get an anime's demographic

# print(demographics)

# Test code for finding the mediums for all anime on the page
"""
for match in soup.find_all('div', class_='js-seasonal-anime-list'):
    print(match.find('div', class_='anime-header').text)
"""
