
import discord
from discord.ext import commands
import asyncio

from cogs.utils import checks

class Mod:
    """Mod tools"""

    def __init__(self, bot):
        self.bot = bot
        self.muted_users = []



    def is_allowed_by_hierarchy(self, server, author, user):

        roles_author = author.top_role #[x.id for x in author.roles if x.id != "@everyone"]
        roles_user = user.top_role#[x.id for x in user.roles if x.id != "@everyone"]

        print("Author", roles_author, "\nUser", roles_user)

        if roles_author == roles_user:
            return False
        elif roles_author > roles_user:
            return True

    @commands.command(name="prune", aliases=["clr", "cls", "clear"], pass_context=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def _prune(self, ctx, number: int):
        """Deletes last X messages"""

        channel = ctx.message.channel
        author = ctx.message.author
        server = author.server
        is_bot = self.bot.user.bot
        has_permissions = channel.permissions_for(server.me).manage_messages

        to_delete = []

        if not has_permissions:
            await self.bot.say("I'm not allowed to delete messages.")
            return

        async for message in self.bot.logs_from(channel, limit=number + 1):
            to_delete.append(message)

        if is_bot:
            await self.mass_purge(to_delete)


    async def mass_purge(self, messages):
        while messages:
            if len(messages) > 1:
                await self.bot.delete_messages(messages[:100])
                messages = messages[100:]
            else:
                await self.bot.delete_message(messages[0])
                messages = []
            await asyncio.sleep(1.5)

    @commands.command(name="ban", pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    async def _ban(self, ctx, user : discord.Member, *reason):
        """Bans user and sends them the reason"""
        author = ctx.message.author
        server = ctx.message.server

        if author == user:
            await self.bot.say(":no_entry_sign: You cannot ban yourself!")
            return
        elif not self.is_allowed_by_hierarchy(server, author, user):
            await self.bot.say(":no_entry_sign: You cannot do this to someone with the same or higher role!")
            return


        colour = discord.Colour.red()
        reason = ' '.join(reason)
        message = ("Banned by **{}** from **{}** with reason: **{}**".format(author, server, reason))

        msg = discord.Embed(colour=colour, description=message)

        await self.bot.ban(user)
        await self.bot.send_message(user, embed=msg)

        await self.bot.say(":b: :regional_indicator_a: :regional_indicator_n: :regional_indicator_n: :regional_indicator_e: :regional_indicator_d: \n:regional_indicator_u: :regional_indicator_s: :regional_indicator_e: :regional_indicator_r: \n{}".format(user.mention))

    @commands.command(name="softban", no_pm=True)
    @checks.admin_or_permissions(ban_members=True)
    async def _softban(self, ctx, user : discord.Member, *reason):
        """Softbans user and sends them the reason"""
        author = ctx.message.author
        server = ctx.message.server

        if author == user:
            await self.bot.say(":no_entry_sign: You cannot ban yourself!")
            return
        elif not self.is_allowed_by_hierarchy(server, author, user):
            await self.bot.say(":no_entry_sign: You cannot do this to someone with the same or higher role!")
            return

        colour = discord.Colour.red()
        reason = ' '.join(reason)
        message = ("You have been removed from **{}** by **{}** with reason: **{}**".format(author, server, reason))

        msg = discord.Embed(colour=colour, description=message)
        msg = discord.Embed(colour=colour, description=message)

        await self.bot.ban(user)
        await self.bot.unban(user.server, user)
        await self.bot.send_message(user, embed=msg)


    @commands.command(name="kick", pass_context=True)
    @checks.mod_or_permissions(kick_members=True)
    async def _kick(self, ctx, user : discord.Member, *reason):
        """Kicks user and sends them the reason"""
        author = ctx.message.author
        server = ctx.message.server

        if author == user:
            await self.bot.say(":no_entry_sign: You cannot ban yourself!")
            return
        elif not self.is_allowed_by_hierarchy(server, author, user):
            await self.bot.say(":no_entry_sign: You cannot do this to someone with the same or higher role!")
            return

        colour = discord.Colour.red()
        reason = ' '.join(reason)
        message = ("Kicked by **{}** from **{}** with reason: **{}**".format(author, server, reason))

        msg = discord.Embed(colour=colour, description=message)

        await self.bot.kick(user)
        await self.bot.send_message(user, embed=msg)

    @commands.command(name="mute", pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def _mute(self, ctx, user: discord.User):
        """Mute a user"""
        author = ctx.message.author
        #server = ctx.message.server

        if author == user:
            await self.bot.say(":no_entry_sign: You cannot mute yourself!")
            return
        if user in self.muted_users:
            await self.bot.say('`{0}` is already muted!'.format(user))
            return
        else:
            await self.bot.server_voice_state(user, mute=True)
            self.muted_users.append(user)
            await self.bot.say("I've muted `{0}`".format(user))


    @commands.command(name="unmute", pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def _unmute(self, ctx, user: discord.User):
        """Unmute a user"""
        author = ctx.message.author

        if author == user:
            await self.bot.say(":no_entry_sign: You cannot unmute yourself!")
            return
        elif user not in self.muted_users:
            await self.bot.say('`{0}` is not muted!'.format(user))
            return
        else:
            await self.bot.server_voice_state(user, mute=False)
            self.muted_users.remove(user)
            await self.bot.say("I've unmuted `{0}`".format(user))

    @commands.command(name="botban", pass_context=True, no_pm=True)
    @checks.mod_or_permissions()
    async def _botban(self, ctx, user: discord.User):
        """Ban user from using the bot"""
        author = ctx.message.author
        #server = ctx.message.server

        if author == user:
            await self.bot.say(":no_entry_sign: You cannot mute yourself!")
            return
        if user in self.muted_users:
            await self.bot.say('`{0}` is already muted!'.format(user))
            return
        else:
            await self.bot.server_voice_state(user, mute=True)
            self.muted_users.append(user)
            await self.bot.say("I've muted `{0}`".format(user))



def setup(bot):
    n = Mod(bot)
    bot.add_cog(n)
