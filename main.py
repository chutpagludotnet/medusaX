import os
import re
import sys
import m3u8
import json
import time
import pytz
import asyncio
import requests
import subprocess
import urllib
import urllib.parse
import yt_dlp
import tgcrypto
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from logs import logging
from bs4 import BeautifulSoup
import medusaxd as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT
from aiohttp import ClientSession
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
import random
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp
import aiofiles
import zipfile
import shutil
import ffmpeg

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

AUTH_USER = os.environ.get('AUTH_USERS', '7527795504').split(',')
AUTH_USERS = [int(user_id) for user_id in AUTH_USER]
if int(OWNER) not in AUTH_USERS:
    AUTH_USERS.append(int(OWNER))
CHANNEL_OWNERS = {}
CHANNELS = os.environ.get('CHANNELS', '').split(',')
CHANNELS_LIST = [int(channel_id) for channel_id in CHANNELS if channel_id.isdigit()]
cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")
api_url = "http://master-api-v3.vercel.app/"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"
token_cp ='eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'
adda_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJkcGthNTQ3MEBnbWFpbC5jb20iLCJhdWQiOiIxNzg2OTYwNSIsImlhdCI6MTc0NDk0NDQ2NCwiaXNzIjoiYWRkYTI0Ny5jb20iLCJuYW1lIjoiZHBrYSIsImVtYWlsIjoiZHBrYTU0NzBAZ21haWwuY29tIiwicGhvbmUiOiI3MzUyNDA0MTc2IiwidXNlcklkIjoiYWRkYS52MS41NzMyNmRmODVkZDkxZDRiNDkxN2FiZDExN2IwN2ZjOCIsImxvZ2luQXBpVmVyc2lvbiI6MX0.0QOuYFMkCEdVmwMVIPeETa6Kxr70zEslWOIAfC_ylhbku76nDcaBoNVvqN4HivWNwlyT0jkUKjWxZ8AbdorMLg"
photologo = 'https://tinypic.host/images/2025/02/07/DeWatermark.ai_1738952933236-1.png' #https://envs.sh/GV0.jpg
photoyt = 'https://tinypic.host/images/2025/03/18/YouTube-Logo.wine.png' #https://envs.sh/GVi.jpg
photocp = 'https://tinypic.host/images/2025/03/28/IMG_20250328_133126.jpg'
photozip = 'https://envs.sh/cD_.jpg'

async def show_random_emojis(message):
    emojis = ['🐼', '🐶', '🐅', '⚡️', '🚀', '✨', '💥', '☠️', '🥂', '🍾', '📬', '👻', '👀', '🌹', '💀', '🐇', '⏳', '🔮', '🦔', '📖', '🦁', '🐱', '🐻‍❄️', '☁️', '🚹', '🚺', '🐠', '🦋']
    emoji_message = await message.reply_text(' '.join(random.choices(emojis, k=1)))
    return emoji_message

# Inline keyboard for start command
BUTTONSCONTACT = InlineKeyboardMarkup([[InlineKeyboardButton(text="📞 Contact", url="https://t.me/saini_contact_bot")]])
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/+3k-1zcJxINYwNGZl"),
            InlineKeyboardButton(text="🛠️ Repo", url="https://github.com/cyberseller999/saini-txt-direct"),
        ],
    ]
)

# Image URLs for the random image feature
image_urls = [
    "https://tinypic.host/images/2025/02/07/IMG_20250207_224444_975.jpg",
    "https://tinypic.host/images/2025/02/07/DeWatermark.ai_1738952933236-1.png",
    # Add more image URLs as needed
]

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    # Get user's first name
    first_name = message.from_user.first_name

    # Create the welcome message
    welcome_text = f"""
<b>👋 Hello {first_name}!</b>

Welcome to the Text To Video Extractor Bot! I can help you extract and process videos from various sources.

<b>🤖 Bot Commands:</b>
• Send me a video URL or text link to extract the video
• /addauth [user_id] - Add authorized user (owner only)
• /remauth [user_id] - Remove authorized user (owner only)
• /users - List all authorized users (owner only)
• /addchnl [channel_id] - Add a channel (-100...)
• /remchnl [channel_id] - Remove a channel
• /channels - List all authorized channels
• /cookies - Upload YouTube cookies file
• /help - Show this help message

<b>Powered by {CREDIT}</b>
"""

    # Send the welcome message with the logo image
    await client.send_photo(
        chat_id=message.chat.id,
        photo=photologo,
        caption=welcome_text,
        reply_markup=keyboard
    )

@bot.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    help_text = f"""
<b>📚 Bot Commands Guide</b>

<b>👤 User Management:</b>
• /addauth [user_id] - Add an authorized user (owner only)
• /remauth [user_id] - Remove an authorized user (owner only)
• /users - List all authorized users (owner only)

<b>📢 Channel Management:</b>
• /addchnl [channel_id] - Add a channel (must start with -100)
• /remchnl [channel_id] - Remove a channel
• /channels - List all authorized channels

<b>🔧 Other Functions:</b>
• /cookies - Upload YouTube cookies file for accessing restricted content
• Send any video URL or text link to extract the video

<b>How to use:</b>
1. Add the bot to your desired channel
2. Use /addchnl to authorize the channel
3. Send video links to extract and process videos

<b>Powered by {CREDIT}</b>
"""
    await message.reply_text(help_text, reply_markup=keyboard)

@bot.on_message(filters.command("addauth") & filters.private)
async def add_auth_user(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command.")

    try:
        new_user_id = int(message.command[1])
        if new_user_id in AUTH_USERS:
            await message.reply_text("User ID is already authorized.")
        else:
            AUTH_USERS.append(new_user_id)
            # Update the environment variable (if needed)
            os.environ['AUTH_USERS'] = ','.join(map(str, AUTH_USERS))
            await message.reply_text(f"User ID {new_user_id} added to authorized users.")
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid user ID.")

@bot.on_message(filters.command("remauth") & filters.private)
async def remove_auth_user(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command.")

    try:
        user_id_to_remove = int(message.command[1])
        if user_id_to_remove not in AUTH_USERS:
            await message.reply_text("User ID is not in the authorized users list.")
        else:
            AUTH_USERS.remove(user_id_to_remove)
            # Update the environment variable (if needed)
            os.environ['AUTH_USERS'] = ','.join(map(str, AUTH_USERS))
            await message.reply_text(f"User ID {user_id_to_remove} removed from authorized users.")
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid user ID.")

@bot.on_message(filters.command("users") & filters.private)
async def list_auth_users(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command.")

    user_list = '\n'.join(map(str, AUTH_USERS))
    await message.reply_text(f"<blockquote>Authorized Users:</blockquote>\n{user_list}")

@bot.on_message(filters.command("addchnl") & filters.private)
async def add_channel(client: Client, message: Message):
    if message.from_user.id not in AUTH_USERS:
        return await message.reply_text("You are not authorized to use this command.")

    try:
        new_channel_id = int(message.command[1])

        # Validate that the channel ID starts with -100
        if not str(new_channel_id).startswith("-100"):
            return await message.reply_text("Invalid channel ID. Channel IDs must start with -100.")

        if new_channel_id in CHANNELS_LIST:
            await message.reply_text("Channel ID is already added.")
        else:
            CHANNELS_LIST.append(new_channel_id)
            CHANNEL_OWNERS[new_channel_id] = message.from_user.id  # Assign the user as the owner of the channel
            # Update the environment variable (if needed)
            os.environ['CHANNELS'] = ','.join(map(str, CHANNELS_LIST))
            await message.reply_text(f"Channel ID {new_channel_id} added to the list and you are now the owner.")
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid channel ID.")

@bot.on_message(filters.command("remchnl") & filters.private)
async def remove_channel(client: Client, message: Message):
    try:
        channel_id_to_remove = int(message.command[1])

        # Check if the channel exists in the list
        if channel_id_to_remove not in CHANNELS_LIST:
            return await message.reply_text("Channel ID is not in the list.")

        # Check if the user is the OWNER or the channel owner
        if message.from_user.id != OWNER and CHANNEL_OWNERS.get(channel_id_to_remove) != message.from_user.id:
            return await message.reply_text("You are not authorized to remove this channel.")

        # Remove the channel
        CHANNELS_LIST.remove(channel_id_to_remove)
        if channel_id_to_remove in CHANNEL_OWNERS:
            del CHANNEL_OWNERS[channel_id_to_remove]  # Remove from the ownership dictionary if present

        # Update the environment variable (if needed)
        os.environ['CHANNELS'] = ','.join(map(str, CHANNELS_LIST))
        await message.reply_text(f"Channel ID {channel_id_to_remove} removed from the list.")
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid channel ID.")

@bot.on_message(filters.command("channels") & filters.private)
async def list_channels(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command.")

    if not CHANNELS_LIST:
        await message.reply_text("No channels have been added yet.")
    else:
        channel_list = '\n'.join(map(str, CHANNELS_LIST))
        await message.reply_text(f"<blockquote>Authorized Channels:</blockquote>\n{channel_list}")

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    await m.reply_text(
        "Please upload the cookies file (.txt format).",
        quote=True
    )

    try:
        # Wait for the user to send the cookies file
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file
        downloaded_path = await input_message.download()

        # Save the cookies file
        with open(cookies_file_path, "wb") as cookies_file:
            with open(downloaded_path, "rb") as uploaded_file:
                cookies_file.write(uploaded_file.read())

        await m.reply_text("✅ YouTube cookies file has been successfully updated!")

        # Clean up the downloaded file
        if os.path.exists(downloaded_path):
            os.remove(downloaded_path)

    except Exception as e:
        await m.reply_text(f"An error occurred: {str(e)}")

# Add more command handlers and functionality as needed

if __name__ == "__main__":
    bot.run()
