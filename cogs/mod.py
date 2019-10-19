
import discord
from discord.ext import commands
import asyncio

from cogs.utils import checks

class Mod(commands.Cog):
    """Mod tools"""

    def __init__(self, bot):
        self.bot = bot
        self.muted_users = []



    def is_allowed_by_hierarchy(self, guild, author, user):

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
        guild = author.guild
        is_bot = self.bot.user.bot
        has_permissions = channel.permissions_for(guild.me).manage_messages

        to_delete = []

        if not has_permissions:
            await ctx.send("I'm not allowed to delete messages.")
            return

        async for message in channel.history(limit=number + 1):
            to_delete.append(message)

        if is_bot:
            await self.mass_purge(to_delete, channel)


    async def mass_purge(self, messages, channel):
        while messages:
            if len(messages) > 1:
                await channel.delete_messages(messages[:100])
                messages = messages[100:]
            else:
                await messages[0].delete()
                messages = []
            await asyncio.sleep(1.5)

    @commands.command(name="ban", pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    async def _ban(self, ctx, *reason):
        """Bans user and sends them the reason"""
        author = ctx.message.author
        guild = ctx.message.guild

        user = ctx.message.mentions[0]

        if author == user:
            await ctx.send(":no_entry_sign: You cannot ban yourself!")
            return
        elif not self.is_allowed_by_hierarchy(guild, author, user):
            await ctx.send(":no_entry_sign: You cannot do this to someone with the same or higher role!")
            return


        colour = discord.Colour.red()
        reason = ' '.join(reason)
        message = ("Banned by **{}** from **{}** with reason: **{}**".format(author, guild, reason))

        msg = discord.Embed(colour=colour, description=message)

        await user.ban()
        await user.send(embed=msg)

        await ctx.send(":b: :regional_indicator_a: :regional_indicator_n: :regional_indicator_n: :regional_indicator_e: :regional_indicator_d: \n:regional_indicator_u: :regional_indicator_s: :regional_indicator_e: :regional_indicator_r: \n{}".format(user.mention))

    @commands.command(name="softban", no_pm=True)
    @checks.admin_or_permissions(ban_members=True)
    async def _softban(self, ctx, *reason):
        """Softbans user and sends them the reason"""
        author = ctx.message.author
        guild = ctx.message.guild

        user = ctx.message.mentions[0]

        if author == user:
            await ctx.send(":no_entry_sign: You cannot ban yourself!")
            return
        elif not self.is_allowed_by_hierarchy(guild, author, user):
            await ctx.send(":no_entry_sign: You cannot do this to someone with the same or higher role!")
            return

        colour = discord.Colour.red()
        reason = ' '.join(reason)
        message = ("You have been removed from **{}** by **{}** with reason: **{}**".format(author, guild, reason))

        msg = discord.Embed(colour=colour, description=message)
        msg = discord.Embed(colour=colour, description=message)

        await user.ban()
        await user.unban()
        await user.send(embed=msg)


    @commands.command(name="kick", pass_context=True)
    @checks.mod_or_permissions(kick_members=True)
    async def _kick(self, ctx, *reason):
        """Kicks user and sends them the reason"""
        author = ctx.message.author
        guild = ctx.message.guild

        user = ctx.message.mentions[0]

        if author == user:
            await ctx.send(":no_entry_sign: You cannot ban yourself!")
            return
        elif not self.is_allowed_by_hierarchy(guild, author, user):
            await ctx.send(":no_entry_sign: You cannot do this to someone with the same or higher role!")
            return

        colour = discord.Colour.red()
        reason = ' '.join(reason)
        message = ("Kicked by **{}** from **{}** with reason: **{}**".format(author, guild, reason))

        msg = discord.Embed(colour=colour, description=message)

        await user.kick()
        await user.send(embed=msg)

    @commands.command(name="mute", pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def _mute(self, ctx):
        """Mute a user"""
        author = ctx.message.author
        #guild = ctx.message.guild

        user = ctx.message.mentions[0]

        if author == user:
            await ctx.send(":no_entry_sign: You cannot mute yourself!")
            return
        if user in self.muted_users:
            await ctx.send('`{0}` is already muted!'.format(user))
            return
        else:
            await user.edit(mute=True)
            self.muted_users.append(user)
            await ctx.send("I've muted `{0}`".format(user))


    @commands.command(name="unmute", pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def _unmute(self, ctx):
        """Unmute a user"""
        author = ctx.message.author

        user = ctx.message.mentions[0]

        if author == user:
            await ctx.send(":no_entry_sign: You cannot unmute yourself!")
            return
        elif user not in self.muted_users:
            await ctx.send('`{0}` is not muted!'.format(user))
            return
        else:
            await user.edit(mute=False)
            self.muted_users.remove(user)
            await ctx.send("I've unmuted `{0}`".format(user))

    @commands.command(name="botban", pass_context=True, no_pm=True)
    @checks.mod_or_permissions()
    async def _botban(self, ctx):
        """Ban user from using the bot"""
        author = ctx.message.author
        #guild = ctx.message.guild

        user = ctx.message.mentions[0]

        if author == user:
            await ctx.send(":no_entry_sign: You cannot mute yourself!")
            return
        if user in self.muted_users:
            await ctx.send('`{0}` is already muted!'.format(user))
            return
        else:
            await user.edit(mute=True)
            self.muted_users.append(user)
            await ctx.send("I've muted `{0}`".format(user))



def setup(bot):
    n = Mod(bot)
    bot.add_cog(n)
