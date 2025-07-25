from telethon import TelegramClient, events
import re

# Use your Bot Token here
bot_token = '8364389014:AAEyyI-7lr5DvGgUZfeCnRtnk02lDvJsmgE'

# Replace with your actual channel IDs
source_channel = -1002885203433  # Channel A
destination_channel = -1002826523175    # Channel B

# List of filter terms to skip
FILTER_TERMS = ["yash"]

# Your custom link to add
CUSTOM_LINK = "🔗 Join Free VIP REGISTER HERE 👉 https://broker-qx.pro/sign-up/?lid=652808"

# Create a bot client
client = TelegramClient(None, api_id=28032895, api_hash='bfb3c9a75844a12c50c6c1ef7fd2801b').start(bot_token=bot_token)

def add_custom_link_if_otc(text):
    # If the message contains "otc" or "OTC", modify it
    if re.search(r'\botc\b', text, flags=re.IGNORECASE):
        # Remove existing links
        text = re.sub(r'https?://\S+|t\.me/\S+', '', text)

        # Remove existing custom link line if any
        text = re.sub(
            r"(🔗\s*Join\s*Free\s*VIP\s*REGISTER\s*HERE.*)",
            '',
            text,
            flags=re.IGNORECASE
        )

        # Append custom link
        text = text.strip() + f"\n\n{CUSTOM_LINK}"

    return text.strip()

@client.on(events.NewMessage(chats=source_channel))
async def forward_message(event):
    message_text = event.message.message or ""

    # Skip if any filter terms match
    if any(term.lower() in message_text.lower() for term in FILTER_TERMS):
        print(f"Message skipped (filtered): {message_text[:50]}..." if message_text else "Message skipped (no text)")
        return

    # Add custom link only if "otc"/"OTC" is present
    updated_text = add_custom_link_if_otc(message_text)

    try:
        await client.send_message(destination_channel, updated_text)
        print(f"Message forwarded: {updated_text[:50]}..." if updated_text else "Message forwarded (no text)")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")

async def main():
    print("✅ Bot is starting...")
    print(f"📌 Filtering messages containing: {', '.join(FILTER_TERMS)}")
    print("🤖 Bot is now running!")

client.loop.run_until_complete(main())
client.run_until_disconnected()
