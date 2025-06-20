import os
from dotenv import load_dotenv
import asyncio
import discord
from discord.ext import commands


class MyBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
    
    async def on_ready(self):
        MESSAGE = f"""
        === Bot 啟動成功 ===
        Bot 名稱: {self.user}
        Bot ID: {self.user.id}
        伺服器數量: {len(self.guilds)}
        ===================
        """
        MESSAGE = '\n'.join(i.strip() for i in MESSAGE.strip().split('\n'))
        print(MESSAGE)
    
    async def setup_hook(self) -> None:
        cogs_to_load = []

        for cog in cogs_to_load:
            try:
                await self.load_extension(cog)
                print(f'succeed to load {cog}')
            except Exception as e:
                print(f'failed to load {cog} - {e}')


async def active(env_path: str='./.env', token_name: str='DISCORD_BOT_TOKEN'):
    load_dotenv(env_path)
    DISCORD_API_KEY = os.environ.get(token_name)
    if DISCORD_API_KEY is None:
        raise ValueError("Cannot get the KEY")

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    bot = MyBot(command_prefix='p?', intents=intents)

    await bot.start(DISCORD_API_KEY)


if __name__ == '__main__':
    asyncio.run(active())
