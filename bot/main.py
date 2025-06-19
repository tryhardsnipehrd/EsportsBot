import discord
import os

CLIENT_TOKEN = os.getenv("DISCORD_TOKEN")
LOG_CHANNEL_ID = 1385096206140838020


if CLIENT_TOKEN == None:
    print("Please provide the bot token with the `DISCORD_TOKEN` variable")
    exit()

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True


client = discord.Client(intents=intents)

log_channel = None


@client.event
async def on_ready():
    global log_channel

    print(f"Logged in as {client.user}")

    log_channel = client.get_channel(LOG_CHANNEL_ID)
    if log_channel == None:
        print(f"Could not connect to channel id {LOG_CHANNEL_ID}")


@client.event
async def on_message_delete( message ):

    global log_channel

    print(f"Message deleted: {message.content}")

    DeletedEmbed = discord.Embed(
        title=message.author.name,
        description=message.content,
        color=0xFF0000
        )
    
    await log_channel.send(embed=DeletedEmbed)


client.run(CLIENT_TOKEN)
