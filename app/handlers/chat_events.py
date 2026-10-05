# app/handlers/chat_events.py

import asyncio
from aiogram import Router, Bot
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER
from aiogram.types import ChatMemberUpdated
from app import ui_text

router = Router()

async def auto_delete_message(bot: Bot, chat_id: int, message_id: int, delay: int = 120):
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass

@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> MEMBER))
async def handle_new_member(event: ChatMemberUpdated, bot: Bot):
    user = event.new_chat_member.user
    chat = event.chat

    if user.is_bot:
        return

    welcome_msg_text = ui_text.WELCOME_TEMPLATE.format(
        username=user.first_name,
        chat_title=chat.title
    )

    try:
        sent_message = await bot.send_message(
            chat_id=chat.id,
            text=welcome_msg_text,
            parse_mode="Markdown"
        )
        
        asyncio.create_task(
            auto_delete_message(bot, chat.id, sent_message.message_id, delay=120)
        )
        
    except Exception as e:
        print(f"Failed to send welcome message: {e}")