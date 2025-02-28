import discord, ObjectClasses, asyncio, random
from discord.ext import commands

class Gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #WoopWoop
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[+]: {self.bot.user.name} Gacha Cog is ready.")
    
    @commands.command(aliases=["sc","collection","collections","c"])
    async def showCollection(self, ctx):
        try:
            def createCollectionEmbed(collectionID):
                collection = ObjectClasses.collection(collectionID)
                collections = ObjectClasses.getCollection()
                color = 0x5C0E80
                dividerImg = "https://cdn.discordapp.com/attachments/1054984334878191636/1061806291091210320/image.png"
                footer_text = "Ori-chan & Friends."
                footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png"
                
                personastr=""
                count=1
                for x in collection.Personas:
                    personastr+=f"[{count}]: {x.Name} ({x.Rarity})\n"
                    count+=1
                
                description = f"**Creator(s):** {collection.Creator}\n\nCollection description:\n```{collection.Description}```\n\nPersonas in the collection:\n```{personastr}```\n\n***More collections and personas will be added in the future!***"
                
                embedToSend = discord.Embed(title=f"Collection: {collection.Name} ({collection.ID}/{len(collections)})",description=description,color=color)
                embedToSend.set_footer(text=footer_text,icon_url=footer_icon)
                embedToSend.set_image(url=dividerImg)
                
                return embedToSend
                
            
            backButton = "◀️"
            forwardButton = "▶️"
            
            collections = ObjectClasses.getCollection()
            
            msgToSend = await ctx.reply(embed=createCollectionEmbed(1))
            
            
            await msgToSend.add_reaction(backButton)
            await msgToSend.add_reaction(forwardButton)
            currCollection = 1
            
            def check(reaction, theuser):
                return theuser == ctx.message.author and str(reaction.emoji) in [backButton, forwardButton]
            
            while True:
                try:
                    reaction, theuser = await self.bot.wait_for('reaction_add', timeout=150.0, check=check)
                
                except asyncio.TimeoutError:
                    await msgToSend.edit(content="Timeout!")
                    await asyncio.sleep(5)
                    await msgToSend.delete()
                    break
                
                
                await reaction.remove(theuser)
                
                if reaction.message.id == msgToSend.id:
                    if str(reaction.emoji) == backButton:
                        if currCollection == 1:
                            currCollection = len(collections)
                        else:
                            currCollection = max(1, currCollection-1)
                        
                        await msgToSend.edit(embed=createCollectionEmbed(currCollection))
                    elif str(reaction.emoji) == forwardButton:
                        if currCollection == len(collections):
                            currCollection = 1
                        else:
                            currCollection = min(len(collections), currCollection+1)
                        
                        await msgToSend.edit(embed=createCollectionEmbed(currCollection))                    
        except Exception as e:
            print(e)
    
    @commands.command(aliases=['op','personabox','pb','openbox'])
    async def openBox(self, ctx):
        try:
            if ObjectClasses.user_exists(ctx.author.id):
                user=ObjectClasses.User(ctx.author.id)
            else:
                user=ObjectClasses.User(ctx.author.id,25000,"freeRole",0)
                user.save_to_database()
            def createInfoEmbed(info):
                
                footer_text = "Ori-chan & Friends."
                footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png"
                dividerImg = "https://cdn.discordapp.com/attachments/1054984334878191636/1061806291091210320/image.png"
                color = 0x5C0E80
                embedToSend=discord.Embed(title="Persona Box Opening", description=info, color=color)
                embedToSend.set_footer(text=footer_text, icon_url=footer_icon)
                embedToSend.set_image(url=dividerImg)
                
                return embedToSend
            
            def checkWin(numbers, winningNumber):
                for x in numbers.keys():
                    if winningNumber in numbers[x]:
                        return x
                    
            def getPersonaPool(rarity):
                personaIDList = []
                dictOfPersonas = ObjectClasses.getPersonas()
                
                for x in dictOfPersonas.keys():
                    if dictOfPersonas[x]["Rarity"] == rarity:
                        personaIDList.append(x)
                
                return personaIDList

            commonPersonaPool = getPersonaPool("Common")
            premiumPersonaPool = getPersonaPool("Premium")

            Prizes = ['Random Premium Unlockable Persona 1x',
                      '250,000 OriCoins',
                      'Premium Persona Unlock Shard 1x',
                      'Random Common Unlockable Persona 1x',
                      'Common Persona Shard 2x',
                      '25,000 OriCoins',
                      '35,000 OriCoins',
                      'Character Limit Unlock Card 5x',
                      'Streak Protection Star 3x']
            Odds = [2,2,6,15,10,25,15,15,10]
            
            
            PrizesAndOddsString=""
            for x, y in zip(Prizes, Odds):
                PrizesAndOddsString+=f"{y}% : {x}\n"
            
            
            
            messageToSend = await ctx.reply(embed=createInfoEmbed(f"\n\n**PersonaBox odds**:\n```{PrizesAndOddsString}```\n\n**Persona Box Cost: 25,000 OriCoins**\nYour Balance: {user.tokensBalance} OC\n\n***Click on the checkmark below to open a box!***"))
            
            checkmark = "✅"
            xmark = "❎"
            await messageToSend.add_reaction(checkmark)
            await messageToSend.add_reaction(xmark)
            def check(reaction, theuser):
                return theuser == ctx.message.author and str(reaction.emoji) in [checkmark, xmark]
            
            while True:
                try:
                    reaction, theuser = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
                except asyncio.TimeoutError:
                    await messageToSend.edit(embed=createInfoEmbed(f"Timed out!"))
                    await asyncio.sleep(5)
                    await messageToSend.delete()
                    break
                
                

                if reaction.message.id == messageToSend.id:
                    await messageToSend.clear_reactions()
                    if str(reaction.emoji) == checkmark:
                        if user.tokensBalance < 25000:
                            await messageToSend.edit(embed=createInfoEmbed(f"You need 25,000 OriCoins to open a box!"))
                            await asyncio.sleep(5)
                            await messageToSend.delete()
                            break
                        elif user.tokensBalance >= 25000:
                            user.tokensBalance -= 25000
                            user.save_to_database()
                            numbers = ObjectClasses.assign_random_numbers(Prizes, Odds)
                            winningNumber = random.randint(1,100)
                            countdown = 4
                            
                            async with ctx.channel.typing():
                                await messageToSend.edit(embed=createInfoEmbed(f"Rolling in 5 seconds!"))

                                await asyncio.sleep(1)

                                for x in range(countdown):
                                    await messageToSend.edit(embed=createInfoEmbed(f"Rolling in {countdown} seconds!"))
                                    countdown = countdown - 1
                                    await asyncio.sleep(1)
                                else:
                                    win = checkWin(numbers, winningNumber)
                                    personaToUnlock = None
                                    if win == "Random Premium Unlockable Persona 1x":
                                        personaToUnlock = random.choice(premiumPersonaPool)
                                        user.unlockPersona(personaToUnlock)
                                        user.save_to_database()
                                    elif win == '250,000 OriCoins':
                                        user.tokensBalance += 250000
                                        user.save_to_database()
                                    elif win == 'Premium Persona Unlock Shard 1x':
                                        user.premiumPersonaShard += 1
                                        user.save_to_database()
                                    elif win == 'Random Common Unlockable Persona 1x':
                                        personaToUnlock = random.choice(commonPersonaPool)
                                        user.unlockPersona(personaToUnlock)
                                        user.save_to_database()
                                    elif win == 'Common Persona Shard 2x':
                                        user.commonPersonaShard += 2
                                        user.save_to_database()
                                    elif win == '25,000 OriCoins':
                                        user.tokensBalance += 25000
                                        user.save_to_database()
                                    elif win == '35,000 OriCoins':
                                        user.tokensBalance += 35000
                                        user.save_to_database()
                                    elif win == 'Character Limit Unlock Card 5x':
                                        user.characterLimitUnlockCard +=5
                                        user.save_to_database()
                                    elif win == 'Streak Protection Star 3x':
                                        user.streakProtectionStar +=3
                                        user.save_to_database()
                                    
                                    if win in ["Random Common Unlockable Persona 1x", "Random Premium Unlockable Persona 1x"]:
                                        persona = ObjectClasses.Persona(personaToUnlock)
                                        await messageToSend.edit(embed=createInfoEmbed(f"Congratulations! You won the following:\n```{win}```\nYou've unlocked the following persona ***{persona.Name}*** from the collection: **{persona.Collection}**!\n*If you already own this persona, you'll be given 5 shards equivalent to the personas rarity!*\n\nWant a receipt of your roll? Click on the checkmark below.\nWant to remove messages? Click the 'x' below."))
                                    else:
                                        await messageToSend.edit(embed=createInfoEmbed(f"Congratulations! You won the following:\n```{win}```\n\nWant a receipt of your roll? Click on the checkmark below.\nWant to remove messages? Click the 'x' below."))
                                    
                                    break
                    elif str(reaction.emoji) == xmark:
                        await asyncio.sleep(2)
                        await messageToSend.delete()
                        await ctx.message.delete()
                        break
            await messageToSend.add_reaction(checkmark)
            await messageToSend.add_reaction(xmark)
            while True:
                try:
                    reaction, theuser = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await messageToSend.clear_reactions()
                    await messageToSend.delete()
                    await ctx.message.delete()
                    break
                if reaction.message.id == messageToSend.id:
                    await messageToSend.clear_reactions()
                    if str(reaction.emoji) == checkmark:
                        discUser = self.bot.get_user(user.ID)
                        if discUser:
                            try:
                                tosendString = ""
                                for x in numbers.keys():
                                    tosendString += f"*{x}*\n```"
                                    for y in numbers[x]:
                                        tosendString+=f"{y}, "
                                    else:
                                        tosendString+="```\n"
                                await discUser.send(embed=createInfoEmbed(f"**Roll information**\n\n{tosendString}\n\nYour winning number is **{winningNumber}**\nYou therefore won {win}"))
                                await asyncio.sleep(3)
                                await messageToSend.delete()
                                await ctx.message.delete()
                                break

                            except Exception as e:
                                print(e)
                    elif str(reaction.emoji) == xmark:
                        await asyncio.sleep(3)
                        await messageToSend.delete()
                        await ctx.message.delete()
                        break

        except Exception as e:
            print(e)
            
    @commands.command(aliases=["shard","Shard"])
    async def unlockShards(self, ctx):
        try:
            if ObjectClasses.user_exists(ctx.author.id):
                user=ObjectClasses.User(ctx.author.id)
            else:
                user=ObjectClasses.User(ctx.author.id,25000,"freeRole",0)
                user.save_to_database()
            def createInfoEmbed(info):
                
                footer_text = "Ori-chan & Friends."
                footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png"
                dividerImg = "https://cdn.discordapp.com/attachments/1054984334878191636/1061806291091210320/image.png"
                color = 0x5C0E80
                embedToSend=discord.Embed(title="Persona Unlock Shards", description=info, color=color)
                embedToSend.set_footer(text=footer_text, icon_url=footer_icon)
                embedToSend.set_image(url=dividerImg)
                
                return embedToSend
            #🟡⚪
            
            def getPersonaPool(rarity):
                personaIDList = []
                dictOfPersonas = ObjectClasses.getPersonas()
                
                for x in dictOfPersonas.keys():
                    if dictOfPersonas[x]["Rarity"] == rarity:
                        personaIDList.append(x)
                
                return personaIDList

            commonPersonaPool = getPersonaPool("Common")
            premiumPersonaPool = getPersonaPool("Premium")

            messageToSend = await ctx.reply(embed=createInfoEmbed(f"Persona unlock shards are obtained from \"PersonaBoxes\", and these are used to unlock personas that you currently don't have. If you manage to get a persona that you own, you'll be given back the shards you've used. Using persona unlock shards will unlock one persona from the assortment of personas at the specified rarity.\n\n**5 Persona Shards per persona!**\n\n**Your shard inventory:**\n[🟡]: You have {user.premiumPersonaShard} Premium Persona Shard(s).\n[⚪]: You have {user.commonPersonaShard} Common Persona Shard(s).\n\n***To use your shards, click on the corresponding emotes below.***"))
            premiumEmote = "🟡"
            commonEmote = "⚪"
            
            await messageToSend.add_reaction(premiumEmote)
            await messageToSend.add_reaction(commonEmote)

            def check(reaction, theuser):
                return theuser == ctx.message.author and str(reaction.emoji) in (premiumEmote, commonEmote)
            
            while True:
                try:
                    reaction, theuser = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
                except asyncio.TimeoutError:
                    await messageToSend.clear_reactions()
                    await messageToSend.edit(embed=createInfoEmbed(f"Timed out!"))
                    await asyncio.sleep(5)
                    await messageToSend.delete()
                    break
                
                await messageToSend.clear_reactions()
                
                if reaction.message.id == messageToSend.id:
                    if str(reaction.emoji) in [premiumEmote, commonEmote]:
                        
                        if str(reaction.emoji) == premiumEmote:
                            if user.premiumPersonaShard < 5:
                                await messageToSend.edit(embed=createInfoEmbed(f"You don't have enough Premium Persona Shards"))
                                await asyncio.sleep(5)
                                await messageToSend.delete()
                                break
                        elif str(reaction.emoji) == commonEmote:
                            if user.commonPersonaShard < 5:
                                await messageToSend.edit(embed=createInfoEmbed(f"You don't have enough Common Persona Shards"))
                                await asyncio.sleep(5)
                                await messageToSend.delete()
                                break                            
                        
                        countdown = 4
                        await messageToSend.edit(embed=createInfoEmbed(f"Rolling in 5 seconds..."))
                        await asyncio.sleep(1)
                        
                        for x in range(countdown):
                            await messageToSend.edit(embed=createInfoEmbed(f"Rolling in {countdown} seconds..."))
                            countdown -= 1
                            await asyncio.sleep(1)
                        else:
                            if str(reaction.emoji) == premiumEmote:
                                user.premiumPersonaShard -= 5
                                user.save_to_database()
                                Persona = ObjectClasses.Persona(random.choice(premiumPersonaPool))
                                user.unlockPersona(Persona.ID)
                            elif str(reaction.emoji) == commonEmote:
                                user.commonPersonaShard -= 5
                                user.save_to_database()
                                Persona = ObjectClasses.Persona(random.choice(commonPersonaPool))
                                user.unlockPersona(Persona.ID)
                            
                            await messageToSend.edit(embed=createInfoEmbed(f"Congratulations! You have unlocked **{Persona.Name}** from the collection: {Persona.Collection}!\n\n*If you already own this persona, you will be given back the shards you've used.*"))
            
        except Exception as e:
            print(e)
    
    @commands.command(aliases=["clu","unlockcl","char"])
    async def toggleCL(self, ctx):
        try:
            def createInfoEmbed(info):
                
                footer_text = "Ori-chan & Friends."
                footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png"
                dividerImg = "https://cdn.discordapp.com/attachments/1054984334878191636/1061806291091210320/image.png"
                color = 0x5C0E80
                embedToSend=discord.Embed(title="Character Limit Unlock", description=info, color=color)
                embedToSend.set_footer(text=footer_text, icon_url=footer_icon)
                embedToSend.set_image(url=dividerImg)
                
                return embedToSend
            if ObjectClasses.user_exists(ctx.author.id):
                user=ObjectClasses.User(ctx.author.id)
            else:
                user=ObjectClasses.User(ctx.author.id,25000,"freeRole",0)
                user.save_to_database()
                
            
            
            if user.CLUnlock == 0:
                if user.characterLimitUnlockCard != 0:
                    user.CLUnlock = 1
                    user.save_to_database()
                    await ctx.reply(embed=createInfoEmbed(f"You have toggled your character limit unlock card.\nYour next messages will consume your character limit unlock cards."), delete_after=5.0)
                    await asyncio.sleep(5)
                    await ctx.message.delete()
                else:
                    await ctx.reply(embed=createInfoEmbed(f"You need at least 1 Character Limit Unlock Card to toggle this!"), delete_after=5.0)
                    await asyncio.sleep(5)
                    await ctx.message.delete()
            else:
                user.CLUnlock = 0
                user.save_to_database()
                await ctx.reply(embed=createInfoEmbed(f"You have toggled your character limit unlock card.\nYou will no longer consume any character limit unlock cards"), delete_after=5.0)
                await asyncio.sleep(5)
                await ctx.message.delete()
        except Exception as e:
            print(e)
    
    @commands.command(aliases=["search"])
    async def persona(self,ctx, *,stringToSearch:str):
        try:
            results = ObjectClasses.searchPersonas(stringToSearch)
            
            def createPersonaEmbed(title,personaID):
                # Set the color, thumbnail, and footer of the embed
                color = 0x5C0E80
                dividerImg="https://cdn.discordapp.com/attachments/1054984334878191636/1061806291091210320/image.png"
                footer_text = "Ori-chan & Friends."
                footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png"
                # Create the embed
                persona = ObjectClasses.Persona(personaID)
                description = f"**Persona Name: {persona.Name}**\n\n**Base Cost: {persona.Cost}**\n**Collection:** {persona.Collection}\n\n**Persona Description: ```{persona.Description}```**\n\n**Persona Introduction: ```{persona.Introduction}```**\n\n*Use the buttons below to view the other matching personas!*"
                embed = discord.Embed(title=f"Persona Menu {title}", description=description, color=color)
                embed.set_footer(text=footer_text, icon_url=footer_icon)
                embed.set_image(url=dividerImg)
                return embed
            if results!=[]:
                currPersona = 0
                messageToSend = await ctx.reply(embed=createPersonaEmbed(f"({currPersona+1}/{len(results)})", results[currPersona].ID))
                forwardEmote="▶️"
                backwardEmote="◀️"
                def check(reaction, theuser):
                    return theuser == ctx.message.author and str(reaction.emoji) in [ forwardEmote, backwardEmote]
                await messageToSend.add_reaction(backwardEmote)
                await messageToSend.add_reaction(forwardEmote)
                
                
                while True:
                    try:
                        reaction, theuser = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
                    except asyncio.TimeoutError:
                        await messageToSend.delete()
                        await ctx.message.delete()
                        break
                    
                    
                    
                    if reaction.message.id == messageToSend.id:
                        await reaction.remove(theuser)
                        if str(reaction.emoji) == forwardEmote:
                            if currPersona == (len(results)-1):
                                currPersona = 0
                            else:
                                currPersona = min(len(results)-1, currPersona+1)
                            await messageToSend.edit(embed=createPersonaEmbed(f"({currPersona+1}/{len(results)})", results[currPersona].ID))
                        if str(reaction.emoji) == backwardEmote:
                            if currPersona == 0:
                                currPersona = len(results) - 1
                            else:
                                currPersona = max(0, currPersona-1)
                            await messageToSend.edit(embed=createPersonaEmbed(f"({currPersona+1}/{len(results)})", results[currPersona].ID))
            else:
                await ctx.reply(f"No results found for `{stringToSearch}`. Please try again.", delete_after=5.0)
            
        except Exception as e:
            print(e)
    
    @commands.command(aliases=['pi','pinv'])
    async def personaInventory(self, ctx):
        try:
            def createInfoEmbed(info):
                
                footer_text = "Ori-chan & Friends."
                footer_icon = "https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png"
                dividerImg = "https://cdn.discordapp.com/attachments/1054984334878191636/1061806291091210320/image.png"
                color = 0x5C0E80
                embedToSend=discord.Embed(title="Unlocked Personas", description=info, color=color)
                embedToSend.set_footer(text=footer_text, icon_url=footer_icon)
                embedToSend.set_image(url=dividerImg)
                
                return embedToSend
            if ObjectClasses.user_exists(ctx.author.id):
                user=ObjectClasses.User(ctx.author.id)
            else:
                user=ObjectClasses.User(ctx.author.id,25000,"freeRole",0)
                user.save_to_database()
            
            userPersonas = user.getUserPersonas()
            
            personaString = "[CPID] [Name] [Collection] [Rarity]\n"
            
            for x in userPersonas.keys():
                personaString += f"[{x+1}]: {userPersonas[x]['Name']}, {userPersonas[x]['Collection']} - {userPersonas[x]['Rarity']}\n"
            
            
            embedToSend = createInfoEmbed(f"You currently own the following unlockable personas:\n```{personaString}```")
            await ctx.reply(embed=embedToSend)
            
            
            
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(Gacha(bot))
