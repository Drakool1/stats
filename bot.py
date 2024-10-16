import discord
from discord.ext import commands
import subprocess
from wallet import stats

# Directly hardcode the token here (not recommended for production)
TOKEN = "MTI5NTk0MzEyMDI0ODExNTI1MA.GQ1eTC.CXZbdKhHXVWyAH6WNoNLNZIIx9qxiWfr6zoDcI"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.channel.name == "bot-for-milliam":
        if len(message.content) == 44:
            # Execute stats.py
            try:
                output = stats(message.content)
                
                # Send the output from stats.py as a message to the Discord channel
                await message.channel.send(f"```{output}```")
            except Exception as e:
                await message.channel.send(f"An error occurred: {e}")
    
    await bot.process_commands(message)

bot.run(TOKEN)