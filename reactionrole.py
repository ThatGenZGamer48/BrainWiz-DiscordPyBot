messageIDs = []

@bot.event
async def on_raw_reaction_add(payload):
  global messageIDs

  for messageID in messageIDs:
    if messageID == payload.message_id:
      user = payload.member
      role = "roleName"
      await user.add_roles(discord.utils.get(user.guild.roles, name=role))

@bot.command()
async def reactionrole(ctx, message_id, role, emoji):
  global messageIDs

  channel = ctx.message.channel

  try:
    msg = await channel.fetch_message(message_id)
  except:
    await ctx.send('Invalid message ID!')
    return
  await msg.add_reaction(emoji)
  messageIDs.append(message_id)
