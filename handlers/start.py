from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from aiogram.filters import Command

from config import WHITE_LIST
from keyboards import get_main_menu

router = Router()

# Конфигурация WebApp
WEBAPP_URL = "https://abarabash67-debug.github.io/africa-mining-app/"


@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = str(message.from_user.id)
    
    # Проверяем, есть ли пользователь в белом списке
    if user_id in WHITE_LIST:
        user_data = WHITE_LIST[user_id]
        role = user_data.get("role", "user")
        
        # Для топ-ролей показываем кнопку WebApp
        if role in ["CEO", "MINE_MANAGER", "ASSISTANT"]:
            # Создаем клавиатуру с кнопкой WebApp
            webapp_btn = KeyboardButton(
                text="📊 Открыть дашборд",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
            
            # Добавляем обычные кнопки для навигации
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [webapp_btn],
                    [KeyboardButton(text="⛏️ Статус карьера")],
                    [KeyboardButton(text="🚛 Парк техники")]
                ],
                resize_keyboard=True,
                is_persistent=True
            )
            
            await message.answer(
                f"👋 Добро пожаловать, {message.from_user.first_name}!\n\n"
                f"Ваша роль: *{role}*\n"
                f"Нажмите «📊 Открыть дашборд», чтобы открыть мобильный дашборд.",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            return
    
    # Для обычных пользователей - стандартное меню через get_main_menu
    user_data = {"role": "user", "lang": "RU"}
    await message.answer(
        f"👋 Добро пожаловать, {message.from_user.first_name}!\n\n"
        "Используйте кнопки ниже для навигации:",
        reply_markup=get_main_menu(user_data)
    )


@router.message(F.text == "📊 Открыть дашборд")
async def open_dashboard(message: Message):
    """Обработчик для тех, у кого нет кнопки WebApp (запасной вариант)"""
    user_id = str(message.from_user.id)
    
    if user_id in WHITE_LIST:
        user_data = WHITE_LIST[user_id]
        role = user_data.get("role", "user")
        
        if role in ["CEO", "MINE_MANAGER", "ASSISTANT"]:
            await message.answer(
                f"📱 Откройте дашборд по ссылке:\n{WEBAPP_URL}\n\n"
                "Или используйте кнопку «📊 Открыть дашборд» на клавиатуре."
            )
        else:
            await message.answer("❌ У вас нет доступа к дашборду.")
    else:
        await message.answer("❌ Доступ запрещен.")