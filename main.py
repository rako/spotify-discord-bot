import requests
import discord
from discord.ext import commands
import os

discord_token = os.environ.get("DISCORD_TOKEN")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

def search_spotify(keyword):
  # spotifyの認証
  auth_response = requests.post(
    "https://accounts.spotify.com/api/token",
    data = {
      "grant_type": "client_credentials",
      "client_id": client_id,
      "client_secret": client_secret
    },
  )

  response_json = auth_response.json()
  token = response_json["access_token"]

  response = requests.get(
    "https://api.spotify.com/v1/search",
    headers={"Authorization": f"Bearer {token}"},
    params={
      "q": keyword,
      "type": "artist",
      "market": "JP",
    },
  )

  return response.json()

@bot.command()
async def search(ctx, keyword):
  if len(keyword) > 20:
    await ctx.send("20文字以下で入力してください")
    return                               # returnで関数を抜けることでapiの呼び出しをしない
  
  result = search_spotify(keyword)

  if len(result["artists"]["items"]) == 0:
    await ctx.send("該当するアーティストが見つかりませんでした")
  elif len(result["artists"]["items"]) == 1:
    url = result["artists"]["items"][0]["external_urls"]["spotify"]
    await ctx.send(url)
  elif len(result["artists"]["items"]) > 1:
    url = result["artists"]["items"][0]["external_urls"]["spotify"]
    message = f"複数見つかったけど、これ？{url}"
    await ctx.send(message)

@bot.command()
async def helpme(ctx):
  await ctx.send("使えるコマンドは、「search <アーティスト名>」だよ。")

bot.run(discord_token)