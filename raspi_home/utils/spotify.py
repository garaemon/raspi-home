#!/usr/bin/env python

import os
import pprint

import spotipy
import spotipy.util


class SpotifyAlbum(object):
    def __init__(self, params):
        self.name = params['name']
        self.external_url = params['external_urls']['spotify']
        self.id = params['id']


class SpotifyArtist(object):
    def __init__(self, params):
        self.name = params['name']
        self.external_url = params['external_urls']['spotify']
        self.id = params['id']


class SpotifySong(object):
    def __init__(self, played_at, params):
        # pp = pprint.PrettyPrinter(indent=2)
        # pp.pprint(params)
        self.params = params
        self.name = params['name']
        self.played_at = played_at
        self.external_url = self.params['external_urls']['spotify']
        self.id = self.params['id']
        self.artists = [SpotifyArtist(param) for param in self.params['artists']]
        self.album = SpotifyAlbum(params['album'])

    def __str__(self):
        return 'Song({}, {})'.format(self.name, self.played_at)

    def __repr__(self):
        return self.__str__()

    def to_row(self):
        'played_at, name, external_url, id'
        return [self.played_at, self.id, self.name, self.external_url,
                ', '.join([artist.name for artist in self.artists]),
                self.album.id, self.album.name]


class SpotifyClient(object):
    def __init__(self):
        token = spotipy.util.prompt_for_user_token(os.environ['SPOTIPY_USER'],
                                                   'user-read-recently-played')
        self.sp = spotipy.Spotify(auth=token)

    def get_recently_played(self):
        params = self.sp._get('me/player/recently-played', limit=50, offset=0)
        songs = []
        for song_item in params['items']:
            songs.append(SpotifySong(song_item['played_at'],
                                     song_item['track']))
        songs.reverse()
        return songs


if __name__ == '__main__':
    client = SpotifyClient()
    songs = client.get_recently_played()
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint([s.to_row() for s in songs])
