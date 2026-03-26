"""
02_commands_and_handlers.py - Multiple Commands and Message Handlers

Demonstrates how to build a bot with multiple commands, argument parsing,
and different message type handlers:
- /start, /help, /caps, /info commands
- Command arguments via context.args
- Filters for text, photos, stickers, and locations
- Unknown command catch-all handler
- Handler registration order and priority

Usage:
    uv run 02_commands_and_handlers.py

Then open Telegram, find your bot, and try:
    /start          -> welcome message
    /help           -> list of commands
    /caps hello     -> "HELLO"
    /info           -> chat and user details
    Send a photo    -> bot acknowledges it
    Send a sticker  -> bot acknowledges it
    /unknown        -> catch-all response
Press Ctrl+C to stop.
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    """
    Configures dual logging: terminal (INFO) and file (DEBUG).
    Logs saved to logs/02_commands_and_handlers.log.
    """
    logs_directory = Path(__file__).parent / "logs"
    logs_directory.mkdir(exist_ok=True)
    log_file_path = logs_directory / "02_commands_and_handlers.log"

    logger = logging.getLogger("commands_bot")
    logger.setLevel(logging.DEBUG)

    terminal_handler = logging.StreamHandler()
    terminal_handler.setLevel(logging.INFO)
    terminal_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    )

    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(funcName)s:%(lineno)d - %(message)s"
        )
    )

    logger.addHandler(terminal_handler)
    logger.addHandler(file_handler)

    return logger


# ---------------------------------------------------------------------------
# Environment setup
# ---------------------------------------------------------------------------

def load_bot_token() -> str:
    """
    Loads the Telegram bot token from the .env file.
    Exits with a clear error if TELEGRAM_BOT_TOKEN is not found.
    """
    env_file_path = Path(__file__).parent / ".env"
    load_dotenv(env_file_path)

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("ERROR: TELEGRAM_BOT_TOKEN not found in .env file.")
        print("Create a .env file with: TELEGRAM_BOT_TOKEN=your_token_here")
        raise SystemExit(1)

    return bot_token


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /start — sends a welcome message.
    """
    logger = logging.getLogger("commands_bot")
    user = update.effective_user
    logger.info(f"/start from {user.first_name} (id: {user.id})")

    welcome_text = (
        f"Hello {user.first_name}!\n\n"
        "I'm a demo bot for learning commands and handlers.\n"
        "Type /help to see what I can do."
    )
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /help — lists all available commands with descriptions.
    """
    logger = logging.getLogger("commands_bot")
    logger.info(f"/help from {update.effective_user.first_name}")

    help_text = (
        "Available commands:\n\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/caps <text> - Convert text to UPPERCASE\n"
        "/info - Show your chat and user details\n\n"
        "I also respond to photos, stickers, and locations!"
    )
    await update.message.reply_text(help_text)


async def caps_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /caps <text> — converts command arguments to uppercase.

    Demonstrates context.args, which splits everything after the command
    into a list of strings. For example:
        /caps hello world  ->  context.args = ["hello", "world"]

    If no arguments are provided, sends a usage hint.
    """
    logger = logging.getLogger("commands_bot")
    user = update.effective_user

    if not context.args:
        logger.debug(f"/caps with no args from {user.first_name}")
        await update.message.reply_text("Usage: /caps <text>\nExample: /caps hello world")
        return

    original_text = " ".join(context.args)
    uppercased_text = original_text.upper()
    logger.info(f"/caps from {user.first_name}: '{original_text}' -> '{uppercased_text}'")

    await update.message.reply_text(uppercased_text)


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /info — displays details about the user and the chat.

    Demonstrates accessing update.effective_user and update.effective_chat
    to extract metadata like user ID, username, chat type, etc.
    """
    logger = logging.getLogger("commands_bot")
    user = update.effective_user
    chat = update.effective_chat
    logger.info(f"/info from {user.first_name} in chat {chat.id}")

    # Build user info section
    user_info_lines = [
        "User Info:",
        f"  ID: {user.id}",
        f"  First name: {user.first_name}",
        f"  Last name: {user.last_name or 'N/A'}",
        f"  Username: @{user.username}" if user.username else "  Username: N/A",
        f"  Is bot: {user.is_bot}",
        f"  Language: {user.language_code or 'N/A'}",
    ]

    # Build chat info section
    chat_info_lines = [
        "\nChat Info:",
        f"  ID: {chat.id}",
        f"  Type: {chat.type}",
    ]
    # Title is only available for groups/channels, not private chats
    if chat.title:
        chat_info_lines.append(f"  Title: {chat.title}")

    info_text = "\n".join(user_info_lines + chat_info_lines)
    await update.message.reply_text(info_text)


# ---------------------------------------------------------------------------
# Message type handlers
# ---------------------------------------------------------------------------

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles plain text messages (not commands).

    Reports the character count and word count of the message.
    """
    logger = logging.getLogger("commands_bot")
    user = update.effective_user
    text = update.message.text
    logger.info(f"Text from {user.first_name}: {text}")

    character_count = len(text)
    word_count = len(text.split())

    await update.message.reply_text(
        f"Got your message! ({character_count} chars, {word_count} words)"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles photo messages.

    Demonstrates accessing photo metadata. Telegram sends multiple sizes
    of the same photo — update.message.photo is a list of PhotoSize
    objects sorted by size. The last element is the largest resolution.
    """
    logger = logging.getLogger("commands_bot")
    user = update.effective_user

    # photo is a list of PhotoSize objects (different resolutions)
    photo_sizes = update.message.photo
    largest_photo = photo_sizes[-1]

    logger.info(
        f"Photo from {user.first_name}: "
        f"{largest_photo.width}x{largest_photo.height}, "
        f"file_id={largest_photo.file_id[:20]}..."
    )

    caption = update.message.caption or "no caption"
    await update.message.reply_text(
        f"Nice photo! ({largest_photo.width}x{largest_photo.height})\n"
        f"Caption: {caption}\n"
        f"Telegram sent {len(photo_sizes)} size(s) of this image."
    )


async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles sticker messages.

    Demonstrates accessing sticker metadata: emoji, set name, and type.
    """
    logger = logging.getLogger("commands_bot")
    user = update.effective_user
    sticker = update.message.sticker

    logger.info(
        f"Sticker from {user.first_name}: "
        f"emoji={sticker.emoji}, set={sticker.set_name}"
    )

    await update.message.reply_text(
        f"Sticker received!\n"
        f"Emoji: {sticker.emoji or 'N/A'}\n"
        f"Set: {sticker.set_name or 'N/A'}\n"
        f"Type: {sticker.type}"
    )


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles location messages.

    Demonstrates accessing latitude and longitude from a shared location.
    """
    logger = logging.getLogger("commands_bot")
    user = update.effective_user
    location = update.message.location

    logger.info(
        f"Location from {user.first_name}: "
        f"lat={location.latitude}, lon={location.longitude}"
    )

    await update.message.reply_text(
        f"Location received!\n"
        f"Latitude: {location.latitude}\n"
        f"Longitude: {location.longitude}"
    )


# ---------------------------------------------------------------------------
# Catch-all for unknown commands
# ---------------------------------------------------------------------------

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Catches any command not matched by previous handlers.

    IMPORTANT: This must be registered LAST among handlers, because
    python-telegram-bot checks handlers in registration order and
    stops at the first match. If this were registered first, it would
    swallow /start, /help, etc.
    """
    logger = logging.getLogger("commands_bot")
    command_text = update.message.text
    logger.info(f"Unknown command: {command_text}")

    await update.message.reply_text(
        f"Sorry, I don't know the command: {command_text}\n"
        "Type /help to see available commands."
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Builds the application, registers all handlers, and starts polling.

    Handler registration order:
    1. Command handlers (/start, /help, /caps, /info) — order among
       these doesn't matter since each matches a specific command string
    2. Message type handlers (text, photo, sticker, location) — each
       uses a different filter so they don't conflict
    3. Unknown command handler — MUST be last, catches unmatched /commands
    """
    logger = setup_logging()
    bot_token = load_bot_token()

    logger.info("Building bot application...")
    application = ApplicationBuilder().token(bot_token).build()

    # --- Command handlers ---
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("caps", caps_command))
    application.add_handler(CommandHandler("info", info_command))

    # --- Message type handlers ---
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))

    # --- Unknown command catch-all (must be last) ---
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    logger.info("Bot is starting... Press Ctrl+C to stop.")
    print("Bot is running. Try: /start, /help, /caps hello, /info")
    print("Also try sending a photo, sticker, or location.")

    application.run_polling()
    logger.info("Bot has stopped.")


if __name__ == "__main__":
    main()
