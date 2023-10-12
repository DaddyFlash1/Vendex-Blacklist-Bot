import discord
from discord.ext import commands
import asyncio  # Import asyncio module for creating a timer

# Define your intents
intents = discord.Intents.all()

# Your bot token
TOKEN = "YOUR BOT TOKEN"

# Create a bot instance with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Define a list of blacklisted user IDs and their reasons
blacklist = {

}

# The name of the role to be assigned to blacklisted users
BLACKLIST_ROLE_ID = "Geblacklisted"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(f"Wachting {len(blacklist)} blacklisted users"))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(f"Wachting {len(blacklist)} blacklisted users"))

    # Check for blacklisted users and send them a message
    for member in bot.get_all_members():
        if member.id in blacklist:
            reason = blacklist[member.id]
            role = discord.utils.get(member.guild.roles, name=BLACKLIST_ROLE_ID)
            if role is not None and role not in member.roles:
                await member.add_roles(role)
                await member.send(f"[RoGuard] Sorry, you are blacklisted for the following reason: {reason}. discord.gg/roguard Contact an admin or make a ticket.")

async def role(ctx):
    role = discord.utils.get(ctx.guild.roles, name=BLACKLIST_ROLE_ID)
    if role is not None:
        members_with_role = [member for member in ctx.guild.members if role in member.roles]
        if members_with_role:
            blacklisted_users = "\n".join([f"{member} ({reason})" for member, reason in blacklist.items() if member.id in [m.id for m in members_with_role]])
            if blacklisted_users:
                await ctx.send(f"Users with the {BLACKLIST_ROLE_ID} role:\n{blacklisted_users}")
            else:
                await ctx.send(f"No users have the {BLACKLIST_ROLE_ID} role.")
        else:
            await ctx.send(f"No users have the {BLACKLIST_ROLE_ID} role.")
    else:
        await ctx.send(f"The {BLACKLIST_ROLE_ID} role does not exist on this server.")

@bot.event
async def on_member_update(before, after):
    # Check if a user was blacklisted after joining the server
    if before.id not in blacklist and after.id in blacklist:
        reason = blacklist[after.id]
        role = discord.utils.get(after.guild.roles, name=BLACKLIST_ROLE_ID)
        if role is not None:
            await after.add_roles(role)
            await after.send(f"[RoGuard] Sorry, you are blacklisted for the following reason: {reason}. Contact an admin or make a ticket.")

async def delete_message(msg, delay=3):
    await asyncio.sleep(delay)
    await msg.delete()

@bot.command()
async def add_blacklist(ctx, user_id: int, reason: str):
    blacklist[user_id] = reason
    confirmation_msg = await ctx.send(f"[RoGuard] User with ID {user_id} has been blacklisted for {reason}.")
    await ctx.author.send(f"[RoGuard] You have added User with ID {user_id} to the blacklist for {reason}.")
    await bot.change_presence(activity=discord.Game(f"Wachting {len(blacklist)} blacklisted users"))
    # Schedule the confirmation message for deletion after 3 seconds
    await delete_message(confirmation_msg)

@bot.command()
async def show(ctx):
    blacklisted_users = "\n".join([f"{member} ({reason})" for member, reason in blacklist.items()])
    
    if not blacklisted_users:
        await ctx.send("No users are currently blacklisted.")
    else:
        await ctx.send(f"Blacklisted Users:\n{blacklisted_users}")

@bot.command()
async def remove_blacklist(ctx, user_id: int):
    if user_id in blacklist:
        del blacklist[user_id]
        confirmation_msg = await ctx.send(f"[RoGuard] User with ID {user_id} has been removed from the blacklist.")
        await ctx.author.send(f"[RoGuard] User with ID {user_id} has been removed from the blacklist.")
        await bot.change_presence(activity=discord.Game(f"Wachting {len(blacklist)} blacklisted users"))
        # Schedule the confirmation message for deletion after 3 seconds
        await delete_message(confirmation_msg)
    else:
        confirmation_msg = await ctx.send(f"[RoGuard] User with ID {user_id} is not blacklisted.")
        await ctx.author.send(f"[RoGuard] User with ID {user_id} is not blacklisted.")
        # Schedule the confirmation message for deletion after 3 seconds
        await delete_message(confirmation_msg)

# Run the bot
bot.run(TOKEN)
