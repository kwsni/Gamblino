"""
Gamblino Discord Bot

CS:GO/CS2 crate opening simulator as a Discord Bot

"""

import os
from dotenv import load_dotenv
from logging import handlers
from requests_cache import install_cache
import discord
from discord.ext import commands
from loot import Loot

load_dotenv()
install_cache(expire_after=540, allowable_methods=('GET'), stale_if_error=True)

token = str(os.getenv("DISCORD_TOKEN"))
handler = handlers.RotatingFileHandler(filename='gamblino.txt', mode='a', encoding='utf-8')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
	try:
		sync = await bot.tree.sync()
		print(f"Successfully synced {len(sync)} commands")
	except Exception as e:
		print(e)

@bot.tree.command(name="open", description="Open a CS2 crate, random if not specified")
async def open(interaction: discord.Interaction):
	loot = Loot().uncrate()
	img = discord.Embed()
	img.set_image(url=loot.img)
	stattrak_str = lambda : "StatTrak™ " if loot.stattrak else ""
	match(loot.rarity):
		# Use ansi formatting to use color text in Discord
		case "Rare":
			await interaction.response.send_message(
				f"{interaction.user.mention}\n"
				f"You have opened:\n"
				f"```ansi\n"
				f"\u001b[0;31m{loot.wear} \u001b[0;33m{stattrak_str()}\u001b[0;31m{loot.name}\n"
				f"```",
				embed=img)
		case "Covert":
			await interaction.response.send_message(
				f"{interaction.user.mention}\n"
				f"You have opened:\n"
				f"```ansi\n"
				f"\u001b[0;31m{loot.wear} \u001b[0;33m{stattrak_str()}\u001b[0;31m{loot.name}\n"
				f"```",
				embed=img)
		case "Classified":
			await interaction.response.send_message(
				f"{interaction.user.mention}\n"
				f"You have opened:\n"
				f"```ansi\n"
				f"\u001b[0;35m{loot.wear} \u001b[0;33m{stattrak_str()}\u001b[0;35m{loot.name}\n"
				f"```",
				embed=img)
		case "Restricted":
			await interaction.response.send_message(
				f"{interaction.user.mention}\n"
				f"You have opened:\n"
				f"```ansi\n"
				f"\u001b[0;35;47m{loot.wear}\u001b[0;35;47m \u001b[0;33;47m{stattrak_str()}\u001b[0;35;47m{loot.name}\n"
				f"```",
				embed=img)
		case "Mil-Spec Grade":
			await interaction.response.send_message(
				f"{interaction.user.mention}\n"
				f"You have opened:\n"
				f"```ansi\n"
				f"\u001b[0;34m{loot.wear} \u001b[0;33m{stattrak_str()}\u001b[0;34m{loot.name}\n"
				f"```",
				embed=img)

bot.run(token, log_handler=handler)