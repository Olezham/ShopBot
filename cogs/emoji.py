from discord.ext import commands
import discord
from . import config  # Подразумевается, что у вас есть модуль config с вашими настройками

class Reactions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.ID_POST:
            channel = self.client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = message.guild.get_member(payload.user_id)
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

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = self.client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = message.guild.get_member(payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = discord.utils.get(message.guild.roles, id=config.ROLES_LIST[emoji])
            await user.remove_roles(role)
        except Exception as _ex:
            print(repr(_ex))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_reactions(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass
        # Получаем объект сообщения по его идентификатору
        channel = self.client.get_channel(config.CHANNEL_FOR_ROLES_ID)  # Канал, в котором находится сообщение
        message_id = 1238128242695602236  # Идентификатор сообщения
        message = await channel.fetch_message(message_id)

        # Ставим реакции под сообщением
        await message.add_reaction('🇷🇺')
        await message.add_reaction('🇪🇺')

def setup(client):
    client.add_cog(Reactions(client))
