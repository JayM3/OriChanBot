import discord
from discord.ext import commands
from discord import app_commands
import ObjectClasses

class PersonaButtonView(discord.ui.View):
    def __init__(self, personas, cog, interaction):
        super().__init__(timeout=60)
        self.cog = cog
        self.personas = personas
        self.current_index = 0
        self.interaction_origin = interaction
        self.message = None
        
        # Add the buttons immediately
        self.update_buttons()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.interaction_origin.user:
            return True
        else:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return False

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)

    def update_buttons(self):
        # Clear existing buttons
        for item in self.children:
            self.remove_item(item)
            
        # Add new buttons
        back_button = discord.ui.Button(label="Back", style=discord.ButtonStyle.secondary, custom_id="back", disabled=(self.current_index == 0))
        back_button.callback = self.back_button_callback
        self.add_item(back_button)
        
        select_button = discord.ui.Button(label="Select", style=discord.ButtonStyle.primary, custom_id="select")
        select_button.callback = self.select_button_callback
        self.add_item(select_button)
        
        next_button = discord.ui.Button(label="Next", style=discord.ButtonStyle.secondary, custom_id="next", disabled=(self.current_index == len(self.personas) - 1))
        next_button.callback = self.next_button_callback
        self.add_item(next_button)

    def get_current_embed(self):
        persona_info = self.personas[self.current_index]
        return self.cog.create_persona_embed(persona_info)

    async def back_button_callback(self, interaction: discord.Interaction):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.get_current_embed(), view=self)

    async def select_button_callback(self, interaction: discord.Interaction):
        selected_persona = self.personas[self.current_index]
        user = ObjectClasses.User(interaction.user.id)
        user.Persona = selected_persona['PersonaID']
        user.save_to_database()
        await interaction.response.send_message(f"Persona changed to: `{selected_persona['Name']}`", ephemeral=True)
        self.stop()

    async def next_button_callback(self, interaction: discord.Interaction):
        if self.current_index < len(self.personas) - 1:
            self.current_index += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.get_current_embed(), view=self)


class OriChanCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_persona_embed(self, persona_info):
        embed = discord.Embed(title=f"Persona: {persona_info['Name']}", description=persona_info['Description'], color=0x5C0E80)
        embed.add_field(name="Collection", value=persona_info['Collection'], inline=False)
        embed.add_field(name="Introduction", value=persona_info['Introduction'], inline=False)
        embed.set_footer(text="Ori-chan & Friends.", icon_url="https://media.discordapp.net/attachments/1054984334878191636/1058809695130890326/image.png")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1054984334878191636/1061806291091210320/image.png")
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[+]: {self.bot.user.name} Commands Cog is ready.")

    @app_commands.command(name="changepersona", description="Change your active persona.")
    @app_commands.describe(persona_name="Optional: Specify persona name to change to")
    async def change_persona_command(self, interaction: discord.Interaction, persona_name: str = None):
        await interaction.response.defer(ephemeral=True)

        user = ObjectClasses.User(interaction.user.id)
        user_personas = user.getUserPersonas()

        if not user_personas:
            await interaction.followup.send("You don't have any personas in your inventory yet!", ephemeral=True)
            return

        if persona_name:
            found_personas = []
            for persona_data in user_personas.values():
                if persona_name.lower() in persona_data['Name'].lower():
                    found_personas.append(persona_data)

            if not found_personas:
                await interaction.followup.send("No persona found with that name in your inventory.", ephemeral=True)
                return
            elif len(found_personas) == 1:
                selected_persona = found_personas[0]
                user.Persona = selected_persona['PersonaID']
                user.save_to_database()
                await interaction.followup.send(f"Persona changed to: `{selected_persona['Name']}`", ephemeral=True)
                return
            else:
                # Multiple personas - show menu to choose
                view = PersonaButtonView(found_personas, self, interaction)
                message = await interaction.followup.send(
                    "Multiple personas found with that name. Please choose one:", 
                    embed=view.get_current_embed(), 
                    view=view, 
                    ephemeral=True
                )
                view.message = message
        else:
            # No persona name provided - show menu of all personas
            persona_list = list(user_personas.values())
            view = PersonaButtonView(persona_list, self, interaction)
            message = await interaction.followup.send(
                "Choose a persona:", 
                embed=view.get_current_embed(), 
                view=view, 
                ephemeral=True
            )
            view.message = message


async def setup(bot):
    await bot.add_cog(OriChanCommandsCog(bot))