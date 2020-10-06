import discord
import sqlite3
import random
import math
import datetime
from discord.ext import commands

on_cooldown = {}

class Bust(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command()
  async def bust(self, ctx):
    author = ctx.message.author.id
    data = sqlite3.connect('main.db')
    curs = data.cursor()
    curs.execute(f"SELECT _level, bust_count, bust_points, point_to_next_level, cooldown, max_points, min_points FROM user_info WHERE user_id = {author}")
    result = curs.fetchone()
    if result is None:
      sql = (f"INSERT INTO user_info (user_id, _level, bust_count, bust_points, point_to_next_level, cooldown, max_points, min_points) VALUES (?,?,?,?,?,?,?,?)")
      level = 1
      bust_cooldown = 86400
      count = 0
      points = 0
      pointNextLevel = 10
      maxpoints = 10
      minpoints = 5
      val = (author, level, count, points, pointNextLevel, bust_cooldown, maxpoints, minpoints)
      curs.execute(sql, val)
      data.commit()
    else:
      level = result[0]
      bust_cooldown = result[4]
      count = result[1]
      points = result[2]
      pointNextLevel = result[3]
      maxpoints = result[5]
      minpoints = result[6]
    try:
      last_bust = datetime.datetime.now() - on_cooldown[author]
    except KeyError:
      last_bust = None
      on_cooldown[author] = datetime.datetime.now()
    if last_bust is None or last_bust.seconds > bust_cooldown:
      randPoint = random.randint(minpoints, maxpoints)
      count = str(int(count) + 1)
      points += randPoint
      if points >= pointNextLevel:
        sql = (f"UPDATE user_info SET _level = ?, bust_count = ?, bust_points = ?, point_to_next_level = ?, cooldown = ?, max_points = ?, min_points = ? WHERE user_id = ?")
        val = (level + 1, count, points % pointNextLevel, math.floor(1.75*level + 9), math.floor((-8/33)*(level - 100)) * 3600, math.floor(1.5*level + 8.5), math.floor(level + 4), author)
        curs.execute(sql, val)
        data.commit()
        bust_embed = discord.Embed(title="**You have busted a nut AND leveled up!** :tada: :partying_face: :eggplant: :sweat_drops:", description=f"{ctx.author.mention} has busted a nut, and leveled up to level {level + 1}! Use the command `?profile` for more info. _wait **{math.floor((-8/33)*(level - 100))}** hours to bust again!_", color=discord.Color.dark_teal())
        await ctx.send(embed=bust_embed)
      else:
        sql = (f"UPDATE user_info SET bust_count = ?, bust_points = ? WHERE user_id = ?")
        val = (count, points, author)
        curs.execute(sql, val)
        data.commit()
        bustembed = discord.Embed(title="**You have busted a nut** :eggplant: :sweat_drops:", description=f"{ctx.author.mention} has busted a nut, wait **{bust_cooldown/3600}** hours to bust again! _You gained {randPoint} points from this bust._", color=discord.Color.greyple())
        await ctx.send(embed=bustembed)
    else:
      MBED = discord.Embed(title="**You are on cooldown!**", description=f"Hold your horses, buddy, you still have `{datetime.timedelta(seconds=bust_cooldown - last_bust.seconds)}` before you can bust another nut. You can decrease bust cooldown by leveling up, be sure to check back often!", color=discord.Color.red())
      await ctx.send(embed=MBED)
    curs.close()
    data.close()

  @commands.command()
  async def profile(self, ctx, *, user:discord.User=None):
    datab = sqlite3.connect('main.db')
    curse = datab.cursor()
    if user is None:
      curse.execute(f"SELECT _level, bust_count, bust_points, point_to_next_level, cooldown, max_points, min_points FROM user_info WHERE user_id = {ctx.message.author.id}")
      result = curse.fetchone()
      if result is None:
        await ctx.send("You haven't busted yet! use `?bust` to get you information!")
      else:
        emmbeed = discord.Embed(title = f"{ctx.author.name}'s Profile")
        emmbeed.add_field(name = "Level", value = f"{result[0]}")
        emmbeed.add_field(name = "Total Busts", value = f"{result[1]}")
        emmbeed.add_field(name = "Points", value = f"{result[2]}/{result[3]}")
        emmbeed.add_field(name = "Cooldown", value = f"{result[4]/3600} hours")
        emmbeed.add_field(name = "Points earned per bust", value = f"Minimum: {result[6]}\nMaximum: {result[5]}")
        emmbeed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
        await ctx.send(embed=emmbeed)
    else:
      curse.execute(f"SELECT _level, bust_count, bust_points, point_to_next_level, cooldown, max_points, min_points FROM user_info WHERE user_id = {user.id}")
      result = curse.fetchone()
      if result is None:
        await ctx.send("This person does not have a profile.")
      else:
        emmbeed = discord.Embed(title = f"{user.name}'s Profile")
        emmbeed.add_field(name = "Level", value = f"{result[0]}")
        emmbeed.add_field(name = "Total Busts", value = f"{result[1]}")
        emmbeed.add_field(name = "Points", value = f"{result[2]}/{result[3]}")
        emmbeed.add_field(name = "Cooldown", value = f"{result[4]/3600} hours")
        emmbeed.add_field(name = "Points earned per bust", value = f"Minimum: {result[6]}\nMaximum: {result[5]}")
        emmbeed.set_thumbnail(url="{}".format(user.avatar_url))
        await ctx.send(embed=emmbeed)
  @profile.error
  async def profile_error(self, ctx, error):
    if isinstance(error, commands.UserNotFound):
      await ctx.send("That person is not in this server!")
    else:
      raise error

def setup(client):
  client.add_cog(Bust(client))