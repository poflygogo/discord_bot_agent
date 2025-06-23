import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)


class Reader(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.target_id = 913017451904663553
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id != self.target_id:
            return
        if message.content:
            logger.info(f"message content: {message.content}")
        if message.embeds:
            for i, embed in enumerate(message.embeds):
                logger.info(f'---Embed #{i+1} ---')
                if embed.title:
                    logger.info(f'title: {embed.title}')
                if embed.description:
                    logger.info(f'description: {embed.description}')
                if embed.footer and embed.footer.text:
                    logger.info(f'footer: {embed.footer.text}')
                logger.info("-" * (20 + len(str(i+1))))

                if embed.title and "累惹" in embed.title:
                    logger.warning('shut down: 低體力')
                    await self.bot.close()
                    return


async def setup(bot: commands.Bot):
    await bot.add_cog(Reader(bot))
