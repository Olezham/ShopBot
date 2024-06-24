import discord
from discord.ext import commands

class UpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='update')
    @commands.has_permissions(administrator=True)
    async def update(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass

        target_channels = [1233849532413116446, 1233550117035053096, 1233674956941037639, 1233674737054646322, 1190696739620012072]
        command_channel = {
            1233849532413116446: 't_ru',
            1233550117035053096: 't_eu',
            1233674956941037639: 'feedback_eu',
            1233674737054646322: 'feedback_ru',
            1190696739620012072: 'embed'
        }

        for channel_id in target_channels:
            target_channel = self.bot.get_channel(channel_id)
            if target_channel is None:
                print(f"Канал с ID {channel_id} не найден.")
                continue
            
            await target_channel.purge()
            message = await target_channel.send('Updating...', delete_after=10)
            context = await self.bot.get_context(message)
            
            command_name = command_channel.get(channel_id)
            if command_name:
                command = self.bot.get_command(command_name)
                if command:
                    await context.invoke(command)
                else:
                    print(f"Команда {command_name} не найдена.")
            else:
                print(f"Команда для канала с ID {channel_id} не назначена.")

            if channel_id == 1190696739620012072:
                # Специальный случай для вызова команды 'article'
                article_command = self.bot.get_command('article')
                if article_command:
                    await context.invoke(article_command)
                else:
                    print("Команда 'article' не найдена.")

        print('Successfully updated')

async def setup(bot):
    await bot.add_cog(UpdateCog(bot))
