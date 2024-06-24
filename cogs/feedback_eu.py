import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import config

class FeedbackEuView(discord.ui.View):
        def __init__(self, bot):
            super().__init__(timeout=None)
            self.bot = bot
            
        @discord.ui.button(label="Leave feedback 💌", style=discord.ButtonStyle.primary, custom_id='Leave_feedback_eu') 
        async def accept_callback(self, interaction: discord.Interaction,button):
            await interaction.response.send_modal(FeedbackEu(self.bot))

class FeedbackEuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='feedback_eu')
    @commands.has_permissions(administrator=True)
    async def feedback_eu(self, ctx):
        await ctx.message.delete()
        
       
        v = FeedbackEuView(self.bot)

        embed = discord.Embed(
            title="Reviews — Your Evaluation of Our Work!", 
            description="We greatly value your opinion and strive to continuously improve the quality of our services.\n\nIf you want to evaluate the work of a designer, your feedback will be extremely useful both for us and for our potential clients."
        )

        embed.set_thumbnail(url="https://i.imgur.com/VWQqPTu.png")

        embed.set_image(url="https://cdn.discordapp.com/attachments/1244920070518345768/1246818864407384104/feedback.png?ex=665dc60e&is=665c748e&hm=7fdb3303c0d85de5a84ffa5ad052d0175aad36403d88e82904de0daeababad81&")

        await ctx.send(embed=embed, view=v)


class FeedbackEu(Modal, title='Feedback'):
    name = TextInput(
        label='Performance evaluation from 1 to 5 ⭐️',
        placeholder='1-5',
        max_length=1
    )
    
    feedback = TextInput(
        label='Write a review',
        style=discord.TextStyle.long,
        placeholder='Be sure to leave a comment',
        required=False,
        max_length=300,
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        embed_color = discord.Color.green()
        try:
            number = int(self.name.value)
            if number > 5:
                number = 5
            if number == 3:
                embed_color = discord.Color.yellow()
            if number < 3:
                embed_color = discord.Color.red()
        except:
            number = 5

        embed = discord.Embed(
            title=f'Feedback from {interaction.user.name}',
            color=embed_color
        )
        stars = "⭐️" * number
        embed.add_field(name='Rating', value=f"{stars}", inline=False)
        embed.add_field(name='Review', value=f"{self.feedback.value}", inline=False)
        
        channel = self.bot.get_channel(config.feedback_chanel_id)
        await channel.send(embed=embed)
        await interaction.response.send_message(f'Thanks for your feedback', ephemeral=True, delete_after=10)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        print(f'Error: {str(error)}')

async def setup(bot):
    bot.add_view(FeedbackEuView(bot))
    await bot.add_cog(FeedbackEuCog(bot))
