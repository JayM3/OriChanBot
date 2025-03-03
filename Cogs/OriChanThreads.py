# Version: 1.2
# Date: 2/26/2025
import discord
from discord.ext import commands
from Cogs import OriChanMain
from datetime import datetime
import datetime as dt
import random,os,openai,asyncio,sqlite3,OriChanRun,ObjectClasses
import asyncOpenAI
import base64, aiohttp, io, docx
from pypdf import PdfReader

dividerImg="https://cdn.discordapp.com/attachments/1054984334878191636/1061806291091210320/image.png"
DB='Database/Main.db'

def user_exists(ID):
    conn = sqlite3.connect(DB)
    cursor = conn.execute('''SELECT * FROM users WHERE ID=?''', (ID,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def createWarnEmbed(description):
    # Set the color, thumbnail, and footer of the embed
    color = 0x5C0E80
    footer_text = "Ori-chan & Friends."
    footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png"
    # Create the embed
    embed = discord.Embed(description=description, color=color)
    embed.set_footer(text=footer_text, icon_url=footer_icon)
    embed.set_image(url=dividerImg)
    return embed

def createReplyEmbed(description,TokensUsed, PersonaName):
    # Set the color, thumbnail, and footer of the embed
    color = 0x5C0E80
    footersChoice=['ko-fi.com/orichan', 'Need help? ori!help!']
    footer_text = f"Ori-chan & Friends. {random.choice(footersChoice)} Used: {TokensUsed} OC"
    footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png"
    # Create the embed
    embed = discord.Embed(title=f'{PersonaName}:',description=description, color=color)
    embed.set_footer(text=footer_text, icon_url=footer_icon)
    embed.set_image(url=dividerImg)
    return embed

class ThreadCommands(commands.Cog):
    def __init__(self,bot):
        Data=OriChanRun.loadData()
        self.bot = bot
        self.StandardFilterThreshold = 0.45
        self.keyToUse=0
        self.APIKEYLIST=Data['APIKeys']
        self.permittedChannels=[1064342742756499518, 1058810679424995328, 'DM']
        self.persona = ObjectClasses.getPersonas()
        self.activeUsers={}
    
    def ContentCheckStd(self, content, APIKEYTOUSE):
        openai.api_key = APIKEYTOUSE
        resp=openai.Moderation.create(input=content)
        unbannedWords={'kill': 'violence'}
        BypassCategories=[]
        for x in unbannedWords.keys():
            if x in content.lower():
                BypassCategories.append(unbannedWords[x])
                
        for x in resp['results'][0]['categories'].keys():
            if x in BypassCategories:
                continue
            else:
                if resp['results'][0]['category_scores'][x] > self.StandardFilterThreshold:
                    return x
        return False
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[+]: {self.bot.user.name} Thread Cog is ready.")
        
    @commands.command(aliases=['st', 'St'])
    async def startthread(self, ctx,*,persona=None):
        try:
            if user_exists(ctx.message.author.id):
                user=ObjectClasses.User(ctx.message.author.id)
            else:
                user=ObjectClasses.User(ctx.message.author.id,25000,"freeRole",0)
                user.save_to_database()

            if user.tokensBalance >= 20000:
                if persona == None:
                    persona=user.Persona
                else:
                    if int(persona):
                        Personas = user.getUserPersonas()
                        IDList=[]
                        for x in Personas.keys():
                            IDList.append(x+1)
                        if int(persona) in IDList:
                            user.Persona = Personas[int(persona)-1]['PersonaID']
                            persona=user.Persona
                        else:
                            await ctx.message.reply(f"The number you've given doesn't correspond to any of your available personas!")
                            return
                    else:
                        await ctx.message.reply(embed=createWarnEmbed('The persona you have mentioned does not exist!\n\nPlease try the command again!'))
                        return

                threadName=f'{str(ctx.message.author)[:-5]} & {self.persona[persona]["Name"]}'
                theMessage = await ctx.message.reply(embed=createWarnEmbed('Creating a new conversation!\n\nClick on a button bellow to choose between a private or public thread conversation!\n🟦: Public Thread\n🟥: Private Thread'))
                                # 🟦 🟥
                blueEmote="🟦"
                redEmote="🟥"

                await theMessage.add_reaction(blueEmote)
                await theMessage.add_reaction(redEmote)

                def check(reaction, theuser):
                    return theuser==ctx.author and str(reaction.emoji) in [blueEmote, redEmote]

                while True:
                    try:
                        reaction, theuser = await self.bot.wait_for('reaction_add', timeout=60, check=check)
                    except asyncio.TimeoutError:
                        await theMessage.clear_reactions()
                        await theMessage.edit(embed=createWarnEmbed('Reaction timeout!'))
                        return

                    await reaction.remove(theuser)
                    if reaction.message.id == theMessage.id:
                        if str(reaction.emoji) == blueEmote:
                            theThread = await theMessage.create_thread(name=threadName,auto_archive_duration=60)
                            await theMessage.edit(embed=createWarnEmbed(f'**Public thread created!**\n[Click here to go to thread!]({theThread.jump_url})'))
                            break
                        elif str(reaction.emoji) == redEmote:
                            theThread = await ctx.channel.create_thread(name=threadName,auto_archive_duration=60, reason=threadName)
                            await theMessage.edit(embed=createWarnEmbed(f'**Private thread created!**\n[Click here to go to thread!]({theThread.jump_url})'))
                            break

                await theMessage.clear_reactions()
                await theThread.add_user(ctx.author)

                async with theThread.typing():
                    theKey=ObjectClasses.GetAKey()
                    systemPrompt=((self.persona[persona]["Prompt"]).replace("[[JAYWASHERE123123JAYWASHERE]]", f"{str(ctx.author)[:-5]}")).replace("[[ARUHELPEDMELUL]]", f"*Walks in the room*\n\nEnd of Example conversation")
                    messages=[
                        {"role": "system", "content": systemPrompt},
                        {"role": "user", "content": "*Walks in the room*"}
                    ]
                    theResponse=await asyncOpenAI.chat_complete(theKey, timeout=30, payload={'model': 'gemini-2.0-flash-exp',
                                                                    'messages': messages,
                                                                    'temperature': 0.9,
                                                                    'top_p':1,
                                                                    "max_completion_tokens": 4096}
                                                                    )
                    now = datetime.now().strftime("%H:%M:%S")
                    print(f"[{now}] - {theResponse}\nUsed key: {(theKey)[-7:]}\nTokens used: {theResponse.json()['usage']['total_tokens']}\nUser: {ctx.author} - {ctx.author.id}")
                    usedTokens=0
                    usedTokens+=(int(theResponse.json()['usage']['total_tokens'])*0.5)
                    user.tokensBalance-=(int(theResponse.json()['usage']['total_tokens'])*0.5)
                    user.save_to_database()
                    try:
                        theReply=theResponse.json()['choices'][0]['message']['content']
                        messages.append({"role": "assistant", "content": theReply})
                    except:
                        theReply="*There was an error processing your message, please try again!*"
                    embedToSend=createReplyEmbed(theReply, str(int(theResponse.json()['usage']['total_tokens'])*0.5), self.persona[persona]['Name'])
                theMessageToSend = await theThread.send(embed=embedToSend)

                infoEmbed = await theThread.send(embed=createWarnEmbed(f"**Thread Information**\n\n**>Send one message at a time!!!<**\nUsed total Ori Coins: {usedTokens} OC\n**To delete thread**: `ori!delete`\n**To lock thread**: `ori!lock`"))
                ErrorMessage=None
                #convoPairs=[f"{theReply}\n"] # No longer needed as messages list handles context


                def check(m):
                    return m.author == ctx.author and m.channel == theThread

                while True:
                    try:
                        msgInp = await self.bot.wait_for('message', timeout=900.0, check=check)
                    except Exception as e:
                        await theMessage.edit(embed=createWarnEmbed(f"Thread closed due to inactivity.\n[Click here to go to thread!]({theThread.jump_url})"))
                        await theThread.edit(locked=True, archived=True)
                        break

                    await infoEmbed.delete()
                    if ErrorMessage is not None:
                        await ErrorMessage.delete()

                    if (msgInp.content).lower()!="ori!delete" and (msgInp.content).lower()!="ori!lock":
                        if user.tokensBalance >= 5000:
                            UserRole=user.getRoleInfo()
                            CharUnlockFoo = 0
                            if user.CLUnlock == 0:
                                charLimit=(user.getRoleInfo())['CharacterLimit']
                            elif user.CLUnlock == 1:
                                if user.characterLimitUnlockCard >= 1:
                                    charLimit=9999
                                    CharUnlockFoo = 1
                                else:
                                    charLimit=(user.getRoleInfo())['CharacterLimit']
                                    user.CLUnlock = 0
                                    user.save_to_database()
                            if len(msgInp.content)>(charLimit):
                                ErrorMessage = await theThread.send(embed=createWarnEmbed(f'Your message exceeded your maximum character limit!\nYour message is {len(msgInp.content)}!\nYour character limit is {UserRole["CharacterLimit"]}'))
                                await msgInp.delete()
                                infoEmbed = await theThread.send(embed=createWarnEmbed(f"**Thread Information**\n\n**>Send one message at a time!!!<**\nUsed total Ori Coins: {usedTokens} OC\n**To delete thread**: `ori!delete`\n**To lock thread**: `ori!lock`"))
                                msgInp=None
                            else:
                                if CharUnlockFoo == 1:
                                    user.characterLimitUnlockCard -= 1
                                    user.save_to_database()
                                async with theThread.typing():
                                    theKey=ObjectClasses.GetAKey()
                                    if msgInp.attachments:
                                        if msgInp.content=="":
                                            msgContent = [{'type': "text", "text": "The user has not provided any text content."}]
                                        else:
                                            msgContent = [{'type': "text", "text": msgInp.content}]
                                        for attachment in msgInp.attachments:
                                            if attachment.content_type and attachment.content_type.startswith('image/'):
                                                async with aiohttp.ClientSession() as session:
                                                    async with session.get(attachment.url) as response:
                                                        image_data = await response.read()
                                                        base64_image = base64.b64encode(image_data).decode('utf-8')
                                                        msgContent.append({'type': "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}})
                                            
                                            elif attachment.content_type and attachment.content_type.startswith('text/'):
                                                async with aiohttp.ClientSession() as session:
                                                    async with session.get(attachment.url) as response:
                                                        text_data = await response.text()
                                                        msgContent.append({'type': "text", "text": f"The user has uploaded the following plain text file:\nFile name: {attachment.filename}\nCONTENT:\n{text_data}"})
                                
                                            elif attachment.content_type and attachment.content_type.startswith('application/pdf'):
                                                async with aiohttp.ClientSession() as session:
                                                    async with session.get(attachment.url) as response:
                                                        pdf_data = await response.read()
                                                        pdf_stream = io.BytesIO(pdf_data)
                                                        pdf_reader = PdfReader(pdf_stream)
                                                        pdf_text = ""
                                                        for page in range(len(pdf_reader.pages)):
                                                            pdf_text += pdf_reader.pages[page].extract_text()
                                                        msgContent.append({'type': "text", "text": f"The user has uploaded the following plain text file:\nFile name: {attachment.filename}\nCONTENT:\n{pdf_text}"})
                                            
                                            elif attachment.content_type and attachment.content_type.startswith('application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
                                                async with aiohttp.ClientSession() as session:
                                                    async with session.get(attachment.url) as response:
                                                        docx_data = await response.read()
                                                        docx_stream = io.BytesIO(docx_data)
                                                        docx_reader = docx.Document(docx_stream)
                                                        docx_text = ""
                                                        for paragraph in docx_reader.paragraphs:
                                                            docx_text += paragraph.text
                                                        msgContent.append({'type': "text", "text": f"The user has uploaded the following plain text file:\nFile name: {attachment.filename}\nCONTENT:\n{docx_text}"})
                                            elif attachment.content_type and attachment.content_type.startswith('audio/'):
                                                async with aiohttp.ClientSession() as session:
                                                    async with session.get(attachment.url) as response:
                                                        audio_data = await response.read()
                                                        base64_audio = base64.b64encode(audio_data).decode('utf-8')
                                                        if attachment.filename.endswith('.mp3'):
                                                            msgContent.append({'type': "input_audio", "input_audio": {"data": base64_audio, "format": "mp3"}})
                                                        elif attachment.filename.endswith('.wav'):
                                                            msgContent.append({'type': "input_audio", "input_audio": {"data": base64_audio, "format": "wav"}})
                                                        else:
                                                            await theThread.send(embed=createWarnEmbed("Please only upload mp3 or wav files!"), delete_after=3.0)
                                        messages.append({"role": "user", "content": msgContent})
                                    else:
                                        messages.append({"role": "user", "content": msgInp.content})
                                    theResponse=await asyncOpenAI.chat_complete(theKey, timeout=30, payload={'model': 'gemini-2.0-flash-exp',
                                                                                    'messages': messages,
                                                                                    'temperature': 0.9,
                                                                                    'top_p':1,
                                                                                    "max_completion_tokens": 4096}
                                                                                    )
                                    now = datetime.now().strftime("%H:%M:%S")
                                    print(f"[{now}] - {theResponse}\nUsed key: {(theKey)[-7:]}\nTokens used: {theResponse.json()['usage']['total_tokens']}\nUser: {ctx.author} - {ctx.author.id}")
                                    usedTokens+=round(int(theResponse.json()['usage']['total_tokens'])*0.5)
                                    user.tokensBalance-=round(int(theResponse.json()['usage']['total_tokens'])*0.5)
                                    user.save_to_database()
                                    try:
                                        theReply=theResponse.json()['choices'][0]['message']['content']
                                    except:
                                        theReply="*There was an error processing your message, please try again!*"
                                    messages.append({"role": "assistant", "content": theReply})
                                    embedToSend=createReplyEmbed(theReply, str(round(int(theResponse.json()['usage']['total_tokens'])*0.5)),self.persona[persona]['Name'])
                                    theMessageToSend = await theThread.send(embed=embedToSend)
                                    infoEmbed = await theThread.send(embed=createWarnEmbed(f"**Thread Information**\n\n**>Send one message at a time!!!<**\nUsed total Ori Coins: {usedTokens} OC\n**To delete thread**: `ori!delete`\n**To lock thread**: `ori!lock`"))
                                    ObjectClasses.registerMessage(theMessageToSend.id, ctx.message.author.id, self.persona[user.Persona]['Name'], msgInp.content, theReply, "Thread Message")

                        else:
                            await theThread.remove_user(ctx.message.author)
                            await theThread.send(embed=createWarnEmbed(f'You have insufficient balance!\nYou need at least 5000 OriCoins to continue a conversation!\nYour current balance is {user.tokensBalance}\n\n**The persona will no longer reply.**'))
                            lock = await theThread.send(embed=createWarnEmbed(f"**Thread Information**\n\n**>THIS THREAD HAS BEEN LOCKED<**\nUsed total Ori Coins: {usedTokens} OC"))
                            await theMessage.edit(embed=createWarnEmbed(f'Thread is locked!\n[Click here to view thread]({theThread.jump_url})'))
                            await theThread.edit(locked=True, archived=True)
                            break

                    elif (msgInp.content).lower()=="ori!delete":
                        await theThread.delete()
                        await theMessage.edit(embed=createWarnEmbed('Thread is deleted!'))
                        break

                    elif (msgInp.content).lower()=="ori!lock":
                        await theMessage.edit(embed=createWarnEmbed(f'Thread is locked!\n[Click here to view thread]({theThread.jump_url})'))
                        await theThread.remove_user(ctx.message.author)
                        lock = await theThread.send(embed=createWarnEmbed(f"**Thread Information**\n\n**>THIS THREAD HAS BEEN LOCKED BY THE OWNER<**\nUsed total Ori Coins: {usedTokens} OC"))
                        await theThread.edit(locked=True, archived=True)
                        break

            else:
                await ctx.message.reply(embed=createWarnEmbed(f'You have insufficient balance!\nYou need at least 20000 OriCoins to create a conversation!\nYour current balance is {user.tokensBalance}'))
        except Exception as e:
            if str(e) == "list index out of range":
                warn = await ctx.message.reply(embed=createWarnEmbed('The persona you have mentioned does not exist!\n\nPlease try the command again!'))
                await asyncio.sleep(5)
                await warn.delete()
            elif str(e) == "'usage'" or str(e) == "":
                 await theMessage.edit(embed=createWarnEmbed(f'Thread is locked!\n[Click here to view thread]({theThread.jump_url})'))
                 await theThread.send(content=f'There was an error while processing your message.\nCauses for this might be server congestions at the AI servers.\nOr the persona has reached its maximum load.')
                 await theThread.edit(locked=True, archived=True)
            else:
                print(e)
                
async def setup(bot):
    await bot.add_cog(ThreadCommands(bot))