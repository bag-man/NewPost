# New Post & ModQueue alert
This script will monitor a list of subreddits for new posts and items in the modqueue. It can then send a message to a slack or discord channel and a private message to a list of users on reddit. 

You just need praw, so run:

    pip install -r requirements.txt

To install the dependencies. You then need to configure copy the `config.json.template` file to `config.json` and update it with the api keys and settings you want. 

### Reddit 
Create your bot / mod account and go to: https://www.reddit.com/prefs/apps/. Create an app and it will give you the credentials you need. 

### Slack
Create a slack app and get a webhook for the channel you would like to post to: https://api.slack.com/incoming-webhooks#getting-started. 

### Discord
In your server settings create a webhook: https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks

### Reddit PM's
Just fill in the usernames you want to be notified in the array. i.e `"users": [ "Isa", "Owen" ],`

### Features
Then just set enabled to true on the notifications you want. You can also disable modqueue or post checking by setting mosqueue or new_posts to false. If you want to listen for only certain keywords you can add a list and enable that too. 

## ToDo
This is still a WIP and an ever evolving project:

* Write some tests for it
* Try and cover more error cases
* Modmail notifications
* Make into a PyPI module and or systemd service
