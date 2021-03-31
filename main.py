import discord
from discord.ext import commands
import requests
import random 
import json
import os
import asyncio
import datetime
import re
from flask import Flask
from threading import Thread
import youtube_dl

app=Flask("")

@app.route("/")
def index():
  return "<h1>Bot is running</h1>"

Thread(target=app.run,args=("0.0.0.0", 8080)).start()
token=os.environ.get("DISCORD_BOT_SECRET")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.reactions = True
intents.messages = True

bot = commands.Bot(command_prefix='-', intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
  print(f"Connected as {bot.user}")
  await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="-help"))

@bot.event
async def on_command_error(ctx, error):
    ignored = (commands.UserInputError)
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            await ctx.send(f'You must wait {int(s)} seconds before using this command once more! Please wait...')
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f'You must wait {int(m)} minutes and {int(s)} seconds before using this command once more! Please wait...')
        else:
            await ctx.send(f'You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds before using this command once more! Please wait...')

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Hey! You don't have enough permissions to use this command.")
        raise error

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Hey! The command is missing an important argument!")
        raise error
  

# Commands for cogs, loadcog and unloadcog.

@bot.command(name="loadcog", description="Loads all the cogs")
@commands.cooldown(1, 30, commands.BucketType.user)
@commands.has_permissions()
async def loadcog(ctx, cog):
    bot.load_extension(f"cogs.{cog}")
    
    await ctx.send(f"Loaded cog {cog}.")
    member = ctx.author.name
    print(f'{member} just used the loadcog command!')

@bot.command(name="unloadcog", description="Unloads all the cogs")
@commands.cooldown(1, 30, commands.BucketType.user)
async def unloadcog(ctx, cog):
    bot.unload_extension(f"cogs.{cog}")
    await ctx.send(f"Unloaded cog {cog}.")
    member = ctx.author.name
    print(f'{member} just used the unloadcog command!')

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.command()
async def help(ctx, category=None):
  if category == None:
    categoryEmbed = discord.Embed(title='Help!', description='Get help by using -help <category>. The categories are below', color=discord.Color.blue())
    categoryEmbed.add_field(name='Admin', value='`-help admin`')
    categoryEmbed.add_field(name='Fun', value='`-help fun`')
    categoryEmbed.add_field(name='Math', value='`-help math`')
    categoryEmbed.add_field(name='Info', value='`-help info`')
    categoryEmbed.add_field(name='Bot', value='`-help bot`')
    await ctx.send(embed=categoryEmbed)
  elif category == 'admin':
    adminEmbed = discord.Embed(title='Admin', description='`ban`, `unban`, `kick`, `purge`, `mute`, `unmute`, `create_text_channel`, `create_category`, `lock`, `unlock`', color=discord.Color.blue())
    await ctx.send(embed=adminEmbed)
  elif category == 'fun':
    funEmbed = discord.Embed(title='Fun', description='`8ball`, `fakemute`, `webhook`, `dice`, `coin`, `gen_nitro`, `epicgamerrate`, `pograte`', color=discord.Color.blue())
    await ctx.send(embed=funEmbed)
  elif category == 'info':
    infoEmbed = discord.Embed(title='Info', description='`ping`, `userinfo`, `serverinfo`, `servercount`, `stats`, `pfp`, `invite`', color=discord.Color.blue())
    await ctx.send(embed=infoEmbed)
  elif category == 'math':
    mathEmbed = discord.Embed(title='Math', description='`add`, `subtract`, `multiply`, `divide`, `exponent`', color=discord.Color.blue())
    await ctx.send(embed=mathEmbed)
  elif category == 'bot':
    botEmbed = discord.Embed(title='Bot', description='`invite`, `supportserver`, `report`, `suggest`, `credits`, `stats`, `guilds`', color=discord.Color.blue())
    await ctx.send(embed=botEmbed)

@commands.command(name='poll', description='A command with which you can have polls!')
@commands.has_permissions(manage_channels=True)
async def poll(self, ctx, *, question, option1=None, option2=None):
    author = ctx.message.author
    if option1 == None and option2 == None:
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title="Poll")
        # embed.add_field(name=f"**✅**",value ="**Yes**")
        # embed.add_field(name=f"**❎**",value="**No**")
        embed.add_field(name="Question", value=question, inline=False)
        embed.set_footer(text=f'Poll By: {author}')
        message = await ctx.send(embed=embed)
        await message.add_reaction('<a:correct:765080491669061633>')
        await message.add_reaction('<a:wrong:765080446937202698>')
    elif option1 == None:
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title="Poll")
        # embed.add_field(name=f"**✅**",value ="Yes")
        # embed.add_field(name=f"\n**❎**",value="No")
        embed.add_field(name="Question", value=question, inline=False)
        embed.set_footer(text=f'Poll By: {author}')
        message = await ctx.send(embed=embed)
        await message.add_reaction('<a:correct:765080491669061633>')
        await message.add_reaction('<a:wrong:765080446937202698>')
    elif option2 == None:
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title="Poll")
        # embed.add_field(name=f"**✅**",value = "Yes")
        # embed.add_field(name=f"\n**❎**",value="No")
        embed.add_field(name="Question", value=question, inline=False)
        embed.set_footer(text=f'Poll By: {author}')
        message = await ctx.send(embed=embed)
        await message.add_reaction('<a:correct:765080491669061633>')
        await message.add_reaction('<a:wrong:765080446937202698>')
    else:
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title="Poll")
        # embed.add_field(name=f"**✅**",value = "Yes")
        # embed.add_field(name=f"\n**❎**",value="No")
        embed.add_field(name="Question", value=question, inline=False)
        embed.set_footer(text=f'Poll By: {author}')
        message = await ctx.send(embed=embed)
        await message.add_reaction('<a:correct:765080491669061633>')
        await message.add_reaction('<a:wrong:765080446937202698>')

@bot.command()
@commands.has_permissions(administrator=True)
async def gstart(ctx, mins: int, *, prize: str):
  embed = discord.Embed(title=prize, color=discord.Color.blue())
  end = datetime.datetime.utcnow() + datetime.timedelta(seconds = round(mins*60))
  embed.add_field(name='Ends at', value=f'{end} UTC')
  embed.set_footer(text=f'Ends: {mins} minutes')
  giveaway = await ctx.send(embed=embed)
  await giveaway.add_reaction('🎉')
  await asyncio.sleep(mins*60)
  giveawayEndMsg = await ctx.channel.fetch_message(giveaway.id) 
  users = await giveawayEndMsg.reactions[0].users().flatten()
  users.pop(users.index(bot.user))
  winner = random.choice(users)
  await ctx.send(f'Congratulations! {winner.mention} won the giveaway for {prize}!')

def convert(time):
  pos = ['s', 'm', 'h', 'd']
  time_dict = {'s': 1, 'm': 60, 'h': 3600, 'd': 3600*24}
  unit = time[1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2
  return val * time_dict[unit]

@bot.command(aliases=['rl'])
@commands.is_owner()
async def reload(ctx, cog):
  async with ctx.channel.typing():
    if ctx.author.id == 780414447894134794:
      if cog == 'all':
        message = await ctx.send('Starting reload...')
        for filename in os.listdir('./cogs'):
          if filename.endswith('.py'):
            bot.unload_extension(f'cogs.{filename[:-3]}')
            await message.edit(content=f'Unloaded {filename}')
            bot.load_extension(f'cogs.{filename[:-3]}')
            await message.edit(content=f'Loaded {filename}')
        await message.edit(content='Reloaded all cogs!')
      else:
        message = await ctx.send('Starting reload...')
        await asyncio.sleep(2)
        bot.unload_extension(f'cogs.{cog}')
        await message.edit(content=f'Unloading cog `{cog}`')
        bot.load_extension(f'cogs.{cog}')
        await asyncio.sleep(2)
        await message.edit(content=f'Reloading cog `{cog}`')
        await asyncio.sleep(2)
        await message.edit(content=f'Reloaded cog `{cog}`')
    else:
      await ctx.send('Hey you aren\'t allowed to use this command!')


bot.run(token)