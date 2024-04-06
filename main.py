import discord
from discord.ext import commands
import requests

# Define intents
intents = discord.Intents.all()

# Discord bot client
client = commands.Bot(command_prefix='.', intents=intents)

# Constants
PREFIX = "."

# Function to fetch data from the API
def fetch_data(url):
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,cs;q=0.7",
        "content-type": "application/json",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }
    payload = {"authenticate_over_turret": True}
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

@client.command()
async def version(ctx):
    try:
        url = "https://deadlinegame.com/api/public/deadline/vars/version"
        data = fetch_data(url)
        if data:
            key_value = data.get("key_value")
            if key_value:
                embed = discord.Embed(title="Game Version", description=key_value, color=discord.Color.blue())
                await ctx.send(embed=embed)
            else:
                await ctx.send("No version available?? idk how the api is stupid")
        else:
            await ctx.send("Failed to fetch game version.")
    except Exception as e:
        print("An error occurred:", e)
        await ctx.send("An error occurred while fetching game version.")


@client.command()
async def info(ctx):
    try:
        url = "https://deadlinegame.com/api/public/deadline/vars/announcement"
        data = fetch_data(url)
        if data:
            key_value = data.get("key_value")
            if key_value:
                embed = discord.Embed(title="Announcement", description=key_value, color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                await ctx.send("No announcement available.")
        else:
            await ctx.send("Failed to fetch announcement.")
    except Exception as e:
        print("An error occurred:", e)
        await ctx.send("An error occurred while fetching announcement.")



@client.command()
async def patchnote(ctx, id: str = None):
    if id is None:
        await ctx.send("Please specify the ID of the patch note you want to view.")
        return

    try:
        url = f"https://deadlinegame.com/api/public/deadline/patchnotes/note/{id}"
        data = fetch_data(url)
        if data:
            game_version = data.get("game_version")
            content = data.get("content")
            date = data.get("date")
            if game_version and content and date:
                message = f"**Patch Note {id}** (Version {game_version}, Date: {date}):\n{content}"
                await ctx.send(message)
            else:
                await ctx.send(f"No patch note found with ID {id}.")
        else:
            await ctx.send("Failed to fetch patch note.")
    except Exception as e:
        print("An error occurred:", e)
        await ctx.send("An error occurred while fetching patch note.")

@client.command()
async def patchnotes(ctx):
    try:
        url = "https://deadlinegame.com/api/public/deadline/patchnotes/list"
        data = fetch_data(url)
        if data:
            embed = discord.Embed(title="Patch Notes", description="List of patch notes", color=discord.Color.blue())
            patch_notes = [f"ID: {note}" for note in data]

            # Split patch notes into groups of 25
            for i in range(0, len(patch_notes), 25):
                embed.add_field(name="Patch Notes", value="\n".join(patch_notes[i:i+25]), inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch patch notes.")
    except Exception as e:
        print("An error occurred:", e)
        await ctx.send("Failed to fetch patch notes.")




# Event: Bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

# Run the bot
client.run('YOUR-ID-HERE')
