#!/usr/bin/env python3
"""
OSRS SOULS v4 — Complete Standalone Single-File Game
DS2 Remastered Majula Graphics + OSRS Mechanics + Xbox Gamepad
Run: python SS.py
"""
import http.server, threading, webbrowser, io, socket, struct, hashlib, base64, json

GAME_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SOUL SCAPE v5</title>
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;overflow:hidden;font-family:'Segoe UI',sans-serif;color:#ddd;cursor:default}
canvas{display:block}
#bars{position:absolute;top:16px;left:16px;z-index:100;pointer-events:none;width:260px}
.bar-row{display:flex;align-items:center;margin-bottom:4px;font-size:11px;letter-spacing:.5px}
.bar-label{width:28px;text-align:right;margin-right:6px;font-weight:700;color:#aaa;font-size:10px}
.bar-bg{flex:1;height:16px;background:rgba(0,0,0,.7);border:1px solid #555;border-radius:2px;overflow:hidden;position:relative}
.bar-fill{height:100%;transition:width .15s}
.bar-text{position:absolute;right:6px;top:0;line-height:16px;font-size:10px;color:#fff;text-shadow:1px 1px 2px #000}
.hp-fill{background:linear-gradient(90deg,#7a1a1a,#cc2020)}
.sta-fill{background:linear-gradient(90deg,#1a5a1a,#33aa33)}
.poi-fill{background:linear-gradient(90deg,#2a2a6a,#4444cc)}
/* === OSRS RIGHT PANEL === */
#osrs-panel{position:fixed;top:0;right:0;width:245px;height:100vh;z-index:300;display:none;flex-direction:column;pointer-events:auto}
#minimap-wrap{width:245px;height:168px;background:#2b2016;border:3px solid #5a4a32;border-top:0;position:relative;overflow:hidden}
#minimap-canvas{width:100%;height:100%;border-radius:0}
#minimap-orbs{position:absolute;top:8px;right:8px;display:flex;flex-direction:column;gap:6px}
.orb{width:30px;height:30px;border-radius:50%;border:2px solid #5a4a32;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;text-shadow:0 0 2px #000}
.orb-hp{background:radial-gradient(circle,#cc2020,#5a0a0a);color:#fff}
.orb-pray{background:radial-gradient(circle,#3388ee,#1a2a5a);color:#fff}
.orb-run{background:radial-gradient(circle,#ccaa22,#5a4a0a);color:#fff}
#tab-strip{display:flex;background:#3b3020;border:2px solid #5a4a32;border-top:0}
.tab-btn{flex:1;padding:5px 0;text-align:center;cursor:pointer;font-size:14px;background:#3b3020;border-right:1px solid #4a3a28;transition:background .15s;line-height:1}
.tab-btn:last-child{border-right:0}
.tab-btn:hover{background:#4a3a28}
.tab-btn.active{background:#564830;box-shadow:inset 0 -2px 0 #c8a96e}
#tab-content{flex:1;background:#3b3020;border:2px solid #5a4a32;border-top:0;overflow-y:auto;padding:0}
#tab-content::-webkit-scrollbar{width:4px}#tab-content::-webkit-scrollbar-thumb{background:#5a4a32;border-radius:2px}
.tab-page{display:none;padding:6px}
.tab-page.active{display:block}
/* Skills tab */
.sk-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2px}
.sk-cell{background:#2b2016;border:1px solid #4a3a28;padding:3px 2px;text-align:center;cursor:default;position:relative}
.sk-cell .sk-ico{font-size:16px;display:block;line-height:1}
.sk-cell .sk-name{font-size:7px;color:#aa9;display:block;white-space:nowrap;overflow:hidden}
.sk-cell .sk-lv{font-size:13px;font-weight:700;color:#ffdd44;display:block}
.sk-cell .sk-xp{font-size:6px;color:#665;display:block}
.sk-total{text-align:center;padding:4px;font-size:11px;color:#ffcc44;background:#2b2016;border:1px solid #4a3a28;margin-top:3px;font-weight:700}
/* Inventory tab */
.inv-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:2px}
.inv-slot{width:52px;height:52px;background:#2b2016;border:1px solid #4a3a28;display:flex;align-items:center;justify-content:center;font-size:8px;color:#aa9;text-align:center;line-height:1.1;cursor:default}
.inv-slot:hover{border-color:#c8a96e}
/* Equipment tab */
.eq-grid{display:flex;flex-direction:column;align-items:center;gap:3px;padding:6px}
.eq-row{display:flex;gap:3px}
.eq-slot{width:50px;height:50px;background:#2b2016;border:1px solid #4a3a28;display:flex;align-items:center;justify-content:center;font-size:8px;color:#aa9;text-align:center;flex-direction:column;cursor:default}
.eq-slot .eq-ico{font-size:16px}
.eq-slot .eq-name{font-size:7px;color:#cc9944;white-space:nowrap;overflow:hidden;max-width:48px}
.eq-stats{font-size:9px;color:#aa9;text-align:center;margin-top:4px;padding:4px;background:#2b2016;border:1px solid #4a3a28}
.eq-stats span{color:#ffcc44}
/* Combat tab */
.cmb-info{padding:8px;text-align:center}
.cmb-info .cmb-lv{font-size:28px;color:#ffcc44;font-weight:700}
.cmb-info .cmb-lbl{font-size:10px;color:#887}
.cmb-row{display:flex;justify-content:space-between;padding:3px 8px;font-size:10px;border-bottom:1px solid #3a2a1a}
.cmb-row span:first-child{color:#aa9}.cmb-row span:last-child{color:#ffdd44;font-weight:700}
/* Prayer tab */
.pray-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:2px}
.pray-slot{width:42px;height:42px;background:#2b2016;border:1px solid #4a3a28;display:flex;align-items:center;justify-content:center;font-size:18px;cursor:pointer;opacity:.5}
.pray-slot.unlocked{opacity:1}
.pray-slot.pray-active{border-color:#ffcc44;background:#3a3018;box-shadow:0 0 6px rgba(255,200,50,.3)}
/* Magic tab */
.magic-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:2px}
.spell-slot{width:50px;height:44px;background:#2b2016;border:1px solid #4a3a28;display:flex;align-items:center;justify-content:center;font-size:16px;cursor:pointer;flex-direction:column;opacity:.5}
.spell-slot.unlocked{opacity:1}
.spell-slot .sp-name{font-size:6px;color:#88a}
/* Chat box */
#chatbox{position:fixed;bottom:0;left:0;width:calc(100% - 250px);height:150px;z-index:300;display:none;flex-direction:column;background:#1a1610;border:2px solid #5a4a32;border-bottom:0;border-left:0}
#chat-log{flex:1;overflow-y:auto;padding:4px 8px;font-size:10px;font-family:monospace;color:#887}
#chat-log::-webkit-scrollbar{width:3px}#chat-log::-webkit-scrollbar-thumb{background:#5a4a32}
#chat-tabs{display:flex;background:#2b2016;border-top:1px solid #4a3a28}
.chat-tab{padding:3px 10px;font-size:10px;color:#887;cursor:pointer;border-right:1px solid #3a2a1a}
.chat-tab.active{color:#ffcc44;background:#3b3020}
.chat-tab:hover{color:#cc9944}
/* Target Frame (WoW-style) */
#target-frame{position:fixed;top:16px;left:50%;transform:translateX(-50%);z-index:200;background:rgba(20,16,10,.92);border:2px solid #5a4a32;border-radius:4px;padding:6px 14px;display:none;align-items:center;gap:10px;min-width:220px}
#target-frame.active{display:flex}
#tf-icon{font-size:28px;line-height:1}
#tf-info{flex:1}
#tf-name{font-size:13px;color:#ff8844;font-weight:700;white-space:nowrap}
#tf-lv{font-size:10px;color:#aa9;margin-left:6px}
#tf-hp-bg{width:100%;height:10px;background:#220000;border:1px solid #555;border-radius:2px;margin-top:3px;overflow:hidden}
#tf-hp-fill{height:100%;background:linear-gradient(90deg,#7a1a1a,#cc2020);transition:width .15s}
#tf-hp-text{font-size:9px;color:#ccc;text-align:center;margin-top:1px}
/* World Map Overlay */
#world-map{position:fixed;inset:0;z-index:800;display:none;background:rgba(10,8,5,.95);flex-direction:column;align-items:center;justify-content:center}
#world-map.active{display:flex}
#wm-title{font-family:'Times New Roman',serif;font-size:28px;color:#c8a96e;letter-spacing:6px;margin-bottom:8px}
#wm-canvas{border:3px solid #5a4a32;cursor:crosshair}
#wm-close{position:absolute;top:16px;right:24px;font-size:24px;color:#887;cursor:pointer}#wm-close:hover{color:#e8d4a8}
#wm-coords{font-size:11px;color:#887;margin-top:8px;letter-spacing:1px}
#death-overlay{position:absolute;inset:0;background:rgba(0,0,0,0);z-index:500;display:flex;align-items:center;justify-content:center;pointer-events:none;transition:background .8s}
#death-overlay.active{background:rgba(0,0,0,.85)}
#death-text{font-size:52px;color:#8b0000;font-family:'Times New Roman',serif;letter-spacing:12px;opacity:0;transition:opacity 1s;text-shadow:0 0 30px rgba(139,0,0,.6)}
#death-overlay.active #death-text{opacity:1}
#controls{position:absolute;bottom:160px;left:50%;transform:translateX(-50%);z-index:100;font-size:10px;color:#665;text-align:center;pointer-events:none;background:rgba(0,0,0,.5);padding:4px 12px;border-radius:3px}
#locbar{position:absolute;top:80px;left:16px;z-index:100;font-size:11px;color:#aa9;pointer-events:none}
#main-menu{position:fixed;inset:0;z-index:9000;background:#000;display:flex;flex-direction:column;align-items:center;justify-content:center;transition:opacity 1s}
#main-menu.hidden{opacity:0;pointer-events:none}
#menu-title{font-family:'Times New Roman',serif;font-size:78px;color:#c8a96e;letter-spacing:16px;text-shadow:0 0 40px rgba(200,160,80,.3);margin-bottom:8px}
#menu-title span{color:#e8d4a8}
#menu-sub{font-size:11px;color:#554;letter-spacing:6px;margin-bottom:50px}
.menu-line{width:300px;height:1px;background:linear-gradient(90deg,transparent,#665530,transparent);margin-bottom:35px}
.mi{font-family:'Times New Roman',serif;font-size:21px;color:#887;padding:7px 0;cursor:pointer;letter-spacing:3px;text-align:center;transition:color .2s}
.mi:hover{color:#e8d4a8;text-shadow:0 0 20px rgba(200,160,80,.4)}.mi.dim{color:#443;pointer-events:none}
#menu-footer{position:absolute;bottom:28px;font-size:10px;color:#443;letter-spacing:2px}
#menu-ver{position:absolute;top:18px;right:28px;font-size:11px;color:#665;text-align:right}
.opts-panel{position:fixed;inset:0;z-index:9500;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center}
.opts-panel.show{display:flex}
.opts-box{width:520px;background:#1a1714;border:2px solid #554430;border-radius:4px;padding:22px 28px}
.opts-box h2{font-family:'Times New Roman',serif;font-size:18px;color:#c8a96e;letter-spacing:3px;margin-bottom:14px;padding-bottom:6px;border-bottom:1px solid #332818}
.opt-row{display:flex;align-items:center;justify-content:space-between;padding:5px 0;border-bottom:1px solid #1a1510;font-size:13px}
.opt-row span{color:#aa9}.opt-val{color:#c8a96e;cursor:pointer;font-size:13px}.opt-val:hover{color:#e8d4a8}
input[type=range]{-webkit-appearance:none;width:160px;height:5px;background:#332818;border-radius:3px;outline:none}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:12px;height:12px;background:#c8a050;border-radius:50%;cursor:pointer}
.opts-btn{display:inline-block;margin-top:14px;padding:7px 22px;font-family:'Times New Roman',serif;font-size:13px;color:#aa9;border:1px solid #443;cursor:pointer;letter-spacing:2px}.opts-btn:hover{color:#e8d4a8;border-color:#886}
#char-create{position:fixed;inset:0;z-index:9200;background:rgba(0,0,0,.95);display:none;align-items:center;justify-content:center;flex-direction:column}
#char-create.show{display:flex}
#char-create h2{font-family:'Times New Roman',serif;font-size:26px;color:#c8a96e;letter-spacing:5px;margin-bottom:24px}
.class-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.class-card{width:130px;padding:16px 10px;background:#1a1714;border:2px solid #443;border-radius:4px;text-align:center;cursor:pointer;transition:border-color .2s}
.class-card:hover{border-color:#c8a96e;background:#2a2418}
.class-card h3{font-family:'Times New Roman',serif;color:#c8a96e;font-size:15px;margin-bottom:4px}
.class-card p{font-size:9px;color:#887}.class-card .cst{font-size:10px;color:#aa9;margin-top:6px}
#game-ui{display:none}
</style>
</head>
<body>
<div id="main-menu"><div id="menu-ver">Ver. 2.0<br>SoulScape</div>
<div id="menu-title">SOUL<span>SCAPE</span></div><div id="menu-sub">AN OSRS × DARK SOULS EXPERIENCE</div><div class="menu-line"></div>
<div class="mi" data-a="new">New Game</div><div class="mi" data-a="cont">Continue</div><div class="mi" data-a="so">Screen Options</div><div class="mi" data-a="go">Game Options</div><div class="mi" data-a="q">Quit Game</div>
<div id="menu-footer">SOUL SCAPE v2.0 — Standalone Engine</div></div>
<div id="screen-opts" class="opts-panel"><div class="opts-box"><h2>Screen Options</h2>
<div class="opt-row"><span>Blood</span><div class="opt-val" data-o="blood">On</div></div>
<div class="opt-row"><span>Particles</span><div class="opt-val" data-o="part">On</div></div>
<div class="opt-row"><span>HUD</span><div class="opt-val" data-o="hud">Always Display</div></div>
<div class="opt-row"><span>Shadows</span><div class="opt-val" data-o="shad">High</div></div>
<div class="opt-row"><span>Adjust Brightness</span><input type="range" min="50" max="200" value="115" id="bright-s"></div>
<div style="text-align:center"><div class="opts-btn" id="scr-back">Back</div></div></div></div>
<div id="game-opts" class="opts-panel"><div class="opts-box"><h2>Game Options</h2>
<div class="opt-row"><span>Camera: Flip Y-axis</span><div class="opt-val" data-o="fy">Normal</div></div>
<div class="opt-row"><span>Camera: Flip X-axis</span><div class="opt-val" data-o="fx">Normal</div></div>
<div class="opt-row"><span>Camera Sensitivity</span><input type="range" min="1" max="20" value="5" id="sens-s"></div>
<div class="opt-row"><span>Auto Lock-on</span><div class="opt-val" data-o="al">On</div></div>
<div class="opt-row"><span>Bloom Effects</span><div class="opt-val" data-o="bl">On</div></div>
<div class="opt-row"><span>Music Volume</span><input type="range" min="0" max="100" value="70"></div>
<div class="opt-row"><span>SFX Volume</span><input type="range" min="0" max="100" value="80"></div>
<div style="text-align:center"><div class="opts-btn" id="gm-back">Back</div></div></div></div>
<div id="char-create"><h2>Choose Your Class</h2><div class="class-grid">
<div class="class-card" data-c="warrior"><h3>Warrior</h3><p>Battle-hardened fighter.</p><div class="cst">STR 14 DEF 12<br>HP 160 STA 110</div></div>
<div class="class-card" data-c="knight"><h3>Knight</h3><p>Noble balanced combatant.</p><div class="cst">STR 11 DEF 16<br>HP 180 STA 90</div></div>
<div class="class-card" data-c="sorcerer"><h3>Sorcerer</h3><p>Master of arcane arts.</p><div class="cst">MAG 16 INT 14<br>HP 100 POI 140</div></div>
<div class="class-card" data-c="deprived"><h3>Deprived</h3><p>Naked. True challenge.</p><div class="cst">ALL 6<br>HP 80 STA 80</div></div>
</div></div>
<div id="game-ui">
<div id="bars">
<div class="bar-row"><span class="bar-label">HP</span><div class="bar-bg"><div class="bar-fill hp-fill" id="hpB" style="width:100%"></div><span class="bar-text" id="hpT">142/142</span></div></div>
<div class="bar-row"><span class="bar-label">STA</span><div class="bar-bg"><div class="bar-fill sta-fill" id="stB" style="width:100%"></div><span class="bar-text" id="stT">100/100</span></div></div>
<div class="bar-row"><span class="bar-label">POI</span><div class="bar-bg"><div class="bar-fill poi-fill" id="poB" style="width:100%"></div><span class="bar-text" id="poT">68/68</span></div></div>
</div>
<div id="locbar">Lv 3 &#183; Majula</div>
<!-- OSRS RIGHT PANEL -->
<div id="osrs-panel">
<div id="minimap-wrap"><canvas id="minimap-canvas"></canvas>
<div id="minimap-orbs"><div class="orb orb-hp" id="orb-hp">99</div><div class="orb orb-pray" id="orb-pray">1</div><div class="orb orb-run" id="orb-run">100</div></div></div>
<div id="tab-strip">
<div class="tab-btn active" data-tab="combat" title="Combat">&#9876;</div>
<div class="tab-btn" data-tab="skills" title="Skills">&#9733;</div>
<div class="tab-btn" data-tab="quests" title="Quests">&#9776;</div>
<div class="tab-btn" data-tab="inventory" title="Inventory">&#127890;</div>
<div class="tab-btn" data-tab="equipment" title="Equipment">&#128737;</div>
<div class="tab-btn" data-tab="prayer" title="Prayer">&#10013;</div>
<div class="tab-btn" data-tab="magic" title="Magic">&#10024;</div>
<div class="tab-btn" data-tab="settings" title="Settings">&#9881;</div>
</div>
<div id="tab-content">
<div class="tab-page active" id="tp-combat"><div class="cmb-info"><div class="cmb-lbl">Combat Level</div><div class="cmb-lv" id="cmb-lv">3</div></div>
<div class="cmb-row"><span>Attack</span><span id="cmb-atk">1</span></div>
<div class="cmb-row"><span>Strength</span><span id="cmb-str">1</span></div>
<div class="cmb-row"><span>Defence</span><span id="cmb-def">1</span></div>
<div class="cmb-row"><span>Hitpoints</span><span id="cmb-hp">10</span></div>
<div class="cmb-row"><span>Ranged</span><span id="cmb-rng">1</span></div>
<div class="cmb-row"><span>Prayer</span><span id="cmb-pray">1</span></div>
<div class="cmb-row"><span>Magic</span><span id="cmb-mag">1</span></div>
<div class="cmb-row"><span>Gear ATK</span><span id="cmb-gatk">0</span></div>
<div class="cmb-row"><span>Gear DEF</span><span id="cmb-gdef">0</span></div>
<div class="cmb-row"><span>Gear STR</span><span id="cmb-gstr">0</span></div>
</div>
<div class="tab-page" id="tp-skills"><div class="sk-grid" id="skill-grid"></div><div class="sk-total" id="sk-total">Total Level: 19</div></div>
<div class="tab-page" id="tp-quests"><div style="padding:8px;font-size:10px;color:#aa9"><b style="color:#cc9944">Quest List</b><br><br>&#9744; Cook's Assistant<br>&#9744; Sheep Shearer<br>&#9744; Romeo & Juliet<br>&#9744; Doric's Quest<br>&#9744; Rune Mysteries<br>&#9744; Imp Catcher<br>&#9744; Witch's Potion<br>&#9744; The Restless Ghost<br>&#9744; Vampire Slayer<br>&#9744; Dragon Slayer</div></div>
<div class="tab-page" id="tp-inventory"><div class="inv-grid" id="inv-grid"></div></div>
<div class="tab-page" id="tp-equipment">
<div class="eq-grid">
<div class="eq-row"><div class="eq-slot" id="eq-Helm"><span class="eq-ico">&#9748;</span><span class="eq-name">Helm</span></div></div>
<div class="eq-row"><div class="eq-slot" id="eq-Weapon"><span class="eq-ico">&#9876;</span><span class="eq-name">Weapon</span></div><div class="eq-slot" id="eq-Chest"><span class="eq-ico">&#128085;</span><span class="eq-name">Chest</span></div><div class="eq-slot" id="eq-Shield"><span class="eq-ico">&#128737;</span><span class="eq-name">Shield</span></div></div>
<div class="eq-row"><div class="eq-slot" id="eq-Legs"><span class="eq-ico">&#128086;</span><span class="eq-name">Legs</span></div></div>
<div class="eq-row"><div class="eq-slot" id="eq-Gloves"><span class="eq-ico">&#9995;</span><span class="eq-name">Gloves</span></div><div class="eq-slot" id="eq-Boots"><span class="eq-ico">&#128095;</span><span class="eq-name">Boots</span></div><div class="eq-slot" id="eq-Ring"><span class="eq-ico">&#128141;</span><span class="eq-name">Ring</span></div></div>
</div>
<div class="eq-stats" id="eq-stats">ATK: <span id="es-atk">0</span> DEF: <span id="es-def">0</span> STR: <span id="es-str">0</span></div>
</div>
<div class="tab-page" id="tp-prayer">
<div style="padding:4px;font-size:10px;color:#aa9;text-align:center;margin-bottom:4px">Prayer Points: <b id="pray-pts">1</b></div>
<div class="pray-grid">
<div class="pray-slot unlocked" data-pr="thickskin" title="Thick Skin (+5% Def)">&#128170;</div>
<div class="pray-slot unlocked" data-pr="burst" title="Burst of Str (+5% Str)">&#9889;</div>
<div class="pray-slot unlocked" data-pr="clarity" title="Clarity (+5% Atk)">&#128161;</div>
<div class="pray-slot" data-pr="rockskin" title="Rock Skin (+10% Def)">&#129704;</div>
<div class="pray-slot" data-pr="superhuman" title="Superhuman Str (+10% Str)">&#128293;</div>
<div class="pray-slot" data-pr="improve" title="Improved Reflexes (+10% Atk)">&#128065;</div>
<div class="pray-slot" data-pr="rapid" title="Rapid Restore">&#10084;</div>
<div class="pray-slot" data-pr="rapid_heal" title="Rapid Heal">&#128147;</div>
<div class="pray-slot" data-pr="protect_item" title="Protect Item">&#128176;</div>
<div class="pray-slot" data-pr="steel_skin" title="Steel Skin (+15% Def)">&#129529;</div>
<div class="pray-slot" data-pr="ultimate" title="Ultimate Str (+15% Str)">&#128165;</div>
<div class="pray-slot" data-pr="incredible" title="Incredible Reflexes (+15% Atk)">&#127942;</div>
<div class="pray-slot" data-pr="protect_magic" title="Protect from Magic">&#128302;</div>
<div class="pray-slot" data-pr="protect_range" title="Protect from Range">&#127993;</div>
<div class="pray-slot" data-pr="protect_melee" title="Protect from Melee">&#9876;</div>
</div></div>
<div class="tab-page" id="tp-magic">
<div style="padding:4px;font-size:10px;color:#88a;text-align:center;margin-bottom:4px">Magic Level: <b id="mag-lv">1</b></div>
<div class="magic-grid">
<div class="spell-slot unlocked" title="Wind Strike">&#127744;<span class="sp-name">Wind Strike</span></div>
<div class="spell-slot unlocked" title="Confuse">&#128171;<span class="sp-name">Confuse</span></div>
<div class="spell-slot" title="Water Strike">&#128167;<span class="sp-name">Water Strike</span></div>
<div class="spell-slot" title="Enchant Lv1">&#128142;<span class="sp-name">Enchant 1</span></div>
<div class="spell-slot" title="Earth Strike">&#127760;<span class="sp-name">Earth Strike</span></div>
<div class="spell-slot" title="Weaken">&#128128;<span class="sp-name">Weaken</span></div>
<div class="spell-slot" title="Fire Strike">&#128293;<span class="sp-name">Fire Strike</span></div>
<div class="spell-slot" title="Bones to Bananas">&#127820;<span class="sp-name">Bones2Ban</span></div>
<div class="spell-slot" title="Wind Bolt">&#127786;<span class="sp-name">Wind Bolt</span></div>
<div class="spell-slot" title="Curse">&#128520;<span class="sp-name">Curse</span></div>
<div class="spell-slot" title="Low Alchemy">&#129689;<span class="sp-name">Low Alch</span></div>
<div class="spell-slot" title="Teleport Lumbridge">&#9889;<span class="sp-name">TP Lumb</span></div>
<div class="spell-slot" title="Water Bolt">&#128166;<span class="sp-name">Water Bolt</span></div>
<div class="spell-slot" title="Teleport Varrock">&#9889;<span class="sp-name">TP Varr</span></div>
<div class="spell-slot" title="High Alchemy">&#129689;<span class="sp-name">High Alch</span></div>
<div class="spell-slot" title="Fire Blast">&#9762;<span class="sp-name">Fire Blast</span></div>
</div></div>
<div class="tab-page" id="tp-settings"><div style="padding:8px;font-size:10px;color:#aa9"><b style="color:#cc9944">Controls</b><br><br><b style="color:#cc9944">Mouse:</b><br>LClick - Attack / Target<br>RClick - Block / Parry<br>MClick+Drag - Camera<br>Scroll - Zoom<br><br><b style="color:#cc9944">Keys:</b><br>WASD - Move<br>Space - Roll<br>Tab - Cycle Lock-on<br>1 - Attack<br>2 - Parry<br>3 - Heal (Estus)<br>4 - Bury Bones<br>Q - Prayer Tab<br>F - Gather/Skill<br>M - World Map<br>Esc - Deselect / Close Map<br>I - Inventory<br>K - Skills<br>F5 - Save<br><br><b style="color:#cc9944">Gamepad:</b><br>LStick - Move<br>RStick - Camera<br>RT/X - Attack<br>LT/B - Block<br>A - Roll<br>RB - Lock-on<br>LB - Stamina<br>Start - Inventory<br>Back - Skills</div></div>
</div>
</div>
<!-- CHAT BOX -->
<div id="chatbox">
<div id="chat-log">Welcome to SoulScape!</div>
<div id="chat-tabs">
<div class="chat-tab active">All</div>
<div class="chat-tab">Game</div>
<div class="chat-tab">Public</div>
<div class="chat-tab">Private</div>
<div class="chat-tab">Clan</div>
</div>
</div>
<div id="controls">WASD Move &#183; Scroll Zoom &#183; LMB Attack/Target &#183; RMB Block &#183; MMB Camera &#183; Space Roll &#183; Tab Lock &#183; 1 Atk &#183; 2 Parry &#183; 3 Heal &#183; 4 Bones &#183; Q Prayer &#183; F Gather &#183; M Map &#183; Esc Deselect</div>
<div id="target-frame"><div id="tf-icon">👹</div><div id="tf-info"><div><span id="tf-name">Enemy</span><span id="tf-lv">Lv 1</span></div><div id="tf-hp-bg"><div id="tf-hp-fill" style="width:100%"></div></div><div id="tf-hp-text">100/100</div></div></div>
<div id="world-map"><div id="wm-title">WORLD MAP</div><canvas id="wm-canvas" width="900" height="700"></canvas><div id="wm-coords">Player: 0, 0</div><div id="wm-close">&times;</div></div>
<div id="death-overlay"><span id="death-text">YOU DIED</span></div>
</div>
<script type="importmap">{"imports":{"three":"https://unpkg.com/three@0.158.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.158.0/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';
import{EffectComposer}from'three/addons/postprocessing/EffectComposer.js';
import{RenderPass}from'three/addons/postprocessing/RenderPass.js';
import{UnrealBloomPass}from'three/addons/postprocessing/UnrealBloomPass.js';

function mkTex(w,h,fn){const c=document.createElement('canvas');c.width=w;c.height=h;fn(c.getContext('2d'),w,h);const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;return t}
const texDirt=mkTex(512,512,(c,w,h)=>{c.fillStyle='#8a7a5a';c.fillRect(0,0,w,h);for(let i=0;i<10000;i++){const v=100+Math.random()*80;c.fillStyle=`rgb(${v+20},${v+10},${v-20})`;c.fillRect(Math.random()*w,Math.random()*h,1+Math.random()*3,1+Math.random()*3)}});texDirt.repeat.set(20,20);
const texStone=mkTex(256,256,(c,w,h)=>{c.fillStyle='#9a9080';c.fillRect(0,0,w,h);for(let i=0;i<1200;i++){const v=120+Math.random()*60;c.fillStyle=`rgb(${v+10},${v+5},${v-10})`;c.fillRect(Math.random()*w,Math.random()*h,2+Math.random()*10,2+Math.random()*10)}c.strokeStyle='#706050';c.lineWidth=2;for(let y=0;y<h;y+=28){c.beginPath();c.moveTo(0,y);c.lineTo(w,y);c.stroke();for(let x=(Math.floor(y/28)%2)*14;x<w;x+=28){c.beginPath();c.moveTo(x,y);c.lineTo(x,y+28);c.stroke()}}});
const texBark=mkTex(64,128,(c,w,h)=>{c.fillStyle='#2a1a0e';c.fillRect(0,0,w,h);for(let y=0;y<h;y+=2){const b=30+Math.random()*25;c.fillStyle=`rgb(${b+12},${b},${b-8})`;c.fillRect(0,y,w,2)}});
const texWood=mkTex(128,128,(c,w,h)=>{c.fillStyle='#5a4530';c.fillRect(0,0,w,h);for(let y=0;y<h;y+=3){const b=50+Math.random()*40;c.fillStyle=`rgb(${b+20},${b+10},${b-10})`;c.fillRect(0,y,w,3)}});

const MS=THREE.MeshStandardMaterial;
const mt={
gnd:new MS({map:texDirt,roughness:.92}),st:new MS({map:texStone,roughness:.82,metalness:.04}),
stD:new MS({map:texStone,color:0x777068,roughness:.88}),bk:new MS({map:texBark,roughness:.9}),
lf:new MS({color:0x1a3a18,roughness:.85,flatShading:true}),lfL:new MS({color:0x2a4a20,roughness:.8,flatShading:true}),
wd:new MS({map:texWood,roughness:.85}),rf:new MS({color:0x8a7a50,roughness:.95}),
wt:new MS({color:0x1a4a5a,roughness:.12,metalness:.55,transparent:true,opacity:.7,side:THREE.DoubleSide,emissive:0x0a2a3a,emissiveIntensity:.2}),
fl:new MS({color:0xff6600,emissive:0xff4400,emissiveIntensity:3,roughness:1}),
rk:new MS({color:0xb0a890,roughness:.88}),rkD:new MS({color:0x8a7a68,roughness:.9}),
armorDk:new MS({color:0x2a2a30,roughness:.4,metalness:.8}),
armorLt:new MS({color:0x4a4a55,roughness:.45,metalness:.7}),
chainmail:new MS({color:0x3a3a40,roughness:.5,metalness:.6}),
skin:new MS({color:0xc4a882,roughness:.8}),
cape:new MS({color:0x6a2020,roughness:.85,side:THREE.DoubleSide}),
swordBlade:new MS({color:0xccc,roughness:.12,metalness:.95,emissive:0x111,emissiveIntensity:.1}),
swordHilt:new MS({color:0x5a4020,roughness:.7,metalness:.3}),
};
function eMat(t){return new MS({color:t==='goblin'?0x2a5a28:t==='cow'?0x7a4a2a:0xcca855,roughness:.7,metalness:.08})}

const skillDefs=['Attack','Strength','Defence','Hitpoints','Ranged','Prayer','Magic','Cooking','Woodcutting','Fishing','Mining','Smithing','Crafting','Firemaking','Herblore','Agility','Thieving','Slayer','Runecraft'];
const skillIcons={Attack:'\u2694',Strength:'\uD83D\uDCAA',Defence:'\uD83D\uDEE1',Hitpoints:'\u2764',Ranged:'\uD83C\uDFF9',Prayer:'\u271D',Magic:'\u2728',Cooking:'\uD83C\uDF56',Woodcutting:'\uD83E\uDE93',Fishing:'\uD83C\uDFA3',Mining:'\u26CF',Smithing:'\uD83D\uDD28',Crafting:'\u2702',Firemaking:'\uD83D\uDD25',Herblore:'\uD83C\uDF3F',Agility:'\uD83C\uDFC3',Thieving:'\uD83D\uDC4B',Slayer:'\uD83D\uDC80',Runecraft:'\uD83D\uDD2E'};
const skills={};skillDefs.forEach(s=>skills[s]={lvl:1,xp:0});skills.Hitpoints.lvl=10;skills.Hitpoints.xp=1154;skills.Attack.lvl=3;skills.Attack.xp=174;skills.Strength.lvl=2;skills.Strength.xp=83;skills.Defence.lvl=2;skills.Defence.xp=83;
const sgEl=document.getElementById('skill-grid');
skillDefs.forEach(s=>{const d=document.createElement('div');d.className='sk-cell';d.id='sk-'+s;d.innerHTML=`<span class="sk-ico">${skillIcons[s]||''}</span><span class="sk-name">${s}</span><span class="sk-lv">${skills[s].lvl}</span><span class="sk-xp">${skills[s].xp}xp</span>`;sgEl.appendChild(d)});
const invEl=document.getElementById('inv-grid');
for(let i=0;i<28;i++){const d=document.createElement('div');d.className='inv-slot';d.id='inv-'+i;invEl.appendChild(d)}
const inventory=[];function updateInvUI(){for(let i=0;i<28;i++){document.getElementById('inv-'+i).textContent=inventory[i]||''}}

// === TAB SWITCHING ===
document.querySelectorAll('.tab-btn').forEach(btn=>btn.addEventListener('click',()=>{
document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));
btn.classList.add('active');
const tp=document.getElementById('tp-'+btn.dataset.tab);if(tp)tp.classList.add('active')}));

// === LOG -> CHAT-LOG ===
function log(msg,col){const el=document.getElementById('chat-log');if(!el)return;const d=document.createElement('div');d.style.color=col||'#887';d.textContent=msg;el.appendChild(d);el.scrollTop=el.scrollHeight}

// === EQUIPMENT UI UPDATE ===
function updateEqUI(){
const gs=totalGear();
document.getElementById('es-atk').textContent=gs.atk;
document.getElementById('es-def').textContent=gs.def;
document.getElementById('es-str').textContent=gs.str;
gearSlots.forEach(s=>{const el=document.getElementById('eq-'+s);if(el){el.querySelector('.eq-name').textContent=equipped[s].name||s}});
document.getElementById('cmb-gatk').textContent=gs.atk;
document.getElementById('cmb-gdef').textContent=gs.def;
document.getElementById('cmb-gstr').textContent=gs.str}

// === UPDATE SKILL CELLS + COMBAT TAB ===
function updateSkillUI(){
const totalLv=skillDefs.reduce((a,s)=>a+skills[s].lvl,0);
document.getElementById('sk-total').textContent='Total Level: '+totalLv;
skillDefs.forEach(s=>{const el=document.getElementById('sk-'+s);if(el){el.querySelector('.sk-lv').textContent=skills[s].lvl;el.querySelector('.sk-xp').textContent=skills[s].xp+'xp'}});
document.getElementById('cmb-lv').textContent=Math.floor((skills.Attack.lvl+skills.Strength.lvl+skills.Defence.lvl+skills.Hitpoints.lvl+skills.Prayer.lvl+skills.Magic.lvl+skills.Ranged.lvl)/4);
document.getElementById('cmb-atk').textContent=skills.Attack.lvl;document.getElementById('cmb-str').textContent=skills.Strength.lvl;
document.getElementById('cmb-def').textContent=skills.Defence.lvl;document.getElementById('cmb-hp').textContent=skills.Hitpoints.lvl;
document.getElementById('cmb-rng').textContent=skills.Ranged.lvl;document.getElementById('cmb-pray').textContent=skills.Prayer.lvl;
document.getElementById('cmb-mag').textContent=skills.Magic.lvl;document.getElementById('mag-lv').textContent=skills.Magic.lvl;
document.getElementById('pray-pts').textContent=skills.Prayer.lvl}

// === PRAYER TOGGLE ===
const activePrayers=new Set();
document.querySelectorAll('.pray-slot.unlocked').forEach(el=>el.addEventListener('click',()=>{
const pr=el.dataset.pr;if(activePrayers.has(pr)){activePrayers.delete(pr);el.classList.remove('pray-active')}
else{activePrayers.add(pr);el.classList.add('pray-active')}
log('Prayer: '+(activePrayers.has(pr)?'ON':'OFF')+' '+el.title,'#cc4')}));

// === MINIMAP ===
const mmCanvas=document.getElementById('minimap-canvas');const mmCtx=mmCanvas.getContext('2d');
mmCanvas.width=245;mmCanvas.height=168;
function drawMinimap(){
mmCtx.fillStyle='#2b2016';mmCtx.fillRect(0,0,245,168);
const scale=.12,cx=122,cy=84;
// Draw regions as colored zones
regions.forEach(r=>{const rx=(r.x-player.x)*scale+cx,rz=(r.z-player.z)*scale+cy;
mmCtx.fillStyle='rgba('+(r.fog>>16)+','+((r.fog>>8)&0xff)+','+(r.fog&0xff)+',0.4)';
mmCtx.beginPath();mmCtx.arc(rx,rz,r.r*scale,0,Math.PI*2);mmCtx.fill()});
// Draw enemies as red dots
enemies.forEach(e=>{const ex=(e.mesh.position.x-player.x)*scale+cx,ez=(e.mesh.position.z-player.z)*scale+cy;
if(ex>2&&ex<243&&ez>2&&ez<166){mmCtx.fillStyle='#cc2020';mmCtx.fillRect(ex-1,ez-1,3,3)}});
// Player arrow
mmCtx.fillStyle='#fff';mmCtx.save();mmCtx.translate(cx,cy);mmCtx.rotate(-player.ang);
mmCtx.beginPath();mmCtx.moveTo(0,-5);mmCtx.lineTo(-3,4);mmCtx.lineTo(3,4);mmCtx.fill();mmCtx.restore();
// Compass
mmCtx.fillStyle='#aa9';mmCtx.font='8px sans-serif';mmCtx.textAlign='center';mmCtx.fillText('N',cx,10);mmCtx.fillText('S',cx,164)}

// === CLICK-TO-TARGET (WoW style) ===
const raycaster=new THREE.Raycaster();
const clickMouse=new THREE.Vector2();
let targetRing=null;
function initTargetRing(){
const rGeo=new THREE.RingGeometry(3.5,4.2,32);const rMat=new THREE.MeshBasicMaterial({color:0xff4444,side:THREE.DoubleSide,transparent:true,opacity:.55});
targetRing=new THREE.Mesh(rGeo,rMat);targetRing.rotation.x=-Math.PI/2;targetRing.visible=false;
}
function updateTargetFrame(){
const tf=document.getElementById('target-frame');
if(!lockOn||!lockOn.mesh){tf.classList.remove('active');if(targetRing)targetRing.visible=false;return}
tf.classList.add('active');
const icons={goblin:'\uD83D\uDC7A',cow:'\uD83D\uDC2E',chicken:'\uD83D\uDC14',guard:'\u2694',darkwiz:'\uD83E\uDDD9',revenant:'\uD83D\uDC7B',skeleton:'\uD83D\uDC80',demon:'\uD83D\uDC79',scorpion:'\uD83E\uDD82',warrior:'\u2694',whiteknight:'\u2694',dwarf:'\u26CF',barbarian:'\uD83E\uDE93',vampire:'\uD83E\uDDDB',zombie:'\uD83E\uDDDF',pirate:'\uD83C\uDFF4',mugger:'\uD83D\uDC64',troll:'\uD83E\uDDCC',ogre:'\uD83D\uDC79',drake:'\uD83D\uDC09',bear:'\uD83D\uDC3B',wolf:'\uD83D\uDC3A',spider:'\uD83D\uDD77',bat:'\uD83E\uDD87',ghost:'\uD83D\uDC7B',golem:'\uD83E\uDEA8',wyrm:'\uD83D\uDC32',shade:'\uD83D\uDC7E',hellhound:'\uD83D\uDD25',imp:'\uD83D\uDC7F',bandit:'\uD83D\uDDE1',rat:'\uD83D\uDC00',snake:'\uD83D\uDC0D',lizard:'\uD83E\uDD8E',elemental:'\uD83C\uDF0A',gargoyle:'\uD83E\uDEA8',knight:'\u2694',mage:'\uD83E\uDDD9',archer:'\uD83C\uDFF9',cultist:'\uD83D\uDD2E'};
document.getElementById('tf-icon').textContent=icons[lockOn.type]||'\uD83D\uDC7E';
document.getElementById('tf-name').textContent=lockOn.type.charAt(0).toUpperCase()+lockOn.type.slice(1);
document.getElementById('tf-lv').textContent='Lv '+(lockOn.lv||1);
const pct=Math.max(0,lockOn.hp/lockOn.maxHp*100);
document.getElementById('tf-hp-fill').style.width=pct+'%';
document.getElementById('tf-hp-text').textContent=Math.max(0,~~lockOn.hp)+'/'+lockOn.maxHp;
if(targetRing&&lockOn.mesh){targetRing.visible=true;targetRing.position.copy(lockOn.mesh.position);targetRing.position.y+=.5;
const sc=1+Math.sin(time*4)*.15;targetRing.scale.set(sc,sc,sc)}
}
function clickTarget(e){
if(!gameStarted||!cam||e.button!==0)return;
clickMouse.x=(e.clientX/innerWidth)*2-1;clickMouse.y=-(e.clientY/innerHeight)*2+1;
raycaster.setFromCamera(clickMouse,cam);
let closest=null,cDist=Infinity;
for(const en of enemies){const hits=raycaster.intersectObject(en.mesh,true);
if(hits.length>0&&hits[0].distance<cDist){cDist=hits[0].distance;closest=en}}
if(closest){lockOn=closest;lockIdx=enemies.indexOf(closest);log('Targeted: '+closest.type+' (Lv'+(closest.lv||1)+')','#f84')}
}

// === WORLD MAP ===
const wmCanvas=document.getElementById('wm-canvas');const wmCtx=wmCanvas.getContext('2d');
function drawWorldMap(){
const W=900,H=700;wmCtx.fillStyle='#0a0805';wmCtx.fillRect(0,0,W,H);
const scale=W/16000,ox=W/2,oy=H/2;
// Draw regions
regions.forEach(r=>{
const rx=r.x*scale+ox,ry=r.z*scale+oy;
const rr=r.r*scale;
const cr=(r.fog>>16)/255,cg=((r.fog>>8)&0xff)/255,cb=(r.fog&0xff)/255;
wmCtx.fillStyle=`rgba(${~~(cr*255)},${~~(cg*255)},${~~(cb*255)},0.5)`;
wmCtx.beginPath();wmCtx.arc(rx,ry,Math.max(rr,8),0,Math.PI*2);wmCtx.fill();
wmCtx.strokeStyle='#5a4a32';wmCtx.lineWidth=1;wmCtx.stroke();
wmCtx.fillStyle='#c8a96e';wmCtx.font='bold 10px sans-serif';wmCtx.textAlign='center';
wmCtx.fillText(r.n,rx,ry-rr-4);
wmCtx.fillStyle='#887';wmCtx.font='8px sans-serif';
wmCtx.fillText('Lv '+r.lv+'+',rx,ry+4)});
// Enemies as tiny dots
enemies.forEach(e=>{const ex=e.mesh.position.x*scale+ox,ey=e.mesh.position.z*scale+oy;
wmCtx.fillStyle='#cc2020';wmCtx.fillRect(ex-1,ey-1,2,2)});
// Player
const px=player.x*scale+ox,py=player.z*scale+oy;
wmCtx.fillStyle='#fff';wmCtx.beginPath();wmCtx.arc(px,py,5,0,Math.PI*2);wmCtx.fill();
wmCtx.strokeStyle='#ffcc44';wmCtx.lineWidth=2;wmCtx.stroke();
wmCtx.fillStyle='#ffcc44';wmCtx.font='bold 11px sans-serif';wmCtx.textAlign='center';
wmCtx.fillText('YOU',px,py-9);
// Grid
wmCtx.strokeStyle='rgba(90,74,50,.2)';wmCtx.lineWidth=.5;
for(let gx=-8000;gx<=8000;gx+=1000){const sx=gx*scale+ox;wmCtx.beginPath();wmCtx.moveTo(sx,0);wmCtx.lineTo(sx,H);wmCtx.stroke()}
for(let gz=-8000;gz<=8000;gz+=1000){const sy=gz*scale+oy;wmCtx.beginPath();wmCtx.moveTo(0,sy);wmCtx.lineTo(W,sy);wmCtx.stroke()}
// Coords
document.getElementById('wm-coords').textContent='Player: '+~~player.x+', '+~~player.z+' \u00B7 '+getReg(player.x,player.z).n;
}
document.getElementById('wm-close').onclick=()=>{document.getElementById('world-map').classList.remove('active')};

let scene,cam,renderer,composer,riverMesh,playerGroup;
let enemies=[],lootArr=[],particles=[],torchData=[];
let dustPts,time=0;
const lightPool=[];const MAX_LIGHTS=8;
const torchPositions=[];
const solidMeshes=[];
const solidBoxes=[];
const PLAYER_R=2.2;
function addSolid(mesh){solidMeshes.push(mesh)}
function buildColliders(){
solidBoxes.length=0;
for(const m of solidMeshes){m.updateMatrixWorld(true);
const b=new THREE.Box3().setFromObject(m);solidBoxes.push(b)}
log('Colliders: '+solidBoxes.length+' objects','#0f0')}
function pushOut(px,py,pz){
let ox=px,oz=pz;
const pr=PLAYER_R;
for(let pass=0;pass<2;pass++){for(const b of solidBoxes){
const minX=b.min.x-pr,maxX=b.max.x+pr,minZ=b.min.z-pr,maxZ=b.max.z+pr;
if(ox>minX&&ox<maxX&&oz>minZ&&oz<maxZ&&py<b.max.y&&py>b.min.y-6){
const ovL=ox-minX,ovR=maxX-ox,ovB=oz-minZ,ovF=maxZ-oz;
const m=Math.min(ovL,ovR,ovB,ovF);
if(m===ovL)ox=minX;else if(m===ovR)ox=maxX;
else if(m===ovB)oz=minZ;else oz=maxZ}}}
return{x:ox,z:oz}}
let keys={},mouse={x:0,y:0,dx:0,dy:0,down:false,right:false,mid:false};
let camYaw=0,camPitch=.35,camDist=60;
let player={x:0,z:0,y:2,vx:0,vz:0,speed:.42,hp:142,maxHp:142,sta:100,maxSta:100,poi:68,maxPoi:68,ang:0,rolling:false,rollT:0,atkCD:0,dead:false,deadTimer:0,blocking:false};
let lockOn=null,lockIdx=-1;
let showSkills=false,showInv=false;
let gpAxes=[0,0,0,0],gpButtons={};

const drops={goblin:[{i:"Bronze Sword",c:.42},{i:"Coins x17",c:.68},{i:"Bones",c:1},{i:"Goblin Mail",c:.08}],
cow:[{i:"Raw Beef",c:1},{i:"Cowhide",c:.85},{i:"Coins x5",c:.4}],
chicken:[{i:"Raw Chicken",c:1},{i:"Feathers x12",c:.9},{i:"Bones",c:1}],
guard:[{i:"Iron Sword",c:.3},{i:"Coins x45",c:.8},{i:"Bread",c:.5}],
skeleton:[{i:"Bones",c:1},{i:"Iron Arrow x5",c:.6},{i:"Ancient Coin",c:.1}],
pirate:[{i:"Coins x30",c:.7},{i:"Rum",c:.4},{i:"Eye Patch",c:.05}],
barbarian:[{i:"Raw Meat",c:.8},{i:"Coins x12",c:.6},{i:"Bear Fur",c:.3}],
vampire:[{i:"Blood Rune",c:.4},{i:"Coins x60",c:.5},{i:"Garlic",c:.2}],
demon:[{i:"Dragon Bones",c:.8},{i:"Rune Scimitar",c:.05},{i:"Coins x200",c:.9}],
scorpion:[{i:"Coins x8",c:.5}],zombie:[{i:"Bones",c:1}]};

// log function defined above at line 326 using chat-log element

// === OSRS-INSPIRED WORLD REGIONS ===
const regions=[
// === ORIGINAL CORE (center) ===
{n:'Lumbridge',x:0,z:0,r:280,lv:1,c:[.48,.55,.28],en:['goblin','cow','chicken'],fog:0x9a8a6a},
{n:'Varrock',x:550,z:50,r:220,lv:15,c:[.48,.42,.32],en:['guard','darkwiz'],fog:0x8a7a5a},
{n:'Wilderness',x:0,z:-650,r:420,lv:50,c:[.14,.09,.07],en:['revenant','skeleton','demon'],fog:0x1a1210},
{n:'Al Kharid',x:580,z:400,r:260,lv:10,c:[.72,.58,.3],en:['scorpion','warrior'],fog:0xb8a870},
{n:'Falador',x:-480,z:280,r:240,lv:20,c:[.52,.52,.48],en:['whiteknight','dwarf'],fog:0xa0a098},
{n:'Barbarian Village',x:280,z:-250,r:180,lv:8,c:[.4,.33,.2],en:['barbarian'],fog:0x7a6a4a},
{n:'Draynor',x:-300,z:-150,r:200,lv:12,c:[.18,.24,.14],en:['vampire','zombie'],fog:0x2a3020},
{n:'Port Sarim',x:-160,z:480,r:220,lv:5,c:[.4,.48,.35],en:['pirate','mugger'],fog:0x8a9a8a},
{n:'Edgeville',x:150,z:-350,r:150,lv:25,c:[.35,.3,.22],en:['skeleton','guard'],fog:0x6a5a40},
{n:'Catherby',x:-500,z:-400,r:180,lv:18,c:[.3,.45,.28],en:['zombie'],fog:0x506848},
// === EXPANDED REGIONS ===
{n:'Ardougne',x:-1200,z:100,r:320,lv:25,c:[.42,.48,.35],en:['guard','knight','thief'],fog:0x8a9a7a},
{n:'Yanille',x:-1400,z:500,r:200,lv:30,c:[.38,.44,.32],en:['ogre','guard'],fog:0x7a8a6a},
{n:'Canifis',x:1300,z:-200,r:240,lv:35,c:[.12,.15,.1],en:['vampire','wolf','ghost'],fog:0x1a2218},
{n:'Morytania',x:1600,z:-400,r:350,lv:40,c:[.1,.12,.08],en:['ghost','shade','vampire'],fog:0x141a10},
{n:'Karamja',x:-200,z:1800,r:400,lv:15,c:[.35,.55,.2],en:['spider','snake','tribesman'],fog:0x6a9a50},
{n:'Brimhaven',x:-500,z:2200,r:280,lv:20,c:[.3,.48,.18],en:['spider','drake','snake'],fog:0x5a8a40},
{n:'Trollheim',x:-200,z:-3500,r:350,lv:55,c:[.3,.28,.22],en:['troll','wolf'],fog:0x5a5040},
{n:'God Wars',x:0,z:-4500,r:400,lv:80,c:[.15,.12,.2],en:['demon','golem','wyrm'],fog:0x201828},
{n:'Deep Wilderness',x:0,z:-1800,r:500,lv:65,c:[.08,.06,.04],en:['revenant','hellhound','demon'],fog:0x0a0808},
{n:'Seers Village',x:-800,z:-100,r:220,lv:22,c:[.42,.5,.35],en:['guard','mage'],fog:0x8a9a7a},
{n:'Rellekka',x:-400,z:-3800,r:300,lv:45,c:[.32,.35,.38],en:['troll','barbarian','wolf'],fog:0x5a6068},
{n:'Keldagrim',x:-800,z:-3200,r:250,lv:50,c:[.38,.32,.28],en:['dwarf','golem'],fog:0x6a5848},
{n:'Mos Le Harmless',x:500,z:2500,r:300,lv:25,c:[.5,.55,.3],en:['pirate','snake','spider'],fog:0x9a9a60},
{n:'Desert Plateau',x:2000,z:600,r:400,lv:35,c:[.75,.6,.32],en:['scorpion','mummy','warrior'],fog:0xc0a070},
{n:'Sophanem',x:2500,z:200,r:260,lv:40,c:[.7,.55,.28],en:['mummy','scarab','snake'],fog:0xb09060},
{n:'Menaphos',x:3000,z:400,r:300,lv:50,c:[.68,.52,.25],en:['mummy','warrior','mage'],fog:0xa88850},
{n:'Tirannwn',x:-3500,z:0,r:450,lv:55,c:[.2,.4,.15],en:['elf','wolf','bear'],fog:0x3a6a28},
{n:'Prifddinas',x:-4000,z:-300,r:300,lv:70,c:[.45,.55,.5],en:['elf','knight','mage'],fog:0x8aaa98},
{n:'Fossil Island',x:2500,z:-1500,r:300,lv:45,c:[.35,.42,.25],en:['wyrm','spider','lizard'],fog:0x6a7a50},
{n:'Zeah Hosidius',x:-2000,z:1200,r:350,lv:15,c:[.5,.55,.3],en:['lizard','chicken','cow'],fog:0x9a9a6a},
{n:'Zeah Shayzien',x:-2500,z:800,r:300,lv:35,c:[.35,.32,.28],en:['knight','warrior','guard'],fog:0x6a5a48},
{n:'Zeah Lovakengj',x:-2800,z:1600,r:280,lv:40,c:[.25,.22,.2],en:['dwarf','golem','bat'],fog:0x4a3a30},
{n:'Zeah Arceuus',x:-2200,z:1800,r:250,lv:50,c:[.18,.15,.25],en:['ghost','shade','cultist'],fog:0x2a2040},
{n:'Zanaris',x:800,z:800,r:200,lv:30,c:[.25,.4,.45],en:['imp','fairy','spider'],fog:0x4a7a8a},
{n:'TzHaar City',x:1800,z:1200,r:250,lv:60,c:[.5,.15,.08],en:['tzhaar','imp','elemental'],fog:0x8a2010}
];
const eHP={goblin:32,cow:45,chicken:18,guard:80,darkwiz:65,revenant:120,skeleton:60,demon:160,scorpion:40,warrior:55,whiteknight:90,dwarf:70,barbarian:50,vampire:85,zombie:45,pirate:55,mugger:30,
troll:140,ogre:110,drake:180,bear:95,wolf:65,spider:50,bat:28,ghost:75,golem:200,wyrm:220,shade:90,hellhound:150,imp:35,bandit:70,rat:15,snake:40,lizard:45,elemental:160,gargoyle:190,knight:100,mage:85,archer:70,cultist:95,thief:40,tribesman:55,mummy:130,scarab:60,elf:120,fairy:30,tzhaar:250};
const eCol={goblin:0x2a5a28,cow:0x7a4a2a,chicken:0xcca855,guard:0x4444aa,darkwiz:0x2a0a3a,revenant:0x1a4a3a,skeleton:0xccccaa,demon:0x5a1010,scorpion:0x4a3a10,warrior:0x886830,whiteknight:0xcccccc,dwarf:0x886644,barbarian:0x8a5a30,vampire:0x2a0a1a,zombie:0x3a5a30,pirate:0x554430,mugger:0x3a3a3a,
troll:0x5a5a4a,ogre:0x4a6a30,drake:0x6a3020,bear:0x4a3020,wolf:0x555555,spider:0x2a2a20,bat:0x3a3040,ghost:0x6a8aaa,golem:0x5a5a60,wyrm:0x4a2040,shade:0x2a2a3a,hellhound:0x5a2010,imp:0x8a2020,bandit:0x4a4030,rat:0x5a4a3a,snake:0x2a4a20,lizard:0x4a6a30,elemental:0x2a4a6a,gargoyle:0x5a5a5a,knight:0x6a6a7a,mage:0x3a3a6a,archer:0x4a5a3a,cultist:0x3a1a3a,thief:0x3a3a3a,tribesman:0x5a4a2a,mummy:0x8a7a5a,scarab:0x2a3a1a,elf:0x4a6a5a,fairy:0x6a8aaa,tzhaar:0x8a3010};
function getReg(x,z){let b=regions[0],d=1e9;for(const r of regions){const dd=Math.hypot(x-r.x,z-r.z);if(dd<d){d=dd;b=r}}return b}
function biomeCol(x,z){const r=getReg(x,z),v=Math.sin(x*1.7+z*2.3)*.03;return[Math.max(0,Math.min(1,r.c[0]+v)),Math.max(0,Math.min(1,r.c[1]+v*.7)),Math.max(0,Math.min(1,r.c[2]+v*.5))]}

function terrainH(x,z){
let h=Math.sin(x*.006)*Math.cos(z*.006)*22+Math.sin(x*.02+z*.012)*8+Math.sin(x*.05)*Math.cos(z*.035)*3;
// Wilderness: rugged
if(z<-350&&z>-2000)h+=Math.sin(x*.08)*Math.cos(z*.06)*10+Math.abs(Math.sin(x*.15+z*.1))*6;
// Deep Wilderness: volcanic
if(z<-2000)h+=Math.sin(x*.04)*15+Math.abs(Math.sin(x*.1+z*.08))*20+Math.sin(z*.03)*10;
// Al Kharid desert: flat
if(x>350&&z>200&&x<2000)h=h*.25+Math.sin(x*.015+z*.02)*10+4;
// Coastal south: flatten near water
if(z>350&&z<1500)h*=Math.max(0,1-(z-350)/400);
// Falador plains: gentle
if(x<-200&&x>-1500&&z>-280&&z<500)h=h*.2+Math.sin(x*.03)*2;
// Northern mountains (Trollheim/GWD)
if(z<-3000)h+=40+Math.sin(x*.02)*30+Math.cos(z*.015)*25+Math.abs(Math.sin(x*.07+z*.05))*18;
// Eastern desert expanse
if(x>2000)h=h*.15+Math.sin(x*.008+z*.01)*6+2;
// Western ocean coast
if(x<-2000)h=h*.3-5+Math.sin(z*.02)*4;
// Morytania swamp (east-south)
if(x>1200&&z>-800&&z<200)h=h*.2-2+Math.sin(x*.04+z*.06)*3;
// Karamja jungle (south)
if(z>1500)h=Math.sin(x*.015)*15+Math.cos(z*.012)*10+Math.sin(x*.06+z*.04)*5+5;
// Tirannwn forest (far west)
if(x<-3000)h=15+Math.sin(x*.01)*20+Math.cos(z*.008)*15+Math.sin(x*.04+z*.03)*8;
// Fremennik mountains
if(x>-800&&x<200&&z<-3500)h+=50+Math.sin(x*.03)*20+Math.cos(z*.02)*30;
return h}

function buildKnight(){
const g=new THREE.Group();
const body=new THREE.Group();
// Helmet
const helm=new THREE.Mesh(new THREE.SphereGeometry(1.5,10,10),mt.armorDk);helm.position.y=9.5;helm.scale.set(1,1.2,.95);body.add(helm);
const v1=new THREE.Mesh(new THREE.BoxGeometry(1.6,.12,.3),new MS({color:0x080808,roughness:1}));v1.position.set(0,9.4,1.35);body.add(v1);
const v2=v1.clone();v2.position.y=9.1;v2.scale.x=.9;body.add(v2);
const plume=new THREE.Mesh(new THREE.BoxGeometry(.4,1.8,.6),mt.cape);plume.position.set(0,10.8,-.6);body.add(plume);
// Neck
const neck=new THREE.Mesh(new THREE.CylinderGeometry(.85,.95,1.2,8),mt.chainmail);neck.position.y=8.1;body.add(neck);
// Torso
const torso=new THREE.Mesh(new THREE.BoxGeometry(3.4,3.8,2),mt.armorDk);torso.position.y=6;body.add(torso);
const ridge=new THREE.Mesh(new THREE.BoxGeometry(.4,3,.3),mt.armorLt);ridge.position.set(0,6,1.1);body.add(ridge);
// Belt
const belt=new THREE.Mesh(new THREE.BoxGeometry(3.6,.5,2.2),mt.swordHilt);belt.position.y=3.9;body.add(belt);
const buckle=new THREE.Mesh(new THREE.BoxGeometry(.6,.4,.3),new MS({color:0xc8a050,roughness:.4,metalness:.7}));buckle.position.set(0,3.9,1.15);body.add(buckle);
// Left arm (shield) as sub-group for animation
const lArm=new THREE.Group();lArm.position.set(-2.4,7.8,0);
const sp1=new THREE.Mesh(new THREE.SphereGeometry(1.15,8,6),mt.armorLt);sp1.scale.set(1,.75,.85);lArm.add(sp1);
const gd1=new THREE.Mesh(new THREE.BoxGeometry(1.4,.3,1.2),mt.armorDk);gd1.position.y=.4;lArm.add(gd1);
const ua1=new THREE.Mesh(new THREE.CylinderGeometry(.5,.45,3.2,6),mt.chainmail);ua1.position.y=-2.6;lArm.add(ua1);
const el1=new THREE.Mesh(new THREE.SphereGeometry(.5,6,6),mt.armorDk);el1.position.y=-4.2;lArm.add(el1);
const fa1=new THREE.Mesh(new THREE.CylinderGeometry(.48,.42,2.8,6),mt.armorDk);fa1.position.y=-5.6;lArm.add(fa1);
const gt1=new THREE.Mesh(new THREE.BoxGeometry(.7,.4,.9),mt.armorDk);gt1.position.y=-7;lArm.add(gt1);
const shield=new THREE.Mesh(new THREE.BoxGeometry(.3,3.2,2.4),mt.shF);shield.position.set(-.4,-4.8,.2);lArm.add(shield);
const sBoss=new THREE.Mesh(new THREE.SphereGeometry(.4,6,6),mt.shT);sBoss.position.set(-.6,-4.8,.2);lArm.add(sBoss);
body.add(lArm);g.userData.lArm=lArm;
// Right arm (sword) as sub-group for animation
const rArm=new THREE.Group();rArm.position.set(2.4,7.8,0);
const sp2=new THREE.Mesh(new THREE.SphereGeometry(1.15,8,6),mt.armorLt);sp2.scale.set(1,.75,.85);rArm.add(sp2);
const gd2=new THREE.Mesh(new THREE.BoxGeometry(1.4,.3,1.2),mt.armorDk);gd2.position.y=.4;rArm.add(gd2);
const ua2=new THREE.Mesh(new THREE.CylinderGeometry(.5,.45,3.2,6),mt.chainmail);ua2.position.y=-2.6;rArm.add(ua2);
const el2=new THREE.Mesh(new THREE.SphereGeometry(.5,6,6),mt.armorDk);el2.position.y=-4.2;rArm.add(el2);
const fa2=new THREE.Mesh(new THREE.CylinderGeometry(.48,.42,2.8,6),mt.armorDk);fa2.position.y=-5.6;rArm.add(fa2);
const gt2=new THREE.Mesh(new THREE.BoxGeometry(.7,.4,.9),mt.armorDk);gt2.position.y=-7;rArm.add(gt2);
const blade=new THREE.Mesh(new THREE.BoxGeometry(.22,.22,7),mt.swordBlade);blade.position.set(0,-7,3.5);blade.rotation.x=.08;rArm.add(blade);
const xguard=new THREE.Mesh(new THREE.BoxGeometry(1.3,.2,.2),mt.swordHilt);xguard.position.set(0,-7,.15);rArm.add(xguard);
const hilt=new THREE.Mesh(new THREE.CylinderGeometry(.12,.12,1.2,5),mt.swordHilt);hilt.position.set(0,-7,-.3);hilt.rotation.x=Math.PI/2;rArm.add(hilt);
body.add(rArm);g.userData.rArm=rArm;
// Legs
[-1,1].forEach(s=>{
const thigh=new THREE.Mesh(new THREE.CylinderGeometry(.6,.5,2.8,6),mt.chainmail);thigh.position.set(s*.75,2.2,0);body.add(thigh);
const knee=new THREE.Mesh(new THREE.SphereGeometry(.55,6,6),mt.armorDk);knee.position.set(s*.75,.8,0);body.add(knee);
const kGuard=new THREE.Mesh(new THREE.BoxGeometry(.5,.5,.6),mt.armorLt);kGuard.position.set(s*.75,.8,.3);body.add(kGuard);
const shin=new THREE.Mesh(new THREE.CylinderGeometry(.5,.45,2.6,6),mt.armorDk);shin.position.set(s*.75,-.6,0);body.add(shin);
const boot=new THREE.Mesh(new THREE.BoxGeometry(.9,.7,1.5),mt.armorDk);boot.position.set(s*.75,-2.1,.15);body.add(boot);
});
// Cape
for(let i=0;i<3;i++){const seg=new THREE.Mesh(new THREE.PlaneGeometry(2.8-i*.3,2,1,2),mt.cape);seg.position.set(0,6.5-i*2,-1.1-i*.15);body.add(seg)}
body.traverse(c=>{if(c.isMesh)c.castShadow=true});
g.add(body);g.userData.body=body;
g.scale.setScalar(.55);
return g;
}

function init(){
scene=new THREE.Scene();scene.background=new THREE.Color(0x8a7a60);scene.fog=new THREE.FogExp2(0x9a8a6a,.0004);
cam=new THREE.PerspectiveCamera(62,innerWidth/innerHeight,.5,6000);
renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'high-performance'});
renderer.setSize(innerWidth,innerHeight);renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=gameOpts?gameOpts.bright:1.15;
renderer.outputColorSpace=THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);

scene.add(new THREE.AmbientLight(0x4a4030,.6));
const sun=new THREE.DirectionalLight(0xffeebb,1.8);sun.position.set(80,160,-60);sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.near=1;sun.shadow.camera.far=800;
sun.shadow.camera.left=-800;sun.shadow.camera.right=800;sun.shadow.camera.top=800;sun.shadow.camera.bottom=-800;sun.shadow.camera.far=3000;
sun.shadow.bias=-.0003;scene.add(sun);
scene.add(new THREE.DirectionalLight(0x6688aa,.3).translateX(-100).translateY(40).translateZ(80));
scene.add(new THREE.HemisphereLight(0x9a8a6a,0x3a2a18,.5));

// Extra materials for expanded world
mt.lava=new MS({color:0xff2200,emissive:0xff4400,emissiveIntensity:2,roughness:1});
mt.sand=new MS({color:0xd4b878,roughness:.95});
mt.stW=new MS({color:0xe0d8cc,roughness:.72,metalness:.05});
mt.bridge=new MS({map:texWood,roughness:.88,color:0x6a5540});
mt.rope=new MS({color:0x8a7a50,roughness:1});
mt.shF=new MS({color:0x3a3a40,roughness:.3,metalness:.8});
mt.shT=new MS({color:0xc8a050,roughness:.4,metalness:.7});

// Biome-colored terrain (16000x16000)
const gGeo=new THREE.PlaneGeometry(16000,16000,400,400);
const gp=gGeo.attributes.position;
const vc=new Float32Array(gp.count*3);
for(let i=0;i<gp.count;i++){const lx=gp.getX(i),lz=-gp.getY(i);gp.setZ(i,terrainH(lx,lz));const c=biomeCol(lx,lz);vc[i*3]=c[0];vc[i*3+1]=c[1];vc[i*3+2]=c[2]}
gGeo.setAttribute('color',new THREE.BufferAttribute(vc,3));
gGeo.computeVertexNormals();
const ground=new THREE.Mesh(gGeo,new MS({vertexColors:true,roughness:.92}));ground.rotation.x=-Math.PI/2;ground.receiveShadow=true;scene.add(ground);

// River running through the world
const rGeo=new THREE.PlaneGeometry(26,600,24,80);
riverMesh=new THREE.Mesh(rGeo,mt.wt);riverMesh.rotation.x=-Math.PI/2;riverMesh.position.set(220,.8,0);scene.add(riverMesh);
// Second river segment
const rGeo2=new THREE.PlaneGeometry(20,400,16,50);
const rv2=new THREE.Mesh(rGeo2,mt.wt);rv2.rotation.x=-Math.PI/2;rv2.position.set(-350,.6,-200);scene.add(rv2);

function arch(x,z,rot,sc){const s=sc||1,g=new THREE.Group();
const lp=new THREE.Mesh(new THREE.BoxGeometry(4*s,22*s,4*s),mt.st);lp.position.set(-6*s,11*s,0);lp.castShadow=true;g.add(lp);
const rp=lp.clone();rp.position.x=6*s;g.add(rp);
const top=new THREE.Mesh(new THREE.BoxGeometry(16*s,4*s,4*s),mt.st);top.position.set(0,24*s,0);top.castShadow=true;g.add(top);
for(let i=0;i<8;i++){const rb=new THREE.Mesh(new THREE.BoxGeometry(1+Math.random()*3,1+Math.random()*2,1+Math.random()*3),mt.stD);
rb.position.set((Math.random()-.5)*14*s,Math.random()*2,(Math.random()-.5)*6);rb.rotation.set(Math.random(),Math.random(),Math.random());rb.castShadow=true;g.add(rb)}
g.position.set(x,terrainH(x,z),z);g.rotation.y=rot||0;scene.add(g)}
// === WORLD BUILDER HELPERS ===
function wall(x,z,w,h,rot){const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,3),mt.st);m.position.set(x,terrainH(x,z)+h/2,z);m.rotation.y=rot||0;m.castShadow=true;scene.add(m);addSolid(m)}
function wallW(x,z,w,h,rot){const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,3),mt.stW);m.position.set(x,terrainH(x,z)+h/2,z);m.rotation.y=rot||0;m.castShadow=true;scene.add(m);addSolid(m)}
function hut(x,z,rot,s){s=s||1;const h=terrainH(x,z);const base=new THREE.Mesh(new THREE.BoxGeometry(12*s,8*s,10*s),mt.wd);base.position.set(x,h+4*s,z);base.rotation.y=rot||0;base.castShadow=true;scene.add(base);addSolid(base);const roof=new THREE.Mesh(new THREE.ConeGeometry(9*s,6*s,4),mt.rf);roof.position.set(x,h+11*s,z);roof.rotation.y=(rot||0)+.785;roof.castShadow=true;scene.add(roof)}
function tower(x,z,s,mat){s=s||1;mat=mat||mt.st;const h=terrainH(x,z);const b=new THREE.Mesh(new THREE.CylinderGeometry(6*s,7*s,30*s,8),mat);b.position.set(x,h+15*s,z);b.castShadow=true;scene.add(b);addSolid(b);const c=new THREE.Mesh(new THREE.ConeGeometry(8*s,10*s,8),mt.stD);c.position.set(x,h+33*s,z);c.castShadow=true;scene.add(c);const fm=new THREE.Mesh(new THREE.SphereGeometry(1.5,6,6),mt.fl);fm.position.set(x,h+30*s,z);scene.add(fm);torchPositions.push({x,y:h+30*s,z,mesh:fm,ph:Math.random()*6.28,big:false})}
function pine(x,z){const h=terrainH(x,z);const tr=new THREE.Mesh(new THREE.CylinderGeometry(1,1.8,14,6),mt.bk);tr.position.set(x,h+7,z);tr.castShadow=true;scene.add(tr);for(let i=0;i<5;i++){const cn=new THREE.Mesh(new THREE.ConeGeometry(7-i*1.2,6,8),i%2?mt.lfL:mt.lf);cn.position.set(x,h+12+i*3.5,z);cn.castShadow=true;scene.add(cn)}}
function palm(x,z){const h=terrainH(x,z);const tr=new THREE.Mesh(new THREE.CylinderGeometry(.6,1,16,6),mt.bk);tr.position.set(x,h+8,z);tr.rotation.z=Math.sin(x)*.15;tr.castShadow=true;scene.add(tr);for(let i=0;i<6;i++){const a=i/6*Math.PI*2;const f=new THREE.Mesh(new THREE.PlaneGeometry(8,2),mt.lf);f.position.set(x+Math.cos(a)*3,h+17,z+Math.sin(a)*3);f.rotation.set(-1,a,0);scene.add(f)}}
const dtMat=new MS({color:0x2a2018,roughness:.95}),dtMat2=new MS({color:0x3a2a18,roughness:.95});
function deadTree(x,z){const h=terrainH(x,z);const tr=new THREE.Mesh(new THREE.CylinderGeometry(.5,1.2,12,5),dtMat);tr.position.set(x,h+6,z);tr.castShadow=true;scene.add(tr);for(let i=0;i<3;i++){const br=new THREE.Mesh(new THREE.CylinderGeometry(.15,.3,5,4),dtMat2);br.position.set(x+(Math.random()-.5)*2,h+8+i*2,z+(Math.random()-.5)*2);br.rotation.set(Math.random(),Math.random(),.5+Math.random());br.castShadow=true;scene.add(br)}}
function bonfire(x,z){const h=terrainH(x,z);for(let i=0;i<10;i++){const a=i/10*Math.PI*2,r=4+Math.random();const rk=new THREE.Mesh(new THREE.IcosahedronGeometry(1.2,0),mt.rk);rk.position.set(x+Math.cos(a)*r,h+.6,z+Math.sin(a)*r);scene.add(rk)}const fm=new THREE.Mesh(new THREE.SphereGeometry(2,8,8),mt.fl);fm.position.set(x,h+3,z);scene.add(fm);torchPositions.push({x,y:h+5,z,mesh:fm,ph:0,big:true})}
function bridge(x,z,rot,len){const h=terrainH(x,z);const pl=new THREE.Mesh(new THREE.BoxGeometry(6,1,len),mt.bridge);pl.position.set(x,h+2,z);pl.rotation.y=rot;pl.castShadow=true;pl.receiveShadow=true;scene.add(pl);const cs=Math.cos(rot),sn=Math.sin(rot);for(let i=0;i<Math.floor(len/5);i++){const t=(i/(len/5-.1)-.5)*len;[-1,1].forEach(sd=>{const p=new THREE.Mesh(new THREE.CylinderGeometry(.2,.25,6,4),mt.wd);p.position.set(x+sn*t+cs*sd*3,h+5,z+cs*t-sn*sd*3);p.castShadow=true;scene.add(p)})}}
function ruin(x,z){const h=terrainH(x,z);for(let i=0;i<5;i++){const w=new THREE.Mesh(new THREE.BoxGeometry(3+Math.random()*6,6+Math.random()*14,3),mt.stD);w.position.set(x+(Math.random()-.5)*20,h+4+Math.random()*6,z+(Math.random()-.5)*20);w.rotation.set(Math.random()*.3,Math.random(),Math.random()*.3);w.castShadow=true;scene.add(w)}}
function torch(tx,tz){const th=terrainH(tx,tz);const post=new THREE.Mesh(new THREE.CylinderGeometry(.4,.6,10,5),mt.wd);post.position.set(tx,th+5,tz);post.castShadow=true;scene.add(post);const fm=new THREE.Mesh(new THREE.SphereGeometry(1.2,6,6),mt.fl);fm.position.set(tx,th+11,tz);scene.add(fm);torchPositions.push({x:tx,y:th+11,z:tz,mesh:fm,ph:Math.random()*6.28,big:false})}

// ========== LUMBRIDGE (0,0) ==========
arch(0,10,0,1.2);arch(-25,-15,.4,1);arch(20,-30,-.3,.9);arch(-10,25,.8,.7);
hut(40,30,.3,1.1);hut(60,15,-.4,1);hut(25,55,.8,.9);hut(55,50,-.2,1);hut(-30,60,.6,1);hut(-50,40,-.2,.9);
bonfire(0,5);wall(-40,-20,30,14,.2);wall(35,10,20,10,-.5);
tower(80,-50,1);tower(-60,-60,.8);
for(let i=0;i<4;i++)wall(-80+i*20,100,18,16,0);tower(-85,100,1.1);tower(-5,100,1.1);
hut(-45,120,.4,1.3);hut(-30,130,-.3,1);
[[30,20],[55,35],[15,45],[50,60],[70,10],[-30,-10],[-50,5],[-70,30],[80,30],[0,-40]].forEach(([x,z])=>torch(x,z));
// Lumbridge trees
for(let i=0;i<25;i++)pine(-80+Math.random()*40,20+Math.random()*100);
for(let i=0;i<25;i++)pine(80+Math.random()*60,-60+Math.random()*100);

// ========== VARROCK (550,50) ==========
for(let i=0;i<8;i++){wall(470+i*22,130,20,20,0);wall(470+i*22,-30,20,20,0)}
for(let i=0;i<8;i++){wall(467,130-i*22,3,20,0);wall(645,130-i*22,3,20,0)}
tower(465,130,1.3);tower(645,130,1.3);tower(465,-30,1.3);tower(645,-30,1.3);
arch(555,130,0,1.2);arch(555,-30,0,1.2);
for(let i=0;i<14;i++){const a=i/14*Math.PI*2;arch(550+Math.cos(a)*45,50+Math.sin(a)*45,a+1.57,.7)}
for(let i=0;i<6;i++){hut(500+i*24,70,Math.random()*2,.8);hut(500+i*24,30,Math.random()*2,.8)}
for(let i=0;i<3;i++)wall(540+i*16,10,14,24,0);tower(535,10,1.5);tower(575,10,1.5);
[490,520,560,590,620].forEach(x=>{torch(x,90);torch(x,10)});bonfire(555,50);
for(let i=0;i<15;i++)pine(460+Math.random()*200,140+Math.random()*60);

// ========== WILDERNESS (0,-650) ==========
for(let i=0;i<15;i++)ruin((Math.random()-.5)*400,-550-Math.random()*250);
for(let i=0;i<8;i++){const lx=(Math.random()-.5)*300,lz=-600-Math.random()*200;const lv=new THREE.Mesh(new THREE.CircleGeometry(6+Math.random()*8,12),mt.lava);lv.rotation.x=-Math.PI/2;lv.position.set(lx,terrainH(lx,lz)+.5,lz);scene.add(lv);torchPositions.push({x:lx,y:terrainH(lx,lz)+4,z:lz,mesh:lv,ph:Math.random()*6.28,big:true,col:0xff4400})}
for(let i=0;i<6;i++){wall(-40+i*16,-580,14,26,0);wall(-40+i*16,-520,14,26,0)}
tower(-45,-580,1.8);tower(55,-580,1.8);tower(-45,-520,1.8);tower(55,-520,1.8);
wall(-200,-400,400,4,0);
for(let i=0;i<20;i++)deadTree((Math.random()-.5)*350,-500-Math.random()*300);

// ========== AL KHARID (580,400) ==========
for(let i=0;i<6;i++){wall(530+i*18,350,16,14,0);wall(530+i*18,450,16,14,0)}
tower(525,350,1.2);tower(640,350,1.2);tower(525,450,1.2);tower(640,450,1.2);
arch(580,350,0,1);arch(580,450,0,1);
for(let i=0;i<6;i++)hut(540+i*18,380+Math.random()*40,Math.random()*2,1);
for(let i=0;i<20;i++)palm(520+Math.random()*120,340+Math.random()*120);
bonfire(580,400);[560,600].forEach(x=>{torch(x,370);torch(x,430)});

// ========== FALADOR (-480,280) ==========
for(let i=0;i<8;i++){wallW(-540+i*16,230,14,24,0);wallW(-540+i*16,330,14,24,0)}
for(let i=0;i<7;i++){wallW(-545,230+i*16,3,24,0);wallW(-415,230+i*16,3,24,0)}
tower(-545,230,1.6,mt.stW);tower(-415,230,1.6,mt.stW);tower(-545,330,1.6,mt.stW);tower(-415,330,1.6,mt.stW);
arch(-480,230,0,1.3);arch(-480,330,0,1.3);
for(let i=0;i<4;i++)hut(-520+i*25,270,Math.random()*2,1);
for(let i=0;i<4;i++)hut(-520+i*25,300,Math.random()*2,.9);
bonfire(-480,280);
for(let i=0;i<15;i++)pine(-550+Math.random()*30,220+Math.random()*120);
for(let i=0;i<15;i++)pine(-400+Math.random()*30,220+Math.random()*120);

// ========== BARBARIAN VILLAGE (280,-250) ==========
for(let i=0;i<6;i++)hut(250+i*18,-240+Math.random()*20,Math.random()*2,1.2);
for(let i=0;i<3;i++)hut(260+i*22,-270,Math.random()*2,1);
bonfire(280,-250);tower(310,-270,.8);
for(let i=0;i<8;i++)pine(240+Math.random()*80,-210+Math.random()*40);
[260,290,310].forEach(x=>torch(x,-240));

// ========== DRAYNOR (-300,-150) ==========
for(let i=0;i<12;i++)deadTree(-280+Math.random()*80,-120-Math.random()*80);
hut(-320,-160,1,.8);hut(-280,-180,-.5,.9);hut(-340,-140,.3,1);
// Draynor Manor
for(let i=0;i<3;i++)wall(-310+i*14,-100,12,18,0);
tower(-315,-100,1.2);tower(-280,-100,1.2);
bonfire(-300,-150);torch(-290,-130);torch(-310,-170);

// ========== PORT SARIM (-160,480) ==========
for(let i=0;i<5;i++)hut(-190+i*20,460+Math.random()*20,.5+Math.random(),1);
bridge(-160,420,0,40);bridge(-120,420,0,40);
// Docks
for(let i=0;i<8;i++){const dk=new THREE.Mesh(new THREE.CylinderGeometry(.5,.7,16,5),mt.wd);dk.position.set(-100+i*10,terrainH(-100+i*10,500)+4,500);dk.castShadow=true;scene.add(dk)}
// Ship hull
const hull=new THREE.Mesh(new THREE.BoxGeometry(14,6,30),mt.wd);hull.position.set(-30,terrainH(-30,510)+3,510);hull.castShadow=true;scene.add(hull);
const mast=new THREE.Mesh(new THREE.CylinderGeometry(.4,.6,30,5),mt.bk);mast.position.set(-30,terrainH(-30,510)+20,510);mast.castShadow=true;scene.add(mast);
bonfire(-160,470);[[-180,470],[-140,470],[-100,490]].forEach(([x,z])=>torch(x,z));

// ========== EDGEVILLE (150,-350) ==========
for(let i=0;i<4;i++)hut(130+i*18,-340+Math.random()*15,Math.random()*2,1);
wall(120,-360,60,12,0);tower(115,-360,1);tower(185,-360,1);
bonfire(155,-350);torch(140,-340);torch(170,-340);

// ========== CATHERBY (-500,-400) ==========
for(let i=0;i<5;i++)hut(-520+i*15,-390+Math.random()*15,Math.random()*2,.9);
for(let i=0;i<10;i++)pine(-540+Math.random()*80,-370-Math.random()*60);
bonfire(-500,-400);bridge(-460,-380,1.2,30);

// ========== ARDOUGNE (-1200,100) ==========
for(let i=0;i<10;i++){wall(-1280+i*18,30,16,20,0);wall(-1280+i*18,170,16,20,0)}
for(let i=0;i<8;i++){wall(-1285,30+i*20,3,20,0);wall(-1115,30+i*20,3,20,0)}
tower(-1285,30,1.5);tower(-1115,30,1.5);tower(-1285,170,1.5);tower(-1115,170,1.5);
arch(-1200,30,0,1.2);arch(-1200,170,0,1.2);
for(let i=0;i<10;i++)hut(-1260+i*16,80+Math.random()*60,Math.random()*2,1);
bonfire(-1200,100);for(let i=0;i<8;i++)torch(-1250+i*14,100);
for(let i=0;i<20;i++)pine(-1300+Math.random()*200,-20+Math.random()*50);

// ========== YANILLE (-1400,500) ==========
for(let i=0;i<6;i++){wall(-1440+i*16,460,14,18,0);wall(-1440+i*16,540,14,18,0)}
tower(-1445,460,1.3);tower(-1355,460,1.3);tower(-1445,540,1.3);tower(-1355,540,1.3);
for(let i=0;i<6;i++)hut(-1430+i*15,490+Math.random()*30,Math.random()*2,.9);
bonfire(-1400,500);

// ========== CANIFIS (1300,-200) ==========
for(let i=0;i<8;i++)hut(1260+i*14,-210+Math.random()*25,Math.random()*2,.8);
for(let i=0;i<15;i++)deadTree(1250+Math.random()*120,-250+Math.random()*100);
tower(1340,-180,1.2);bonfire(1300,-200);torch(1280,-190);torch(1320,-210);

// ========== MORYTANIA (1600,-400) ==========
for(let i=0;i<20;i++)deadTree(1500+Math.random()*250,-500+Math.random()*200);
for(let i=0;i<5;i++)ruin(1550+Math.random()*150,-450+Math.random()*120);
tower(1600,-400,1.5);tower(1650,-350,1);bonfire(1600,-400);
for(let i=0;i<4;i++)wall(1560+i*20,-460,18,16,0);

// ========== KARAMJA (-200,1800) ==========
for(let i=0;i<40;i++)palm(-350+Math.random()*300,1650+Math.random()*350);
for(let i=0;i<8;i++)hut(-250+i*18,1780+Math.random()*30,Math.random()*2,1);
bonfire(-200,1800);bridge(-180,1650,0,40);
for(let i=0;i<6;i++)torch(-260+i*20,1800);

// ========== BRIMHAVEN (-500,2200) ==========
for(let i=0;i<30;i++)palm(-600+Math.random()*200,2100+Math.random()*200);
for(let i=0;i<6;i++)hut(-540+i*16,2190+Math.random()*25,Math.random()*2,.9);
tower(-500,2180,1.3);bonfire(-500,2200);cave(-520,2250,.4);

// ========== TROLLHEIM (-200,-3500) ==========
for(let i=0;i<10;i++)ruin(-300+Math.random()*200,-3550+Math.random()*100);
for(let i=0;i<6;i++)tower(-280+i*30,-3480,1+Math.random()*.5);
wall(-250,-3550,200,30,0);bonfire(-200,-3500);
for(let i=0;i<8;i++)deadTree(-300+Math.random()*200,-3400+Math.random()*80);

// ========== GOD WARS (0,-4500) ==========
for(let i=0;i<12;i++)ruin(-200+Math.random()*400,-4600+Math.random()*200);
for(let i=0;i<8;i++){const lx=-150+Math.random()*300,lz=-4550+Math.random()*150;const lv=new THREE.Mesh(new THREE.CircleGeometry(6+Math.random()*10,12),mt.lava);lv.rotation.x=-Math.PI/2;lv.position.set(lx,terrainH(lx,lz)+.5,lz);scene.add(lv);torchPositions.push({x:lx,y:terrainH(lx,lz)+4,z:lz,mesh:lv,ph:Math.random()*6.28,big:true,col:0xff2200})}
tower(-50,-4500,2.5);tower(50,-4500,2.5);tower(0,-4400,2);
for(let i=0;i<6;i++)wall(-80+i*30,-4380,28,35,0);

// ========== DEEP WILDERNESS (0,-1800) ==========
for(let i=0;i<25;i++)ruin(-300+Math.random()*600,-1900+Math.random()*300);
for(let i=0;i<30;i++)deadTree(-350+Math.random()*700,-1950+Math.random()*350);
for(let i=0;i<6;i++){const lx=-200+Math.random()*400,lz=-1850+Math.random()*200;const lv=new THREE.Mesh(new THREE.CircleGeometry(5+Math.random()*6,12),mt.lava);lv.rotation.x=-Math.PI/2;lv.position.set(lx,terrainH(lx,lz)+.5,lz);scene.add(lv)}
wall(-200,-1500,400,6,0);

// ========== SEERS VILLAGE (-800,-100) ==========
for(let i=0;i<8;i++)hut(-850+i*16,-110+Math.random()*20,Math.random()*2,1);
tower(-820,-80,1.2);tower(-760,-120,1);
for(let i=0;i<15;i++)pine(-880+Math.random()*160,-150+Math.random()*100);
bonfire(-800,-100);[[-810,-90],[-790,-110],[-770,-90],[-830,-110]].forEach(([x,z])=>torch(x,z));

// ========== RELLEKKA (-400,-3800) ==========
for(let i=0;i<10;i++)hut(-450+i*16,-3810+Math.random()*25,Math.random()*2,1.2);
for(let i=0;i<6;i++)wall(-460+i*20,-3850,18,14,0);
tower(-465,-3850,1.4);tower(-345,-3850,1.4);
bonfire(-400,-3800);for(let i=0;i<8;i++)pine(-480+Math.random()*160,-3750+Math.random()*40);

// ========== KELDAGRIM (-800,-3200) ==========
for(let i=0;i<8;i++)wall(-850+i*14,-3230,12,30,0);
for(let i=0;i<8;i++)wall(-850+i*14,-3170,12,30,0);
tower(-855,-3230,2);tower(-740,-3230,2);tower(-855,-3170,2);tower(-740,-3170,2);
for(let i=0;i<6;i++)hut(-840+i*16,-3200,Math.random()*2,.8);
bonfire(-800,-3200);cave(-820,-3250,.2);

// ========== MOS LE HARMLESS (500,2500) ==========
for(let i=0;i<25;i++)palm(400+Math.random()*200,2400+Math.random()*200);
for(let i=0;i<8;i++)hut(460+i*14,2490+Math.random()*20,Math.random()*2,.9);
bonfire(500,2500);bridge(480,2380,0,35);

// ========== DESERT PLATEAU (2000,600) ==========
for(let i=0;i<20;i++)palm(1900+Math.random()*200,550+Math.random()*100);
for(let i=0;i<8;i++)wall(1950+i*14,560,12,16,0);
tower(1945,560,1.3);tower(2060,560,1.3);
for(let i=0;i<6;i++)hut(1960+i*16,600+Math.random()*30,Math.random()*2,1);
bonfire(2000,600);

// ========== SOPHANEM (2500,200) ==========
for(let i=0;i<8;i++){wall(2440+i*16,150,14,22,0);wall(2440+i*16,250,14,22,0)}
tower(2435,150,1.5);tower(2565,150,1.5);tower(2435,250,1.5);tower(2565,250,1.5);
for(let i=0;i<6;i++)hut(2460+i*16,190+Math.random()*30,Math.random()*2,.9);
bonfire(2500,200);for(let i=0;i<15;i++)palm(2420+Math.random()*180,130+Math.random()*140);

// ========== MENAPHOS (3000,400) ==========
for(let i=0;i<10;i++){wall(2940+i*14,350,12,24,0);wall(2940+i*14,450,12,24,0)}
for(let i=0;i<8;i++){wall(2935,350+i*14,3,24,0);wall(3075,350+i*14,3,24,0)}
tower(2935,350,1.8);tower(3075,350,1.8);tower(2935,450,1.8);tower(3075,450,1.8);
arch(3000,350,0,1.4);arch(3000,450,0,1.4);
for(let i=0;i<10;i++)hut(2960+i*12,390+Math.random()*30,Math.random()*2,.8);
bonfire(3000,400);for(let i=0;i<10;i++)palm(2920+Math.random()*170,330+Math.random()*140);

// ========== TIRANNWN (-3500,0) ==========
for(let i=0;i<50;i++)pine(-3700+Math.random()*400,-150+Math.random()*300);
for(let i=0;i<8;i++)hut(-3540+i*14,-10+Math.random()*25,Math.random()*2,.9);
bonfire(-3500,0);tower(-3520,30,1.2);tower(-3480,-30,1);
for(let i=0;i<6;i++)torch(-3540+i*16,0);

// ========== PRIFDDINAS (-4000,-300) ==========
for(let i=0;i<12;i++){const a=i/12*Math.PI*2;wallW(-4000+Math.cos(a)*120,-300+Math.sin(a)*120,14,30,a)}
for(let i=0;i<8;i++){const a=i/8*Math.PI*2;tower(-4000+Math.cos(a)*100,-300+Math.sin(a)*100,1.8,mt.stW)}
for(let i=0;i<6;i++){const a=i/6*Math.PI*2;hut(-4000+Math.cos(a)*60,-300+Math.sin(a)*60,a,1)}
bonfire(-4000,-300);
for(let i=0;i<30;i++)pine(-4150+Math.random()*300,-450+Math.random()*300);

// ========== FOSSIL ISLAND (2500,-1500) ==========
for(let i=0;i<15;i++)pine(2400+Math.random()*200,-1600+Math.random()*200);
for(let i=0;i<10;i++)deadTree(2450+Math.random()*150,-1550+Math.random()*150);
for(let i=0;i<5;i++)ruin(2450+Math.random()*100,-1520+Math.random()*80);
cave(2480,-1550,.3);bonfire(2500,-1500);

// ========== ZEAH HOSIDIUS (-2000,1200) ==========
for(let i=0;i<10;i++)hut(-2060+i*16,1180+Math.random()*30,Math.random()*2,1);
for(let i=0;i<20;i++)pine(-2100+Math.random()*200,1140+Math.random()*120);
bonfire(-2000,1200);

// ========== ZEAH SHAYZIEN (-2500,800) ==========
for(let i=0;i<8;i++){wall(-2560+i*16,760,14,22,0);wall(-2560+i*16,840,14,22,0)}
tower(-2565,760,1.5);tower(-2435,760,1.5);
for(let i=0;i<6;i++)hut(-2540+i*16,790+Math.random()*20,Math.random()*2,.9);
bonfire(-2500,800);

// ========== ZEAH LOVAKENGJ (-2800,1600) ==========
for(let i=0;i<6;i++)wall(-2840+i*16,1570,14,24,0);
for(let i=0;i<4;i++)tower(-2840+i*22,1560,1.3);
cave(-2820,1620,.5);cave(-2780,1580,-.3);bonfire(-2800,1600);
for(let i=0;i<8;i++)deadTree(-2850+Math.random()*100,1550+Math.random()*80);

// ========== ZEAH ARCEUUS (-2200,1800) ==========
for(let i=0;i<8;i++)ruin(-2250+Math.random()*100,1760+Math.random()*80);
for(let i=0;i<6;i++)tower(-2240+i*16,1810,1,mt.stD);
for(let i=0;i<4;i++)hut(-2230+i*16,1780,Math.random()*2,.8);
bonfire(-2200,1800);for(let i=0;i<10;i++)deadTree(-2280+Math.random()*160,1740+Math.random()*120);

// ========== ZANARIS (800,800) ==========
for(let i=0;i<12;i++){const a=i/12*Math.PI*2;hut(800+Math.cos(a)*70,800+Math.sin(a)*70,a,.7)}
bonfire(800,800);for(let i=0;i<20;i++)pine(740+Math.random()*120,740+Math.random()*120);

// ========== TZHAAR CITY (1800,1200) ==========
for(let i=0;i<10;i++){const lx=1750+Math.random()*100,lz=1150+Math.random()*100;const lv=new THREE.Mesh(new THREE.CircleGeometry(4+Math.random()*6,12),mt.lava);lv.rotation.x=-Math.PI/2;lv.position.set(lx,terrainH(lx,lz)+.5,lz);scene.add(lv);torchPositions.push({x:lx,y:terrainH(lx,lz)+3,z:lz,mesh:lv,ph:Math.random()*6.28,big:true,col:0xff3300})}
for(let i=0;i<6;i++)wall(1760+i*16,1160,14,20,0);
tower(1755,1160,1.8);tower(1855,1160,1.8);tower(1800,1240,1.5);
cave(1810,1180,.2);bonfire(1800,1200);

// === BRIDGES over rivers ===
bridge(220,0,Math.PI/2,32);bridge(220,100,Math.PI/2,32);bridge(220,-100,Math.PI/2,32);
bridge(-350,-100,Math.PI/2,26);bridge(-350,-300,Math.PI/2,26);
bridge(-1200,200,0,30);bridge(1300,-100,Math.PI/2,30);bridge(-200,1650,0,40);

// === SCATTER TREES BY BIOME (massive world) ===
for(let i=0;i<800;i++){const x=(Math.random()-.5)*14000,z=(Math.random()-.5)*12000;const rg=getReg(x,z);
if(rg.n.includes('Desert')||rg.n==='Al Kharid'||rg.n==='Sophanem'||rg.n==='Menaphos')palm(x,z);
else if(rg.n==='Wilderness'||rg.n.includes('Wild')||rg.n==='Draynor'||rg.n==='Morytania'||rg.n==='Canifis')deadTree(x,z);
else if(rg.n==='Karamja'||rg.n==='Brimhaven'||rg.n.includes('Harmless'))palm(x,z);
else pine(x,z)}

// === SCATTER BOULDERS (massive) ===
for(let i=0;i<300;i++){const bx=(Math.random()-.5)*14000,bz=(Math.random()-.5)*12000,s=2+Math.random()*5;const geo=new THREE.IcosahedronGeometry(s,1);const pos=geo.attributes.position;for(let j=0;j<pos.count;j++){pos.setX(j,pos.getX(j)+Math.random()*.8);pos.setY(j,pos.getY(j)+Math.random()*.8);pos.setZ(j,pos.getZ(j)+Math.random()*.8)}geo.computeVertexNormals();const bld=new THREE.Mesh(geo,Math.random()>.5?mt.rk:mt.rkD);bld.position.set(bx,terrainH(bx,bz)+s*.4,bz);bld.castShadow=true;scene.add(bld)}

// === GRASS TUFTS (billboard quads in green biomes) ===
const grassMat=new MS({color:0x3a5a20,roughness:1,side:THREE.DoubleSide,transparent:true,opacity:.85});
const grassMat2=new MS({color:0x4a6a28,roughness:1,side:THREE.DoubleSide,transparent:true,opacity:.8});
for(let i=0;i<600;i++){const gx=(Math.random()-.5)*10000,gz=(Math.random()-.5)*10000;const rg=getReg(gx,gz);
if(rg.n==='Wilderness'||rg.n==='Al Kharid')continue;
const gh=terrainH(gx,gz);const gp=new THREE.PlaneGeometry(.8+Math.random()*.6,2+Math.random()*2);
const gm=new THREE.Mesh(gp,Math.random()>.5?grassMat:grassMat2);gm.position.set(gx,gh+1+Math.random(),gz);gm.rotation.y=Math.random()*Math.PI;scene.add(gm);
const gm2=gm.clone();gm2.rotation.y+=Math.PI/2;scene.add(gm2)}

// === WATERFALLS ===
function waterfall(x,z,h,w){const wfGeo=new THREE.PlaneGeometry(w,h,4,12);const wfMat=new MS({color:0x4a8aaa,roughness:.2,metalness:.3,transparent:true,opacity:.6,side:THREE.DoubleSide,emissive:0x1a3a4a,emissiveIntensity:.2});
const wf=new THREE.Mesh(wfGeo,wfMat);wf.position.set(x,terrainH(x,z)+h/2,z);scene.add(wf);
const pool=new THREE.Mesh(new THREE.CircleGeometry(w*1.2,12),mt.wt);pool.rotation.x=-Math.PI/2;pool.position.set(x,terrainH(x,z)+.3,z+2);scene.add(pool)}
waterfall(-480,-420,25,10);waterfall(-350,-150,18,8);waterfall(200,200,15,6);
waterfall(-1250,50,20,8);waterfall(1350,-250,15,6);waterfall(-3600,-50,30,12);waterfall(-800,-3250,22,10);waterfall(2480,-1520,18,8);

// === CAVE ENTRANCES ===
function cave(x,z,rot){const h=terrainH(x,z);const cg=new THREE.Group();
const arch=new THREE.Mesh(new THREE.TorusGeometry(8,3,6,8,Math.PI),new MS({color:0x3a3530,roughness:.95}));arch.position.y=8;arch.rotation.z=Math.PI;cg.add(arch);
const dark=new THREE.Mesh(new THREE.CircleGeometry(7,8),new MS({color:0x050505,roughness:1}));dark.position.set(0,5,-1);cg.add(dark);
for(let i=0;i<6;i++){const r=new THREE.Mesh(new THREE.IcosahedronGeometry(2+Math.random()*2,0),mt.rk);r.position.set(-8+Math.random()*16,Math.random()*3,(Math.random()-.5)*4);r.castShadow=true;cg.add(r)}
cg.position.set(x,h,z);cg.rotation.y=rot||0;scene.add(cg)}
cave(50,-600,.5);cave(-250,-180,-.3);cave(-520,-430,.8);

// === SKELETON BONE PILES ===
function bonePile(x,z){const h=terrainH(x,z);const boneMat=new MS({color:0xccccaa,roughness:.85});
for(let i=0;i<8;i++){const b=new THREE.Mesh(new THREE.CylinderGeometry(.08,.08,.8+Math.random(),4),boneMat);b.position.set(x+(Math.random()-.5)*3,h+.3,z+(Math.random()-.5)*3);b.rotation.set(Math.random()*Math.PI,Math.random()*Math.PI,Math.random()*Math.PI);scene.add(b)}
const skull=new THREE.Mesh(new THREE.SphereGeometry(.5,6,6),boneMat);skull.position.set(x,h+.6,z);scene.add(skull)}
for(let i=0;i<40;i++){const bx=(Math.random()-.5)*8000,bz=(Math.random()-.5)*8000;bonePile(bx,bz)}
bonePile(30,-580);bonePile(-20,-620);bonePile(60,-550);

playerGroup=buildKnight();scene.add(playerGroup);

// === FIRELINK SHRINE (Spawn Hub at 0,5) ===
const fH=terrainH(0,5);
// Circular stone base
const shrBase=new THREE.Mesh(new THREE.CylinderGeometry(18,20,3,16),mt.st);shrBase.position.set(0,fH+1.5,5);shrBase.receiveShadow=true;scene.add(shrBase);
const shrFloor=new THREE.Mesh(new THREE.CylinderGeometry(17,17,1,16),mt.stD);shrFloor.position.set(0,fH+3.2,5);scene.add(shrFloor);
// Back wall + pillars
for(let i=0;i<5;i++){const px=-12+i*6;const pil=new THREE.Mesh(new THREE.CylinderGeometry(.8,1,16,6),mt.st);pil.position.set(px,fH+11,5-14);pil.castShadow=true;scene.add(pil);addSolid(pil)}
const bWall=new THREE.Mesh(new THREE.BoxGeometry(30,14,2),mt.stD);bWall.position.set(0,fH+10,5-15);bWall.castShadow=true;scene.add(bWall);
// Arched entrance
const sArch=new THREE.Mesh(new THREE.BoxGeometry(14,3,3),mt.st);sArch.position.set(0,fH+17,-10);sArch.castShadow=true;scene.add(sArch);
// Side walls
const lW=new THREE.Mesh(new THREE.BoxGeometry(2,12,24),mt.stD);lW.position.set(-16,fH+9,5-2);lW.castShadow=true;scene.add(lW);
const rW=lW.clone();rW.position.x=16;scene.add(rW);
// Steps leading down
for(let i=0;i<4;i++){const step=new THREE.Mesh(new THREE.BoxGeometry(10+i*2,1,3),mt.st);step.position.set(0,fH+2.5-i*.8,12+i*3);step.receiveShadow=true;scene.add(step)}
// Thrones (stone seats)
[-8,8].forEach(sx=>{const seat=new THREE.Mesh(new THREE.BoxGeometry(3,4,2),mt.stD);seat.position.set(sx,fH+5,5-10);seat.castShadow=true;scene.add(seat);const back=new THREE.Mesh(new THREE.BoxGeometry(3,6,.5),mt.st);back.position.set(sx,fH+7,5-11);scene.add(back)});
// Blacksmith anvil
const anvil=new THREE.Mesh(new THREE.BoxGeometry(2,2,1.5),mt.armorDk);anvil.position.set(12,fH+4.2,5);anvil.castShadow=true;scene.add(anvil);
// Register Firelink Shrine solids
addSolid(shrBase);addSolid(shrFloor);addSolid(bWall);addSolid(lW);addSolid(rW);addSolid(sArch);addSolid(anvil);

// === SPAWN ENEMIES PER REGION ===
regions.forEach(rg=>{rg.en.forEach(et=>{const cnt=Math.max(4,Math.round(rg.r/40));for(let i=0;i<cnt;i++){const ex=rg.x+(Math.random()-.5)*rg.r*1.4,ez=rg.z+(Math.random()-.5)*rg.r*1.4;spawnE(et,ex,ez,rg.lv)}})});

// === DYNAMIC LIGHT POOL (only 8 active PointLights) ===
for(let i=0;i<MAX_LIGHTS;i++){const l=new THREE.PointLight(0xff8833,0,60,1.5);scene.add(l);lightPool.push(l)}

const dGeo=new THREE.BufferGeometry();const dN=6000,dP=new Float32Array(dN*3);
for(let i=0;i<dN;i++){dP[i*3]=(Math.random()-.5)*2000;dP[i*3+1]=Math.random()*60+5;dP[i*3+2]=(Math.random()-.5)*2000}
dGeo.setAttribute('position',new THREE.BufferAttribute(dP,3));
dustPts=new THREE.Points(dGeo,new THREE.PointsMaterial({color:0xddcc99,size:.5,transparent:true,opacity:.3,depthWrite:false,blending:THREE.AdditiveBlending}));scene.add(dustPts);

composer=new EffectComposer(renderer);composer.addPass(new RenderPass(scene,cam));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(innerWidth,innerHeight),.4,.5,.88));
window.addEventListener('resize',()=>{cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);composer.setSize(innerWidth,innerHeight)});
initTargetRing();scene.add(targetRing);
buildColliders();
log('World loaded: '+torchPositions.length+' lights, '+enemies.length+' enemies, '+solidBoxes.length+' colliders','#0f0');
}

// === GEAR SYSTEM ===
const gear={atk:10,def:5,str:8,name:'Starter'};
const gearSlots=['Helm','Chest','Legs','Weapon','Shield','Boots','Gloves','Ring'];
const equipped={};gearSlots.forEach(s=>equipped[s]={name:'None',atk:1,def:1,str:1});
equipped.Weapon={name:'Starter Sword',atk:10,def:0,str:5};equipped.Shield={name:'Starter Shield',atk:0,def:5,str:0};
function totalGear(){let a=0,d=0,s=0;gearSlots.forEach(sl=>{a+=equipped[sl].atk;d+=equipped[sl].def;s+=equipped[sl].str});return{atk:a,def:d,str:s}}

function buildEnemy(type,lv){
const g=new THREE.Group();const col=eCol[type]||0x888888;const mat=new MS({color:col,roughness:.7});const matD=new MS({color:col,roughness:.6,metalness:.15});
const sc=.4+lv*.006;
// Body
const body=new THREE.Mesh(new THREE.CylinderGeometry(1.2,1.5,5,8),mat);body.position.y=4.5;body.castShadow=true;g.add(body);
// Head
const headG=type==='skeleton'?new THREE.BoxGeometry(1.8,1.8,1.8):new THREE.SphereGeometry(1.2,8,8);
const head=new THREE.Mesh(headG,matD);head.position.y=8;head.castShadow=true;g.add(head);
// Eyes
const eyeM=new MS({color:type==='demon'?0xff2200:type==='revenant'?0x00ff88:0xff4444,emissive:type==='demon'?0xff0000:0xff4444,emissiveIntensity:1.5});
[-0.4,0.4].forEach(ex=>{const eye=new THREE.Mesh(new THREE.SphereGeometry(.2,5,5),eyeM);eye.position.set(ex,8.2,1);g.add(eye)});
// Arms
[-1,1].forEach(s=>{const arm=new THREE.Mesh(new THREE.CylinderGeometry(.35,.3,4,5),mat);arm.position.set(s*1.8,5,0);arm.castShadow=true;g.add(arm)});
// Legs
[-1,1].forEach(s=>{const leg=new THREE.Mesh(new THREE.CylinderGeometry(.4,.35,3.5,5),mat);leg.position.set(s*.6,1.5,0);leg.castShadow=true;g.add(leg)});
// Weapon (varies by type)
if(type==='demon'||type==='revenant'||type==='whiteknight'||type==='guard'){
const wpn=new THREE.Mesh(new THREE.BoxGeometry(.15,.15,5),new MS({color:0xaaaacc,roughness:.2,metalness:.9}));wpn.position.set(1.8,3,2);wpn.rotation.x=.2;g.add(wpn)}
if(type==='barbarian'||type==='pirate'||type==='warrior'){
const axe=new THREE.Mesh(new THREE.BoxGeometry(.8,1.5,.15),new MS({color:0x888,roughness:.3,metalness:.8}));axe.position.set(1.8,5.5,1);g.add(axe)}
// HP bar above head
const barBg=new THREE.Mesh(new THREE.PlaneGeometry(3,.35),new MS({color:0x220000,side:THREE.DoubleSide}));barBg.position.y=10;g.add(barBg);
const barFg=new THREE.Mesh(new THREE.PlaneGeometry(3,.3),new MS({color:0x00cc00,side:THREE.DoubleSide}));barFg.position.y=10;barFg.position.z=.01;g.add(barFg);
g.userData.hpBar=barFg;
g.scale.setScalar(sc);
return g;
}

function spawnE(type,x,z,lv){const hp=eHP[type]||40;const mesh=buildEnemy(type,lv||1);
const e={mesh,hp,maxHp:hp,poi:30,x,z,type,lv:lv||1,atkCD:0,aggro:50+(lv||1)*2,dmg:Math.max(5,8+(lv||1)*2)};
const h=terrainH(x,z);e.mesh.position.set(x,h,z);scene.add(e.mesh);enemies.push(e)}

function calcHit(a,d){const g=totalGear();const ab=a===player?40+g.atk:22+((a.lv||1)*1.5);const db=d===player?30+g.def:15;return Math.random()<Math.max(.08,Math.min(.94,(ab/(db+12))*.82))}

function spawnLoot(x,z,e){
// Always drop gear that is 1% better than current best in a random slot
const slot=gearSlots[Math.floor(Math.random()*gearSlots.length)];
const cur=equipped[slot];const boost=1.01;
const newItem={name:e.type+' '+slot+' Lv'+(e.lv||1),atk:Math.ceil(Math.max(cur.atk*boost,cur.atk+1)),def:Math.ceil(Math.max(cur.def*boost,cur.def+1)),str:Math.ceil(Math.max(cur.str*boost,cur.str+1)),slot};
const c=0xffdd44;const m=new THREE.Mesh(new THREE.BoxGeometry(2.5,2.5,2.5),new MS({color:c,emissive:c,emissiveIntensity:.6,roughness:.3,metalness:.3}));
m.position.set(x,terrainH(x,z)+4,z);m.userData={vx:(Math.random()-.5)*5,vz:(Math.random()-.5)*5,vy:8,life:900,item:newItem.name,gear:newItem};scene.add(m);lootArr.push(m);
// Also drop bones/coins
const c2=0xccccaa;const m2=new THREE.Mesh(new THREE.BoxGeometry(1.5,1.5,1.5),new MS({color:c2,emissive:c2,emissiveIntensity:.2,roughness:.6}));
m2.position.set(x+2,terrainH(x,z)+4,z+2);m2.userData={vx:(Math.random()-.5)*4,vz:(Math.random()-.5)*4,vy:7,life:600,item:'Bones'};scene.add(m2);lootArr.push(m2);
}
function hitFX(x,y,z,col=0xff4400){for(let i=0;i<25;i++){const p=new THREE.Mesh(new THREE.SphereGeometry(.3,4,4),new MS({color:col,emissive:col,emissiveIntensity:1.5,roughness:1}));p.position.set(x,y,z);p.userData={vx:(Math.random()-.5)*10,vy:(Math.random()-.5)*10+4,vz:(Math.random()-.5)*10,life:22};scene.add(p);particles.push(p)}}
function cycleLock(){if(!enemies.length)return;lockIdx=(lockIdx+1)%enemies.length;lockOn=enemies[lockIdx];log('Locked on: '+lockOn.type,'#cc4')}
function parry(){player.blocking=true;if(lockOn){const d=Math.hypot(lockOn.mesh.position.x-player.x,lockOn.mesh.position.z-player.z);if(d<18){hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+6,lockOn.mesh.position.z,0x00ffff);lockOn.hp-=12;player.sta=Math.min(player.sta+28,player.maxSta);skills.Defence.xp+=8;log('PARRY RIPOSTE!','#0ff')}}}

let gpIndex=-1;
window.addEventListener('gamepadconnected',e=>{gpIndex=e.gamepad.index;log('Controller connected: '+e.gamepad.id,'#0f0');console.log('Gamepad connected',e.gamepad)});
window.addEventListener('gamepaddisconnected',e=>{if(e.gamepad.index===gpIndex)gpIndex=-1;log('Controller disconnected','#f80')});
function pollGamepad(){
const gps=navigator.getGamepads?navigator.getGamepads():[];
let gp=null;
if(gpIndex>=0&&gps[gpIndex])gp=gps[gpIndex];
else{for(let i=0;i<gps.length;i++){if(gps[i]){gp=gps[i];gpIndex=i;break}}}
if(!gp)return;
const dz=.12;
gpAxes[0]=Math.abs(gp.axes[0])>dz?gp.axes[0]:0;
gpAxes[1]=Math.abs(gp.axes[1])>dz?gp.axes[1]:0;
gpAxes[2]=Math.abs(gp.axes[2])>dz?gp.axes[2]:0;
gpAxes[3]=Math.abs(gp.axes[3])>dz?gp.axes[3]:0;
gpButtons.a=gp.buttons[0]?.pressed;gpButtons.x=gp.buttons[2]?.pressed;
gpButtons.b=gp.buttons[1]?.pressed;gpButtons.y=gp.buttons[3]?.pressed;
gpButtons.lb=gp.buttons[4]?.pressed;gpButtons.rb=gp.buttons[5]?.pressed;
gpButtons.lt=gp.buttons[6]?.value>.3;gpButtons.rt=gp.buttons[7]?.value>.3;
gpButtons.start=gp.buttons[9]?.pressed;gpButtons.back=gp.buttons[8]?.pressed;
gpButtons.dUp=gp.buttons[12]?.pressed;gpButtons.dDown=gp.buttons[13]?.pressed;
gpButtons.dLeft=gp.buttons[14]?.pressed;gpButtons.dRight=gp.buttons[15]?.pressed;
}

function loop(){
requestAnimationFrame(loop);time+=.016;pollGamepad();
if(player.dead){player.deadTimer-=.016;if(player.deadTimer<=0){player.dead=false;player.hp=player.maxHp;player.sta=player.maxSta;player.x=0;player.z=5;player.y=terrainH(0,5);document.getElementById('death-overlay').classList.remove('active');log('Respawned at bonfire','#cc4')}composer.render();return}

const gSens=(gameOpts?gameOpts.sens:5)/5;camYaw+=gpAxes[2]*.35*gSens*(gameOpts?gameOpts.flipx:1);camPitch=Math.max(.05,Math.min(1.2,camPitch-gpAxes[3]*.25*gSens*(gameOpts?gameOpts.flipy:1)));
// Auto-camera: lerp camYaw behind player when not panning
if(!mouse.mid&&!lockOn){let targetYaw=player.ang+Math.PI;while(targetYaw>Math.PI)targetYaw-=Math.PI*2;while(targetYaw<-Math.PI)targetYaw+=Math.PI*2;let yd=targetYaw-camYaw;while(yd>Math.PI)yd-=Math.PI*2;while(yd<-Math.PI)yd+=Math.PI*2;camYaw+=yd*.03}

const fwd=new THREE.Vector3(-Math.sin(camYaw),0,-Math.cos(camYaw));
const right=new THREE.Vector3(fwd.z,0,-fwd.x);
let moveDir=new THREE.Vector3();
if(keys['w']||gpButtons.dUp)moveDir.add(fwd);if(keys['s']||gpButtons.dDown)moveDir.sub(fwd);
if(keys['a']||gpButtons.dLeft)moveDir.add(right);if(keys['d']||gpButtons.dRight)moveDir.sub(right);
if(gpAxes[0]||gpAxes[1]){moveDir.sub(right.clone().multiplyScalar(gpAxes[0]));moveDir.sub(fwd.clone().multiplyScalar(gpAxes[1]))}

let spd=player.speed;
if(player.rolling){player.rollT--;if(player.rollT<=0)player.rolling=false;spd*=3.6}

if(moveDir.lengthSq()>.001){moveDir.normalize();
const steps=spd>1?4:2;const stepSpd=spd/steps;
for(let st=0;st<steps;st++){player.x+=moveDir.x*stepSpd;player.z+=moveDir.z*stepSpd;
const co=pushOut(player.x,player.y,player.z);player.x=co.x;player.z=co.z}
const targetAng=Math.atan2(moveDir.x,moveDir.z);
let diff=targetAng-player.ang;while(diff>Math.PI)diff-=Math.PI*2;while(diff<-Math.PI)diff+=Math.PI*2;
player.ang+=diff*.15}
else{const co=pushOut(player.x,player.y,player.z);player.x=co.x;player.z=co.z}

player.y=terrainH(player.x,player.z);
const curReg=getReg(player.x,player.z);
const totalLv=skillDefs.reduce((a,s)=>a+skills[s].lvl,0);
const gs=totalGear();document.getElementById('locbar').textContent='Lv '+totalLv+' \u00B7 '+curReg.n+' (Lv '+curReg.lv+'+) \u00B7 ATK:'+gs.atk+' DEF:'+gs.def+' STR:'+gs.str;
scene.fog.color.set(curReg.fog);scene.background.set(curReg.fog);

if(keys['q']||gpButtons.lb)player.sta=Math.min(player.sta+5,player.maxSta);
else player.sta=Math.min(player.sta+1,player.maxSta);

if((keys[' ']||gpButtons.a)&&!player.rolling&&player.sta>24){player.rolling=true;player.rollT=22;player.sta-=24;skills.Agility.xp+=2}
if(mouse.right||gpButtons.lt||gpButtons.b){parry()}else{player.blocking=false}
// Gamepad: RB=lock-on, Start=inventory, Back=skills
if(gpButtons.rb&&!player._rbCD){cycleLock();player._rbCD=20}
if(player._rbCD)player._rbCD--;
if(gpButtons.start&&!player._stCD){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="inventory"]').classList.add('active');document.getElementById('tp-inventory').classList.add('active');player._stCD=20}
if(player._stCD)player._stCD--;
if(gpButtons.back&&!player._bkCD){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="skills"]').classList.add('active');document.getElementById('tp-skills').classList.add('active');player._bkCD=20}
if(player._bkCD)player._bkCD--;

playerGroup.position.set(player.x,player.y+1,player.z);playerGroup.rotation.y=player.ang;
// Rolling: full forward tumble
if(player.rolling){const rPct=1-player.rollT/22;playerGroup.rotation.x=rPct*Math.PI*2;playerGroup.position.y+=Math.sin(rPct*Math.PI)*3}
else{playerGroup.rotation.x=0}
// Attack swing animation on right arm
if(playerGroup.userData.rArm){const rA=playerGroup.userData.rArm;
if(player.atkCD>7){rA.rotation.x=-1.2+Math.sin((14-player.atkCD)/7*Math.PI)*1.8;rA.rotation.z=-.3}
else if(player.atkCD>0){rA.rotation.x*=.8;rA.rotation.z*=.8}
else{rA.rotation.x=0;rA.rotation.z=0}}
// Shield raise on parry
if(playerGroup.userData.lArm){const lA=playerGroup.userData.lArm;
if(player.blocking){lA.rotation.x+=(-.9-lA.rotation.x)*.3;lA.rotation.z+=(.5-lA.rotation.z)*.3;lA.position.x+=(-.8-lA.position.x)*.2;lA.position.z+=(1.5-lA.position.z)*.2}
else{lA.rotation.x*=.82;lA.rotation.z*=.82;lA.position.x+=(-2.4-lA.position.x)*.15;lA.position.z+=(0-lA.position.z)*.15}}

const camX=player.x+Math.sin(camYaw)*Math.cos(camPitch)*camDist;
const camZ=player.z+Math.cos(camYaw)*Math.cos(camPitch)*camDist;
const camY=player.y+Math.sin(camPitch)*camDist;
cam.position.x+=(camX-cam.position.x)*.1;cam.position.z+=(camZ-cam.position.z)*.1;cam.position.y+=(camY-cam.position.y)*.1;
if(lockOn&&lockOn.mesh){const mx=(player.x+lockOn.mesh.position.x)*.5,mz=(player.z+lockOn.mesh.position.z)*.5;cam.lookAt(mx,player.y+8,mz)}
else cam.lookAt(player.x,player.y+8,player.z);

for(let i=enemies.length-1;i>=0;i--){let e=enemies[i];
let dx=player.x-e.mesh.position.x,dz=player.z-e.mesh.position.z,dist=Math.hypot(dx,dz);
if(dist<e.aggro){const a=Math.atan2(dz,dx);e.mesh.position.x+=Math.cos(a)*.2;e.mesh.position.z+=Math.sin(a)*.2;
const eh=terrainH(e.mesh.position.x,e.mesh.position.z);e.mesh.position.y=eh+Math.sin(time*2+i)*.3;
e.mesh.rotation.y=Math.atan2(dx,dz);
if(dist<12&&e.atkCD<=0){if(calcHit(e,player)){const gd=totalGear();let blockMult=player.blocking?.65:.3;const blocked=Math.floor(gd.def*blockMult);const realDmg=Math.max(1,e.dmg-blocked);player.hp-=realDmg;if(player.blocking){player.sta-=8;skills.Defence.xp+=4;hitFX(player.x,player.y+8,player.z,0x4488ff);log(`BLOCKED ${e.type}! -${realDmg} (absorbed ${blocked})`,'#48f')}else{hitFX(player.x,player.y+8,player.z);log(`${e.type} hit for ${realDmg} (blocked ${blocked})`,'#f44')}}e.atkCD=42}}
e.atkCD=Math.max(0,e.atkCD-1);
// Update enemy HP bar
if(e.mesh.userData.hpBar){const pct=Math.max(0,e.hp/e.maxHp);e.mesh.userData.hpBar.scale.x=pct;e.mesh.userData.hpBar.material.color.set(pct>.5?0x00cc00:pct>.25?0xccaa00:0xcc0000);
e.mesh.userData.hpBar.lookAt(cam.position)}
if(e.hp<=0){spawnLoot(e.mesh.position.x,e.mesh.position.z,e);scene.remove(e.mesh);enemies.splice(i,1);if(lockOn===e)lockOn=null;
const xpMult=Math.max(1,(e.lv||1)*.8);skills.Attack.xp+=Math.round(15*xpMult);skills.Strength.xp+=Math.round(12*xpMult);skills.Hitpoints.xp+=Math.round(10*xpMult);
log(e.type+' (Lv'+(e.lv||1)+') slain! +'+Math.round(37*xpMult)+'xp','#fa4');
const rt=e.type,rx=e.x,rz=e.z,rlv=getReg(rx,rz).lv;setTimeout(()=>{if(scene)spawnE(rt,rx+(Math.random()-.5)*30,rz+(Math.random()-.5)*30,rlv)},15000)}}

if((mouse.down||gpButtons.rt||gpButtons.x||keys['1'])&&player.atkCD<=0&&player.sta>19){player.atkCD=14;player.sta-=19;
const gStats=totalGear();const pDmg=Math.max(12,10+gStats.atk+gStats.str);
if(lockOn&&lockOn.hp>0&&Math.hypot(lockOn.mesh.position.x-player.x,lockOn.mesh.position.z-player.z)<22){
lockOn.hp-=pDmg;lockOn.poi-=16;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+6,lockOn.mesh.position.z);
log('Hit '+lockOn.type+' for '+pDmg,'#ff8');
if(lockOn.poi<=0){lockOn.hp-=Math.round(pDmg*.5);lockOn.poi=30;log('POISE BREAK!','#ff4')}}
else{for(let i=enemies.length-1;i>=0;i--){let e=enemies[i],edx=e.mesh.position.x-player.x,edz=e.mesh.position.z-player.z;
if(Math.hypot(edx,edz)<16){const eAng=Math.atan2(edx,edz);let ad=eAng-player.ang;while(ad>Math.PI)ad-=Math.PI*2;while(ad<-Math.PI)ad+=Math.PI*2;
if(Math.abs(ad)<1.2&&calcHit(player,e)){e.hp-=pDmg;hitFX(e.mesh.position.x,e.mesh.position.y+6,e.mesh.position.z);log('Hit '+e.type+' for '+pDmg,'#ff8')}}}}}
player.atkCD=Math.max(0,player.atkCD-1);if(player._parryCD)player._parryCD--;if(player._estusCD)player._estusCD--;

for(let i=lootArr.length-1;i>=0;i--){let l=lootArr[i];l.userData.vy-=.45;l.position.x+=l.userData.vx*.6;l.position.z+=l.userData.vz*.6;l.position.y+=l.userData.vy*.6;l.userData.vx*=.92;l.userData.vz*=.92;l.userData.life--;l.rotation.y+=.05;
const lh=terrainH(l.position.x,l.position.z)+1.5;if(l.position.y<lh){l.position.y=lh;l.userData.vy*=-.4}
if(l.userData.life<=0){scene.remove(l);lootArr.splice(i,1);continue}
if(Math.hypot(l.position.x-player.x,l.position.z-player.z)<9){
if(l.userData.gear){const g=l.userData.gear;equipped[g.slot]=g;updateEqUI();log('EQUIPPED: '+g.name+' [ATK+'+g.atk+' DEF+'+g.def+' STR+'+g.str+']','#0ff')}
if(inventory.length<28){inventory.push(l.userData.item);updateInvUI();log('Picked up: '+l.userData.item,'#ff4')}else log('Inventory full!','#f44');
scene.remove(l);lootArr.splice(i,1)}}

for(let i=particles.length-1;i>=0;i--){let p=particles[i];p.position.x+=p.userData.vx*.14;p.position.y+=p.userData.vy*.14;p.position.z+=p.userData.vz*.14;p.userData.vy-=.5;p.userData.life--;p.scale.setScalar(Math.max(0,p.userData.life/22));if(p.userData.life<=0){scene.remove(p);particles.splice(i,1)}}

// Animate torch meshes + assign 8 nearest PointLights
const sorted=torchPositions.map(t=>({...t,d:Math.hypot(t.x-player.x,t.z-player.z)})).sort((a,b)=>a.d-b.d);
for(let i=0;i<MAX_LIGHTS;i++){const l=lightPool[i];if(i<sorted.length&&sorted[i].d<200){const t=sorted[i];l.position.set(t.x,t.y,t.z);l.intensity=(t.big?3.5:1.8)+Math.sin(time*8+t.ph)*(t.big?1.2:.5);l.color.set(t.col||0xff8833);l.distance=t.big?50:40}else{l.intensity=0}}
torchPositions.forEach(t=>{if(t.mesh){t.mesh.position.y+=Math.sin(time*6+t.ph)*.015;t.mesh.scale.setScalar((t.big?1:.7)+Math.sin(time*10+t.ph)*(t.big?.25:.12))}});

if(dustPts){const dp=dustPts.geometry.attributes.position;for(let i=0;i<dp.count;i++){let y=dp.getY(i);y+=.012;if(y>55)y=5;dp.setY(i,y)}dp.needsUpdate=true;dustPts.position.set(player.x,0,player.z)}

if(riverMesh){const wp=riverMesh.geometry.attributes.position;for(let i=0;i<wp.count;i++){wp.setZ(i,Math.sin(wp.getX(i)*.3+time*2)*.5+Math.cos(wp.getY(i)*.2+time*1.4)*.3)}wp.needsUpdate=true;riverMesh.geometry.computeVertexNormals()}

if(keys['f']||gpButtons.lb){const nT=Math.hypot(player.x+100,player.z-50)<50;const nR=Math.hypot(player.x+70,player.z+80)<40;
if(nT){skills.Woodcutting.xp+=18;hitFX(player.x,player.y+8,player.z,0x44aa22);log('Woodcutting +18xp','#6a4')}
else if(nR){skills.Fishing.xp+=22;hitFX(player.x,player.y+8,player.z,0x2288ff);log('Fishing +22xp','#48f')}}

skillDefs.forEach(s=>{const sk=skills[s];const newLvl=Math.min(99,Math.max(1,Math.floor(1+Math.sqrt(sk.xp/50))));if(newLvl>sk.lvl){sk.lvl=newLvl;log(`${s} leveled up to ${newLvl}!`,'#ff0')}});
if(time*60%30<1){updateSkillUI();updateEqUI();
document.getElementById('orb-hp').textContent=Math.max(0,~~player.hp);
document.getElementById('orb-pray').textContent=skills.Prayer.lvl;
document.getElementById('orb-run').textContent=~~(player.sta/player.maxSta*100);
drawMinimap()}

const hp=Math.max(0,player.hp/player.maxHp*100),st=player.sta/player.maxSta*100,po=player.poi/player.maxPoi*100;
document.getElementById('hpB').style.width=hp+'%';document.getElementById('stB').style.width=st+'%';document.getElementById('poB').style.width=po+'%';
document.getElementById('hpT').textContent=Math.max(0,~~player.hp)+'/'+player.maxHp;
document.getElementById('stT').textContent=~~player.sta+'/'+player.maxSta;document.getElementById('poT').textContent=~~player.poi+'/'+player.maxPoi;

if(player.hp<=0&&!player.dead){player.dead=true;player.deadTimer=3;document.getElementById('death-overlay').classList.add('active');log('YOU DIED','#f00')}

updateTargetFrame();
if(ws&&ws.readyState===1&&++sendCt%3===0){ws.send(JSON.stringify({t:'p',id:myId,x:player.x,y:player.y,z:player.z,a:player.ang}))}

composer.render()}

window.addEventListener('keydown',e=>{
const k=e.key.toLowerCase();keys[k]=true;
if(k==='tab'){e.preventDefault();cycleLock()}
if(k==='i'){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="inventory"]').classList.add('active');document.getElementById('tp-inventory').classList.add('active')}
if(k==='k'){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="skills"]').classList.add('active');document.getElementById('tp-skills').classList.add('active')}
if(k==='f5'){e.preventDefault();if(gameStarted)saveGame()}
if(k==='2'&&!player._parryCD){parry();player._parryCD=15}
if(k==='3'&&!player._estusCD){const heal=Math.round(player.maxHp*.3);player.hp=Math.min(player.hp+heal,player.maxHp);log('Used Estus Flask: +'+heal+' HP','#0f0');player._estusCD=90}
if(k==='4'){const bi=inventory.indexOf('Bones');if(bi>=0){inventory.splice(bi,1);updateInvUI();skills.Prayer.xp+=15;log('Buried bones: Prayer +15xp','#cc4')}}
if(k==='q'){e.preventDefault();document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="prayer"]').classList.add('active');document.getElementById('tp-prayer').classList.add('active')}
if(k==='m'){const wm=document.getElementById('world-map');if(wm.classList.contains('active')){wm.classList.remove('active')}else{wm.classList.add('active');drawWorldMap()}}
if(k==='escape'){const wm=document.getElementById('world-map');if(wm.classList.contains('active'))wm.classList.remove('active');else{lockOn=null;lockIdx=-1;log('Target cleared','#887')}}
if(k==='f'&&gameStarted){e.preventDefault();const nT=Math.hypot(player.x+100,player.z-50)<50;const nR=Math.hypot(player.x+70,player.z+80)<40;const nM=Math.hypot(player.x-300,player.z+100)<60;
if(nT){skills.Woodcutting.xp+=18;log('Woodcutting +18xp','#6a4')}
else if(nR){skills.Fishing.xp+=22;log('Fishing +22xp','#48f')}
else if(nM){skills.Mining.xp+=20;log('Mining +20xp','#a86')}
else log('Nothing to gather here','#887')}
});
window.addEventListener('beforeunload',()=>{if(gameStarted&&!player.dead)saveGame()});
window.addEventListener('keyup',e=>keys[e.key.toLowerCase()]=false);
window.addEventListener('mousemove',e=>{
mouse.x=(e.clientX/innerWidth)*2-1;mouse.y=-(e.clientY/innerHeight)*2+1;
if(mouse.mid){const s=(gameOpts?gameOpts.sens:5)/5;const fx=gameOpts?gameOpts.flipx:1;const fy=gameOpts?gameOpts.flipy:1;camYaw+=e.movementX*.005*s*fx;camPitch=Math.max(.05,Math.min(1.2,camPitch-e.movementY*.005*s*fy))}
});
window.addEventListener('mousedown',e=>{if(e.button===0){mouse.down=true;clickTarget(e)}if(e.button===2)mouse.right=true;if(e.button===1){e.preventDefault();mouse.mid=true}});
window.addEventListener('mouseup',e=>{if(e.button===0)mouse.down=false;if(e.button===2)mouse.right=false;if(e.button===1)mouse.mid=false});
window.addEventListener('wheel',e=>{camDist=Math.max(8,Math.min(300,camDist+e.deltaY*.08))});
window.addEventListener('contextmenu',e=>e.preventDefault());

let ws,myId=-1,otherPlayers={},sendCt=0;
function connectMP(){
const host=window.location.hostname||'127.0.0.1';
ws=new WebSocket('ws://'+host+':8081');
ws.onopen=()=>log('Multiplayer connected!','#0f0');
ws.onmessage=(ev)=>{
const d=JSON.parse(ev.data);
if(d.t==='id'){myId=d.id;log('Your Player ID: '+d.id,'#0f0')}
else if(d.t==='p'){
if(!otherPlayers[d.id]){otherPlayers[d.id]=buildKnight();scene.add(otherPlayers[d.id]);log('Player '+d.id+' joined!','#0f0')}
otherPlayers[d.id].position.set(d.x,d.y+2.6,d.z);otherPlayers[d.id].rotation.y=d.a;
}
else if(d.t==='l'){
if(otherPlayers[d.id]){scene.remove(otherPlayers[d.id]);delete otherPlayers[d.id];log('Player '+d.id+' left','#f80')}
}
};
ws.onerror=()=>{};
ws.onclose=()=>{setTimeout(connectMP,3000)};
}
// === SAVE / LOAD SYSTEM (localStorage) ===
const SAVE_KEY='soulscape_save';
function saveGame(){
try{const data={player:{x:player.x,z:player.z,hp:player.hp,maxHp:player.maxHp,sta:player.sta,maxSta:player.maxSta,poi:player.poi,maxPoi:player.maxPoi,speed:player.speed},
skills:{},inventory:[...inventory],equipped:{},opts:{...gameOpts},ver:2};
skillDefs.forEach(s=>data.skills[s]={lvl:skills[s].lvl,xp:skills[s].xp});
gearSlots.forEach(s=>data.equipped[s]={...equipped[s]});
localStorage.setItem(SAVE_KEY,JSON.stringify(data));
log('Game saved!','#0f0');return true}catch(e){log('Save failed: '+e.message,'#f44');return false}}

function loadGame(){
try{const raw=localStorage.getItem(SAVE_KEY);if(!raw)return false;
const data=JSON.parse(raw);
player.x=data.player.x;player.z=data.player.z;player.hp=data.player.hp;player.maxHp=data.player.maxHp;
player.sta=data.player.sta;player.maxSta=data.player.maxSta;player.poi=data.player.poi;player.maxPoi=data.player.maxPoi;
player.speed=data.player.speed||.42;player.y=terrainH(player.x,player.z);
skillDefs.forEach(s=>{if(data.skills[s]){skills[s].lvl=data.skills[s].lvl;skills[s].xp=data.skills[s].xp}});
if(data.inventory){inventory.length=0;data.inventory.forEach(i=>inventory.push(i));updateInvUI()}
if(data.equipped){gearSlots.forEach(s=>{if(data.equipped[s])equipped[s]=data.equipped[s]})}
if(data.opts){Object.assign(gameOpts,data.opts)}
updateSkillUI();updateEqUI();
document.getElementById('hpT').textContent=Math.round(player.hp)+'/'+player.maxHp;
document.getElementById('stT').textContent=Math.round(player.sta)+'/'+player.maxSta;
document.getElementById('poT').textContent=Math.round(player.poi)+'/'+player.maxPoi;
log('Game loaded! Pos: '+Math.round(player.x)+','+Math.round(player.z),'#0f0');
return true}catch(e){log('Load failed: '+e.message,'#f44');return false}}

function hasSave(){return !!localStorage.getItem(SAVE_KEY)}

// Auto-save every 30 seconds
setInterval(()=>{if(gameStarted&&!player.dead)saveGame()},30000);

// === MENU & OPTIONS LOGIC ===
const gameOpts={blood:true,particles:true,flipy:1,flipx:1,sens:5,bloom:true,bright:1.15};
const classStats={warrior:{hp:160,sta:110,poi:60},knight:{hp:180,sta:90,poi:68},sorcerer:{hp:100,sta:80,poi:140},deprived:{hp:80,sta:80,poi:80}};
let gameStarted=false;

function startGame(isLoad){
document.getElementById('main-menu').classList.add('hidden');
document.getElementById('char-create').classList.remove('show');
document.getElementById('game-ui').style.display='block';
document.getElementById('osrs-panel').style.display='flex';
document.getElementById('chatbox').style.display='flex';
document.body.style.cursor='crosshair';
if(!gameStarted){gameStarted=true;
try{init();if(isLoad)loadGame();updateSkillUI();updateEqUI();loop();connectMP()}catch(err){const cl=document.getElementById('chat-log');if(cl)cl.textContent='ERROR: '+err.message;console.error(err)}}}

document.querySelectorAll('.mi').forEach(el=>el.addEventListener('click',()=>{
const a=el.dataset.a;
if(a==='new'){document.getElementById('main-menu').classList.add('hidden');document.getElementById('char-create').classList.add('show')}
else if(a==='cont'){if(hasSave()){startGame(true)}else{log('No save found!','#f44')}}
else if(a==='so')document.getElementById('screen-opts').classList.add('show');
else if(a==='go')document.getElementById('game-opts').classList.add('show');
else if(a==='q'){try{window.close()}catch(e){}}
}));
document.getElementById('scr-back').onclick=()=>document.getElementById('screen-opts').classList.remove('show');
document.getElementById('gm-back').onclick=()=>document.getElementById('game-opts').classList.remove('show');
document.getElementById('bright-s').oninput=e=>{gameOpts.bright=e.target.value/100;if(renderer)renderer.toneMappingExposure=gameOpts.bright};
document.getElementById('sens-s').oninput=e=>gameOpts.sens=+e.target.value;
document.querySelectorAll('.opt-val').forEach(el=>el.onclick=()=>{const o=el.dataset.o;
if(['blood','part','al','bl'].includes(o)){const on=el.textContent==='On';el.textContent=on?'Off':'On';gameOpts[o]=!on}
else if(o==='fy'){gameOpts.flipy*=-1;el.textContent=gameOpts.flipy>0?'Normal':'Inverted'}
else if(o==='fx'){gameOpts.flipx*=-1;el.textContent=gameOpts.flipx>0?'Normal':'Inverted'}
else if(o==='hud')el.textContent=el.textContent==='Always Display'?'Auto':'Always Display';
else if(o==='shad')el.textContent=el.textContent==='High'?'Low':'High'});
document.querySelectorAll('.class-card').forEach(el=>el.addEventListener('click',()=>{
const cls=el.dataset.c,s=classStats[cls];
player.hp=s.hp;player.maxHp=s.hp;player.sta=s.sta;player.maxSta=s.sta;player.poi=s.poi;player.maxPoi=s.poi;
document.getElementById('hpT').textContent=s.hp+'/'+s.hp;document.getElementById('stT').textContent=s.sta+'/'+s.sta;document.getElementById('poT').textContent=s.poi+'/'+s.poi;
setTimeout(()=>{startGame(false)},500)}));
</script>
</body>
</html>"""

# === RAW WEBSOCKET SERVER (no pip install needed) ===
WS_MAGIC = b'258EAFA5-E914-47DA-95CA-5AB5DC65FE97'
ws_clients = {}  # id -> socket
ws_lock = threading.Lock()
_next_id = [0]

def ws_handshake(conn):
    data = conn.recv(4096)
    key = None
    for line in data.decode(errors='ignore').split('\r\n'):
        if line.lower().startswith('sec-websocket-key:'):
            key = line.split(':', 1)[1].strip()
    if not key:
        return False
    accept = base64.b64encode(hashlib.sha1(key.encode() + WS_MAGIC).digest()).decode()
    conn.sendall((
        'HTTP/1.1 101 Switching Protocols\r\n'
        'Upgrade: websocket\r\n'
        'Connection: Upgrade\r\n'
        f'Sec-WebSocket-Accept: {accept}\r\n\r\n'
    ).encode())
    return True

def ws_decode(data):
    if len(data) < 2: return None, data
    b1, b2 = data[0], data[1]
    op = b1 & 0x0F
    masked = b2 & 0x80
    ln = b2 & 0x7F
    off = 2
    if ln == 126:
        if len(data) < 4: return None, data
        ln = struct.unpack('>H', data[2:4])[0]; off = 4
    elif ln == 127:
        if len(data) < 10: return None, data
        ln = struct.unpack('>Q', data[2:10])[0]; off = 10
    if masked:
        if len(data) < off + 4: return None, data
        mask = data[off:off+4]; off += 4
    if len(data) < off + ln: return None, data
    payload = data[off:off+ln]
    if masked: payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    remain = data[off+ln:]
    if op == 8: return ('close', b''), remain
    if op == 9: return ('ping', payload), remain
    return ('text', payload.decode()), remain

def ws_encode(text):
    d = text.encode()
    f = bytearray([0x81])
    if len(d) < 126: f.append(len(d))
    elif len(d) < 65536: f.append(126); f.extend(struct.pack('>H', len(d)))
    else: f.append(127); f.extend(struct.pack('>Q', len(d)))
    f.extend(d)
    return bytes(f)

def ws_broadcast(msg, exclude=None):
    frame = ws_encode(msg)
    with ws_lock:
        for cid, c in list(ws_clients.items()):
            if cid != exclude:
                try: c.sendall(frame)
                except: pass

def ws_client(conn, addr):
    if not ws_handshake(conn):
        conn.close(); return
    cid = _next_id[0]; _next_id[0] += 1
    with ws_lock: ws_clients[cid] = conn
    try:
        conn.sendall(ws_encode(json.dumps({'t': 'id', 'id': cid})))
        buf = b''
        while True:
            chunk = conn.recv(4096)
            if not chunk: break
            buf += chunk
            while buf:
                result, buf = ws_decode(buf)
                if result is None: break
                kind, payload = result
                if kind == 'close': raise ConnectionError
                if kind == 'ping':
                    conn.sendall(bytes([0x8A, len(payload)]) + payload)
                if kind == 'text':
                    try:
                        d = json.loads(payload)
                        d['id'] = cid  # enforce server-side ID
                        ws_broadcast(json.dumps(d), exclude=cid)
                    except: pass
    except: pass
    finally:
        with ws_lock: ws_clients.pop(cid, None)
        try: ws_broadcast(json.dumps({'t': 'l', 'id': cid}))
        except: pass
        conn.close()

def ws_server():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('0.0.0.0', 8081))
    srv.listen(20)
    while True:
        c, a = srv.accept()
        threading.Thread(target=ws_client, args=(c, a), daemon=True).start()

# === HTTP SERVER ===
class GameHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html', '/SS.html', '/game'):
            data = GAME_HTML.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404)
    def log_message(self, fmt, *args):
        pass

PORT = 8080
print('=' * 60)
print('  OSRS SOULS v4 — Standalone Multiplayer Game Server')
print('=' * 60)
print(f'\n  Game:        http://127.0.0.1:{PORT}/')
print(f'  WebSocket:   ws://0.0.0.0:8081  (LAN multiplayer)')
print('  Open multiple tabs or share your IP for LAN co-op!')
print('  Press Ctrl+C to stop.\n')

threading.Thread(target=ws_server, daemon=True).start()
httpd = http.server.HTTPServer(('0.0.0.0', PORT), GameHandler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
webbrowser.open(f'http://127.0.0.1:{PORT}/')
try:
    while True: threading.Event().wait(1)
except KeyboardInterrupt:
    print('\nServer stopped. Thanks for playing!')
