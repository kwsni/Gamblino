"""
Gamblino Discord Bot

CS:GO/CS2 crate opening simulator as a Discord Bot

"""

import logging, logging.handlers, discord
from os import getenv
from dotenv import load_dotenv
from discord.ext import commands
from loot import Loot

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
	def __init__(self):
		intents = discord.Intents.default()
		super().__init__(command_prefix='!', intents=intents)

	async def on_ready(self):
		try:
			sync = await super().tree.sync()
			log.info(f"Successfully synced {len(sync)} commands")
		except Exception as e:
			log.error(e)

bot = GamblinoBot()

@bot.tree.command(name="open", description="Open a random crate from Counter-Strike 2")
async def open(interaction: discord.Interaction):
	log.info(f"Opening crate for {interaction.user.name} id:{interaction.user.id}")
	loot = await Loot().uncrate()
	img = discord.Embed()
	img.set_image(url=loot.img)
	stattrak_str = lambda : "StatTrak™ " if loot.stattrak else ""
	color = ""
	stattrak_color = "\u001b[0;33m"
	match(loot.rarity):
		# Use ansi formatting to use color text in Discord
		case "Rare":
			color = "\u001b[0;31m]"
		case "Covert":
			color = "\u001b[0;31m"
		case "Classified":
			color = "\u001b[0;35m"
		case "Restricted":
			color = "\u001b[0;35;47m"
			stattrak_color = "\u001b[0;33;47m"
		case "Mil-Spec Grade":
			color = "\u001b[0;34m"
	log.info(f"Opened {loot} from {loot.crate_name}")
	await interaction.response.send_message(
				f"{interaction.user.mention}\n"
				f"You have opened from {loot.crate_name}:\n"
				f"```ansi\n"
				f"{color}{loot.wear}{stattrak_color} {stattrak_str()}{color}{loot.name}\n"
				f"```",
				embed=img)

token = str(getenv("DISCORD_TOKEN"))
bot.run(token, log_handler=None)