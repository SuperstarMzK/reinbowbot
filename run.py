import discord
from discord.ext import commands
import secrets

prefix = ["?", "//"]

initial_extensions = ['cogs.general',
                      'cogs.fun',
                      'cogs.mod'
                      ]

# https://bot.discord.io/reinbow

description = """Reinbow Bot written by TeaSeaPea."""

bot = commands.Bot(command_prefix=prefix, description=description, pm_help=True)

hello_msg = ":fire: :100: Thanks for adding me do ?help for info! :100: :fire:"

def get_welcome_channel(guild):
    return guild.system_channel

def get_guild_name(guild):
    return guild.name

@bot.event
async def on_ready():
    print("-------------------------------------------")
    print("Logged in as: " + bot.user.name)
    print("Client ID: " + str(bot.user.id))
    print("---------------------------------------------\nBot by TeaSeaPea (mzk)\n---------------------------------------------")
    game = discord.Game("?help")
    await bot.change_presence(activity=game)

@bot.event
async def on_guild_join(guild):
    default = get_welcome_channel(guild)
    await default.send(hello_msg)

@bot.event
async def on_member_join(member):
    svr = get_guild_name(member.guild)
    default = get_welcome_channel(member.guild)
    joinmessage = "{}\nWelcome to **{}**".format(member.mention, svr)
    await default.send(joinmessage)


for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as n:
        print("Failed to load extension {}\n{}: {}".format(extension, type(n).__name__, n))


bot.run(secrets.BOT_TOKEN)







