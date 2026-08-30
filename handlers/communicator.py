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
    USER_CONTEXT[sender_id] = {"recipient": recipient_id}
    await callback.answer()


@router.message(F.text)
async def handle_text_message(message: Message):
    user_id = str(message.from_user.id)
    
    # Проверяем, что пользователь в контексте и это не команда
    if message.text.startswith('/') or user_id not in USER_CONTEXT:
        return
    
    # Проверяем, что пользователь есть в WHITE_LIST
    if user_id not in WHITE_LIST:
        await message.answer("❌ Доступ запрещен")
        return
    
    recipient_id = USER_CONTEXT[user_id]["recipient"]
    sender_name = WHITE_LIST[user_id].get("name", "Пользователь")
    lang = WHITE_LIST[user_id].get("lang", "RU")
    
    # Загружаем сообщения
    messages = load_messages()
    if recipient_id not in messages:
        messages[recipient_id] = []
    
    # Сохраняем сообщение
    messages[recipient_id].append({
        "id": str(datetime.now().timestamp()),
        "from": user_id,
        "from_name": sender_name,
        "text": message.text,
        "timestamp": datetime.now().isoformat(),
        "read": False
    })
    save_messages(messages)
    
    # Отправляем уведомление получателю
    # Импортируем bot внутри функции, чтобы избежать циклического импорта
    from bot import bot
    
    try:
        await bot.send_message(
            recipient_id,
            f"📨 **От {sender_name}:**\n{message.text[:100]}..."
        )
    except Exception as e:
        print(f"Не удалось отправить уведомление: {e}")
    
    # Подтверждение отправителю
    await message.answer(
        "✅ Отправлено",
        reply_markup=get_communicator_menu(lang)
    )
    
    # Очищаем контекст
    del USER_CONTEXT[user_id]


@router.message(F.text.in_(["📥 Входящие", "📥 Inbox", "📥 Boîte"]))
async def inbox_messages(message: Message):
    user_id = str(message.from_user.id)
    if user_id not in WHITE_LIST:
        return
    
    messages = load_messages()
    user_messages = messages.get(user_id, [])
    
    if not user_messages:
        await message.answer("📭 **Нет сообщений**")
        return
    
    # Показываем последние 5 сообщений
    unread = [m for m in user_messages if not m.get("read", False)]
    read = [m for m in user_messages if m.get("read", False)]
    
    text = f"📨 **Входящие**\n\n"
    text += f"📬 Непрочитанные: {len(unread)}\n"
    text += f"📖 Прочитанные: {len(read)}\n\n"
    
    if unread:
        text += "**Новые сообщения:**\n"
        for msg in unread[-5:]:
            text += f"• {msg['from_name']}: {msg['text'][:50]}...\n"
            # Помечаем как прочитанное
            msg["read"] = True
    
    save_messages(messages)
    await message.answer(text)


@router.message(F.text.in_(["🔙 Назад", "🔙 Back", "🔙 Retour"]))
async def back_to_main(message: Message):
    user_id = str(message.from_user.id)
    if user_id not in WHITE_LIST:
        return
    
    from keyboards import get_main_menu
    user_data = WHITE_LIST[user_id]
    await message.answer(
        "🔙 Возврат в главное меню",
        reply_markup=get_main_menu(user_data)
    )