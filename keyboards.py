from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from typing import Dict
from config import WHITE_LIST

# Конфигурация WebApp
WEBAPP_URL = "https://abarabash67-debug.github.io/africa-mining-app/"


def get_language_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_RU")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_EN")],
        [InlineKeyboardButton(text="🇫🇷 Français", callback_data="lang_FR")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_main_menu(user_data: Dict) -> ReplyKeyboardMarkup:
    role = user_data.get("role", "user")
    lang = user_data.get("lang", "RU")
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
            "translate": "🌐 Синхронизация докладов",
            "dashboard": "📊 Открыть дашборд"
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
            "translate": "🌐 Reports Sync",
            "dashboard": "📊 Open Dashboard"
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
            "translate": "🌐 Synchronisation",
            "dashboard": "📊 Ouvrir Dashboard"
        }
    }
    texts = t[lang]
    
    # === ВСЕГДА ПОКАЗЫВАЕМ КНОПКУ ДАШБОРДА ДЛЯ ТОП-РОЛЕЙ ===
    if role in ["CEO", "MINE_MANAGER", "ASSISTANT"]:
        buttons.append([
            KeyboardButton(
                text=texts["dashboard"],
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ])
    
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
        buttons.append([KeyboardButton(text=texts["translate"])])
        buttons.append([KeyboardButton(text=texts["ai"])])
    
    # 4. MINING_HEAD (Начальник майнинга) — добыча + взрывы
    elif role == "MINING_HEAD":
        buttons.append([KeyboardButton(text=texts["blast"])])
        buttons.append([KeyboardButton(text=texts["maint"])])
        buttons.append([KeyboardButton(text=texts["ai"])])
    
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


# ============================================================
# НЕДОСТАЮЩИЕ ФУНКЦИИ (ДОБАВЛЕНЫ)
# ============================================================

def get_communicator_menu(lang: str) -> ReplyKeyboardMarkup:
    """Клавиатура меню Коммуникатора"""
    texts = {
        "RU": {"new": "✉️ Новое", "inbox": "📥 Входящие", "back": "🔙 Назад"},
        "EN": {"new": "✉️ New", "inbox": "📥 Inbox", "back": "🔙 Back"},
        "FR": {"new": "✉️ Nouveau", "inbox": "📥 Boîte", "back": "🔙 Retour"}
    }
    t = texts.get(lang, texts["RU"])
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["new"])],
            [KeyboardButton(text=t["inbox"])],
            [KeyboardButton(text=t["back"])]
        ],
        resize_keyboard=True
    )


def get_recipients_keyboard(lang: str, exclude_user_id: str) -> InlineKeyboardMarkup:
    """Клавиатура для выбора получателя сообщения"""
    buttons = []
    for uid, data in WHITE_LIST.items():
        if uid != exclude_user_id:
            name = data.get("name", uid)
            role = data.get("role", "user")
            buttons.append([
                InlineKeyboardButton(
                    text=f"{name} ({role})",
                    callback_data=f"recipient_{uid}"
                )
            ])
    
    back_texts = {
        "RU": "🔙 Назад",
        "EN": "🔙 Back",
        "FR": "🔙 Retour"
    }
    back_text = back_texts.get(lang, "🔙 Back")
    buttons.append([InlineKeyboardButton(text=back_text, callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Стандартная клавиатура для обычных пользователей"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⛏️ Статус карьера")],
            [KeyboardButton(text="🚛 Парк техники")]
        ],
        resize_keyboard=True,
        is_persistent=True
    )


def get_webapp_keyboard(role: str) -> ReplyKeyboardMarkup:
    """Клавиатура для топ-ролей с кнопкой WebApp"""
    keyboard = [
        [KeyboardButton(
            text="📊 Открыть дашборд",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
        [KeyboardButton(text="⛏️ Статус карьера")],
        [KeyboardButton(text="🚛 Парк техники")]
    ]
    
    if role == "CEO":
        keyboard.append([
            KeyboardButton(text="🌍 Глобальная сводка"),
            KeyboardButton(text="📊 Финансовый отчет")
        ])
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True
    )


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой отмены"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )