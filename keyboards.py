from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict
from config import WHITE_LIST

def get_language_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_RU")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_EN")],
        [InlineKeyboardButton(text="🇫🇷 Français", callback_data="lang_FR")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_main_menu(user_data: Dict) -> ReplyKeyboardMarkup:
    role = user_data["role"]
    lang = user_data["lang"]
    buttons = []
    
    t = {
        "RU": {
            "lang": "🌐 Сменить язык",
            "prod": "⛏️ Статус карьера",
            "fleet": "🚛 Парк техники",
            "comm": "💬 Коммуникатор",
            "vip": "💬 VIP-Чат",
            "ceo": "🌍 Сводка по Африке",
            "report": "📊 Детальный отчет",
            "maint": "🔧 Статус ремонтов",
            "blast": "💥 Взрывные работы",
            "ware": "📦 Статус склада",
            "plant": "🏭 Статус фабрики",
            "ai": "🧠 ИИ-Аналитика",
            "translate": "🌐 Синхронизация докладов"
        },
        "EN": {
            "lang": "🌐 Change language",
            "prod": "⛏️ Mine Status",
            "fleet": "🚛 Equipment Fleet",
            "comm": "💬 Communicator",
            "vip": "💬 VIP Chat",
            "ceo": "🌍 Africa Summary",
            "report": "📊 Detailed Report",
            "maint": "🔧 Maintenance",
            "blast": "💥 Blasting",
            "ware": "📦 Warehouse",
            "plant": "🏭 Processing Plant",
            "ai": "🧠 AI Analytics",
            "translate": "🌐 Reports Sync"
        },
        "FR": {
            "lang": "🌐 Changer de langue",
            "prod": "⛏️ Statut Mine",
            "fleet": "🚛 Flotte",
            "comm": "💬 Communicateur",
            "vip": "💬 Chat VIP",
            "ceo": "🌍 Rapport Afrique",
            "report": "📊 Rapport Détaillé",
            "maint": "🔧 Maintenance",
            "blast": "💥 Tir",
            "ware": "📦 Entrepôt",
            "plant": "🏭 Usine",
            "ai": "🧠 Analyse IA",
            "translate": "🌐 Synchronisation"
        }
    }
    texts = t[lang]
    
    # === ОБЩИЕ КНОПКИ ДЛЯ ВСЕХ ===
    buttons.append([KeyboardButton(text=texts["lang"])])
    buttons.append([KeyboardButton(text=texts["prod"])])
    buttons.append([KeyboardButton(text=texts["fleet"])])
    buttons.append([KeyboardButton(text=texts["comm"])])
    buttons.append([KeyboardButton(text=texts["vip"])])
    
    # === КНОПКИ ПО РОЛЯМ ===
    
    # 1. CEO (Гендиректор) — всё
    if role == "CEO":
        buttons.append([KeyboardButton(text=texts["ceo"])])
        buttons.append([KeyboardButton(text=texts["report"])])
        buttons.append([KeyboardButton(text=texts["ai"])])
        buttons.append([KeyboardButton(text=texts["translate"])])
    
    # 2. MINE_MANAGER (Директор рудника) — всё по руднику
    elif role == "MINE_MANAGER":
        buttons.append([KeyboardButton(text=texts["report"])])
        buttons.append([KeyboardButton(text=texts["maint"])])
        buttons.append([KeyboardButton(text=texts["blast"])])
        buttons.append([KeyboardButton(text=texts["ware"])])
        buttons.append([KeyboardButton(text=texts["plant"])])
        buttons.append([KeyboardButton(text=texts["ai"])])
        buttons.append([KeyboardButton(text=texts["translate"])])
    
    # 3. ASSISTANT (Помощник-переводчик) — вся техника + переводы
    elif role == "ASSISTANT":
        buttons.append([KeyboardButton(text=texts["maint"])])
        buttons.append([KeyboardButton(text=texts["blast"])])
        buttons.append([KeyboardButton(text=texts["ware"])])
        buttons.append([KeyboardButton(text=texts["plant"])])
        buttons.append([KeyboardButton(text=texts["translate"])])  # ← КЛЮЧЕВАЯ КНОПКА ДЛЯ ПЕРЕВОДЧИКА
        buttons.append([KeyboardButton(text=texts["ai"])])
    
    # 4. MINING_HEAD (Начальник майнинга) — добыча + взрывы
    elif role == "MINING_HEAD":
        buttons.append([KeyboardButton(text=texts["blast"])])
        buttons.append([KeyboardButton(text=texts["maint"])])
        buttons.append([KeyboardButton(text=texts["ai"])])
    
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_communicator_menu(lang: str) -> ReplyKeyboardMarkup:
    texts = {
        "RU": {"new": "✉️ Новое", "inbox": "📥 Входящие", "back": "🔙 Назад"},
        "EN": {"new": "✉️ New", "inbox": "📥 Inbox", "back": "🔙 Back"},
        "FR": {"new": "✉️ Nouveau", "inbox": "📥 Boîte", "back": "🔙 Retour"}
    }
    t = texts[lang]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t["new"])], [KeyboardButton(text=t["inbox"])], [KeyboardButton(text=t["back"])]],
        resize_keyboard=True
    )

def get_recipients_keyboard(lang: str, exclude_user_id: str) -> InlineKeyboardMarkup:
    buttons = []
    for uid, data in WHITE_LIST.items():
        if uid != exclude_user_id:
            buttons.append([InlineKeyboardButton(text=f"{data['name']} ({data['role']})", callback_data=f"recipient_{uid}")])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)