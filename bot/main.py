import discord
import os

CLIENT_TOKEN = os.getenv("DISCORD_TOKEN")
# This is where the deletions and other logs will be sent
LOG_CHANNEL_ID = 1385096206140838020

# Verify that we actually got a bot token
if CLIENT_TOKEN == None:
    print("Please provide the bot token with the `DISCORD_TOKEN` variable")
    exit()

intents = discord.Intents.default()
# We need to be able to *read* messages
intents.message_content = True
# As well as get the messages from id (for logs)
intents.messages = True


client = discord.Client(intents=intents)

# This ensures we have a variable to log to
log_channel = None


@client.event
async def on_ready():
    # This needs to be global to fix scoping issues
    global log_channel

    print(f"Logged in as {client.user}")

    log_channel = client.get_channel(LOG_CHANNEL_ID)
    if log_channel == None:
        print(f"Could not connect to channel id {LOG_CHANNEL_ID}")
        exit() # TODO: Change this to setting a flag to disable logging instead


@client.event
async def on_message_delete( message ):
    # Again, need global to fix scoping
    global log_channel

    print(f"Message deleted: {message.content}")

    # Build our embed, using red as our color
    DeletedEmbed = discord.Embed(
        title=message.author.name,
        description=message.content,
        color=0xFF0000
        )

    # Send the embed. Uses await to not be blocking
    await log_channel.send(embed=DeletedEmbed)


client.run(CLIENT_TOKEN)
