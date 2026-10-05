# app/handlers/anti_spam.py

import time
from aiogram import Router, Bot, F
from aiogram.types import Message, ChatPermissions
from app import ui_text
from app.database.db_manager import add_warn

router = Router()

STOP_WORDS = ["casino", "казино", "crypto", "заработок", "ставь"]

def is_spam(text: str) -> bool:
    if not text:
        return False
    
    text_lower = text.lower()
    
    if "http://" in text_lower or "https://" in text_lower or "t.me/" in text_lower:
        return True
        
    for word in STOP_WORDS:
        if word in text_lower:
            return True
            
    return False

@router.message(F.chat.type.in_({"group", "supergroup"}))
async def monitor_chat(message: Message, bot: Bot):
    if message.from_user.is_bot:
        return

    try:
        member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        if member.status in ["creator", "administrator"]:
            return
    except Exception:
        pass

    if is_spam(message.text):
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_mention = message.from_user.mention_html()

        try:
            await message.delete()
        except Exception:
            pass

        warns_count = await add_warn(user_id, chat_id)

        mute_permissions = ChatPermissions(can_send_messages=False)

        try:
            if warns_count == 1:
                until_date = int(time.time()) + 120
                await bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=mute_permissions,
                    until_date=until_date
                )
                
                await bot.send_message(
                    chat_id=chat_id,
                    text=ui_text.WARN_TIER_1.format(user_mention=user_mention),
                    parse_mode="HTML"
                )

            elif warns_count == 2:
                until_date = int(time.time()) + 1800
                await bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=mute_permissions,
                    until_date=until_date
                )
                
                await bot.send_message(
                    chat_id=chat_id,
                    text=ui_text.WARN_TIER_2.format(user_mention=user_mention),
                    parse_mode="HTML"
                )

            else:
                await bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
                
                await bot.send_message(
                    chat_id=chat_id,
                    text=ui_text.WARN_TIER_3.format(user_mention=user_mention),
                    parse_mode="HTML"
                )

        except Exception as e:
            print(f"Failed to punish user {user_id}: {e}")