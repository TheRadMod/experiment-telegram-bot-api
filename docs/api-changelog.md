# Telegram Bot API Changelog (Recent)

Source: https://core.telegram.org/bots/api-changelog

## Bot API 9.5 (March 1, 2026)
- MessageEntity type "date_time" for displaying formatted dates/times
- `sendMessageDraft` method available to ALL bots (previously limited)
- Tag management: `setChatMemberTag` method, `sender_tag` field in Message
- `can_manage_tags` capability for administrators
- `iconCustomEmojiId` for bottom buttons in Web Apps

## Bot API 9.4 (February 9, 2026)
- Bots with Telegram Premium can use custom emoji in direct messages
- Forum topics in private chats
- Button styling: `style` and `icon_custom_emoji_id` fields
- Profile photo management: `setMyProfilePhoto`, `removeMyProfilePhoto`
- Video quality information retrieval
- User profile audios fetching
- Gift rarity and burn status

## Bot API 9.3 (December 31, 2025)
- Forum topics in private chats with `has_topics_enabled`
- `sendMessageDraft` for streaming partial messages (initially limited)
- Checklist support with `sendChecklist` capabilities
- Gift system enhancements (colors, backgrounds, variants)
- Channel direct messages support
- Suggested posts functionality
- Increased paid media price limit to 25,000 Telegram Stars

## Bot API 9.2 (August 15, 2025)
- Checklist task completion tracking
- Direct messages in channels with topic handling
- `approveSuggestedPost` and `declineSuggestedPost` methods

## Bot API 9.1 (July 3, 2025)
- `sendChecklist` and `editMessageChecklist` methods
- Increased maximum poll options to 12
- `getMyStarBalance` for checking bot Telegram Stars balance
