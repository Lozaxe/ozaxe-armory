import requests, json, re
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import os

URL = "https://classic-armory.org/character/eu/tbc-anniversary/spineshatter/ozaxe"
headers = {"User-Agent":"Mozilla/5.0"}

# garde l'ancien data.json si le scrape plante
old = {}
if os.path.exists("data.json"):
    try: old = json.load(open("data.json", encoding="utf-8"))
    except: pass

html = requests.get(URL, headers=headers, timeout=20).text
soup = BeautifulSoup(html, "lxml")
text = soup.get_text(" ", strip=True)

def find(pattern):
    m = re.search(pattern, text, re.I)
    return m.group(1) if m else ""

data = {
    "updated": datetime.now(timezone.utc).isoformat(),
    "level": 20,
    "base": {
        "health": find(r"Health[, ]+(\d+)"),
        "mana": find(r"Mana[, ]+(\d+)"),
        "stamina": find(r"Stamina[, ]+(\d+)"),
        "strength": find(r"Strength[, ]+(\d+)"),
        "agility": find(r"Agility[, ]+(\d+)"),
        "intellect": find(r"Intellect[, ]+(\d+)"),
        "spirit": find(r"Spirit[, ]+(\d+)")
    },
    "melee": {
        "damage": find(r"Damage[, ]+([\d\- ]+)"),
        "speed": find(r"Speed[, ]+([\d\.]+)"),
        "ap": find(r"Attack Power[, ]+(\d+)"),
        "crit": find(r"Crit Chance[, ]+([\d\.]+%?)"),
        "haste": find(r"Haste[, ]+([\d\.]+%?)")
    },
    "spell": {
        "healing": find(r"Healing[, ]+(\d+)"),
        "damage": find(r"Spell Damage[, ]+(\d+)"),
        "penetration": find(r"Penetration[, ]+(\d+)"),
        "mp5": find(r"Mana per 5[, ]+(\d+)"),
        "crit": find(r"Spell Crit[, ]+([\d\.]+%?)")
    },
    "defense": {
        "armor": find(r"Armor[, ]+(\d+)"),
        "dodge": find(r"Dodge[, ]+([\d\.]+%?)"),
        "parry": find(r"Parry[, ]+([\d\.]+%?)"),
        "block": find(r"Block[, ]+([\d\.]+%?)"),
        "defense": find(r"Defense[, ]+(\d+)")
    },
    "gear": old.get("gear", []) # on ne touche pas au gear pour l'instant
}

# si une valeur est vide, reprends l'ancienne (évite la régression)
for sec in ["base","melee","spell","defense"]:
    for k,v in data[sec].items():
        if not v and old.get(sec,{}).get(k):
            data[sec][k] = old[sec][k]

with open("data.json","w",encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK - stats restaurées")
