import re
from pyrogram import Client
from pyrogram.types import Message
from info import API_ID, API_HASH
from typing import List

# Set up the keyword pattern and output file
KEYWORD_PATTERN = re.compile(r"\bبرنامه\s?نویسی\b")
OUTPUT_FILE = "history_with_matches.txt"


def load_channels(filename: str) -> List[str]:
    """
    Loads a list of channel usernames from a file.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []


def contains_keyword(text: str) -> bool:
    """
    Checks whether the message text contains the target keyword.
    """
    return bool(KEYWORD_PATTERN.search(text))


async def message_user_if_possible(app: Client, message: Message):
    """
    Sends a private message to the sender if possible.
    """
    sender = message.from_user
    if sender and not sender.is_self:
        try:
            await app.send_message(sender.id, "سلام برنامه نویسی داش؟")
            print(f"Messaged user: {sender.id}")
        except Exception as e:
            print(f"Could not message user {sender.id}: {e}")


async def fetch_history_and_message_users(app: Client, channels: List[str], limit: int = 100):
    """
    Fetches message history from channels, writes messages to file,
    and privately messages users if their message matches the pattern.
    """
    try:
        async with app:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                for channel in channels:
                    f.write(f"\n--- Messages from ({channel}) ---\n")
                    print(f"Checking channel: {channel}")

                    async for message in app.get_chat_history(channel, limit=limit):
                        clean_text = message.text.replace("\n", " ") if message.text else ""
                        if clean_text:
                            f.write(clean_text + "\n")

                            if contains_keyword(clean_text):
                                await message_user_if_possible(app, message)
    except Exception as e:
        print(f"Error during processing: {e}")


async def send_text_message(app: Client, user_id: str, message: str):
    """
    Manually send a text message to a user/channel.
    """
    try:
        async with app:
            await app.send_message(user_id, message)
            print(f"Manual message sent to {user_id}")
    except Exception as e:
        print(f"Failed to send message to {user_id}: {e}")


def main():
    proxy_config = {
        "hostname": "127.0.0.1",
        "port": 10808,
        "scheme": "socks5"
    }

    app = Client(
        "Tabchi",
        api_id=API_ID,
        api_hash=API_HASH,
        proxy=proxy_config
    )

    channels = load_channels("IDs.txt")

    async def runner():
        await fetch_history_and_message_users(app, channels)
        # manually test:
        # await send_text_message(app, "username_or_id", "Hello from TabchiBot")

    app.run(runner())


if __name__ == "__main__":
    main()