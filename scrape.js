const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ userAgent: 'Mozilla/5.0' });
  await page.goto('https://classic-armory.org/character/eu/tbc-anniversary/spineshatter/ozaxe', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);

  const html = await page.content();
  const get = (re) => (html.match(re)?.[1] || '').trim();

  const data = {
    name: "Ozaxe",
    level: Number(get(/Level\s+(\d+)/i)) || 20,
    race: "Orc",
    class: "Warrior",
    spec: "Arms",
    stats: {
      strength: Number(get(/Strength\D+(\d+)/i)) || 68,
      crit: Number(get(/Crit\D+([\d.,]+)/i).replace(',','.')) || 11.11,
      ap: Number(get(/Attack Power\D+(\d+)/i)) || 0
    },
    professions: { mining: 90, jewelcrafting: 54 },
    updated: Math.floor(Date.now()/1000)
  };

  fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
  await browser.close();
  console.log('OK', data);
})();
