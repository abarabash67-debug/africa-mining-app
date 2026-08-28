# config.py
BOT_TOKEN = "8767167366:AAGs3xtM72FYcx7nc1GKxDba2b7la13JaeQ"

WHITE_LIST = {
    "5895527047": {"name": "Генеральный Директор Африка", "role": "CEO", "lang": "FR", "region": "all_africa", "department": "executive", "access_level": 100},
    "987654321": {"name": "Директор рудника Конго", "role": "MINE_MANAGER", "lang": "EN", "region": "congo", "department": "management", "access_level": 90},
    "5895527048": {"name": "Помощник- Переводчик Конго", "role": "CHIEF_ENGINEER", "lang": "RU", "region": "congo", "department": "engineering", "access_level": 80},
    "111111111": {"name": "Начальник майнинга Конго", "role": "MINING_HEAD", "lang": "EN", "region": "congo", "department": "mining", "access_level": 80},
    "222222222": {"name": "Начальник переработки Конго", "role": "PROCESSING_HEAD", "lang": "FR", "region": "congo", "department": "processing", "access_level": 75},
    "333333333": {"name": "Начальник склада Конго", "role": "WAREHOUSE_HEAD", "lang": "RU", "region": "congo", "department": "logistics", "access_level": 70},
    "444444444": {"name": "Главный механик Конго", "role": "CHIEF_MECHANIC", "lang": "EN", "region": "congo", "department": "maintenance", "access_level": 75},
    "555555555": {"name": "Начальник взрывных работ", "role": "BLASTING_HEAD", "lang": "RU", "region": "congo", "department": "safety", "access_level": 70},
    "666666666": {"name": "Директор рудника Замбия", "role": "MINE_MANAGER", "lang": "EN", "region": "zambia", "department": "management", "access_level": 90},
    "777777777": {"name": "Директор рудника Танзания", "role": "MINE_MANAGER", "lang": "EN", "region": "tanzania", "department": "management", "access_level": 90},
}

ROLE_TRANSLATIONS = {
    "CEO": {"RU": "Генеральный Директор", "EN": "CEO", "FR": "PDG"},
    "MINE_MANAGER": {"RU": "Директор рудника", "EN": "Mine Manager", "FR": "Directeur"},
    "CHIEF_ENGINEER": {"RU": "Помощник- Переводчик", "EN": "Chief Engineer", "FR": "Ingénieur Chef"},
    "MINING_HEAD": {"RU": "Начальник майнинга", "EN": "Mining Head", "FR": "Chef Exploitation"},
    "PROCESSING_HEAD": {"RU": "Начальник переработки", "EN": "Processing Head", "FR": "Chef Traitement"},
    "WAREHOUSE_HEAD": {"RU": "Начальник склада", "EN": "Warehouse Head", "FR": "Chef Entrepôt"},
    "CHIEF_MECHANIC": {"RU": "Главный механик", "EN": "Chief Mechanic", "FR": "Mécanicien Chef"},
    "BLASTING_HEAD": {"RU": "Начальник взрывных работ", "EN": "Blasting Head", "FR": "Chef Tir"}
}