import discord
from discord.ext import commands, tasks
import logging
import pyautogui

import asyncio

logger = logging.getLogger(__name__)


class Reader(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.target_id = 913017451904663553
        self.adv_script_loop.start()
    
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
                    ping_message = '@315764312700485632 機器人即將關閉'
                    await message.channel.send(ping_message)
                    await self.bot.close()
                    return
                
                if embed.title and any((i in embed.title) for i in {'冒險', '探索'}):
                    logger.info("偵測到戰鬥訊息，執行治療檢查...")
                    await asyncio.to_thread(self._execute_healing, embed)
    
    def cog_unload(self):
        # 5. 當 Cog 被卸載時 (例如重載指令)，優雅地取消背景任務
        self.adv_script_loop.cancel()

    def _execute_healing(self, embed: discord.Embed):
        try:
            description = embed.description
            if not description or "HP" not in description:
                return
            idx = description.index("HP")
            hp, max_hp = map(lambda x: int(x.strip('`')), description[idx+3:-1].split('/'))
            unit = max_hp // 5
            heal_mul = (max_hp - hp) // unit
            if heal_mul > 0:
                logger.info(f"執行治療腳本: >heal 1 {heal_mul}")
                pyautogui.write(f'>heal 1 {heal_mul}', interval=0.1)
                pyautogui.press('enter')
        except (ValueError, IndexError, TypeError) as e:
            logger.error(f"執行 pyautogui 腳本時出錯: {e}", exc_info=True)

    @tasks.loop(seconds=32)
    async def adv_script_loop(self):
        try:
            logger.info("固定任務：執行 >adv 指令。")
            pyautogui.write('>adv', interval=0.1)
            pyautogui.press('enter')
        except Exception as e:
            logger.error(f'執行 >adv 指令時出錯: {e}', exc_info=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Reader(bot))
