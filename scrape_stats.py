import requests, json, re
from datetime import datetime, timezone

URL = "https://classic-armory.org/character/eu/tbc-anniversary/spineshatter/ozaxe"
html = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"}, timeout=20).text

# le texte brut contient "Health 779 Mana 820..." même sans JS
def get(val):
    m = re.search(rf"{val}[^\d]*(\d+[\d\.\- %]*)", html, re.I)
    return m.group(1).strip() if m else ""

data = {
    "updated": datetime.now(timezone.utc).isoformat(),
    "base": {
        "health": get("Health"),
        "mana": get("Mana"),
        "stamina": get("Stamina"),
        "strength": get("Strength"),
        "agility": get("Agility"),
        "intellect": get("Intellect"),
        "spirit": get("Spirit")
    },
    "melee": {
        "damage": get("Damage"),
        "speed": get("Speed"),
        "ap": get("Attack Power"),
        "crit": get("Crit Chance"),
        "haste": get("Haste")
    },
    "spell": {
        "healing": get("Healing"),
        "damage": get("Spell Damage"),
        "penetration": get("Penetration"),
        "mp5": get("Mana per 5"),
        "crit": get("Spell Crit")
    },
    "defense": {
        "armor": get("Armor"),
        "dodge": get("Dodge"),
        "parry": get("Parry"),
        "block": get("Block"),
        "defense": get("Defense")
    }
}

with open("data.json","w",encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
