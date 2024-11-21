import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import numpy as np

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
    # Get the user who invoked the command (the challenger)
    challenger = ctx.author

    # Ensure the command is not used to duel the same person
    if challenger == opponent:
        await ctx.send("You cannot duel yourself!")
        return
    if opponent == ctx.guild.me:
        await ctx.send("You can't duel the law!")
        await ctx.send(f"{challenger.mention} has been shot and killed....")
        if KICKING:
            challenger.kick()
    
    # Mention both users in the message
    await ctx.send(f"{challenger.mention} has challenged {opponent.mention} to a duel!")
    await ctx.send(f"When it is {duel_time} be the first to respond with \"bang\" to win the duel.")

    wait_time = np.random.randint(1,30)
    print(wait_time)
    await asyncio.sleep(wait_time)
    await ctx.send(f"IT'S {duel_time}! {challenger.mention} {opponent.mention}")
    
    # Define a check to ensure the message is from the challenger or opponent
    def check(m):
        return m.author in [challenger, opponent]

    try:
        # Wait for a message from either the challenger or opponent
        message = await bot.wait_for("message", check=check, timeout=10.0)  # 60 seconds timeout
        # Check if the message contains the correct keyword
        if message.content.lower() == "bang":
            await ctx.send(f"{message.author.mention} wins the duel!")
            if message.author == challenger:
                #KICK OPPONENT
                await ctx.send(f"{opponent.mention} has been killed...")
                if KICKING:
                    opponent.kick()
                    # bot.kick(opponent)
                
            if message.author == opponent:
                #KICK CHALLENGER
                await ctx.send(f"{challenger.mention} has been killed...")
                if KICKING:
                    challenger.kick()
                    # bot.kick(challenger)
                
        else:
            await ctx.send(f"{message.author.mention} misfired!")
            await ctx.send(f"{message.author.mention} has been killed...")
            if KICKING:
                message.author.kick()
                # bot.kick(message.author)

    except asyncio.TimeoutError:
        await ctx.send("Time's up! Everyone got confused.")
        await ctx.send(f"{challenger.mention} has been killed...")
        await ctx.send(f"{opponent.mention} has been killed...")
        if KICKING:
            challenger.kick()
            opponent.kick()

# Run the bot
bot.run(TOKEN)