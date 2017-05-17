import discord
from discord.ext import commands
import secrets

prefix = ["?", "//"]

initial_extensions = ['cogs.general',
                      'cogs.fun',
                      'cogs.mod',
                      ]

# https://bot.discord.io/reinbow

description = """Reinbow Bot written by TeaSeaPea."""

bot = commands.Bot(command_prefix=prefix, description=description, pm_help=True)

hello_msg = ":fire: :100: Thanks for adding me do ?help for info! :100: :fire:"

def get_welcome_channel(server):
    return server.default_channel

def get_server_name(server):
    return server.name

@bot.event
async def on_ready():
    print("-------------------------------------------")
    print("Logged in as: " + bot.user.name)
    print("Client ID: " + bot.user.id)
    print("---------------------------------------------\nBot by TeaSeaPea (mzk)\n---------------------------------------------")
    await bot.change_presence(game=discord.Game(name='?help'))

@bot.event
async def on_server_join(server):
    default = server.default_channel
    await bot.send_message(default, hello_msg)

@bot.event
async def on_member_join(member):
    svr = get_server_name(member.server)
    default = get_welcome_channel(member.server)
    joinmessage = "{}\nWelcome to **{}**".format(member.mention, svr)
    await bot.send_message(default, joinmessage)


for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as n:
        print("Failed to load extension {}\n{}: {}".format(extension, type(n).__name__, n))


bot.run(secrets.BOT_TOKEN)







