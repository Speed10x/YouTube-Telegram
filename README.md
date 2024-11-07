# # YouTube Telegram Bot

This Telegram bot mirrors YouTube content with a YouTube-like UI, supports live streaming, and offers download functionality.

## Features

- YouTube-like UI within Telegram
- Video search functionality
- Trending videos display
- Video playback (streaming)
- Video download option with quality selection
- Inline navigation
- Periodic updates of trending videos

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/youtube-telegram-bot.git
   cd youtube-telegram-bot
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Telegram Bot:
   - Create a new bot on Telegram by talking to [@BotFather](https://t.me/BotFather)
   - Get your API ID and API Hash from [Telegram's developer portal](https://my.telegram.org/apps)

4. Set up your YouTube Data API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project and enable the YouTube Data API v3
   - Create credentials (API Key) for the YouTube Data API

5. Set your environment variables:
   ```
   export TELEGRAM_API_ID=your_api_id
   export TELEGRAM_API_HASH=your_api_hash
   export TELEGRAM_BOT_TOKEN=your_bot_token
   export YOUTUBE_API_KEY=your_youtube_api_key
   ```

## Usage

1. Start a chat with your bot on Telegram.
2. Use the following commands:
   - `/start`: Get a welcome message and instructions
   - `/search`: Search for YouTube videos
   - `/trending`: See trending YouTube videos
3. Use the inline buttons to play or download videos in different qualities.

## Deployment on Render

1. Fork this repository to your GitHub account.

2. Sign up for a [Render](https://render.com/) account if you haven't already.

3. In Render, create a new Web Service and connect it to your GitHub repository.

4. Configure the Web Service:
   - Environment: Docker
   - Build Command: (leave empty)
   - Start Command: (leave empty)

5. Add the environment variables in the Render dashboard:
   - `TELEGRAM_API_ID`
   - `TELEGRAM_API_HASH`
   - `TELEGRAM_BOT_TOKEN`
   - `YOUTUBE_API_KEY`

6. Click "Create Web Service" to deploy your bot.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
