import discord
from discord.ext import commands

class Events(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    await self.client.change_presence(activity=discord.Activity(name="?bust | 12.3k balls busted today", type=discord.ActivityType.listening))
    print("online")
  
  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    MBED = discord.Embed(title=":wave: **Hello!** Thanks for adding me in your server!", description="This is the new **Ball Buster Botᵀᴹ** for Discord, for your ball busting needs!\n*(:notepad_spiral: Dev's note: this bot is still a work in progress.)*", colour=discord.Colour.blurple())
    MBED.add_field(name="**Current command(s) for the bot are:** prefix is \"?\"", value="`?bust`- busts a nut :sweat_drops:\n`?profile` - shows information about your bust level and other people's bust levels.")
    channels = guild.text.channels
    for channel in channels:
      if channel and channel.permissions_for(guild.me).send_messages:
        await channel.send(embed=MBED)

def setup(client):
  client.add_cog(Events(client))