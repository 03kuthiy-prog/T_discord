import discord
from discord import app_commands
from discord.ext import commands
from discord import Member
import os
from dotenv import load_dotenv

import Session_mdl
from Session_mdl import Session

# .env ファイルを読み込む
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN_MAIN')

class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync()  # スラッシュコマンドを同期

bot = MyBot(command_prefix="None", intents=discord.Intents.default())

@bot.tree.command(name="args", description="文字列を受け取って返します")
@app_commands.describe(text="返してほしい文字列")
async def arg(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f"{text}なんだね")

@bot.tree.command(name="create",description="セッションインスタンス作成")
@app_commands.describe(name="シナリオ名",players="参加者",kp="kp(GM)メンバー")
async def createS(interaction: discord.Interaction,name:str,
                  players:str,kp:Member):
    bean=Session(name,players,kp)
    await interaction.response.send_message(bean.toString()+"\nで作成")




bot.run(TOKEN)
