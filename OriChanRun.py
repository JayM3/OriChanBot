# Version: 1.1
# Date: 1/24/2023
import discord, os,asyncio
from discord.ext import commands
from Cogs import OriChanMain

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content=True
bot = commands.Bot(command_prefix=['ori!','Ori!'], intents=intents, help_command=None)
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


async def load():
    for filename in os.listdir('./Cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'Cogs.{filename[:-3]}')
            print(f"[x]: Cog Loaded: Cogs.{filename[:-3]}")



async def main():
    
    Data=loadData()
    APIKeysString=""
    Count=1
    for x in Data['APIKeys']:
        APIKeysString+=f"\n[x]: {Count} > {(x)[-7:]}"
        Count+=1
    print(f"[x]: Loaded API Keys: {APIKeysString}\n[x]: Bot Token: {(Data['BotToken'])[-7:]}")

    await load()
    
    await bot.start(Data['BotToken'])
    
    


asyncio.run(main())


