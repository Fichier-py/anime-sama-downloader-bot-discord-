# 📺 Anime Downloader Discord Bot

The Anime Downloader Discord Bot is a Python-based automation project that allows users to search, download, and retrieve anime episodes directly from Discord. It combines Discord.py, yt-dlp, Flask, and ngrok to build a complete pipeline from user commands to downloadable video links.

The bot is designed to simplify anime episode retrieval by automating web scraping, video downloading, local file hosting, and public link generation.

---

## 🧠 How it works

The system is built around three main components:

### 1. Discord Interface
The bot acts as the main interface. Users interact through commands to define:
- anime name
- season
- language
- episode range

These values are temporarily stored in memory and used to build requests.

---

### 2. Episode extraction & downloading
When the download command is triggered, the bot:
- builds a URL based on user input
- fetches the anime catalog page
- extracts video links using regex

Supported sources:
- sibnet.ru
- sendvid.com

The extracted links are downloaded using `yt-dlp` and saved locally as `.mp4` files.

---

### 3. File hosting & sharing
A Flask server runs in the background to serve downloaded files. ngrok exposes this server to the internet, generating a public URL.

These links are sent back to Discord so users can download the videos. Afterward, files are automatically deleted.

---

## ⚙️ Commands

### 🎬 !anime <name>
Defines the anime to download.

Examples:
- `!anime frieren`
- `!anime attack-on-titan`

---

### 📀 !season <number>
Sets the anime season.

Example:
- `!season 1`

---

### 🈯 !language <vf/vostfr/vf1/vf2>
Sets the audio/subtitle language.

Options:
- vf
- vf1
- vf2
- vostfr

---

### ⬇️ !run <start-end>
Main command to download episodes.

Examples:
- `!run 1-1`
- `!run 1-2`

Limit:
- maximum 2 episodes per request

---

### 📁 !files
Generates public download links for all `.mp4` files stored locally using Flask + ngrok.

---

### ❓ !help
Displays all available commands and usage rules.

---

## 📦 Installation

Before running the bot, make sure you have Python 3.10 or higher installed on your system. The bot depends on several external libraries, so a proper setup is required for everything to work correctly.

All dependencies can be installed automatically using the requirements file provided with the project:

pip install -r requirements.txt

This installs all required packages at once:
- Discord.py (bot functionality)
- requests (HTTP requests)
- yt-dlp (video downloading)
- Flask (local server)
- pyngrok (public tunnel)

If you do not have a requirements file, install everything manually:

pip install discord.py requests yt-dlp flask pyngrok

FFmpeg is strongly recommended for proper video handling and format compatibility.

On Windows:
- Download FFmpeg from the official website
- Add it to system PATH

On Linux:

sudo apt update
sudo apt install ffmpeg

After installation, verify your setup by checking Python and installed packages. If imports work without errors, the bot is ready to run.
