from telethon import TelegramClient, events
import re

api_id = 22278613
api_hash = '7913c40bc63fcb60705a0ce9076349ac'
bot_token = '8173515952:AAEu8r9anGuEayTp4xCgmS4ku-vNj0Xl7kw'

# Source Channels to listen to
SOURCE_CHANNELS = ['Stock_aaj_or_kal', 'officialequitymaster2']

# Destination Channel
TARGET_CHANNEL = 'smart_trading_alerts'  # replace with your real channel username (without @)

# Filters
LINK_FILTERS = [
    "https://t.me/", "https://cosmofeed.com/", "https://wa.me/", "https://x.com/"
]

USERNAME_PATTERN = r'@\w+'

def contains_filtered_links(text):
    return any(link in text for link in LINK_FILTERS)

def clean_text(text):
    # Remove usernames and filtered links
    text = re.sub(USERNAME_PATTERN, '', text)
    for link in LINK_FILTERS:
        text = text.replace(link, '')
    return text.strip()

# Initialize Bot
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    msg = event.message
    if msg.text:
        if contains_filtered_links(msg.text):
            return  # Skip forwarding
        cleaned = clean_text(msg.text)
        if cleaned:
            await client.send_message(TARGET_CHANNEL, cleaned)
    elif msg.photo:
        caption = msg.text or ''
        if contains_filtered_links(caption):
            return
        caption = clean_text(caption)
        await client.send_file(TARGET_CHANNEL, msg.photo, caption=caption)

print("Bot is running...")
client.run_until_disconnected()
