# handlers/production.py
from aiogram import Router, F
from aiogram.types import Message
from typing import Optional, Dict, Any

from config import WHITE_LIST
from data import (
    PRODUCTION_DATA,
    FLEET_DATA,
    get_production_by_country,
    get_country_summary,
    get_africa_summary
)

router = Router()


def _get_lang_text(texts: Dict[str, str], lang: str) -> str:
    """Безопасное получение текста по языку"""
    return texts.get(lang, texts.get("RU", "❌ Язык не поддерживается"))


def _format_issues(issues: Optional[list], lang: str) -> str:
    """Форматирование списка проблем"""
    no_issues = {
        "RU": "Нет проблем",
        "EN": "No issues",
        "FR": "Aucun problème"
    }
    if not issues or not isinstance(issues, list):
        return no_issues.get(lang, "No issues")
    return ", ".join(issues) if issues else no_issues.get(lang, "No issues")


@router.message(F.text.contains("⛏️ Статус карьера") | 
                F.text.contains("⛏️ Mine Status") | 
                F.text.contains("⛏️ Statut de la Mine"))
async def mine_status(message: Message):
    user_id = str(message.from_user.id)
    
    # Проверка пользователя
    if user_id not in WHITE_LIST:
        return
    
    user_data = WHITE_LIST[user_id]
    lang = user_data.get("lang", "RU")
    role = user_data.get("role", "user")
    region = user_data.get("region", "Конго")
    
    # ===== ГЛОБАЛЬНЫЙ ДОСТУП =====
    if region == "all_africa":
        summary = get_africa_summary()
        
        # CEO - с финансами
        if role == "CEO":
            texts = {
                "RU": f"""🌍 **ГЛОБАЛЬНАЯ СВОДКА ПО АФРИКЕ** (CEO)

📊 **ИТОГО ПО АФРИКЕ:**
  • Всего рудников: 9
  • Стран: 3
  • План: {summary['total_plan']:,} т/сут
  • Факт: {summary['total_actual']:,} т/сут
  • Выполнение: {summary['total_percent']}%

📋 **ПО СТРАНАМ:**
{self._format_country_summary(summary['countries'])}

💼 **ФИНАНСОВЫЕ ПОКАЗАТЕЛИ:**
  • Конго: ${self._get_financial_data('congo'):,}/т
  • Танзания: ${self._get_financial_data('tanzania'):,}/т
  • Мозамбик: ${self._get_financial_data('mozambique'):,}/т

🚨 **КРИТИЧЕСКИЕ АЛЕРТЫ:**
{self._format_alerts(summary['all_issues'])}"""
            }
            await message.answer(_get_lang_text(texts, lang))
            return
        
        # Остальные - без финансов
        else:
            texts = {
                "RU": f"""🌍 **ГЛОБАЛЬНАЯ СВОДКА ПО АФРИКЕ**

📊 **ИТОГО ПО АФРИКЕ:**
  • Всего рудников: 9
  • Стран: 3
  • План: {summary['total_plan']:,} т/сут
  • Факт: {summary['total_actual']:,} т/сут
  • Выполнение: {summary['total_percent']}%

📋 **ПО СТРАНАМ:**
{self._format_country_summary(summary['countries'])}

🚨 **КРИТИЧЕСКИЕ АЛЕРТЫ:**
{self._format_alerts(summary['all_issues'])}"""
            }
            await message.answer(_get_lang_text(texts, lang))
            return
    
    # ===== ДИРЕКТОР РУДНИКА =====
    country_mines = get_production_by_country(region)
    country_summary = get_country_summary(region)
    
    if not country_mines:
        await message.answer(f"❌ Данные по региону {region} не найдены")
        return
    
    mine_list = "\n".join([
        f"  • {data['name']}: {data['actual_daily']:,} т ({data['percent']}%)"
        for data in country_mines.values()
    ])
    
    texts = {
        "RU": f"⛏️ **{region.upper()}** ({country_summary['mines_count']} рудников)\n\n"
              f"📊 **ИТОГО ПО СТРАНЕ:**\n"
              f"  • План: {country_summary['total_plan']:,} т/сут\n"
              f"  • Факт: {country_summary['total_actual']:,} т/сут\n"
              f"  • Выполнение: {country_summary['total_percent']}%\n\n"
              f"📋 **РУДНИКИ:**\n{mine_list}\n\n"
              f"🚨 **ПРОБЛЕМЫ:**\n{_format_issues(country_summary['issues'], lang)}"
    }
    await message.answer(_get_lang_text(texts, lang))


@router.message(F.text.contains("🚛"))
async def equipment_fleet(message: Message):
    user_id = str(message.from_user.id)
    
    if user_id not in WHITE_LIST:
        return
    
    user_data = WHITE_LIST[user_id]
    lang = user_data.get("lang", "RU")
    role = user_data.get("role", "user")
    
    fleet = FLEET_DATA
    total_active = sum(data.get('active', 0) for data in fleet.values())
    total = sum(data.get('total', 0) for data in fleet.values())
    total_breakdown = sum(data.get('breakdown', 0) for data in fleet.values())
    
    # ===== CEO: ТОЛЬКО ИТОГИ =====
    if role == "CEO":
        efficiency = int(total_active / total * 100) if total > 0 else 0
        texts = {
            "RU": f"🚛 **ПАРК ТЕХНИКИ ПО АФРИКЕ**\n\n"
                  f"• Всего машин: {total}\n"
                  f"• В работе: {total_active}\n"
                  f"• В ремонте: {total_breakdown}\n"
                  f"• Эффективность: {efficiency}%\n\n"
                  f"📊 **Детализация по запросу**\n"
                  f"Нажмите '📊 Детальный отчет' для полной информации.",
            "EN": f"🚛 **EQUIPMENT FLEET AFRICA**\n\n"
                  f"• Total units: {total}\n"
                  f"• Active: {total_active}\n"
                  f"• Under repair: {total_breakdown}\n"
                  f"• Efficiency: {efficiency}%\n\n"
                  f"📊 **Details on request**\n"
                  f"Press '📊 Detailed Report' for full info.",
            "FR": f"🚛 **FLOTTE AFRIQUE**\n\n"
                  f"• Total unités: {total}\n"
                  f"• En service: {total_active}\n"
                  f"• En panne: {total_breakdown}\n"
                  f"• Efficacité: {efficiency}%\n\n"
                  f"📊 **Détails sur demande**\n"
                  f"Appuyez sur '📊 Rapport Détaillé' pour plus d'informations."
        }
        await message.answer(_get_lang_text(texts, lang))
        return
    
    # ===== ВСЕ ОСТАЛЬНЫЕ: ДЕТАЛЬНО =====
    result = "🚛 **FLEET DETAILS**\n\n"
    for name, data in fleet.items():
        active = data.get('active', 0)
        total_units = data.get('total', 0)
        breakdown = data.get('breakdown', 0)
        
        line = f"• **{name.upper()}**: {active}/{total_units} active"
        if breakdown > 0:
            line += f" (ремонт: {breakdown})"
        result += line + "\n"
    
    await message.answer(result)


def _format_country_summary(self, countries: dict) -> str:
    """Вспомогательный метод для форматирования сводки по странам"""
    lines = []
    for country, data in countries.items():
        lines.append(f"🇨🇩 **{country}:**")
        lines.append(f"  • План: {data['total_plan']:,} т/сут")
        lines.append(f"  • Факт: {data['total_actual']:,} т/сут")
        lines.append(f"  • Выполнение: {data['total_percent']}%")
    return "\n".join(lines)


def _format_alerts(self, alerts: list) -> str:
    """Форматирование списка алертов"""
    if not alerts:
        return "  • Нет критических проблем"
    return "\n".join([f"  • {alert}" for alert in alerts])


def _get_financial_data(self, country: str) -> int:
    """Получение финансовых данных (заглушка)"""
    # TODO: заменить на реальные данные из data.py
    financials = {
        "congo": 12400,
        "tanzania": 8200,
        "mozambique": 5800
    }
    return financials.get(country, 0)