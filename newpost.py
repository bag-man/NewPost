import sys
import praw
import time
import requests
import json

CONFIG_FILE='config.json'

def check_new_posts(sub):
    for post in r.subreddit(sub).new(limit=10):
        if first is True:
            seen_posts.append(post.id)
        if config['keywords']['enabled'] and not any(x.lower() in post.title.lower() for x in config['keywords']['list']):
            seen_posts.append(post.id)
        if post.id not in seen_posts:
            notify(sub, post.title, post.shortlink)
        seen_posts.append(post.id)

def check_modqueue(sub):
    for item in r.subreddit(sub).mod.modqueue(limit=None):
        if first is True:
            seen_modqueue.append(item.id)
        if item.id not in seen_modqueue:
            url = 'https://reddit.com' + item.permalink
            notify(sub, 'Modqueue', url)
            seen_modqueue.append(item.id)

def notify(subreddit, title, url):
    if config['discord']['enabled']:
        notify_discord(subreddit, title, url)
    if config['slack']['enabled']:
        notify_slack(subreddit, title, url)
    if config['reddit_pm']['enabled']:
        notify_reddit(subreddit, title, url)
    if config['telegram']['enabled']:
        notify_telegram(subreddit, title, url)
    if config['debug']:
        print(subreddit + ' | ' + title + ' | ' +  url)

def notify_discord(subreddit, title, url):
    message = title + " | <" + url + ">"
    payload = { 'content': message }
    headers = { 'Content-Type': 'application/json', }
    requests.post(config['discord']['webhook'], data=json.dumps(payload), headers=headers)

def notify_slack(subreddit, title, url):
    message = title + " | " + url
    payload = { 'text': message }
    headers = { 'Content-Type': 'application/json', }
    requests.post(config['slack']['webhook'], data=json.dumps(payload), headers=headers)

def notify_reddit(subreddit, title, url):
    if title is 'Modqueue':
        subject = 'New item in modqueue on /r/' + subreddit + '!'
    else:
        subject = 'New post on /r/' + subreddit + '!'

    message = '[' + title + '](' + url + ')'

    for user in config['reddit_pm']['users']:
        r.redditor(user).message(subject, message)

def notify_telegram(subreddit, title, url):
    message = '<b>[/r/{}]</b> {} - {}'.format(subreddit, title, url)
    payload = { 
        'chat_id': config['telegram']['chat_id'],
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.post("https://api.telegram.org/bot{}/sendMessage".format(config['telegram']['token']),
                  data=payload)

with open(CONFIG_FILE) as config_file:
    config = json.load(config_file)

r = praw.Reddit(
    user_agent = config['reddit']['user_agent'],
    client_id = config['reddit']['client_id'],
    client_secret = config['reddit']['client_secret'],
    username = config['reddit']['username'],
    password = config['reddit']['password']
)

seen_posts = []
seen_modqueue = []
first = True

while True:
    try:
        for sub in config['subreddits']:
            if config['modqueue']:
                check_modqueue(sub)
            if config['new_posts']:
                check_new_posts(sub)

            time.sleep(5)
            first = False
    except KeyboardInterrupt:
        print('\n')
        sys.exit(0)
    except Exception as e:
        print('Error:', e)
        time.sleep(5)


