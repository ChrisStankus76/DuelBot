import os
import asyncio
import discord
import numpy as np
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
KICKING = True

intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content in version 2.0+
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def duel(ctx, opponent: discord.Member):

    times_of_day = ["HIGH NOON", "DAWN", "DUSK", "MIDNIGHT"]
    duel_time = np.random.choice(times_of_day)
    challenger = ctx.author

    if challenger == opponent:
        await ctx.send("You cannot duel yourself!")
        return
    if opponent == ctx.guild.me:
        await ctx.send("You can't duel the law!")
        await ctx.send(f"{challenger.mention} has been shot and deleted....")
        if KICKING:
            await challenger.kick()

    # Mention both users in the message
    await ctx.send(f"{challenger.mention} has challenged {opponent.mention} to a duel!")
    await ctx.send(f"When it is {duel_time} be the first to respond with \"bang\" to win the duel.")

    wait_time = np.random.randint(1,30)
    print(wait_time)
    await asyncio.sleep(wait_time)
    await ctx.send(f"IT'S {duel_time}! {challenger.mention} {opponent.mention}")

    def check(m):
        return m.author in [challenger, opponent]

    try:
        # Wait for a message from either the challenger or opponent
        message = await bot.wait_for("message", check=check, timeout=10.0)
        if message.content.lower() == "bang":
            await ctx.send(f"{message.author.mention} wins the duel!")
            if message.author == challenger:
                await ctx.send(f"{opponent.mention} has been deleted...")
                if KICKING:
                    await opponent.kick()

            if message.author == opponent:
                await ctx.send(f"{challenger.mention} has been deleted...")
                if KICKING:
                    await challenger.kick()

        else:
            await ctx.send(f"{message.author.mention} misfired!")
            await ctx.send(f"{message.author.mention} has been deleted...")
            if KICKING:
                message.author.kick()

    except asyncio.TimeoutError:
        await ctx.send("Time's up! Everyone got confused.")
        await ctx.send(f"{challenger.mention} has been deleted...")
        await ctx.send(f"{opponent.mention} has been deleted...")
        if KICKING:
            await challenger.kick()
            await opponent.kick()

bot.run(TOKEN)
