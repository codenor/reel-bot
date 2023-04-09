from __future__ import unicode_literals
from yt_dlp import YoutubeDL
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re

intents = discord.Intents.all()
client = discord.Client(intents=intents)

load_dotenv()
token = os.getenv("TOKEN")

@client.event
async def on_ready():
    print("Bot is ready and running!")

@client.event
async def on_message(message):
    link = "https://www.instagram.com/reel/"
    if link in message.content:
        user_message = str(message.content)
        try:
            convert_message = (re.search("(?P<url>https?://.*?/reel/[^/\s]+)", user_message).group("url"))
        except AttributeError:
            # no match, ignore message
            return
        try:
            async with message.channel.typing():
                ydl_opts = {
                    'outtmpl': 'media/%(extractor)s-%(id)s.%(ext)s',
                    'noplaylist': True,
                    'quiet': True,
                    'no_warnings': True,
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                    'cookiefile': 'cookies.txt',
                }
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(convert_message, download=True)
                    filename = ydl.prepare_filename(info)
                    if os.path.getsize(filename) < 25 * 1024 * 1024:
                        await message.reply(mention_author=False ,file=discord.File(f"{filename}"))
                        await message.edit(suppress=True)
                        os.remove(f"{filename}")
                    else:
                        print(f"Unable to send {filename} file exceeds 25mb")
                        os.remove(f"{filename}")
        except:
            return
        
client.run(token)