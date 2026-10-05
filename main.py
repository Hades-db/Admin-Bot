import asyncio
from aiogram import Bot, Dispatcher
from app.config import TOKEN
from app.database.db_manager import init_db
from app.handlers import chat_events, anti_spam


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    await init_db()

    dp.include_router(chat_events.router)
    dp.include_router(anti_spam.router)

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        print("Admin-Bot started successfully!")
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        print("\nBot stopped manually.")
    except Exception as ex:
        print(f"Critical Bot Exception: {ex}")
    finally:
        await bot.session.close()
        print("Bot completely shut down.")

if __name__ == "__main__":
    asyncio.run(main())