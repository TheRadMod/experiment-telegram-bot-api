# Telegram Bot API Reference (v9.5 - March 2026)

Source: https://core.telegram.org/bots/api

## Overview

The Telegram Bot API is an HTTP-based interface for developers building bots. Bots receive a unique authentication token from BotFather and make HTTPS requests to `https://api.telegram.org/bot<token>/METHOD_NAME`.

## Authentication & Request Methods

**Token Format:** `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

**Supported HTTP Methods:** GET, POST

**Parameter Passing Options:**
- URL query strings
- application/x-www-form-urlencoded
- application/json (except file uploads)
- multipart/form-data (for file uploads)

**Response Format:** JSON with required `ok` boolean field and optional `description` and `error_code` fields.

## Getting Updates

### Long Polling (getUpdates)
Retrieves incoming updates. Parameters include `offset`, `limit` (1-100, default 100), `timeout`, and `allowed_updates`.

### Webhooks (setWebhook)
Configure HTTPS endpoint to receive updates. Supports custom certificates, IP addresses, max connections (1-100, default 40), and secret tokens.

**Supported Webhook Ports:** 443, 80, 88, 8443

## Core Types

### User Object
- `id`: Unique identifier (64-bit)
- `is_bot`: Boolean
- `first_name`, `last_name`, `username`: Strings
- `language_code`: IETF language tag
- `is_premium`, `has_topics_enabled`: Booleans

### Chat Object
- `id`: Unique identifier
- `type`: "private", "group", "supergroup", or "channel"
- `title`, `username`, `first_name`, `last_name`: Optional strings
- `is_forum`, `is_direct_messages`: Optional booleans

### Message Object
Core messaging fields:
- `message_id`: Integer (0 if scheduled)
- `message_thread_id`: Optional, for forum topics
- `from`: Sender User object
- `date`: Unix timestamp
- `chat`: Chat object
- `text`: Message content
- `entities`: Array of MessageEntity objects
- `reply_to_message`: Message object

**Media Fields:**
- `animation`, `audio`, `document`, `photo`, `video`, `video_note`, `voice`
- `sticker`, `game`, `poll`, `venue`, `location`, `contact`, `dice`

### MessageEntity Object
Types: "mention", "hashtag", "cashtag", "bot_command", "url", "email", "phone_number", "bold", "italic", "underline", "strikethrough", "spoiler", "blockquote", "expandable_blockquote", "code", "pre", "text_link", "text_mention", "custom_emoji", "date_time"

### Update Object
Contains exactly one update type:
- `message`, `edited_message`, `channel_post`, `edited_channel_post`
- `business_message`, `edited_business_message`, `deleted_business_messages`
- `message_reaction`, `message_reaction_count`
- `inline_query`, `chosen_inline_result`
- `callback_query`
- `shipping_query`, `pre_checkout_query`, `purchased_paid_media`
- `poll`, `poll_answer`
- `my_chat_member`, `chat_member`, `chat_join_request`

## Message Sending Methods

### sendMessage
- `chat_id`, `text` (1-4096 chars), `parse_mode` ("HTML", "Markdown", "MarkdownV2")
- `entities`, `link_preview_options`, `reply_markup`, `reply_parameters`

### sendPhoto
- `chat_id`, `photo` (InputFile or file_id), `caption` (0-1024 chars)
- `has_spoiler`, `show_caption_above_media`

### sendVideo
- `chat_id`, `video`, `duration`, `width`, `height`, `thumbnail`
- `caption`, `supports_streaming`, `has_spoiler`

### sendAnimation
Similar to sendVideo with animation-specific parameters.

### sendAudio
- `chat_id`, `audio`, `duration`, `performer`, `title`, `caption`

### sendDocument
- `chat_id`, `document`, `thumbnail`, `caption`, `disable_content_type_detection`

### sendVoice
- `chat_id`, `voice`, `caption`, `duration`

### sendVideoNote
- `chat_id`, `video_note`, `duration`, `length`, `thumbnail`

### sendMediaGroup
- `chat_id`, `media` (array of InputMedia types)

### sendLocation
- `chat_id`, `latitude`, `longitude`, `horizontal_accuracy`, `live_period`

### sendVenue
- `chat_id`, `latitude`, `longitude`, `title`, `address`

### sendContact
- `chat_id`, `phone_number`, `first_name`, `last_name`

### sendPoll
- `chat_id`, `question`, `options` (2-10 InputPollOption)
- `is_anonymous`, `type` ("quiz"/"regular"), `correct_option_id`

### sendDice
- `chat_id`, `emoji` (one of: dice, darts, bowling, basketball, football, slot machine)

### sendSticker
- `chat_id`, `sticker` (InputFile, file_id, or URL)

### sendInvoice
- `chat_id`, `title`, `description`, `payload`, `provider_token`
- `currency`, `prices`, `need_name`, `need_phone_number`, etc.

### sendPaidMedia
- `chat_id`, `star_count` (1-25000), `media` (array of InputPaidMedia)

### sendMessageDraft (API 9.5)
Stream partial messages while being generated. Available to all bots.

## Message Editing & Deletion

- `editMessageText`, `editMessageCaption`, `editMessageMedia`, `editMessageReplyMarkup`
- `deleteMessage`, `deleteMessages` (1-100 messages)
- `forwardMessage`, `forwardMessages`, `copyMessage`, `copyMessages`

## Chat Management

- `getChat`, `getChatAdministrators`, `getChatMemberCount`, `getChatMember`
- `leaveChat`, `setChatTitle`, `setChatDescription`, `setChatPhoto`, `deleteChatPhoto`
- `pinChatMessage`, `unpinChatMessage`, `unpinAllChatMessages`
- `setChatPermissions`, `setChatAdministratorCustomTitle`

## User & Member Management

- `getMe` — Returns bot information
- `banChatMember`, `unbanChatMember`, `restrictChatMember`, `promoteChatMember`
- `setChatMemberTag` (API 9.5)

## Forum Topics

- `createForumTopic`, `editForumTopic`, `closeForumTopic`, `reopenForumTopic`
- `deleteForumTopic`, `unpinAllForumTopicMessages`

## Bot Profile

- `setMyName`/`getMyName`, `setMyDescription`/`getMyDescription`
- `setMyShortDescription`/`getMyShortDescription`
- `setMyProfilePhoto`/`removeMyProfilePhoto`

## Commands & Menus

- `setMyCommands`, `getMyCommands`, `deleteMyCommands`
- `setChatMenuButton`, `getChatMenuButton`

## Inline Mode

### answerInlineQuery
- `inline_query_id`, `results` (0-50 InlineQueryResult objects)
- `cache_time`, `is_personal`, `next_offset`, `button`

Result types: Article, Photo, Gif, Mpeg4Gif, Video, Audio, Document, Location, Venue, Contact, Game, and Cached variants.

## Payments

- `sendInvoice`, `answerShippingQuery`, `answerPreCheckoutQuery`

## Stickers

- `sendSticker`, `getStickerSet`, `getCustomEmojiStickers`
- `uploadStickerFile`, `createNewStickerSet`, `addStickerToSet`
- `setStickerPositionInSet`, `deleteStickerFromSet`, `replaceStickerInSet`

## Games

- `sendGame`, `setGameScore`, `getGameHighScores`

## Gifts

- `getAvailableGifts`, `getBusinessAccountGifts`, `getUserGifts`, `getChatGifts`

## Keyboard & Button Objects

### InlineKeyboardMarkup / InlineKeyboardButton
- `text`, `url`, `callback_data`, `web_app`, `switch_inline_query`, `pay`, `copy_text`

### ReplyKeyboardMarkup / KeyboardButton
- `text`, `request_users`, `request_chat`, `request_contact`, `request_location`, `request_poll`

### ReplyKeyboardRemove / ForceReply

## File Size Limits

**Cloud Bot API:** Download: No limit, Upload: Max 50 MB
**Local Bot API Server:** Download: No limit, Upload: Max 2000 MB

## Error Handling

Responses include `ok` (boolean), `result` (if ok=true), `description` (error message), `error_code`, and `parameters` (ResponseParameters with recovery hints).
