import discord, asyncio, ObjectClasses
from Cogs.OriChanMain import user_exists
from discord.ext import commands
from discord import app_commands
class HelpDropdown(discord.ui.Select):
    def __init__(self, category_pages):
        self.category_pages = category_pages
        options = [
            discord.SelectOption(label=category, description=page['description'])
            for category, page in category_pages.items()
        ]
        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.category_pages[self.values[0]]['embed'], view=HelpView(self.category_pages))

class HelpView(discord.ui.View):
    def __init__(self, category_pages):
        super().__init__(timeout=180)
        self.add_item(HelpDropdown(category_pages))

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category_pages = {} # Will be populated in on_ready

    def create_help_embed(self, title, description, command_list=None):
        embed = discord.Embed(title=title, description=description, color=0x5C0E80)
        embed.set_footer(text="Ori-chan & Friends.", icon_url="https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1054984334878191636/1061806291091210320/image.png")
        if command_list:
            for name, command_info in command_list.items():
                embed.add_field(name=name, value=command_info, inline=False)
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[+]: {self.bot.user.name} Help Cog is ready.")
        self.populate_help_categories()

    def populate_help_categories(self):
        # --- General Category ---
        general_commands = {
            "/help": "Shows this help menu.",
            "/balance": "Shows your balance and other information.",
            "ori!daily (ori!d)": "Claim your daily OriCoin reward.",
            "ori!baltop (ori!leaderboard, ori!bt)": "Shows the top 10 OriCoin leaderboard.",
            "ori!donate": "Information on how to donate and support Ori-chan.",
            "ori!give (ori!transfer, ori!t, ori!g) <@user> <amount>": "Transfer OriCoins to another user.",
        }
        general_embed = self.create_help_embed("General Commands", "These are general commands for Ori-chan usage.", general_commands)

        # --- Persona Category ---
        persona_commands = {
            "ori!persona (ori!search) <persona name>": "Search for a persona by name.",
            "/changepersona [Persona Name]": "Change your active persona. Name is optional to browse.",
            "ori!personaInventory (ori!pi, ori!pinv)": "View your unlocked persona inventory.",
            "ori!startthread (ori!st, ori!St) [persona number]": "Start a private or public thread with a persona. Number is optional.",
        }
        persona_embed = self.create_help_embed("Persona Commands", "Commands related to interacting with and managing personas.", persona_commands)

        # --- Gacha Category ---
        gacha_commands = {
            "ori!showCollection (ori!sc, ori!collection, ori!collections, ori!c)": "View available persona collections.",
            "ori!openBox (ori!openbox, ori!pb, ori!personabox, ori!op)": "Open a Persona Box to get rewards and personas.",
            "ori!unlockShards (ori!shard, ori!Shard)": "Use persona shards to unlock random personas of a chosen rarity.",
            "ori!toggleCL (ori!clu, ori!unlockcl, ori!char)": "Toggle character limit unlock card usage for unlimited characters per message (if you have cards).",
        }
        gacha_embed = self.create_help_embed("Gacha Commands", "Commands for the persona gacha system.", gacha_commands)

        # --- Developer Category (Owner Only) ---
        developer_commands = {
            "ori!reExt (ori!re)": "Reloads bot extensions (cogs).",
            "ori!giveAdmin <@user> <amount>": "Gives OriCoins to a user (admin command).",
            "ori!infoAdmin <@user>": "Shows detailed user information (admin command).",
            "ori!changeRole <@user> <role>": "Changes a user's role (admin command). Roles: freeRole, standardDonator, bundleDonator1, bundleDonator2, bundleDonator3, betaTester, developer.",
            "ori!challenge": "Starts a challenge event (admin command).",
        }
        developer_embed = self.create_help_embed("Developer Commands (Owner Only)", "Commands for bot developers and owner.", developer_commands)


        self.category_pages = {
            "General": {'embed': general_embed, 'description': "General bot commands."},
            "Persona": {'embed': persona_embed, 'description': "Persona interaction commands."},
            "Gacha": {'embed': gacha_embed, 'description': "Persona gacha and collection commands."},
            "Developer (Owner Only)": {'embed': developer_embed, 'description': "Developer and bot owner commands (owner only)."}
        }


    @app_commands.command(name="help", description="Shows the help menu.")
    async def help(self, interaction: discord.Interaction):
        if not user_exists(interaction.user.id):
            userToGive=ObjectClasses.User(interaction.user.id,25000,"freeRole",0)
            userToGive.save_to_database()
        is_owner = await self.bot.is_owner(interaction.user)
        if not is_owner:
            # Remove Developer category for non-owners
            if "Developer (Owner Only)" in self.category_pages:
                del self.category_pages["Developer (Owner Only)"]
        else:
             # Ensure Developer category is present for owners (in case it was removed before)
            if "Developer (Owner Only)" not in self.category_pages:
                self.populate_help_categories() # Repopulate to include developer commands
        initial_category = "General" # Default category to show first
        view = HelpView(self.category_pages)
        HelpInteraction = await interaction.response.send_message(embed=self.category_pages[initial_category]['embed'], view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))