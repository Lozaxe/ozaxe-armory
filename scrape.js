<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Ozaxe - Armurerie Live</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0b1018;color:#e6edf3;font-family:system-ui;margin:0;padding:2rem}
.card{background:#131b26;padding:1.5rem;border-radius:16px;margin-bottom:1rem}
h1{color:#0070de}
.mono{font-family:ui-monospace}
</style>
</head>
<body>
<h1>Ozaxe <span style="font-size:14px;color:#999">Spineshatter • lvl <span id="lvl">20</span></span></h1>
<div class="card">
  <div>Force: <b id="force">68</b> • Agi: <b id="agi">48</b> • Endu: <b id="endu">69</b></div>
  <div>Dégâts: <b id="dmg">79-104</b> • Crit: <b id="crit">11.11%</b> • PA: <b id="pa">156</b></div>
  <div>Minage: <b id="minage">90/150</b> • Joa: <b id="joa">54/75</b></div>
  <div style="margin-top:8px;font-size:12px;color:#888">Dernière maj: <span id="updated">-</span></div>
</div>
<div class="card" id="gear">Chargement...</div>
<script>
async function load(){
  try{
    const r = await fetch('data.json?'+Date.now());
    const d = await r.json();
    document.getElementById('lvl').textContent = d.level||20;
    document.getElementById('force').textContent = d.stats?.force||68;
    document.getElementById('agi').textContent = d.stats?.agility||48;
    document.getElementById('endu').textContent = d.stats?.stamina||69;
    document.getElementById('dmg').textContent = d.melee?.damage||'79-104';
    document.getElementById('crit').textContent = d.melee?.crit||'11.11%';
    document.getElementById('pa').textContent = d.melee?.ap||156;
    document.getElementById('minage').textContent = d.professions?.mining||'90/150';
    document.getElementById('joa').textContent = d.professions?.jc||'54/75';
    document.getElementById('updated').textContent = new Date(d.updated*1000).toLocaleString('fr-FR');
    document.getElementById('gear').innerHTML = '<b>Stuff:</b> ' + (d.gear||[]).join(' • ');
  }catch(e){}
}
load();
setInterval(load,30000);
</script>
</body>
</html>
