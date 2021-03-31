import discord
from discord.ext import commands
import json
import os

with open("./config.json") as f:
    configData = json.load(f)

prefix = configData["Prefix"]


class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Bot(bot))