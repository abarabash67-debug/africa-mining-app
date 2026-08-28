from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from config import WHITE_LIST, ROLE_TRANSLATIONS
from keyboards import get_language_keyboard, get_main_menu
from utils import get_user_lang

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = str(message.from_user.id)
    if user_id not in WHITE_LIST:
        await message.answer("❌ Доступ запрещен.")
        return
    
    user_data = WHITE_LIST[user_id]
    
    if "lang" not in user_data or user_data["lang"] not in ["RU", "EN", "FR"]:
        await message.answer("🌍 **Выберите язык:**", reply_markup=get_language_keyboard())
        return
    
    lang = user_data["lang"]
    role = user_data["role"]
    texts = {
        "RU": f"🏗️ **Добро пожаловать, {user_data['name']}!**\nРегион: {user_data['region'].upper()}\nДолжность: {ROLE_TRANSLATIONS.get(role, {}).get('RU', role)}",
        "EN": f"🏗️ **Welcome, {user_data['name']}!**\nRegion: {user_data['region'].upper()}\nPosition: {ROLE_TRANSLATIONS.get(role, {}).get('EN', role)}",
        "FR": f"🏗️ **Bienvenue, {user_data['name']}!**\nRégion: {user_data['region'].upper()}\nPoste: {ROLE_TRANSLATIONS.get(role, {}).get('FR', role)}"
    }
    await message.answer(texts[lang], reply_markup=get_main_menu(user_data))

@router.callback_query(F.data.startswith("lang_"))
async def language_selected(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    lang_code = callback.data.split("_")[1]
    
    if user_id in WHITE_LIST:
        WHITE_LIST[user_id]["lang"] = lang_code
    
    user_data = WHITE_LIST[user_id]
    await callback.message.delete()
    await callback.message.answer(
        f"✅ Язык: {lang_code}",
        reply_markup=get_main_menu(user_data)
    )
    await callback.answer()

@router.message(Command("language"))
@router.message(F.text.in_(["🌐 Сменить язык", "🌐 Change language", "🌐 Changer de langue"]))
async def change_language(message: Message):
    await message.answer("🌍 **Выберите язык:**", reply_markup=get_language_keyboard())