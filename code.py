##NOTE: NEV THIS IS A BURNING MESS AND I'VE BEEN WORKING ON IT FOR HALF AN HOUR
#lol idk how this is gonna go

import logging, discord, datetime, json, sys, analyticord
from discord.ext import commands
import conf
from colorama import init, Fore, Back, Style



print("""Initialising Colorama...

""")
init()
print(Style.BRIGHT + Back.BLUE + Fore.RED + 'Color' + Fore.GREEN + 'ama' + Style.RESET_ALL + ' initialised!')
token = conf.token
actoken = conf.actoken
print("Tokens loaded")
analytics = analyticord.AnalytiCord(actoken)



#DEBUG = i want to hear the sound of the air moving as a pin drops
#INFO = i want to hear a pin drop
#WARNING = i want to know if something goes wrong
#CRITICAL = do not warn me unless something is on fire


loglevel = logging.DEBUG

bot = commands.Bot(command_prefix='!', description='hi', pm_help=True)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
# set a formatter or something here
logger.addHandler(stdout_handler)

@bot.event
async def on_ready():
    bot.start_time = datetime.datetime.now()
    print('Bot started at ', Style.BRIGHT, Fore.YELLOW, bot.start_time, Style.RESET_ALL)
    print("Logged in as {} with ID {}".format(bot.user.name+'#'+bot.user.discriminator, bot.user.id))
    users = sum(1 for user in bot.get_all_members())
    channels = sum(1 for channel in bot.get_all_channels())
    print("Serving {} users in {} channels on {} guilds".format(users, channels, len(bot.servers)))
    game = discord.Game(name='dear god')
    await analytics.start()
    await bot.change_presence(status=discord.Status.idle, game=game)


@bot.command(pass_context=True)
async def source(ctx):
    await bot.reply("it worked")

@bot.event
async def on_server_join(guild):

    print(Style.BRIGHT, Fore.CYAN+ 'GUILD_CREATE: {0.name} <{0.id}>'.format(guild) + Style.RESET_ALL)
    guilds = len(bot.servers)
    print("I am now in "+guilds+' server(s).')
    await analytics.send('guildJoin', guilds)

@bot.event
async def on_server_remove(guild):

    print(Style.BRIGHT, Fore.RED + 'GUILD_REMOVE: {0.name} (id {0.id})'.format(guild) + Style.RESET_ALL)
    guildsLeft = len(bot.servers)
    await analytics.send('guildJoin', guildsLeft)

@bot.command(pass_context=True)
async def analyticord(ctx):
    Embed = discord.Embed(title="AnalytiCord: An analytics platform for Discord bots, by Nevexo & Nightmare. https://AnalytiCord.solutions", color=0x197CE0, url='https://AnalytiCord.solutions'),
    Embed.set_image(url="https://cdn.discordapp.com/attachments/347438752571981855/347438802232410112/Analyticord_Discord_Blurple.svg")
    await bot.say(embed=Embed)



@bot.command(pass_context=True)
async def shutdown(ctx):
    await bot.reply("I'm shutting down now.")
    game = discord.Game(name='Shutting down...')
    await bot.change_presence(status=discord.Status.dnd)
    print(Back.RED, Style.BRIGHT, "Bot shutting down by request of [this should say author]")
    await analytics.send('disconnect', 'true')
    await bot.logout()



bot.run(token)
