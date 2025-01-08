import discord
import praw
import random
import requests
import instaloader
import asyncio
from discord.ext import commands, tasks
from io import BytesIO
import os

# initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# initialize reddit api
reddit = praw.Reddit(client_id='eFlQA2036d6HB6Yb69GDBA',
                     client_secret='N6Ba0uB0vSL2W9L0VxmAeoaYA0i-DA',
                     user_agent='discord-cat-bot')

# initialize instagram api
insta_loader = instaloader.Instaloader()

instagram_username = 'catbotdiscord'
instagram_password = 'catbotpassword'

def login_instagram():
    try:
        # check if session file exists and load it
        session_file = f"{instagram_username}_session"
        if os.path.exists(session_file):
            insta_loader.load_session_from_file(instagram_username)
            print("Session loaded from file.")
        else:
            print("No session found. Logging in with username and password...")
            insta_loader.context.log("Logging in with username and password...")
            insta_loader.login(instagram_username, instagram_password)
            insta_loader.save_session_to_file()  # save session to file for future use
            print("Session saved to file.")
    except Exception as e:
        print(f"Error logging in to Instagram: {e}")


# list of subreddits to fetch cat images from
subreddits = ['cat', 'cats', 'CatsStandingUp', 'CatTaps', 'Catswithjobs', 'WhatsWrongWithYourCat', 'CatSmiles', 'NameMyCatcatpictures', 'sillycats', 'catpics']

# list of instagram accounts to fetch cat images from
instagram_users = ['fatfatpankocat']

# fetch random cat image from reddit
def fetch_reddit_cat():
    subreddit = random.choice(subreddits)
    posts = reddit.subreddit(subreddit).top('hour', limit=200)
    post = random.choice([post for post in posts if post.url.endswith(('jpg', 'jpeg', 'png'))])
    return post.url

# fetch random cat image from instagram
def fetch_instagram_cat():
    user = random.choice(instagram_users)
    posts = instaloader.Profile.from_username(insta_loader.context, user).get_posts()
    post = random.choice([post for post in posts if post.url.endswith(('jpg', 'jpeg', 'png'))])
    return post.url

# fetch panko cat image
def fetch_panko_cat():
    user = 'fatfatpankocat'
    posts = instaloader.Profile.from_username(insta_loader.context, user).get_posts()
    post = random.choice([post for post in posts if post.url.endswith(('jpg', 'jpeg', 'png'))])
    return post.url

# send cat image to discord channel
async def send_cat_image(channel):
    try:
        # fetch a random cat image from reddit or instagram
        image_source = fetch_reddit_cat
        image_url = image_source()

        # send image to discord
        response = requests.get(image_url)
        img = BytesIO(response.content)
        await channel.send(file=discord.File(img, 'cat.jpg'))
    except Exception as e:
        print(f"failed to get a cat picture because luka is a fucking idiot: {e}")

# send panko image to discord channel
async def send_panko_image(channel):
    try:
        # fetch panko cat image
        image_source = fetch_panko_cat
        image_url = image_source()

        # send image to discord
        response = requests.get(image_url)
        img = BytesIO(response.content)
        await channel.send(file=discord.File(img, 'cat.jpg'))
    except Exception as e:
        print(f"failed to get a cat picture because luka is a fucking idiot: {e}")

# command to send cat image when someone types !cat
@bot.command()
async def cat(ctx):
    await send_cat_image(ctx.channel)

# command to send cat image when someone types !panko
@bot.command()
async def panko(ctx):
    await send_panko_image(ctx.channel)        

# background task to post cat images on a timer
@tasks.loop(minutes=15)
async def post_cat_on_timer():
    channel = bot.get_channel(1326534078803083295)
    await send_cat_image(channel)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    login_instagram()  # log in to instagram before starting the tasks
    post_cat_on_timer.start()  # start the periodic posting task

# run the bot
bot.run('MTMyNjUyODY0MzI0MDk1NTk5NA.GeOzAT.-XH8yMwy2G2nB4vKH4BvT16fXGkM1HU-qC7bj8')
