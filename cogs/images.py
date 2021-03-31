import discord
from discord.ext import commands
import random 
import datetime 
import asyncio 
from PIL import Image 
from io import BytesIO 

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Just **YEET** it")
    async def yeet(self, ctx):
      file = discord.File("yeet.jpg", filename="yeet.jpg")
      await ctx.message.delete()
      await ctx.send(file=file)

    @commands.command(description="Wanted command.")
    async def wanted(self, ctx, user: discord.Member=None):
      if user == None: 
        user = ctx.author

      wanted = Image.open("../wanted.jpg")
      asset = user.avatar_url_as(size = 128)
      data = BytesIO(await asset.read())
      pfp = Image.open(data)

      pfp = pfp.resize((270, 270))

      wanted.paste(pfp, (103, 210))
      wanted.save("profile.jpg")
      
      await ctx.send(file = discord.File("profile.jpg"))

def setup(bot):
    bot.add_cog(Info(bot))


