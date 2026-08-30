from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime

from config import WHITE_LIST
from utils import load_vip_messages, save_vip_messages

router = Router()

@router.message(F.text.in_(["💬 VIP-Чат", "💬 VIP Chat", "💬 Chat VIP"]))
async def vip_chat_menu(message: Message):
    user_id = str(message.from_user.id)
    if user_id not in WHITE_LIST:
        return
    
    await message.answer(
        "💬 **VIP-Чат**\n\n"
        "Напишите сообщение, и оно будет отправлено всем топ-менеджерам."
    )


@router.message(F.text)
async def handle_vip_message(message: Message):
    user_id = str(message.from_user.id)
    
    if message.text.startswith('/') or user_id not in WHITE_LIST:
        return
    
    # Проверяем, что это сообщение в VIP-чате (не из других хендлеров)
    if not message.text or len(message.text) > 200:
        return
    
    sender_name = WHITE_LIST[user_id].get("name", "Пользователь")
    
    # Сохраняем сообщение
    vip_messages = load_vip_messages()
    vip_messages.append({
        "id": str(datetime.now().timestamp()),
        "from": user_id,
        "from_name": sender_name,
        "text": message.text,
        "timestamp": datetime.now().isoformat()
    })
    save_vip_messages(vip_messages)
    
    # Отправляем всем топ-менеджерам
    from bot import bot
    
    sent_count = 0
    for uid, data in WHITE_LIST.items():
        if uid != user_id and data.get("role") in ["CEO", "MINE_MANAGER", "ASSISTANT"]:
            try:
                await bot.send_message(
                    uid,
                    f"💬 **VIP-сообщение от {sender_name}:**\n\n{message.text}"
                )
                sent_count += 1
            except Exception as e:
                print(f"Не удалось отправить VIP-сообщение {uid}: {e}")
    
    await message.answer(f"✅ Сообщение отправлено {sent_count} топ-менеджерам.")