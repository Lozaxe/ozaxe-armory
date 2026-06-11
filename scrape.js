const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let data = {};
  try { data = JSON.parse(fs.readFileSync('data.json','utf8')); } catch(e){}
  data.history = data.history || [];

  try {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.goto('https://classic-armory.org/character/eu/tbc-anniversary/spineshatter/ozaxe', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(10000);

    const txt = await page.evaluate(() => document.body.innerText);
    const get = (re) => Number((txt.match(re)||[])[1]?.replace(',','.')) || 0;
    const gear = await page.evaluate(() => [...document.querySelectorAll('img')].filter(i=>i.src.includes('inv_')||i.src.includes('wow.zamimg')).slice(0,16).map(i=>({name:i.alt||'Item', icon:i.src})));

    const now = Math.floor(Date.now()/1000);
    const level = get(/Level\s+(\d+)/i) || data.level || 20;
    const strength = get(/Strength\D+(\d+)/i) || data.stats?.strength || 68;

    data = {
     ...data,
      name: "Ozaxe",
      level,
      race: "Orc",
      class: "Chaman", // ← corrigé
      spec: "Amélioration", // mets Élém/Resto si tu veux
      stats: {
        strength,
        stamina: get(/Stamina\D+(\d+)/i) || data.stats?.stamina || 0,
        agility: get(/Agility\D+(\d+)/i) || data.stats?.agility || 0,
        crit: get(/Crit\D+([\d.,]+)/i) || data.stats?.crit || 11.11,
        ap: get(/Attack Power\D+(\d+)/i) || data.stats?.ap || 0,
      },
      professions: {
        mining: get(/Mining\D+(\d+)/i) || data.professions?.mining || 90,
        jewelcrafting: get(/Jewelcrafting\D+(\d+)/i) || data.professions?.jewelcrafting || 54
      },
      gear: gear.length? gear : data.gear || [],
      updated: now,
      history: [...data.history, { t: now, level, str: strength }]
               .filter(h => h.t > now - 7*24*3600) // garde 7 jours
    };
    await browser.close();
  } catch(e){ data.updated = Math.floor(Date.now()/1000); }

  fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
})();
