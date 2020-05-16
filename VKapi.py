import webbrowser
import urllib.request
import urllib.parse
import json
import sys
import requests
import os


class VKAuth:
    CLIENT_ID = 7454649
    REDIRECT_URI = 'https://oauth.vk.com/blank.html'
    DISPLAY = 'page'
    SCOPE = 'photos'
    RESPONSE_TYPE = 'token'
    VERSION = '5.103'

    def __init__(self):
        link = 'https://oauth.vk.com/authorize?client_id={}&display={}&redirect_uri={}&scope={}&response_type={}&v={}'.format(
            self.CLIENT_ID, self.DISPLAY, self.REDIRECT_URI, self.SCOPE, self.RESPONSE_TYPE, self.VERSION)
        webbrowser.open(link)

    def get_token(self):
        print('Enter a token:')
        self.token = input()
        return self.token


class AlbumApi:
    VERSION = '5.103'

    def __init__(self, access_token, user_id):
        self.user_id = user_id
        self.access_token = access_token

    def get_albums(self):
        link = 'https://api.vk.com/method/photos.getAlbums?access_token={}&user_id={}&v={}'.format(
            self.access_token, self.user_id, self.VERSION)
        data = urllib.request.urlopen(link)
        albums_info = json.loads(data.read())
        print(albums_info)
        try:
            return albums_info['response']['items']
        except KeyError:
            if albums_info['error']['error_code'] == 5:
                print('Invalid token')
                sys.exit(3)

    def find_album_by_name(self, name):
        albums = self.get_albums()
        for album in albums:
            if album['title'] == name:
                return album['id']
        print('User {} has no album with name {}'.format(self.user_id, name))
        sys.exit(4)

    def get_upload_server(self, album_id):
        link = 'https://api.vk.com/method/photos.getUploadServer?access_token={}&album_id={}&v={}'.format(
            self.access_token, album_id, self.VERSION)
        data = urllib.request.urlopen(link)
        server_info = json.loads(data.read())
        try:
            return server_info['response']['upload_url']
        except KeyError:
            print('Error while upload photos. Not enough permissions')
            sys.exit(5)

    def upload_image(self, upload_url, image):
        file = {'file1': (os.path.basename(image), open(image, 'rb'))}
        response = requests.post(upload_url, files=file)
        return response.json()

    def save_photos(self, album_id, server, photos_list, aid, hash):
        link = 'https://api.vk.com/method/photos.save?access_token={}&album_id={}&server={}&aid={}&hash={}&v={}'.format(
            self.access_token, album_id, server, aid, hash, self.VERSION)
        response = requests.post(link, data={'photos_list': photos_list})
