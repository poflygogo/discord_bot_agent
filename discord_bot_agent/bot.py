import os
from dotenv import load_dotenv
import discord


def run(env_path: str='./.env', token_name: str='DISCORD_BOT_TOKEN'):
    load_dotenv(env_path)
    DISCORD_API_KEY = os.environ.get(token_name)
    if DISCORD_API_KEY is None:
        raise ValueError("Cannot get the KEY")

    intents = discord.Intents.default()
    bot = discord.Client(intents=intents)

    bot.run(DISCORD_API_KEY)


if __name__ == '__main__':
    run()