import discord
import requests
import json
from discord.ext import commands
import os
import re
import yt_dlp
from yt_dlp.utils import DownloadError
from flask import Flask , send_file
import threading
import time
from pyngrok import ngrok
from urllib.parse import quote

app = Flask(__name__)





intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}
@bot.command()
async def aide(ctx):
    embed = discord.Embed(
        title="📺 Bot Anime Downloader",
        description="Commandes disponibles et utilisation",
        color=discord.Color.blue()
    )

    # Commandes
    embed.add_field(
        name="🎬 !anime <nom>",
        value="Définit l'anime à télécharger\nEx: !anime frieren\n⚠️ Remplace les espaces par des tirets\nEx: attack-on-titan",
        inline=False
    )

    embed.add_field(
        name="📀 !saison <numéro>",
        value="Choisit la saison\nEx: !saison 1\n⚠️ Ne pas écrire 'saison1'",
        inline=False
    )

    embed.add_field(
        name="🈯 !langue <vf/vostfr>",
        value="Choisit la langue\nEx: !langue vf\n\n"
              "Si plusieurs VF existent :\n"
              "- vf (par défaut)\n"
              "- vf1\n"
              "- vf2\n"
              "(ex: Netflix / Crunchyroll)",
        inline=False
    )

    embed.add_field(
        name="⬇️ !run <début-fin>",
        value="Télécharge les épisodes\n"
              "Ex:\n"
              "- !run 1-1 → 1 épisode\n"
              "- !run 1-2 → max 2 épisodes",
        inline=False
    )

    embed.add_field(
        name="📁 !fichiers",
        value="Génère les liens de téléchargement des fichiers MP4",
        inline=False
    )

    # Règles importantes
    embed.add_field(
        name="⚠️ Règles importantes",
        value="✔️ Faire !anime + !saison + !langue avant !run\n"
              "✔️ Maximum 2 épisodes par téléchargement\n"
              "❌ Ne pas utiliser le bot à plusieurs en même temps",
        inline=False
    )

    embed.set_footer(text="Bot anime downloader")

    await ctx.send(embed=embed)

@bot.command()
async def anime(ctx, * ,  message1):
    global message_anime
    message_anime = message1
    await ctx.send(f"l'anime {message1} est enregistré.")

@bot.command()
async def saison (ctx , * , message2):
    global message_saison
    message_saison = message2
    await ctx.send(f"la saison {message2} est enregistré.")
@bot.command()
async def langue (ctx , * , message3):
    global message_langue
    message_langue = message3
    await ctx.send (f"la langue {message3}est enregistré.")

@bot.command()
async def run (ctx , message4):
    message_nb_ep = message4

    debut , fin = message_nb_ep.split("-")
    debut = int(debut)
     
    fin = int(fin)
    if fin - debut > 2:
        await ctx.send("Tu ne peux pas télécharger plus de 2 épisodes à la fois.")
        return
    for i in range(debut -1 , fin):
        global nb_ep_anime
        message_nb_ep = i
        response = requests.get(f"https://anime-sama.to/catalogue/{message_anime}/saison{message_saison}/{message_langue}/episodes.js?filever=124")
        await ctx.send(response.url)
        sibnet = re.findall(r'https://video\.sibnet\.ru/[^\s\'"]+', response.text)
        sendvid = re.findall(r'https://sendvid.com/[^\s\'"]+',response.text)
        if sibnet:
            try:
                ep = sibnet[message_nb_ep]
                url = ep
                ydl_opts = {"outtmpl" :'%(title)s.%(ext)s',
                        "format" : "best" , 'socket_timeout': 60,  }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                await ctx.send("Téléchargement terminé. Veuillez faire !fichiers pour obtenir le lien.")

            except IndexError:
                await ctx.send("Tu as écrit une mauvaise information. Vérifie bien le titre, la saison ou la langue si elle est disponible.")
            except OSError:
                await ctx.send("Il n’y a plus de stockage sur le serveur. Veuillez attendre ou appeler le développeur.")
            except DownloadError:
                await ctx.send("Il y a un problème de téléchargement. Recommencez, vous vous êtes peut-être trompé. Veuillez contacter le développeur si le problème persiste.")


        elif not sibnet:
            try:
                ep = sendvid[message_nb_ep]
                url = ep
                ydl_opts = {"outtmpl" : "%(title)s.%(ext)s", 
                        "format" : "best"  , 'socket_timeout': 60,}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                await ctx.send("Téléchargement terminé. Veuillez faire !fichiers pour obtenir le lien.")

            except IndexError:
                await ctx.send("Tu as écrit une mauvaise information. Vérifie bien le titre, la saison ou la langue si elle est disponible.")
            except OSError:
                await ctx.send("Il n’y a plus de stockage sur le serveur. Veuillez attendre ou appeler le développeur.")
            except DownloadError:
                await ctx.send("Il y a un problème de téléchargement. Recommencez, vous vous êtes peut-être trompé. Veuillez contacter le développeur si le problème persiste.")

ton_ip = "your ip"
DOSSIER = os.path.dirname(os.path.abspath(__file__))

def get_all_mp4():
    return [f for f in os.listdir(DOSSIER) if f.lower().endswith(".mp4")]

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(DOSSIER, filename), as_attachment=True)

def run_flask():
    app.run(host="0.0.0.0", port=80)  # IP publique + port serveur

threading.Thread(target=run_flask, daemon=True).start()  # lance Flask en arrière-
ngrok.set_auth_token("NGROK TOKEN")
time.sleep(1)

public_url = ngrok.connect(80).public_url

@bot.command()
async def fichiers(ctx):
    files = get_all_mp4()

    if not files:
        await ctx.send("Aucun fichier trouvé.")
        return

    for f in files:
        await ctx.send(f"{public_url}/download/{quote(f)}")
        time.sleep(10)
        for fichier in os.listdir("."):
            if fichier.endswith(".mp4"):
                os.remove(fichier)

bot.run("DISCORD TOKEN")


