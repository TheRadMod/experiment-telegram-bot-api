"""
03_inline_keyboards.py - Inline Keyboards and Callback Queries

Demonstrates interactive inline keyboards within Telegram messages:
- Building inline keyboards with InlineKeyboardMarkup / InlineKeyboardButton
- Handling button presses via CallbackQueryHandler
- callback_query.answer() to dismiss the loading spinner
- Editing messages in-place after button press (edit_message_text)
- Multi-row keyboard layouts
- Dynamic keyboards: toggle buttons that change state on press
- Submenu navigation with a "Back" button

Usage:
    uv run 03_inline_keyboards.py

Then in Telegram:
    /menu   -> shows main menu with interactive buttons
    Press buttons to navigate submenus and toggle settings.
Press Ctrl+C to stop.
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    """
    Configures dual logging: terminal (INFO) and file (DEBUG).
    Logs saved to logs/03_inline_keyboards.log.
    """
    logs_directory = Path(__file__).parent / "logs"
    logs_directory.mkdir(exist_ok=True)
    log_file_path = logs_directory / "03_inline_keyboards.log"

    logger = logging.getLogger("keyboard_bot")
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
# Keyboard builders
# ---------------------------------------------------------------------------

def build_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Builds the main menu keyboard with 3 buttons in separate rows.

    Each button has:
    - text: what the user sees
    - callback_data: string sent to the bot when pressed (max 64 bytes)

    Layout:
        [ Status  ]
        [ Settings ]
        [ About   ]
    """
    keyboard = [
        [InlineKeyboardButton("Status", callback_data="menu_status")],
        [InlineKeyboardButton("Settings", callback_data="menu_settings")],
        [InlineKeyboardButton("About", callback_data="menu_about")],
    ]
    return InlineKeyboardMarkup(keyboard)


def build_settings_keyboard(notifications_on: bool, dark_mode_on: bool) -> InlineKeyboardMarkup:
    """
    Builds a settings submenu with toggle buttons.

    Toggle buttons display current state and flip it when pressed.
    The callback_data encodes the action (which setting to toggle).

    Layout:
        [ Notifications: ON/OFF ]
        [ Dark Mode: ON/OFF     ]
        [ << Back               ]
    """
    notifications_label = "Notifications: ON" if notifications_on else "Notifications: OFF"
    dark_mode_label = "Dark Mode: ON" if dark_mode_on else "Dark Mode: OFF"

    keyboard = [
        [InlineKeyboardButton(notifications_label, callback_data="toggle_notifications")],
        [InlineKeyboardButton(dark_mode_label, callback_data="toggle_dark_mode")],
        [InlineKeyboardButton("<< Back", callback_data="menu_back")],
    ]
    return InlineKeyboardMarkup(keyboard)


def build_confirm_keyboard() -> InlineKeyboardMarkup:
    """
    Builds a simple yes/no confirmation keyboard.

    Demonstrates placing multiple buttons in a single row
    by putting them in the same inner list.

    Layout:
        [ Yes ] [ No ]
    """
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="confirm_yes"),
            InlineKeyboardButton("No", callback_data="confirm_no"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /start — sends a welcome message with a hint to try /menu.
    """
    logger = logging.getLogger("keyboard_bot")
    logger.info(f"/start from {update.effective_user.first_name}")

    await update.message.reply_text(
        "Welcome! This bot demonstrates inline keyboards.\n"
        "Type /menu to see an interactive menu."
    )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /menu — sends a message with the main menu inline keyboard.

    Initializes default settings in context.user_data if not already set.
    context.user_data persists for the duration of the bot process
    (per user), making it ideal for tracking toggle states.
    """
    logger = logging.getLogger("keyboard_bot")
    logger.info(f"/menu from {update.effective_user.first_name}")

    # Initialize settings defaults in user_data if first time
    if "notifications_on" not in context.user_data:
        context.user_data["notifications_on"] = True
    if "dark_mode_on" not in context.user_data:
        context.user_data["dark_mode_on"] = False

    keyboard = build_main_menu_keyboard()
    await update.message.reply_text("Main Menu:", reply_markup=keyboard)


# ---------------------------------------------------------------------------
# Callback query handler
# ---------------------------------------------------------------------------

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Central handler for all inline keyboard button presses.

    When a user presses an inline button, Telegram sends a CallbackQuery
    with the callback_data string. This function:
    1. Calls query.answer() to dismiss the loading spinner on the button
    2. Routes to the correct action based on the callback_data prefix
    3. Edits the original message in-place (text + keyboard)

    Key concepts:
    - query.answer() MUST be called, otherwise Telegram shows a loading
      spinner on the button for up to 30 seconds
    - query.answer(text="...") shows a brief toast notification to the user
    - query.edit_message_text() replaces the message content and keyboard
    """
    query = update.callback_query
    logger = logging.getLogger("keyboard_bot")
    logger.info(f"Button press: '{query.data}' from {update.effective_user.first_name}")

    # Always answer the callback query first to dismiss the spinner
    await query.answer()

    callback_data = query.data

    # --- Main menu buttons ---
    if callback_data == "menu_status":
        await handle_status(query, context)

    elif callback_data == "menu_settings":
        await handle_settings(query, context)

    elif callback_data == "menu_about":
        await handle_about(query)

    # --- Settings toggles ---
    elif callback_data == "toggle_notifications":
        await handle_toggle_notifications(query, context)

    elif callback_data == "toggle_dark_mode":
        await handle_toggle_dark_mode(query, context)

    # --- Navigation ---
    elif callback_data == "menu_back":
        await handle_back_to_menu(query)

    # --- Confirmation buttons ---
    elif callback_data == "confirm_yes":
        await query.edit_message_text("Confirmed!")

    elif callback_data == "confirm_no":
        await query.edit_message_text("Cancelled.")

    else:
        logger.warning(f"Unknown callback_data: {callback_data}")


async def handle_status(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Shows bot status info and a confirmation prompt.

    Demonstrates replacing the keyboard entirely with a different one.
    """
    notifications_status = "ON" if context.user_data.get("notifications_on", True) else "OFF"
    dark_mode_status = "ON" if context.user_data.get("dark_mode_on", False) else "OFF"

    status_text = (
        "Bot Status:\n\n"
        f"  Notifications: {notifications_status}\n"
        f"  Dark Mode: {dark_mode_status}\n"
        f"  Uptime: Running\n\n"
        "Reset settings?"
    )
    await query.edit_message_text(
        text=status_text,
        reply_markup=build_confirm_keyboard(),
    )


async def handle_settings(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Shows the settings submenu with toggle buttons.

    Reads current toggle states from context.user_data and passes
    them to the keyboard builder so button labels reflect current state.
    """
    notifications_on = context.user_data.get("notifications_on", True)
    dark_mode_on = context.user_data.get("dark_mode_on", False)

    await query.edit_message_text(
        text="Settings:\nTap a toggle to change it.",
        reply_markup=build_settings_keyboard(notifications_on, dark_mode_on),
    )


async def handle_about(query) -> None:
    """
    Shows about info with a Back button.
    """
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("<< Back", callback_data="menu_back")]
    ])
    await query.edit_message_text(
        text=(
            "About:\n\n"
            "This bot demonstrates inline keyboards and callback queries.\n"
            "Part of the Telegram Bot API learning experiment.\n\n"
            "Script: 03_inline_keyboards.py"
        ),
        reply_markup=keyboard,
    )


async def handle_toggle_notifications(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Toggles the notifications setting and refreshes the settings keyboard.

    Demonstrates the pattern: flip state in user_data, then re-render
    the keyboard with updated labels. The user sees the button text
    change instantly without leaving the settings submenu.
    """
    logger = logging.getLogger("keyboard_bot")

    # Flip the toggle
    current_value = context.user_data.get("notifications_on", True)
    new_value = not current_value
    context.user_data["notifications_on"] = new_value
    logger.info(f"Notifications toggled: {current_value} -> {new_value}")

    # Re-render settings keyboard with updated state
    dark_mode_on = context.user_data.get("dark_mode_on", False)
    await query.edit_message_text(
        text="Settings:\nTap a toggle to change it.",
        reply_markup=build_settings_keyboard(new_value, dark_mode_on),
    )


async def handle_toggle_dark_mode(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Toggles the dark mode setting and refreshes the settings keyboard.
    Same pattern as handle_toggle_notifications.
    """
    logger = logging.getLogger("keyboard_bot")

    current_value = context.user_data.get("dark_mode_on", False)
    new_value = not current_value
    context.user_data["dark_mode_on"] = new_value
    logger.info(f"Dark mode toggled: {current_value} -> {new_value}")

    notifications_on = context.user_data.get("notifications_on", True)
    await query.edit_message_text(
        text="Settings:\nTap a toggle to change it.",
        reply_markup=build_settings_keyboard(notifications_on, new_value),
    )


async def handle_back_to_menu(query) -> None:
    """
    Returns to the main menu by editing the message back to the
    main menu text and keyboard.
    """
    await query.edit_message_text(
        text="Main Menu:",
        reply_markup=build_main_menu_keyboard(),
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Builds the application, registers handlers, and starts polling.

    Two handler types are used:
    1. CommandHandler — for /start and /menu slash commands
    2. CallbackQueryHandler — for ALL inline button presses

    CallbackQueryHandler catches every callback query. Routing to
    specific actions happens inside button_callback() based on
    the callback_data string.
    """
    logger = setup_logging()
    bot_token = load_bot_token()

    logger.info("Building bot application...")
    application = ApplicationBuilder().token(bot_token).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("menu", menu_command))

    # Single callback query handler for all button presses
    application.add_handler(CallbackQueryHandler(button_callback))

    logger.info("Bot is starting... Press Ctrl+C to stop.")
    print("Bot is running. Type /menu in Telegram to see the inline keyboard.")

    application.run_polling()
    logger.info("Bot has stopped.")


if __name__ == "__main__":
    main()
