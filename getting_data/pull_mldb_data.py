import json
import requests
import bs4
from bs4 import BeautifulSoup
from collections import defaultdict

def get_list_of_songs(mldb_artist_link, debug=True):
    # Collect first page of artists’ list
    page = requests.get(mldb_artist_link)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get list of song links
    song_name_list = soup.find(id='thelist')
    song_name_list_items = song_name_list.find_all('td')
    song_links = list()
    for table_row in song_name_list_items:
        link_tag = table_row.contents[0]
        song_links.append('http://www.mldb.org/' + link_tag.get('href'))
        if debug:
            print('Found song link: ', 'http://www.mldb.org/' + link_tag.get('href'))
    return song_links

def get_lyrics_for_songs(song_links, debug=True):
    lyrics = defaultdict(str)
    for link in song_links:
        try:
            song_page = requests.get(link)
            soup = BeautifulSoup(song_page.text, 'html.parser')
            song_name = soup.find('h1').contents[0]
            lyrics_object = soup.find(class_='songtext')
            lyrics_parts = [x.strip() for x in lyrics_object.contents if type(x) is not bs4.element.Tag]
            lyrics[song_name] = '\n'.join(lyrics_parts)
            if debug:
                print('Got lyrics for song: ' + song_name)
        except Exception as e:
            if debug:
                print(e)
    return lyrics

def store_lyrics(lyrics, json_file_name, debug=True):
    with open(json_file_name, 'w') as f:
        json.dump(lyrics, f)
    if debug:
        print('Dumped lyrics to JSON file: ', json_file_name)

def find_artist_link(artist_name, debug=True):
    artist_name = artist_name.replace(' ', '+')
    query_link = 'http://www.mldb.org/search?mq=' + artist_name + '&si=1&mm=0&ob=1'
    page = requests.get(query_link)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find(id='thelist')
    # fa gets artist name tag, contents[0] of that gets the <a> tag
    artist_link = 'http://www.mldb.org/' + table.find(class_='fa').contents[0].get('href')
    if debug:
        print('Found artist link: ', artist_link)
    return artist_link

def get_all_artist_lyrics(artist_name, debug=True):
    artist_name = artist_name.lower()
    artist_link = find_artist_link(artist_name, debug=debug)
    list_of_songs = get_list_of_songs(artist_link, debug=debug)
    lyrics = get_lyrics_for_songs(list_of_songs, debug=debug)
    store_lyrics(lyrics, artist_name.replace(' ', '_') + '_lyrics.json', debug=debug)

# get_all_artist_lyrics('Queen')
# get_all_artist_lyrics('Taylor Swift')
