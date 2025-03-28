# Version: 1.2
# Date: 2/26/2025
import discord
from discord.ext import commands
import random,os,asyncio,sqlite3, ObjectClasses, OriChanRun
from datetime import datetime
import datetime as dt
import asyncOpenAI, base64, aiohttp, io, docx
from pypdf import PdfReader
dividerImg="https://cdn.discordapp.com/attachments/1054984334878191636/1061806291091210320/image.png"
DB='Database/Main.db'
def user_exists(ID):
    conn = sqlite3.connect(DB)
    cursor = conn.execute('''SELECT * FROM users WHERE ID=?''', (ID,))
    row = cursor.fetchone()
    conn.close()
    return row is not None
def createPersonaEmbed(title,description):
    # Set the color, thumbnail, and footer of the embed
    color = 0x5C0E80
    footer_text = "Ori-chan & Friends."
    footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png"
    # Create the embed
    embed = discord.Embed(title=f"Persona Menu {title}", description=description, color=color)
    embed.set_footer(text=footer_text, icon_url=footer_icon)
    embed.set_image(url=dividerImg)
    return embed
def createChallengeEmbed():
    # Set the color, thumbnail, and footer of the embed
    color = 0x5C0E80
    footer_text = "Ori-chan & Friends."
    footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png" #❓ ❔
    description=f"Here's another OriChan challenge with a new look!\n\n**❔Firstly, who's <@761658981034754058>?**\nThis bot offers an AI assistant called a \"persona\" so you can have conversations anytime and anywhere. With 8 unique personas to choose from, you'll be able find one that suits your needs. These personas can help you with any task from giving custom recipes to providing feedback. To use these personas, however, requires OriCoins which are acquired by talking in the server, doing daily rewards, or participating in events.\n\n**❓⊱Then what's the challenge?**\n⊱*Create a funny thread with a persona!*\n⊱How funny? As funny as you can make it to be!\n⊱For clarifications, just ask <@224143661510819840>!\n\n**❔⊱How to submit your entry?**\n⊱There'll be a public thread under this message.\n⊱Post screenshots or links to your threads!\n\n**❓⊱How to get started?**\n⊱First go to the channel: <#1058666466876063836>\n⊱Start a thread with a persona using `ori!st`\n⊱For further help, use the `ori!help` command!\n\n**❔⊱What do you win?**\n⊱Those that are judged to be funny get **20,000** OriCoins!\n⊱Unfunny ones get 10,000 OriCoins for participating!\n⊱Funniest one gets an extra 25,000 OriCoins!\n\n**❓⊱Is there a deadline?**\n⊱Until the thread below closes!\n⊱So, *24* hours from when this post was made!"
    # Create the embed
    embed = discord.Embed(title="🏆Challenge Time🏆", description=description, color=color)
    embed.set_footer(text=footer_text, icon_url=footer_icon)
    embed.set_image(url=dividerImg)
    return embed
def createWarnEmbed(description):
    # Set the color, thumbnail, and footer of the embed
    color = 0x5C0E80
    footer_text = "Ori-chan & Friends."
    footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png"
    # Create the embed
    embed = discord.Embed(title="🚨Warning🚨", description=description, color=color)
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
def createUserInfoEmbed(username,userid, userthumbnail):
    # Set the color, thumbnail, and footer of the embed
    color = 0x5C0E80
    thumbnail = userthumbnail
    footer_text = "Ori-chan & Friends."
    footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png"
    title=f"{username}'s Info!"
    user=ObjectClasses.User(userid)

    role=user.role
    roleToShow=""

    if role in ['standardDonator','bundleDonator1','bundleDonator2','bundleDonator3']:
        roleToShow="Donator"
    elif role == 'betaTester':
        roleToShow="Beta Tester"
    elif role == 'developer':
        roleToShow="Developer"
    elif role == 'freeRole':
        roleToShow="Standard"


    if user.lastDaily is None:
        lastDailyString="No daily yet!"
    else:
        lastDailyString=user.lastDaily.strftime("%I:%M %p - %m/%d/%Y CEST")
    description=f"Current persona: {ObjectClasses.Persona(int(user.Persona)).Name}\nUser role: {roleToShow}\nOriCoins: {user.tokensBalance} OC\n\n**Streak Info:**\nDaily Streak: {user.dailyStreak}\nLast Daily: {lastDailyString}\n\n**Inventory:**\nCharacter Limit Unlock Card: {user.characterLimitUnlockCard}\nStreak Protection Star: {user.streakProtectionStar}\nCommon Persona Shard: {user.commonPersonaShard}\nPremium Persona Shard: {user.premiumPersonaShard}"
    # Create the embed
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_thumbnail(url=thumbnail)
    embed.set_footer(text=footer_text, icon_url=footer_icon)
    embed.set_image(url=dividerImg)
    return embed
def createDonationEmbed():
    # Set the color, thumbnail, and footer of the embed
    color = 0x5C0E80
    thumbnail = "https://media.discordapp.net/attachments/1054984334878191636/1061815855459082350/61e1116779fc0a9bd5bdbcc7_Frame206.png"
    footer_text = "Ori-chan & Friends."
    footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png"
    roles={
        "7$ & Under":{
            "CharacterLimit": 600,
            "BaseDaily": 7500,
            "StreakBonus": 1150},
        "8$-11$":{
            "CharacterLimit": 750,
            "BaseDaily": 12500,
            "StreakBonus": 1850},
        "12$-14$":{
            "CharacterLimit": 1000,
            "BaseDaily": 15000,
            "StreakBonus": 2500},
        "15$ & Up":{
            "CharacterLimit": 'Unlimited',
            "BaseDaily": 17500,
            "StreakBonus": 3500}
        }
    title = "💵Donation Info💵"
    description="\n**[Click here to donate!](https://ko-fi.com/orichan)**\n\nYour donation would help support the development of Ori-san, as she is constantly learning and growing as an AI, making her more effective in helping people. Keeping her running and developing her costs <@224143661510819840> a lot of money too.\n\nHowever, by donating you'll get the following perks:\nOn top of the perks below, for every 1$ donated, you'll get 50,000 OriCoins.\n\n`CL`: Character limit\n`DR`: Base daily reward amount.\n`SB`: Bonus per daily streak."
    # Create the embed
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_thumbnail(url=thumbnail)
    embed.set_footer(text=footer_text, icon_url=footer_icon)
    embed.set_image(url=dividerImg)
    count=0
    for x in roles.keys():
        count+=1
        embed.add_field(name=f"Donation of {x}:", value=f"┇⊸⊱`CL`: {roles[x]['CharacterLimit']}\n┇⊸⊱`DR`: {roles[x]['BaseDaily']} OC\n╰⊸¤⊱`SB`: {roles[x]['StreakBonus']} OC", inline=True)
        if count==2:
            embed.add_field(name="\u200b", value=f"\u200b", inline=False)
    return embed

class MainClass(commands.Cog):
    def __init__(self,bot):
        Data=OriChanRun.loadData()
        self.bot = bot
        self.StandardFilterThreshold = 10.00
        self.keyToUse=0
        self.APIKEYLIST=Data['APIKeys']
        self.permittedChannels=[1064342742756499518, 1058810679424995328, 'DM', 1062492948035543041, 1062982724148805663]
        self.persona = ObjectClasses.getPersonas()
        self.activeUsers={}
    def ContentCheckStd(self, content, APIKEYTOUSE):
        return False
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="Commands: /help"))
        print(f"[+]: {self.bot.user.name} Main Cog is ready.")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            ifUserExists=user_exists(message.author.id)
            if message.author == self.bot.user:
                return
            else:
                if ifUserExists:
                    if message.author.id not in self.activeUsers.keys():
                        self.activeUsers[message.author.id]=[dt.datetime.now(), True]
                    else:
                        if self.activeUsers[message.author.id][1] == False:
                            self.activeUsers[message.author.id][1]=True
                            user=ObjectClasses.User(message.author.id)
                            user.tokensBalance+=75
                            user.save_to_database()
                        elif self.activeUsers[message.author.id][1] == True:
                            diff = dt.datetime.now() - self.activeUsers[message.author.id][0]
                            if diff.total_seconds() >= 5:
                                self.activeUsers[message.author.id][0]=dt.datetime.now()
                                self.activeUsers[message.author.id][1]=False
                                
            if isinstance(message.channel, discord.DMChannel):
                if ifUserExists:
                    user=ObjectClasses.User(message.author.id)
                    if user.role != "freeRole" or user.role != "betaTester":
                        theChannel="DM"
                        self.StandardFilterThreshold = 0.555
            else:
                theChannel=message.channel.id
                self.StandardFilterThreshold = 0.455
            if theChannel in self.permittedChannels:
                if f"<@{self.bot.user.id}>" in message.content or message.reference!=None:
                    if message.reference!=None:
                        try:
                            Fwoop = ObjectClasses.getMessage(message.reference.message_id)
                            if Fwoop == None:
                                return                    
                        except Exception as e:
                            return
                    if ifUserExists:
                        user=ObjectClasses.User(message.author.id)
                    else:
                        user=ObjectClasses.User(message.author.id,25000,"freeRole",0)
                        user.save_to_database()
                    messageContent=message.content.replace(f"<@{self.bot.user.id}>","")
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
                    if len(messageContent) <= charLimit:
                        theKey=ObjectClasses.GetAKey()
                        async with message.channel.typing():
                            check=self.ContentCheckStd(messageContent,theKey)
                        if check==False:
                            if user.tokensBalance>2000:
                                if CharUnlockFoo == 1:
                                    user.characterLimitUnlockCard -= 1
                                    user.save_to_database()
                                async with message.channel.typing():
                                    messages = [{"role": "system", "content": f'<System Prompt>\n{((self.persona[user.Persona]["Prompt"]).replace("[[JAYWASHERE123123JAYWASHERE]]", f"{str(message.author)}")).replace("[[ARUHELPEDMELUL]]", f"*walks in*\n\nEnd of example conversation.")}\n{self.persona[user.Persona]["Name"]} should always use {str(message.author)}\'s name in the conversation.\n<End System Prompt>\n{self.persona[user.Persona]["Name"]} is currently talking to: {str(message.author)}\nCurrent date (DD/MM/YYYY): {datetime.now().day}/{datetime.now().month}/{datetime.now().year}\n'}]
                                    if message.reference!=None:
                                        messageReference = ObjectClasses.getMessage(message.reference.message_id)
                                        if messageReference[2] == ObjectClasses.Persona(user.Persona).Name:
                                            if messageReference[3] == user.ID:   
                                                messages.append({"role": "user", "content": [{'type': "text", "text": messageReference[0]}]})
                                                messages.append({"role": "assistant", "content": [{'type': "text", "text": messageReference[1]}]})
                                                
                                                if message.attachments:
                                                    if messageContent=="":
                                                        msgContent = [{'type': "text", "text": "The user has not provided any text content."}]
                                                    else:
                                                        msgContent = [{'type': "text", "text": messageContent}]
                                                    for attachment in message.attachments:
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
                                                                        await message.reply(embed=createWarnEmbed("Please only upload mp3 or wav files!"), delete_after=5.0)
                                                                        break
                                                    messages.append({"role": "user", "content": msgContent})
                                                    
                                                else:
                                                    content = messageContent
                                                    messages.append({"role": "user", "content": content})
                                            else:
                                                await message.reply(embed=createWarnEmbed("Please only reply to your own message!"), delete_after=5.0)
                                                await asyncio.sleep(5)
                                                await message.delete()
                                                return
                                        else:
                                            await message.reply(embed=createWarnEmbed("Please only reply to the same persona you've referenced!"),  delete_after=5.0)  
                                            await asyncio.sleep(5)
                                            await message.delete()
                                            return
                                    else:
                                        if message.attachments:
                                            if messageContent=="":
                                                msgContent = [{'type': "text", "text": "The user has not provided any text content."}]
                                            else:
                                                msgContent = [{'type': "text", "text": messageContent}]
                                            for attachment in message.attachments:
                                                print(attachment.content_type)
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
                                                                await message.reply(embed=createWarnEmbed("Please only upload mp3 or wav files!"), delete_after=5.0)
                                                                break
                                            messages.append({"role": "user", "content": msgContent})
                                        else:
                                            messages.append({"role": "user", "content": messageContent})
                                    promptToSend = messages                           
                                    theResponse=await asyncOpenAI.chat_complete(theKey, timeout=30, payload={'model': 'gemini-2.0-flash-exp',
                                                                                    "messages": promptToSend,
                                                                                                             "temperature": 1,
                                                                                                             "top_p":1,
                                                                                                             "max_completion_tokens": 4096})

                                    now = datetime.now().strftime("%H:%M:%S")                       
                                    print(f"[{now}] - {theResponse}\nUsed key: {(theKey)[-7:]}\nTokens used: {theResponse.json()['usage']['total_tokens']}\nUser: {message.author} - {message.author.id}")
                                    usedTokens=0
                                    usedTokens+=round(int(theResponse.json()['usage']['total_tokens'])*0.5)
                                    user.tokensBalance-=round(int(theResponse.json()['usage']['total_tokens'])*0.5)
                                    user.save_to_database()
                                    theReply=theResponse.json()['choices'][0]['message']['content']
                                    embedToSend=createReplyEmbed(theReply, str(round(int(theResponse.json()['usage']['total_tokens'])*0.5)),f"{self.persona[user.Persona]['Name']} (1)")
                                theMessageToSend = await message.reply(embed=embedToSend)
                                
                                ObjectClasses.registerMessage(theMessageToSend.id, message.author.id, self.persona[user.Persona]['Name'], messageContent, theReply, "Message")
                                #▶️ ◀️
                                listOfEmbeds=[embedToSend]
                                currMessage=0
                                repeatEmote="🔁"
                                forwardEmote="▶️"
                                backwardEmote="◀️"
                                await theMessageToSend.add_reaction(backwardEmote)
                                await theMessageToSend.add_reaction(repeatEmote)
                                await theMessageToSend.add_reaction(forwardEmote)
                                def check(reaction, theuser):
                                    return theuser == message.author and str(reaction.emoji) in [repeatEmote, forwardEmote, backwardEmote]
                                while True:
                                    try:
                                        reaction, theuser = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
                                    except asyncio.TimeoutError:
                                        await theMessageToSend.clear_reactions()
                                        break
                                    await reaction.remove(theuser)
                                    if reaction.message.id == theMessageToSend.id:    
                                        if str(reaction.emoji) == repeatEmote:
                                            if user.tokensBalance >= 2000:
                                                async with message.channel.typing():
                                                    theKey=ObjectClasses.GetAKey()
                                                    theResponse=await asyncOpenAI.chat_complete(theKey, timeout=30, payload={'model': 'gemini-2.0-flash-exp',
                                                                                    "messages": promptToSend,
                                                                                                             "temperature":1,
                                                                                                             "top_p":1,
                                                                                                             "max_completion_tokens": 4096})
                                                    now = datetime.now().strftime("%H:%M:%S")
                                                    print(f"[{now}] - {theResponse}\nUsed key: {(theKey)[-7:]}\nTokens used: {theResponse.json()['usage']['total_tokens']}\nUser: {message.author} - {message.author.id}")
                                                    user.tokensBalance-=round(int(theResponse.json()['usage']['total_tokens'])*0.5)
                                                    user.save_to_database()                                            
                                                    usedTokens+=round(int(theResponse.json()['usage']['total_tokens'])*0.5)
                                                    theReply=theResponse.json()['choices'][0]['message']['content']
                                                    embedToSend=createReplyEmbed(theReply, str(round(int(theResponse.json()['usage']['total_tokens'])*0.5)),f"{self.persona[user.Persona]['Name']} ({len(listOfEmbeds)+1})")
                                                    listOfEmbeds.append(embedToSend)
                                                    currMessage=(len(listOfEmbeds)-1)
                                                    
                                                    
                                                    
                                                await theMessageToSend.edit(embed=listOfEmbeds[currMessage])
                                                ObjectClasses.registerMessage(theMessageToSend.id, message.author.id, self.persona[user.Persona]['Name'], messageContent, theReply, f"Reroll Message #{len(listOfEmbeds)}")
                                            else:
                                                await message.channel.send(embed=createWarnEmbed(f'You have insufficient balance!\nYou need at least 2000 OriCoins to send <@{self.bot.user.id}> a message!\nYour current balance is {user.tokensBalance}'))
                                                await theMessageToSend.clear_reactions()
                                                break
                                        elif str(reaction.emoji) == forwardEmote:
                                            if currMessage == (len(listOfEmbeds)-1):
                                                currMessage = 0
                                            else:
                                                currMessage = min(len(listOfEmbeds) - 1, currMessage+1)
                                            embedToSend=listOfEmbeds[currMessage]
                                            await theMessageToSend.edit(embed=embedToSend)
                                        elif str(reaction.emoji) == backwardEmote:
                                            if currMessage == 0:
                                                currMessage = len(listOfEmbeds)-1
                                            else:
                                                currMessage = max(0, currMessage-1)
                                            embedToSend=listOfEmbeds[currMessage]
                                            await theMessageToSend.edit(embed=embedToSend)
                            else:
                                await message.reply(embed=createWarnEmbed(f'You have insufficient balance!\nYou need at least 2000 OriCoins to send <@{self.bot.user.id}> a message!\nYour current balance is {user.tokensBalance}'))
                        else:
                            await message.delete()
                            await message.channel.send(content=f'<@{message.author.id}>',embed=createWarnEmbed(f'Please only ask appropriate messages! <@{self.bot.user.id}> doesn\'t like these things!\nYour message contains the following: `{check}` content!'))
                    else:
                        await message.reply(embed=createWarnEmbed(f'Your message is too long!\nYour character limit is {user.getRoleInfo()["CharacterLimit"]}!\nYour message was {len(messageContent)}!'))
        except Exception as e:
            print(f"ERROR: {e} - {str(message.author)}")
            if str(e) == "'usage'" or str(e) == "":
                msg = await message.reply(content=f'There was an error while processing your message.\nCauses for this might be server congestions at the AI servers.\nOr the persona has taken too much time processing your message.')
                await asyncio.sleep(5)
                await msg.delete()
    
    @commands.command()
    async def giveAdmin(self,ctx,member:discord.Member, bal:int):
        try:
            memberid=member.id
            authorid=ctx.author.id
            if user_exists(memberid):
                userToGive=ObjectClasses.User(memberid)
            else:
                userToGive=ObjectClasses.User(memberid,25000,"freeRole",0)
                userToGive.save_to_database()

            if user_exists(authorid):
                userSender=ObjectClasses.User(authorid)
            else:
                userSender=ObjectClasses.User(authorid,25000,"freeRole",0)
                userSender.save_to_database()
            
            
            if userSender.role == "developer":
                userToGive.tokensBalance += bal
                userToGive.save_to_database()
                await ctx.message.delete()
                msg = await ctx.send(f"Sent {bal} OriCoins to <@{userToGive.ID}>")
            
            
        except Exception as e:
            print(e)

    @commands.command()
    @commands.is_owner()
    async def challenge(self, ctx):
        theMessage = await ctx.send(content='@everyone',embed=createChallengeEmbed())
        theThread = await theMessage.create_thread(name="Challenge Submission",auto_archive_duration=1440)
    @commands.command()
    @commands.is_owner()
    async def infoAdmin(self,ctx,member:discord.Member):
        try:
            if user_exists(member.id):
                user=ObjectClasses.User(member.id)
            else:
                user=ObjectClasses.User(member.id,25000,"freeRole",0)
                user.save_to_database()
            userThumbnail=member.avatar.url
            userid=member.id
            embedToSend=createUserInfoEmbed(f"{str(member)[:-5]}",userid, userThumbnail)
            await ctx.message.reply(content=f'<@{ctx.author.id}>',embed=embedToSend)
        except Exception as e:
            print(e)
    @commands.command()
    @commands.is_owner()
    async def changeRole(self,ctx,member:discord.Member, role:str):
        try:
            if user_exists(member.id):
                user=ObjectClasses.User(member.id)
            else:
                user=ObjectClasses.User(member.id,25000,"freeRole",0)
                user.save_to_database()
            user.role=role
            user.save_to_database()
            await ctx.message.reply(f'User: {member}\'s role is now: {role}!')
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(MainClass(bot))