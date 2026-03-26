# Telegram Bot Api - Experimental Project

## Overview
This experiment explores the Telegram Bot API using the `python-telegram-bot`
library (v22.7). The goal is to learn all capabilities of the Bot API —
from basic messaging to payments, inline mode, and group management — to
become an expert for later use in larger projects.

## Technology Version
- Technology: Telegram Bot API
- Version: 9.5 (March 1, 2026)
- Python client version: python-telegram-bot 22.7
- Python requirement: 3.10+
- Version check date: 2026-03-26
- Note: Future sessions should check if a newer version is available
  and decide whether to use this version or upgrade.

## Documentation Sources
IMPORTANT: All scripts in this experiment MUST be based on the
fetched documentation stored in the docs/ folder, NOT on general
training knowledge. This ensures accuracy for the specific version.

- Official Bot API docs: https://core.telegram.org/bots/api
- Bot API changelog: https://core.telegram.org/bots/api-changelog
- python-telegram-bot GitHub: https://github.com/python-telegram-bot/python-telegram-bot
- python-telegram-bot docs: https://docs.python-telegram-bot.org/
- First Bot tutorial: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions---Your-first-Bot
- docs/ folder contents:
  - telegram-bot-api-reference.md (full API reference, all methods and types)
  - python-telegram-bot-library.md (library architecture, handlers, patterns)
  - api-changelog.md (recent API versions 9.1-9.5)

## Key Concepts
1. Bot lifecycle — token creation, polling vs webhooks, Application architecture
2. Handlers and filters — routing updates to callbacks based on type and content
3. Keyboards and inline buttons — interactive UI within Telegram chats
4. Conversation flows — multi-step stateful interactions using ConversationHandler
5. Media handling — sending/receiving photos, documents, audio, video
6. Inline mode — using the bot from any chat via @mention
7. Group/channel management — permissions, moderation, forum topics
8. Payments — invoices, shipping, pre-checkout, Telegram Stars
9. Persistence and scheduling — storing state, job queue for timed tasks
10. Error handling and best practices — logging, rate limiting, graceful shutdown

## Capabilities to Explore
1. Bot setup and echo bot (hello world)
2. Commands and message handlers
3. Inline keyboards and callback queries
4. Sending media (photos, documents, audio, video)
5. Receiving and downloading media
6. Conversation handlers (multi-step flows)
7. Bot commands menu and descriptions
8. Inline mode (use bot from any chat)
9. Group and channel management
10. Webhooks (vs polling)
11. Payments API
12. Custom filters and middleware
13. Error handling and persistence
14. Rate limiting and best practices

## Script Conventions
- Language: Python
- Naming: NN_descriptive_name.py (numbered for progression)
- Each script: Self-contained, runnable independently with `uv run NN_name.py`
- Logging: `print` for user-facing output + `logging` module with file handler
  for detailed logs (saved to `logs/` directory)
- Output: Both terminal and file output. Terminal for immediate feedback,
  files for artifacts (downloaded media, logs, data)
- run_all script: Yes — `run_all.py` with interactive selection menu
  to choose which script to run
- Docstring: Each script starts with a docstring explaining the concept
- Main guard: All scripts use `if __name__ == "__main__"`
- Bot token: Loaded from environment variable `TELEGRAM_BOT_TOKEN`
  or from a `.env` file (using python-dotenv)

## Progression Plan
1. `01_echo_bot.py` - Create bot, handle /start, echo messages back
2. `02_commands_and_handlers.py` - Multiple commands, message filters, argument parsing
3. `03_inline_keyboards.py` - Inline keyboard buttons, callback queries, button updates
4. `04_send_media.py` - Send photos, documents, audio, video, media groups
5. `05_receive_media.py` - Receive and download user-sent media files
6. `06_conversation_handler.py` - Multi-step conversation with states and fallbacks
7. `07_bot_commands_menu.py` - Set bot commands, descriptions, menu button
8. `08_inline_mode.py` - Inline queries, results, chosen inline results
9. `09_group_management.py` - Permissions, banning, promoting, forum topics
10. `10_webhooks.py` - Set up webhook-based update receiving
11. `11_payments.py` - Create invoices, handle shipping/checkout queries
12. `12_custom_filters.py` - Build custom filter classes, middleware patterns
13. `13_error_handling_persistence.py` - Error handlers, PicklePersistence, user/chat data
14. `14_rate_limiting_best_practices.py` - Rate limiter, job queue, graceful shutdown

## Prerequisites
- Python 3.10+
- Telegram account (to interact with the bot)
- Bot token from @BotFather:
  1. Open Telegram, search for @BotFather
  2. Send `/newbot`
  3. Choose a name (display name) and username (must end in `bot`)
  4. BotFather returns the token — save it
- Environment setup:
  ```bash
  # Create .env file in experiment directory
  echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env
  ```
- Python packages:
  ```bash
  uv add python-telegram-bot[all] python-dotenv
  ```
  The `[all]` extra installs: job-queue, webhooks, rate-limiter,
  callback-data, socks, http2, passport support.

## Integration Notes
- The echo bot pattern (script 01) is the foundation for any Telegram bot project
- Command and handler patterns (scripts 02-03) form the routing layer
  for any bot application
- Conversation handlers (script 06) can be extracted for multi-step
  user onboarding, form filling, or wizard-style interfaces
- Media handling (scripts 04-05) enables file processing pipelines
  (e.g., image processing bots, document conversion)
- Group management (script 09) enables moderation bots and community tools
- Payments (script 11) enables e-commerce and subscription-based bots
- Persistence (script 13) is essential for any stateful bot in production
- Webhook setup (script 10) is the production deployment pattern
  (polling is for development only)

## GitHub Repository
- Repository: https://github.com/TheRadMod/experiment-telegram-bot-api
- Visibility: public

## Learnings
<!-- As we build scripts and explore the technology, record key learnings here.
This section is a living document — update it after each script with:
- Gotchas, surprises, or non-obvious behavior discovered
- Patterns that worked well (or didn't)
- API quirks, version-specific behavior, or undocumented findings
- Performance observations or limits encountered
- Useful tips for future use in larger projects

Format: group by script or topic, keep entries concise. -->

### 01_echo_bot
- `ApplicationBuilder().token(token).build()` + `run_polling()` is the minimal
  boilerplate to get a bot running
- `filters.TEXT & ~filters.COMMAND` is the idiomatic way to catch plain text only
- `update.message.reply_text()` is a convenience shortcut that auto-targets
  the correct chat — prefer it over `context.bot.send_message(chat_id=...)`
- Handler registration order matters — first match wins
- `run_polling()` blocks the main thread until Ctrl+C

### 02_commands_and_handlers
- `context.args` splits everything after the command into a list of strings
  (e.g., `/caps hello world` -> `["hello", "world"]`)
- `update.message.photo` is a list of PhotoSize objects (different resolutions),
  `[-1]` gives the largest — Telegram always sends multiple sizes
- `filters.Sticker.ALL` catches all sticker types (static, animated, video)
- Unknown command handler must be registered last — first match wins
- `update.effective_user` and `update.effective_chat` are convenience accessors
  that work across all update types (messages, callbacks, etc.)

### 03_inline_keyboards
- `callback_query.answer()` MUST be called on every button press, otherwise
  Telegram shows a loading spinner for up to 30 seconds
- `callback_query.edit_message_text()` replaces message content + keyboard in-place
- Keyboard layout: each inner list = one row of buttons. Two buttons in the
  same list = side by side. Separate lists = stacked vertically.
- `callback_data` is limited to 64 bytes — use short prefixes for routing
- `context.user_data` is a per-user dict that persists for the bot's lifetime
  (in memory only, lost on restart — use Persistence for durability)
- Toggle pattern: flip state in user_data, re-render keyboard with new labels
- One `CallbackQueryHandler` can handle all buttons — route inside the callback
  by inspecting `query.data`

## Status
- Created: 2026-03-26
- Status: Learning
