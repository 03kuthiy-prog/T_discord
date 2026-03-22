import discord
from discord import app_commands
from discord.ext import commands
from discord import Member
import session
from session import Session
import asyncio
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
TOKEN =os.getenv('DISCORD_TOKEN')

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.progSess:Session=None #進行中　Session型
    async def setup_hook(self):
        await self.tree.sync()  # スラッシュコマンドを同期
    def setSession(self,progSess:session):
        self.progSess=progSess
    def isStartable(self):
        return (self.progSess is None)
    def nextSection(self):
        ans:str="セッションが未完成"
        if not self.isStartable():#開始不可→現在進行形でやっている
                self.progSess.nextSection()
                self.progSess.updateSection()
                ans=self.progSess.getSection()
        #ans=self.progSess.name
        return ans
    def addChangeWord(self,bfr:str,aft:str):
        return self.progSess.addChangewords(bfr,aft)
    def getUpdated(self):    
        self.progSess.updateSection()
        return self.progSess.getSection()

bot = MyBot(command_prefix="None", intents=discord.Intents.default())

@bot.tree.command(name="list", description="シナリオid:怪談白のシナリオ")
#@app_commands.describe(text="返してほしい文字列")
async def arg(interaction: discord.Interaction):
    await interaction.response.send_message("id01:けものつき")

@bot.tree.command(name="start",description="怪談白のセッションスレッドを作成")
@app_commands.describe(scenalioid="シナリオid",tutoflg="チュートリアル表示")
async def start(interaction: discord.Interaction,scenalioid:str,tutoflg:bool =False):
    if bot.isStartable() :
        kh= Session(scenalioid)
        bot.setSession(kh)
        await interaction.response.send_message(kh.name, ephemeral=False)
        msg=await interaction.original_response()
        thread = await msg.create_thread(name="怪談白物語："+kh.name)
        await thread.send("語るは九十九の怪語り。残る一つはどこにかあらん。"+
                            "一がなければ語りは閉まらぬ。百に届かぬ白物語。九十九に付くもの露すら知らず。")
        if tutoflg :
            await thread.send("PC達はある集まりの百物語に参加しています。PC達は知っている。"
                            +"百の怪談が集まれば、世にも恐ろしいことが起きるということを。"
                            +"今まさに最後の一人(GM)が最後の一話を語ろうとしています。何とかして怖い話を怖くない話にしましょう。")
    else:
        await interaction.response.send_message("現在進行中のセッションがあります。\nお待ちください")
#===================(セッション時の操作)======================
@bot.tree.command(name="next",description="セッション操作、次の文を送信")
async def next(interaction: discord.Interaction):
    if not isinstance(interaction.channel, discord.Thread):
        await interaction.response.send_message("このコマンドはスレッド内でのみ使用できます。",ephemeral=True)
        return
    # ここから先はスレッド内でのみ実行される
    await interaction.response.send_message("続きを読みます")
    mess=bot.nextSection()
    if mess!="終了":
        await interaction.channel.send(mess)
    else:#終了
        await createResult(interaction)

@bot.tree.command(name="change",description="これって○○じゃなくて××ですよね")
@app_commands.describe(old_word="○○(変更前)",new_word="XX(変更後)",rewrite_flg="変更後の再描写を行う")
async def change(interaction: discord.Interaction,old_word:str,new_word:str,rewrite_flg:bool=True):
    if not isinstance(interaction.channel, discord.Thread):
        await interaction.response.send_message(
            "このコマンドはスレッド内でのみ使用できます。",
            ephemeral=True
        )
        return
    # ここから先はスレッド内でのみ実行される
    kwr="です" if bot.addChangeWord(old_word,new_word) else "ではありません"

    mess=("(自動)成功です\n"+
        f"そうでした そうでした\n{old_word} ではなく {new_word} でした\n"+
        f"{old_word}はキーワード{kwr}"
    )
    await interaction.response.send_message(mess)
    #await interaction.followup.send(f"そうでした そうでした\n{old_word} ではなく {new_word} でした")
    #kwr="です" if bot.addChangeWord(old_word,new_word) else "ではありません"
    #await interaction.followup.send(f"{old_word}はキーワード{kwr}")
    if rewrite_flg :
        await interaction.channel.send(bot.getUpdated())

async def createResult(interaction: discord.Interaction,):
    await interaction.channel.send("これにてこの話は以上です。\n" +bot.progSess.getKeyword())
    for sct in bot.progSess.getResultSections() :
        await interaction.channel.send(sct)
    await interaction.channel.send(f"怪談白物語: {bot.progSess.name}\n"
                                   +f"シナリオ参照元: {bot.progSess.url}"
                                   +"\n※このスレッドは10秒ほどでクローズドされます。"
                                   )
    await asyncio.sleep(10)
    await interaction.channel.edit(archived=True)
    bot.progSess=None
bot.run(TOKEN)



