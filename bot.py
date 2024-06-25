import discord
from discord.ext import commands
from discord import app_commands
import requests
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os
import pprint

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
ALLOWED_GUILD_ID = int(os.getenv('ALLOWED_GUILD_ID'))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.tree.command(name="ping", description="Get the ping")
async def ping(interaction: discord.Interaction):
    if interaction.guild.id != ALLOWED_GUILD_ID:
        await interaction.response.send_message("This bot only works in the designated server.", ephemeral=True)
        return

    await interaction.response.send_message(f"**Latency:** {int((bot.latency * 1000))}ms", ephemeral=True)

# @bot.tree.command(name="create_event", description="Schedule a server event")
# @app_commands.describe(weeks="How many weeks of CTFs do you want to add to the Events Tab?")
# async def create_event(interaction: discord.Interaction, weeks: int):


bot.run(TOKEN)
