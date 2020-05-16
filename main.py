import argparse
import os
import VKapi
import utils
import sys

IMAGES_EXTENSIONS = ['.jpg', '.png', '.jpeg']


def parse_args():
    arg_parser = argparse.ArgumentParser("python main.py")
    arg_parser.add_argument('-d', '--directory', metavar='directory', required=True, help='directory with images')
    arg_parser.add_argument('-a', '--album', metavar='album', required=True, help='Album name (case sensitive)')
    arg_parser.add_argument('-t', '--token', metavar='token', help='VK authentication token (if you already have it)')
    arg_parser.add_argument('-u', '--user', metavar='user id', help='User id')
    res = arg_parser.parse_args()
    if not res.token:
        auth = VKapi.VKAuth()
        _token = auth.get_token()
    else:
        _token = res.token

    if not res.user:
        _user = get_user_id()
    else:
        _user = res.user

    return res.directory, res.album, _token, _user


def find_images(path):
    _images = []
    try:
        for file in os.listdir(path):
            for ext in IMAGES_EXTENSIONS:
                if file.endswith(ext):
                    _images.append(os.path.join(path, file))
    except OSError:
        print(f'Wrong directory {path}')
        sys.exit(1)
    return _images


def get_user_id():
    print('Enter a user id:')
    return input()


if __name__ == "__main__":
    directory, album, token, user = parse_args()

    images = find_images(directory)
    if not images:
        print(f"can't find images in {directory}")
        sys.exit(2)

    album_api = VKapi.AlbumApi(token, user)
    # TODO make error handling
    album_id = album_api.find_album_by_name(album)
    progressBar = utils.ProgressBar(len(images))

    for image in images:
        upload_url = album_api.get_upload_server(album_id)
        response = album_api.upload_image(upload_url, image)
        album_api.save_photos(album_id, response['server'], response['photos_list'], response['aid'], response['hash'])
        progressBar.update()
