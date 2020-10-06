import os
import keep_alive
from discord.ext import commands
buster = commands.Bot(command_prefix='?')
tkn = os.getenv("TOKEN")

@buster.command(hidden=True)
async def load(ctx, extension):
  buster.load_extension(f'COGS.{extension}')

@buster.command(hidden=True)
async def unload(ctx, extension):
  buster.unload_extension(f'COGS.{extension}')

for filename in os.listdir('./COGS'):
  if filename.endswith('.py'):
    buster.load_extension(f'COGS.{filename[:-3]}')

keep_alive.keep_alive()

buster.run(tkn)