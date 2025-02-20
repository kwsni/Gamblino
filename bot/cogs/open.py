import discord, logging
from discord.ext import commands
from discord import app_commands
from util.loot import Loot

log = logging.getLogger(__name__)

class Open(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    open = app_commands.Group(name='open', description='Open loot from CS2')
    
    @open.command(name='case', 
                description='Open a case from CS2'
    )
    async def case(self, interaction: discord.Interaction, case_name: str) -> None:
        log.info(f'Opening case for {interaction.user.name} id:{interaction.user.id}')
        loot = await Loot().rollCase(case_name)
        img = discord.Embed()
        img.set_image(url=loot.img)
        stattrak_str = lambda : 'StatTrak™ ' if loot.stattrak else ''
        color = ''
        stattrak_color = '\u001b[0;33m'
        match(loot.rarity):
            # Use ansi formatting to use color text in Discord
            case 'Rare':
                color = '\u001b[0;31m]'
            case 'Covert':
                color = '\u001b[0;31m'
            case 'Classified':
                color = '\u001b[0;35m'
            case 'Restricted':
                color = '\u001b[0;35;47m'
                stattrak_color = '\u001b[0;33;47m'
            case 'Mil-Spec Grade':
                color = '\u001b[0;34m'
        log.info(f'Opened {loot} from {case_name}')
        await interaction.response.send_message(
                    f'{interaction.user.mention}\n'
                    f'You have opened from {case_name}:\n'
                    f'```ansi\n'
                    f'{color}{loot.wear}{stattrak_color} {stattrak_str()}{color}{loot.name}\n'
                    f'```',
                    embed=img)
        
    @case.autocomplete('case_name')
    async def case_autocomplete(
            self,
            interaction: discord.Interaction,
            current: str,
    ) -> list[app_commands.Choice[str]]:
        case_names = ['CS:GO Weapon Case', 'eSports 2013 Case', 'Operation Bravo Case', 'CS:GO Weapon Case 2',
                      'eSports 2013 Winter Case', 'Winter Offensive Weapon Case', 'CS:GO Weapon Case 3',
                      'Operation Phoenix Weapon Case', 'Huntsman Weapon Case', 'Operation Breakout Weapon Case',
                      'eSports 2014 Summer Case', 'Operation Vanguard Weapon Case', 'Chroma Case',
                      'Chroma 2 Case', 'Falchion Case', 'Shadow Case', 'Revolver Case', 'Operation Wildfire Case',
                      'Chroma 3 Case', 'Gamma Case', 'Gamma 2 Case', 'Glove Case', 'Spectrum Case',
                      'Operation Hydra Case', 'Spectrum 2 Case''Clutch Case', 'Horizon Case',
                      'Danger Zone Case', 'Prisma Case', 'Shattered Web Case', 'CS20 Case',
                      'Prisma 2 Case','Fracture Case', 'Operation Broken Fang Case','Snakebite Case',
                      'Operation Riptide Case', 'Dreams & Nightmares Case', 'Recoil Case', 'Revolution Case',
                      'Kilowatt Case']
        return [app_commands.Choice(name=case_name, value=case_name)
                for case_name in case_names if current.lower() in case_name.lower()]