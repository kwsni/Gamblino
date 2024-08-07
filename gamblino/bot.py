"""
Gamblino Discord Bot

Counter-Strike 2 crate opening simulator as a Discord Bot

"""

import asyncio, logging, logging.handlers, discord
from os import getenv
from dotenv import load_dotenv
from discord.ext import commands
from gamblino.cogs.open import Open

load_dotenv()

root_log = logging.getLogger()
root_log.setLevel(logging.INFO)

log = logging.getLogger('gamblino-bot')

rotating_handler = logging.handlers.RotatingFileHandler(
	filename='gamblino.log', 
	mode='a', 
	encoding='utf-8', 
	maxBytes=10 * 1024 * 1024, 
	backupCount=5)

dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')

rotating_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(discord.utils._ColourFormatter())

root_log.addHandler(rotating_handler)
root_log.addHandler(stream_handler)

class GamblinoBot(commands.Bot):
	def __init__(self) -> None:
		intents = discord.Intents.default()
		super().__init__(command_prefix='!', intents=intents)

	async def on_ready(self) -> None:
		try:
			sync = await super().tree.sync()
			log.info(f"Successfully synced {len(sync)} commands")
		except Exception as e:
			log.error(e)

bot = GamblinoBot()

async def main() -> None:
	await bot.add_cog(Open(bot))

if __name__ == '__main__':
	asyncio.run(main())

token = str(getenv('DISCORD_TOKEN'))
bot.run(token, log_handler=None)