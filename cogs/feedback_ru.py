import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import config


class FeedbackRuView(discord.ui.View):
        def __init__(self, bot):
            super().__init__(timeout=None)
            self.bot = bot
            
        @discord.ui.button(label="Оставить отзыв 💌", style=discord.ButtonStyle.primary,custom_id='leave_feedback_ru') 
        async def accept_callback(self, interaction: discord.Interaction,button):
            await interaction.response.send_modal(Feedback(self.bot))

class FeedbackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='feedback_ru')
    @commands.has_permissions(administrator=True)
    async def feedback_ru(self, ctx):
        await ctx.message.delete()
        
        v = FeedbackRuView(self.bot)

        embed = discord.Embed(
            title="Отзывы — Ваша оценка нашей работы!", 
            description="Мы придаем большое значение вашему мнению и стремимся постоянно улучшать качество наших услуг.\n\nЕсли вы хотите оценить работу дизайнера, ваш отзыв будет крайне полезен как для нас, так и для наших потенциальных клиентов."
        )
        embed.set_thumbnail(url="https://i.imgur.com/VWQqPTu.png") 
        embed.set_image(url="https://cdn.discordapp.com/attachments/1244920070518345768/1246818864407384104/feedback.png?ex=665dc60e&is=665c748e&hm=7fdb3303c0d85de5a84ffa5ad052d0175aad36403d88e82904de0daeababad81&")
        await ctx.send(embed=embed, view=v)


class Feedback(Modal, title='Feedback'):
    name = TextInput(
        label='Оценка работы от 1 до 5 ⭐️',
        placeholder='1-5',
        max_length=1
    )
    
    feedback = TextInput(
        label='Напишите отзыв',
        style=discord.TextStyle.long,
        placeholder='Обязательно оставьте свой комментарий',
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
            title=f'Отзыв от пользователя {interaction.user.name}',
            color=embed_color
        )
        stars = "⭐️" * number
        embed.add_field(name='Оценка', value=f"{stars}", inline=False)
        embed.add_field(name='Отзыв', value=f"{self.feedback.value}", inline=False)
        
        channel = self.bot.get_channel(config.feedback_chanel_id)
        await channel.send(embed=embed)
        await interaction.response.send_message(f'Спасибо за отзыв', ephemeral=True, delete_after=10)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        print(f'Error: {str(error)} ')

async def setup(bot):
    bot.add_view(FeedbackRuView(bot))
    await bot.add_cog(FeedbackCog(bot))
