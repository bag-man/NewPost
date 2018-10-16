import sys
import praw
import time
import requests
import json

from slackclient import SlackClient
sc = SlackClient('WEB_API_KEY')

users = ['Midasx']
reddits = ['detroitredwings']
seen = []

r = praw.Reddit(
    user_agent='NewPost',
    client_id='RGtz43e2ZuuuoA',
    client_secret='clientsecret',
    username='NewPostAlert',
    password='password'
)

print("Logged in")

first = True

while True:
    try:
        for sub in reddits:
            for post in r.subreddit(sub).new(limit=10):
                if first is True:
                    seen.append(post.id)
                if post.id not in seen:
                    # subject = 'New post in ' + str(post.subreddit)
                    # content = '[' + post.title + '](' + post.shortlink + ')'
                    # for user in users:
                    #     r.redditor(user).message(subject, content)

                    if post.author != 'OctoMod':
                        message = post.title + " | " + post.shortlink

                        sc.api_call(
                            'chat.postMessage',
                            channel='#alerts',
                            username='New Post Alert',
                            text=message
                        )

                        url = 'https://discordapp.com/api/webhooks/<your web hook token here>'
                        payload = { "content": message }
                        headers = { 'Content-Type': 'application/json', }
                        requests.post(url, data=json.dumps(payload), headers=headers)

                    seen.append(post.id)

        time.sleep(5)
        first = False
    except KeyboardInterrupt:
        print('\n')
        sys.exit(0)
    except Exception as e:
        print(e)
        time.sleep(5)
