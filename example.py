from telethon import TelegramClient, events
import re
import os  # Optional: for environment variables

# Replace with your API credentials
api_id = 'xxxxxxxx'  # Your API ID
api_hash = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # Your API Hash

# Replace with the ID of the public source channel
source_channel_id = xxxxxxxxxx  # Use the numeric ID here (replace with actual numeric ID)

# Replace with the bot username (without @)
bot_username = 'example1bot'  # The bot's public username

# Initialize the Telegram client (logged in as a user)
client = TelegramClient('anon', api_id, api_hash)

# Counter for forwarded messages
forward_count = 1

async def main():
    await client.start()

    try:
        # Fetch the channel entity using the chat ID
        channel = await client.get_entity(source_channel_id)
        # Print channel details
        print("Sisokiki Bot started.")  # Confirmation message when the bot starts
    except Exception as e:
        print(f"Error fetching channel details: {e}")

# Function to send messages to the bot (as a normal user)
async def forward_to_bot(message_text):
    global forward_count  # Use the global counter
    # Prepare the full message with count
    full_message = f"{message_text}"  # Do not include "Forwarded: {forward_count}."
    
    # Send the message to the bot without the forwarded prefix
    await client.send_message(bot_username, full_message)
    
    # Print the forwarded message with its count for logging
    print(f"Forwarded: {forward_count}. {full_message}")  
    forward_count += 1  # Increment the count after forwarding

# Event handler for new messages in the source channel
@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    # Check if the message contains text or media (photo)
    if event.message.message:
        message = event.message.message  # Get the message text

        # Forward only if the message contains a link or is a photo
        if re.search(r'http[s]?://', message) or event.message.media:  # Check for links or media
            await forward_to_bot(message)  # Send the message to the bot
    elif event.message.media:  # If the message has media (like a photo)
        media_message = "This message contains a photo."
        await forward_to_bot(media_message)  # Send a custom message for media

# Start the client and run it
with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
