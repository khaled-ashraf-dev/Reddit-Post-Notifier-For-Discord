import praw
import discord
from discord.ext import tasks

# Enter The Discord Bot's Token
TOKEN = 'Token-Here'

# Enter the channel ID here
# You can get it from the discord server by right-clicking on the channel and clicking 'Copy ID'
channel_id = 1031480065113985076

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Enter Your Reddit App Data
# Leave check_for_async Unchanged
reddit = praw.Reddit(client_id='client-id-here', \
                     client_secret='client-secret-here', \
                     user_agent='user-agent-here', \
                     check_for_async=False)

# Replace self with your target subreddit
subreddit = reddit.subreddit('self')

# Storing posts' IDs
ids = []

# Checking for new posts every 5 seconds
@tasks.loop(seconds=5)
async def notifier():
    channel = client.get_channel(channel_id)
    
    for submission in subreddit.new(limit=5):
        post_id = submission.id
        title = submission.title
        body = submission.selftext
        author = submission.author
        sub_name = submission.subreddit_name_prefixed
        url = "https://www.reddit.com" + submission.permalink
        
        if body:
            body = ' '.join(body.split()[:20]) + '...'

        # Creating An Embed 
        embed=discord.Embed(title=title, url=url, description=body, color=0xef2929)
        embed.set_thumbnail(url="https://www.iconpacks.net/icons/2/free-reddit-logo-icon-2436-thumb.png")
        embed.add_field(name=sub_name, value=author, inline=False)
        
        # Sending The Message If The Post ID Was Not Used Before
        if not post_id in ids:
            ids.append(post_id)
            await channel.send(embed=embed)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    notifier.start()

# Running The Bot
client.run(TOKEN)