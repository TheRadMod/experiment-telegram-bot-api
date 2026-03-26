"""
01_echo_bot.py - Hello World Telegram Bot

Demonstrates the most basic Telegram bot functionality:
- Loading bot token securely from .env file
- Handling the /start command
- Echoing back any text message the user sends
- Setting up dual logging (terminal + file)

This is the foundation pattern for all subsequent scripts.

Usage:
    uv run 01_echo_bot.py

Then open Telegram, find your bot, and send /start or any text message.
Press Ctrl+C in the terminal to stop the bot.
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
    Configures dual logging: terminal output and file output.

    - Terminal (StreamHandler): INFO level, human-readable format
    - File (FileHandler): DEBUG level, detailed format with timestamps
      Logs are saved to logs/01_echo_bot.log
    """
    logs_directory = Path(__file__).parent / "logs"
    logs_directory.mkdir(exist_ok=True)
    log_file_path = logs_directory / "01_echo_bot.log"

    logger = logging.getLogger("echo_bot")
    logger.setLevel(logging.DEBUG)

    # Terminal handler — INFO level, concise format
    terminal_handler = logging.StreamHandler()
    terminal_handler.setLevel(logging.INFO)
    terminal_format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    terminal_handler.setFormatter(terminal_format)

    # File handler — DEBUG level, detailed format
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(funcName)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(file_format)

    logger.addHandler(terminal_handler)
    logger.addHandler(file_handler)

    return logger


# ---------------------------------------------------------------------------
# Environment setup
# ---------------------------------------------------------------------------

def load_bot_token() -> str:
    """
    Loads the Telegram bot token from the .env file.

    Looks for TELEGRAM_BOT_TOKEN in the .env file located in the same
    directory as this script. Exits with a clear error if not found.
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
# Handler callbacks
# ---------------------------------------------------------------------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /start command.

    Sends a welcome message explaining what the bot does.
    This is the first thing a user sees when they interact with the bot.
    """
    logger = logging.getLogger("echo_bot")

    user = update.effective_user
    logger.info(f"/start command received from {user.first_name} (id: {user.id})")

    welcome_message = (
        f"Hello {user.first_name}! 👋\n\n"
        "I'm an echo bot. Send me any text message and I'll send it right back.\n\n"
        "This bot is part of a Telegram Bot API learning experiment."
    )
    await update.message.reply_text(welcome_message)


async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Echoes back any text message the user sends.

    Uses the reply_text convenience shortcut on the message object,
    which automatically sends to the correct chat and quotes the
    original message.
    """
    logger = logging.getLogger("echo_bot")

    user_text = update.message.text
    user = update.effective_user
    logger.info(f"Message from {user.first_name} (id: {user.id}): {user_text}")

    await update.message.reply_text(f"You said: {user_text}")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Creates the Application, registers handlers, and starts polling.

    Handler registration order matters:
    1. CommandHandler for /start — catches the /start command
    2. MessageHandler for text — catches all non-command text messages

    The filters.TEXT & ~filters.COMMAND combination ensures we only
    echo plain text, not commands like /start.
    """
    logger = setup_logging()
    bot_token = load_bot_token()

    logger.info("Building bot application...")

    # Build the application using the builder pattern
    application = ApplicationBuilder().token(bot_token).build()

    # Register handlers
    # 1. /start command handler
    application.add_handler(CommandHandler("start", start_command))

    # 2. Text message handler (excludes commands)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message)
    )

    logger.info("Bot is starting... Press Ctrl+C to stop.")
    print("Bot is running. Open Telegram and send a message to your bot.")

    # Start polling — this blocks until Ctrl+C
    application.run_polling()

    logger.info("Bot has stopped.")


if __name__ == "__main__":
    main()
