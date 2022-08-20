import os
import random

from tempfile import NamedTemporaryFile

import requests

from dotenv import load_dotenv


API_VERSION = 5.131


def download_random_comic():
    url_template = 'https://xkcd.com/{}/info.0.json'

    latest_comic_response = requests.get(
        url_template.format(''),
    )
    latest_comic_response.raise_for_status()

    latest_comic = latest_comic_response.json()['num']
    random_comic = random.randint(1, latest_comic)

    random_comic_response = requests.get(
        url_template.format(random_comic),
    )
    random_comic_response.raise_for_status()

    decoded_response = random_comic_response.json()

    img_url = decoded_response['img']
    message = decoded_response['alt']

    img_response = requests.get(img_url)
    img_response.raise_for_status()

    img = img_response.content

    return img, message


def get_upload_url(access_token, api_version, group_id):
    api_endpoint = 'https://api.vk.com/method/photos.getWallUploadServer'

    response = requests.get(api_endpoint, params={
        'access_token': access_token,
        'v': api_version,
        'group_id': group_id,
    })
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']

    return upload_url


def upload_image_to_server(upload_url, image):
    files = {
        'photo': image,
    }

    response = requests.post(upload_url, files=files)
    response.raise_for_status()

    decoded_response = response.json()

    photo = decoded_response['photo']
    server = decoded_response['server']
    response_hash = decoded_response['hash']

    return photo, server, response_hash


def save_image_to_server(
        access_token,
        api_version,
        group_id,
        photo,
        server,
        response_hash,
):

    api_endpoint = 'https://api.vk.com/method/photos.saveWallPhoto'

    response = requests.post(api_endpoint, params={
        'access_token': access_token,
        'v': api_version,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': response_hash,
    })
    response.raise_for_status()

    decoded_response = response.json()

    owner_id = decoded_response['response'][0]['owner_id']
    image_id = decoded_response['response'][0]['id']

    image_as_attachment = '{type}{owner_id}_{media_id}'.format(
        type='photo',
        owner_id=owner_id,
        media_id=image_id,
    )

    return image_as_attachment


def post_wall(access_token, api_version, group_id, message, attachment):
    api_endpoint = 'https://api.vk.com/method/wall.post'

    response = requests.post(api_endpoint, params={
        'access_token': access_token,
        'v': api_version,
        'owner_id': -group_id,
        'message': message,
        'attachments': attachment,
    })
    response.raise_for_status()


def main():
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']
    group_id = int(os.environ['VK_GROUP_ID'])

    vk_upload_url = get_upload_url(access_token, API_VERSION, group_id)

    with NamedTemporaryFile(suffix='.png') as tmp:
        img, message = download_random_comic()
        tmp.write(img)
        tmp.seek(0)

        photo, server, response_hash = upload_image_to_server(vk_upload_url, tmp)
        image_attachment = save_image_to_server(
            access_token,
            API_VERSION,
            group_id,
            photo,
            server,
            response_hash,
        )
        post_wall(
            access_token,
            API_VERSION,
            group_id,
            message,
            image_attachment,
        )


if __name__ == '__main__':
    main()
