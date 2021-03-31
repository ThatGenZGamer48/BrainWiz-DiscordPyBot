import discord
from discord.ext import commands
import json
import random
import requests
import youtube_dl
import datetime
import asyncio 
import random

with open("./config.json") as f:
    configData = json.load(f)

prefix = configData["Prefix"]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Fun(bot))