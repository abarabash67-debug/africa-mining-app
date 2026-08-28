from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from config import WHITE_LIST
from keyboards import get_main_menu

router = Router()

# Хранилище активных пользователей в VIP-чате
VIP_USERS = set()

@router.message(Command("vipchat"))
async def vip_chat_start(message: Message):
    user_id = str(message.from_user.id)
    if user_id not in WHITE_LIST:
        await message.answer("❌ Доступ запрещен")
        return
    
    VIP_USERS.add(user_id)
    lang = WHITE_LIST[user_id]["lang"]
    
    texts = {
        "RU": "💬 **Вы вошли в VIP-Чат!**\n\nВсе сообщения будут автоматически переведены на 3 языка.\nКоманда: /leave - покинуть чат",
        "EN": "💬 **You entered VIP Chat!**\n\nAll messages will be auto-translated to 3 languages.\nCommand: /leave - leave chat",
        "FR": "💬 **Vous êtes dans le Chat VIP!**\n\nTous les messages seront traduits en 3 langues.\nCommande: /leave - quitter le chat"
    }
    await message.answer(texts[lang])

@router.message(Command("leave"))
async def leave_vip_chat(message: Message):
    user_id = str(message.from_user.id)
    VIP_USERS.discard(user_id)
    
    lang = WHITE_LIST.get(user_id, {}).get("lang", "RU")
    texts = {
        "RU": "👋 Вы покинули VIP-чат",
        "EN": "👋 You left VIP chat",
        "FR": "👋 Vous avez quitté le chat VIP"
    }
    await message.answer(texts[lang], reply_markup=get_main_menu(WHITE_LIST.get(user_id, {})))

@router.message(F.text)
async def handle_vip_message(message: Message):
    user_id = str(message.from_user.id)
    
    # Проверяем, в VIP-чате ли пользователь
    if user_id not in VIP_USERS:
        return
    
    if message.text.startswith('/'):
        return
    
    if user_id not in WHITE_LIST:
        return
    
    user_data = WHITE_LIST[user_id]
    lang = user_data["lang"]
    name = user_data["name"]
    text = message.text
    
    # Отправляем сообщение всем в VIP-чате (кроме отправителя)
    for vip_user in VIP_USERS:
        if vip_user != user_id:
            try:
                await bot.send_message(
                    vip_user,
                    f"💬 **{name}** ({lang}):\n{text}"
                )
            except:
                pass
    
    # Подтверждение отправителю
    texts = {
        "RU": f"✅ Ваше сообщение отправлено в VIP-чат ({len(VIP_USERS)-1} получателей)",
        "EN": f"✅ Your message sent to VIP chat ({len(VIP_USERS)-1} recipients)",
        "FR": f"✅ Votre message envoyé au chat VIP ({len(VIP_USERS)-1} destinataires)"
    }
    await message.answer(texts.get(lang, texts["RU"]))

# Обработчик кнопки VIP-Чат
@router.message(F.text.in_(["💬 VIP-Чат", "💬 VIP Chat", "💬 Chat VIP"]))
async def vip_chat_button(message: Message):
    await vip_chat_start(message)