import discord
from discord.ext import commands
import random
import time


class General:
    """General commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="join", pass_context=True)
    async def _join(self, ctx):
        """Join Official Bot Discord"""
        author = ctx.message.author
        print(author)
        await self.bot.say("{} Join **#DoorSquad** at https://discord.io/doorsquad".format(author.mention))


    @commands.command(name="contact", aliases=["cnt"], pass_context=True)
    async def contact(self, ctx, *, message : str):
        """Sends a message to the bot developer (owner)"""
        owner = discord.utils.get(self.bot.get_all_members(),
                                  id="277844990695178240")
        server = ctx.message.server
        author = ctx.message.author
        footer = "User ID: " + author.id + " | Server ID: " + server.id
        source = "From {}".format(server)

        colour = discord.Colour.green()

        description = "Sent by {} {}".format(author, source)

        msg = discord.Embed(colour=colour, description=message)
        msg.set_author(name=description)
        msg.set_footer(text=footer)

        await self.bot.send_message(owner, embed=msg)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong."""
        t1 = time.perf_counter()
        await self.bot.send_typing(ctx.message.channel)
        t2 = time.perf_counter()
        thedata = (":ping_pong: **Pong.**\nTime: " + str(round((t2 - t1) * 1000)) + "ms")
        color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
        color = int(color, 16)
        data = discord.Embed(description=thedata, colour=discord.Colour(value=color))

        await self.bot.say(embed=data)

    @commands.command(name="userinfo", aliases=["whois"], pass_context=True, no_pm=True)
    async def _userinfo(self, ctx, *, user: discord.Member = None):
        """Shows information about a user"""
        author = ctx.message.author
        server = ctx.message.server
        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]
        joined_at = user.joined_at
        since_created = (ctx.message.timestamp - user.created_at).days
        since_joined = (ctx.message.timestamp - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        member_number = sorted(server.members,
                               key=lambda m: m.joined_at).index(user) + 1

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)
        game = "Chilling in {} status".format(user.status)

        if user.game is None:
            pass
        elif user.game.url is None:
            game = "Playing {}".format(user.game)
        else:
            game = "Streaming: [{}]({})".format(user.game, user.game.url)

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = discord.Embed(description=game, colour=user.colour)
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

        await self.bot.say(embed=data)

    @commands.command(name="serverinfo", pass_context=True, no_pm=True)
    async def _serverinfo(self, ctx):
        """Shows information about the server"""
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        colour = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        data = discord.Embed(
            description=created_at,
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        await self.bot.say(embed=data)

    @commands.command(name="report", pass_context=True, no_pm=True)
    async def _report(self, ctx, user: discord.Member, *, reason):
        """Reports user and sends report to Bot Admin"""
        author = ctx.message.author
        server = ctx.message.server


        joined_at = user.joined_at
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        joined_on = "{}".format(user_joined)

        #args = ''.join(reason)
        adminlist = []
        check = lambda r: r.name in 'Bot Admin'

        members = server.members
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
        data.add_field(name="Reported user joinned this server on", value=joined_on)
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
           await self.bot.send_message(i, embed=data)


def setup(bot):
    n = General(bot)
    bot.add_cog(n)
