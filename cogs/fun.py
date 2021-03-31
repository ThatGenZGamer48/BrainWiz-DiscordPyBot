import discord
from discord.ext import commands
import json
import random
import requests
import youtube_dl

with open("./config.json") as f:
    configData = json.load(f)

prefix = configData["Prefix"]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def webhook(self, ctx, *, message):
     pfp = requests.get(ctx.author.avatar_url_as(format='png', size=256)).content
     hook = await ctx.channel.create_webhook(
              name = ctx.author.name,
              avatar = pfp)
     await ctx.message.delete()
     await hook.send(message)
     await hook.delete()

        # 8ball command!
    @commands.command(aliases=['8ball', 'test'], description="Asks 8ball a question.")
    async def _8ball(self, ctx, *, question=None):
      if question != None:
        responses = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]

        
        print(f"{ctx.author.name} used the command.")
        await ctx.send(f":8ball: | {random.choice(responses)}")
      else:
        await ctx.send("Please specify a question. Format = -8ball [question] without the brackets")

    @commands.command(description="Rolls a dice.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dice(self, ctx):
      dicenumber_one = random.randint(1, 6)
      dicenumber_two = random.randint(1, 6)
      await ctx.send(f"You rolled a {dicenumber_one} and a {dicenumber_two}!")

    @commands.command(description="Flips a coin", aliases=['coinflip', 'flipcoin'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coin(self, ctx, call = None):
      coinflip = ['Heads', 'Tails']
      flip = random.choice(coinflip)
      if call == flip.lower():
        await ctx.send(f"{flip} it is! Nice one there!")
      elif call == flip:
        await ctx.send(f"{flip} it is! Nice one there!")
      elif call != flip.lower():
        await ctx.send(f"{flip} it is! A bit of bad luck there, Try again!")
      elif call != flip:
        await ctx.send(f"{flip} it is! A bit of bad luck there, Try again!")
      else:
        await ctx.send("Invalid argument passed! Please pass either heads or tails.")

    @commands.command()
    async def poll(self, ctx, question, option1, option2):
      await ctx.channel.purge(limit=1)
      embed = discord.Embed(title=question, description=f"**✅ {option1}**\n**❎ {option2}**")
      message = await ctx.send(embed=embed)
      await message.add_reaction('✅')
      await message.add_reaction('❎')

    @commands.command(description='Blesses a user.', aliases=['blezz'])
    async def bless(self, ctx, name):
      blesses = [
        'I hope sony sends you their new PS5 for free by accident!',
        'I hope that the gaming PC you buy comes with a free Mac',
        'I hope that you get 100 marks in every single exam you write',
        'I hope you win every single discord nitro giveaway!',
        'I hope you become moderator in every single discord server you join!'
      ]
      await ctx.send(f'{name}, {random.choice(blesses)}')

    @commands.command(description="Random nitro code generator.")
    async def gen_nitro(self, ctx):
      alphabets = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z']
      nitro_code = f"https://discord.gift/{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}{random.choice(alphabets)}"
      embed=discord.Embed(title="1x RANDOM NITRO CODE", description=f"`{nitro_code}`")
      await ctx.send("I have dmmed you 1x nitro random code!")
      await ctx.author.send(embed=embed)
    
    @commands.command(description="Rates a gamer...")
    async def epicgamerrate(self, ctx, member: discord.Member = None):
      rate = random.randrange(100)
      if member != None:
        embed = discord.Embed(title="Epic Gamer Rate", description=f"You are {rate}% epic gamer!", colour=discord.Colour.blue())
        await ctx.send(embed=embed)
      else:
        embed = discord.Embed(title="Epic Gamer Rate", description=f"You are {rate}% epic gamer!", colour=discord.Colour.blue())
        await ctx.send(embed=embed)
    
    @commands.command(name='fakemute')
    async def fakemute(self, ctx, member: discord.Member = None):
      if member == None: 
        await ctx.send(f"{ctx.author} is muted!")
      else:
        await ctx.send(f"{member} is muted!")
    
    @commands.command(name='pograte')
    async def pog(self, ctx, member: discord.Member=None):
      if member != None: 
        pograte = random.randrange(100)
        await ctx.send(f'You are {pograte}% pog <:pog:815829175687577662>')
      else:
        pograte3 = random.randrange(100)
        await ctx.send(f'You are {pograte3}% pog <:pog:815829175687577662>')

def setup(bot):
    bot.add_cog(Fun(bot))