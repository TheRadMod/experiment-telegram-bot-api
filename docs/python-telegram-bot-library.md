# python-telegram-bot Library Reference (v22.7)

Source: https://github.com/python-telegram-bot/python-telegram-bot

## Overview

Pure Python, asynchronous wrapper for the Telegram Bot API.
Supports Bot API 9.5. Requires Python 3.10+.

## Installation

```bash
pip install python-telegram-bot --upgrade
# Or with uv:
uv add python-telegram-bot
```

### Optional Dependencies
- `[passport]`: cryptography for Telegram Passport
- `[socks]`: SOCKS5 proxy support
- `[http2]`: HTTP/2 protocol support
- `[rate-limiter]`: aiolimiter for rate limiting
- `[webhooks]`: tornado for webhook functionality
- `[callback-data]`: cachetools for advanced callback handling
- `[job-queue]`: APScheduler for scheduled tasks
- `[all]`: All optional dependencies
- `[ext]`: All telegram.ext related packages

## Architecture

Two main components:
1. **Pure API Layer** (`telegram`): Direct access to Telegram Bot API
2. **Extensions** (`telegram.ext`): High-level abstractions

### Core Classes (telegram.ext)
- **Application**: Main entry point, coordinates updater, queue, and handlers
- **Updater**: Continuously retrieves messages from Telegram
- **Handlers**: Route updates to callback functions
- **ContextTypes**: Provides context object to callbacks

## Quick Start

```python
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()
    application.add_handler(CommandHandler('start', start))
    application.run_polling()
```

## Handler Types

### CommandHandler
Respond to slash commands like `/start`, `/help`:
```python
CommandHandler('start', callback_function)
```

### MessageHandler
Handle messages matching specific filters:
```python
from telegram.ext import filters, MessageHandler
MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
```

### CallbackQueryHandler
Handle inline keyboard button presses:
```python
from telegram.ext import CallbackQueryHandler
CallbackQueryHandler(button_callback)
```

### InlineQueryHandler
Handle inline mode queries:
```python
from telegram.ext import InlineQueryHandler
InlineQueryHandler(inline_callback)
```

### ConversationHandler
Multi-step conversation flows with states:
```python
from telegram.ext import ConversationHandler
ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        STATE_1: [MessageHandler(filters.TEXT, step_one)],
        STATE_2: [MessageHandler(filters.TEXT, step_two)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
```

## Filter System

Combine filters using operators:
- `&` (AND): `filters.TEXT & filters.Entity("url")`
- `|` (OR): `filters.PHOTO | filters.VIDEO`
- `~` (NOT): `~filters.COMMAND`

Common filters:
- `filters.TEXT`, `filters.COMMAND`, `filters.PHOTO`, `filters.VIDEO`
- `filters.Document`, `filters.AUDIO`, `filters.VOICE`
- `filters.Entity("mention")`, `filters.Regex("pattern")`
- `filters.ChatType.PRIVATE`, `filters.ChatType.GROUP`

## Context Object

Every callback receives `(update, context)`:
- `context.bot`: The Bot instance
- `context.args`: Command arguments as list
- `context.user_data`: Per-user persistent dict
- `context.chat_data`: Per-chat persistent dict
- `context.bot_data`: Global persistent dict

## Convenience Shortcuts

Messages have shortcut methods:
```python
# Instead of:
await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello")
# Use:
await update.message.reply_text("Hello")
```

## Application Lifecycle

```python
application = ApplicationBuilder().token('TOKEN').build()

# Register handlers
application.add_handler(handler1)
application.add_handler(handler2)

# Start polling (blocks until Ctrl+C)
application.run_polling()

# Or for webhooks:
application.run_webhook(
    listen="0.0.0.0",
    port=8443,
    secret_token="...",
    webhook_url="https://your-domain.com/webhook"
)
```

## Job Queue

Schedule recurring tasks:
```python
async def callback(update, context):
    context.job_queue.run_once(alarm, when=10, chat_id=chat_id)
    context.job_queue.run_repeating(check, interval=60, first=10)
```

## Persistence

Store user_data, chat_data, bot_data across restarts:
```python
from telegram.ext import PicklePersistence
persistence = PicklePersistence(filepath="bot_data")
application = ApplicationBuilder().token('TOKEN').persistence(persistence).build()
```

## Error Handling

```python
async def error_handler(update, context):
    logger.error(f"Exception: {context.error}")

application.add_error_handler(error_handler)
```

## Async Patterns

All callbacks are async functions:
```python
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Response")
```
