import tweepy
from PIL import Image
import requests
from io import BytesIO
import numpy as np

consumer_key = 'TUsO1lzISC4kMxxaeGJQSK4RJ'
consumer_secret = 'DiD0jtgc86F4kWDXQtFzvHEsR6XfsWnNFNTVBu7Db4O4BoESPU'
access_token = '1111803728762302465-jJGLPd4fQ93QZ0OPJwmAcCQ0koxyQD'
access_token_secret = 'IQVI6L06wcgkoV1F2zPkc0ONpnx64SXl9oocuMpyrJAOU'

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

counter_position_map = {
    1:[463,345],
    2:[580,345],
    3:[698,345],
    4:[816,345],
    5:[934,345],
}

def get_circle_profile_image(url):
    profile_image_url = url.replace('_normal', '')
    response = requests.get(profile_image_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    np_img = np.array(img)
    h, w, _ = np_img.shape
    x, y = np.ogrid[:h, :w]
    center_x, center_y = w // 2, h // 2
    mask = (x - center_x) ** 2 + (y - center_y) ** 2 > (h // 2) ** 2
    np_img[mask] = [255, 255, 255, 0]
    img = Image.fromarray(np_img, mode='RGBA')
    img = img.resize((103, 103))
    return img


def fetch_profile_image():
    followers = api.get_followers(count=5)
    picture_count = 0
    for follower in followers:
        picture_count += 1
        draw_profile_on_header(follower.profile_image_url_https, 'header.png',counter_position_map.get(picture_count)[0],counter_position_map.get(picture_count)[1])


def draw_profile_on_header(url, header_file,position_x=0,position_y=0):
    header_img = Image.open(header_file).convert("RGBA")
    circle_profile_img = get_circle_profile_image(url)
    header_img.alpha_composite(circle_profile_img, dest=(position_x, position_y))
    header_img.save('header.png')

def main():
    try:
        fetch_profile_image()
        print('update twitter header')
        api.update_profile_banner('header.png')
    except tweepy.TweepError as e:
        print("Error: " + str(e))
    

if __name__ == '__main__':
    main()