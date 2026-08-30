import json
import os
from typing import List, Dict, Any

# ============================================================
# КОНСТАНТЫ
# ============================================================

MESSAGES_FILE = "messages.json"
VIP_MESSAGES_FILE = "vip_messages.json"


# ============================================================
# ФУНКЦИИ ДЛЯ ОБЫЧНОГО КОММУНИКАТОРА
# ============================================================

def load_messages() -> Dict[str, List[Dict[str, Any]]]:
    """
    Загружает сообщения коммуникатора из JSON-файла.
    Возвращает словарь {user_id: [список сообщений]}.
    """
    if not os.path.exists(MESSAGES_FILE):
        return {}
    
    try:
        with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Ошибка загрузки сообщений: {e}")
        return {}


def save_messages(messages: Dict[str, List[Dict[str, Any]]]) -> bool:
    """
    Сохраняет сообщения коммуникатора в JSON-файл.
    Возвращает True в случае успеха, False при ошибке.
    """
    try:
        with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"⚠️ Ошибка сохранения сообщений: {e}")
        return False


# ============================================================
# ФУНКЦИИ ДЛЯ VIP-ЧАТА
# ============================================================

def load_vip_messages() -> List[Dict[str, Any]]:
    """
    Загружает сообщения VIP-чата из JSON-файла.
    Если файла нет — возвращает пустой список.
    """
    if not os.path.exists(VIP_MESSAGES_FILE):
        return []
    
    try:
        with open(VIP_MESSAGES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Ошибка загрузки VIP-сообщений: {e}")
        return []


def save_vip_messages(messages: List[Dict[str, Any]]) -> bool:
    """
    Сохраняет сообщения VIP-чата в JSON-файл.
    Возвращает True в случае успеха, False при ошибке.
    """
    try:
        with open(VIP_MESSAGES_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"⚠️ Ошибка сохранения VIP-сообщений: {e}")
        return False


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (опционально)
# ============================================================

def clear_messages() -> None:
    """Очищает все сообщения (для тестирования)"""
    if os.path.exists(MESSAGES_FILE):
        os.remove(MESSAGES_FILE)
    if os.path.exists(VIP_MESSAGES_FILE):
        os.remove(VIP_MESSAGES_FILE)
    print("✅ Все сообщения очищены")


def get_unread_count(user_id: str) -> int:
    """
    Возвращает количество непрочитанных сообщений для пользователя.
    """
    messages = load_messages()
    user_messages = messages.get(user_id, [])
    return len([m for m in user_messages if not m.get("read", False)])


def get_vip_messages_count() -> int:
    """
    Возвращает общее количество сообщений в VIP-чате.
    """
    return len(load_vip_messages())