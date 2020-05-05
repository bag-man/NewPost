import sys
import praw
import time
import requests
import json

CONFIG_FILE='config.json'

def handle_post(submission):
    url = submission.shortlink
    title = submission.title
    sub = submission.subreddit.display_name

    if config['keywords']['enabled']:
        if any(x.lower() in post.title.lower() for x in config['keywords']['list']):
            notify(sub, title, url)
    else:
        notify(sub, title, url)

def handle_modqueue(item):
    url = 'https://reddit.com' + item.permalink
    sub = item.subreddit.display_name
    notify(sub, 'Modqueue', url)

def notify(subreddit, title, url):
    if first: return
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

first = True
subreddits = '+'.join(config['subreddits'])
modqueue_stream = (r.subreddit('mod').mod.stream.modqueue(pause_after=-1)
                   if config['modqueue'] else [])
submission_stream = (r.subreddit(subreddits).stream.submissions(pause_after=-1)
                     if config['new_posts'] else [])

while True:
    try:
        for item in modqueue_stream:
            if item is None:
                break
            handle_modqueue(item)

        for submission in submission_stream:
            if submission is None:
                break
            handle_post(submission)

        first = False
        time.sleep(1)
    except KeyboardInterrupt:
        print('\n')
        sys.exit(0)
    except Exception as e:
        print('Error:', e)
        time.sleep(30)


