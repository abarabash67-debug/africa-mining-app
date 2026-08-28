from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from datetime import datetime
from config import WHITE_LIST
from keyboards import get_communicator_menu, get_recipients_keyboard
from utils import load_messages, save_messages

router = Router()
USER_CONTEXT = {}

@router.message(F.text.in_(["💬 Коммуникатор", "💬 Communicator", "💬 Communicateur"]))
async def communicator_menu(message: Message):
    user_id = str(message.from_user.id)
    if user_id not in WHITE_LIST:
        return
    lang = WHITE_LIST[user_id]["lang"]
    await message.answer("📨 **Коммуникатор**", reply_markup=get_communicator_menu(lang))

@router.message(F.text.in_(["✉️ Новое", "✉️ New", "✉️ Nouveau"]))
async def new_message(message: Message):
    user_id = str(message.from_user.id)
    if user_id not in WHITE_LIST:
        return
    lang = WHITE_LIST[user_id]["lang"]
    await message.answer("✉️ **Выберите получателя:**", reply_markup=get_recipients_keyboard(lang, user_id))

@router.callback_query(F.data.startswith("recipient_"))
async def recipient_selected(callback: CallbackQuery):
    recipient_id = callback.data.split("_")[1]
    sender_id = str(callback.from_user.id)
    
    if sender_id not in WHITE_LIST:
        await callback.answer("❌ Доступ запрещен")
        return
    
    await callback.message.edit_text("✉️ **Напишите сообщение:**", reply_markup=None)
    USER_CONTEXT[callback.from_user.id] = {"recipient": recipient_id}
    await callback.answer()

@router.message(F.text)
async def handle_text_message(message: Message):
    user_id = str(message.from_user.id)
    if message.text.startswith('/') or user_id not in USER_CONTEXT:
        return
    
    recipient_id = USER_CONTEXT[user_id]["recipient"]
    sender_name = WHITE_LIST[user_id]["name"]
    
    messages = load_messages()
    if recipient_id not in messages:
        messages[recipient_id] = []
    
    messages[recipient_id].append({
        "id": str(datetime.now().timestamp()),
        "from": user_id,
        "from_name": sender_name,
        "text": message.text,
        "timestamp": datetime.now().isoformat(),
        "read": False
    })
    save_messages(messages)
    
    try:
        await bot.send_message(recipient_id, f"📨 **От {sender_name}:**\n{message.text[:100]}...")
    except:
        pass
    
    await message.answer("✅ Отправлено", reply_markup=get_communicator_menu(WHITE_LIST[user_id]["lang"]))
    del USER_CONTEXT[user_id]