import discord
import os
from dotenv import load_dotenv

from discord.ext import commands
from discord import app_commands

# .env ファイルを読み込む
load_dotenv()

# Botのトークン
TOKEN = os.getenv('DISCORD_TOKEN_MAIN')
# Botのコマンドプレフィックスと設定
intents = discord.Intents.default()
intents.message_content = True
'''
class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync() 
'''
bot = commands.Bot(command_prefix='!', intents=intents) 
# MyBot(command_prefix="!", intents=discord.Intents.default())
#     commands.Bot(command_prefix='!', intents=intents)


# Bot起動時のイベント
@bot.event
async def on_ready():
   print(f'ログインしました: {bot.user}')
# コマンド例: !hello と入力すると応答
@bot.command()
async def hello(ctx):
   await ctx.send('こんにちは！')



@bot.tree.command(name="arg", description="文字列を受け取って返します")
@app_commands.describe(text="返してほしい文字列")
async def arg(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f"{text}なんだね")

# Botを起動
bot.run(TOKEN)