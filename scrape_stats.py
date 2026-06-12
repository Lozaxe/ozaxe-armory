import requests, re, json, datetime
from bs4 import BeautifulSoup

URL = "https://classic-armory.org/character/eu/tbc-anniversary/spineshatter/ozaxe"
html = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"}).text

# Classic Armory met les stats en texte brut pour le SEO
text = re.sub(r'\s+', ' ', BeautifulSoup(html, 'html.parser').get_text())

def get(pattern, default=0):
    m = re.search(pattern, text)
    return m.group(1) if m else default

data = {
  "updated": datetime.datetime.utcnow().isoformat()+"Z",
  "base": {
    "health": int(get(r'Health[,\s]+(\d+)', 779)),
    "mana": int(get(r'Mana[,\s]+(\d+)', 820)),
    "stamina": int(get(r'Stamina[,\s]+(\d+)', 73)),
    "strength": int(get(r'Strength[,\s]+(\d+)', 64)),
    "agility": int(get(r'Agility[,\s]+(\d+)', 48)),
    "intellect": int(get(r'Intellect[,\s]+(\d+)', 47)),
    "spirit": int(get(r'Spirit[,\s]+(\d+)', 60)),
  },
  "melee": {
    "damage": get(r'Damage[,\s]+([\d\s\-–]+)', "78 - 102"),
    "speed": get(r'Speed[,\s]+([\d,\.]+)', "2,90"),
    "ap": int(get(r'Attack Power[,\s]+(\d+)', 150)),
    "crit": get(r'Crit Chance[,\s]+([\d,\.]+%)', "6,27%"),
    "haste": get(r'Haste[,\s]+([\d,\.]+%)', "0,00%"),
  },
  "spell": {
    "healing": int(get(r'Bonus Healing[,\s]+(\d+)', 0)),
    "damage": int(get(r'Bonus Damage[,\s]+(\d+)', 0)),
    "penetration": int(get(r'Penetration[,\s]+(\d+)', 0)),
    "mp5": int(get(r'Mana Regen[,\s]+(\d+)', 40)),
    "crit": get(r'Combat Regen.*?Crit Chance[,\s]+([\d,\.]+%)', "4,64%"),
  },
  "defense": {
    "armor": int(get(r'Armor[,\s]+(\d+)', 477)),
    "dodge": get(r'Dodge[,\s]+([\d,\.]+%)', "6,39%"),
    "parry": get(r'Parry[,\s]+([\d,\.]+%)', "0,00%"),
    "block": get(r'Block[,\s]+([\d,\.]+%)', "4,56%"),
    "defense": int(get(r'Defense[,\s]+(\d+)', 94)),
  }
}

with open("data.json","w") as f:
    json.dump(data,f,indent=2)
