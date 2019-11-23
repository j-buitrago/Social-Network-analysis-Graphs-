import sys
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

def related_albums(sp, artist_id):
    i = 0
    albums = []
    albums_def = list()
    while True:
        artist_info = sp.artist_albums(artist_id, album_type='album', offset=i, limit=1)
        i += len(artist_info['items'])
        try:
            album_name = artist_info['items'][0]['name']
            if album_name not in albums_def:
                album_image = artist_info['items'][0]['images'][0]['url']
                album_uri = artist_info['items'][0]['uri'].split(':')[2]
                album = {'name': album_name, 'uri': album_uri, 'image': album_image}
                albums.append(album)
                albums_def.append(album_name)
        except IndexError:
            if len(artist_info['items']) < 1:
                break
    return albums

def get_artist(artist):

    info = dict()
    info['id'] = artist['name']
    info['uri'] = artist['uri']
    info['popularity'] = artist['popularity']
    info['followers'] = artist['followers']['total']
    info['type'] = artist['type']
    info['image'] = artist['images'][0]["url"]

    return info

def related_artists(sp, artist_id, artists, artists_list,aristas):

    artists_list.setdefault(str(1), [])
    artist_info = sp.artist_related_artists(artist_id)

    artists = sp.artist(artist_id)
    artists = artists["name"]
    aristas.setdefault(artists, [])

    for artist in artist_info['artists']:
        for level in artists_list.keys():
            for art in artists_list[level]:
                if artist['name'] == art['id']:
                        index_to_delete = artists_list[level].index(art)
                        del artists_list[level][index_to_delete]

            artist_id = artist['uri'].split(':')[2]
            artists_list[str(1)].append(get_artist(artist))
            if artist["name"] not in aristas[artists]:
                aristas[artists].append(artist["name"])

def add_albums(sp, graph, artists):

    for i in artists.keys():
        for artist in artists[i]:
            artist_id = artist['uri'].split(':')[2]
            albums = related_albums(sp, artist_id)
            for album in albums:
                edge = dict()
                node = dict()
                node['id'] = album['name']
                node['type'] = 'album'
                node['image'] = album['image']
                node['uri'] = album['uri']
                graph["nodes"].append(node)
                edge["source"] = artist['id']
                edge["target"] = node['id']
                graph["links"].append(edge)
    return graph

if __name__ == '__main__':

    client_id = "f71c807cbb6e477a9f9550acf45227c2"
    client_secret = "92774a1bc6114a41b8e202374a3aa08f"

    # utilizaremos coldplay como artista 
    artist_id = '4gzpq5DPGxSnKTe4SA8HAU'
    final_graph_filename = '../datos/coldplay.json'

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    related = 0
    artists = None
    artists_list = dict()
    
    graph = dict()
    graph["directed"] = False
    graph["multigraph"] = False
    graph['graph'] = {}
    graph["nodes"] = list()
    graph["links"] = list()


    aristas = dict()
    related_artists(sp, artist_id, artists, artists_list, aristas)

    main_artist_info = sp.artist(artist_id)
    artists_list[str(related)] = []
    artists_list[str(related)].append(get_artist(main_artist_info))

    for level in artists_list.keys():
        for node in artists_list[level]:
            graph["nodes"].append(node)

    graph = add_albums(sp, graph, artists_list)

    for artist in aristas.keys():
        for friend_artist in aristas[artist]:
            edge = dict()
            edge["source"] = artist
            edge["target"] = friend_artist
            graph["links"].append(edge)

    with open(final_graph_filename, 'w') as outfile:
        json.dump(graph, outfile)

