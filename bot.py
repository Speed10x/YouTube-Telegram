import os
import asyncio
from telethon import TelegramClient, events, Button
from telethon.tl.types import InputWebDocument
from googleapiclient.discovery import build
import yt_dlp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp
from flask import Flask
from threading import Thread
import tempfile
from telethon.errors import TimeoutError

# Configuration
API_ID = os.environ.get('TELEGRAM_API_ID')
API_HASH = os.environ.get('TELEGRAM_API_HASH')
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

# Initialize the Telegram client
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Initialize the YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# YoutubeDL configuration
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "YouTube Telegram Bot is running!"

# Helper function to create a YouTube-like UI
async def create_youtube_ui(title, description, thumbnail_url, video_id):
    keyboard = [
        [Button.url("▶️ Watch on YouTube", f"https://www.youtube.com/watch?v={video_id}")],
        [Button.inline("🔍 Search", data="search"), Button.inline("🔥 Trending", data="trending")]
    ]
    
    return {
        'title': title,
        'description': description,
        'thumb_url': thumbnail_url,
        'buttons': keyboard
    }

# Helper function to download thumbnail
async def download_thumbnail(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                f = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                f.write(await response.read())
                f.close()
                return f.name
    return None

# Handler for /start command
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("Welcome to the YouTube Telegram Bot! 🎥\n"
                      "Use /search to find videos or /trending to see what's popular.")

# Handler for /search command
@bot.on(events.NewMessage(pattern='/search'))
async def search(event):
    sender = await event.get_sender()
    async with bot.conversation(sender) as conv:
        await conv.send_message("What would you like to search for?")
        try:
            response = await conv.get_response(timeout=30)
            query = response.text
            search_response = youtube.search().list(q=query, type='video', part='id,snippet', maxResults=5).execute()
            
            for item in search_response['items']:
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                description = item['snippet']['description']
                thumbnail_url = item['snippet']['thumbnails']['default']['url']
                
                ui = await create_youtube_ui(title, description, thumbnail_url, video_id)
                thumb_path = await download_thumbnail(ui['thumb_url'])
                if thumb_path:
                    await conv.send_file(thumb_path, caption=f"**{ui['title']}**\n\n{ui['description']}", buttons=ui['buttons'])
                    os.unlink(thumb_path)
                else:
                    await conv.send_message(f"**{ui['title']}**\n\n{ui['description']}", buttons=ui['buttons'])
        except TimeoutError:
            await conv.send_message("Search request timed out. Please try again.")

# Handler for /trending command
@bot.on(events.NewMessage(pattern='/trending'))
async def trending(event):
    trending_response = youtube.videos().list(part='id,snippet', chart='mostPopular', regionCode='US', maxResults=5).execute()
    
    for item in trending_response['items']:
        video_id = item['id']
        title = item['snippet']['title']
        description = item['snippet']['description']
        thumbnail_url = item['snippet']['thumbnails']['default']['url']
        
        ui = await create_youtube_ui(title, description, thumbnail_url, video_id)
        thumb_path = await download_thumbnail(ui['thumb_url'])
        if thumb_path:
            await event.reply(file=thumb_path, caption=f"**{ui['title']}**\n\n{ui['description']}", buttons=ui['buttons'])
            os.unlink(thumb_path)
        else:
            await event.reply(f"**{ui['title']}**\n\n{ui['description']}", buttons=ui['buttons'])

# Handler for inline button callbacks
@bot.on(events.CallbackQuery())
async def callback(event):
    data = event.data.decode('utf-8')
    if data == 'search':
        await event.answer("Use /search to find videos")
    elif data == 'trending':
        await event.answer("Fetching trending videos...")
        await trending(event)

# Scheduler for updating trending videos
scheduler = AsyncIOScheduler()

async def update_trending():
    trending_response = youtube.videos().list(part='id,snippet', chart='mostPopular', regionCode='US', maxResults=5).execute()
    # Here you would update a database or cache with the new trending videos
    print("Updated trending videos")

scheduler.add_job(update_trending, 'interval', hours=1)
scheduler.start()

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# Start the bot
if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    bot.run_until_disconnected()
