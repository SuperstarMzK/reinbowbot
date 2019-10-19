import discord
from discord.ext import commands
import random
import time


class General(commands.Cog):
    """General commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="join", pass_context=True)
    async def _join(self, ctx):
        """Join Official Bot Discord"""
        author = ctx.message.author
        print(author)
        await ctx.send("{} Join **#DoorSquad** at https://discord.io/doorsquad".format(author.mention))


    @commands.command(name="contact", aliases=["cnt"], pass_context=True)
    async def contact(self, ctx, *, message : str):
        """Sends a message to the bot developer (owner)"""
        owner = self.bot.get_user(277844990695178240)
        guild = ctx.message.guild
        author = ctx.message.author
        footer = "User ID: " + str(author.id) + " | Guild ID: " + str(guild.id)
        source = "From {}".format(guild)

        colour = discord.Colour.green()

        description = "Sent by {} {}".format(author, source)

        msg = discord.Embed(colour=colour, description=message)
        msg.set_author(name=description)
        msg.set_footer(text=footer)

        await owner.send(embed=msg)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong."""
        t1 = time.perf_counter()
        await discord.abc.Messageable.trigger_typing(ctx.message.channel)
        t2 = time.perf_counter()
        thedata = (":ping_pong: **Pong.**\nTime: " + str(round((t2 - t1) * 1000)) + "ms")
        color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
        color = int(color, 16)
        data = discord.Embed(description=thedata, colour=discord.Colour(value=color))

        await ctx.send(embed=data)

    @commands.command(name="userinfo", aliases=["whois"], pass_context=True, no_pm=True)
    async def _userinfo(self, ctx, *, user: discord.Member = None):
        """Shows information about a user"""
        author = ctx.message.author
        guild = ctx.message.guild
        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]
        joined_at = user.joined_at
        since_created = (ctx.message.created_at - user.created_at).days
        since_joined = (ctx.message.created_at - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        member_number = sorted(guild.members,
                               key=lambda m: m.joined_at).index(user) + 1

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)
        activities = "Chilling in {} status".format(user.status)

        print(user.activities)

        if user.activities is None:
            pass
        try:
            activities = "Streaming: [{}]({})".format(user.activities[0], user.activities[1])
        except IndexError:
            activities = "Playing {}".format(user.activities[0])


        if roles:
            roles = sorted(roles, key=[x.name for x in guild.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = discord.Embed(description=activities, colour=user.colour)
        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="Roles", value=roles, inline=False)
        data.set_footer(text="Member #{} | User ID:{}"
                             "".format(member_number, user.id))

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.avatar_url:
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=name)

        await ctx.send(embed=data)

    @commands.command(name="serverinfo", pass_context=True, no_pm=True)
    async def _serverinfo(self, ctx):
        """Shows information about the server"""
        guild = ctx.message.guild
        online = len([m.status for m in guild.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(guild.members)
        text_channels = len([x for x in guild.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(guild.channels) - text_channels
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                      "".format(guild.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        colour = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        data = discord.Embed(
            description=created_at,
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(guild.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(guild.roles))
        data.add_field(name="Owner", value=str(guild.owner))
        data.set_footer(text="Guild ID: " + str(guild.id))

        if guild.icon_url:
            data.set_author(name=guild.name, url=guild.icon_url)
            data.set_thumbnail(url=guild.icon_url)
        else:
            data.set_author(name=guild.name)

        await ctx.send(embed=data)

    @commands.command(name="report", pass_context=True, no_pm=True)
    async def _report(self, ctx, user: discord.Member, *, reason):
        """Reports user and sends report to Bot Admin"""
        author = ctx.message.author
        guild = ctx.message.guild


        joined_at = user.joined_at
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        joined_on = "{}".format(user_joined)

        #args = ''.join(reason)
        adminlist = []
        check = lambda r: r.name in 'Bot Admin'

        members = guild.members
        for i in members:

            role = bool(discord.utils.find(check, i.roles))

            if role is True:
                adminlist.append(i)
            else:
                pass

        colour = discord.Colour.magenta()

        description = "User Report"
        data = discord.Embed(description=description, colour=colour)
        data.add_field(name="Report reason", value=reason)
        data.add_field(name="Report by", value=author)
        data.add_field(name="Reported user joined this server on", value=joined_on)
        data.set_footer(text="User ID:{}"
                             "".format(user.id))

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.avatar_url:
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=name)

        for i in adminlist:
           await i.send(embed=data)


def setup(bot):
    n = General(bot)
    bot.add_cog(n)
