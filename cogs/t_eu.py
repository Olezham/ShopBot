import discord
from discord.ext import commands
from discord.ui import Button, View

import asyncio
import config


class TicketEuView(discord.ui.View):
        def __init__(self, bot):
            super().__init__(timeout=None)
            self.bot = bot
            
        @discord.ui.button(label="Close the ticket 🔐", style=discord.ButtonStyle.red, custom_id='close_ticket_eu') 
        async def accept_callback(self, interaction: discord.Interaction,button):
            guild = interaction.guild
            ls = []
            for i in config.ticket_close_role:
                ls.append(guild.get_role(i))

            if any(role in interaction.user.roles for role in ls):
                await interaction.response.send_message(f"**This channel will be automaticly delete in 30 seconds ** ", delete_after=30)
                await asyncio.sleep(30)
                await interaction.channel.delete()

            if guild.get_role(1181541370851237920) in interaction.user.roles:
                await interaction.response.send_message(f"**This channel will be automaticly delete in 30 seconds ** ", delete_after=30)
                await asyncio.sleep(30)
                await interaction.channel.delete()

class TicketEuStartView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        
    @discord.ui.button(label="Create Order 📨", style=discord.ButtonStyle.green, custom_id='create_ticket_eu') 
    async def accept_callback(self, interaction: discord.Interaction,button):
        guild = interaction.guild
        role = guild.get_role(config.ticket_role)
        dio = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True),
            role: discord.PermissionOverwrite(view_channel=True)
        }

        

        v = TicketEuView(self.bot)

        category = interaction.guild.get_channel(config.ticket_category_id)

        channel = await interaction.guild.create_text_channel(name=f"{interaction.user.name}-ticket", overwrites=dio, category=category)

        ticketcreate = discord.Embed(title="🆘 Your ticket 🆘", description=f"Ask a question about your purchase in the ticket. You will receive a reply shortly")

        await channel.send(embed=ticketcreate, view=v)
        await channel.send(content=f"<@&1181541370851237920> Your request will be shortlly processed.")
        await interaction.response.send_message(f"**Your ticket has been created -->** {channel.mention}", ephemeral=True, delete_after=30)


class TicketEuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='t_eu')
    @commands.has_permissions(administrator=True)
    async def t_eu(self,ctx):
        await ctx.message.delete()

     

        v = TicketEuStartView(self.bot)

        embed = discord.Embed(title="Welcome! 👋", description="Here you can manage your inquiries and requests.\n\nTo start addressing your issues, please click the 'Create Order' button below.")
        embed.set_thumbnail(url="https://i.imgur.com/VWQqPTu.png")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1244920070518345768/1246818118097965247/order.png?ex=665dc55c&is=665c73dc&hm=59cf4a9f5f361f7219e1147aabcebd56ef027b3ebc3b4b3ede5e2865eb0d8cbc&")
        await ctx.send(embed=embed, view=v)

        
 
async def setup(bot):
    bot.add_view(TicketEuView(bot))
    bot.add_view(TicketEuStartView(bot))
    await bot.add_cog(TicketEuCog(bot))