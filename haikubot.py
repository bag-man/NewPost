import sys
import praw
import time
import pafy
from urllib import parse

reddits = ['youtubehaikuclassic']
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
                    content = post.title + " | " + post.shortlink
                    choices = post.flair.choices()

                    if post.domain != 'youtube.com' and post.domain != 'youtu.be':
                        #print(content + " | " + post.domain)

                        post.flair.select(choices[3]["flair_template_id"])
                        post.reply("Hey /u/" + str(post.author) + " your submission was not a YouTube link so we had to remove it! :(")
                        post.mod.remove()
                    else:
                        video = pafy.new(post.url)

                        duration = video.duration.split(":")
                        duration[0] = int(duration[0]) * 60 * 60
                        duration[1] = int(duration[1]) * 60
                        duration[2] = int(duration[2])
                        duration = sum(duration)

                        try:
                            timestamp = int(parse.parse_qs(parse.urlparse(post.url).query)['t'][0])
                        except:
                            timestamp = False

                        if timestamp:
                            duration -= timestamp

                        #print(content + " | " + post.url + " | " + video.duration + " | " + str(duration))

                        if duration > 30:
                            post.flair.select(choices[2]["flair_template_id"])
                            post.reply("Hey /u/" + str(post.author) + " your submission was longer than 30 seconds so we had to remove it :(")
                            post.mod.remove()
                        elif duration > 15:
                            post.flair.select(choices[0]["flair_template_id"])
                            post.mod.approve()
                        else:
                            post.flair.select(choices[1]["flair_template_id"])
                            post.mod.approve()

                    seen.append(post.id)

        time.sleep(5)
        first = False
    except KeyboardInterrupt:
        print('\n')
        sys.exit(0)
    except Exception as e:
        print(e)
