import sys
import praw
import time

user = 'Midasx'
reddits = ['vim']
seen = []

r = praw.Reddit(user_agent='NewPost',
                client_id='RGtz43e2ZuuuoA',
                client_secret='*******************',
                username='NewPostAlert',
                password='***********',)

print("Logged in")

first = True

while True:
    try:
        for sub in reddits:
            for post in r.subreddit(sub).new(limit=10):
                if first is True:
                    seen.append(post.id)
                if post.id not in seen:
                    subject = 'New post in ' + str(post.subreddit)
                    content = '[' + post.title + '](' + post.shortlink + ')'
                    r.redditor(user).message(subject, content)
                    print('New post! Sending PM.')
                    seen.append(post.id)

        time.sleep(5)
        first = False
    except KeyboardInterrupt:
        print('\n')
        sys.exit(0)
    except Exception as e:
        print(e)
