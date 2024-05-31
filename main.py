import discord
from discord.ext import commands
from discord.ui import Button, View

import config as config

import asyncio
import os

intents = discord.Intents().all()
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print('Updating...')
    await update(None) # функция для обновления системы тикетов и фидбэка
    await add_reactions(None)
    print("Update successfully")
    print("Bot online")


@client.command()
@commands.has_permissions(administrator=True)
async def t_ru(ctx):

    await ctx.message.delete()

    button = Button(label="Создать заказ 📨", style=discord.ButtonStyle.green)

    button.callback = ticketfunction_ru
    v = View(timeout=None).add_item(button)

    embed = discord.Embed(title="Добро пожаловать в канал тикетов ✉️", description="Если у вас есть вопросы или пожелания, пожалуйста, нажмите на кнопку \"Создать заказ\".")

    embed.set_thumbnail(url="https://i.imgur.com/u3BG2eV.png") 

    await ctx.send(embed=embed, view=v)


async def ticketfunction_ru(interaction: discord.Interaction):
    guild = interaction.guild
    role = guild.get_role(config.ticket_role)
    dio = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True),
        role: discord.PermissionOverwrite(view_channel=True)
    }
    
    closebtn = Button(label="Закрыть тикет 🔐", style=discord.ButtonStyle.red)
    closebtn.callback = close_ticket
   
    v = View(timeout=None).add_item(closebtn)
   
    category = interaction.guild.get_channel(config.ticket_category_id)
    
    channel = await interaction.guild.create_text_channel(name=f"{interaction.user.name}-ticket", overwrites=dio, category=category)

    ticketcreate = discord.Embed(title="🆘 Ваш тикет 🆘", description=f"Задайте вопрос по покупке в тикете. В скором времени вам ответят")

    await channel.send(embed=ticketcreate, view=v)

    await interaction.response.send_message(f"**Ваш тикет создан -->** {channel.mention}", ephemeral=True, delete_after=30)

@client.command()
@commands.has_permissions(administrator=True)
async def t_eu(ctx):
    await ctx.message.delete()
    button = Button(label="Create Order 📨", style=discord.ButtonStyle.green)
    button.callback = ticketfunction_eu
    v = View(timeout=None).add_item(button)
    embed = discord.Embed(title="Welcome to the ticket channel. ✉️", description="If you have any questions or requests, please click on the \"Create Order\" button!")
    embed.set_thumbnail(url="https://i.imgur.com/u3BG2eV.png") 
    await ctx.send(embed=embed, view=v)

async def ticketfunction_eu(interaction: discord.Interaction):
    guild = interaction.guild
    role = guild.get_role(config.ticket_role)
    dio = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True),
        role: discord.PermissionOverwrite(view_channel=True)
    }
    closebtn = Button(label="Close the ticket 🔐", style=discord.ButtonStyle.red)
    closebtn.callback = close_ticket
    v = View(timeout=None).add_item(closebtn)
    category = interaction.guild.get_channel(config.ticket_category_id)
    channel = await interaction.guild.create_text_channel(name=f"{interaction.user.name}-ticket", overwrites=dio, category=category)
    ticketcreate = discord.Embed(title="🆘 Your ticket 🆘", description=f"Ask a question about your purchase in the ticket. You will receive a reply shortly")
    await channel.send(embed=ticketcreate, view=v)
    await interaction.response.send_message(f"**Your ticket has been created -->** {channel.mention}", ephemeral=True, delete_after=30)
    # conn.cursor().execute("INSERT INTO ticket (openticket) VALUES (?)", [interaction.user.id])
    # conn.commit() 


async def close_ticket(interaction: discord.Interaction):
     
    guild = interaction.guild
    ls = []
    for i in config.ticket_close_role:
        ls.append(guild.get_role(i))

    if any(role in interaction.user.roles for role in ls):
        await interaction.response.send_message(f"**Этот канал автоматически удалится через 30 секунд ** ", ephemeral=True, delete_after=30)
        await asyncio.sleep(30)
        await interaction.channel.delete()

    if guild.get_role(1181541370851237920) in interaction.user.roles:
        await interaction.response.send_message(f"**Этот канал автоматически удалится через 30 секунд ** ", ephemeral=True, delete_after=30)
        await asyncio.sleep(30)
        await interaction.channel.delete()



class Feedback(discord.ui.Modal, title='Feedback'):
    
    name = discord.ui.TextInput(
        label='Оценка работы от 1 до 5 ⭐️',
        placeholder='1-5',
        max_length=1
    )
    
    feedback = discord.ui.TextInput(
        label='Напишите отзыв',
        style=discord.TextStyle.long,
        placeholder='Обязательно оставьте свой комментарий',
        required=False,
        max_length=300,
    )

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
        channel = client.get_channel(config.feedback_chanel_id)
        await channel.send(embed=embed)
        await interaction.response.send_message(f'Спасибо за отзыв', ephemeral=True, delete_after = 30)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is

@client.command()
@commands.has_permissions(administrator=True)
async def feedback_ru(ctx):
    await ctx.message.delete()
    button = Button(label="Оставить отзыв 💌", style=discord.ButtonStyle.primary)
    button.callback = modal_callback
    v = View(timeout=None).add_item(button)
    embed = discord.Embed(title="Отзывы", description="Хотите оценить работу или дизайнера? Оставьте отзыв 💌")
    embed.set_thumbnail(url="https://i.imgur.com/u3BG2eV.png") 
    await ctx.send(embed=embed, view=v)

async def modal_callback(interaction: discord.Interaction):
    await interaction.response.send_modal(Feedback())



class Feedback_eu(discord.ui.Modal, title='Feedback'):
    
    name = discord.ui.TextInput(
        label='Performance evaluation from 1 to 5 ⭐️',
        placeholder='1-5',
        max_length=1
    )
    
    feedback = discord.ui.TextInput(
        label='Write a review',
        style=discord.TextStyle.long,
        placeholder='Be sure to leave a comment',
        required=False,
        max_length=300,
    )

    async def on_submit(self,interaction: discord.Interaction):
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
        channel = client.get_channel(config.feedback_chanel_id)
        await channel.send(embed=embed)
        await interaction.response.send_message(f'Thanks for your feedback', ephemeral=True, delete_after = 30)

    async def on_error(interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
@client.command()
@commands.has_permissions(administrator=True)
async def feedback_eu(ctx):
    await ctx.message.delete()
    button = Button(label="Leave feedback 💌", style=discord.ButtonStyle.primary)
    button.callback = modal_callback_eu
    v = View(timeout=None).add_item(button)
    embed = discord.Embed(title="Feedback", description="Want to rate a job or designer? Leave a review 💌")
    embed.set_thumbnail(url="https://i.imgur.com/u3BG2eV.png")
    await ctx.send(embed=embed, view=v)

async def modal_callback_eu(interaction: discord.Interaction):
    await interaction.response.send_modal(Feedback_eu())

@client.command()
@commands.has_permissions(administrator=True)
async def update(ctx):
    try:
        ctx.message.delete()
    except:
        pass
    target_channels = [1233849532413116446,1233550117035053096,1233674956941037639,1233674737054646322,1190696739620012072] # ID of the target channel
    command_channel = {1233849532413116446:'t_ru',
                       1233550117035053096:'t_eu',
                       1233674956941037639:'feedback_eu',
                       1233674737054646322:'feedback_ru',
                       1190696739620012072:'embed'
                       }
    for i in target_channels:
        target_channel = client.get_channel(i)
        await target_channel.purge()
        message = await target_channel.send('Upd-ating ...', delete_after = 10)
        context = await client.get_context(message)
        await context.invoke(client.get_command(command_channel[i]))
    print('Successfully updated')


@client.event
async def on_raw_reaction_add(payload):
        if payload.message_id == config.ID_POST:
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = discord.utils.get(message.guild.members, id=payload.user_id)
            emoji = str(payload.emoji)

            if user.bot:
                return

            try:
                role = discord.utils.get(message.guild.roles, id=config.ROLES_LIST[emoji])

                if len([i for i in user.roles if i.id not in config.USER_ROLES_LIST]) <= config.MAX_ROLES:
                    await user.add_roles(role)
                else:
                    await message.remove_reaction(payload.emoji, user)

            except Exception as _ex:
                print(repr(_ex))

@client.event
async def on_raw_reaction_remove(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = discord.utils.get(message.guild.members, id=payload.user_id)

    try:
        emoji = str(payload.emoji)
        role = discord.utils.get(message.guild.roles, id=config.ROLES_LIST[emoji])
        await user.remove_roles(role)
    except Exception as _ex:
        print(repr(_ex))

@client.command()
@commands.has_permissions(administrator=True)
async def add_reactions(ctx):
    try:
        ctx.message.delete()
    except:
        pass
    # Получаем объект сообщения по его идентификатору
    channel = client.get_channel(config.CHANNEL_FOR_ROLES_ID) # Канал, в котором находится сообщение
    message_id = 1238128242695602236  # Идентификатор сообщения
    message = await channel.fetch_message(message_id)

    # Ставим реакции под сообщением
    
    await message.add_reaction('🇷🇺')
    await message.add_reaction('🇪🇺')

@client.command()
@commands.has_permissions(administrator=True)
async def embed(ctx):
    
    await ctx.message.delete()
    button = Button(label="Отправить Embed 📯 ", style=discord.ButtonStyle.green)
    button.callback = modal_embed_callback
    button1 = Button(label="Подобрать цвет", style=discord.ButtonStyle.secondary, url='https://www.spycolor.com/')

    v = View(timeout=None).add_item(button)
    v.add_item(button1)
    
    embed = discord.Embed(title="Отправка Embed📡", description=" ## Нажмите на кнопку для отправки Ембеда в новости", color=discord.Color.random())

    await ctx.send(embed=embed, view=v)

async def modal_embed_callback(interaction: discord.Interaction):
    await interaction.response.send_modal(EmbedModal())

class EmbedModal(discord.ui.Modal, title='Embed'):
    
    titile = discord.ui.TextInput(
        label='Заголовок',
        placeholder='...',
        required=False
    )
    
    color = discord.ui.TextInput(
        label='Цвет',
        placeholder='rgb(<number>, <number>, <number>)',
        required=False
    )

    image_url = discord.ui.TextInput(
        label='Url картинки',
        placeholder='https://imgur.com/a/3do0u8t',
        required=False
    )

    main_text = discord.ui.TextInput(
        label='Основной текст',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here...',
        max_length=4000
    )

    async def on_submit(self, interaction: discord.Interaction):
        
        if self.color.value != '':
            embed_color = discord.Color.from_str(self.color.value)
        else:
            embed_color = discord.Color.random()
            
        embed = discord.Embed(title= self.titile.value, description=self.main_text, color=embed_color)
        
        if self.image_url.value is not None:
            embed.set_image(url=self.image_url.value)
        embed.set_thumbnail(url="https://i.imgur.com/u3BG2eV.png")
        channel = client.get_channel(1183367937957048440)
        
        await channel.send(content='@everyone', embed=embed)
        await interaction.response.send_message('Embed Успешно создан',ephemeral=True, delete_after = 30,)



client.run(config.TOKEN)