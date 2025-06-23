import os
from dotenv import load_dotenv
import asyncio
import discord
from discord.ext import commands
import logging
import logging.handlers
from datetime import datetime


class MyBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.logger = logging.getLogger(f'discord.{self.__class__.__name__}')
    
    async def on_ready(self):
        MESSAGE = f"""
        === Bot 啟動成功 ===
        Bot 名稱: {self.user}
        Bot ID: {self.user.id}
        伺服器數量: {len(self.guilds)}
        ===================
        """
        MESSAGE = '\n'.join(i.strip() for i in MESSAGE.strip().split('\n'))
        self.logger.info(MESSAGE)
    
    async def setup_hook(self) -> None:
        cogs_to_load = ["cogs.Reader"]

        for cog in cogs_to_load:
            try:
                await self.load_extension(cog)
                self.logger.info(f'succeed to load {cog}')
            except Exception as e:
                self.logger.info(f'failed to load {cog} - {e}')


def setup_logging():
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')

    # 控制台處理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 檔案處理器
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file_name = f'discord_bot_{timestamp}.log'
    file_handler = logging.FileHandler(
        filename=os.path.join(log_dir, log_file_name),
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    


async def active(env_path: str='./.env', token_name: str='DISCORD_BOT_TOKEN'):
    setup_logging()
    load_dotenv(env_path)
    DISCORD_API_KEY = os.environ.get(token_name)
    if DISCORD_API_KEY is None:
        logging.critical("Cannot Get discord token, please check your .env file")
        return

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    bot = MyBot(command_prefix='p?', intents=intents)

    await bot.start(DISCORD_API_KEY)


if __name__ == '__main__':
    asyncio.run(active())
