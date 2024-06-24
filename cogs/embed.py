import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput

class EmbedView(discord.ui.View):
        def __init__(self, bot):
            super().__init__(timeout=None)
            self.bot = bot
            self.add_item(Button(label="Подобрать цвет", style=discord.ButtonStyle.link, url='https://www.spycolor.com/'))
            
        @discord.ui.button(label="Отправить Embed 📯", style=discord.ButtonStyle.green, custom_id='Send_Modal') 
        async def accept_callback(self, interaction: discord.Interaction,button):
            await interaction.response.send_modal(EmbedModal(self.bot))


class EmbedModal(discord.ui.Modal, title='Embed'):
    
    titile = discord.ui.TextInput(
        label='Заголовок',
        placeholder='Введите заголовок...',
        required=False
    )

    image_url = discord.ui.TextInput(
        label='URL картинки',
        placeholder='https://imgur.com/a/3do0u8t',
        required=False
    )

    main_text = discord.ui.TextInput(
        label='Основной текст',
        style=discord.TextStyle.long,
        placeholder='Введите ваш текст здесь...',
        max_length=4000
    )

    channel_id = discord.ui.TextInput(
        label='ID канала',
        placeholder='Введите ID канала',
        required=True
    )

    outside_text = discord.ui.TextInput(
        label='Внешний текст',
        placeholder='Введите текст, который будет отображаться вне Embed',
        required=False,
        max_length=2000
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        # Фиксированный цвет Embed
        embed_color = discord.Color(int('4426c6', 16))
        
        # Проверка ID канала
        try:
            channel_id = int(self.channel_id.value)
            channel = self.bot.get_channel(channel_id)
            if not channel:
                await interaction.response.send_message('Ошибка: Канал не найден. Пожалуйста, проверьте ID канала.', ephemeral=True, delete_after=30)
                return
        except ValueError:
            await interaction.response.send_message('Ошибка: Неверный формат ID канала. Пожалуйста, введите числовое значение.', ephemeral=True, delete_after=30)
            return

        # Создание и отправка Embed
        embed = discord.Embed(title= self.titile.value, description=self.main_text.value, color=embed_color)
        if self.image_url.value:
            embed.set_image(url=self.image_url.value)
        embed.set_thumbnail(url="https://i.imgur.com/VWQqPTu.png")
        
        message_content = self.outside_text.value if self.outside_text.value else None
        await channel.send(content=message_content, embed=embed)
        
        await interaction.response.send_message('Embed успешно создан', ephemeral=True, delete_after=10)

class EmbedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='embed')
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx):
        await ctx.message.delete()
        
        

        v = EmbedView(self.bot)
        
        
        embed = discord.Embed(
            title="Отправка Embed📡",
            description="## Нажмите на кнопку для отправки Ембеда в новости",
            color=discord.Color.random()
        )

        await ctx.send(embed=embed, view=v)


async def setup(bot):
    bot.add_view(EmbedView(bot))
    await bot.add_cog(EmbedCog(bot))
