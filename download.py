import requests
import os
import zipfile
import json
import html
import io

api = 'https://beatsaver.com/api/songs/new/{}'
dl = 'https://beatsaver.com/download/{}'

def fetch_page(start: int):
    resp = requests.get(api.format(start)).json()
    songs = resp['songs']
    num = len(songs)
    return songs, num + start, num == 0

def check_json(key: str):
    if os.path.isfile('songs.json'):
        with open('songs.json', 'r') as handle:
            check = json.loads(handle.read())
            if key in check:
                return True
            else:
                return False
    else:
        return False

def write_json(key: str): 
    if os.path.isfile('songs.json'):
        with open('songs.json', 'r') as handle:
            data = json.loads(handle.read())
    else:
        data = []

    data.append(key)

    with open('songs.json', 'w') as handle:
        handle.write(json.dumps(data))

def download(song):
    key = song['key']
    name = song['name']

    # If we know we've downloaded a song already, skip it
    if check_json(key):
        return

    # *unzips*
    zip_file = requests.get(dl.format(key)).content
    try:
        with zipfile.ZipFile(io.BytesIO(zip_file)) as song_zip:
            song_zip.extractall('CustomSongs/{}'.format(song['key']))
            
        # Save the fact we've downloaded this song
        write_json(key)
        print('Downloading {}'.format(name))
    except:
        print('Failed to download {}. An Error occoured'.format(html.unescape(name)))

def main():
    done = False
    start = 0
    
    while not done:
        songs, start, done = fetch_page(start)
        for song in songs:
            download(song)

main()
