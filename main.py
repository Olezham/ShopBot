import discord
from discord.ext import commands
from discord.ui import Button, View

import config as config

import asyncio
# try:
#     conn = sqlite3.connect("ticket.db")
#     conn.cursor().execute("CREATE TABLE IF NOT EXISTS ticket (openticket INT)")
#     conn.commit()
# except:
#     pass

intents = discord.Intents().all()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print('Updating...')
    await update(None)
    print("Bot online")

@client.command()
@commands.has_permissions(administrator=True)
async def t_ru(ctx):
    await ctx.message.delete()
    button = Button(label="Создать тикет в тех.поддержку 📨", style=discord.ButtonStyle.green)
    button.callback = ticketfunction_ru
    v = View(timeout=None).add_item(button)
    embed = discord.Embed(title="✉️ Тех.Поддержка ✉️", description="## По вопросам покупки/уточнения вопросов создайте тикет ")
    embed.set_thumbnail(url="https://cdn-icons-png.freepik.com/512/785/785530.png?ga=GA1.1.1544554669.1711359609") 
    await ctx.send(embed=embed, view=v)

async def ticketfunction_ru(interaction: discord.Interaction):
    guild = interaction.guild
    role = guild.get_role(config.ticket_role)
    dio = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True),
        role: discord.PermissionOverwrite(view_channel=True)
    }
    # if isOpen(interaction.user.id):
    #     await interaction.response.send_message("Вы уже открыли билет, подождите 24 часа", ephemeral=True)
    # else:
    closebtn = Button(label="Закрыть тикет 🔐", style=discord.ButtonStyle.red)
    closebtn.callback = close_ticket
    v = View(timeout=None).add_item(closebtn)
    category = interaction.guild.get_channel(config.ticket_category_id)
    channel = await interaction.guild.create_text_channel(name=f"{interaction.user.name}-ticket", overwrites=dio, category=category)
    ticketcreate = discord.Embed(title="🆘 Ваш тикет 🆘", description=f"Задайте вопрос по покупке или тех.части. В скором времени мы вам ответим")
    await channel.send(embed=ticketcreate, view=v)
    await interaction.response.send_message(f"**Ваш тикет создан -->** {channel.mention}", ephemeral=True, delete_after=30)
    #conn.cursor().execute("INSERT INTO ticket (openticket) VALUES (?)", [interaction.user.id])
    #conn.commit() 

@client.command()
@commands.has_permissions(administrator=True)
async def t_eu(ctx):
    await ctx.message.delete()
    button = Button(label="Create a ticket to tech support 📨", style=discord.ButtonStyle.green)
    button.callback = ticketfunction_eu
    v = View(timeout=None).add_item(button)
    embed = discord.Embed(title="✉️ Tech Support ✉️", description="## For purchase/clarification questions, create a ticket")
    embed.set_thumbnail(url='https://cdn-icons-png.freepik.com/512/785/785530.png?ga=GA1.1.1544554669.1711359609') # НЕ ЗАБЫТЬ ПОСТАВИТЬ ИКОНКУ
    await ctx.send(embed=embed, view=v)

async def ticketfunction_eu(interaction: discord.Interaction):
    guild = interaction.guild
    role = guild.get_role(config.ticket_role)
    dio = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True),
        role: discord.PermissionOverwrite(view_channel=True)
    }
    # if isOpen(interaction.user.id):
    #     await interaction.response.send_message("Вы уже открыли билет, подождите 24 часа", ephemeral=True)
    #else:
    closebtn = Button(label="Close the ticket 🔐", style=discord.ButtonStyle.red)
    closebtn.callback = close_ticket
    v = View(timeout=None).add_item(closebtn)
    category = interaction.guild.get_channel(config.ticket_category_id)
    channel = await interaction.guild.create_text_channel(name=f"{interaction.user.name}-ticket", overwrites=dio, category=category)
    ticketcreate = discord.Embed(title="🆘 Your ticket 🆘", description=f"Ask us a question about your purchase or maintenance. We will get back to you shortly")
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
        await interaction.response.send_message(f"**This channel will close automatic in 30 seconds ** ", ephemeral=True, delete_after=30)
        await asyncio.sleep(30)
        await interaction.channel.delete()
    if guild.get_role(1181541370851237920) in interaction.user.roles:
        await interaction.response.send_message(f"**This channel will close automatic in 30 seconds ** ", ephemeral=True, delete_after=30)
        await asyncio.sleep(30)
        await interaction.channel.delete()
    # if config.ticket_role in interaction.user.roles:
    #     await interaction.channel.delete()
    #     print('Роль продавца')
        
        
# async def reset_db():
#     for a, in conn.cursor().execute("SELECT openticket FROM ticket").fetchall():
#         try:
#             conn.cursor().execute("DELETE FROM ticket WHERE openticket = ?", [a])
#             conn.commit()
#         except:
#             pass

# def isOpen(user_id: int):
#     result = conn.cursor().execute("SELECT openticket FROM ticket WHERE openticket = ?", [user_id])
#     if len(result.fetchall()) > 0:
#         return True
#     else:
#         return False



class Feedback(discord.ui.Modal, title='Feedback'):
    
    name = discord.ui.TextInput(
        label='Оценка 1-5⭐️',
        placeholder='1-5',
        max_length=1
    )
    
    feedback = discord.ui.TextInput(
        label='Напишите отзыв',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here...',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Спасибо за отзыв', ephemeral=True, delete_after = 30)
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
    embed = discord.Embed(title="Отзывы", description="Хотите оценить роботу магазина или продовца? Оставте отзыв💌")
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4658/4658943.png")
    await ctx.send(embed=embed, view=v)

async def modal_callback(interaction: discord.Interaction):
    await interaction.response.send_modal(Feedback())



class Feedback_eu(discord.ui.Modal, title='Feedback'):
    
    name = discord.ui.TextInput(
        label='Rating 1-5⭐️',
        placeholder='1-5',
        max_length=1
    )
    
    feedback = discord.ui.TextInput(
        label='Write a review',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here...',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback', ephemeral=True, delete_after = 30)
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
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
@client.command()
@commands.has_permissions(administrator=True)
async def feedback_eu(ctx):
    await ctx.message.delete()
    button = Button(label="Leave feedback 💌", style=discord.ButtonStyle.primary)
    button.callback = modal_callback_eu
    v = View(timeout=None).add_item(button)
    embed = discord.Embed(title="Feedback", description="Do you want to evaluate the work of a store or seller? Leave a review💌")
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4658/4658943.png")
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
    target_channels = [1233849532413116446,1233550117035053096,1233674956941037639,1233674737054646322] # ID of the target channel
    command_channel = {1233849532413116446:'t_ru',
                       1233550117035053096:'t_eu',
                       1233674956941037639:'feedback_eu',
                       1233674737054646322:'feedback_ru'
                       }
    for i in target_channels:
        target_channel = client.get_channel(i)
        await target_channel.purge()
        message = await target_channel.send('Updating ...', delete_after = 10)
        context = await client.get_context(message)
        await context.invoke(client.get_command(command_channel[i]))
    print('Successfully updated')


client.run(config.TOKEN)


