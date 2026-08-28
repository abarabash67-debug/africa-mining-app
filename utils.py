import json
import os
from typing import Dict

MESSAGES_FILE = "messages.json"

def load_messages() -> Dict:
    """Загружает сообщения из файла. Если файла нет - создаёт пустой."""
    if not os.path.exists(MESSAGES_FILE):
        # Создаём пустой файл, если его нет
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return {}
    
    try:
        with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Если файл повреждён - создаём новый
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return {}

def save_messages(messages: Dict):
    """Сохраняет сообщения в файл"""
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def get_user_lang(user_id: str, white_list: Dict) -> str:
    """Получает язык пользователя из белого списка"""
    return white_list.get(user_id, {}).get("lang", "RU")