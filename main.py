import os
import random

from tempfile import NamedTemporaryFile

import requests

from dotenv import load_dotenv


GROUP_ID = 215398764
API_VERSION = 5.131


def download_random_image_and_message():
    api_template = 'https://xkcd.com/{}/info.0.json'

    response_latest_comic = requests.get(
        api_template.format(''),
    )
    response_latest_comic.raise_for_status()

    latest_comic = response_latest_comic.json()['num']
    random_comic = random.randint(1, latest_comic)

    response_random_comic = requests.get(
        api_template.format(random_comic),
    )
    response_random_comic.raise_for_status()

    decoded_response = response_random_comic.json()

    img_url = decoded_response['img']
    message = decoded_response['alt']

    response_img = requests.get(img_url)
    response_img.raise_for_status()

    img = response_img.content

    return img, message


def post_vk_wall(photo, message, params):
    api_template = 'https://api.vk.com/method/{}'

    response_upload_server = requests.get(
        api_template.format('photos.getWallUploadServer'),
        params=params,
    )
    response_upload_server.raise_for_status()
    upload_url = response_upload_server.json()['response']['upload_url']

    files = {
        'photo': photo,
    }

    response_upload_photo = requests.post(upload_url, files=files)
    response_upload_photo.raise_for_status()

    decoded_response_upload_photo = response_upload_photo.json()

    params['photo'] = decoded_response_upload_photo['photo']
    params['server'] = decoded_response_upload_photo['server']
    params['hash'] = decoded_response_upload_photo['hash']

    response_save_photo = requests.post(
        api_template.format('photos.saveWallPhoto'),
        params=params,
    )
    response_save_photo.raise_for_status()

    attachment_meta = response_save_photo.json()["response"][0]

    params['owner_id'] = -params['group_id']
    params['message'] = message
    params['attachments'] = '{type}{owner_id}_{media_id}'.format(
        type='photo',
        owner_id=attachment_meta["owner_id"],
        media_id=attachment_meta["id"],
    )

    del params['photo']
    del params['server']
    del params['hash']
    del params['group_id']

    response_post_wall = requests.post(
        api_template.format('wall.post'),
        params=params,
    )
    response_post_wall.raise_for_status()


def main():
    load_dotenv()
    access_token = os.environ['ACCESS_TOKEN']

    params = {
        'access_token': access_token,
        'v': API_VERSION,
        'group_id': GROUP_ID,
    }

    with NamedTemporaryFile(suffix='.png') as tmp:
        img, message = download_random_image_and_message()
        tmp.write(img)
        tmp.seek(0)
        post_vk_wall(tmp, message, params)


if __name__ == '__main__':
    main()
