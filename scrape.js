const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ userAgent: 'Mozilla/5.0' });
  await page.goto('https://classic-armory.org/character/eu/tbc-anniversary/spineshatter/ozaxe', { waitUntil: 'networkidle' });
  await page.waitForTimeout(8000); // laisse le JS charger

  const data = await page.evaluate(() => {
    const txt = document.body.innerText;
    const num = (re) => Number((txt.match(re) || [])[1]?.replace(',','.')) || 0;

    // gear – prend toutes les icônes d'items
    const gear = [...document.querySelectorAll('img')].filter(i =>
      i.src.includes('wow.zamimg') || i.src.includes('render')
    ).map(i => ({
      name: i.alt || i.title || 'Item',
      icon: i.src,
      slot: i.closest('div')?.innerText?.slice(0,20) || ''
    })).filter((v,i,a)=> a.findIndex(t=>t.icon===v.icon)===i).slice(0,16);

    return {
      name: "Ozaxe",
      level: num(/Level\s+(\d+)/i) || 20,
      race: "Orc",
      class: "Warrior",
      spec: "Arms",
      stats: {
        strength: num(/Strength\D+(\d+)/i) || 68,
        agility: num(/Agility\D+(\d+)/i) || 0,
        stamina: num(/Stamina\D+(\d+)/i) || 0,
        crit: num(/Melee Crit\D+([\d.,]+)/i) || num(/Crit\D+([\d.,]+)/i) || 11.11,
        ap: num(/Attack Power\D+(\d+)/i) || 0,
        hit: num(/Hit Rating\D+(\d+)/i) || 0
      },
      professions: {
        mining: num(/Mining\D+(\d+)/i) || 90,
        jewelcrafting: num(/Jewelcrafting\D+(\d+)/i) || 54
      },
      gear,
      updated: Math.floor(Date.now()/1000)
    };
  });

  fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
  await browser.close();
  console.log('V2 OK', data.level, data.stats.strength);
})();
