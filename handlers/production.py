from aiogram import Router, F
from aiogram.types import Message

from config import WHITE_LIST
from data import PRODUCTION_DATA, FLEET_DATA

router = Router()


@router.message(F.text.contains("⛏️ Статус карьера") | 
                F.text.contains("⛏️ Mine Status") | 
                F.text.contains("⛏️ Statut de la Mine"))
async def mine_status(message: Message):
    user_id = str(message.from_user.id)
    if user_id not in WHITE_LIST:
        return
    
    user_data = WHITE_LIST[user_id]
    lang = user_data["lang"]
    role = user_data["role"]
    region = user_data.get("region", "Конго")
    
    # ===== CEO: ВСЯ АФРИКА =====
    if role == "CEO":
        congo = PRODUCTION_DATA.get("congo", {})
        zambia = PRODUCTION_DATA.get("zambia", {})
        tanzania = PRODUCTION_DATA.get("tanzania", {})
        
        texts = {
            "RU": f"🌍 **ГЛОБАЛЬНАЯ СВОДКА ПО АФРИКЕ** (CEO)\n\n"
                  f"🇨🇩 Конго: {congo.get('actual_daily', 0):,} т ({congo.get('percent', 0)}%)\n"
                  f"🇿🇲 Замбия: {zambia.get('actual_daily', 0):,} т ({zambia.get('percent', 0)}%)\n"
                  f"🇹🇿 Танзания: {tanzania.get('actual_daily', 0):,} т ({tanzania.get('percent', 0)}%)\n\n"
                  f"📊 ИТОГО: {congo.get('actual_daily', 0) + zambia.get('actual_daily', 0) + tanzania.get('actual_daily', 0):,} т",
            "EN": f"🌍 **GLOBAL AFRICA SUMMARY** (CEO)\n\n"
                  f"🇨🇩 Congo: {congo.get('actual_daily', 0):,} t ({congo.get('percent', 0)}%)\n"
                  f"🇿🇲 Zambia: {zambia.get('actual_daily', 0):,} t ({zambia.get('percent', 0)}%)\n"
                  f"🇹🇿 Tanzania: {tanzania.get('actual_daily', 0):,} t ({tanzania.get('percent', 0)}%)\n\n"
                  f"📊 TOTAL: {congo.get('actual_daily', 0) + zambia.get('actual_daily', 0) + tanzania.get('actual_daily', 0):,} t",
            "FR": f"🌍 **RAPPORT RÉGIONAL AFRIQUE** (PDG)\n\n"
                  f"🇨🇩 Congo: {congo.get('actual_daily', 0):,} t ({congo.get('percent', 0)}%)\n"
                  f"🇿🇲 Zambie: {zambia.get('actual_daily', 0):,} t ({zambia.get('percent', 0)}%)\n"
                  f"🇹🇿 Tanzanie: {tanzania.get('actual_daily', 0):,} t ({tanzania.get('percent', 0)}%)\n\n"
                  f"📊 TOTAL: {congo.get('actual_daily', 0) + zambia.get('actual_daily', 0) + tanzania.get('actual_daily', 0):,} t"
        }
        await message.answer(texts[lang])
        return
    
    # ===== ВСЕ ОСТАЛЬНЫЕ: ТОЛЬКО СВОЙ РУДНИК =====
    prod = PRODUCTION_DATA.get(region, {})
    if not prod:
        await message.answer(f"❌ Данные по региону {region} не найдены")
        return
    
    texts = {
        "RU": f"⛏️ **{region.upper()}**\nРуда: {prod.get('ore', 'N/A')}\nПлан: {prod.get('plan_daily', 0):,} т\nФакт: {prod.get('actual_daily', 0):,} т ({prod.get('percent', 0)}%)",
        "EN": f"⛏️ **{region.upper()}**\nOre: {prod.get('ore', 'N/A')}\nPlan: {prod.get('plan_daily', 0):,} t\nActual: {prod.get('actual_daily', 0):,} t ({prod.get('percent', 0)}%)",
        "FR": f"⛏️ **{region.upper()}**\nMinerai: {prod.get('ore', 'N/A')}\nPlan: {prod.get('plan_daily', 0):,} t\nRéel: {prod.get('actual_daily', 0):,} t ({prod.get('percent', 0)}%)"
    }
    await message.answer(texts[lang])


@router.message(F.text.contains("🚛"))
async def equipment_fleet(message: Message):
    user_id = str(message.from_user.id)
    if user_id not in WHITE_LIST:
        return
    
    fleet = FLEET_DATA
    
    total_active = sum(data.get('active', 0) for data in fleet.values())
    total = sum(data.get('total', 0) for data in fleet.values())
    total_breakdown = sum(data.get('breakdown', 0) for data in fleet.values())
    efficiency = int(total_active / total * 100) if total > 0 else 0
    
    texts = {
        "RU": f"🚛 **ПАРК ТЕХНИКИ**\n\n• Всего: {total}\n• В работе: {total_active}\n• В ремонте: {total_breakdown}\n• Эффективность: {efficiency}%",
        "EN": f"🚛 **EQUIPMENT FLEET**\n\n• Total: {total}\n• Active: {total_active}\n• Under repair: {total_breakdown}\n• Efficiency: {efficiency}%",
        "FR": f"🚛 **FLOTTE**\n\n• Total: {total}\n• En service: {total_active}\n• En panne: {total_breakdown}\n• Efficacité: {efficiency}%"
    }
    
    lang = WHITE_LIST[user_id].get("lang", "RU")
    await message.answer(texts[lang])