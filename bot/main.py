import aiosqlite as sql
import asyncio
import discord
from discord import app_commands
from dotenv import load_dotenv; load_dotenv()
import os


CLIENT_TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH")
REACT_MESSAGE_ID = int(os.getenv("REACT_MESSAGE_ID"))

# Verify that we actually got a bot token
if CLIENT_TOKEN == None:
    print("Please provide the bot token with the `DISCORD_TOKEN` variable")
    exit()

# This is where the deletions and other logs will be sent
LOG_CHANNEL_ID = None
# This ensures we have a variable to log to
log_channel = None

intents = discord.Intents.default()
# We need to be able to *read* messages
intents.message_content = True
# As well as get the messages from id (for logs)
intents.messages = True

client = discord.Client(intents=intents)


# Let's connect to the database, and ensure tables are setup
async def setup_database():
    async with sql.connect(DATABASE_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS reacts(emote text, role int);")
        await db.execute("CREATE TABLE IF NOT EXISTS settings(name text, data text);")
        await db.commit()

# DEBUG
async def debug_database(table):
    async with sql.connect(DATABASE_PATH) as db:
        db.row_factory = sql.Row
        async with db.execute(f"SELECT * FROM {table}") as cursor:
            for row in await cursor.fetchall():
                for item in row:
                    print(f"{item} | ", end="")
                print()



async def get_settings():
    async with sql.connect(DATABASE_PATH) as db:
        # Anything we need immediately will need to be specified here.
        global LOG_CHANNEL_ID
        result = await db.execute("SELECT * FROM settings WHERE name='log_channel'")
        result = await result.fetchone()
        LOG_CHANNEL_ID = int(result[1])
        print(f"Log Channel ID Retrieved from DB: {LOG_CHANNEL_ID}")
    
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

@client.event
async def on_raw_reaction_add( payload ):
    if payload.message_id == REACT_MESSAGE_ID:
        emoji = payload.emoji
        if emoji.url == "":
            parsed_name = ord(emoji.name)
        else:
            parsed_name = emoji.name

        match parsed_name:
            case "RL":
                print("Ball Chaser")
            case "catface":
                print("Here Kitty Kitty")
            case 129370:
                print("Egg")


# Start
if __name__ == "__main__":
    # Setup the database to ensure it exists and is ready
    asyncio.run(setup_database())
    asyncio.run(get_settings())


    client.run(CLIENT_TOKEN)
