# Version: 1.1
# Date: 1/24/2023
import random,os,openai,asyncio,sqlite3, OriChanRun, random
from typing import Dict
from datetime import datetime
import datetime as dt
DB='Database/Main.db'

class User:
    def __init__(self, ID, TokensBalance=None, Role=None, Persona=None):
        self.ID = ID
        self.tokensBalance = TokensBalance
        self.role = Role
        self.lastDaily = None
        self.dailyStreak = 0
        self.Persona=Persona
        self.streakProtectionStar = 0
        self.characterLimitUnlockCard = 0
        self.commonPersonaShard = 0
        self.premiumPersonaShard = 0
        self.CLUnlock = 0

        if (TokensBalance is None) and (Role is None) and (Persona is None):
            self.load_from_database()
        else:
            conn = sqlite3.connect(DB)
            last_daily_string = None
            if self.lastDaily is not None:
                last_daily_string = self.lastDaily.isoformat()
            conn.execute('''
                INSERT INTO users (ID, tokensBalance, role, lastDaily, dailyStreak, persona, streakProtectionStar, characterLimitUnlockCard, commonPersonaShard, premiumPersonaShard, CLUnlock)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.ID, self.tokensBalance, self.role, last_daily_string, self.dailyStreak, self.Persona, self.streakProtectionStar, self.characterLimitUnlockCard, self.commonPersonaShard, self.premiumPersonaShard, self.CLUnlock))

            conn.commit()
            conn.close()

    def load_from_database(self):
        conn = sqlite3.connect(DB)
        cursor = conn.execute('''SELECT * FROM users WHERE ID=?''', (self.ID,))
        row = cursor.fetchone()
        if row is not None:
            self.tokensBalance = row[1]
            self.role = row[2]
            last_daily_string = row[3]
            if last_daily_string is not None:
                self.lastDaily = datetime.fromisoformat(last_daily_string)
            self.dailyStreak = row[4]
            self.Persona = row[5]
            self.streakProtectionStar = row[6]
            self.characterLimitUnlockCard = row[7]
            self.commonPersonaShard = row[8]
            self.premiumPersonaShard = row[9]
            self.CLUnlock = row[10]
        conn.close()

    def save_to_database(self):
        conn = sqlite3.connect(DB)
        last_daily_string = None
        if self.lastDaily is not None:
            last_daily_string = self.lastDaily.isoformat()
        conn.execute('''

            UPDATE users SET tokensBalance=?, role=?, lastDaily=?, dailyStreak=?, persona=?, streakProtectionStar=?, characterLimitUnlockCard=?, commonPersonaShard=?, premiumPersonaShard=?, CLUnlock=? WHERE ID=?

        ''', (self.tokensBalance, self.role, last_daily_string, self.dailyStreak, self.Persona,self.streakProtectionStar, self.characterLimitUnlockCard, self.commonPersonaShard, self.premiumPersonaShard, self.CLUnlock ,self.ID))
        conn.commit()
        conn.close()
    #PROPERTIES


    def getRoleInfo(self):
        roles={
        "freeRole":{
            "CharacterLimit": 450,
            "BaseDaily": 5000,
            "StreakBonus": 1000},
        "standardDonator":{
            "CharacterLimit": 600,
            "BaseDaily": 7500,
            "StreakBonus": 1150},
        "bundleDonator1":{
            "CharacterLimit": 750,
            "BaseDaily": 12500,
            "StreakBonus": 1850},
        "bundleDonator2":{
            "CharacterLimit": 1000,
            "BaseDaily": 15000,
            "StreakBonus": 2500},
        "bundleDonator3":{
            "CharacterLimit": 9999,
            "BaseDaily": 17500,
            "StreakBonus": 3500},
        "betaTester":{
            "CharacterLimit": 550,
            "BaseDaily": 8000,
            "StreakBonus": 1250},
        "developer":{
            "CharacterLimit": 99999,
            "BaseDaily": 8000,
            "StreakBonus": 1500},
        }

        for x in roles.keys():
            if x == self.role:
                return roles[x]

    def DoDaily(self):
        role=self.getRoleInfo()
        streakProtectionStar=self.streakProtectionStar

        if self.dailyStreak==0:
            self.tokensBalance+=role['BaseDaily']
            self.dailyStreak+=1
            now=datetime.now()
            self.lastDaily=now
            self.save_to_database()
            return True
        else:
            now=datetime.now()
            diff=now - self.lastDaily
            if diff.total_seconds() >= 86400:
                if diff.total_seconds() <= 86400+86400:
                    self.tokensBalance+=(role['BaseDaily']+(role['StreakBonus']*self.dailyStreak))
                    self.dailyStreak+=1
                    if self.dailyStreak >= 15:
                        self.dailyStreak=14
                    self.lastDaily=now
                    self.save_to_database()
                    return True
                else:
                    diff_days = diff.days
                    rounded_diff_days = round(diff.days)
                    if streakProtectionStar >0 and streakProtectionStar >= rounded_diff_days:
                        self.tokensBalance+=(role['BaseDaily']+(role['StreakBonus']*self.dailyStreak))
                        self.dailyStreak+=1
                        if self.dailyStreak >= 15:
                            self.dailyStreak=14
                        self.lastDaily=now
                        self.streakProtectionStar-=rounded_diff_days
                        self.save_to_database()
                        return True
                    else:
                        self.tokensBalance+=(role['BaseDaily'])
                        self.dailyStreak=1
                        self.lastDaily=now
                        self.save_to_database()
                        return True
            else:
                return False
    
    def getUserPersonas(self):
        conn = sqlite3.connect(DB)
        
        
        userPersonas={}
        allPersonas=getPersonas()
        c = conn.cursor()
        c.execute("SELECT PersonaID FROM unlockedPersona WHERE UserID=?", (self.ID,))
        unlocked_personas = c.fetchall()
        RelativeID=0
        for x in allPersonas.keys():
            if allPersonas[x]['Rarity'] == 'Free':
                userPersonas[RelativeID] ={
                    'PersonaID': x,
                    'Name': allPersonas[x]['Name'],
                    'Description':allPersonas[x]['Description'],
                    'Introduction': allPersonas[x]['Introduction'],
                    'Prompt':allPersonas[x]['Prompt'],
                    'Rarity': allPersonas[x]['Rarity'],
                    'Collection': allPersonas[x]['Collection'],
                    'Cost': allPersonas[x]['Cost']
                }
                RelativeID+=1
        else:
            if unlocked_personas != []:
                for x in unlocked_personas:
                    userPersonas[RelativeID] ={
                        'PersonaID': x[0],
                        'Name': allPersonas[x[0]]['Name'],
                        'Description':allPersonas[x[0]]['Description'],
                        'Introduction': allPersonas[x[0]]['Introduction'],
                        'Prompt':allPersonas[x[0]]['Prompt'],
                        'Rarity': allPersonas[x[0]]['Rarity'],
                        'Collection': allPersonas[x[0]]['Collection'],
                        'Cost': allPersonas[x[0]]['Cost']
                    }
                    RelativeID+=1
        return userPersonas
    
    def unlockPersona(self, personaID):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        
        c.execute("SELECT PersonaID FROM unlockedPersona WHERE UserID=?", (self.ID,))
        unlockedPersonas = c.fetchall()
        if unlockedPersonas != []:
            for x in unlockedPersonas:
                currPersona = Persona(x[0])
                if currPersona.ID == personaID:
                    if currPersona.Rarity == 'Premium':
                        self.premiumPersonaShard+=5
                        self.save_to_database()
                        return
                    elif currPersona.Rarity == 'Common':
                        self.commonPersonaShard+=5
                        self.save_to_database()
                        return
            else:

                c.execute('''
                        INSERT INTO unlockedPersona (UserID, PersonaID)
                        VALUES (?,?)
                        ''', (self.ID, personaID))
        else:
            c.execute('''
                    INSERT INTO unlockedPersona (UserID, PersonaID)
                    VALUES (?,?)
                    ''', (self.ID, personaID))

        conn.commit()
        conn.close()
        return
    def getListOfUnlockedPersona(self):
        outputList=[]
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT PersonaID FROM unlockedPersona WHERE UserID=?", (self.ID,))
        unlockedPersonas = c.fetchall()
        if unlockedPersonas != []:
            for x in unlockedPersonas:
                currPersona=Persona(unlockedPersonas[x[0]])
                outputList.append(currPersona)
        
        return outputList
        
        
        


class Persona:
    def __init__(self, ID=None, Name=None, Description=None, Introduction=None, Prompt=None, Rarity=None, Collection=None, Cost=None, CollectionID=None, Thumbnail=None):
        self.ID = ID
        self.Name = Name
        self.Description = Description
        self.Introduction = Introduction
        self.Prompt = Prompt
        self.Rarity = Rarity
        self.Collection = Collection
        self.Cost = Cost
        self.CollectionID = CollectionID
        self.Thumbnail = Thumbnail        

        if (Name is None) and (Description is None) and (Introduction is None) and (Prompt is None) and (Rarity is None) and (Collection is None) and (ID is not None) and (Cost is None) and (CollectionID is None) and (Thumbnail is None):


            self.load_from_database()
        
    def load_from_database(self):
        conn = sqlite3.connect(DB)
        cursor = conn.execute('''SELECT * FROM persona WHERE ID=?''', (self.ID,))
        row = cursor.fetchone()
        if row is not None:
            self.Name = row[1]
            self.Description = row[2]
            self.Introduction = row[3]
            self.Prompt = row[4]
            self.Rarity = row[5]
            self.Collection = row[6]
            self.Cost = row[7]
            self.CollectionID = row[8]
            self.Thumbnail = row[9]
            
        conn.close()

    def save_to_database(self):
        conn = sqlite3.connect(DB)
        conn.execute('''

            UPDATE persona SET ID=?, Name=?, Description=?, Introduction=?, Prompt=?, Rarity=?, Collection=?, Cost=?, CollectionID=?, Thumbnail=? WHERE ID=?

        ''', (self.Name,self.Description,self.Introduction,self.Prompt,self.Rarity,self.Collection,self.Cost, self.CollectionID, self.Thumbnail,self.ID))
        conn.commit()
        conn.close()

class collection:
    def __init__(self, ID=None, Name=None, Creator=None, Description=None):
        self.ID = ID
        self.Name = Name
        self.Creator = Creator
        self.Description = Description
        self.Personas = []
        
        if (Name is None) and (Creator is None) and (Description is None):
            self.load_from_database()
            self.Personas = self.loadPersonasFromCollection()
    
    def load_from_database(self):
        conn = sqlite3.connect(DB)
        row = conn.execute("SELECT * FROM collection WHERE ID=?",(self.ID,)).fetchone()
        
        if row is not None:
            self.Name = row[1]
            self.Creator = row[2]
            self.Description = row[3]
            self.Personas = self.loadPersonasFromCollection()

        conn.close()
    
    def loadPersonasFromCollection(self):
        conn = sqlite3.connect(DB)
        row = conn.execute("SELECT ID FROM persona WHERE CollectionID=?",(self.ID,)).fetchall()
        output = []
        if row is not None:

            for x in row:
                persona=Persona(x[0])
                output.append(persona)
        conn.close()
        
        return output

    
def getCollection():
    conn = sqlite3.connect(DB)

    cursor = conn.execute("SELECT ID FROM collection")

    listOfCollections = []
    rows = cursor.fetchall()

    if rows is not None:

        for row in rows:
            listOfCollections.append(collection(row[0]))
    
    conn.close()
    
    return listOfCollections    

def getPersonas():
    conn = sqlite3.connect(DB)
    
    cursor = conn.execute(
        '''
        SELECT ID, Name, Description, Introduction, Prompt, Rarity, Collection, Cost, Thumbnail
        FROM persona
        '''
    )
    results = cursor.fetchall()
    personas_dict = {}
    for result in results:
        personas_dict[result[0]] ={
            'Name': result[1],
            'Description': result[2],
            'Introduction': result[3],
            'Prompt': result[4],
            'Rarity': result[5],
            'Collection': result[6],
            'Cost': result[7],
            'Thumbnail': result[8]
        }
    return personas_dict

def registerMessage(ID, UserID, Persona, Input, Output, Type):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    date = datetime.now().isoformat()
    c.execute("INSERT INTO message (ID, Date, UserID, Persona, Input, Output, Type) VALUES (?, ?, ?, ?, ?, ?, ?)", 
              (ID, date, UserID, Persona, Input, Output, Type))
    conn.commit()
    conn.close()

# def registerTransaction(MsgID, FromUserID, ToUserID, Amount):
#     conn = sqlite3.connect(DB)
#     c = conn.cursor()
#     date = datetime.now().isoformat()
#     c.execute("INSERT INTO transaction (ID, FromUserID, ToUserID, Amount, Date) VALUES (?, ?, ?, ?, ?)", (MsgID, FromUserID, ToUserID, Amount, date))
#     conn.commit()
#     conn.close()
    

def GetAKey():
    with open('keyToUse.txt', 'r+') as f:
        keyToUse= int(f.read().strip("þÿ\x00"))
        keys=(OriChanRun.loadData())['APIKeys']
        
        toWrite= keyToUse+1
        if toWrite==len(keys):
            toWrite=0
        f.truncate(0)
        with open('keyToUse.txt', 'w') as z:
            z.write(str(toWrite))
        
        return keys[keyToUse]

def assign_random_numbers(key_list: list[str], numbers_per_key: list[int]) -> dict[str, list[int]]:
    number_list = []
    result = {}

    for i in range(sum(numbers_per_key)):
        number_list.append(i+1)

    random.shuffle(number_list)

    for key, n in zip(key_list, numbers_per_key):
        result[key] = number_list[:n]
        number_list = number_list[n:]

    return result

def user_exists(ID):
    conn = sqlite3.connect(DB)
    cursor = conn.execute('''SELECT * FROM users WHERE ID=?''', (ID,))
    row = cursor.fetchone()
    conn.close()
    return row is not None


def searchPersonas(string):
    if type(string) != str:
        raise ValueError("Input must be a string")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    output_list = []
    c.execute("SELECT ID FROM persona WHERE Name LIKE ?", ('%'+string+'%',))
    results = c.fetchall()
    conn.close()
    if len(results) != 0:
        for result in results:
            persona_to_add = Persona(result[0])
            output_list.append(persona_to_add)
    return output_list

def getMessage(messageID):
    conn = sqlite3.connect(DB)
    cursor = conn.execute("SELECT Input, Output, Persona, UserID FROM message WHERE ID = ?", (messageID,))
    c = cursor.fetchone()
    if c != None:
        return c
    else:
        return None