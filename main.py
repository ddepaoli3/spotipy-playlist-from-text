#!/usr/bin/env python

import auth
import argparse

def get_playlist(playlist_name, spotify_client, username):
	for playlist in spotify_client.spotify.user_playlists(username)['items']:
		if playlist['name'] == playlist_name:
			print "Playlist gia esistente"
			return playlist
	#Playlist not present, so create it
	print "Playlist da creare"
	playlist = spotify_client.spotify.user_playlist_create(username, playlist_name)
	return playlist

def get_track(string_to_search, spotify_client):
	try:
		result = spotify_client.spotify.search(string_to_search)
		id = result["tracks"]["items"][0]
	except Exception, e:
		return None
	return id

def argument():
    parser = argparse.ArgumentParser(description="Search and add song to a spotify playlist from a list in file.")
    parser.add_argument("-i", "--input-file", required=True,
            help="Input file with list of songs")
    parser.add_argument("-p", "--playlist", required=True,
            help="Name of playlist")
    parser.add_argument("-u", "--username", required=True,
            help="Name of user")
    args = parser.parse_args()
    return args

##Main function
if __name__ == '__main__':
	args = argument()
	spotify_client = auth.Client()
	playlist = get_playlist(args.playlist, spotify_client, args.username)
	not_found = []
	count = 1
	with open(args.input_file, 'r') as f:
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