import discord
from discord.ext import commands, tasks
from discord.ui import Button, View, Modal, TextInput
import requests
from database import mysql


class ArticleEuView(discord.ui.View):
        def __init__(self, bot):
            self.bot = bot
            super().__init__(timeout=None)
            
        @discord.ui.button(label="Add article 🔥", style=discord.ButtonStyle.primary,custom_id='Add_article_eu')  # the button has a custom_id set
        async def accept_callback(self, interaction: discord.Interaction,button):
            await interaction.response.send_modal(ArticleEuModal(self.bot))

class ArticleEuModal(Modal, title='Article'):
    
    titile = TextInput(
        label='Title',
        placeholder='...',
        required=True
    )

    main_text = TextInput(
        label='About article',
        style=discord.TextStyle.long,
        placeholder='Cool photoshop',
        max_length=4000
    )

    price = TextInput(
        label='Price in USD',
        placeholder='50',
        required=True
    )

    image_url = TextInput(
        label='Url from picture',
        placeholder='https://imgur.com/a/3do0u8t',
        required=True
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        try:
            mysql.add_article_eu(self.titile.value, self.price.value, self.main_text.value, self.image_url.value)
            await interaction.response.send_message('Article is seccsesfully!', ephemeral=True, delete_after=30)
            await ArticleEuCog.auto_update_price(self)  # Убедитесь, что эта функция определена и доступна

        except Exception as ex:
            await interaction.response.send_message('Возникла ошибка при добавлении товара', ephemeral=True, delete_after=30)
            print(str(ex))

class ArticleEuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def get_rub_rate(self):
        responce = requests.get('https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_y2o97LrUbTP0ewqKidgYYXJa7pODNPou2O04pERa&currencies=RUB').json()

        return responce['data']['RUB']
    
    @commands.Cog.listener()
    async def on_ready(self):
        # Функция будет запускаться при старте бота
        self.auto_update_price.start()
        await self.auto_update_price()

    @tasks.loop(hours=24)  
    async def auto_update_price(self):
        channel_id = 1254013847942070314  
        channel = self.bot.get_channel(channel_id)
        if not channel:
            print("Канал для обновления цен не найден.")
            return

        data = mysql.get_all_articles_eu()  # Получение всех товаров из базы данных
        
        # Очистка сообщений в канале
        await channel.purge()
        
        for item in data:
            embed = discord.Embed(title=item['title'], description=item['about'], color=discord.Color.purple())
            price_usd = int(item['price'])
            
            embed.add_field(name='Цена', value=f'{price_usd} USD' , inline=False)
            
            embed.set_image(url=item['picture'])
            
            await channel.send(embed=embed)

    @commands.command(name='article_eu')
    @commands.has_permissions(administrator=True)
    async def article_eu(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass
        
        
        v = ArticleEuView(self.bot)
        
        
        embed = discord.Embed(
            title="Add an Article 🏵",
            description="## Press the button to add new Article in list",
            color=discord.Color.random()
        )

        await ctx.send(embed=embed, view=v)
        
    

async def setup(bot):
    bot.add_view(ArticleEuView(bot))
    await bot.add_cog(ArticleEuCog(bot))
