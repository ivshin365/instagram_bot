import time
from instagrapi import Client
import random
import praw
import requests

# connect to reddit
reddit = praw.Reddit(client_id='O97hL_NLQl0DTJwfjdRZkQ',
                     client_secret='5KYC3Y4T3D3yE_GgdIil98BbY22l5Q',
                     user_agent='DavidIvshin',
                     username='David_ivshin',
                     password='paraivshin365')

url: ""
quote: ""

def get_new_image():
    global url, quote
    subreddit = reddit.subreddit('90dayfianceuncensored')
    posts = subreddit.new(limit=50)
    for submission in posts:
        if not submission.stickied:
            if submission.score > 300:
                image_formats = ("image/png", "image/jpeg", "image/jpg")
                r = requests.head(submission.url)
                if r.headers.get("content-type", '') in image_formats:
                    print('fetching post from sub-reddit...')
                    print(submission.title + ' - Upvotes >' + str(submission.score))
                    print(submission.url)
                    quote = submission.title
                    url = submission.url
    return [url, quote]


# Save image to local folder

def save_image():
    url, quote = get_new_image()
    response = requests.get(url)
    if response.status_code == 200:
        with open("sample.jpg", 'wb') as f:
            f.write(response.content)


# load instagram credentials from file

with open("credentials.txt", "r") as f:
    username, password = f.read().splitlines()

client = Client()
client.login(username, password)

hashtag = "90dayfiance"
medias = client.hashtag_medias_recent(hashtag, 20)

comments = ["Awsome!!", "fire🔥!!", "Love it!"]

def like_and_follow():
    for i, media in enumerate(medias):
        client.media_like(media.id)
        print(f"Liked post number {i + 1} of hashtag {hashtag}")
        if i % 2 == 0:
            client.user_follow(media.user.pk)
            print(f"followed user {media.user.username}")
            time.sleep(8)
            comment = random.choice(comments)
            client.media_comment(media.id, comment)
            print(f"commented {comment} under post number {i + 1}")


def upload_photo():
    url, quote = get_new_image()
    client.photo_upload(path="sample.jpg",
                        caption=f"{quote} \n. \n. \n #90dayfiancememes #90dayfiance #realitytv #90dayfiancetheotherway #funny #90dayfiancehappilyeverafter #90dayfiancebeforethe90days #90dayfiancenews #90dayfiancewhatnow #90df #90dayfiance_tlc #90dayfiancefans #bravomemes")
    print(f"posting new post: {quote}")

while True:
    get_new_image()
    time.sleep(5)
    save_image()
    time.sleep(5)
    upload_photo()
    time.sleep(5)
    like_and_follow()
    break