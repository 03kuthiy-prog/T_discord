import discord
from discord import Member


class Session:
    def __init__(self,name,players:list[Member],kp:Member):
        self.name=name
        self.players=[]#players
        self.kp=kp

    def addPlayers(self,newPL:Member):
        self.players.append(newPL)

    def toString(self):
        ans="シナリオ名："+self.name
        ans+="\n kp："+self.kp.display_name
        ans+="\nメンバー："+self.players
        return ans