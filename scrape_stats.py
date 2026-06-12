import requests, json, re
from bs4 import BeautifulSoup
from datetime import datetime, timezone

URL = "https://classic-armory.org/character/eu/tbc-anniversary/spineshatter/ozaxe"
headers = {"User-Agent":"Mozilla/5.0"}

html = requests.get(URL, headers=headers, timeout=20).text
soup = BeautifulSoup(html, "lxml")

data = {
    "updated": datetime.now(timezone.utc).isoformat(),
    "level": 20,
    "base": {},
    "melee": {},
    "spell": {},
    "defense": {},
    "gear": []
}

# --- stats (comme avant) ---
def text_after(label):
    el = soup.find(string=re.compile(label, re.I))
    if not el: return ""
    # cherche le prochain nombre
    nxt = el.find_parent().find_next_sibling()
    return nxt.get_text(strip=True) if nxt else ""

for k in ["health","mana","stamina","strength","agility","intellect","spirit"]:
    v = text_after(k)
    if v: data["base"][k] = v

for k in ["damage","speed","ap","crit","haste"]:
    v = text_after(k)
    if v: data["melee"][k] = v

for k in ["healing","damage","penetration","mp5","crit"]:
    v = text_after(k)
    if v: data["spell"][k] = v

for k in ["armor","dodge","parry","block","defense"]:
    v = text_after(k)
    if v: data["defense"][k] = v

# --- GEAR : parse tous les items ---
# Classic Armory met les items dans des <a class="item"> avec data-quality
for a in soup.select("a.item, div.item-slot a,.gear-slot a"):
    name = a.get("data-name") or a.get("title") or a.text.strip()
    icon = ""
    img = a.find("img")
    if img and img.get("src"):
        icon = img["src"]
        if icon.startswith("//"): icon = "https:" + icon
    slot = a.get("data-slot") or a.parent.get("data-slot","")
    ilvl = a.get("data-ilvl","")
    quality = "epic" if "epic" in str(a.get("class")) else "rare" if "rare" in str(a.get("class")) else "uncommon"

    if name and len(name) > 2:
        data["gear"].append({
            "slot": slot.lower(),
            "name": name,
            "ilvl": ilvl,
            "icon": icon,
            "quality": quality
        })

# tri dans l'ordre WoW
order = ["head","neck","shoulder","back","chest","shirt","tabard","wrist","hands","waist","legs","feet","finger1","finger2","trinket1","trinket2","mainhand","offhand","ranged"]
data["gear"] = sorted(data["gear"], key=lambda x: order.index(x["slot"]) if x["slot"] in order else 99)

with open("data.json","w",encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"OK - {len(data['gear'])} items scraped")
