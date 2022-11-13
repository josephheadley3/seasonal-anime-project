# Imports
from bs4 import BeautifulSoup as bs
import requests
import psycopg2

# Web Scraper
response = requests.get('https://myanimelist.net/anime/season/2022/fall').text
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


# Test code for finding anime info on base case anime 'Chainsaw Man'
"""
info = soup.find('div', class_='js-seasonal-anime')
print(info.find('span', class_='js-title').text) # How to get an anime's title
print(info.find('span', class_='js-score').text) # How to get an anime's score
print(info.find('div', class_='info').text.split('\n')[1].split(',')[0]) # How to get an anime's episode numbers
print(info.find('div', class_='info').text.split('\n')[2].strip()) # How to get an anime's episode length
print(info.find('span', class_='js-members').text) # How to get an anime's member count
print(info.find('div', class_='info').text.split('\n')[0]) # How to get an anime's start date
print(info.find('p', class_='preline').text) # How to get an anime's synopsis
print([genre.text.strip() for genre in info.find_all('span', class_='genre')]) # How to get an anime's genres
print(info.find('div', class_='properties').find_all('div', class_='property')[2].find('span', class_='item').text) # How to get an anime's genres
print(info.find('div', class_='properties').find_all('div', class_='property')[3].find('span', class_='item').text) # How to get an anime's genres
print(info.find('div', class_='properties').find_all('div', class_='property')[0].find('span', class_='item').text) # How to get an anime's studio
print(info.find('div', class_='properties').find_all('div', class_='property')[1].find('span', class_='item').text) # How to get an anime's source material
print(info.find('a', class_='link-title')['href']) # How to get an anime's url
print(info.find('img')['src']) # How to get an anime's image link
"""


# Parsing through html info
for match in soup.find_all('div', class_='js-seasonal-anime'):
    titles.append(match.find('span', class_='js-title').text) # How to get an anime's title
    scores.append(float(match.find('span', class_='js-score').text)) # How to get an anime's score
    epnums.append(match.find('div', class_='info').text.split('\n')[1].split(',')[0]) # How to get an anime's episode numbers
    eplens.append(match.find('div', class_='info').text.split('\n')[2].strip()) # How to get an anime's episode length
    memnums.append(int(match.find('span', class_='js-members').text)) # How to get an anime's member count
    startdates.append(match.find('div', class_='info').text.split('\n')[0]) # How to get an anime's start date
    synopses.append(match.find('p', class_='preline').text) # How to get an anime's synopsis
    gnr_placeholder = [genre.text.strip() for genre in match.find_all('span', class_='genre')] # How to get an anime's genres
    try:
        gnr_placeholder.extend([match.find('div', class_='properties').find_all('div', class_='property')[2].find('span', class_='item').text])
    except:
        gnr_placeholder.extend([])
    try:
        gnr_placeholder.extend([match.find('div', class_='properties').find_all('div', class_='property')[3].find('span', class_='item').text])
    except:
        gnr_placeholder.extend([])
    genres.append(gnr_placeholder)
    studios.append(match.find('div', class_='properties').find_all('div', class_='property')[0].find('span', class_='item').text) # How to get an anime's studio
    sources.append(match.find('div', class_='properties').find_all('div', class_='property')[1].find('span', class_='item').text) # How to get an anime's source material
    urls.append(match.find('a', class_='link-title')['href']) # How to get an anime's url
    try:
        imagelinks.append(match.find('img')['src']) # How to get an anime's image link
    except:
        imagelinks.append(match.find('img')['data-src'])


# Sanity check that the lengths of all the lists are the same [length = 175]
"""
# print(len(titles))
# print(len(scores))
# print(len(epnums))
# print(len(eplens))
# print(len(memnums))
# print(len(startdates))
# print(len(synopses))
# print(len(genres))
# print(len(studios))
# print(len(sources))
# print(len(urls))
# print(len(imagelinks))
"""

# Establishing database connection
conn = psycopg2.connect(
   database="postgres", user='postgres', password='Boston2021', host='localhost', port= '5432', options="-c search_path=data_analytics"
)

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

# Dropping table in case it already exists
cursor.execute("DROP TABLE IF EXISTS anime_spring22")

# Create new table to hold webscraped data
cursor.execute('''CREATE TABLE anime_spring22(
    Title TEXT NOT NULL,
    Score FLOAT8 NOT NULL,
    Episode_Count TEXT,
    Episode_Length TEXT,
    Member_Count INT,
    Start_Date TEXT,
    Synopsis TEXT,
    Genre TEXT[],
    Studio TEXT,
    Source TEXT,
    URL TEXT,
    Image Text)''')


# Insert webscraped data into newly created table
for i in range(0, len(titles)):
    cursor.execute(""" INSERT INTO anime_spring22("title", "score", "episode_count", "episode_length", "member_count", "start_date", "synopsis", "genre", "studio", "source", "url", "image") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (titles[i], scores[i], epnums[i], eplens[i], memnums[i], startdates[i], synopses[i], genres[i], studios[i], sources[i], urls[i], imagelinks[i]))

# Commit changes from inserting webscraped data to the database
conn.commit()

# Close database connection
conn.close()

 