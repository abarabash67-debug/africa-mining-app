PRODUCTION_DATA = {
    # ===== КОНГО (3 рудника) =====
    "congo_1": {
        "name": "Конго-1",
        "country": "Конго",
        "ore": "Медь (Cu)",
        "plan_daily": 5000,
        "actual_daily": 5100,
        "percent": 102,
        "quality": "Сорт 1 (98%)",
        "issues": ["Сбой конвейера"],
        "lat": "-4.5",
        "lon": "15.5"
    },
    "congo_2": {
        "name": "Конго-2",
        "country": "Конго",
        "ore": "Медь (Cu)",
        "plan_daily": 4000,
        "actual_daily": 3900,
        "percent": 97.5,
        "quality": "Сорт 1 (96%)",
        "issues": ["Замена футеровки мельницы"],
        "lat": "-4.8",
        "lon": "15.8"
    },
    "congo_3": {
        "name": "Конго-3",
        "country": "Конго",
        "ore": "Медь (Cu)",
        "plan_daily": 3000,
        "actual_daily": 3240,
        "percent": 108,
        "quality": "Сорт 1 (99%)",
        "issues": [],
        "lat": "-5.0",
        "lon": "16.0"
    },
    
    # ===== ТАНЗАНИЯ (3 рудника) =====
    "tanzania_1": {
        "name": "Танзания-1",
        "country": "Танзания",
        "ore": "Золото (Au)",
        "plan_daily": 200,
        "actual_daily": 210,
        "percent": 105,
        "quality": "Проба 18 карат",
        "issues": [],
        "lat": "-6.2",
        "lon": "35.0"
    },
    "tanzania_2": {
        "name": "Танзания-2",
        "country": "Танзания",
        "ore": "Золото (Au)",
        "plan_daily": 180,
        "actual_daily": 175,
        "percent": 97.2,
        "quality": "Проба 17 карат",
        "issues": ["Плановый ремонт"],
        "lat": "-6.5",
        "lon": "35.3"
    },
    "tanzania_3": {
        "name": "Танзания-3",
        "country": "Танзания",
        "ore": "Золото (Au)",
        "plan_daily": 120,
        "actual_daily": 125,
        "percent": 104.2,
        "quality": "Проба 18 карат",
        "issues": [],
        "lat": "-6.8",
        "lon": "35.6"
    },
    
    # ===== МОЗАМБИК (3 рудника) =====
    "mozambique_1": {
        "name": "Мозамбик-1",
        "country": "Мозамбик",
        "ore": "Уголь",
        "plan_daily": 3000,
        "actual_daily": 2850,
        "percent": 95,
        "quality": "Энергетический (6000 ккал)",
        "issues": ["Проблемы с логистикой"],
        "lat": "-15.5",
        "lon": "32.0"
    },
    "mozambique_2": {
        "name": "Мозамбик-2",
        "country": "Мозамбик",
        "ore": "Уголь",
        "plan_daily": 2500,
        "actual_daily": 2600,
        "percent": 104,
        "quality": "Коксующийся (7500 ккал)",
        "issues": [],
        "lat": "-15.8",
        "lon": "32.3"
    },
    "mozambique_3": {
        "name": "Мозамбик-3",
        "country": "Мозамбик",
        "ore": "Уголь",
        "plan_daily": 1500,
        "actual_daily": 1400,
        "percent": 93.3,
        "quality": "Энергетический (5800 ккал)",
        "issues": ["Себестоимость выше плана"],
        "lat": "-16.0",
        "lon": "32.6"
    }
}

def get_production_by_country(country: str) -> dict:
    """Возвращает данные по всем рудникам страны"""
    result = {}
    for key, value in PRODUCTION_DATA.items():
        if value["country"] == country:
            result[key] = value
    return result

def get_all_africa_data() -> dict:
    """Возвращает данные по всей Африке"""
    return PRODUCTION_DATA

def get_country_summary(country: str) -> dict:
    """Возвращает сводку по стране"""
    mines = get_production_by_country(country)
    if not mines:
        return {}
    
    total_plan = sum(m["plan_daily"] for m in mines.values())
    total_actual = sum(m["actual_daily"] for m in mines.values())
    total_percent = int((total_actual / total_plan) * 100) if total_plan > 0 else 0
    
    all_issues = []
    for m in mines.values():
        all_issues.extend(m.get("issues", []))
    
    return {
        "total_plan": total_plan,
        "total_actual": total_actual,
        "total_percent": total_percent,
        "issues": all_issues,
        "mines_count": len(mines)
    }

def get_africa_summary() -> dict:
    """Возвращает сводку по всей Африке"""
    countries = ["Конго", "Танзания", "Мозамбик"]
    summary = {}
    total_plan = 0
    total_actual = 0
    all_issues = []
    
    for country in countries:
        country_data = get_country_summary(country)
        summary[country] = country_data
        total_plan += country_data.get("total_plan", 0)
        total_actual += country_data.get("total_actual", 0)
        all_issues.extend(country_data.get("issues", []))
    
    return {
        "countries": summary,
        "total_plan": total_plan,
        "total_actual": total_actual,
        "total_percent": int((total_actual / total_plan) * 100) if total_plan > 0 else 0,
        "all_issues": all_issues
    }

# ПАРК ТЕХНИКИ (ОБНОВЛЁННЫЙ)
FLEET_DATA = {
    # Конго
    "congo_hitachi": {"country": "Конго", "brand": "HITACHI", "total": 100, "active": 88, "maintenance": 8, "breakdown": 4},
    "congo_caterpillar": {"country": "Конго", "brand": "CATERPILLAR", "total": 50, "active": 42, "maintenance": 5, "breakdown": 3},
    "congo_volvo": {"country": "Конго", "brand": "VOLVO", "total": 30, "active": 25, "maintenance": 3, "breakdown": 2},
    
    # Танзания
    "tanzania_hitachi": {"country": "Танзания", "brand": "HITACHI", "total": 30, "active": 28, "maintenance": 1, "breakdown": 1},
    "tanzania_caterpillar": {"country": "Танзания", "brand": "CATERPILLAR", "total": 20, "active": 18, "maintenance": 1, "breakdown": 1},
    
    # Мозамбик
    "mozambique_hitachi": {"country": "Мозамбик", "brand": "HITACHI", "total": 25, "active": 22, "maintenance": 2, "breakdown": 1},
    "mozambique_caterpillar": {"country": "Мозамбик", "brand": "CATERPILLAR", "total": 15, "active": 13, "maintenance": 1, "breakdown": 1},
}