import discord
from dotenv import load_dotenv; load_dotenv()
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


@client.eventn
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

#    print(f"Message deleted: {message.content}")
    message_author = message.author
    author_name = message_author.nick if message_author.nick else message_author.name
    author_id = message_author.id
    author_pfp = message_author.display_avatar.url


    # Build our embed, using red as our color
    DeletedEmbed = discord.Embed(
        title=f"{author_name} - {author_id}",
        description=message.content,
        color=0xFF0000
        )
    DeletedEmbed.set_thumbnail(url=author_pfp)
    # Send the embed. Uses await to not be blocking
    await log_channel.send(embed=DeletedEmbed)

@client.event
async def on_message_edit( old_message, new_message ):
    global log_channel

    # We need to exit out if this wasn't a direct edit
    # We can check this by seeing if they two messages are the exact same content.
    if old_message.content == new_message.content:
        return
    
    message_author = old_message.author
    author_name = message_author.nick if message_author.nick else message_author.name
    author_id = message_author.id
    author_pfp = message_author.display_avatar.url


    # Create our embed
    EditedEmbed = discord.Embed(
        title=f"{author_name} - <{author_id}>",
        color=0xF9B52C,
        description=f"**Old:** {old_message.content}\n\n**+New:** {new_message.content}"
    )
    EditedEmbed.set_thumbnail(url=author_pfp)

    await log_channel.send(embed=EditedEmbed)
    

client.run(CLIENT_TOKEN)
