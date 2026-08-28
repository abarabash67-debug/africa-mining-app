import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector

from config import BOT_TOKEN
from handlers import start, production, communicator, vip_chat  # ← ДОБАВИЛИ VIP_CHAT

dp = Dispatcher()
dp.include_router(start.router)
dp.include_router(production.router)
dp.include_router(communicator.router)
dp.include_router(vip_chat.router)  # ← ДОБАВИЛИ

async def main():
    proxy_connector = ProxyConnector.from_url("socks5://127.0.0.1:10808")
    client_session = aiohttp.ClientSession(connector=proxy_connector)
    session = AiohttpSession()
    session._session = client_session
    
    global bot
    bot = Bot(token=BOT_TOKEN, session=session)
    
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())