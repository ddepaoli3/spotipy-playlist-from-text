#!/usr/bin/env python

import auth

USERNAME = "ddepaoli3"
FILENAME = "parte1"
PLAYLISTNAME = "Belle varie - Parte 1"

def get_playlist(playlist_name, spotify_client):
	for playlist in spotify_client.spotify.user_playlists(USERNAME)['items']:
		if playlist['name'] == playlist_name:
			print "Playlist gia esistente"
			return playlist
	#Playlist not present, so create it
	print "Playlist da creare"
	playlist = spotify_client.spotify.user_playlist_create(USERNAME, PLAYLISTNAME)
	return playlist

def get_track(string_to_search, spotify_client):
	try:
		result = spotify_client.spotify.search(string_to_search)
		id = result["tracks"]["items"][0]
	except Exception, e:
		return None
	return id


##Main function
if __name__ == '__main__':
	spotify_client = auth.Client()
	playlist = get_playlist(PLAYLISTNAME, spotify_client)
	not_found = []
	count = 1
	with open(FILENAME, 'r') as f:
		content = f.readlines()
		for line in content:
			track = get_track(line, spotify_client)
			if track:
				print("Track {} found! {}/{}").format(line, count, len(content))
				results = spotify_client.spotify.user_playlist_add_tracks(USERNAME, playlist["id"], [track["id"]])
			else:
				not_found.append(line)
			count = count + 1
	print not_found