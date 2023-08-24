"""
Gamblino Discord Bot

CSGO crate opening simulator as a Discord Bot

"""

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from loot import Loot

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# invoke command by sending "${command} in DMs or channels where the bot has permission to view"
@bot.command()
async def open(ctx):
	loot = Loot().uncrate()
	stattrak_str = lambda : "StatTrak™ " if loot.stattrak else ""
	await ctx.send(loot.img)
	match(loot.rarity):
		# Use ansi formatting to use color text in Discord
		case "Rare":
			await ctx.send(
				f"You have opened:\n"
				f"```ansi\n"
				f"\u001b[0;31m{loot.wear} \u001b[0;33m{stattrak_str()}\u001b[0;31m{loot.name}\n"
				f"```")
		case "Covert":
			await ctx.send(
				f"You have opened:\n"
				f"```ansi\n"
				f"\u001b[0;31m{loot.wear} \u001b[0;33m{stattrak_str()}\u001b[0;31m{loot.name}\n"
				f"```")
		case "Classified":
			await ctx.send(
				f"You have opened:\n"
				f"```ansi\n"
				f"\u001b[0;35m{loot.wear} \u001b[0;33m{stattrak_str()}\u001b[0;35m{loot.name}\n"
				f"```")
		case "Restricted":
			await ctx.send(
				f"You have opened:\n"
				f"```ansi\n"
				f"\u001b[0;35;47m{loot.wear}\u001b[0;35;47m \u001b[0;33;47m{stattrak_str()}\u001b[0;35;47m{loot.name}\n"
				f"```")
		case "Mil-Spec Grade":
			await ctx.send(
				f"You have opened:\n"
				f"```ansi\n"
				f"\u001b[0;34m{loot.wear} \u001b[0;33m{stattrak_str()}\u001b[0;34m{loot.name}\n"
				f"```")

bot.run(os.getenv("DISCORD_TOKEN"))