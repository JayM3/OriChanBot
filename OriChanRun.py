# Version: 1.1
# Date: 1/24/2023
import discord, os,asyncio
from discord.ext.commands import Bot
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content=True


class OriChan(Bot):
    def __init__(self):
        super().__init__(command_prefix=['ori!','Ori!'], intents=intents, help_command=None)
    
    async def setup_hook(self):
        await load(self)

def loadData():
    KEYS={}
    for filename in os.listdir('./Data'):
        if filename.endswith('.txt'):
            if filename == "BotToken.txt":
                with open(f'Data/{filename}', 'r') as f:
                    KEYS['BotToken']=f.read()
            elif filename=="APIKeys.txt":
                with open(f'Data/{filename}', 'r') as f:
                    KEYS['APIKeys']=[]
                    foo=(f.read().split("\n"))
                    for key in foo:
                        KEYS['APIKeys'].append(key)
    return KEYS


async def load(bot:Bot):
    for filename in os.listdir('./Cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'Cogs.{filename[:-3]}')
            print(f"[x]: Cog Loaded: Cogs.{filename[:-3]}")


bot = OriChan()


@bot.command(description='Reloads relevant cogs.', aliases=['re'])
@commands.is_owner()
async def sync(ctx):
    await ctx.message.delete()
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s).")
    for filename in os.listdir('./Cogs'):
        if filename.endswith('.py'):
            await bot.reload_extension(f'Cogs.{filename[:-3]}')
            print(f'[+]: Reloaded Cog: {filename[:-3]}')


if __name__ == '__main__':
    bot.run(loadData()['BotToken'])