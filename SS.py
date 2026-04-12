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
/* === WOW-STYLE PLAYER UNIT FRAME === */
#bars{position:absolute;top:12px;left:12px;z-index:200;pointer-events:none;width:280px}
#player-frame{background:linear-gradient(180deg,rgba(30,24,16,.95),rgba(20,16,10,.92));border:2px solid #5a4a32;border-radius:6px;padding:8px 10px 6px;position:relative;box-shadow:0 2px 12px rgba(0,0,0,.6)}
#pf-header{display:flex;align-items:center;gap:8px;margin-bottom:5px}
#pf-portrait{width:42px;height:42px;border-radius:50%;border:2px solid #c8a96e;background:radial-gradient(circle,#3a3020,#1a1610);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0}
#pf-info{flex:1}
#pf-name{font-size:13px;color:#c8a96e;font-weight:700;font-family:'Times New Roman',serif;letter-spacing:1px}
#pf-level{font-size:10px;color:#aa9;margin-left:4px}
.bar-row{display:flex;align-items:center;margin-bottom:3px;font-size:10px}
.bar-label{width:26px;text-align:right;margin-right:5px;font-weight:700;color:#aaa;font-size:9px;text-shadow:0 1px 2px #000}
.bar-bg{flex:1;height:14px;background:rgba(0,0,0,.8);border:1px solid #444;border-radius:3px;overflow:hidden;position:relative;box-shadow:inset 0 1px 3px rgba(0,0,0,.5)}
.bar-fill{height:100%;transition:width .2s;border-radius:2px}
.bar-text{position:absolute;right:5px;top:0;line-height:14px;font-size:9px;color:#fff;text-shadow:1px 1px 2px #000;font-weight:700}
.hp-fill{background:linear-gradient(180deg,#44cc44,#228822);box-shadow:inset 0 1px 0 rgba(255,255,255,.15)}
.sta-fill{background:linear-gradient(180deg,#ccaa22,#887710);box-shadow:inset 0 1px 0 rgba(255,255,255,.15)}
.poi-fill{background:linear-gradient(180deg,#5588dd,#2244aa);box-shadow:inset 0 1px 0 rgba(255,255,255,.15)}
/* === WOW ACTION BAR === */
#action-bar{position:fixed;bottom:8px;left:50%;transform:translateX(-50%);z-index:400;display:none;align-items:center;gap:0;pointer-events:auto}
#action-bar.active{display:flex}
#ab-wrap{background:linear-gradient(180deg,rgba(40,32,20,.95),rgba(25,20,12,.98));border:2px solid #5a4a32;border-radius:6px;padding:5px 8px;display:flex;gap:3px;box-shadow:0 -2px 15px rgba(0,0,0,.5)}
.ab-slot{width:44px;height:44px;background:linear-gradient(180deg,#2a2418,#1a1610);border:2px solid #4a3a28;border-radius:4px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;position:relative;transition:border-color .15s,background .15s}
.ab-slot:hover{border-color:#c8a96e;background:linear-gradient(180deg,#3a3020,#2a2418)}
.ab-slot.on-cd{opacity:.5}
.ab-ico{font-size:20px;line-height:1;pointer-events:none}
.ab-key{position:absolute;bottom:1px;right:3px;font-size:8px;color:#887;font-weight:700;pointer-events:none}
.ab-name{font-size:6px;color:#aa9;white-space:nowrap;overflow:hidden;pointer-events:none;margin-top:1px}
.ab-cd{position:absolute;inset:0;background:rgba(0,0,0,.6);border-radius:3px;display:none;align-items:center;justify-content:center;font-size:14px;color:#ff8;font-weight:700}
.ab-slot.on-cd .ab-cd{display:flex}
/* === XP BAR === */
#xp-bar-wrap{position:fixed;bottom:60px;left:50%;transform:translateX(-50%);z-index:350;width:540px;display:none}
#xp-bar-wrap.active{display:block}
#xp-bar-bg{width:100%;height:10px;background:rgba(0,0,0,.7);border:1px solid #4a3a28;border-radius:5px;overflow:hidden}
#xp-bar-fill{height:100%;background:linear-gradient(90deg,#6a3acc,#aa66ff);border-radius:4px;transition:width .3s;width:0%}
#xp-bar-text{text-align:center;font-size:9px;color:#aa88dd;margin-top:2px}
/* === OSRS RIGHT PANEL === */
#osrs-panel{position:fixed;top:0;right:0;width:250px;height:100vh;z-index:300;display:none;flex-direction:column;pointer-events:auto}
#minimap-wrap{width:250px;height:168px;background:linear-gradient(180deg,#2b2016,#1e1810);border:2px solid #5a4a32;border-radius:0 0 0 8px;position:relative;overflow:hidden;box-shadow:-2px 2px 10px rgba(0,0,0,.4)}
#minimap-canvas{width:100%;height:100%;border-radius:0}
#minimap-orbs{position:absolute;top:8px;right:8px;display:flex;flex-direction:column;gap:6px}
.orb{width:32px;height:32px;border-radius:50%;border:2px solid #5a4a32;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;text-shadow:0 0 3px #000;box-shadow:0 1px 4px rgba(0,0,0,.5)}
.orb-hp{background:radial-gradient(circle,#44cc44,#1a5a1a);color:#fff}
.orb-pray{background:radial-gradient(circle,#3388ee,#1a2a5a);color:#fff}
.orb-run{background:radial-gradient(circle,#ccaa22,#5a4a0a);color:#fff}
#tab-strip{display:flex;background:linear-gradient(180deg,#3b3020,#2e2518);border:2px solid #5a4a32;border-top:0;gap:1px;padding:2px 2px 0}
.tab-btn{flex:1;padding:6px 0;text-align:center;cursor:pointer;font-size:15px;background:#2a2018;border-radius:4px 4px 0 0;border:1px solid transparent;transition:all .15s;line-height:1;position:relative}
.tab-btn:hover{background:#3a3020;border-color:#5a4a32;color:#e8d4a8}
.tab-btn.active{background:#4a3a28;border-color:#c8a96e;box-shadow:inset 0 -2px 0 #c8a96e,0 1px 4px rgba(200,169,110,.2)}
.tab-btn[title]:hover::after{content:attr(title);position:absolute;bottom:-22px;left:50%;transform:translateX(-50%);background:#1a1610;border:1px solid #5a4a32;color:#e8d4a8;font-size:9px;padding:2px 6px;border-radius:3px;white-space:nowrap;z-index:999;pointer-events:none}
#tab-content{flex:1;background:linear-gradient(180deg,#3b3020,#2e2518);border:2px solid #5a4a32;border-top:0;overflow-y:auto;padding:0;box-shadow:-2px 0 10px rgba(0,0,0,.3)}
#tab-content::-webkit-scrollbar{width:5px}#tab-content::-webkit-scrollbar-thumb{background:#6a5a42;border-radius:3px}#tab-content::-webkit-scrollbar-track{background:#2a2018}
.tab-page{display:none;padding:6px}
.tab-page.active{display:block}
/* Skills tab */
.sk-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2px}
.sk-cell{background:linear-gradient(180deg,#2e2418,#221c12);border:1px solid #4a3a28;padding:4px 2px;text-align:center;cursor:default;position:relative;border-radius:3px;transition:border-color .15s}
.sk-cell:hover{border-color:#c8a96e;background:linear-gradient(180deg,#3a3020,#2e2418)}
.sk-cell .sk-ico{font-size:16px;display:block;line-height:1}
.sk-cell .sk-name{font-size:7px;color:#aa9;display:block;white-space:nowrap;overflow:hidden}
.sk-cell .sk-lv{font-size:14px;font-weight:700;color:#ffdd44;display:block;text-shadow:0 1px 2px rgba(0,0,0,.5)}
.sk-cell .sk-xp{font-size:7px;color:#776;display:block}
.sk-total{text-align:center;padding:6px;font-size:12px;color:#ffcc44;background:linear-gradient(180deg,#2e2418,#221c12);border:1px solid #5a4a32;margin-top:4px;font-weight:700;border-radius:3px;text-shadow:0 1px 2px rgba(0,0,0,.5)}
/* Inventory tab */
.inv-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:3px}
.inv-slot{width:52px;height:52px;background:linear-gradient(180deg,#2e2418,#1e1810);border:2px solid #3a2a1a;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:8px;color:#aa9;text-align:center;line-height:1.1;cursor:pointer;transition:all .15s}
.inv-slot:hover{border-color:#c8a96e;background:linear-gradient(180deg,#3a3020,#2a2418);box-shadow:0 0 6px rgba(200,169,110,.2)}
/* Equipment tab */
.eq-grid{display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px}
.eq-row{display:flex;gap:4px}
.eq-slot{width:52px;height:52px;background:linear-gradient(180deg,#2e2418,#1e1810);border:2px solid #3a2a1a;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:8px;color:#aa9;text-align:center;flex-direction:column;cursor:pointer;transition:all .15s}
.eq-slot:hover{border-color:#c8a96e;box-shadow:0 0 8px rgba(200,169,110,.25)}
.eq-slot .eq-ico{font-size:18px}
.eq-slot .eq-name{font-size:7px;color:#cc9944;white-space:nowrap;overflow:hidden;max-width:48px}
.eq-stats{font-size:10px;color:#aa9;text-align:center;margin-top:4px;padding:6px;background:linear-gradient(180deg,#2e2418,#221c12);border:1px solid #4a3a28;border-radius:3px}
.eq-stats span{color:#ffcc44;font-weight:700}
/* Combat tab */
.cmb-info{padding:10px;text-align:center;background:linear-gradient(180deg,rgba(50,40,25,.3),transparent);border-radius:4px;margin-bottom:4px}
.cmb-info .cmb-lv{font-size:32px;color:#ffcc44;font-weight:700;text-shadow:0 2px 6px rgba(255,200,50,.3);font-family:'Times New Roman',serif}
.cmb-info .cmb-lbl{font-size:11px;color:#887;letter-spacing:2px;text-transform:uppercase}
.cmb-row{display:flex;justify-content:space-between;padding:4px 10px;font-size:11px;border-bottom:1px solid rgba(90,74,50,.3);transition:background .1s}
.cmb-row:hover{background:rgba(200,169,110,.06)}
.cmb-row span:first-child{color:#aa9}.cmb-row span:last-child{color:#ffdd44;font-weight:700}
/* Prayer tab */
.pray-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:3px}
.pray-slot{width:42px;height:42px;background:linear-gradient(180deg,#2e2418,#1e1810);border:2px solid #3a2a1a;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:18px;cursor:pointer;opacity:.4;transition:all .15s}
.pray-slot.unlocked{opacity:1}
.pray-slot.unlocked:hover{border-color:#c8a96e;transform:scale(1.08)}
.pray-slot.pray-active{border-color:#ffcc44;background:linear-gradient(180deg,#3a3018,#2a2410);box-shadow:0 0 10px rgba(255,200,50,.4)}
/* Magic tab */
.magic-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:3px}
.spell-slot{width:52px;height:46px;background:linear-gradient(180deg,#1e1828,#161220);border:2px solid #2a2848;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:17px;cursor:pointer;flex-direction:column;opacity:.4;transition:all .15s}
.spell-slot.unlocked{opacity:1}
.spell-slot.unlocked:hover{border-color:#6688dd;transform:scale(1.05);box-shadow:0 0 8px rgba(100,130,220,.3)}
.spell-slot .sp-name{font-size:7px;color:#88a}
/* Chat box */
#chatbox{position:fixed;bottom:0;left:0;width:380px;height:160px;z-index:300;display:none;flex-direction:column;background:linear-gradient(180deg,rgba(26,22,16,.92),rgba(20,16,10,.95));border:2px solid #5a4a32;border-bottom:0;border-left:0;border-radius:0 6px 0 0;box-shadow:2px -2px 10px rgba(0,0,0,.4)}
#chat-log{flex:1;overflow-y:auto;padding:6px 10px;font-size:11px;font-family:'Consolas','Courier New',monospace;color:#aa9;line-height:1.5}
#chat-log::-webkit-scrollbar{width:4px}#chat-log::-webkit-scrollbar-thumb{background:#6a5a42;border-radius:2px}#chat-log::-webkit-scrollbar-track{background:transparent}
#chat-tabs{display:flex;background:linear-gradient(90deg,#2b2016,#3b3020);border-top:1px solid #4a3a28;padding:0 2px}
.chat-tab{padding:4px 12px;font-size:10px;color:#776;cursor:pointer;border-right:1px solid rgba(74,58,40,.4);transition:all .15s;letter-spacing:.5px}
.chat-tab.active{color:#ffcc44;background:rgba(200,169,110,.1)}
.chat-tab:hover{color:#e8d4a8;background:rgba(200,169,110,.05)}
/* Target Frame (WoW-style) */
#target-frame{position:fixed;top:12px;left:310px;z-index:200;background:linear-gradient(180deg,rgba(30,24,16,.95),rgba(20,16,10,.92));border:2px solid #5a4a32;border-radius:6px;padding:8px 14px;display:none;align-items:center;gap:10px;min-width:240px;box-shadow:0 2px 12px rgba(0,0,0,.6)}
#target-frame.active{display:flex}
#tf-icon{font-size:30px;line-height:1;width:40px;height:40px;display:flex;align-items:center;justify-content:center;border:2px solid #cc4444;border-radius:50%;background:radial-gradient(circle,#3a2020,#1a1010)}
#tf-info{flex:1}
#tf-name{font-size:13px;color:#ff6644;font-weight:700;white-space:nowrap;font-family:'Times New Roman',serif}
#tf-lv{font-size:10px;color:#aa9;margin-left:6px}
#tf-hp-bg{width:100%;height:12px;background:rgba(0,0,0,.8);border:1px solid #555;border-radius:3px;margin-top:4px;overflow:hidden;box-shadow:inset 0 1px 3px rgba(0,0,0,.5)}
#tf-hp-fill{height:100%;background:linear-gradient(180deg,#cc3030,#882020);transition:width .15s;border-radius:2px}
#tf-hp-text{font-size:9px;color:#ddd;text-align:center;margin-top:2px;font-weight:700}
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
#controls{position:absolute;bottom:78px;left:50%;transform:translateX(-50%);z-index:100;font-size:9px;color:#554;text-align:center;pointer-events:none;background:rgba(0,0,0,.4);padding:3px 10px;border-radius:10px;letter-spacing:.5px;opacity:.6;transition:opacity .3s}
#controls:hover{opacity:1}
#locbar{position:absolute;top:8px;left:50%;transform:translateX(-50%);z-index:150;font-size:12px;color:#c8a96e;pointer-events:none;background:linear-gradient(90deg,transparent,rgba(20,16,10,.8),transparent);padding:4px 30px;letter-spacing:2px;font-family:'Times New Roman',serif;text-shadow:0 1px 4px rgba(0,0,0,.6)}
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
<div id="player-frame">
<div id="pf-header"><div id="pf-portrait">&#9876;</div><div id="pf-info"><span id="pf-name">Knight</span><span id="pf-level">Lv 3</span></div></div>
<div class="bar-row"><span class="bar-label">HP</span><div class="bar-bg"><div class="bar-fill hp-fill" id="hpB" style="width:100%"></div><span class="bar-text" id="hpT">142/142</span></div></div>
<div class="bar-row"><span class="bar-label">STA</span><div class="bar-bg"><div class="bar-fill sta-fill" id="stB" style="width:100%"></div><span class="bar-text" id="stT">100/100</span></div></div>
<div class="bar-row"><span class="bar-label">MP</span><div class="bar-bg"><div class="bar-fill poi-fill" id="poB" style="width:100%"></div><span class="bar-text" id="poT">68/68</span></div></div>
</div>
</div>
<div id="locbar">Lv 3 &#183; Lumbridge</div>
<!-- WOW ACTION BAR -->
<div id="action-bar"><div id="ab-wrap">
<div class="ab-slot" data-action="attack" title="Attack"><span class="ab-ico">&#9876;</span><span class="ab-name">Attack</span><span class="ab-key">1</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="parry" title="Parry/Block"><span class="ab-ico">&#128737;</span><span class="ab-name">Parry</span><span class="ab-key">2</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="heal" title="Estus Flask"><span class="ab-ico">&#127863;</span><span class="ab-name">Heal</span><span class="ab-key">3</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="bones" title="Bury Bones"><span class="ab-ico">&#129460;</span><span class="ab-name">Bones</span><span class="ab-key">4</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="prayer" title="Prayer (Q)"><span class="ab-ico">&#10013;</span><span class="ab-name">Prayer</span><span class="ab-key">Q</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="gather" title="Gather (F)"><span class="ab-ico">&#9935;</span><span class="ab-name">Gather</span><span class="ab-key">F</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="roll" title="Dodge Roll"><span class="ab-ico">&#128168;</span><span class="ab-name">Roll</span><span class="ab-key">Spc</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="lock" title="Cycle Target"><span class="ab-ico">&#127919;</span><span class="ab-name">Lock</span><span class="ab-key">Tab</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="map" title="World Map"><span class="ab-ico">&#128506;</span><span class="ab-name">Map</span><span class="ab-key">M</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="inv" title="Inventory (I)"><span class="ab-ico">&#127890;</span><span class="ab-name">Bag</span><span class="ab-key">I</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="skills" title="Skills (K)"><span class="ab-ico">&#9733;</span><span class="ab-name">Skills</span><span class="ab-key">K</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="save" title="Quick Save"><span class="ab-ico">&#128190;</span><span class="ab-name">Save</span><span class="ab-key">F5</span><div class="ab-cd"></div></div>
</div></div>
<!-- XP BAR -->
<div id="xp-bar-wrap"><div id="xp-bar-bg"><div id="xp-bar-fill"></div></div><div id="xp-bar-text">Combat XP: 0</div></div>
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
<div class="tab-page" id="tp-settings"><div style="padding:8px;font-size:10px;color:#aa9"><b style="color:#cc9944">Controls</b><br><br><b style="color:#cc9944">Mouse:</b><br>LClick - Attack / Target<br>RClick - Block / Parry<br>MClick+Drag - Camera<br>Scroll - Zoom<br><br><b style="color:#cc9944">Keys:</b><br>WASD - Move<br>Space - Roll<br>Tab - Cycle Lock-on<br>1 - Attack<br>2 - Parry<br>3 - Heal (Estus)<br>4 - Bury Bones<br>Q - Prayer Tab<br>F - Gather/Skill<br>M - World Map<br>Esc - Deselect / Close Map<br>I - Inventory<br>K - Skills<br>F5 - Save<br><br><b style="color:#cc9944">Gamepad (Dark Souls):</b><br>LStick - Move<br>RStick - Camera<br>RT - Light Attack<br>RB - Parry / Heavy<br>LT - Block / Guard<br>B/○ - Roll<br>A/✕ - Heal (Estus)<br>X/□ - Use Item<br>Y/△ - Two-Hand<br>LS Click - Lock-on<br>Start - Inventory<br>Back - Skills</div></div>
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
import{ShaderPass}from'three/addons/postprocessing/ShaderPass.js';
// Dark Souls color grading + vignette shader
const DSColorGradeShader={uniforms:{tDiffuse:{value:null},vignetteAmount:{value:.06},desatAmount:{value:0.0},tintR:{value:1.02},tintG:{value:1.01},tintB:{value:1.0}},vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
fragmentShader:'uniform sampler2D tDiffuse;uniform float vignetteAmount;uniform float desatAmount;uniform float tintR;uniform float tintG;uniform float tintB;varying vec2 vUv;void main(){vec4 c=texture2D(tDiffuse,vUv);c.rgb*=vec3(tintR,tintG,tintB);c.rgb=pow(c.rgb,vec3(0.95));vec2 q=vUv;q*=1.0-q;float v=q.x*q.y*16.0;v=pow(v,vignetteAmount);c.rgb*=mix(vec3(0.85),vec3(1.0),v);gl_FragColor=c;}'};

function mkTex(w,h,fn){const c=document.createElement('canvas');c.width=w;c.height=h;fn(c.getContext('2d'),w,h);const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;return t}
// Dark Souls style ground - dark, muddy, mossy
const texDirt=mkTex(512,512,(c,w,h)=>{c.fillStyle='#6a6248';c.fillRect(0,0,w,h);for(let i=0;i<18000;i++){const v=70+Math.random()*70;const g=Math.random()>.85?v+15:0;c.fillStyle=`rgb(${v+15},${v+8+g},${v-5})`;c.fillRect(Math.random()*w,Math.random()*h,1+Math.random()*4,1+Math.random()*4)}for(let i=0;i<500;i++){c.fillStyle=`rgba(40,55,30,${.06+Math.random()*.1})`;c.fillRect(Math.random()*w,Math.random()*h,3+Math.random()*12,3+Math.random()*12)}for(let i=0;i<300;i++){c.fillStyle=`rgba(90,80,60,${.06+Math.random()*.1})`;c.beginPath();c.arc(Math.random()*w,Math.random()*h,1+Math.random()*3,0,Math.PI*2);c.fill()}for(let i=0;i<100;i++){c.fillStyle=`rgba(50,60,35,${.05+Math.random()*.08})`;const rx=Math.random()*w,ry=Math.random()*h;c.fillRect(rx,ry,Math.random()*20,1)}});texDirt.repeat.set(20,20);
// Gothic stone - dark grey with deep mortar lines, weathering, cracks
const texStone=mkTex(512,512,(c,w,h)=>{c.fillStyle='#8a8578';c.fillRect(0,0,w,h);for(let i=0;i<4000;i++){const v=90+Math.random()*60;c.fillStyle=`rgb(${v+5},${v+3},${v-2})`;c.fillRect(Math.random()*w,Math.random()*h,2+Math.random()*14,2+Math.random()*14)}c.strokeStyle='#4a4540';c.lineWidth=2.5;for(let y=0;y<h;y+=32){c.beginPath();c.moveTo(0,y+Math.random()*2);c.lineTo(w,y+Math.random()*2);c.stroke();for(let x=(Math.floor(y/32)%2)*16;x<w;x+=32){c.beginPath();c.moveTo(x+Math.random()*2,y);c.lineTo(x+Math.random()*2,y+32);c.stroke()}}for(let i=0;i<40;i++){c.strokeStyle=`rgba(50,45,38,${.1+Math.random()*.15})`;c.lineWidth=.5+Math.random();c.beginPath();const sx=Math.random()*w,sy=Math.random()*h;c.moveTo(sx,sy);for(let j=0;j<5;j++)c.lineTo(sx+Math.random()*35-17,sy+Math.random()*35-17);c.stroke()}for(let i=0;i<200;i++){c.fillStyle=`rgba(60,75,50,${.04+Math.random()*.06})`;c.fillRect(Math.random()*w,Math.random()*h,2+Math.random()*8,2+Math.random()*8)}for(let i=0;i<80;i++){c.fillStyle=`rgba(120,115,100,${.05+Math.random()*.08})`;c.beginPath();c.arc(Math.random()*w,Math.random()*h,1+Math.random()*4,0,Math.PI*2);c.fill()}});
// Dark bark with deep grooves
const texBark=mkTex(128,256,(c,w,h)=>{c.fillStyle='#4a3828';c.fillRect(0,0,w,h);for(let y=0;y<h;y+=2){const b=40+Math.random()*35;c.fillStyle=`rgb(${b+12},${b+4},${b-6})`;c.fillRect(0,y,w,2)}for(let i=0;i<50;i++){c.strokeStyle=`rgba(25,18,10,${.2+Math.random()*.25})`;c.lineWidth=1+Math.random()*2.5;c.beginPath();c.moveTo(Math.random()*w,0);c.lineTo(Math.random()*w,h);c.stroke()}for(let i=0;i<20;i++){c.fillStyle=`rgba(70,55,35,${.1+Math.random()*.1})`;const kx=Math.random()*w,ky=Math.random()*h;c.beginPath();c.ellipse(kx,ky,2+Math.random()*3,1+Math.random()*2,0,0,Math.PI*2);c.fill()}});
// Weathered dark wood
const texWood=mkTex(128,128,(c,w,h)=>{c.fillStyle='#5a4838';c.fillRect(0,0,w,h);for(let y=0;y<h;y+=2){const b=50+Math.random()*40;c.fillStyle=`rgb(${b+15},${b+8},${b-8})`;c.fillRect(0,y,w,2+Math.random())}for(let i=0;i<30;i++){c.strokeStyle=`rgba(30,22,14,${.15+Math.random()*.2})`;c.lineWidth=.5+Math.random()*.5;c.beginPath();c.moveTo(Math.random()*w,0);c.lineTo(Math.random()*w,h);c.stroke()}for(let i=0;i<15;i++){c.fillStyle=`rgba(80,65,45,${.08+Math.random()*.08})`;c.fillRect(Math.random()*w,Math.random()*h,Math.random()*6,Math.random()*6)}});
// Metal texture for armor
const texMetal=mkTex(256,256,(c,w,h)=>{c.fillStyle='#5a5a65';c.fillRect(0,0,w,h);for(let i=0;i<2500;i++){const v=60+Math.random()*50;c.fillStyle=`rgb(${v+3},${v+3},${v+10})`;c.fillRect(Math.random()*w,Math.random()*h,1+Math.random()*4,1+Math.random()*4)}for(let i=0;i<80;i++){c.strokeStyle=`rgba(90,90,100,${.08+Math.random()*.12})`;c.lineWidth=.5+Math.random()*.5;c.beginPath();c.moveTo(Math.random()*w,Math.random()*h);c.lineTo(Math.random()*w,Math.random()*h);c.stroke()}for(let i=0;i<20;i++){c.fillStyle=`rgba(130,125,115,${.06+Math.random()*.08})`;c.beginPath();c.arc(Math.random()*w,Math.random()*h,5+Math.random()*15,0,Math.PI*2);c.fill()}for(let i=0;i<40;i++){c.fillStyle=`rgba(70,68,60,${.1+Math.random()*.1})`;c.fillRect(Math.random()*w,Math.random()*h,1,1+Math.random()*3)}});

const MS=THREE.MeshStandardMaterial;
const mt={
gnd:new MS({map:texDirt,roughness:.92,metalness:.02}),
st:new MS({map:texStone,roughness:.75,metalness:.08}),
stD:new MS({map:texStone,color:0x7a7568,roughness:.82,metalness:.05}),
stGoth:new MS({map:texStone,color:0x8a8578,roughness:.72,metalness:.1}),
bk:new MS({map:texBark,roughness:.9}),
lf:new MS({color:0x1a4a18,roughness:.85,flatShading:true}),
lfL:new MS({color:0x2a5a22,roughness:.8,flatShading:true}),
wd:new MS({map:texWood,roughness:.85}),
rf:new MS({color:0x6a5a48,roughness:.9}),
rfSlate:new MS({color:0x5a5855,roughness:.82,metalness:.12}),
wt:new MS({color:0x1a5a6a,roughness:.08,metalness:.55,transparent:true,opacity:.7,side:THREE.DoubleSide,emissive:0x0a3040,emissiveIntensity:.2}),
fl:new MS({color:0xff6600,emissive:0xff4400,emissiveIntensity:3.5,roughness:1}),
flEmber:new MS({color:0xff9955,emissive:0xff7733,emissiveIntensity:2,roughness:1,transparent:true,opacity:.8}),
rk:new MS({color:0x8a8578,roughness:.88}),rkD:new MS({color:0x6a6558,roughness:.9}),
armorDk:new MS({map:texMetal,color:0x3a3a42,roughness:.3,metalness:.9}),
armorLt:new MS({map:texMetal,color:0x5a5a65,roughness:.35,metalness:.85}),
armorWorn:new MS({map:texMetal,color:0x4a4840,roughness:.42,metalness:.78}),
chainmail:new MS({color:0x4a4a55,roughness:.4,metalness:.75}),
skin:new MS({color:0xc4a882,roughness:.8}),
cape:new MS({color:0x7a2222,roughness:.85,side:THREE.DoubleSide}),
capeTattered:new MS({color:0x5a1818,roughness:.88,side:THREE.DoubleSide,transparent:true,opacity:.92}),
swordBlade:new MS({color:0xccccdd,roughness:.06,metalness:.97,emissive:0x222233,emissiveIntensity:.12}),
swordHilt:new MS({color:0x5a4028,roughness:.7,metalness:.35}),
gold:new MS({color:0xd8b060,roughness:.28,metalness:.88,emissive:0x302010,emissiveIntensity:.12}),
leather:new MS({color:0x4a3a28,roughness:.88,metalness:.05}),
};
function eMat(t){return new MS({color:t==='goblin'?0x2a5a28:t==='cow'?0x7a4a2a:0xcca855,roughness:.7,metalness:.08})}

const skillDefs=['Attack','Strength','Defence','Hitpoints','Ranged','Prayer','Magic','Cooking','Woodcutting','Fishing','Mining','Smithing','Crafting','Firemaking','Herblore','Agility','Thieving','Slayer','Runecraft'];
const skillIcons={Attack:'\u2694',Strength:'\uD83D\uDCAA',Defence:'\uD83D\uDEE1',Hitpoints:'\u2764',Ranged:'\uD83C\uDFF9',Prayer:'\u271D',Magic:'\u2728',Cooking:'\uD83C\uDF56',Woodcutting:'\uD83E\uDE93',Fishing:'\uD83C\uDFA3',Mining:'\u26CF',Smithing:'\uD83D\uDD28',Crafting:'\u2702',Firemaking:'\uD83D\uDD25',Herblore:'\uD83C\uDF3F',Agility:'\uD83C\uDFC3',Thieving:'\uD83D\uDC4B',Slayer:'\uD83D\uDC80',Runecraft:'\uD83D\uDD2E'};
const skills={};skillDefs.forEach(s=>skills[s]={lvl:1,xp:0});skills.Hitpoints.lvl=10;skills.Hitpoints.xp=1154;skills.Attack.lvl=3;skills.Attack.xp=174;skills.Strength.lvl=2;skills.Strength.xp=83;skills.Defence.lvl=2;skills.Defence.xp=83;
const sgEl=document.getElementById('skill-grid');
skillDefs.forEach(s=>{const d=document.createElement('div');d.className='sk-cell';d.id='sk-'+s;d.innerHTML=`<span class="sk-ico">${skillIcons[s]||''}</span><span class="sk-name">${s}</span><span class="sk-lv">${skills[s].lvl}</span><span class="sk-xp">${skills[s].xp}xp</span>`;sgEl.appendChild(d)});
const invEl=document.getElementById('inv-grid');
for(let i=0;i<28;i++){const d=document.createElement('div');d.className='inv-slot';d.id='inv-'+i;invEl.appendChild(d)}
const inventory=[];
// Map common item names to gear slots for equip-from-inventory
const itemSlotMap={};
function updateInvUI(){for(let i=0;i<28;i++){const el=document.getElementById('inv-'+i);el.textContent=inventory[i]||'';
el.onclick=null;
if(inventory[i]){const item=inventory[i];
el.onclick=()=>{
// Check if item is equippable by matching specialLoot or common gear names
const sl=typeof specialLoot!=='undefined'?specialLoot.find(l=>l.name===item):null;
if(sl){const old=equipped[sl.slot];equipped[sl.slot]={name:sl.name,atk:sl.atk,def:sl.def,str:sl.str};
const idx=inventory.indexOf(item);if(idx>=0)inventory.splice(idx,1);
if(old&&old.name!=='None')inventory.push(old.name);
log('Equipped '+sl.name+' [ATK+'+sl.atk+' DEF+'+sl.def+' STR+'+sl.str+']','#0ff');updateInvUI();updateEqUI();return}
// Check if it's a skill item — use it
if(typeof skillItems!=='undefined'&&skillItems[item]){const sk=skillItems[item];const idx=inventory.indexOf(item);if(idx>=0)inventory.splice(idx,1);
skills[sk.skill].xp+=sk.xp;const lv=Math.max(skills[sk.skill].lvl,Math.floor(1+Math.sqrt(skills[sk.skill].xp/50)));
if(lv>skills[sk.skill].lvl){skills[sk.skill].lvl=lv;log(sk.skill+' level up! Lv '+lv,'#ff0')}
log('Used '+item+': '+sk.skill+' +'+sk.xp+'xp','#cc4');updateInvUI();if(typeof updateSkillUI==='function')updateSkillUI();return}
}}}}

// === TAB SWITCHING ===
document.querySelectorAll('.tab-btn').forEach(btn=>btn.addEventListener('click',()=>{
document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));
btn.classList.add('active');
const tp=document.getElementById('tp-'+btn.dataset.tab);if(tp)tp.classList.add('active')}));

// === ACTION BAR CLICKS ===
function switchTab(tabName){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));const btn=document.querySelector('[data-tab="'+tabName+'"]');if(btn)btn.classList.add('active');const tp=document.getElementById('tp-'+tabName);if(tp)tp.classList.add('active')}
document.querySelectorAll('.ab-slot').forEach(slot=>slot.addEventListener('click',()=>{
const a=slot.dataset.action;
if(a==='attack')document.dispatchEvent(new KeyboardEvent('keydown',{key:'1'}));
else if(a==='parry')document.dispatchEvent(new KeyboardEvent('keydown',{key:'2'}));
else if(a==='heal')document.dispatchEvent(new KeyboardEvent('keydown',{key:'3'}));
else if(a==='bones')document.dispatchEvent(new KeyboardEvent('keydown',{key:'4'}));
else if(a==='prayer')switchTab('prayer');
else if(a==='gather')document.dispatchEvent(new KeyboardEvent('keydown',{key:'f'}));
else if(a==='roll')document.dispatchEvent(new KeyboardEvent('keydown',{key:' '}));
else if(a==='lock')document.dispatchEvent(new KeyboardEvent('keydown',{key:'Tab'}));
else if(a==='map')document.dispatchEvent(new KeyboardEvent('keydown',{key:'m'}));
else if(a==='inv')switchTab('inventory');
else if(a==='skills')switchTab('skills');
else if(a==='save')document.dispatchEvent(new KeyboardEvent('keydown',{key:'F5'}));
}));

// === LOG -> CHAT-LOG ===
function log(msg,col){const el=document.getElementById('chat-log');if(!el)return;const d=document.createElement('div');d.style.color=col||'#887';d.textContent=msg;el.appendChild(d);el.scrollTop=el.scrollHeight}

// === EQUIPMENT UI UPDATE ===
function updateEqUI(){
const gs=totalGear();
document.getElementById('es-atk').textContent=gs.atk;
document.getElementById('es-def').textContent=gs.def;
document.getElementById('es-str').textContent=gs.str;
gearSlots.forEach(s=>{const el=document.getElementById('eq-'+s);if(el){el.querySelector('.eq-name').textContent=equipped[s].name||s;
el.onclick=()=>{if(equipped[s].name!=='None'){const old=equipped[s].name;if(inventory.length<28){inventory.push(old);updateInvUI()}
equipped[s]={name:'None',atk:0,def:0,str:0};log('Unequipped '+old,'#cc8');updateEqUI()}}}});
document.getElementById('cmb-gatk').textContent=gs.atk;
document.getElementById('cmb-gdef').textContent=gs.def;
document.getElementById('cmb-gstr').textContent=gs.str;
if(typeof refreshPlayerModel==='function')refreshPlayerModel()}

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
mmCanvas.width=250;mmCanvas.height=168;
function drawMinimap(){
mmCtx.fillStyle='#2b2016';mmCtx.fillRect(0,0,250,168);
const scale=.12,cx=125,cy=84;
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
let playerClass='knight';
let enemies=[],lootArr=[],particles=[],torchData=[];
let dustPts,time=0;
const lightPool=[];const MAX_LIGHTS=8;
const torchPositions=[];
const solidMeshes=[];
const solidBoxes=[];
// Dungeon system globals (must be accessible from game loop)
let inDungeon=null;let dungeonGroup=null;const dungeons=[];const dungeonObjs=[];const enterableBuildings=[];
// Culling globals
let cullFrame=0;let distanceCull=null,shadowCull=null,checkInteractions=null;
// Terrain mesh reference for accurate height + door system
let groundMesh=null;const doors=[];
// Teleport system — destinations for each city
const teleports=[
{name:'Umbridgelay',x:0,z:0,unlocked:true},
{name:'Arrockvay',x:550,z:50,unlocked:true},
{name:'Aladorfay',x:-480,z:280,unlocked:true},
{name:'Ardougneway',x:-1200,z:100,unlocked:true},
{name:'Alway Aridkhay',x:580,z:400,unlocked:true},
{name:'Ortpay Arimsay',x:-160,z:480,unlocked:true},
{name:'Edgevillay',x:150,z:-350,unlocked:true},
{name:'Aynordray',x:-300,z:-150,unlocked:true},
{name:'Atherbycay',x:-500,z:-400,unlocked:true},
{name:'Arbarianba Illagevay',x:280,z:-250,unlocked:true},
{name:'Anilleyay',x:-1400,z:500,unlocked:true},
{name:'Anifiscay',x:1300,z:-200,unlocked:true},
{name:'Aramjakay',x:-200,z:1800,unlocked:true},
{name:'Ollheimtray',x:-200,z:-3500,unlocked:true},
{name:'Eerssay Illagevay',x:-800,z:-100,unlocked:true},
{name:'Ellekkaray',x:-400,z:-3800,unlocked:true},
{name:'Eldagrimkay',x:-800,z:-3200,unlocked:true},
{name:'Ifddinas pray',x:-4000,z:-300,unlocked:true},
{name:'Aartzhay Itycay',x:1800,z:1200,unlocked:true},
{name:'Ophanemsay',x:2500,z:200,unlocked:true},
{name:'Anarisza y',x:800,z:800,unlocked:true}
];
let showTeleport=false;
// Skill items: items that grant XP when used (F key near resource spots)
const skillItems={
'Bronze Pickaxe':{skill:'Mining',xp:15},'Iron Pickaxe':{skill:'Mining',xp:25},'Steel Pickaxe':{skill:'Mining',xp:40},'Rune Pickaxe':{skill:'Mining',xp:65},
'Bronze Hatchet':{skill:'Woodcutting',xp:15},'Iron Hatchet':{skill:'Woodcutting',xp:25},'Steel Hatchet':{skill:'Woodcutting',xp:40},'Rune Hatchet':{skill:'Woodcutting',xp:65},
'Fishing Rod':{skill:'Fishing',xp:30},'Fly Fishing Rod':{skill:'Fishing',xp:50},'Harpoon':{skill:'Fishing',xp:80},
'Tinderbox':{skill:'Firemaking',xp:25},'Augmented Tinderbox':{skill:'Firemaking',xp:60},
'Chisel':{skill:'Crafting',xp:20},'Needle':{skill:'Crafting',xp:30},
'Hammer':{skill:'Smithing',xp:25},'Golden Hammer':{skill:'Smithing',xp:60},
'Knife':{skill:'Cooking',xp:20},'Raw Beef':{skill:'Cooking',xp:15},'Raw Chicken':{skill:'Cooking',xp:10},'Raw Meat':{skill:'Cooking',xp:15},'Raw Salmon':{skill:'Cooking',xp:30},'Raw Swordfish':{skill:'Cooking',xp:50},'Raw Tuna':{skill:'Cooking',xp:40},'Raw Bear Meat':{skill:'Cooking',xp:25},'Raw Shark x5':{skill:'Cooking',xp:100},'Raw Chompy':{skill:'Cooking',xp:35},
'Bones':{skill:'Prayer',xp:15},'Big Bones':{skill:'Prayer',xp:30},'Dragon Bones':{skill:'Prayer',xp:72},'Drake Bones':{skill:'Prayer',xp:50},'Wyrm Bones':{skill:'Prayer',xp:55},'Troll Bones':{skill:'Prayer',xp:40},'Wolf Bones':{skill:'Prayer',xp:25},'Wyvern Bones':{skill:'Prayer',xp:60},'Hydra Bones':{skill:'Prayer',xp:80},
'Nature Rune':{skill:'Runecraft',xp:20},'Death Rune':{skill:'Runecraft',xp:35},'Blood Rune':{skill:'Runecraft',xp:50},'Soul Rune x3':{skill:'Runecraft',xp:60},'Chaos Rune x5':{skill:'Runecraft',xp:40},'Fire Rune x20':{skill:'Runecraft',xp:30},'Law Rune x3':{skill:'Runecraft',xp:45},'Mind Rune x15':{skill:'Runecraft',xp:25},'Wrath Rune x5':{skill:'Runecraft',xp:70},
'Herb':{skill:'Herblore',xp:25},'Garlic':{skill:'Herblore',xp:10},'Antidote':{skill:'Herblore',xp:30},'Antipoison':{skill:'Herblore',xp:20},'Prayer Potion':{skill:'Herblore',xp:40},
'Lockpick':{skill:'Thieving',xp:30},'Spider Silk':{skill:'Crafting',xp:15},'Cowhide':{skill:'Crafting',xp:10},'Snake Skin':{skill:'Crafting',xp:20},'Lizard Skin':{skill:'Crafting',xp:25},'Dragon Hide':{skill:'Crafting',xp:60},'Black Dragonhide':{skill:'Crafting',xp:80},'Hydra Leather':{skill:'Crafting',xp:70},
'Iron Ore':{skill:'Mining',xp:20},'Gold Ore':{skill:'Mining',xp:40},'Elemental Ore':{skill:'Mining',xp:50},'Runite Ore':{skill:'Mining',xp:80},'Granite x3':{skill:'Mining',xp:45}
};
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
// Skip if entity is on top of or above this solid (standing on it)
if(py>=b.max.y-1)continue;
if(ox>minX&&ox<maxX&&oz>minZ&&oz<maxZ&&py>b.min.y-6){
const ovL=ox-minX,ovR=maxX-ox,ovB=oz-minZ,ovF=maxZ-oz;
const m=Math.min(ovL,ovR,ovB,ovF);
if(m===ovL)ox=minX;else if(m===ovR)ox=maxX;
else if(m===ovB)oz=minZ;else oz=maxZ}}}
return{x:ox,z:oz}}
// Surface height: terrain or top of any walkable solid below the entity
function surfaceH(px,pz,py){
const th=meshTerrainH(px,pz);
let best=th;
const pr=PLAYER_R;
for(const b of solidBoxes){
if(px>b.min.x-pr&&px<b.max.x+pr&&pz>b.min.z-pr&&pz<b.max.z+pr){
// If player is near or above the top of this box, they can stand on it
if(b.max.y>best&&(py===undefined||py>=b.max.y-3)){best=b.max.y}}}
return best}
// Accurate terrain mesh height via bilinear interpolation on the actual geometry
function meshTerrainH(wx,wz){
if(!groundMesh)return terrainH(wx,wz);
const pos=groundMesh.geometry.attributes.position;
const segs=200,size=80000,half=size/2,cell=size/segs,cols=segs+1;
const fi=(wx+half)/cell,fj=(half+wz)/cell;
const i0=Math.max(0,Math.min(segs-1,Math.floor(fi))),j0=Math.max(0,Math.min(segs-1,Math.floor(fj)));
const fx=fi-i0,fz=fj-j0;
const h00=pos.getZ(j0*cols+i0),h10=pos.getZ(j0*cols+i0+1),h01=pos.getZ((j0+1)*cols+i0),h11=pos.getZ((j0+1)*cols+i0+1);
return h00*(1-fx)*(1-fz)+h10*fx*(1-fz)+h01*(1-fx)*fz+h11*fx*fz}
let keys={},mouse={x:0,y:0,dx:0,dy:0,down:false,right:false,mid:false};
let camYaw=0,camPitch=.35,camDist=60;
let player={x:0,z:0,y:2,vx:0,vz:0,speed:.42,hp:142,maxHp:142,sta:100,maxSta:100,poi:68,maxPoi:68,ang:0,rolling:false,rollT:0,atkCD:0,dead:false,deadTimer:0,blocking:false};
let lockOn=null,lockIdx=-1;
let showSkills=false,showInv=false;
let gpAxes=[0,0,0,0],gpButtons={};

const drops={goblin:[{i:"Bronze Sword",c:.42},{i:"Coins x17",c:.68},{i:"Bones",c:1},{i:"Goblin Mail",c:.08},{i:"Bronze Pickaxe",c:.05},{i:"Nature Rune",c:.12},{i:"Chef Hat",c:.03},{i:"Goblin Book",c:.02}],
cow:[{i:"Raw Beef",c:1},{i:"Cowhide",c:.85},{i:"Coins x5",c:.4},{i:"Bucket of Milk",c:.3},{i:"Cow Horn",c:.1}],
chicken:[{i:"Raw Chicken",c:1},{i:"Feathers x12",c:.9},{i:"Bones",c:1},{i:"Egg",c:.4}],
guard:[{i:"Iron Sword",c:.3},{i:"Coins x45",c:.8},{i:"Bread",c:.5},{i:"Steel Chainbody",c:.08},{i:"Iron Pickaxe",c:.04},{i:"Guard Journal",c:.02},{i:"Iron Hatchet",c:.06}],
skeleton:[{i:"Bones",c:1},{i:"Iron Arrow x5",c:.6},{i:"Ancient Coin",c:.1},{i:"Skull Fragment",c:.15},{i:"Death Rune",c:.08},{i:"Skeletal Boots",c:.03}],
pirate:[{i:"Coins x30",c:.7},{i:"Rum",c:.4},{i:"Eye Patch",c:.05},{i:"Cutlass",c:.1},{i:"Fishing Rod",c:.06},{i:"Raw Swordfish",c:.15},{i:"Treasure Map",c:.02},{i:"Cannon Ball x5",c:.08}],
barbarian:[{i:"Raw Meat",c:.8},{i:"Coins x12",c:.6},{i:"Bear Fur",c:.3},{i:"Steel Hatchet",c:.08},{i:"Tinderbox",c:.1},{i:"Raw Salmon",c:.2},{i:"Barbarian Helm",c:.04}],
vampire:[{i:"Blood Rune",c:.4},{i:"Coins x60",c:.5},{i:"Garlic",c:.2},{i:"Vampyre Dust",c:.7},{i:"Blood Shard",c:.03},{i:"Dark Bow",c:.02},{i:"Ruby Ring",c:.05}],
demon:[{i:"Dragon Bones",c:.8},{i:"Rune Scimitar",c:.05},{i:"Coins x200",c:.9},{i:"Infernal Ash",c:.6},{i:"Fire Rune x20",c:.4},{i:"Dragon Dagger",c:.04},{i:"Obsidian Shard",c:.03},{i:"Infernal Cape Shard",c:.01}],
scorpion:[{i:"Coins x8",c:.5},{i:"Poison Stinger",c:.3},{i:"Antidote",c:.1}],
zombie:[{i:"Bones",c:1},{i:"Zombie Champion Scroll",c:.01},{i:"Rotten Food",c:.5},{i:"Iron Nails x8",c:.3}],
wolf:[{i:"Wolf Bones",c:.8},{i:"Wolf Fur",c:.6},{i:"Raw Meat",c:.7},{i:"Claws",c:.1}],
bear:[{i:"Bear Fur",c:.8},{i:"Raw Bear Meat",c:.7},{i:"Big Bones",c:.5},{i:"Bear Paw",c:.04}],
spider:[{i:"Spider Silk",c:.6},{i:"Coins x3",c:.5},{i:"Red Spider Eggs",c:.2},{i:"Spider Fang",c:.08}],
drake:[{i:"Drake Bones",c:.8},{i:"Dragon Scale",c:.15},{i:"Coins x80",c:.6},{i:"Drake Claw",c:.03},{i:"Wrath Rune x5",c:.1}],
ghost:[{i:"Ghost Essence",c:.5},{i:"Coins x20",c:.4},{i:"Death Rune",c:.2},{i:"Ectoplasm",c:.3},{i:"Ghost Robe Top",c:.04}],
shade:[{i:"Shade Robe",c:.1},{i:"Coins x40",c:.5},{i:"Death Rune x3",c:.15},{i:"Shadow Key",c:.02}],
troll:[{i:"Troll Bones",c:.8},{i:"Granite x3",c:.5},{i:"Coins x35",c:.6},{i:"Throwing Rock x10",c:.3},{i:"Granite Maul",c:.02}],
ogre:[{i:"Big Bones",c:.8},{i:"Coins x25",c:.6},{i:"Ogre Bow",c:.05},{i:"Raw Chompy",c:.3}],
knight:[{i:"Steel Platebody",c:.1},{i:"Coins x55",c:.7},{i:"Steel Sword",c:.15},{i:"Steel Shield",c:.08}],
mage:[{i:"Law Rune x3",c:.3},{i:"Coins x40",c:.6},{i:"Staff of Air",c:.06},{i:"Wizard Robe",c:.04},{i:"Mystic Gloves",c:.02}],
thief:[{i:"Coins x35",c:.8},{i:"Lockpick",c:.2},{i:"Diamond",c:.04},{i:"Thieving Cape Shard",c:.01}],
dwarf:[{i:"Coins x20",c:.7},{i:"Iron Ore",c:.5},{i:"Steel Pickaxe",c:.06},{i:"Dwarven Stout",c:.2},{i:"Gold Ore",c:.08}],
whiteknight:[{i:"Mithril Sword",c:.1},{i:"Coins x65",c:.7},{i:"White Shield",c:.05},{i:"Prayer Potion",c:.08}],
darkwiz:[{i:"Chaos Rune x5",c:.4},{i:"Coins x30",c:.6},{i:"Wizard Hat",c:.1},{i:"Mind Rune x15",c:.5},{i:"Mystic Robe Bottom",c:.03}],
revenant:[{i:"Revenant Ether x10",c:.6},{i:"Coins x150",c:.5},{i:"Ancient Statuette",c:.02},{i:"Craw Bow",c:.01},{i:"Amulet of Avarice",c:.005}],
hellhound:[{i:"Big Bones",c:.8},{i:"Coins x80",c:.5},{i:"Smouldering Stone",c:.02},{i:"Hellhound Fang",c:.05},{i:"Clue Scroll",c:.08}],
imp:[{i:"Coins x3",c:.5},{i:"Imp Bead",c:.8},{i:"Firelighter",c:.15}],
tzhaar:[{i:"Obsidian Shard",c:.4},{i:"Tokkul x50",c:.8},{i:"Obsidian Maul",c:.02},{i:"Obsidian Shield",c:.03},{i:"Fire Cape Shard",c:.01}],
elf:[{i:"Crystal Shard",c:.5},{i:"Coins x100",c:.6},{i:"Crystal Bow Seed",c:.02},{i:"Elven Signet",c:.01},{i:"Raw Tuna",c:.3}],
mummy:[{i:"Coins x50",c:.6},{i:"Pharaoh Sceptre Shard",c:.01},{i:"Gold Leaf",c:.1},{i:"Bandage",c:.4}],
scarab:[{i:"Coins x15",c:.5},{i:"Scarab Carapace",c:.3},{i:"Keris Shard",c:.02}],
tribesman:[{i:"Coins x10",c:.5},{i:"Poisoned Spear",c:.15},{i:"Tribal Mask",c:.03}],
fairy:[{i:"Fairy Dust",c:.6},{i:"Nature Rune x3",c:.4},{i:"Fairy Ring Piece",c:.02}],
mugger:[{i:"Coins x8",c:.8},{i:"Bronze Dagger",c:.3}],
rat:[{i:"Bones",c:.5},{i:"Rat Tail",c:.3}],
snake:[{i:"Snake Skin",c:.5},{i:"Coins x6",c:.4},{i:"Antipoison",c:.1}],
lizard:[{i:"Lizard Skin",c:.5},{i:"Coins x10",c:.4}],
elemental:[{i:"Elemental Ore",c:.4},{i:"Coins x70",c:.5},{i:"Elemental Shield Shard",c:.03}],
archer:[{i:"Steel Arrow x15",c:.6},{i:"Coins x30",c:.5},{i:"Maple Bow",c:.08}],
cultist:[{i:"Soul Rune x3",c:.3},{i:"Dark Totem Piece",c:.05},{i:"Coins x40",c:.5}],
gargoyle:[{i:"Granite Dust",c:.5},{i:"Coins x100",c:.6},{i:"Granite Maul",c:.03}],
bandit:[{i:"Coins x25",c:.8},{i:"Desert Amulet",c:.05}],
golem:[{i:"Runite Ore",c:.15},{i:"Coins x120",c:.5},{i:"Golem Heart",c:.02}],
wyrm:[{i:"Wyrm Bones",c:.8},{i:"Dragon Knife",c:.03},{i:"Coins x90",c:.5}]};

// log function defined above at line 326 using chat-log element

// === OSRS-INSPIRED WORLD REGIONS ===
const regions=[
// === ORIGINAL CORE (center) ===
{n:'Umbridgelay',x:0,z:0,r:280,lv:1,c:[.42,.52,.28],en:['goblin','cow','chicken'],fog:0x7a8a9a},
{n:'Arrockvay',x:550,z:50,r:220,lv:15,c:[.45,.40,.32],en:['guard','darkwiz'],fog:0x8a7a5a},
{n:'Ildernesway',x:0,z:-650,r:420,lv:50,c:[.18,.12,.10],en:['revenant','skeleton','demon'],fog:0x3a2820},
{n:'Alway Aridkhay',x:580,z:400,r:260,lv:10,c:[.68,.55,.30],en:['scorpion','warrior'],fog:0xb0a070},
{n:'Aladorfay',x:-480,z:280,r:240,lv:20,c:[.50,.50,.48],en:['whiteknight','dwarf'],fog:0x9a9a98},
{n:'Arbarianba Illagevay',x:280,z:-250,r:180,lv:8,c:[.38,.32,.20],en:['barbarian'],fog:0x7a6a4a},
{n:'Aynordray',x:-300,z:-150,r:200,lv:12,c:[.20,.28,.16],en:['vampire','zombie'],fog:0x3a4830},
{n:'Ortpay Arimsay',x:-160,z:480,r:220,lv:5,c:[.38,.46,.34],en:['pirate','mugger'],fog:0x8a9a8a},
{n:'Edgevillay',x:150,z:-350,r:150,lv:25,c:[.32,.28,.20],en:['skeleton','guard'],fog:0x6a5a40},
{n:'Atherbycay',x:-500,z:-400,r:180,lv:18,c:[.28,.42,.26],en:['zombie'],fog:0x506848},
// === EXPANDED REGIONS ===
{n:'Ardougneway',x:-1200,z:100,r:320,lv:25,c:[.40,.46,.34],en:['guard','knight','thief'],fog:0x8a9a7a},
{n:'Anilleyay',x:-1400,z:500,r:200,lv:30,c:[.36,.42,.30],en:['ogre','guard'],fog:0x7a8a6a},
{n:'Anifiscay',x:1300,z:-200,r:240,lv:35,c:[.15,.20,.12],en:['vampire','wolf','ghost'],fog:0x2a3820},
{n:'Orytaniamay',x:1600,z:-400,r:350,lv:40,c:[.12,.16,.10],en:['ghost','shade','vampire'],fog:0x1a2a18},
{n:'Aramjakay',x:-200,z:1800,r:400,lv:15,c:[.32,.52,.20],en:['spider','snake','tribesman'],fog:0x6a9a50},
{n:'Imhavenbray',x:-500,z:2200,r:280,lv:20,c:[.28,.46,.16],en:['spider','drake','snake'],fog:0x5a8a40},
{n:'Ollheimtray',x:-200,z:-3500,r:350,lv:55,c:[.30,.28,.24],en:['troll','wolf'],fog:0x5a5040},
{n:'Odgay Arsway',x:0,z:-4500,r:400,lv:80,c:[.18,.14,.22],en:['demon','golem','wyrm'],fog:0x2a2030},
{n:'Eepday Ildernesway',x:0,z:-1800,r:500,lv:65,c:[.12,.10,.08],en:['revenant','hellhound','demon'],fog:0x1a1510},
{n:'Eerssay Illagevay',x:-800,z:-100,r:220,lv:22,c:[.40,.48,.34],en:['guard','mage'],fog:0x8a9a7a},
{n:'Ellekkaray',x:-400,z:-3800,r:300,lv:45,c:[.32,.35,.38],en:['troll','barbarian','wolf'],fog:0x5a6068},
{n:'Eldagrimkay',x:-800,z:-3200,r:250,lv:50,c:[.36,.30,.26],en:['dwarf','golem'],fog:0x6a5848},
{n:'Osmay Elay Armlesshay',x:500,z:2500,r:300,lv:25,c:[.48,.52,.28],en:['pirate','snake','spider'],fog:0x9a9a60},
{n:'Esertday Ateauplay',x:2000,z:600,r:400,lv:35,c:[.70,.58,.30],en:['scorpion','mummy','warrior'],fog:0xc0a070},
{n:'Ophanemsay',x:2500,z:200,r:260,lv:40,c:[.65,.52,.26],en:['mummy','scarab','snake'],fog:0xb09060},
{n:'Enaphossmay',x:3000,z:400,r:300,lv:50,c:[.62,.50,.24],en:['mummy','warrior','mage'],fog:0xa88850},
{n:'Irannwntay',x:-3500,z:0,r:450,lv:55,c:[.20,.40,.15],en:['elf','wolf','bear'],fog:0x3a6a28},
{n:'Ifddinas pray',x:-4000,z:-300,r:300,lv:70,c:[.42,.52,.48],en:['elf','knight','mage'],fog:0x8aaa98},
{n:'Ossilfay Islandway',x:2500,z:-1500,r:300,lv:45,c:[.34,.40,.24],en:['wyrm','spider','lizard'],fog:0x6a7a50},
{n:'Eahzay Osidiushay',x:-2000,z:1200,r:350,lv:15,c:[.48,.52,.28],en:['lizard','chicken','cow'],fog:0x9a9a6a},
{n:'Eahzay Ayzien shay',x:-2500,z:800,r:300,lv:35,c:[.34,.30,.26],en:['knight','warrior','guard'],fog:0x6a5a48},
{n:'Eahzay Ovakengjlay',x:-2800,z:1600,r:280,lv:40,c:[.26,.22,.18],en:['dwarf','golem','bat'],fog:0x4a3a30},
{n:'Eahzay Arceuusway',x:-2200,z:1800,r:250,lv:50,c:[.20,.16,.28],en:['ghost','shade','cultist'],fog:0x2a2040},
{n:'Anarisza y',x:800,z:800,r:200,lv:30,c:[.25,.40,.44],en:['imp','fairy','spider'],fog:0x4a7a8a},
{n:'Aartzhay Itycay',x:1800,z:1200,r:250,lv:60,c:[.48,.16,.08],en:['tzhaar','imp','elemental'],fog:0x8a2010}
];
const eHP={goblin:32,cow:45,chicken:18,guard:80,darkwiz:65,revenant:120,skeleton:60,demon:160,scorpion:40,warrior:55,whiteknight:90,dwarf:70,barbarian:50,vampire:85,zombie:45,pirate:55,mugger:30,
troll:140,ogre:110,drake:180,bear:95,wolf:65,spider:50,bat:28,ghost:75,golem:200,wyrm:220,shade:90,hellhound:150,imp:35,bandit:70,rat:15,snake:40,lizard:45,elemental:160,gargoyle:190,knight:100,mage:85,archer:70,cultist:95,thief:40,tribesman:55,mummy:130,scarab:60,elf:120,fairy:30,tzhaar:250,
// NEW MONSTERS
dragon:400,blackdragon:550,hydra:480,kraken:420,cerberus:500,basilisk:180,cockatrice:120,wyvern:280,abyssal:200,dagannoth:160,kalphite:220,jad:650,zuk:900,nightmare:750,vorkath:800,zilyana:600,graardor:700,kreearra:550,kril:650,nex:1000,mimic:300,bloodveld:140,kurask:170,turoth:130,nechryael:200,abyssaldemon:240,darkbeast:260,skeletalwyvern:300,brutalblue:200,brutalred:350,brutalblack:450};
const eCol={goblin:0x2a5a28,cow:0x7a4a2a,chicken:0xcca855,guard:0x4444aa,darkwiz:0x2a0a3a,revenant:0x1a4a3a,skeleton:0xccccaa,demon:0x5a1010,scorpion:0x4a3a10,warrior:0x886830,whiteknight:0xcccccc,dwarf:0x886644,barbarian:0x8a5a30,vampire:0x2a0a1a,zombie:0x3a5a30,pirate:0x554430,mugger:0x3a3a3a,
troll:0x5a5a4a,ogre:0x4a6a30,drake:0x6a3020,bear:0x4a3020,wolf:0x555555,spider:0x2a2a20,bat:0x3a3040,ghost:0x6a8aaa,golem:0x5a5a60,wyrm:0x4a2040,shade:0x2a2a3a,hellhound:0x5a2010,imp:0x8a2020,bandit:0x4a4030,rat:0x5a4a3a,snake:0x2a4a20,lizard:0x4a6a30,elemental:0x2a4a6a,gargoyle:0x5a5a5a,knight:0x6a6a7a,mage:0x3a3a6a,archer:0x4a5a3a,cultist:0x3a1a3a,thief:0x3a3a3a,tribesman:0x5a4a2a,mummy:0x8a7a5a,scarab:0x2a3a1a,elf:0x4a6a5a,fairy:0x6a8aaa,tzhaar:0x8a3010,
dragon:0x2a6a1a,blackdragon:0x1a1a1a,hydra:0x4a6a3a,kraken:0x1a3a5a,cerberus:0x5a1a1a,basilisk:0x5a6a3a,cockatrice:0x6a7a2a,wyvern:0x3a4a5a,abyssal:0x2a0a2a,dagannoth:0x4a5a2a,kalphite:0x5a4a1a,jad:0x8a2a00,zuk:0xaa3a10,nightmare:0x2a1a3a,vorkath:0x2a5a6a,zilyana:0xaaaacc,graardor:0x5a4a3a,kreearra:0x3a5a3a,kril:0x5a1a2a,nex:0x4a0a3a,mimic:0x6a5a2a,bloodveld:0x6a2a2a,kurask:0x4a6a2a,turoth:0x3a5a2a,nechryael:0x4a2a4a,abyssaldemon:0x3a1a3a,darkbeast:0x1a1a2a,skeletalwyvern:0x8a8a7a,brutalblue:0x2a3a6a,brutalred:0x6a2a1a,brutalblack:0x1a1a1a};
// NEW MONSTER DROPS
drops.dragon=[{i:"Dragon Bones",c:1},{i:"Dragon Hide",c:.9},{i:"Coins x500",c:.8},{i:"Dragon Platelegs",c:.04},{i:"Dragon Med Helm",c:.06},{i:"Draconic Visage",c:.005},{i:"Dragon Spear",c:.02}];
drops.blackdragon=[{i:"Dragon Bones",c:1},{i:"Black Dragonhide",c:.9},{i:"Coins x800",c:.7},{i:"Dragon Platebody",c:.01},{i:"Draconic Visage",c:.01},{i:"Dragon Crossbow",c:.008}];
drops.hydra=[{i:"Hydra Bones",c:1},{i:"Hydra Leather",c:.3},{i:"Hydra Claw",c:.02},{i:"Coins x600",c:.7},{i:"Brimstone Ring Piece",c:.03}];
drops.kraken=[{i:"Kraken Tentacle",c:.08},{i:"Trident of the Seas",c:.02},{i:"Coins x400",c:.6},{i:"Raw Shark x5",c:.4},{i:"Mystic Water Staff",c:.05}];
drops.cerberus=[{i:"Primordial Crystal",c:.015},{i:"Pegasian Crystal",c:.015},{i:"Eternal Crystal",c:.015},{i:"Smouldering Stone",c:.02},{i:"Coins x700",c:.6},{i:"Hellhound Fang",c:.1}];
drops.basilisk=[{i:"Basilisk Jaw",c:.02},{i:"Coins x150",c:.5},{i:"Mystic Hat",c:.04}];
drops.wyvern=[{i:"Wyvern Bones",c:.8},{i:"Dragon Platelegs",c:.02},{i:"Battlestaff",c:.08},{i:"Coins x350",c:.6}];
drops.abyssal=[{i:"Abyssal Whip",c:.015},{i:"Coins x200",c:.5},{i:"Death Rune x8",c:.3}];
drops.kalphite=[{i:"Coins x100",c:.6},{i:"Potato Cactus",c:.3},{i:"Dragon Chain",c:.005}];
drops.jad=[{i:"Fire Cape",c:.5},{i:"Tokkul x200",c:.8},{i:"Obsidian Maul",c:.1},{i:"Coins x2000",c:.9}];
drops.zuk=[{i:"Infernal Cape",c:.4},{i:"Tokkul x500",c:.9},{i:"Coins x5000",c:1},{i:"TzKal Cape Shard",c:.1}];
drops.vorkath=[{i:"Vorkath Head",c:.05},{i:"Dragonbone Necklace",c:.03},{i:"Dragon Bolts x20",c:.3},{i:"Coins x3000",c:.8},{i:"Skeletal Visage",c:.005}];
drops.nightmare=[{i:"Nightmare Staff",c:.02},{i:"Inquisitor Mace",c:.01},{i:"Coins x4000",c:.7},{i:"Orb of Darkness",c:.008}];
drops.nex=[{i:"Torva Platebody",c:.008},{i:"Torva Platelegs",c:.008},{i:"Torva Helm",c:.008},{i:"Zaryte Crossbow",c:.005},{i:"Ancient Hilt",c:.005},{i:"Coins x8000",c:.9}];
function getReg(x,z){let b=regions[0],d=1e9;for(const r of regions){const dd=Math.hypot(x-r.x,z-r.z);if(dd<d){d=dd;b=r}}return b}
function biomeCol(x,z){const r=getReg(x,z),v=Math.sin(x*1.7+z*2.3)*.03;return[Math.max(0,Math.min(1,r.c[0]+v)),Math.max(0,Math.min(1,r.c[1]+v*.7)),Math.max(0,Math.min(1,r.c[2]+v*.5))]}

// Seeded RNG for consistent procedural terrain
function seededRand(x,z){let n=Math.sin(x*127.1+z*311.7)*43758.5453;return n-Math.floor(n)}
function noise2D(x,z){const ix=Math.floor(x),iz=Math.floor(z),fx=x-ix,fz=z-iz;const a=seededRand(ix,iz),b=seededRand(ix+1,iz),c=seededRand(ix,iz+1),d=seededRand(ix+1,iz+1);const ux=fx*fx*(3-2*fx),uz=fz*fz*(3-2*fz);return a+(b-a)*ux+(c-a)*uz+(a-b-c+d)*ux*uz}
function fbm(x,z,oct){let v=0,a=1,f=1,t=0;for(let i=0;i<oct;i++){v+=noise2D(x*f,z*f)*a;t+=a;a*=.5;f*=2}return v/t}

function terrainH(x,z){
// Base rolling terrain
let h=fbm(x*.0008,z*.0008,6)*60-15;
// Add medium detail
h+=Math.sin(x*.006)*Math.cos(z*.006)*18+Math.sin(x*.02+z*.015)*6;
// === MOUNTAIN RANGES ===
// Northern mountains (Trollheim/GWD) - towering peaks
if(z<-3000){const mf=Math.min(1,(-3000-z)/800);h+=mf*(80+fbm(x*.003,z*.003,5)*120+Math.abs(Math.sin(x*.015+z*.012))*40)}
// Fremennik mountains
if(x>-800&&x<200&&z<-3500){const mf=Math.min(1,(-3500-z)/500);h+=mf*(60+fbm(x*.004,z*.004,4)*80)}
// Western mountain spine (Tirannwn)
if(x<-3000){const mf=Math.min(1,(-3000-x)/1000);h+=mf*(40+fbm(x*.002,z*.002,5)*100+Math.sin(z*.008)*30)}
// Eastern highlands
if(x>3000){const mf=Math.min(1,(x-3000)/1500);h+=mf*(30+fbm(x*.003,z*.003,4)*70)}
// Far north arctic peaks
if(z<-6000){const mf=Math.min(1,(-6000-z)/2000);h+=mf*(100+fbm(x*.002,z*.002,6)*160)}
// === BIOME TERRAIN MODIFIERS ===
// Wilderness: rugged
if(z<-350&&z>-3000)h+=Math.sin(x*.08)*Math.cos(z*.06)*8+Math.abs(Math.sin(x*.15+z*.1))*5;
// Al Kharid desert: flat dunes
if(x>350&&z>200&&x<3000)h=h*.2+fbm(x*.005,z*.005,3)*15+4;
// Coastal south: flatten near water
const coastD=z-350;if(coastD>0&&coastD<600)h*=Math.max(0,1-coastD/400);
// Falador plains: gentle rolling
if(x<-200&&x>-1500&&z>-280&&z<500)h=h*.3+Math.sin(x*.02)*3;
// Deep Wilderness: volcanic
if(z<-2000&&z>-3000)h+=Math.sin(x*.04)*12+Math.abs(Math.sin(x*.1+z*.08))*15;
// Morytania swamp
if(x>1200&&x<2000&&z>-800&&z<200)h=h*.15-3+Math.sin(x*.04+z*.06)*2;
// Karamja jungle (south)
if(z>1500&&z<4000)h=fbm(x*.004,z*.004,4)*25+5;
// Tirannwn forest
if(x<-3000&&x>-5000)h=Math.max(h,15+fbm(x*.003,z*.003,4)*35);
return h}

// === LAKE GENERATION ===
const lakes=[
{x:-480,z:-420,r:40,d:8},{x:200,z:200,r:30,d:6},{x:-1250,z:50,r:35,d:7},
{x:800,z:900,r:50,d:10},{x:-3500,z:-100,r:60,d:12},{x:2500,z:-1500,r:45,d:9},
{x:-2000,z:1400,r:55,d:8},{x:1500,z:800,r:40,d:7},{x:-800,z:-3400,r:50,d:10},
{x:300,z:1800,r:35,d:6},{x:-1400,z:600,r:30,d:5},{x:2000,z:1000,r:45,d:8},
{x:-3000,z:-2000,r:70,d:15},{x:3500,z:-500,r:55,d:10},{x:-5000,z:500,r:80,d:14}
];
function isInLake(x,z){for(const l of lakes){const d=Math.hypot(x-l.x,z-l.z);if(d<l.r)return{...l,dist:d}}return null}

// === PLAYER MODEL BUILDER — class-based with equipment rendering ===
// Materials for class appearances
const mt_robe=new MS({color:0x2a1a4a,roughness:.8});const mt_robeHood=new MS({color:0x1a0a3a,roughness:.85});
const mt_robeGold=new MS({color:0xc4a240,roughness:.5,metalness:.4});
const mt_warLeather=new MS({color:0x5a3a1a,roughness:.85});const mt_warChain=new MS({color:0x7a7a7a,roughness:.5,metalness:.6});
const mt_skinBase=new MS({color:0xc4956a,roughness:.95});const mt_hairDk=new MS({color:0x2a1a0a,roughness:1});
const mt_cloth=new MS({color:0x6a5a4a,roughness:.9});

function buildBaseBody(body){
// Bare humanoid: head, torso, arms, legs (skin)
const head=new THREE.Mesh(new THREE.SphereGeometry(1.3,10,10),mt_skinBase);head.position.y=9.8;head.scale.set(1,1.15,.95);body.add(head);
// Eyes
const eyeMat=new MS({color:0x111111,roughness:1});
[-1,1].forEach(s=>{const eye=new THREE.Mesh(new THREE.SphereGeometry(.15,5,5),eyeMat);eye.position.set(s*.45,10,1.15);body.add(eye)});
// Neck
const neck=new THREE.Mesh(new THREE.CylinderGeometry(.5,.6,.8,8),mt_skinBase);neck.position.y=8.5;body.add(neck);
// Torso
const torso=new THREE.Mesh(new THREE.BoxGeometry(3.2,4,1.8),mt_skinBase);torso.position.y=5.8;body.add(torso);
// Arms (bare)
const buildArm=(side)=>{const arm=new THREE.Group();arm.position.set(side*2.4,7.8,0);
const ua=new THREE.Mesh(new THREE.CylinderGeometry(.4,.38,3,8),mt_skinBase);ua.position.y=-2.2;arm.add(ua);
const fa=new THREE.Mesh(new THREE.CylinderGeometry(.38,.32,2.8,8),mt_skinBase);fa.position.y=-5;arm.add(fa);
const hand=new THREE.Mesh(new THREE.BoxGeometry(.6,.4,.7),mt_skinBase);hand.position.y=-6.6;arm.add(hand);
return arm};
const lArm=buildArm(-1);body.add(lArm);
const rArm=buildArm(1);body.add(rArm);
// Legs (bare)
[-1,1].forEach(s=>{
const thigh=new THREE.Mesh(new THREE.CylinderGeometry(.5,.45,3,8),mt_skinBase);thigh.position.set(s*.8,2,0);body.add(thigh);
const shin=new THREE.Mesh(new THREE.CylinderGeometry(.42,.35,3,8),mt_skinBase);shin.position.set(s*.8,-.8,0);body.add(shin);
const foot=new THREE.Mesh(new THREE.BoxGeometry(.7,.5,1.3),mt_skinBase);foot.position.set(s*.8,-2.5,.15);body.add(foot);
});
return{lArm,rArm};
}

function addHelm_Knight(body){
const helmBase=new THREE.Mesh(new THREE.SphereGeometry(1.6,12,12),mt.armorDk);helmBase.position.y=9.8;helmBase.scale.set(1,1.25,.98);body.add(helmBase);
const faceplate=new THREE.Mesh(new THREE.BoxGeometry(2.2,1.8,.25),mt.armorLt);faceplate.position.set(0,9.5,1.45);body.add(faceplate);
const visorMat=new MS({color:0x040404,roughness:1});
for(let i=0;i<3;i++){const vs=new THREE.Mesh(new THREE.BoxGeometry(1.4+(.3-i*.15),.08,.3),visorMat);vs.position.set(0,9.8-i*.28,1.58);body.add(vs)}
const nasal=new THREE.Mesh(new THREE.BoxGeometry(.18,1.6,.3),mt.armorLt);nasal.position.set(0,9.5,1.58);body.add(nasal);
const crest=new THREE.Mesh(new THREE.BoxGeometry(.25,1,.8),mt.armorDk);crest.position.set(0,11.1,0);body.add(crest);
const aventail=new THREE.Mesh(new THREE.CylinderGeometry(1.7,1.9,1.4,10,1,true),mt.chainmail);aventail.position.y=8.5;body.add(aventail);
const plume=new THREE.Mesh(new THREE.BoxGeometry(.3,2.2,.5),mt.cape);plume.position.set(0,11.5,-.5);plume.rotation.x=.15;body.add(plume);
}
function addChest_Knight(body){
const gorget=new THREE.Mesh(new THREE.CylinderGeometry(1.1,1.3,1,10),mt.armorLt);gorget.position.y=8;body.add(gorget);
const torso=new THREE.Mesh(new THREE.BoxGeometry(3.6,4,2.2),mt.armorDk);torso.position.y=5.8;body.add(torso);
const ridge=new THREE.Mesh(new THREE.BoxGeometry(.3,3.4,.35),mt.armorLt);ridge.position.set(0,5.8,1.2);body.add(ridge);
[-1,1].forEach(s=>{const cp=new THREE.Mesh(new THREE.BoxGeometry(1.4,1.6,.3),mt.armorLt);cp.position.set(s*.7,6.8,1.2);body.add(cp)});
for(let i=0;i<6;i++){const rv=new THREE.Mesh(new THREE.SphereGeometry(.08,4,4),mt.gold);rv.position.set(-.6+i*.24,7.6,1.35);body.add(rv)}
const fauld=new THREE.Mesh(new THREE.BoxGeometry(3.8,1.2,2.3),mt.armorWorn);fauld.position.y=3.5;body.add(fauld);
const belt=new THREE.Mesh(new THREE.BoxGeometry(4,.6,2.4),mt.leather);belt.position.y=3.8;body.add(belt);
const buckle=new THREE.Mesh(new THREE.BoxGeometry(.7,.5,.3),mt.gold);buckle.position.set(0,3.8,1.25);body.add(buckle);
}
function addLegs_Knight(body){
[-1.2,-.4,.4,1.2].forEach(x=>{const tas=new THREE.Mesh(new THREE.BoxGeometry(.9,1.8,.2),mt.armorDk);tas.position.set(x,2.4,1.1);body.add(tas)});
const mailSkirt=new THREE.Mesh(new THREE.CylinderGeometry(1.6,2,2,10,1,true),mt.chainmail);mailSkirt.position.y=2.2;body.add(mailSkirt);
[-1,1].forEach(s=>{
const cuisse=new THREE.Mesh(new THREE.CylinderGeometry(.65,.58,3,8),mt.armorWorn);cuisse.position.set(s*.8,2,0);body.add(cuisse);
const knee=new THREE.Mesh(new THREE.SphereGeometry(.6,8,6),mt.armorDk);knee.position.set(s*.8,.5,0);body.add(knee);
const greave=new THREE.Mesh(new THREE.CylinderGeometry(.55,.48,2.8,8),mt.armorDk);greave.position.set(s*.8,-.8,0);body.add(greave);
const gPlate=new THREE.Mesh(new THREE.BoxGeometry(.5,2.4,.2),mt.armorLt);gPlate.position.set(s*.8,-.8,.45);body.add(gPlate);
});}
function addBoots_Knight(body){
[-1,1].forEach(s=>{
const boot=new THREE.Mesh(new THREE.BoxGeometry(1,.8,1.7),mt.armorDk);boot.position.set(s*.8,-2.3,.2);body.add(boot);
const toe=new THREE.Mesh(new THREE.BoxGeometry(.8,.3,.6),mt.armorLt);toe.position.set(s*.8,-2.5,.8);body.add(toe);
const sole=new THREE.Mesh(new THREE.BoxGeometry(1.05,.15,1.8),mt.leather);sole.position.set(s*.8,-2.7,.2);body.add(sole);
});}
function addShield(lArm){
const shield=new THREE.Mesh(new THREE.BoxGeometry(.35,4,2.8),mt.armorDk);shield.position.set(-.5,-4.5,.3);lArm.add(shield);
const shBordV=new THREE.Mesh(new THREE.BoxGeometry(.38,.3,2.9),mt.armorLt);shBordV.position.set(-.5,-2.6,.3);lArm.add(shBordV);
const shBordB=new THREE.Mesh(new THREE.BoxGeometry(.38,.3,2.9),mt.armorLt);shBordB.position.set(-.5,-6.4,.3);lArm.add(shBordB);
const sBoss=new THREE.Mesh(new THREE.SphereGeometry(.45,8,8),mt.gold);sBoss.position.set(-.7,-4.5,.3);lArm.add(sBoss);
}
function addSword(rArm){
const blade=new THREE.Mesh(new THREE.BoxGeometry(.2,.18,7.5),mt.swordBlade);blade.position.set(0,-7,3.8);blade.rotation.x=.06;rArm.add(blade);
const fuller=new THREE.Mesh(new THREE.BoxGeometry(.06,.1,5.5),new MS({color:0x556,roughness:.15,metalness:.9}));fuller.position.set(0,-6.9,3.8);fuller.rotation.x=.06;rArm.add(fuller);
const xguard=new THREE.Mesh(new THREE.BoxGeometry(1.6,.25,.25),mt.swordHilt);xguard.position.set(0,-7,.15);rArm.add(xguard);
[-1,1].forEach(s=>{const tip=new THREE.Mesh(new THREE.SphereGeometry(.12,5,5),mt.gold);tip.position.set(s*.8,-7,.15);rArm.add(tip)});
const hilt=new THREE.Mesh(new THREE.CylinderGeometry(.14,.14,1.4,6),mt.leather);hilt.position.set(0,-7,-.4);hilt.rotation.x=Math.PI/2;rArm.add(hilt);
const pommel=new THREE.Mesh(new THREE.SphereGeometry(.2,6,6),mt.gold);pommel.position.set(0,-7,-1.1);rArm.add(pommel);
}
function addStaff(rArm){
const shaft=new THREE.Mesh(new THREE.CylinderGeometry(.12,.1,10,6),mt.wd);shaft.position.set(0,-4,1.5);shaft.rotation.x=.1;rArm.add(shaft);
const orb=new THREE.Mesh(new THREE.SphereGeometry(.5,8,8),new MS({color:0x6644cc,emissive:0x4422aa,emissiveIntensity:.8,roughness:.3}));orb.position.set(0,-4,6.8);rArm.add(orb);
const orbRing=new THREE.Mesh(new THREE.TorusGeometry(.55,.06,6,12),mt.gold);orbRing.position.set(0,-4,6.8);rArm.add(orbRing);
}
function addPauldrons_Knight(lArm,rArm){
[lArm,rArm].forEach(arm=>{
const paul=new THREE.Mesh(new THREE.SphereGeometry(1.3,10,8),mt.armorLt);paul.scale.set(1.1,.8,.95);arm.add(paul);
const paulRim=new THREE.Mesh(new THREE.BoxGeometry(1.8,.2,1.6),mt.armorDk);paulRim.position.y=-.5;arm.add(paulRim);
const ua=new THREE.Mesh(new THREE.CylinderGeometry(.55,.5,3,8),mt.armorWorn);ua.position.y=-2.4;arm.add(ua);
const el=new THREE.Mesh(new THREE.SphereGeometry(.55,8,6),mt.armorDk);el.position.y=-4;arm.add(el);
const fa=new THREE.Mesh(new THREE.CylinderGeometry(.5,.44,2.8,8),mt.armorDk);fa.position.y=-5.5;arm.add(fa);
const gt=new THREE.Mesh(new THREE.BoxGeometry(.8,.5,1),mt.armorDk);gt.position.y=-7;arm.add(gt);
});}
function addGloves_Knight(lArm,rArm){
[lArm,rArm].forEach(arm=>{
const gt=new THREE.Mesh(new THREE.BoxGeometry(.85,.6,1.1),mt.armorDk);gt.position.y=-6.8;arm.add(gt);
const knk=new THREE.Mesh(new THREE.BoxGeometry(.85,.15,.5),mt.armorLt);knk.position.set(0,-6.5,.3);arm.add(knk);
});}
function addCape(body,mat){
mat=mat||mt.cape;
for(let i=0;i<5;i++){const cw=3-i*.25,ch=1.8+i*.2;const cMat=i>2?mt.capeTattered:mat;const seg=new THREE.Mesh(new THREE.PlaneGeometry(cw,ch,2,3),cMat);seg.position.set(0,6.5-i*1.7,-1.15-i*.12);body.add(seg)}
const clasp=new THREE.Mesh(new THREE.SphereGeometry(.15,5,5),mt.gold);clasp.position.set(0,7.5,-1.1);body.add(clasp);
}

function buildPlayerModel(cls){
const g=new THREE.Group();const body=new THREE.Group();
const{lArm,rArm}=buildBaseBody(body);
const eq=typeof equipped!=='undefined'?equipped:null;
const hasHelm=eq&&eq.Helm&&eq.Helm.name!=='None';
const hasChest=eq&&eq.Chest&&eq.Chest.name!=='None';
const hasLegs=eq&&eq.Legs&&eq.Legs.name!=='None';
const hasBoots=eq&&eq.Boots&&eq.Boots.name!=='None';
const hasGloves=eq&&eq.Gloves&&eq.Gloves.name!=='None';
const hasWeapon=eq&&eq.Weapon&&eq.Weapon.name!=='None';
const hasShield=eq&&eq.Shield&&eq.Shield.name!=='None';

if(cls==='knight'){
// Knight: full plate armor default + equipment overrides
if(hasHelm)addHelm_Knight(body);else{addHelm_Knight(body);}
if(hasChest)addChest_Knight(body);else{addChest_Knight(body);}
if(hasLegs)addLegs_Knight(body);else{addLegs_Knight(body);}
if(hasBoots)addBoots_Knight(body);else{addBoots_Knight(body);}
addPauldrons_Knight(lArm,rArm);
if(hasGloves)addGloves_Knight(lArm,rArm);else{addGloves_Knight(lArm,rArm);}
if(hasWeapon)addSword(rArm);else{addSword(rArm);}
if(hasShield)addShield(lArm);else{addShield(lArm);}
addCape(body);
}else if(cls==='warrior'){
// Warrior: chainmail torso, leather arms, medium armor, no closed helm
// Head: open face with hair
const hair=new THREE.Mesh(new THREE.SphereGeometry(1.4,8,8),mt_hairDk);hair.position.y=10.5;hair.scale.set(1,.6,1);body.add(hair);
// Chainmail chest
const chainTorso=new THREE.Mesh(new THREE.BoxGeometry(3.4,4,2),mt_warChain);chainTorso.position.y=5.8;body.add(chainTorso);
const belt=new THREE.Mesh(new THREE.BoxGeometry(3.6,.5,2.1),mt.leather);belt.position.y=3.9;body.add(belt);
const buckle=new THREE.Mesh(new THREE.BoxGeometry(.6,.4,.25),mt.gold);buckle.position.set(0,3.9,1.1);body.add(buckle);
if(hasHelm){// Warrior helm: open-face iron helm
const wHelm=new THREE.Mesh(new THREE.SphereGeometry(1.5,10,10),mt.armorWorn);wHelm.position.y=10.2;wHelm.scale.set(1,1.1,.9);body.add(wHelm);
const noseguard=new THREE.Mesh(new THREE.BoxGeometry(.15,1.5,.2),mt.armorLt);noseguard.position.set(0,9.8,1.3);body.add(noseguard);
}
// Leather shoulders
[lArm,rArm].forEach(arm=>{
const paul=new THREE.Mesh(new THREE.SphereGeometry(1,8,6),mt_warLeather);paul.scale.set(1,.7,.9);arm.add(paul);
const ua=new THREE.Mesh(new THREE.CylinderGeometry(.45,.42,3,8),mt_warLeather);ua.position.y=-2.2;arm.add(ua);
const fa=new THREE.Mesh(new THREE.CylinderGeometry(.42,.36,2.8,8),mt_warChain);fa.position.y=-5;arm.add(fa);
const glv=new THREE.Mesh(new THREE.BoxGeometry(.65,.45,.8),mt_warLeather);glv.position.y=-6.6;arm.add(glv);
});
// Warrior legs: leather + chain
if(hasLegs||true){[-1,1].forEach(s=>{
const cuisse=new THREE.Mesh(new THREE.CylinderGeometry(.55,.48,3,8),mt_warChain);cuisse.position.set(s*.8,2,0);body.add(cuisse);
const shin=new THREE.Mesh(new THREE.CylinderGeometry(.48,.4,2.8,8),mt_warLeather);shin.position.set(s*.8,-.8,0);body.add(shin);
});}
// Boots: leather
if(hasBoots||true){[-1,1].forEach(s=>{
const boot=new THREE.Mesh(new THREE.BoxGeometry(.9,.7,1.5),mt_warLeather);boot.position.set(s*.8,-2.3,.15);body.add(boot);
});}
if(hasWeapon)addSword(rArm);else{addSword(rArm);}
if(hasShield){addShield(lArm);}else{// Warrior default: round wooden shield
const rshield=new THREE.Mesh(new THREE.CylinderGeometry(2,2,.2,12),mt.wd);rshield.position.set(-.5,-4,.4);rshield.rotation.z=Math.PI/2;lArm.add(rshield);
const boss=new THREE.Mesh(new THREE.SphereGeometry(.4,8,8),mt.armorLt);boss.position.set(-.7,-4,.5);lArm.add(boss);
}
}else if(cls==='sorcerer'){
// Sorcerer: flowing robes, hood, staff
// Hood
const hood=new THREE.Mesh(new THREE.SphereGeometry(1.7,10,10),mt_robeHood);hood.position.y=10.2;hood.scale.set(1,1.2,.95);body.add(hood);
// Shadow under hood (face hidden)
const faceShadow=new THREE.Mesh(new THREE.SphereGeometry(1,8,8),new MS({color:0x0a0a0a,roughness:1}));faceShadow.position.set(0,9.6,1);faceShadow.scale.set(.6,.5,.3);body.add(faceShadow);
// Glowing eyes
const glowEye=new MS({color:0x6644ff,emissive:0x6644ff,emissiveIntensity:2});
[-1,1].forEach(s=>{const eye=new THREE.Mesh(new THREE.SphereGeometry(.12,5,5),glowEye);eye.position.set(s*.35,9.7,1.2);body.add(eye)});
// Robe torso (long flowing)
const robeTorso=new THREE.Mesh(new THREE.BoxGeometry(3.4,4.5,2),mt_robe);robeTorso.position.y=5.5;body.add(robeTorso);
// Gold trim on robe
const trim1=new THREE.Mesh(new THREE.BoxGeometry(3.5,.15,2.05),mt_robeGold);trim1.position.set(0,7.7,0);body.add(trim1);
const trim2=new THREE.Mesh(new THREE.BoxGeometry(.2,4.5,.15),mt_robeGold);trim2.position.set(0,5.5,1.05);body.add(trim2);
// Robe skirt (long, covers legs)
const robeSkirt=new THREE.Mesh(new THREE.CylinderGeometry(1.2,2.2,5,10),mt_robe);robeSkirt.position.y=0.5;body.add(robeSkirt);
const skirtTrim=new THREE.Mesh(new THREE.TorusGeometry(2.15,.06,6,16),mt_robeGold);skirtTrim.position.y=-2;skirtTrim.rotation.x=Math.PI/2;body.add(skirtTrim);
// Robe sleeves
[lArm,rArm].forEach(arm=>{
const sleeve=new THREE.Mesh(new THREE.CylinderGeometry(.6,.8,5,8),mt_robe);sleeve.position.y=-3.5;arm.add(sleeve);
const cuff=new THREE.Mesh(new THREE.TorusGeometry(.75,.06,6,10),mt_robeGold);cuff.position.y=-6;cuff.rotation.x=Math.PI/2;arm.add(cuff);
});
// Sash/belt
const sash=new THREE.Mesh(new THREE.BoxGeometry(3.6,.4,2.1),mt_robeGold);sash.position.y=3.5;body.add(sash);
// Staff instead of sword
addStaff(rArm);
// Magic book in left hand
const book=new THREE.Mesh(new THREE.BoxGeometry(.8,1,.5),new MS({color:0x3a1a0a,roughness:.8}));book.position.set(0,-6.5,.5);lArm.add(book);
const pages=new THREE.Mesh(new THREE.BoxGeometry(.75,.85,.1),new MS({color:0xeeddaa,roughness:.9}));pages.position.set(0,-6.5,.78);lArm.add(pages);
}else if(cls==='deprived'){
// Deprived: bare skin, loincloth only
// Hair (messy)
const hair=new THREE.Mesh(new THREE.SphereGeometry(1.35,8,8),mt_hairDk);hair.position.y=10.5;hair.scale.set(1.05,.5,1.05);body.add(hair);
// Loincloth
const loin=new THREE.Mesh(new THREE.BoxGeometry(2.5,1.2,1.8),mt_cloth);loin.position.y=3;body.add(loin);
// Simple wrap on arms
[lArm,rArm].forEach(arm=>{
const wrap=new THREE.Mesh(new THREE.CylinderGeometry(.35,.3,1.2,6),mt_cloth);wrap.position.y=-5.5;arm.add(wrap);
});
// Club (basic weapon)
if(hasWeapon){addSword(rArm);}else{
const club=new THREE.Mesh(new THREE.CylinderGeometry(.15,.25,5,6),mt.wd);club.position.set(0,-6,2.5);club.rotation.x=.1;rArm.add(club);
}
// Bare feet by default
// If gear is equipped, add it visually
if(hasHelm){const headband=new THREE.Mesh(new THREE.TorusGeometry(1.35,.1,6,12),mt_cloth);headband.position.y=10;headband.rotation.x=Math.PI/2;body.add(headband);}
if(hasChest){const vest=new THREE.Mesh(new THREE.BoxGeometry(3.3,3.5,1.9),mt_warLeather);vest.position.y=5.8;vest.material=vest.material.clone();vest.material.transparent=true;vest.material.opacity=.8;body.add(vest);}
if(hasShield){addShield(lArm);}
}
body.traverse(c=>{if(c.isMesh)c.castShadow=true});
g.add(body);g.userData.body=body;g.userData.lArm=lArm;g.userData.rArm=rArm;
g.scale.setScalar(.55);
return g;
}

// Keep buildKnight for multiplayer other-player models
function buildKnight(){return buildPlayerModel('knight')}

// Rebuild player model when equipment changes
function refreshPlayerModel(){
if(!scene||!playerGroup)return;
const pos=playerGroup.position.clone();const rot=playerGroup.rotation.y;
scene.remove(playerGroup);
playerGroup=buildPlayerModel(playerClass);
playerGroup.position.copy(pos);playerGroup.rotation.y=rot;
scene.add(playerGroup);
}

function init(){
console.log('INIT START');
scene=new THREE.Scene();scene.background=new THREE.Color(0xaaccee);scene.fog=new THREE.FogExp2(0xaaccee,.00008);
cam=new THREE.PerspectiveCamera(62,innerWidth/innerHeight,.5,30000);
renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'high-performance',stencil:false,depth:true});
renderer.setSize(innerWidth,innerHeight);renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=gameOpts?gameOpts.bright:2.0;
renderer.outputColorSpace=THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);

// Bright outdoor lighting
scene.add(new THREE.AmbientLight(0x8899aa,1.2));
const sun=new THREE.DirectionalLight(0xfff5e0,3.0);sun.position.set(200,350,-100);sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.near=1;sun.shadow.camera.far=1200;
sun.shadow.camera.left=-400;sun.shadow.camera.right=400;sun.shadow.camera.top=400;sun.shadow.camera.bottom=-400;
sun.shadow.bias=-.0002;sun.shadow.normalBias=.02;scene.add(sun);
// Sky fill light
const fill=new THREE.DirectionalLight(0xaaccee,.8);fill.position.set(-200,100,150);scene.add(fill);
// Warm rim light
const rim=new THREE.DirectionalLight(0xeebb88,.6);rim.position.set(-80,180,-250);scene.add(rim);
// Hemisphere: bright sky / warm ground
scene.add(new THREE.HemisphereLight(0xccddff,0x886644,.9));
// Sky dome (dramatic gradient)
const skyGeo=new THREE.SphereGeometry(5000,32,24);
const skyColors=new Float32Array(skyGeo.attributes.position.count*3);
for(let i=0;i<skyGeo.attributes.position.count;i++){const y=skyGeo.attributes.position.getY(i)/5000;
const t=Math.max(0,Math.min(1,(y+.2)/.7));
const r=.55+t*.3,g=.65+t*.25,b=.8+t*.15;
skyColors[i*3]=r;skyColors[i*3+1]=g;skyColors[i*3+2]=b}
skyGeo.setAttribute('color',new THREE.BufferAttribute(skyColors,3));
const skyMat=new MS({vertexColors:true,side:THREE.BackSide,fog:false,roughness:1,metalness:0});
const sky=new THREE.Mesh(skyGeo,skyMat);scene.add(sky);

// Extra materials for expanded world (Dark Souls palette)
mt.lava=new MS({color:0xdd2200,emissive:0xff3300,emissiveIntensity:3,roughness:1});
mt.sand=new MS({color:0xd4b878,roughness:.95});
mt.stW=new MS({map:texStone,color:0xccccbb,roughness:.68,metalness:.06});
mt.bridge=new MS({map:texWood,roughness:.88,color:0x6a5540});
mt.rope=new MS({color:0x8a7a50,roughness:1});
mt.shF=new MS({color:0x4a4a55,roughness:.28,metalness:.85});
mt.shT=new MS({color:0xd8b060,roughness:.32,metalness:.82});

// Biome-colored terrain (80000x80000) - massive world
mt.snow=new MS({color:0xeeeeff,roughness:.7,metalness:.05});
mt.lakeMat=new MS({color:0x2a7a9a,roughness:.05,metalness:.4,transparent:true,opacity:.75,side:THREE.DoubleSide,emissive:0x1a4a6a,emissiveIntensity:.15});
const gGeo=new THREE.PlaneGeometry(80000,80000,200,200);
const gp=gGeo.attributes.position;
const vc=new Float32Array(gp.count*3);
for(let i=0;i<gp.count;i++){const lx=gp.getX(i),lz=-gp.getY(i);
const h=terrainH(lx,lz);gp.setZ(i,h);
// Color: biome base + height-based (snow on peaks, rock on steep)
const bc=biomeCol(lx,lz);
if(h>120){const sf=Math.min(1,(h-120)/60);vc[i*3]=bc[0]*(1-sf)+.92*sf;vc[i*3+1]=bc[1]*(1-sf)+.92*sf;vc[i*3+2]=bc[2]*(1-sf)+.95*sf}
else if(h>80){const rf=Math.min(1,(h-80)/40);vc[i*3]=bc[0]*(1-rf)+.45*rf;vc[i*3+1]=bc[1]*(1-rf)+.42*rf;vc[i*3+2]=bc[2]*(1-rf)+.38*rf}
else{vc[i*3]=bc[0];vc[i*3+1]=bc[1];vc[i*3+2]=bc[2]}}
gGeo.setAttribute('color',new THREE.BufferAttribute(vc,3));
gGeo.computeVertexNormals();
const ground=new THREE.Mesh(gGeo,new MS({vertexColors:true,roughness:.88}));ground.rotation.x=-Math.PI/2;ground.receiveShadow=true;scene.add(ground);groundMesh=ground;
// === LAKES ===
lakes.forEach(l=>{const lGeo=new THREE.CircleGeometry(l.r,24);const lMesh=new THREE.Mesh(lGeo,mt.lakeMat);lMesh.rotation.x=-Math.PI/2;lMesh.position.set(l.x,meshTerrainH(l.x,l.z)+1,l.z);scene.add(lMesh)});

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
g.position.set(x,meshTerrainH(x,z),z);g.rotation.y=rot||0;scene.add(g)}
// === WORLD BUILDER HELPERS ===
function wall(x,z,w,h,rot){const bY=meshTerrainH(x,z);const g=new THREE.Group();
const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,3),mt.st);m.position.y=h/2;m.castShadow=true;g.add(m);addSolid(m);
// Crenellations
const cN=Math.max(2,Math.floor(w/4));for(let i=0;i<cN;i++){if(i%2===0){const cr=new THREE.Mesh(new THREE.BoxGeometry(w/cN*.8,2,3.2),mt.stD);cr.position.set(-w/2+w/cN*(i+.5),h+1,0);cr.castShadow=true;g.add(cr)}}
// Arrow slits
const slitN=Math.max(1,Math.floor(w/8));for(let i=0;i<slitN;i++){const sl=new THREE.Mesh(new THREE.BoxGeometry(.4,2,.2),new MS({color:0x0a0a0a,roughness:1}));sl.position.set(-w/2+w/(slitN+1)*(i+1),h*.6,1.6);g.add(sl)}
// Base molding
const base=new THREE.Mesh(new THREE.BoxGeometry(w+1,1,3.8),mt.stD);base.position.y=.5;g.add(base);
g.position.set(x,bY,z);g.rotation.y=rot||0;scene.add(g)}
function wallW(x,z,w,h,rot){const bY=meshTerrainH(x,z);const g=new THREE.Group();
const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,3),mt.stW);m.position.y=h/2;m.castShadow=true;g.add(m);addSolid(m);
const cN=Math.max(2,Math.floor(w/4));for(let i=0;i<cN;i++){if(i%2===0){const cr=new THREE.Mesh(new THREE.BoxGeometry(w/cN*.8,2,3.2),mt.stW);cr.position.set(-w/2+w/cN*(i+.5),h+1,0);cr.castShadow=true;g.add(cr)}}
const slitN=Math.max(1,Math.floor(w/8));for(let i=0;i<slitN;i++){const sl=new THREE.Mesh(new THREE.BoxGeometry(.4,2,.2),new MS({color:0x0a0a0a,roughness:1}));sl.position.set(-w/2+w/(slitN+1)*(i+1),h*.6,1.6);g.add(sl)}
const base=new THREE.Mesh(new THREE.BoxGeometry(w+1,1,3.8),mt.stD);base.position.y=.5;g.add(base);
g.position.set(x,bY,z);g.rotation.y=rot||0;scene.add(g)}
function hut(x,z,rot,s){s=s||1;const h=meshTerrainH(x,z);const g=new THREE.Group();
const wW=12*s,wD=10*s,wH=8*s,wallT=.6*s;const doorW=3*s,doorH2=5.5*s;
const doorMat=new MS({color:0x3a2818,roughness:.85,metalness:.05});
const intFloorMat=new MS({color:0x5a4a38,roughness:.92});
const winGlassMat=new MS({color:0x2a4a6a,roughness:.15,metalness:.3,emissive:0x1a3a5a,emissiveIntensity:.5,transparent:true,opacity:.5});
// Foundation
const found=new THREE.Mesh(new THREE.BoxGeometry(wW+2*s,1.5*s,wD+2*s),mt.st);found.position.y=.75*s;found.castShadow=true;g.add(found);addSolid(found);
// Interior floor
const intFloor=new THREE.Mesh(new THREE.BoxGeometry(wW-.5*s,.2*s,wD-.5*s),intFloorMat);intFloor.position.y=1.6*s;intFloor.receiveShadow=true;g.add(intFloor);
// Back wall (solid)
const backW=new THREE.Mesh(new THREE.BoxGeometry(wW,wH,wallT),mt.wd);backW.position.set(0,wH/2+1.5*s,-wD/2);backW.castShadow=true;g.add(backW);addSolid(backW);
// Left wall (solid)
const leftW=new THREE.Mesh(new THREE.BoxGeometry(wallT,wH,wD),mt.wd);leftW.position.set(-wW/2,wH/2+1.5*s,0);leftW.castShadow=true;g.add(leftW);addSolid(leftW);
// Right wall (solid)
const rightW=leftW.clone();rightW.position.x=wW/2;g.add(rightW);addSolid(rightW);
// Front wall — two sections flanking doorway
const fwSideW=(wW-doorW)/2;
const fwL=new THREE.Mesh(new THREE.BoxGeometry(fwSideW,wH,wallT),mt.wd);fwL.position.set(-(doorW+fwSideW)/2,wH/2+1.5*s,wD/2);fwL.castShadow=true;g.add(fwL);addSolid(fwL);
const fwR=fwL.clone();fwR.position.x=(doorW+fwSideW)/2;g.add(fwR);addSolid(fwR);
// Lintel above door
const lintel=new THREE.Mesh(new THREE.BoxGeometry(doorW+1*s,1.2*s,wallT+.2*s),mt.stD);lintel.position.set(0,doorH2+1.5*s+.6*s,wD/2);lintel.castShadow=true;g.add(lintel);
// Top section above door
const topH=wH-doorH2-1.2*s;if(topH>0){const topW=new THREE.Mesh(new THREE.BoxGeometry(doorW,topH,wallT),mt.wd);topW.position.set(0,doorH2+1.5*s+1.2*s+topH/2,wD/2);g.add(topW)}
// Door — pivots on left edge
const doorPivot=new THREE.Group();doorPivot.position.set(-doorW/2,1.5*s,wD/2);
const doorPanel=new THREE.Mesh(new THREE.BoxGeometry(doorW,doorH2,.25*s),doorMat);doorPanel.position.set(doorW/2,doorH2/2,0);doorPanel.castShadow=true;doorPivot.add(doorPanel);
// Door handle
const doorHandle=new THREE.Mesh(new THREE.SphereGeometry(.2*s,5,5),mt.gold);doorHandle.position.set(doorW*.8,doorH2*.45,.2*s);doorPivot.add(doorHandle);
// Iron banding on door
for(let i=0;i<3;i++){const band=new THREE.Mesh(new THREE.BoxGeometry(doorW-.2*s,.15*s,.3*s),mt.armorDk);band.position.set(doorW/2,doorH2*.2+i*doorH2*.3,0);doorPivot.add(band)}
g.add(doorPivot);
// Track door for animation — compute world position of pivot
const doorWorldX=x+Math.cos(rot||0)*(-(doorW/2))+Math.sin(rot||0)*(wD/2);
const doorWorldZ=z-Math.sin(rot||0)*(-(doorW/2))+Math.cos(rot||0)*(wD/2);
doors.push({pivot:doorPivot,x:doorWorldX,z:doorWorldZ,openAng:-Math.PI/2,cur:0});
// Roof with overhang
const roof=new THREE.Mesh(new THREE.ConeGeometry(9.5*s,6*s,4),mt.rf);roof.position.y=wH+4*s;roof.rotation.y=.785;roof.castShadow=true;g.add(roof);
const ridge=new THREE.Mesh(new THREE.BoxGeometry(13*s,.3*s,.3*s),mt.stD);ridge.position.y=wH+7*s;ridge.rotation.y=.785;g.add(ridge);
// Windows (both sides) with glass + shutters
[-1,1].forEach(sd=>{const winH=2*s,winW=1.5*s;
const glass=new THREE.Mesh(new THREE.BoxGeometry(.1*s,winH,winW),winGlassMat);glass.position.set((wW/2+.05)*sd,5*s,0);g.add(glass);
const frame=new THREE.Mesh(new THREE.BoxGeometry(.3*s,winH+.4*s,winW+.4*s),mt.wd);frame.position.set((wW/2+.15)*sd,5*s,0);g.add(frame);
const sill=new THREE.Mesh(new THREE.BoxGeometry(.5*s,.15*s,winW+.6*s),mt.st);sill.position.set((wW/2+.2)*sd,3.9*s,0);g.add(sill);
// Shutters that frame the window
const sh1=new THREE.Mesh(new THREE.BoxGeometry(.12*s,winH+.2*s,.6*s),mt.wd);sh1.position.set((wW/2+.2)*sd,5*s,winW/2+.35*s);g.add(sh1);
const sh2=sh1.clone();sh2.position.z=-(winW/2+.35*s);g.add(sh2)});
// Chimney
const chim=new THREE.Mesh(new THREE.BoxGeometry(2*s,4*s,2*s),mt.st);chim.position.set(-4*s,wH+5*s,-3*s);chim.castShadow=true;g.add(chim);
const chimTop=new THREE.Mesh(new THREE.BoxGeometry(2.4*s,.4*s,2.4*s),mt.stD);chimTop.position.set(-4*s,wH+7.2*s,-3*s);g.add(chimTop);
// Corner posts
[[-1,-1],[-1,1],[1,-1],[1,1]].forEach(([cx,cz])=>{const p=new THREE.Mesh(new THREE.CylinderGeometry(.3*s,.4*s,wH+.5*s,5),mt.wd);p.position.set(cx*(wW/2-.2*s),wH/2+1.5*s,cz*(wD/2-.2*s));p.castShadow=true;g.add(p)});
// Steps leading to door
for(let i=0;i<3;i++){const step=new THREE.Mesh(new THREE.BoxGeometry(doorW+1*s,.4*s,1.2*s),mt.st);step.position.set(0,.2+i*.4*s,wD/2+.6*s+i*1.2*s);step.receiveShadow=true;g.add(step)}
// Interior detail: table + chair
const tbl=new THREE.Mesh(new THREE.BoxGeometry(3*s,.15*s,2*s),mt.wd);tbl.position.set(0,3.5*s,-2*s);g.add(tbl);
const tblLeg1=new THREE.Mesh(new THREE.CylinderGeometry(.1*s,.1*s,2*s,4),mt.wd);
[[-1,-1],[-1,1],[1,-1],[1,1]].forEach(([lx,lz])=>{const lg=tblLeg1.clone();lg.position.set(lx*1.3*s,2.4*s,-2*s+lz*.8*s);g.add(lg)});
g.position.set(x,h,z);g.rotation.y=rot||0;scene.add(g)}
function tower(x,z,s,mat){s=s||1;mat=mat||mt.st;const h=meshTerrainH(x,z);const g=new THREE.Group();
// Base (wider)
const base=new THREE.Mesh(new THREE.CylinderGeometry(7.5*s,8.5*s,4*s,10),mat);base.position.y=2*s;base.castShadow=true;g.add(base);addSolid(base);
// Main body
const b=new THREE.Mesh(new THREE.CylinderGeometry(6*s,7*s,30*s,10),mat);b.position.y=17*s;b.castShadow=true;g.add(b);addSolid(b);
// Battlement ring
for(let i=0;i<10;i++){const a=i/10*Math.PI*2;const cr=new THREE.Mesh(new THREE.BoxGeometry(2.5*s,2*s,1.5*s),mt.stD);cr.position.set(Math.cos(a)*6.5*s,33*s,Math.sin(a)*6.5*s);cr.rotation.y=a;cr.castShadow=true;g.add(cr)}
// Conical roof
const roof=new THREE.Mesh(new THREE.ConeGeometry(8*s,10*s,10),mt.rfSlate);roof.position.y=38*s;roof.castShadow=true;g.add(roof);
// Roof finial
const fin=new THREE.Mesh(new THREE.SphereGeometry(.6*s,5,5),mt.gold);fin.position.y=43.5*s;g.add(fin);
// Windows (arrow slits on 4 sides, 3 levels)
for(let lv=0;lv<3;lv++){for(let i=0;i<4;i++){const a=i/4*Math.PI*2;
const slit=new THREE.Mesh(new THREE.BoxGeometry(.4*s,2*s,.15*s),new MS({color:0x101010,roughness:1}));
slit.position.set(Math.cos(a)*6.5*s,8*s+lv*8*s,Math.sin(a)*6.5*s);slit.rotation.y=a;g.add(slit)}}
// Balcony
const balcRing=new THREE.Mesh(new THREE.TorusGeometry(7.5*s,.3*s,5,12),mat);balcRing.position.y=26*s;balcRing.rotation.x=Math.PI/2;g.add(balcRing);
const balcFloor=new THREE.Mesh(new THREE.CylinderGeometry(7.5*s,7.5*s,.3*s,12),mat);balcFloor.position.y=25.8*s;g.add(balcFloor);
// Door — pivoting, opens on approach
{const tDoorW=3*s,tDoorH=6*s,tR=7.2*s;
const tDoorPivot=new THREE.Group();tDoorPivot.position.set(-tDoorW/2,0,tR);
const tDoorPanel=new THREE.Mesh(new THREE.BoxGeometry(tDoorW,tDoorH,.3*s),new MS({color:0x3a2818,roughness:.85,metalness:.05}));tDoorPanel.position.set(tDoorW/2,tDoorH/2,0);tDoorPanel.castShadow=true;tDoorPivot.add(tDoorPanel);
const tDH=new THREE.Mesh(new THREE.SphereGeometry(.2*s,5,5),mt.gold);tDH.position.set(tDoorW*.8,tDoorH*.4,.2*s);tDoorPivot.add(tDH);
for(let bi=0;bi<2;bi++){const bb=new THREE.Mesh(new THREE.BoxGeometry(tDoorW-.3*s,.2*s,.35*s),mt.armorDk);bb.position.set(tDoorW/2,tDoorH*.25+bi*tDoorH*.35,0);tDoorPivot.add(bb)}
g.add(tDoorPivot);
const tdWX=x+Math.sin(0)*tR,tdWZ=z+Math.cos(0)*tR;
doors.push({pivot:tDoorPivot,x:tdWX,z:tdWZ,openAng:-Math.PI/2,cur:0})}
// Torch
const fm=new THREE.Mesh(new THREE.SphereGeometry(1.5,6,6),mt.fl);fm.position.y=30*s;g.add(fm);
g.position.set(x,h,z);scene.add(g);
torchPositions.push({x,y:h+30*s,z,mesh:fm,ph:Math.random()*6.28,big:false})}
function pine(x,z){const h=meshTerrainH(x,z);const g=new THREE.Group();
// Roots (exposed)
for(let i=0;i<4;i++){const a=i/4*Math.PI*2;const root=new THREE.Mesh(new THREE.CylinderGeometry(.15,.4,3,4),mt.bk);root.position.set(Math.cos(a)*1.5,.5,Math.sin(a)*1.5);root.rotation.z=Math.cos(a)*.5;root.rotation.x=Math.sin(a)*.5;root.castShadow=true;g.add(root)}
// Trunk (tapered, knotty)
const tr=new THREE.Mesh(new THREE.CylinderGeometry(.8,2,16,8),mt.bk);tr.position.y=8;tr.castShadow=true;g.add(tr);
// Bark knots
for(let i=0;i<5;i++){const kn=new THREE.Mesh(new THREE.SphereGeometry(.3+Math.random()*.3,5,5),mt.bk);kn.position.set((Math.random()-.5)*1.5,3+Math.random()*10,(Math.random()-.5)*1.5);g.add(kn)}
// Branches with foliage layers (7 layers, decreasing size)
for(let i=0;i<7;i++){const cn=new THREE.Mesh(new THREE.ConeGeometry(7.5-i*1,5,10),i%2?mt.lfL:mt.lf);cn.position.y=12+i*3;cn.castShadow=true;g.add(cn);
// Sub-branches
if(i<5){for(let j=0;j<3;j++){const a=j/3*Math.PI*2+i*.5;const br=new THREE.Mesh(new THREE.CylinderGeometry(.08,.15,2.5,4),mt.bk);br.position.set(Math.cos(a)*(3-i*.3),11+i*3,Math.sin(a)*(3-i*.3));br.rotation.z=Math.cos(a)*.6;br.rotation.x=Math.sin(a)*.6;g.add(br)}}}
g.position.set(x,h,z);scene.add(g)}
function palm(x,z){const h=meshTerrainH(x,z);const g=new THREE.Group();
// Trunk (curved, segmented)
const tr=new THREE.Mesh(new THREE.CylinderGeometry(.5,.9,18,8),mt.bk);tr.position.y=9;tr.rotation.z=Math.sin(x)*.12;tr.castShadow=true;g.add(tr);
// Trunk rings
for(let i=0;i<8;i++){const ring=new THREE.Mesh(new THREE.TorusGeometry(.65,.08,4,8),mt.bk);ring.position.y=2+i*2;ring.rotation.x=Math.PI/2;g.add(ring)}
// Coconuts
for(let i=0;i<3;i++){const cn=new THREE.Mesh(new THREE.SphereGeometry(.4,6,6),new MS({color:0x5a4030,roughness:.9}));cn.position.set(Math.cos(i*2)*.8,17.5,Math.sin(i*2)*.8);g.add(cn)}
// Fronds (larger, more detailed)
for(let i=0;i<8;i++){const a=i/8*Math.PI*2;const f=new THREE.Mesh(new THREE.PlaneGeometry(9,2.5),mt.lf);f.position.set(Math.cos(a)*3,18,Math.sin(a)*3);f.rotation.set(-1.1,a,0);g.add(f);
const f2=new THREE.Mesh(new THREE.PlaneGeometry(6,1.5),mt.lfL);f2.position.set(Math.cos(a)*2.5,18.5,Math.sin(a)*2.5);f2.rotation.set(-.8,a+.2,0);g.add(f2)}
g.position.set(x,h,z);scene.add(g)}
const dtMat=new MS({color:0x3a2a1a,roughness:.95}),dtMat2=new MS({color:0x4a3a22,roughness:.95});
function deadTree(x,z){const h=meshTerrainH(x,z);const g=new THREE.Group();
// Gnarled trunk
const tr=new THREE.Mesh(new THREE.CylinderGeometry(.4,1.5,14,6),dtMat);tr.position.y=7;tr.rotation.z=Math.random()*.15-.075;tr.castShadow=true;g.add(tr);
// Exposed roots
for(let i=0;i<5;i++){const a=i/5*Math.PI*2;const root=new THREE.Mesh(new THREE.CylinderGeometry(.1,.3,2.5,4),dtMat2);root.position.set(Math.cos(a)*1.3,.5,Math.sin(a)*1.3);root.rotation.z=Math.cos(a)*.6;root.rotation.x=Math.sin(a)*.6;g.add(root)}
// Main branches (thicker, more)
for(let i=0;i<6;i++){const br=new THREE.Mesh(new THREE.CylinderGeometry(.1,.3,4+Math.random()*3,4),dtMat2);br.position.set((Math.random()-.5)*1.5,8+Math.random()*5,(Math.random()-.5)*1.5);br.rotation.set(Math.random()-.3,Math.random(),.4+Math.random()*.6);br.castShadow=true;g.add(br);
// Twig sub-branches
for(let j=0;j<2;j++){const tw=new THREE.Mesh(new THREE.CylinderGeometry(.03,.08,1.5+Math.random(),3),dtMat);tw.position.copy(br.position);tw.position.y+=1.5;tw.rotation.set(Math.random(),Math.random(),Math.random());g.add(tw)}}
// Bark peeling
for(let i=0;i<4;i++){const peel=new THREE.Mesh(new THREE.PlaneGeometry(.5,1.5),new MS({color:0x5a4a30,roughness:1,side:THREE.DoubleSide}));peel.position.set((Math.random()-.5)*1.2,4+Math.random()*6,(Math.random()-.5)*1.2);peel.rotation.set(Math.random(),Math.random(),Math.random());g.add(peel)}
g.position.set(x,h,z);scene.add(g)}
function bonfire(x,z){const h=meshTerrainH(x,z);const g=new THREE.Group();
// Stone ring
for(let i=0;i<14;i++){const a=i/14*Math.PI*2,r=4.5+Math.random()*.5;const rk=new THREE.Mesh(new THREE.IcosahedronGeometry(.8+Math.random()*.6,0),mt.rk);rk.position.set(Math.cos(a)*r,.4,Math.sin(a)*r);rk.castShadow=true;g.add(rk)}
// Coal bed
const coal=new THREE.Mesh(new THREE.CylinderGeometry(3,3.5,.5,10),new MS({color:0x1a1010,roughness:1}));coal.position.y=.3;g.add(coal);
// Glowing embers in coal
for(let i=0;i<8;i++){const em=new THREE.Mesh(new THREE.SphereGeometry(.2+Math.random()*.3,5,5),new MS({color:0xff4400,emissive:0xff2200,emissiveIntensity:3,roughness:1}));em.position.set((Math.random()-.5)*4,.5,(Math.random()-.5)*4);g.add(em)}
// Log structure (teepee style)
for(let i=0;i<5;i++){const a=i/5*Math.PI*2;const log=new THREE.Mesh(new THREE.CylinderGeometry(.2,.35,6,5),mt.wd);log.position.set(Math.cos(a)*1.5,2.5,Math.sin(a)*1.5);log.rotation.z=Math.cos(a)*.3;log.rotation.x=Math.sin(a)*.3;log.castShadow=true;g.add(log)}
// Main flame
const fm=new THREE.Mesh(new THREE.SphereGeometry(2.5,8,8),mt.fl);fm.position.y=3.5;g.add(fm);
// Inner flame (brighter)
const fmI=new THREE.Mesh(new THREE.SphereGeometry(1.2,6,6),new MS({color:0xffaa22,emissive:0xffcc44,emissiveIntensity:5,roughness:1}));fmI.position.y=4;g.add(fmI);
// Iron pot (optional deco)
const pot=new THREE.Mesh(new THREE.SphereGeometry(1.2,8,6,0,Math.PI*2,0,Math.PI/2),new MS({color:0x2a2a2a,roughness:.6,metalness:.7}));pot.position.set(3.5,1,0);pot.rotation.x=Math.PI;g.add(pot);
g.position.set(x,h,z);scene.add(g);
torchPositions.push({x,y:h+5,z,mesh:fm,ph:0,big:true})}
function bridge(x,z,rot,len){const h=meshTerrainH(x,z);const g=new THREE.Group();
// Main planks (individual)
const planks=Math.floor(len/2);for(let i=0;i<planks;i++){const pl=new THREE.Mesh(new THREE.BoxGeometry(5.5,.3,1.8),mt.bridge);pl.position.set(0,2,(i-planks/2)*2);pl.castShadow=true;pl.receiveShadow=true;g.add(pl)}
// Support beams underneath
const bridgeDeck=new THREE.Mesh(new THREE.BoxGeometry(5.5,.4,len),mt.bridge);bridgeDeck.position.set(0,2.1,0);bridgeDeck.receiveShadow=true;g.add(bridgeDeck);addSolid(bridgeDeck);
[-2.2,2.2].forEach(sx=>{const beam=new THREE.Mesh(new THREE.BoxGeometry(.6,.6,len),mt.wd);beam.position.set(sx,1.5,0);beam.castShadow=true;g.add(beam)});
// Rope railings
[-1,1].forEach(sd=>{
const rope=new THREE.Mesh(new THREE.CylinderGeometry(.08,.08,len,6),mt.rope);rope.position.set(sd*3,5,0);rope.rotation.x=Math.PI/2;g.add(rope);
const ropeL=new THREE.Mesh(new THREE.CylinderGeometry(.06,.06,len,6),mt.rope);ropeL.position.set(sd*3,3.5,0);ropeL.rotation.x=Math.PI/2;g.add(ropeL)});
// Vertical posts
const posts=Math.floor(len/5);for(let i=0;i<posts;i++){const t=(i/(posts-.1)-.5)*len;
[-1,1].forEach(sd=>{const p=new THREE.Mesh(new THREE.CylinderGeometry(.15,.2,6,4),mt.wd);p.position.set(sd*3,5,t);p.castShadow=true;g.add(p);
// Cross braces
const brace=new THREE.Mesh(new THREE.CylinderGeometry(.06,.06,2,3),mt.wd);brace.position.set(sd*2.5,3,t);brace.rotation.z=sd*.5;g.add(brace)})}
// Stone anchors at ends
[-1,1].forEach(end=>{const anc=new THREE.Mesh(new THREE.BoxGeometry(6,3,3),mt.st);anc.position.set(0,1.5,end*len/2);anc.castShadow=true;g.add(anc)});
g.position.set(x,h,z);g.rotation.y=rot;scene.add(g)}
function ruin(x,z){const h=meshTerrainH(x,z);const g=new THREE.Group();
// Standing wall fragments
for(let i=0;i<3;i++){const w=new THREE.Mesh(new THREE.BoxGeometry(3+Math.random()*5,8+Math.random()*16,2.5),mt.stD);w.position.set((Math.random()-.5)*18,5+Math.random()*4,(Math.random()-.5)*18);w.rotation.set(Math.random()*.15,Math.random(),Math.random()*.15);w.castShadow=true;g.add(w);addSolid(w)}
// Fallen columns
for(let i=0;i<2;i++){const col=new THREE.Mesh(new THREE.CylinderGeometry(.6,.8,8+Math.random()*4,6),mt.st);col.position.set((Math.random()-.5)*16,1,(Math.random()-.5)*16);col.rotation.z=Math.PI/2+Math.random()*.3;col.castShadow=true;g.add(col)}
// Rubble pile
for(let i=0;i<12;i++){const rb=new THREE.Mesh(new THREE.IcosahedronGeometry(.5+Math.random()*2,0),Math.random()>.5?mt.rk:mt.stD);rb.position.set((Math.random()-.5)*18,Math.random()*2,(Math.random()-.5)*18);rb.rotation.set(Math.random(),Math.random(),Math.random());rb.castShadow=true;g.add(rb)}
// Broken arch
const archL=new THREE.Mesh(new THREE.BoxGeometry(2.5,12,2.5),mt.st);archL.position.set(-5,6,0);archL.castShadow=true;g.add(archL);
const archR=new THREE.Mesh(new THREE.BoxGeometry(2.5,8,2.5),mt.st);archR.position.set(5,4,0);archR.rotation.z=.1;archR.castShadow=true;g.add(archR);
// Overgrown moss patches
for(let i=0;i<6;i++){const moss=new THREE.Mesh(new THREE.PlaneGeometry(1.5+Math.random()*2,1+Math.random()*1.5),new MS({color:0x2a4a1a,roughness:1,side:THREE.DoubleSide,transparent:true,opacity:.6}));moss.position.set((Math.random()-.5)*14,1+Math.random()*6,(Math.random()-.5)*14);moss.rotation.set(Math.random(),Math.random(),Math.random());g.add(moss)}
g.position.set(x,h,z);scene.add(g)}
function torch(tx,tz){const th=meshTerrainH(tx,tz);const g=new THREE.Group();
// Post
const post=new THREE.Mesh(new THREE.CylinderGeometry(.3,.5,10,6),mt.wd);post.position.y=5;post.castShadow=true;g.add(post);
// Iron bracket
const bracket=new THREE.Mesh(new THREE.BoxGeometry(.8,.15,.8),new MS({color:0x3a3a3a,roughness:.5,metalness:.7}));bracket.position.y=10.2;g.add(bracket);
const hook=new THREE.Mesh(new THREE.TorusGeometry(.3,.06,4,6,Math.PI),new MS({color:0x3a3a3a,roughness:.5,metalness:.7}));hook.position.set(0,10.5,.3);g.add(hook);
// Oil cup
const cup=new THREE.Mesh(new THREE.CylinderGeometry(.3,.2,.5,6),new MS({color:0x2a2a2a,roughness:.6,metalness:.6}));cup.position.y=10.5;g.add(cup);
// Flame (teardrop shape)
const fm=new THREE.Mesh(new THREE.SphereGeometry(1,6,6),mt.fl);fm.position.y=11.5;fm.scale.set(.8,1.2,.8);g.add(fm);
const fmTip=new THREE.Mesh(new THREE.ConeGeometry(.4,1,5),new MS({color:0xffaa22,emissive:0xff8800,emissiveIntensity:4,roughness:1}));fmTip.position.y=12.5;g.add(fmTip);
g.position.set(tx,th,tz);scene.add(g);
torchPositions.push({x:tx,y:th+11,z:tz,mesh:fm,ph:Math.random()*6.28,big:false})}

// === GOTHIC ARCHITECTURE BUILDERS ===
function gothicSpire(x,z,h,sc){sc=sc||1;const bY=meshTerrainH(x,z);const g=new THREE.Group();
// Base pillar (octagonal)
const base=new THREE.Mesh(new THREE.CylinderGeometry(4*sc,5*sc,h*.6,8),mt.stGoth);base.position.y=h*.3;base.castShadow=true;g.add(base);addSolid(base);
// Upper taper
const upper=new THREE.Mesh(new THREE.CylinderGeometry(3*sc,4*sc,h*.25,8),mt.st);upper.position.y=h*.7;upper.castShadow=true;g.add(upper);
// Pointed spire top
const spire=new THREE.Mesh(new THREE.ConeGeometry(3.5*sc,h*.45,8),mt.stD);spire.position.y=h*.95+h*.2;spire.castShadow=true;g.add(spire);
// Finial (ornament at top)
const finial=new THREE.Mesh(new THREE.SphereGeometry(.8*sc,6,6),mt.gold);finial.position.y=h*1.2+h*.2;g.add(finial);
// Window slits on 4 sides
for(let i=0;i<4;i++){const a=i/4*Math.PI*2;
const slit=new THREE.Mesh(new THREE.BoxGeometry(.6*sc,3*sc,.2),new MS({color:0x050505,roughness:1}));
slit.position.set(Math.cos(a)*(4.2*sc),h*.4,Math.sin(a)*(4.2*sc));slit.rotation.y=a;g.add(slit);
// Pointed arch above slit
const arch=new THREE.Mesh(new THREE.ConeGeometry(.8*sc,1.5*sc,3),mt.stGoth);arch.position.set(Math.cos(a)*(4.1*sc),h*.4+2.2*sc,Math.sin(a)*(4.1*sc));arch.rotation.y=a;g.add(arch)}
// Crenellations at transition
for(let i=0;i<8;i++){const a=i/8*Math.PI*2;const cr=new THREE.Mesh(new THREE.BoxGeometry(1.5*sc,1.5*sc,1*sc),mt.stGoth);cr.position.set(Math.cos(a)*(4.8*sc),h*.62,Math.sin(a)*(4.8*sc));cr.rotation.y=a;cr.castShadow=true;g.add(cr)}
g.position.set(x,bY,z);scene.add(g);
const fm=new THREE.Mesh(new THREE.SphereGeometry(1.5,6,6),mt.fl);fm.position.set(x,bY+h*.55,z);scene.add(fm);
torchPositions.push({x,y:bY+h*.55,z,mesh:fm,ph:Math.random()*6.28,big:false})}

function gothicArch(x,z,rot,sc){sc=sc||1;const bY=meshTerrainH(x,z);const g=new THREE.Group();
// Two pillars
[-1,1].forEach(s=>{const p=new THREE.Mesh(new THREE.BoxGeometry(3*sc,24*sc,3*sc),mt.stGoth);p.position.set(s*7*sc,12*sc,0);p.castShadow=true;g.add(p);addSolid(p);
// Capital (decorative top)
const cap=new THREE.Mesh(new THREE.BoxGeometry(4*sc,1.5*sc,4*sc),mt.st);cap.position.set(s*7*sc,24.5*sc,0);cap.castShadow=true;g.add(cap);
// Pillar base
const pb=new THREE.Mesh(new THREE.BoxGeometry(4*sc,2*sc,4*sc),mt.stD);pb.position.set(s*7*sc,1*sc,0);g.add(pb)});
// Pointed arch top (triangular approximation)
const archTop=new THREE.Mesh(new THREE.ConeGeometry(8*sc,8*sc,4),mt.stGoth);archTop.position.set(0,29*sc,0);archTop.rotation.y=Math.PI/4;archTop.castShadow=true;g.add(archTop);
// Lintel
const lintel=new THREE.Mesh(new THREE.BoxGeometry(18*sc,2*sc,3*sc),mt.st);lintel.position.set(0,25*sc,0);lintel.castShadow=true;g.add(lintel);
// Rubble
for(let i=0;i<6;i++){const rb=new THREE.Mesh(new THREE.IcosahedronGeometry(.8+Math.random()*1.5,0),mt.rkD);
rb.position.set((Math.random()-.5)*12*sc,Math.random()*1.5,(Math.random()-.5)*5);rb.rotation.set(Math.random(),Math.random(),Math.random());g.add(rb)}
g.position.set(x,bY,z);g.rotation.y=rot||0;scene.add(g)}

function flyingButtress(x,z,rot,sc){sc=sc||1;const bY=meshTerrainH(x,z);const g=new THREE.Group();
// Base pier
const pier=new THREE.Mesh(new THREE.BoxGeometry(2.5*sc,18*sc,2.5*sc),mt.stGoth);pier.position.set(0,9*sc,0);pier.castShadow=true;g.add(pier);
// Arch arm (angled)
const arm=new THREE.Mesh(new THREE.BoxGeometry(1.5*sc,2*sc,14*sc),mt.st);arm.position.set(0,16*sc,6*sc);arm.rotation.x=-.35;arm.castShadow=true;g.add(arm);
// Pinnacle on top
const pin=new THREE.Mesh(new THREE.ConeGeometry(1.5*sc,6*sc,6),mt.stD);pin.position.set(0,21*sc,0);pin.castShadow=true;g.add(pin);
g.position.set(x,bY,z);g.rotation.y=rot||0;scene.add(g)}

function cathedral(x,z,rot,sc){sc=sc||1;const bY=meshTerrainH(x,z);const g=new THREE.Group();
// Main nave
const nave=new THREE.Mesh(new THREE.BoxGeometry(20*sc,25*sc,40*sc),mt.stGoth);nave.position.y=12.5*sc;nave.castShadow=true;g.add(nave);addSolid(nave);
// Peaked roof
const roof=new THREE.Mesh(new THREE.BoxGeometry(22*sc,3*sc,42*sc),mt.rfSlate);roof.position.y=26*sc;roof.rotation.z=0;roof.castShadow=true;g.add(roof);addSolid(roof);
const roofPeak=new THREE.Mesh(new THREE.BoxGeometry(4*sc,8*sc,42*sc),mt.rfSlate);roofPeak.position.y=30*sc;roofPeak.castShadow=true;g.add(roofPeak);
// Front face with pointed entrance
const front=new THREE.Mesh(new THREE.BoxGeometry(22*sc,30*sc,2*sc),mt.st);front.position.set(0,15*sc,21*sc);front.castShadow=true;g.add(front);addSolid(front);
// Entrance void
const door=new THREE.Mesh(new THREE.BoxGeometry(6*sc,12*sc,3*sc),new MS({color:0x050505,roughness:1}));door.position.set(0,6*sc,21*sc);g.add(door);
// Pointed gable
const gable=new THREE.Mesh(new THREE.ConeGeometry(12*sc,14*sc,4),mt.stGoth);gable.position.set(0,37*sc,21*sc);gable.rotation.y=Math.PI/4;gable.castShadow=true;g.add(gable);
// Rose window (circle of small arches)
for(let i=0;i<8;i++){const a=i/8*Math.PI*2;const spoke=new THREE.Mesh(new THREE.BoxGeometry(.3*sc,3*sc,.3),mt.stD);spoke.position.set(Math.cos(a)*3.5*sc,22*sc+Math.sin(a)*3.5*sc,22*sc);spoke.rotation.z=a;g.add(spoke)}
const rwRing=new THREE.Mesh(new THREE.TorusGeometry(3.5*sc,.4*sc,6,16),mt.st);rwRing.position.set(0,22*sc,22*sc);g.add(rwRing);
const rwGlow=new THREE.Mesh(new THREE.CircleGeometry(3*sc,12),new MS({color:0x2a3a5a,emissive:0x1a2a4a,emissiveIntensity:.8,side:THREE.DoubleSide}));rwGlow.position.set(0,22*sc,21.8*sc);g.add(rwGlow);
// Bell towers (twin spires)
[-1,1].forEach(s=>{const tw=new THREE.Mesh(new THREE.BoxGeometry(6*sc,35*sc,6*sc),mt.stGoth);tw.position.set(s*14*sc,17.5*sc,19*sc);tw.castShadow=true;g.add(tw);addSolid(tw);
const sp=new THREE.Mesh(new THREE.ConeGeometry(4*sc,16*sc,8),mt.stD);sp.position.set(s*14*sc,43*sc,19*sc);sp.castShadow=true;g.add(sp);
const fin=new THREE.Mesh(new THREE.SphereGeometry(.6*sc,5,5),mt.gold);fin.position.set(s*14*sc,51*sc,19*sc);g.add(fin)});
// Side buttresses
for(let i=0;i<4;i++){const bz=-15+i*10;
[-1,1].forEach(s=>{const but=new THREE.Mesh(new THREE.BoxGeometry(2*sc,16*sc,2*sc),mt.stGoth);but.position.set(s*12*sc,8*sc,bz*sc);but.castShadow=true;g.add(but);
const arm=new THREE.Mesh(new THREE.BoxGeometry(4*sc,1.5*sc,1.5*sc),mt.st);arm.position.set(s*12*sc,14*sc,bz*sc);g.add(arm)})}
// Interior torches
const fm1=new THREE.Mesh(new THREE.SphereGeometry(1.2,6,6),mt.fl);fm1.position.set(0,bY+10*sc,z);scene.add(fm1);
torchPositions.push({x,y:bY+10*sc,z,mesh:fm1,ph:Math.random()*6.28,big:true});
g.position.set(x,bY,z);g.rotation.y=rot||0;scene.add(g)}

function grandStairs(x,z,rot,steps,w,sc){sc=sc||1;steps=steps||12;w=w||10;const bY=meshTerrainH(x,z);const g=new THREE.Group();
for(let i=0;i<steps;i++){const step=new THREE.Mesh(new THREE.BoxGeometry(w*sc,1.2*sc,2.5*sc),mt.stGoth);step.position.set(0,i*1.1*sc,i*2.2*sc);step.castShadow=true;step.receiveShadow=true;g.add(step);addSolid(step)}
// Balustrades
[-1,1].forEach(s=>{for(let i=0;i<steps;i+=2){const post=new THREE.Mesh(new THREE.CylinderGeometry(.3*sc,.35*sc,4*sc,5),mt.st);post.position.set(s*(w/2+.5)*sc,i*1.1*sc+2*sc,i*2.2*sc);post.castShadow=true;g.add(post)}});
g.position.set(x,bY,z);g.rotation.y=rot||0;scene.add(g)}

// ========== LUMBRIDGE (0,0) — minimal hand-placed, procCity handles bulk ==========
gothicArch(0,10,0,1.2);bonfire(0,5);
cathedral(120,80,-.3,.8);grandStairs(120,108,-.3,8,8,.8);
torch(30,20);torch(55,35);torch(0,-40);

// ========== VARROCK (550,50) ==========
cathedral(555,50,0,1.2);grandStairs(555,80,0,10,12,1);bonfire(555,50);
torch(490,90);torch(620,10);

// ========== WILDERNESS (0,-650) ==========
for(let i=0;i<5;i++)ruin((Math.random()-.5)*300,-550-Math.random()*200);
for(let i=0;i<3;i++){const lx=(Math.random()-.5)*200,lz=-600-Math.random()*150;const lv=new THREE.Mesh(new THREE.CircleGeometry(6+Math.random()*8,8),mt.lava);lv.rotation.x=-Math.PI/2;lv.position.set(lx,meshTerrainH(lx,lz)+.5,lz);scene.add(lv);torchPositions.push({x:lx,y:meshTerrainH(lx,lz)+4,z:lz,mesh:lv,ph:Math.random()*6.28,big:true,col:0xff4400})}
tower(-45,-580,1.5);tower(55,-580,1.5);

// ========== AL KHARID (580,400) ==========
tower(525,350,1.2);tower(640,450,1.2);bonfire(580,400);

// ========== FALADOR (-480,280) ==========
cathedral(-480,280,Math.PI/2,1);grandStairs(-480,305,0,8,10,.9);bonfire(-480,260);

// ========== BARBARIAN VILLAGE (280,-250) ==========
hut(260,-240,.3,1.2);hut(300,-260,-.5,1);bonfire(280,-250);

// ========== DRAYNOR (-300,-150) ==========
hut(-320,-160,1,.8);hut(-280,-180,-.5,.9);tower(-315,-100,1.2);bonfire(-300,-150);

// ========== PORT SARIM (-160,480) ==========
hut(-190,460,.5,1);hut(-150,470,.8,1);bridge(-160,420,0,40);
const hull=new THREE.Mesh(new THREE.BoxGeometry(14,6,30),mt.wd);hull.position.set(-30,meshTerrainH(-30,510)+3,510);hull.castShadow=true;scene.add(hull);
bonfire(-160,470);

// ========== EDGEVILLE (150,-350) ==========
hut(140,-340,.5,1);hut(170,-345,-.3,1);bonfire(155,-350);

// ========== CATHERBY (-500,-400) ==========
hut(-520,-390,.3,.9);hut(-505,-395,-.5,.9);bonfire(-500,-400);

// ========== ARDOUGNE (-1200,100) ==========
cathedral(-1200,100,0,1);bonfire(-1200,100);torch(-1250,100);torch(-1150,100);

// ========== CANIFIS (1300,-200) ==========
hut(1270,-210,.3,.8);hut(1330,-205,-.4,.8);tower(1340,-180,1.2);bonfire(1300,-200);

// ========== MORYTANIA (1600,-400) ==========
for(let i=0;i<3;i++)ruin(1550+Math.random()*100,-450+Math.random()*80);
tower(1600,-400,1.5);bonfire(1600,-400);

// ========== KARAMJA (-200,1800) ==========
hut(-230,1790,.3,1);hut(-170,1810,-.5,1);bonfire(-200,1800);

// ========== TROLLHEIM (-200,-3500) ==========
for(let i=0;i<3;i++)ruin(-250+Math.random()*100,-3530+Math.random()*60);
tower(-200,-3480,1.5);bonfire(-200,-3500);

// ========== GOD WARS (0,-4500) ==========
for(let i=0;i<4;i++)ruin(-100+Math.random()*200,-4550+Math.random()*100);
tower(-50,-4500,2.5);tower(50,-4500,2.5);

// ========== DEEP WILDERNESS (0,-1800) ==========
for(let i=0;i<5;i++)ruin(-200+Math.random()*400,-1900+Math.random()*200);

// ========== SEERS VILLAGE (-800,-100) ==========
hut(-840,-110,.3,1);hut(-770,-100,-.5,1);tower(-820,-80,1.2);bonfire(-800,-100);

// ========== RELLEKKA (-400,-3800) ==========
hut(-440,-3810,.3,1.2);hut(-370,-3800,-.5,1.2);bonfire(-400,-3800);

// ========== KELDAGRIM (-800,-3200) ==========
tower(-855,-3230,2);tower(-740,-3230,2);bonfire(-800,-3200);cave(-820,-3250,.2);

// ========== PRIFDDINAS (-4000,-300) ==========
cathedral(-4000,-300,0,1.5);grandStairs(-4000,-265,0,14,14,1.2);bonfire(-4000,-300);

// ========== TZHAAR CITY (1800,1200) ==========
for(let i=0;i<3;i++){const lx=1760+Math.random()*80,lz=1160+Math.random()*80;const lv=new THREE.Mesh(new THREE.CircleGeometry(5,8),mt.lava);lv.rotation.x=-Math.PI/2;lv.position.set(lx,meshTerrainH(lx,lz)+.5,lz);scene.add(lv);torchPositions.push({x:lx,y:meshTerrainH(lx,lz)+3,z:lz,mesh:lv,ph:Math.random()*6.28,big:true,col:0xff3300})}
tower(1800,1200,1.8);cave(1810,1180,.2);bonfire(1800,1200);

// === BRIDGES over rivers ===
bridge(220,0,Math.PI/2,32);bridge(220,100,Math.PI/2,32);bridge(220,-100,Math.PI/2,32);
bridge(-350,-100,Math.PI/2,26);bridge(-350,-300,Math.PI/2,26);
bridge(-1200,200,0,30);bridge(1300,-100,Math.PI/2,30);bridge(-200,1650,0,40);

console.log('INIT: hand-placed done, starting scatter');
// === SCATTER TREES (GPU InstancedMesh — 6 draw calls instead of ~9600) ===
{const PINE_MAX=1200,PALM_MAX=400,DEAD_MAX=300;
const _pos=new THREE.Vector3(),_quat=new THREE.Quaternion(),_scl=new THREE.Vector3(),_m=new THREE.Matrix4();
// Pine: trunk cylinder + canopy cone
const pineTG=new THREE.CylinderGeometry(.6,1,12,4);const pineCG=new THREE.ConeGeometry(5,14,5);
const pineTrunks=new THREE.InstancedMesh(pineTG,mt.bk,PINE_MAX);
const pineCanopies=new THREE.InstancedMesh(pineCG,mt.lf,PINE_MAX);
// Palm: trunk + top sphere
const palmTG=new THREE.CylinderGeometry(.3,.7,14,4);const palmCG=new THREE.SphereGeometry(4,5,4);
const palmTrunks=new THREE.InstancedMesh(palmTG,mt.bk,PALM_MAX);
const palmTops=new THREE.InstancedMesh(palmCG,mt.lfL,PALM_MAX);
// Dead: trunk + branch
const deadMat=new MS({color:0x3a2a1a,roughness:.95});
const deadTG=new THREE.CylinderGeometry(.2,.7,10,4);const deadBG=new THREE.CylinderGeometry(.08,.2,4,3);
const deadTrunks=new THREE.InstancedMesh(deadTG,deadMat,DEAD_MAX);
const deadBranches=new THREE.InstancedMesh(deadBG,deadMat,DEAD_MAX);
let pi=0,pa=0,de=0;_quat.identity();
for(let i=0;i<1200;i++){const x=(Math.random()-.5)*60000,z=(Math.random()-.5)*50000;
if(isInLake(x,z))continue;const rg=getReg(x,z);const h=meshTerrainH(x,z);if(h>100)continue;
const sc=.7+Math.random()*.6;
const isDes=rg.n.includes('Desert')||rg.n==='Al Kharid'||rg.n==='Sophanem'||rg.n==='Menaphos';
const isDead=rg.n==='Wilderness'||rg.n.includes('Wild')||rg.n==='Draynor'||rg.n==='Morytania'||rg.n==='Canifis';
const isTrop=rg.n==='Karamja'||rg.n==='Brimhaven'||rg.n.includes('Harmless');
if((isDes||isTrop)&&pa<PALM_MAX){
_scl.set(sc,sc+Math.random()*.3,sc);_pos.set(x,h+7*sc,z);_m.compose(_pos,_quat,_scl);palmTrunks.setMatrixAt(pa,_m);
_pos.set(x,h+15*sc,z);_scl.set(sc,sc*.8,sc);_m.compose(_pos,_quat,_scl);palmTops.setMatrixAt(pa,_m);pa++;
}else if(isDead&&de<DEAD_MAX){
_scl.set(sc,sc,sc);_pos.set(x,h+5*sc,z);_m.compose(_pos,_quat,_scl);deadTrunks.setMatrixAt(de,_m);
_pos.set(x+sc*2,h+7*sc,z);_scl.set(sc,sc*.8,sc);_m.compose(_pos,_quat,_scl);deadBranches.setMatrixAt(de,_m);de++;
}else if(pi<PINE_MAX){
_scl.set(sc,sc+Math.random()*.4,sc);_pos.set(x,h+6*sc,z);_m.compose(_pos,_quat,_scl);pineTrunks.setMatrixAt(pi,_m);
_pos.set(x,h+13*sc,z);_scl.set(sc,sc,sc);_m.compose(_pos,_quat,_scl);pineCanopies.setMatrixAt(pi,_m);pi++;}}
pineTrunks.count=pi;pineCanopies.count=pi;palmTrunks.count=pa;palmTops.count=pa;deadTrunks.count=de;deadBranches.count=de;
[pineTrunks,pineCanopies,palmTrunks,palmTops,deadTrunks,deadBranches].forEach(m=>{m.instanceMatrix.needsUpdate=true;m.frustumCulled=false;scene.add(m)});
}

// === SCATTER BOULDERS (GPU instanced - 2 draw calls instead of 800) ===
{const boulderGeo=new THREE.IcosahedronGeometry(1,1);
const bPos=boulderGeo.attributes.position;for(let j=0;j<bPos.count;j++){bPos.setX(j,bPos.getX(j)+(Math.random()-.5)*.3);bPos.setY(j,bPos.getY(j)+(Math.random()-.5)*.3);bPos.setZ(j,bPos.getZ(j)+(Math.random()-.5)*.3)}boulderGeo.computeVertexNormals();
const bInst1=new THREE.InstancedMesh(boulderGeo,mt.rk,800);const bInst2=new THREE.InstancedMesh(boulderGeo,mt.rkD,800);
let c1=0,c2=0;const dm=new THREE.Matrix4();
for(let i=0;i<1600&&(c1<800||c2<800);i++){const bx=(Math.random()-.5)*60000,bz=(Math.random()-.5)*50000;
if(isInLake(bx,bz))continue;const s=2+Math.random()*5;dm.makeScale(s,s,s);dm.setPosition(bx,meshTerrainH(bx,bz)+s*.4,bz);
if(Math.random()>.5&&c1<800){bInst1.setMatrixAt(c1++,dm)}else if(c2<800){bInst2.setMatrixAt(c2++,dm)}}
bInst1.count=c1;bInst2.count=c2;bInst1.instanceMatrix.needsUpdate=true;bInst2.instanceMatrix.needsUpdate=true;
bInst1.castShadow=true;bInst2.castShadow=true;scene.add(bInst1);scene.add(bInst2)}

// === GRASS TUFTS (GPU instanced - 1 draw call instead of 2000) ===
{const grassGeo=new THREE.PlaneGeometry(1,2.5);
const grassMat=new MS({color:0x3a5a20,roughness:1,side:THREE.DoubleSide,transparent:true,opacity:.7});
const grassInst=new THREE.InstancedMesh(grassGeo,grassMat,5000);
let gi=0;const gm=new THREE.Matrix4(),gr=new THREE.Matrix4();
for(let i=0;i<3000&&gi<5000;i++){const gx=(Math.random()-.5)*50000,gz=(Math.random()-.5)*40000;const rg=getReg(gx,gz);
if(rg.n==='Wilderness'||rg.n==='Al Kharid'||isInLake(gx,gz))continue;
const gh=meshTerrainH(gx,gz);if(gh>80)continue;
gr.makeRotationY(Math.random()*Math.PI);gm.makeTranslation(gx,gh+1.5,gz);gm.multiply(gr);grassInst.setMatrixAt(gi++,gm);
gr.makeRotationY(Math.random()*Math.PI+Math.PI/2);gm.makeTranslation(gx,gh+1.5,gz);gm.multiply(gr);grassInst.setMatrixAt(gi++,gm)}
grassInst.count=gi;grassInst.instanceMatrix.needsUpdate=true;scene.add(grassInst)}

console.log('INIT: scatter done, starting procCity');
// === PROCEDURAL CITY GENERATION ===
// Footprint tracking to prevent building overlap
const cityFootprints=[];
function canPlace(bx,bz,rad){for(const f of cityFootprints){if(Math.hypot(bx-f.x,bz-f.z)<rad+f.r)return false}return true}
function markPlace(bx,bz,rad){cityFootprints.push({x:bx,z:bz,r:rad})}
function procCity(cx,cz,radius,density,style){
const bTypes=['house','shop','tavern','workshop','warehouse','manor'];
const nBuildings=Math.floor(density*radius/4);
// City walls
const wallSegs=Math.floor(radius*2*Math.PI/30);
for(let i=0;i<wallSegs;i++){const a=i/wallSegs*Math.PI*2;
wall(cx+Math.cos(a)*(radius+5),cz+Math.sin(a)*(radius+5),16,18,a)}
// Corner towers
for(let i=0;i<6;i++){const a=i/6*Math.PI*2;const tx=cx+Math.cos(a)*(radius+8),tz=cz+Math.sin(a)*(radius+8);tower(tx,tz,1.3);markPlace(tx,tz,12)}
// Gate arches
for(let i=0;i<4;i++){const a=i/4*Math.PI*2;gothicArch(cx+Math.cos(a)*(radius+5),cz+Math.sin(a)*(radius+5),a,1)}
// Streets
const streetMat=new MS({color:0x6a6a60,roughness:.95});
for(let i=0;i<4;i++){const a=i/4*Math.PI*2;const sLen=radius*1.8;
const st=new THREE.Mesh(new THREE.BoxGeometry(4,.1,sLen),streetMat);st.position.set(cx+Math.cos(a)*radius*.4,meshTerrainH(cx,cz)+.2,cz+Math.sin(a)*radius*.4);st.rotation.y=a;st.receiveShadow=true;scene.add(st)}
// Buildings with overlap prevention
let placed=0;
for(let i=0;i<nBuildings*3&&placed<nBuildings;i++){
const a=Math.random()*Math.PI*2;const r=14+Math.random()*(radius-20);
const bx=cx+Math.cos(a)*r,bz=cz+Math.sin(a)*r;
if(isInLake(bx,bz))continue;
const bType=bTypes[Math.floor(Math.random()*bTypes.length)];
const sc=.7+Math.random()*.6;const footprint=bType==='manor'?18*sc:bType==='warehouse'?14*sc:10*sc;
if(!canPlace(bx,bz,footprint))continue;
markPlace(bx,bz,footprint);placed++;
const bRot=a+Math.PI+Math.random()*.4-.2;
if(bType==='house'||bType==='shop')hut(bx,bz,bRot,sc);
else if(bType==='tavern'){hut(bx,bz,bRot,sc*1.3);torch(bx+Math.cos(bRot)*8,bz+Math.sin(bRot)*8)}
else if(bType==='workshop'){hut(bx,bz,bRot,sc*.9)}
else if(bType==='warehouse'){const h=meshTerrainH(bx,bz);const wh=new THREE.Mesh(new THREE.BoxGeometry(16*sc,12*sc,14*sc),mt.wd);wh.position.set(bx,h+6*sc,bz);wh.rotation.y=bRot;wh.castShadow=true;scene.add(wh);addSolid(wh);const rf=new THREE.Mesh(new THREE.BoxGeometry(18*sc,1*sc,16*sc),mt.rf);rf.position.set(bx,h+12.5*sc,bz);rf.rotation.y=bRot;scene.add(rf);addSolid(rf)}
else if(bType==='manor'){hut(bx,bz,bRot,sc*1.5);
for(let f=0;f<4;f++){const fa=bRot+f/4*Math.PI*2;const fx=bx+Math.cos(fa)*12*sc,fz=bz+Math.sin(fa)*12*sc;
const fence=new THREE.Mesh(new THREE.BoxGeometry(8*sc,3,.2),mt.wd);fence.position.set(fx,meshTerrainH(fx,fz)+1.5,fz);fence.rotation.y=fa;scene.add(fence)}}}
// Market square at center (reserve footprint)
markPlace(cx,cz,22);
for(let i=0;i<6;i++){const a=i/6*Math.PI*2;const sx=cx+Math.cos(a)*15,sz=cz+Math.sin(a)*15;
const stall=new THREE.Mesh(new THREE.BoxGeometry(4,3,3),mt.wd);stall.position.set(sx,meshTerrainH(sx,sz)+1.5,sz);stall.rotation.y=a;scene.add(stall);addSolid(stall);
const canopy=new THREE.Mesh(new THREE.BoxGeometry(5,.15,4),new MS({color:[0x8a2020,0x203a8a,0x2a6a2a,0x8a6a20,0x6a2a6a,0x2a6a6a][i],roughness:.9}));canopy.position.set(sx,meshTerrainH(sx,sz)+3.2,sz);canopy.rotation.y=a;scene.add(canopy)}
const fountain=new THREE.Mesh(new THREE.CylinderGeometry(4,5,2,12),mt.st);fountain.position.set(cx,meshTerrainH(cx,cz)+1,cz);scene.add(fountain);addSolid(fountain);
const fWater=new THREE.Mesh(new THREE.CylinderGeometry(3.5,3.5,.5,12),mt.lakeMat);fWater.position.set(cx,meshTerrainH(cx,cz)+2.3,cz);scene.add(fWater);
bonfire(cx+20,cz+20);bonfire(cx-20,cz-20);
}

// === MASSIVE CASTLE GENERATOR ===
function castle(cx,cz,sc,rot){
sc=sc||1;rot=rot||0;const bY=meshTerrainH(cx,cz);const g=new THREE.Group();
// --- OUTER CURTAIN WALL (huge perimeter) ---
const wallR=120*sc,wallH=40*sc,wallT=6*sc;
const wallSegs=20;
for(let i=0;i<wallSegs;i++){const a=i/wallSegs*Math.PI*2;const a2=(i+1)/wallSegs*Math.PI*2;
const wx=Math.cos(a)*wallR,wz=Math.sin(a)*wallR;
const segLen=wallR*2*Math.PI/wallSegs;
const wm=new THREE.Mesh(new THREE.BoxGeometry(segLen,wallH,wallT),mt.stGoth);
wm.position.set((Math.cos(a)+Math.cos(a2))/2*wallR,wallH/2,(Math.sin(a)+Math.sin(a2))/2*wallR);
wm.rotation.y=-(a+a2)/2+Math.PI/2;wm.castShadow=true;g.add(wm);addSolid(wm);
// Battlements on top
for(let b=0;b<3;b++){const bOff=(b-1)*segLen/3;
const merlon=new THREE.Mesh(new THREE.BoxGeometry(3*sc,4*sc,wallT+1),mt.stD);
merlon.position.set(wm.position.x+Math.cos(-(a+a2)/2+Math.PI/2)*bOff,wallH+2*sc,wm.position.z+Math.sin(-(a+a2)/2+Math.PI/2)*bOff);
merlon.rotation.y=wm.rotation.y;g.add(merlon)}}
// --- CORNER TOWERS (8 massive towers) ---
for(let i=0;i<8;i++){const a=i/8*Math.PI*2;const tx=Math.cos(a)*(wallR+4*sc),tz=Math.sin(a)*(wallR+4*sc);
const tH=55*sc;
const tBase=new THREE.Mesh(new THREE.CylinderGeometry(10*sc,12*sc,tH,12),mt.stGoth);tBase.position.set(tx,tH/2,tz);tBase.castShadow=true;g.add(tBase);addSolid(tBase);
const tRoof=new THREE.Mesh(new THREE.ConeGeometry(12*sc,18*sc,12),mt.rfSlate);tRoof.position.set(tx,tH+9*sc,tz);tRoof.castShadow=true;g.add(tRoof);
const tFin=new THREE.Mesh(new THREE.SphereGeometry(1.5*sc,6,6),mt.gold);tFin.position.set(tx,tH+18*sc,tz);g.add(tFin);
// Tower battlements
for(let b=0;b<8;b++){const ba=b/8*Math.PI*2;
const merlon=new THREE.Mesh(new THREE.BoxGeometry(3*sc,4*sc,3*sc),mt.stD);
merlon.position.set(tx+Math.cos(ba)*10.5*sc,tH+2*sc,tz+Math.sin(ba)*10.5*sc);g.add(merlon)}}
// --- KEEP (central massive tower) ---
const keepW=50*sc,keepD=40*sc,keepH=80*sc;
const keep=new THREE.Mesh(new THREE.BoxGeometry(keepW,keepH,keepD),mt.stGoth);keep.position.y=keepH/2;keep.castShadow=true;g.add(keep);addSolid(keep);
// Keep roof
const keepRoof=new THREE.Mesh(new THREE.BoxGeometry(keepW+6*sc,4*sc,keepD+6*sc),mt.rfSlate);keepRoof.position.y=keepH+2*sc;keepRoof.castShadow=true;g.add(keepRoof);addSolid(keepRoof);
// Keep battlements
for(let i=0;i<12;i++){const bx=-keepW/2+i*keepW/11;
const m1=new THREE.Mesh(new THREE.BoxGeometry(3*sc,5*sc,3*sc),mt.stD);m1.position.set(bx,keepH+4.5*sc,keepD/2);m1.castShadow=true;g.add(m1);
const m2=m1.clone();m2.position.z=-keepD/2;g.add(m2)}
for(let i=0;i<8;i++){const bz=-keepD/2+i*keepD/7;
const m1=new THREE.Mesh(new THREE.BoxGeometry(3*sc,5*sc,3*sc),mt.stD);m1.position.set(keepW/2,keepH+4.5*sc,bz);g.add(m1);
const m2=m1.clone();m2.position.x=-keepW/2;g.add(m2)}
// Keep windows (rows of tall gothic windows)
for(let lv=0;lv<3;lv++){for(let i=0;i<6;i++){const wx=-keepW/2+keepW/(6+1)*(i+1);
const win=new THREE.Mesh(new THREE.BoxGeometry(2*sc,8*sc,.5),new MS({color:0x1a2a4a,emissive:0x0a1a3a,emissiveIntensity:.6,transparent:true,opacity:.5}));
win.position.set(wx,20*sc+lv*22*sc,keepD/2+.5);g.add(win);
const wFrame=new THREE.Mesh(new THREE.BoxGeometry(3*sc,9*sc,.3),mt.stD);wFrame.position.set(wx,20*sc+lv*22*sc,keepD/2+.7);g.add(wFrame)}}
// --- GATEHOUSE (front entrance with portcullis) ---
const ghW=20*sc,ghH=35*sc,ghD=14*sc;
const ghL=new THREE.Mesh(new THREE.BoxGeometry(ghW/2-3*sc,ghH,ghD),mt.stGoth);ghL.position.set(-ghW/4-1.5*sc,ghH/2,wallR);ghL.castShadow=true;g.add(ghL);addSolid(ghL);
const ghR=ghL.clone();ghR.position.x=ghW/4+1.5*sc;g.add(ghR);addSolid(ghR);
// Portcullis arch
const ghArch=new THREE.Mesh(new THREE.BoxGeometry(7*sc,4*sc,ghD),mt.stD);ghArch.position.set(0,ghH-2*sc,wallR);g.add(ghArch);
// Gatehouse towers
[-1,1].forEach(s=>{const gt=new THREE.Mesh(new THREE.CylinderGeometry(7*sc,8*sc,ghH+10*sc,10),mt.stGoth);
gt.position.set(s*12*sc,(ghH+10*sc)/2,wallR);gt.castShadow=true;g.add(gt);addSolid(gt);
const gtRoof=new THREE.Mesh(new THREE.ConeGeometry(9*sc,14*sc,10),mt.rfSlate);gtRoof.position.set(s*12*sc,ghH+12*sc,wallR);g.add(gtRoof)});
// --- INNER COURTYARD FEATURES ---
// Great hall
const hallW=36*sc,hallH=30*sc,hallD=60*sc;
const hall=new THREE.Mesh(new THREE.BoxGeometry(hallW,hallH,hallD),mt.stD);hall.position.set(0,hallH/2,-30*sc);hall.castShadow=true;g.add(hall);addSolid(hall);
const hallRoof=new THREE.Mesh(new THREE.BoxGeometry(hallW+4*sc,3*sc,hallD+4*sc),mt.rfSlate);hallRoof.position.set(0,hallH+1.5*sc,-30*sc);g.add(hallRoof);addSolid(hallRoof);
// Chapel spire
const chapel=new THREE.Mesh(new THREE.BoxGeometry(16*sc,25*sc,20*sc),mt.st);chapel.position.set(40*sc,12.5*sc,-20*sc);chapel.castShadow=true;g.add(chapel);addSolid(chapel);
const chapelSpire=new THREE.Mesh(new THREE.ConeGeometry(6*sc,30*sc,6),mt.rfSlate);chapelSpire.position.set(40*sc,40*sc,-20*sc);chapelSpire.castShadow=true;g.add(chapelSpire);
const cross=new THREE.Mesh(new THREE.BoxGeometry(.5*sc,4*sc,.5*sc),mt.gold);cross.position.set(40*sc,56*sc,-20*sc);g.add(cross);
// Courtyard torches
for(let i=0;i<6;i++){const ta=i/6*Math.PI*2;const ttx=Math.cos(ta)*40*sc,ttz=Math.sin(ta)*40*sc;
const tPost=new THREE.Mesh(new THREE.CylinderGeometry(.4*sc,.5*sc,12*sc,5),mt.wd);tPost.position.set(ttx,6*sc,ttz);g.add(tPost);
const tFlame=new THREE.Mesh(new THREE.SphereGeometry(1*sc,6,6),mt.fl);tFlame.position.set(ttx,13*sc,ttz);g.add(tFlame);
torchPositions.push({x:cx+ttx*Math.cos(rot)-ttz*Math.sin(rot),y:bY+13*sc,z:cz+ttx*Math.sin(rot)+ttz*Math.cos(rot),mesh:tFlame,ph:i,big:true})}
// Inner well
const well=new THREE.Mesh(new THREE.CylinderGeometry(3*sc,3.5*sc,3*sc,10),mt.st);well.position.set(20*sc,1.5*sc,20*sc);g.add(well);
g.position.set(cx,bY,cz);g.rotation.y=rot;scene.add(g);
markPlace(cx,cz,wallR+20*sc);
}

console.log('INIT: procCity defined, generating cities');
// Generate cities at major regions
procCity(0,0,80,1,'medieval');          // Lumbridge
procCity(555,50,70,1.2,'medieval');      // Varrock
procCity(-480,280,65,1,'white');        // Falador
procCity(-1200,100,70,1,'medieval');    // Ardougne

// === MASSIVE CASTLES ===
castle(900,-800,1.2,0);       // Eastern Fortress
castle(-2000,-500,1.5,.5);    // Western Stronghold
castle(0,-1800,1.8,Math.PI/6);// Wilderness Castle (huge)
castle(-800,600,1,-.3);       // Southern Keep
castle(1500,400,1.3,.8);      // Desert Citadel

// === WATERFALLS ===
function waterfall(x,z,h,w){const bY=meshTerrainH(x,z);const g=new THREE.Group();
const wfGeo=new THREE.PlaneGeometry(w,h,6,16);const wfMat=new MS({color:0x4a8aaa,roughness:.1,metalness:.35,transparent:true,opacity:.6,side:THREE.DoubleSide,emissive:0x1a4a5a,emissiveIntensity:.25});
const wf=new THREE.Mesh(wfGeo,wfMat);wf.position.y=h/2;g.add(wf);
// Inner cascade (brighter)
const wf2=new THREE.Mesh(new THREE.PlaneGeometry(w*.6,h,4,12),new MS({color:0x6aaacc,roughness:.05,metalness:.3,transparent:true,opacity:.4,side:THREE.DoubleSide,emissive:0x2a5a6a,emissiveIntensity:.3}));wf2.position.set(0,h/2,.2);g.add(wf2);
// Rocky sides
[-1,1].forEach(s=>{for(let i=0;i<4;i++){const rk=new THREE.Mesh(new THREE.IcosahedronGeometry(1+Math.random()*2,0),mt.rk);rk.position.set(s*(w/2+1),Math.random()*h,Math.random()*2-1);rk.castShadow=true;g.add(rk)}});
// Mist spray at base
for(let i=0;i<6;i++){const mist=new THREE.Mesh(new THREE.SphereGeometry(.5+Math.random()*1.5,6,6),new MS({color:0xaaccdd,transparent:true,opacity:.15,roughness:1}));mist.position.set((Math.random()-.5)*w*1.2,-1+Math.random()*3,(Math.random()-.5)*4);g.add(mist)}
// Pool
const pool=new THREE.Mesh(new THREE.CircleGeometry(w*1.4,14),mt.wt);pool.rotation.x=-Math.PI/2;pool.position.set(0,.3,3);g.add(pool);
g.position.set(x,bY,z);scene.add(g)}
waterfall(-480,-420,25,10);waterfall(200,200,15,6);waterfall(-1250,50,20,8);

// === CAVE ENTRANCES ===
function cave(x,z,rot){const h=meshTerrainH(x,z);const cg=new THREE.Group();
const arch=new THREE.Mesh(new THREE.TorusGeometry(8,3,6,8,Math.PI),new MS({color:0x3a3530,roughness:.95}));arch.position.y=8;arch.rotation.z=Math.PI;cg.add(arch);
const dark=new THREE.Mesh(new THREE.CircleGeometry(7,8),new MS({color:0x050505,roughness:1}));dark.position.set(0,5,-1);cg.add(dark);
for(let i=0;i<3;i++){const r=new THREE.Mesh(new THREE.IcosahedronGeometry(2+Math.random()*2,0),mt.rk);r.position.set(-8+Math.random()*16,Math.random()*3,(Math.random()-.5)*4);cg.add(r)}
cg.position.set(x,h,z);cg.rotation.y=rot||0;scene.add(cg)}
cave(50,-600,.5);cave(-250,-180,-.3);cave(-520,-430,.8);

// === SKELETON BONE PILES ===
function bonePile(x,z){const h=meshTerrainH(x,z);const boneMat=new MS({color:0xccccaa,roughness:.85});
for(let i=0;i<3;i++){const b=new THREE.Mesh(new THREE.CylinderGeometry(.08,.08,.8+Math.random(),4),boneMat);b.position.set(x+(Math.random()-.5)*3,h+.3,z+(Math.random()-.5)*3);b.rotation.set(Math.random()*Math.PI,Math.random()*Math.PI,Math.random()*Math.PI);scene.add(b)}
const skull=new THREE.Mesh(new THREE.SphereGeometry(.5,6,6),boneMat);skull.position.set(x,h+.6,z);scene.add(skull)}
for(let i=0;i<5;i++){const bx=(Math.random()-.5)*4000,bz=(Math.random()-.5)*4000;bonePile(bx,bz)}

playerGroup=buildPlayerModel(playerClass);scene.add(playerGroup);

// === FIRELINK SHRINE (Spawn Hub at 0,5) — Gothic Ruin ===
const fH=meshTerrainH(0,5);
// Circular stone base (larger, weathered)
const shrBase=new THREE.Mesh(new THREE.CylinderGeometry(22,24,4,16),mt.stGoth);shrBase.position.set(0,fH+2,5);shrBase.receiveShadow=true;scene.add(shrBase);
const shrFloor=new THREE.Mesh(new THREE.CylinderGeometry(20,20,1.5,16),mt.stD);shrFloor.position.set(0,fH+4.2,5);scene.add(shrFloor);
// Broken gothic pillars (varying heights - some crumbled)
const pillarHeights=[18,14,18,10,18,14,18];
for(let i=0;i<7;i++){const px=-18+i*6;const ph=pillarHeights[i];
const pil=new THREE.Mesh(new THREE.CylinderGeometry(1,1.3,ph,8),mt.stGoth);pil.position.set(px,fH+ph/2+3.5,5-16);pil.castShadow=true;scene.add(pil);addSolid(pil);
// Capital on intact pillars
if(ph>12){const cap=new THREE.Mesh(new THREE.BoxGeometry(3,1.5,3),mt.st);cap.position.set(px,fH+ph+4,5-16);cap.castShadow=true;scene.add(cap)}}
// Grand back wall
const bWall=new THREE.Mesh(new THREE.BoxGeometry(40,18,3),mt.stGoth);bWall.position.set(0,fH+12,5-18);bWall.castShadow=true;scene.add(bWall);
// Pointed arch above entrance
const sArchL=new THREE.Mesh(new THREE.BoxGeometry(4,22,3),mt.st);sArchL.position.set(-8,fH+14,-12);sArchL.castShadow=true;scene.add(sArchL);
const sArchR=sArchL.clone();sArchR.position.x=8;scene.add(sArchR);
const sArchTop=new THREE.Mesh(new THREE.ConeGeometry(9,8,4),mt.stGoth);sArchTop.position.set(0,fH+27,-12);sArchTop.rotation.y=Math.PI/4;sArchTop.castShadow=true;scene.add(sArchTop);
// Side walls (thicker, taller)
const lW=new THREE.Mesh(new THREE.BoxGeometry(3,16,30),mt.stD);lW.position.set(-20,fH+11,5-2);lW.castShadow=true;scene.add(lW);
const rW=lW.clone();rW.position.x=20;scene.add(rW);
// Grand staircase leading down
for(let i=0;i<6;i++){const step=new THREE.Mesh(new THREE.BoxGeometry(12+i*2,1.2,3.5),mt.stGoth);step.position.set(0,fH+3.5-i*1,14+i*3.5);step.receiveShadow=true;scene.add(step)}
// Thrones (gothic high-backed)
[-10,10].forEach(sx=>{const seat=new THREE.Mesh(new THREE.BoxGeometry(4,5,2.5),mt.stD);seat.position.set(sx,fH+6,5-12);seat.castShadow=true;scene.add(seat);
const back=new THREE.Mesh(new THREE.BoxGeometry(4,10,.8),mt.stGoth);back.position.set(sx,fH+10,5-13);scene.add(back);
const finial=new THREE.Mesh(new THREE.ConeGeometry(1.2,3,4),mt.stD);finial.position.set(sx,fH+16,5-13);scene.add(finial)});
// Blacksmith anvil
const anvil=new THREE.Mesh(new THREE.BoxGeometry(2.5,2.5,2),mt.armorDk);anvil.position.set(14,fH+5.5,5);anvil.castShadow=true;scene.add(anvil);
// Shrine bonfire (larger, brighter)
const shrFire=new THREE.Mesh(new THREE.SphereGeometry(3,10,10),mt.fl);shrFire.position.set(0,fH+7,5);scene.add(shrFire);
torchPositions.push({x:0,y:fH+8,z:5,mesh:shrFire,ph:0,big:true});
// Scattered rubble for atmosphere
for(let i=0;i<15;i++){const rb=new THREE.Mesh(new THREE.IcosahedronGeometry(.5+Math.random()*1.5,0),mt.rkD);
rb.position.set((Math.random()-.5)*30,fH+Math.random()*2,5+(Math.random()-.5)*20);rb.rotation.set(Math.random(),Math.random(),Math.random());scene.add(rb)}
// Register Firelink Shrine solids
addSolid(shrBase);addSolid(shrFloor);addSolid(bWall);addSolid(lW);addSolid(rW);addSolid(sArchL);addSolid(sArchR);addSolid(anvil);

// === DUNGEON SYSTEM ===
console.log('INIT: cities+waterfalls+caves+bones done, starting dungeons');
const bossTypes={demon:{hp:500,dmg:35,col:0x8a1010,name:'Infernal Lord'},golem:{hp:600,dmg:30,col:0x5a5a60,name:'Ancient Golem'},wyrm:{hp:450,dmg:40,col:0x4a2050,name:'Shadow Wyrm'},tzhaar:{hp:700,dmg:45,col:0xaa4010,name:'TzTok-Xil'},vampire:{hp:400,dmg:35,col:0x3a0a1a,name:'Blood Count'},elf:{hp:350,dmg:50,col:0x4a6a5a,name:'Crystal Guardian'},
dragon:{hp:800,dmg:50,col:0x2a6a1a,name:'King Black Dragon'},hydra:{hp:900,dmg:55,col:0x4a6a3a,name:'Alchemical Hydra'},kraken:{hp:650,dmg:40,col:0x1a3a5a,name:'Cave Kraken'},cerberus:{hp:750,dmg:60,col:0x5a1a1a,name:'Cerberus'},vorkath:{hp:1000,dmg:65,col:0x2a5a6a,name:'Vorkath'},nightmare:{hp:1200,dmg:70,col:0x2a1a3a,name:'The Nightmare'},nex:{hp:1500,dmg:80,col:0x4a0a3a,name:'Nex'},jad:{hp:850,dmg:55,col:0x8a2a00,name:'TzTok-Jad'},zuk:{hp:2000,dmg:90,col:0xaa3a10,name:'TzKal-Zuk'}};
const specialLoot=[
// WEAPONS (30+)
{name:'Dragon Longsword',atk:45,def:5,str:30,slot:'Weapon',rarity:'rare'},
{name:'Abyssal Whip',atk:55,def:0,str:40,slot:'Weapon',rarity:'rare'},
{name:'Dragon Scimitar',atk:40,def:3,str:28,slot:'Weapon',rarity:'rare'},
{name:'Godsword (Armadyl)',atk:75,def:5,str:55,slot:'Weapon',rarity:'legendary'},
{name:'Godsword (Bandos)',atk:70,def:5,str:65,slot:'Weapon',rarity:'legendary'},
{name:'Godsword (Saradomin)',atk:72,def:10,str:50,slot:'Weapon',rarity:'legendary'},
{name:'Godsword (Zamorak)',atk:78,def:3,str:58,slot:'Weapon',rarity:'legendary'},
{name:'Scythe of Vitur',atk:90,def:0,str:70,slot:'Weapon',rarity:'mythic'},
{name:'Twisted Bow',atk:85,def:0,str:60,slot:'Weapon',rarity:'mythic'},
{name:'Ghrazi Rapier',atk:65,def:0,str:50,slot:'Weapon',rarity:'legendary'},
{name:'Blade of Saeldor',atk:62,def:5,str:48,slot:'Weapon',rarity:'legendary'},
{name:'Inquisitor Mace',atk:60,def:0,str:55,slot:'Weapon',rarity:'legendary'},
{name:'Nightmare Staff',atk:55,def:5,str:35,slot:'Weapon',rarity:'legendary'},
{name:'Trident of the Swamp',atk:50,def:3,str:30,slot:'Weapon',rarity:'rare'},
{name:'Toxic Blowpipe',atk:48,def:0,str:35,slot:'Weapon',rarity:'rare'},
{name:'Dragon Claws',atk:52,def:5,str:42,slot:'Weapon',rarity:'rare'},
{name:'Elder Maul',atk:58,def:0,str:60,slot:'Weapon',rarity:'legendary'},
{name:'Zaryte Crossbow',atk:80,def:0,str:55,slot:'Weapon',rarity:'mythic'},
{name:'Tumeken Shadow',atk:95,def:0,str:75,slot:'Weapon',rarity:'mythic'},
// HELMS (10+)
{name:'Dragon Full Helm',atk:3,def:35,str:5,slot:'Helm',rarity:'rare'},
{name:'Torva Full Helm',atk:5,def:55,str:10,slot:'Helm',rarity:'mythic'},
{name:'Neitiznot Faceguard',atk:8,def:40,str:12,slot:'Helm',rarity:'legendary'},
{name:'Serpentine Helm',atk:3,def:45,str:8,slot:'Helm',rarity:'rare'},
{name:'Justiciar Faceguard',atk:0,def:50,str:3,slot:'Helm',rarity:'legendary'},
{name:'Ancestral Hat',atk:25,def:8,str:0,slot:'Helm',rarity:'legendary'},
{name:'Slayer Helm (i)',atk:12,def:30,str:10,slot:'Helm',rarity:'rare'},
// CHEST (10+)
{name:'Bandos Chestplate',atk:5,def:45,str:15,slot:'Chest',rarity:'rare'},
{name:'Ancestral Robe Top',atk:30,def:10,str:0,slot:'Chest',rarity:'legendary'},
{name:'Torva Platebody',atk:8,def:65,str:15,slot:'Chest',rarity:'mythic'},
{name:'Justiciar Chestguard',atk:0,def:60,str:5,slot:'Chest',rarity:'legendary'},
{name:'Inquisitor Hauberk',atk:10,def:50,str:18,slot:'Chest',rarity:'legendary'},
{name:'Crystal Body',atk:20,def:35,str:8,slot:'Chest',rarity:'rare'},
{name:'Karil Leathertop',atk:18,def:30,str:5,slot:'Chest',rarity:'rare'},
{name:'Armadyl Chestplate',atk:15,def:42,str:8,slot:'Chest',rarity:'rare'},
// LEGS (8+)
{name:'Armadyl Chainskirt',atk:5,def:40,str:10,slot:'Legs',rarity:'rare'},
{name:'Torva Platelegs',atk:5,def:58,str:12,slot:'Legs',rarity:'mythic'},
{name:'Bandos Tassets',atk:4,def:42,str:14,slot:'Legs',rarity:'rare'},
{name:'Justiciar Legguards',atk:0,def:55,str:3,slot:'Legs',rarity:'legendary'},
{name:'Ancestral Robe Bottom',atk:25,def:8,str:0,slot:'Legs',rarity:'legendary'},
{name:'Dragon Platelegs',atk:3,def:35,str:5,slot:'Legs',rarity:'rare'},
// SHIELDS (6+)
{name:'Dragonfire Shield',atk:5,def:50,str:5,slot:'Shield',rarity:'legendary'},
{name:'Avernic Defender',atk:18,def:35,str:12,slot:'Shield',rarity:'legendary'},
{name:'Elysian Spirit Shield',atk:0,def:65,str:0,slot:'Shield',rarity:'mythic'},
{name:'Arcane Spirit Shield',atk:25,def:40,str:0,slot:'Shield',rarity:'mythic'},
{name:'Spectral Spirit Shield',atk:15,def:45,str:0,slot:'Shield',rarity:'legendary'},
{name:'Crystal Shield',atk:5,def:38,str:3,slot:'Shield',rarity:'rare'},
// BOOTS (6+)
{name:'Primordial Boots',atk:2,def:25,str:10,slot:'Boots',rarity:'rare'},
{name:'Pegasian Boots',atk:12,def:18,str:5,slot:'Boots',rarity:'rare'},
{name:'Eternal Boots',atk:18,def:10,str:0,slot:'Boots',rarity:'rare'},
{name:'Dragon Boots',atk:2,def:20,str:8,slot:'Boots',rarity:'rare'},
{name:'Guardian Boots',atk:0,def:28,str:3,slot:'Boots',rarity:'legendary'},
// GLOVES (5+)
{name:'Barrows Gloves',atk:10,def:15,str:10,slot:'Gloves',rarity:'rare'},
{name:'Ferocious Gloves',atk:14,def:12,str:14,slot:'Gloves',rarity:'legendary'},
{name:'Tormented Bracelet',atk:18,def:5,str:2,slot:'Gloves',rarity:'legendary'},
{name:'Zaryte Vambraces',atk:15,def:10,str:5,slot:'Gloves',rarity:'mythic'},
// RINGS (6+)
{name:'Berserker Ring',atk:15,def:5,str:20,slot:'Ring',rarity:'legendary'},
{name:'Ring of Suffering',atk:0,def:22,str:0,slot:'Ring',rarity:'legendary'},
{name:'Brimstone Ring',atk:12,def:12,str:12,slot:'Ring',rarity:'legendary'},
{name:'Ultor Ring',atk:18,def:3,str:22,slot:'Ring',rarity:'mythic'},
{name:'Bellator Ring',atk:20,def:5,str:18,slot:'Ring',rarity:'mythic'},
{name:'Venator Ring',atk:16,def:3,str:15,slot:'Ring',rarity:'mythic'}
];

function genDungeon(entranceX,entranceZ,depth,theme,bossType){
const d={x:entranceX,z:entranceZ,depth,theme,bossType,rooms:[],entered:false};
// Generate rooms procedurally
const nRooms=3+Math.floor(Math.random()*4)+depth;
let rx=0,rz=0;
for(let i=0;i<nRooms;i++){
const w=20+Math.random()*30,h=15+Math.random()*15,l=20+Math.random()*30;
const dir=Math.floor(Math.random()*4);
if(dir===0)rz-=l+5;else if(dir===1)rz+=l+5;else if(dir===2)rx-=w+5;else rx+=w+5;
d.rooms.push({x:rx,z:rz,w,h,l,isBoss:i===nRooms-1,enemies:i===nRooms-1?[{type:bossType,lv:depth*10+20}]:
Array.from({length:2+Math.floor(Math.random()*3)},()=>({type:theme==='fire'?'demon':theme==='undead'?'skeleton':'spider',lv:depth*5+10}))})
}
dungeons.push(d);
// Place cave entrance in world
cave(entranceX,entranceZ,Math.random()*Math.PI*2);
return d}

function enterDungeon(d){
if(inDungeon)return;inDungeon=d;d.entered=true;
// Hide overworld, show dungeon
dungeonGroup=new THREE.Group();
const floorMat=new MS({color:d.theme==='fire'?0x2a1a0a:d.theme==='undead'?0x1a1a1a:0x1a2a1a,roughness:.95});
const wallMat=new MS({color:d.theme==='fire'?0x3a2010:d.theme==='undead'?0x2a2a2a:0x2a3a2a,roughness:.9,metalness:.05});
const ceilMat=new MS({color:0x1a1a1a,roughness:1});
d.rooms.forEach((rm,idx)=>{
// Floor
const fl=new THREE.Mesh(new THREE.BoxGeometry(rm.w,.5,rm.l),floorMat);fl.position.set(rm.x,-d.depth*50,rm.z);fl.receiveShadow=true;dungeonGroup.add(fl);
// Walls
const wN=new THREE.Mesh(new THREE.BoxGeometry(rm.w,rm.h,2),wallMat);wN.position.set(rm.x,-d.depth*50+rm.h/2,rm.z-rm.l/2);wN.castShadow=true;dungeonGroup.add(wN);
const wS=wN.clone();wS.position.z=rm.z+rm.l/2;dungeonGroup.add(wS);
const wE=new THREE.Mesh(new THREE.BoxGeometry(2,rm.h,rm.l),wallMat);wE.position.set(rm.x+rm.w/2,-d.depth*50+rm.h/2,rm.z);wE.castShadow=true;dungeonGroup.add(wE);
const wW=wE.clone();wW.position.x=rm.x-rm.w/2;dungeonGroup.add(wW);
// Ceiling
const ceil=new THREE.Mesh(new THREE.BoxGeometry(rm.w,1,rm.l),ceilMat);ceil.position.set(rm.x,-d.depth*50+rm.h,rm.z);dungeonGroup.add(ceil);
// Torches
[[-1,-1],[-1,1],[1,-1],[1,1]].forEach(([sx,sz])=>{const fm=new THREE.Mesh(new THREE.SphereGeometry(.8,6,6),mt.fl);
fm.position.set(rm.x+sx*(rm.w/2-2),-d.depth*50+rm.h*.7,rm.z+sz*(rm.l/2-2));dungeonGroup.add(fm);
torchPositions.push({x:rm.x+sx*(rm.w/2-2),y:-d.depth*50+rm.h*.7,z:rm.z+sz*(rm.l/2-2),mesh:fm,ph:Math.random()*6.28,big:false})});
// Decor
if(d.theme==='undead'){for(let i=0;i<5;i++){bonePile(rm.x+(Math.random()-.5)*rm.w*.6,rm.z+(Math.random()-.5)*rm.l*.6)}}
// Spawn enemies in room
rm.enemies.forEach(e=>{spawnE(e.type,rm.x+(Math.random()-.5)*rm.w*.5,rm.z+(Math.random()-.5)*rm.l*.5,e.lv)});
// Boss room chest
if(rm.isBoss){const chest=new THREE.Mesh(new THREE.BoxGeometry(3,2,2),new MS({color:0xc8a040,roughness:.4,metalness:.6}));
chest.position.set(rm.x,-d.depth*50+1.5,rm.z);chest.castShadow=true;dungeonGroup.add(chest);
const lid=new THREE.Mesh(new THREE.BoxGeometry(3.2,.5,2.2),new MS({color:0xb09030,roughness:.45,metalness:.55}));
lid.position.set(rm.x,-d.depth*50+2.8,rm.z);dungeonGroup.add(lid)}
});
// Corridors between rooms
for(let i=0;i<d.rooms.length-1;i++){
const a=d.rooms[i],b=d.rooms[i+1];
const cx=(a.x+b.x)/2,cz=(a.z+b.z)/2;
const cl=Math.hypot(b.x-a.x,b.z-a.z);
const corr=new THREE.Mesh(new THREE.BoxGeometry(6,.5,cl),floorMat);corr.position.set(cx,-d.depth*50,cz);
corr.rotation.y=Math.atan2(b.x-a.x,b.z-a.z);dungeonGroup.add(corr)}
scene.add(dungeonGroup);
player.x=d.rooms[0].x;player.z=d.rooms[0].z;
log('Entered dungeon! Depth: '+d.depth+' — defeat the boss for special loot!','#f80')}

function exitDungeon(){if(!inDungeon)return;
if(dungeonGroup){scene.remove(dungeonGroup);dungeonGroup=null}
player.x=inDungeon.x;player.z=inDungeon.z+10;inDungeon=null;
log('Exited dungeon.','#0f0')}

// Generate dungeons at key locations
genDungeon(50,-600,1,'undead','golem');genDungeon(-250,-180,1,'fire','demon');genDungeon(-520,-430,2,'cave','wyrm');
genDungeon(-820,-3250,3,'undead','golem');genDungeon(2480,-1550,2,'cave','wyrm');genDungeon(1810,1180,3,'fire','tzhaar');
genDungeon(-2820,1620,2,'undead','golem');genDungeon(-2780,1580,1,'cave','wyrm');genDungeon(-3600,-50,2,'cave','elf');
genDungeon(0,-4500,4,'fire','demon');genDungeon(-800,-3200,3,'undead','golem');genDungeon(1300,-200,2,'undead','vampire');
// NEW BOSS DUNGEONS
genDungeon(2100,650,3,'fire','dragon');genDungeon(-200,1900,2,'cave','hydra');genDungeon(500,2600,2,'cave','kraken');
genDungeon(150,-400,3,'fire','cerberus');genDungeon(2500,-1400,4,'cave','vorkath');genDungeon(-2200,1850,3,'undead','nightmare');
genDungeon(0,-4600,5,'fire','nex');genDungeon(1850,1250,4,'fire','jad');genDungeon(1900,1300,5,'fire','zuk');

// === ENTERABLE BUILDINGS ===
function makeEnterable(x,z,type,name){
enterableBuildings.push({x,z,type,name,r:8});
// Door marker (glowing)
const doorGlow=new THREE.Mesh(new THREE.BoxGeometry(2.5,4,.1),new MS({color:0xffcc44,emissive:0xffaa22,emissiveIntensity:1.5,transparent:true,opacity:.4}));
doorGlow.position.set(x,meshTerrainH(x,z)+2.5,z);scene.add(doorGlow)}

// Make key buildings enterable
makeEnterable(40,30,'house','Lumbridge House');makeEnterable(60,15,'shop','Lumbridge Shop');
makeEnterable(500,70,'tavern','Blue Moon Inn');makeEnterable(550,30,'shop','Varrock Sword Shop');
makeEnterable(-520,270,'house','Falador Manor');makeEnterable(-480,300,'shop','Falador General Store');
makeEnterable(-1260,80,'shop','Ardougne Market');makeEnterable(-1200,120,'tavern','Flying Horse Inn');
makeEnterable(560,380,'shop','Al Kharid Gem Stall');makeEnterable(-320,-160,'house','Draynor Manor');

// Check dungeon/building entry in game loop
checkInteractions=function(){
const px=player.x,pz=player.z;
// Dungeon entry
if(!inDungeon){for(const d of dungeons){if(Math.hypot(px-d.x,pz-d.z)<12){
log('Press E to enter dungeon (Depth '+d.depth+')','#ff0');
if(keys['KeyE']){enterDungeon(d);break}}}}
else{// Check if at entrance room
const rm0=inDungeon.rooms[0];
if(Math.hypot(px-rm0.x,pz-rm0.z)<8&&keys['KeyE'])exitDungeon();
// Check boss room for loot
const bossRoom=inDungeon.rooms[inDungeon.rooms.length-1];
if(Math.hypot(px-bossRoom.x,pz-bossRoom.z)<6){
const bossAlive=enemies.some(e=>e.type===inDungeon.bossType&&Math.hypot(e.x-bossRoom.x,e.z-bossRoom.z)<20);
if(!bossAlive){log('Boss defeated! Press E to loot chest','#ff0');
if(keys['KeyE']){const loot=specialLoot[Math.floor(Math.random()*specialLoot.length)];
log('★ Found: '+loot.name+' ('+loot.rarity+') ATK:'+loot.atk+' DEF:'+loot.def+' STR:'+loot.str,'#ffd700');
if(loot.atk>equipped[loot.slot].atk||loot.def>equipped[loot.slot].def){equipped[loot.slot]={name:loot.name,atk:loot.atk,def:loot.def,str:loot.str};log('Equipped '+loot.name+' to '+loot.slot+'!','#0f0')}
else{log('Added to inventory','#aaa')}
exitDungeon()}}}}
// Building entry
for(const b of enterableBuildings){if(Math.hypot(px-b.x,pz-b.z)<b.r){
log('Press E to enter '+b.name,'#ff0');break}}};

console.log('INIT: dungeons done, spawning enemies');
// === SPAWN ENEMIES PER REGION ===
regions.forEach(rg=>{rg.en.forEach(et=>{const cnt=Math.max(2,Math.round(rg.r/80));for(let i=0;i<cnt;i++){const ex=rg.x+(Math.random()-.5)*rg.r*1.4,ez=rg.z+(Math.random()-.5)*rg.r*1.4;spawnE(et,ex,ez,rg.lv)}})});

// === DYNAMIC LIGHT POOL (only 8 active PointLights) ===
for(let i=0;i<MAX_LIGHTS;i++){const l=new THREE.PointLight(0xff8833,0,60,1.5);scene.add(l);lightPool.push(l)}

// Atmospheric ash/ember motes (dense)
const dGeo=new THREE.BufferGeometry();const dN=2000,dP=new Float32Array(dN*3);
for(let i=0;i<dN;i++){dP[i*3]=(Math.random()-.5)*1200;dP[i*3+1]=Math.random()*60+1;dP[i*3+2]=(Math.random()-.5)*1200}
dGeo.setAttribute('position',new THREE.BufferAttribute(dP,3));
dustPts=new THREE.Points(dGeo,new THREE.PointsMaterial({color:0xccaa66,size:.5,transparent:true,opacity:.25,depthWrite:false,blending:THREE.AdditiveBlending}));scene.add(dustPts);
// Ember particles
const embGeo=new THREE.BufferGeometry();const embN=500,embP=new Float32Array(embN*3);
for(let i=0;i<embN;i++){embP[i*3]=(Math.random()-.5)*600;embP[i*3+1]=Math.random()*40+1;embP[i*3+2]=(Math.random()-.5)*600}
embGeo.setAttribute('position',new THREE.BufferAttribute(embP,3));
const embers=new THREE.Points(embGeo,new THREE.PointsMaterial({color:0xff6633,size:.4,transparent:true,opacity:.2,depthWrite:false,blending:THREE.AdditiveBlending}));scene.add(embers);
// Firefly/pollen floating light particles
const ffGeo=new THREE.BufferGeometry();const ffN=300,ffP=new Float32Array(ffN*3);
for(let i=0;i<ffN;i++){ffP[i*3]=(Math.random()-.5)*800;ffP[i*3+1]=2+Math.random()*20;ffP[i*3+2]=(Math.random()-.5)*800}
ffGeo.setAttribute('position',new THREE.BufferAttribute(ffP,3));
const fireflies=new THREE.Points(ffGeo,new THREE.PointsMaterial({color:0xeedd66,size:.6,transparent:true,opacity:.35,depthWrite:false,blending:THREE.AdditiveBlending}));scene.add(fireflies);

composer=new EffectComposer(renderer);composer.addPass(new RenderPass(scene,cam));
// Bloom at half res for glow effects (affordable now with reduced draw calls)
const bloomPass=new UnrealBloomPass(new THREE.Vector2(innerWidth,innerHeight),0.55,0.5,0.78);composer.addPass(bloomPass);
const dsGrade=new ShaderPass(DSColorGradeShader);composer.addPass(dsGrade);
window.addEventListener('resize',()=>{cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);composer.setSize(innerWidth,innerHeight)});
initTargetRing();scene.add(targetRing);
buildColliders();
log('World loaded: '+torchPositions.length+' lights, '+enemies.length+' enemies, '+solidBoxes.length+' colliders','#0f0');
console.log('INIT COMPLETE: scene children='+scene.children.length+', enemies='+enemies.length);

// === GPU PERFORMANCE: Distance culling system ===
const CULL_DIST=600;const CULL_DIST_SQ=CULL_DIST*CULL_DIST;
const noCull=new Set();
scene.traverse(c=>{
if(c===ground||c===riverMesh||c===dustPts||c===playerGroup||c.isLight||c.isPoints||c.isInstancedMesh)noCull.add(c);
if(c.parent&&noCull.has(c.parent))noCull.add(c);
});
scene.children.forEach(c=>{if(c.geometry&&c.geometry.type==='SphereGeometry'&&c.geometry.parameters.radius>=4000)noCull.add(c)});

distanceCull=function(){
const px=player.x,pz=player.z;
scene.children.forEach(c=>{
if(noCull.has(c)||c===playerGroup)return;
if(!c.position)return;
const dx=c.position.x-px,dz=c.position.z-pz;
c.visible=(dx*dx+dz*dz)<CULL_DIST_SQ;
});};
shadowCull=function(){
const px=player.x,pz=player.z;const SD=CULL_DIST_SQ;
scene.traverse(c=>{if(c.isMesh&&c.castShadow){const dx=c.position.x-px,dz=c.position.z-pz;
if(dx*dx+dz*dz>SD)c.castShadow=false;else c.castShadow=true}});};
}

// === GEAR SYSTEM ===
const gear={atk:10,def:5,str:8,name:'Starter'};
const gearSlots=['Helm','Chest','Legs','Weapon','Shield','Boots','Gloves','Ring'];
const equipped={};gearSlots.forEach(s=>equipped[s]={name:'None',atk:1,def:1,str:1});
equipped.Weapon={name:'Starter Sword',atk:10,def:0,str:5};equipped.Shield={name:'Starter Shield',atk:0,def:5,str:0};
function totalGear(){let a=0,d=0,s=0;gearSlots.forEach(sl=>{a+=equipped[sl].atk;d+=equipped[sl].def;s+=equipped[sl].str});return{atk:a,def:d,str:s}}

function buildEnemy(type,lv){
const g=new THREE.Group();const col=eCol[type]||0x888888;const mat=new MS({color:col,roughness:.7});const matD=new MS({color:col,roughness:.55,metalness:.2});const matLt=new MS({color:col,roughness:.6,metalness:.1});
const sc=.4+lv*.006;
const isArmored=type==='guard'||type==='whiteknight'||type==='knight'||type==='warrior'||type==='barbarian';
const isUndead=type==='skeleton'||type==='zombie'||type==='ghost'||type==='shade'||type==='revenant';
const isBeast=type==='wolf'||type==='bear'||type==='spider'||type==='snake'||type==='bat'||type==='cow'||type==='chicken'||type==='rat'||type==='lizard'||type==='scarab';
const isDemon=type==='demon'||type==='hellhound'||type==='tzhaar'||type==='elemental';
// === TORSO ===
if(isBeast){
const torso=new THREE.Mesh(new THREE.SphereGeometry(2,10,8),mat);torso.position.y=3.5;torso.scale.set(1,.8,1.4);torso.castShadow=true;g.add(torso);
// Fur tufts
for(let i=0;i<8;i++){const tuft=new THREE.Mesh(new THREE.ConeGeometry(.3,.8,4),matD);tuft.position.set((Math.random()-.5)*2.5,3+Math.random()*2,(Math.random()-.5)*2);tuft.rotation.set(Math.random(),Math.random(),Math.random());g.add(tuft)}
} else {
const torso=new THREE.Mesh(new THREE.CylinderGeometry(1.3,1.6,5.5,10),mat);torso.position.y=4.5;torso.castShadow=true;g.add(torso);
// Chest detail
if(isArmored){
const chest=new THREE.Mesh(new THREE.BoxGeometry(2.8,3,.3),matD);chest.position.set(0,5,1.1);chest.castShadow=true;g.add(chest);
const ridge=new THREE.Mesh(new THREE.BoxGeometry(.2,2.5,.35),matLt);ridge.position.set(0,5,1.25);g.add(ridge);
// Shoulder guards
[-1,1].forEach(s=>{const pad=new THREE.Mesh(new THREE.SphereGeometry(.8,8,6),matD);pad.position.set(s*1.8,7,.2);pad.scale.set(1.2,.7,1);pad.castShadow=true;g.add(pad);
const rim=new THREE.Mesh(new THREE.BoxGeometry(1.2,.15,.8),matLt);rim.position.set(s*1.8,6.6,.2);g.add(rim)});
// Belt
const belt=new THREE.Mesh(new THREE.BoxGeometry(3.2,.4,2.2),new MS({color:0x4a3a20,roughness:.85}));belt.position.y=2.2;g.add(belt);
const buckle=new THREE.Mesh(new THREE.BoxGeometry(.4,.3,.25),new MS({color:0xc8a050,roughness:.4,metalness:.7}));buckle.position.set(0,2.2,1.15);g.add(buckle);
} else if(isDemon){
// Demon spikes
for(let i=0;i<6;i++){const spike=new THREE.Mesh(new THREE.ConeGeometry(.25,1.5,4),matD);spike.position.set((Math.random()-.5)*2,4+Math.random()*3,(Math.random()-.5)*2);spike.rotation.set(Math.random()-.5,0,Math.random()-.5);g.add(spike)}
}}
// === HEAD ===
if(isBeast){
const head=new THREE.Mesh(new THREE.SphereGeometry(1,8,8),matD);head.position.set(0,4.5,2.5);head.scale.set(1,.8,1.2);head.castShadow=true;g.add(head);
// Snout/muzzle
const snout=new THREE.Mesh(new THREE.BoxGeometry(.8,.5,1),mat);snout.position.set(0,4.2,3.5);g.add(snout);
// Ears
[-1,1].forEach(s=>{const ear=new THREE.Mesh(new THREE.ConeGeometry(.3,.6,4),matD);ear.position.set(s*.6,5.3,2.3);g.add(ear)});
} else {
const headG=type==='skeleton'?new THREE.BoxGeometry(1.8,2,1.8):isDemon?new THREE.SphereGeometry(1.4,10,10):new THREE.SphereGeometry(1.2,10,10);
const head=new THREE.Mesh(headG,matD);head.position.y=8;head.castShadow=true;g.add(head);
if(isArmored){
// Helm
const helm=new THREE.Mesh(new THREE.SphereGeometry(1.4,8,8),matD);helm.position.y=8.2;helm.scale.set(1,1.1,.95);g.add(helm);
// Visor
const visor=new THREE.Mesh(new THREE.BoxGeometry(1.6,.1,.25),new MS({color:0x080808,roughness:1}));visor.position.set(0,8,1.3);g.add(visor);
// Nose guard
const nose=new THREE.Mesh(new THREE.BoxGeometry(.15,1.2,.2),matLt);nose.position.set(0,8,1.35);g.add(nose);
} else if(isDemon){
// Horns
[-1,1].forEach(s=>{const horn=new THREE.Mesh(new THREE.ConeGeometry(.3,2.5,5),new MS({color:0x2a1a0a,roughness:.7,metalness:.3}));horn.position.set(s*.8,9.5,-.3);horn.rotation.z=s*.3;horn.rotation.x=-.2;horn.castShadow=true;g.add(horn)});
} else if(type==='skeleton'){
// Jaw
const jaw=new THREE.Mesh(new THREE.BoxGeometry(1.2,.4,1),matLt);jaw.position.set(0,7,0);g.add(jaw);
}}
// === EYES ===
const eyeCol=isDemon?0xff2200:isUndead?0x00ff88:type==='ghost'?0x88ccff:type==='tzhaar'?0xff8800:0xff4444;
const eyeEmit=isDemon?0xff0000:isUndead?0x00aa55:0xff4444;
const eyeM=new MS({color:eyeCol,emissive:eyeEmit,emissiveIntensity:2});
if(!isBeast){
[-0.4,0.4].forEach(ex=>{const eye=new THREE.Mesh(new THREE.SphereGeometry(.22,6,6),eyeM);eye.position.set(ex,8.3,1.1);g.add(eye)});
} else {
[-0.35,0.35].forEach(ex=>{const eye=new THREE.Mesh(new THREE.SphereGeometry(.18,5,5),eyeM);eye.position.set(ex,4.8,3.2);g.add(eye)});
}
// === ARMS ===
if(!isBeast){
[-1,1].forEach(s=>{
const armGrp=new THREE.Group();armGrp.position.set(s*2,7,0);
const upperArm=new THREE.Mesh(new THREE.CylinderGeometry(.4,.35,2.8,6),mat);upperArm.position.y=-1.5;upperArm.castShadow=true;armGrp.add(upperArm);
const elbow=new THREE.Mesh(new THREE.SphereGeometry(.35,6,6),matD);elbow.position.y=-3;armGrp.add(elbow);
const forearm=new THREE.Mesh(new THREE.CylinderGeometry(.35,.3,2.5,6),mat);forearm.position.y=-4.2;forearm.castShadow=true;armGrp.add(forearm);
const hand=new THREE.Mesh(new THREE.BoxGeometry(.5,.3,.6),matD);hand.position.y=-5.5;armGrp.add(hand);
if(isArmored){
const brace=new THREE.Mesh(new THREE.CylinderGeometry(.42,.38,.8,6),matD);brace.position.y=-3.5;armGrp.add(brace)}
g.add(armGrp);
if(s===1)g.userData.rArm=armGrp;
});
} else {
// Beast legs (4 legs)
[[-1,1.5],[1,1.5],[-1,-1.5],[1,-1.5]].forEach(([sx,sz])=>{
const leg=new THREE.Mesh(new THREE.CylinderGeometry(.3,.25,3,5),mat);leg.position.set(sx,1.5,sz);leg.castShadow=true;g.add(leg);
const paw=new THREE.Mesh(new THREE.SphereGeometry(.3,5,5),matD);paw.position.set(sx,0,sz);g.add(paw)});
}
// === LEGS (humanoids) ===
if(!isBeast){
[-1,1].forEach(s=>{
const thigh=new THREE.Mesh(new THREE.CylinderGeometry(.45,.4,2.5,6),mat);thigh.position.set(s*.65,1.8,0);thigh.castShadow=true;g.add(thigh);
const knee=new THREE.Mesh(new THREE.SphereGeometry(.38,6,6),matD);knee.position.set(s*.65,.5,0);g.add(knee);
const shin=new THREE.Mesh(new THREE.CylinderGeometry(.38,.32,2.2,6),mat);shin.position.set(s*.65,-.6,0);shin.castShadow=true;g.add(shin);
const boot=new THREE.Mesh(new THREE.BoxGeometry(.7,.5,1.2),matD);boot.position.set(s*.65,-1.8,.1);g.add(boot);
if(isArmored){
const greave=new THREE.Mesh(new THREE.BoxGeometry(.4,1.8,.2),matLt);greave.position.set(s*.65,-.6,.4);g.add(greave);
const kneePad=new THREE.Mesh(new THREE.BoxGeometry(.4,.4,.3),matD);kneePad.position.set(s*.65,.5,.35);g.add(kneePad)}
});}
// === WEAPONS (per type) ===
if(type==='demon'||type==='revenant'||type==='whiteknight'||type==='guard'||type==='knight'){
// Sword with crossguard
const blade=new THREE.Mesh(new THREE.BoxGeometry(.15,.12,5.5),new MS({color:0xbbbbdd,roughness:.1,metalness:.95}));blade.position.set(2,2,2.5);blade.rotation.x=.15;g.add(blade);
const xguard=new THREE.Mesh(new THREE.BoxGeometry(1,.15,.15),new MS({color:0x5a4020,roughness:.6,metalness:.4}));xguard.position.set(2,2,.1);g.add(xguard);
const hilt=new THREE.Mesh(new THREE.CylinderGeometry(.08,.08,.9,5),new MS({color:0x4a3018,roughness:.8}));hilt.position.set(2,2,-.3);hilt.rotation.x=Math.PI/2;g.add(hilt);
// Shield for knights/guards
if(type==='whiteknight'||type==='guard'||type==='knight'){
const sh=new THREE.Mesh(new THREE.BoxGeometry(.25,3,2),matD);sh.position.set(-2,3.5,.5);g.add(sh);
const shBoss=new THREE.Mesh(new THREE.SphereGeometry(.3,6,6),new MS({color:0xc8a050,roughness:.4,metalness:.7}));shBoss.position.set(-2.2,3.5,.5);g.add(shBoss);
const shRim=new THREE.Mesh(new THREE.BoxGeometry(.26,.2,2.1),matLt);shRim.position.set(-2,4.9,.5);g.add(shRim)}}
if(type==='barbarian'||type==='pirate'||type==='warrior'||type==='troll'||type==='ogre'){
// Axe with handle
const handle=new THREE.Mesh(new THREE.CylinderGeometry(.1,.12,4.5,4),new MS({color:0x5a4530,roughness:.9}));handle.position.set(2,3.5,.5);handle.rotation.x=.3;g.add(handle);
const axeH=new THREE.Mesh(new THREE.BoxGeometry(.9,1.8,.15),new MS({color:0x888899,roughness:.25,metalness:.85}));axeH.position.set(2,5.5,1.2);g.add(axeH)}
if(type==='mage'||type==='darkwiz'||type==='cultist'||type==='elf'){
// Staff with orb
const staff=new THREE.Mesh(new THREE.CylinderGeometry(.08,.1,6,5),new MS({color:0x4a3828,roughness:.9}));staff.position.set(1.8,4.5,0);staff.castShadow=true;g.add(staff);
const orb=new THREE.Mesh(new THREE.SphereGeometry(.4,8,8),new MS({color:type==='darkwiz'?0x6a1a8a:0x2a6a8a,emissive:type==='darkwiz'?0x4a0a6a:0x1a4a6a,emissiveIntensity:2,roughness:.2,metalness:.5}));orb.position.set(1.8,7.8,0);g.add(orb)}
if(type==='spider'){
// Extra legs
for(let i=0;i<4;i++){[-1,1].forEach(s=>{const sleg=new THREE.Mesh(new THREE.CylinderGeometry(.1,.08,3,4),matD);sleg.position.set(s*1.5,2.5,-1+i*.8);sleg.rotation.z=s*.8;sleg.rotation.x=(i-.5)*.2;g.add(sleg)})}}
// === TAIL for beasts ===
if(type==='wolf'||type==='bear'||type==='lizard'||type==='hellhound'){
const tail=new THREE.Mesh(new THREE.CylinderGeometry(.15,.08,2.5,4),mat);tail.position.set(0,3,-3);tail.rotation.x=-.5;g.add(tail)}
// === WINGS for bat/demon ===
if(type==='bat'||type==='demon'){
[-1,1].forEach(s=>{const wing=new THREE.Mesh(new THREE.PlaneGeometry(3,2.5),new MS({color:col,roughness:.8,side:THREE.DoubleSide,transparent:true,opacity:.7}));wing.position.set(s*2.5,5.5,-.5);wing.rotation.y=s*.4;g.add(wing)})}
// === GHOST transparency ===
if(type==='ghost'||type==='shade'){
g.traverse(c=>{if(c.isMesh&&c.material){c.material=c.material.clone();c.material.transparent=true;c.material.opacity=.5}})}
// HP bar above head
const barY=isBeast?6:10.5;
const barBg=new THREE.Mesh(new THREE.PlaneGeometry(3,.35),new MS({color:0x220000,side:THREE.DoubleSide}));barBg.position.y=barY;g.add(barBg);
const barFg=new THREE.Mesh(new THREE.PlaneGeometry(3,.3),new MS({color:0x00cc00,side:THREE.DoubleSide}));barFg.position.y=barY;barFg.position.z=.01;g.add(barFg);
g.userData.hpBar=barFg;
g.scale.setScalar(sc);
return g;
}

// Enemy attack styles: determines range, speed, telegraph, and animation
const eAtkStyles={
guard:'slash',whiteknight:'slash',knight:'slash',warrior:'slash',barbarian:'chop',pirate:'chop',
skeleton:'slash',zombie:'smash',ghost:'magic',shade:'magic',revenant:'magic',
wolf:'bite',bear:'swipe',spider:'bite',snake:'bite',bat:'bite',cow:'charge',chicken:'peck',rat:'bite',lizard:'bite',scarab:'bite',
demon:'smash',hellhound:'bite',tzhaar:'smash',elemental:'magic',
mage:'magic',darkwiz:'magic',cultist:'magic',elf:'magic',
troll:'smash',ogre:'smash',dragon:'breath',hydra:'breath',cerberus:'bite',vorkath:'breath',nightmare:'magic',nex:'magic',jad:'magic',zuk:'breath',kraken:'smash'
};
const eAtkRange={slash:10,chop:11,smash:12,bite:8,swipe:10,charge:14,peck:6,magic:28,breath:22};
function spawnE(type,x,z,lv){const hp=eHP[type]||40;const mesh=buildEnemy(type,lv||1);
const style=eAtkStyles[type]||'slash';const range=eAtkRange[style]||10;
const e={mesh,hp,maxHp:hp,poi:30,x,z,type,lv:lv||1,atkCD:0,aggro:50+(lv||1)*2,dmg:Math.max(5,8+(lv||1)*2),
atkStyle:style,atkRange:range,windUp:0,swingT:0,strafeAng:Math.random()*Math.PI*2,strafeCW:Math.random()>.5?1:-1};
const h=meshTerrainH(x,z);e.mesh.position.set(x,h,z);scene.add(e.mesh);enemies.push(e)}

function calcHit(a,d){const g=totalGear();const ab=a===player?40+g.atk:22+((a.lv||1)*1.5);const db=d===player?30+g.def:15;return Math.random()<Math.max(.08,Math.min(.94,(ab/(db+12))*.82))}

function spawnLoot(x,z,e){
// Always drop gear that is 1% better than current best in a random slot
const slot=gearSlots[Math.floor(Math.random()*gearSlots.length)];
const cur=equipped[slot];const boost=1.01;
const newItem={name:e.type+' '+slot+' Lv'+(e.lv||1),atk:Math.ceil(Math.max(cur.atk*boost,cur.atk+1)),def:Math.ceil(Math.max(cur.def*boost,cur.def+1)),str:Math.ceil(Math.max(cur.str*boost,cur.str+1)),slot};
const c=0xffdd44;const m=new THREE.Mesh(new THREE.BoxGeometry(2.5,2.5,2.5),new MS({color:c,emissive:c,emissiveIntensity:.6,roughness:.3,metalness:.3}));
m.position.set(x,meshTerrainH(x,z)+4,z);m.userData={vx:(Math.random()-.5)*5,vz:(Math.random()-.5)*5,vy:8,life:900,item:newItem.name,gear:newItem};scene.add(m);lootArr.push(m);
// Also drop bones/coins
const c2=0xccccaa;const m2=new THREE.Mesh(new THREE.BoxGeometry(1.5,1.5,1.5),new MS({color:c2,emissive:c2,emissiveIntensity:.2,roughness:.6}));
m2.position.set(x+2,meshTerrainH(x,z)+4,z+2);m2.userData={vx:(Math.random()-.5)*4,vz:(Math.random()-.5)*4,vy:7,life:600,item:'Bones'};scene.add(m2);lootArr.push(m2);
}
function hitFX(x,y,z,col=0xff4400){for(let i=0;i<25;i++){const p=new THREE.Mesh(new THREE.SphereGeometry(.3,4,4),new MS({color:col,emissive:col,emissiveIntensity:1.5,roughness:1}));p.position.set(x,y,z);p.userData={vx:(Math.random()-.5)*10,vy:(Math.random()-.5)*10+4,vz:(Math.random()-.5)*10,life:22};scene.add(p);particles.push(p)}}
function cycleLock(){if(!enemies.length)return;lockIdx=(lockIdx+1)%enemies.length;lockOn=enemies[lockIdx];log('Locked on: '+lockOn.type,'#cc4')}
function parry(){player.blocking=true;if(lockOn){const d=Math.hypot(lockOn.mesh.position.x-player.x,lockOn.mesh.position.z-player.z);if(d<18){hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+6,lockOn.mesh.position.z,0x00ffff);lockOn.hp-=12;player.sta=Math.min(player.sta+28,player.maxSta);skills.Defence.xp+=8;log('PARRY RIPOSTE!','#0ff')}}}

let gpIndex=-1;
// Dark Souls-style gamepad mapping (customizable)
// Maps action names to gamepad button indices. Standard: A=0 B=1 X=2 Y=3 LB=4 RB=5 LT=6 RT=7 Back=8 Start=9 LSClick=10 RSClick=11 DUp=12 DDown=13 DLeft=14 DRight=15
const gpMap={
roll:1,     // B/Circle = Roll (Dark Souls default)
attack:7,   // RT = Light Attack
parry:5,    // RB = Parry/Heavy Attack
block:6,    // LT = Block/Guard
lockon:10,  // LS Click = Lock-on (DS3 style)
heal:0,     // A/Cross = Heal (Estus)
useItem:2,  // X/Square = Use item
twoHand:3,  // Y/Triangle = Two-hand toggle
inventory:9,// Start = Inventory/Menu
skills:8,   // Back/Select = Skills
dUp:12,dDown:13,dLeft:14,dRight:15
};
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
// Read raw buttons, map through gpMap
const isP=idx=>gp.buttons[idx]?.pressed;const isV=idx=>(gp.buttons[idx]?.value||0)>.3;
gpButtons.a=isP(gpMap.heal);gpButtons.x=isP(gpMap.useItem);
gpButtons.b=isP(gpMap.roll);gpButtons.y=isP(gpMap.twoHand);
gpButtons.lb=isV(gpMap.block);gpButtons.rb=isP(gpMap.parry);
gpButtons.lt=isV(gpMap.block);gpButtons.rt=isV(gpMap.attack);
gpButtons.start=isP(gpMap.inventory);gpButtons.back=isP(gpMap.skills);
gpButtons.dUp=isP(gpMap.dUp);gpButtons.dDown=isP(gpMap.dDown);
gpButtons.dLeft=isP(gpMap.dLeft);gpButtons.dRight=isP(gpMap.dRight);
// Lock-on via mapped button
if(isP(gpMap.lockon)&&!player._lkCD){cycleLock();player._lkCD=20}
if(player._lkCD)player._lkCD--;
}

function loop(){
requestAnimationFrame(loop);time+=.016;pollGamepad();
if(player.dead){player.deadTimer-=.016;if(player.deadTimer<=0){player.dead=false;player.hp=player.maxHp;player.sta=player.maxSta;player.x=0;player.z=5;player.y=meshTerrainH(0,5);document.getElementById('death-overlay').classList.remove('active');log('Respawned at bonfire','#cc4')}composer.render();return}

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

player.y=inDungeon?-inDungeon.depth*50+2:surfaceH(player.x,player.z,player.y);
const curReg=getReg(player.x,player.z);
const totalLv=skillDefs.reduce((a,s)=>a+skills[s].lvl,0);
document.getElementById('locbar').textContent=(inDungeon?'⚔ Dungeon Depth '+inDungeon.depth+' — ':'')+curReg.n+' · Zone Lv '+curReg.lv+'+';
if(!inDungeon){const fogC=new THREE.Color(curReg.fog);const skyC=new THREE.Color(0xaaccee);fogC.lerp(skyC,.5);scene.fog.color.copy(fogC);scene.background.copy(skyC)}
else{scene.fog.color.set(0x0a0a0a);scene.background.set(0x050505)}
if(checkInteractions)checkInteractions();

// Animate doors: open when player is near, close when far
for(let di=0;di<doors.length;di++){const d=doors[di];
const dd=Math.hypot(player.x-d.x,player.z-d.z);
const tgt=dd<18?d.openAng:0;
d.cur+=(tgt-d.cur)*.08;
if(Math.abs(d.cur)<.01)d.cur=0;
d.pivot.rotation.y=d.cur}

// GPU perf: distance cull every 4 frames, shadow cull every 20, sun follows player
cullFrame++;
if(cullFrame%4===0&&distanceCull)distanceCull();
if(cullFrame%20===0&&shadowCull)shadowCull();
{
// Move sun shadow camera to follow player for tight shadow coverage
if(!window._sunRef)window._sunRef=scene.children.find(c=>c.isDirectionalLight&&c.castShadow);
if(window._sunRef){window._sunRef.position.set(player.x+200,350,player.z-100);window._sunRef.target.position.set(player.x,player.y,player.z);window._sunRef.target.updateMatrixWorld()}}

if(keys['q'])player.sta=Math.min(player.sta+5,player.maxSta);
else player.sta=Math.min(player.sta+1,player.maxSta);
// Heal with A/Cross or key 3
if((keys['3']||gpButtons.a)&&!player._healCD&&player.hp<player.maxHp){player.hp=Math.min(player.hp+40,player.maxHp);player._healCD=60;log('Healed with Estus Flask','#4c4');hitFX(player.x,player.y+6,player.z,0x44cc44)}
if(player._healCD)player._healCD--;

if((keys[' ']||gpButtons.b)&&!player.rolling&&player.sta>24){player.rolling=true;player.rollT=22;player.sta-=24;skills.Agility.xp+=2}
if(mouse.right||gpButtons.lt||gpButtons.lb){parry()}else{player.blocking=false}
// Gamepad: RB=parry riposte
if(gpButtons.rb&&!player._rbCD){parry();player._rbCD=12}
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
const faceAng=Math.atan2(dx,dz);
if(dist<e.aggro){
const isMelee=e.atkStyle==='slash'||e.atkStyle==='chop'||e.atkStyle==='smash'||e.atkStyle==='bite'||e.atkStyle==='swipe'||e.atkStyle==='charge'||e.atkStyle==='peck';
const stopDist=isMelee?e.atkRange*.7:e.atkRange*.85;
// Movement: approach until in range, then circle-strafe
if(dist>stopDist&&e.swingT<=0){
const a=Math.atan2(dz,dx);const spd=e.atkStyle==='charge'&&e.windUp>15?.6:.2;
e.mesh.position.x+=Math.cos(a)*spd;e.mesh.position.z+=Math.sin(a)*spd;
} else if(dist<stopDist*1.3&&e.swingT<=0&&isMelee){
// Circle-strafe when in range and not attacking
e.strafeAng+=.015*e.strafeCW;
const sx=Math.cos(e.strafeAng)*.12,sz=Math.sin(e.strafeAng)*.12;
e.mesh.position.x+=sx;e.mesh.position.z+=sz;
}
const eco=pushOut(e.mesh.position.x,e.mesh.position.y,e.mesh.position.z);e.mesh.position.x=eco.x;e.mesh.position.z=eco.z;
const eh=surfaceH(e.mesh.position.x,e.mesh.position.z,e.mesh.position.y);e.mesh.position.y=eh+Math.sin(time*2+i)*.15;
e.mesh.rotation.y=faceAng;
// Attack logic: wind-up → swing → damage → cooldown
if(dist<e.atkRange&&e.atkCD<=0&&e.swingT<=0){
// Start wind-up
e.windUp++;
// Visual telegraph: lean back during windup
if(e.mesh.userData.rArm&&e.windUp<18){e.mesh.userData.rArm.rotation.x=-e.windUp*.12}
const windUpTime=e.atkStyle==='magic'||e.atkStyle==='breath'?24:e.atkStyle==='smash'?20:e.atkStyle==='charge'?28:15;
if(e.windUp>=windUpTime){
// Execute attack
e.swingT=12;e.windUp=0;e.atkCD=36+Math.floor(Math.random()*16);
// Ranged: spawn projectile
if(e.atkStyle==='magic'||e.atkStyle==='breath'){
const pc=e.atkStyle==='magic'?0x6a1aaa:0xff4400;const pe=e.atkStyle==='magic'?0x4a0a8a:0xff2200;
const proj=new THREE.Mesh(new THREE.SphereGeometry(e.atkStyle==='breath'?1.2:.7,6,6),new MS({color:pc,emissive:pe,emissiveIntensity:3,transparent:true,opacity:.8}));
proj.position.copy(e.mesh.position);proj.position.y+=6;
const pAng=Math.atan2(player.z-e.mesh.position.z,player.x-e.mesh.position.x);
proj.userData={vx:Math.cos(pAng)*1.2,vz:Math.sin(pAng)*1.2,life:80,dmg:e.dmg,owner:e};
scene.add(proj);particles.push(proj);
} else {
// Melee: damage if still in range
if(dist<e.atkRange*1.15){
if(calcHit(e,player)){const gd=totalGear();let blockMult=player.blocking?.65:.3;const blocked=Math.floor(gd.def*blockMult);const realDmg=Math.max(1,e.dmg-blocked);
player.hp-=realDmg;
if(player.blocking){player.sta-=8;skills.Defence.xp+=4;hitFX(player.x,player.y+8,player.z,0x4488ff);log(`BLOCKED ${e.type}! -${realDmg} (absorbed ${blocked})`,'#48f')}
else{hitFX(player.x,player.y+8,player.z);log(`${e.type} hit for ${realDmg} (blocked ${blocked})`,'#f44')}}}}
}} else {e.windUp=Math.max(0,e.windUp-1)}
// Swing animation
if(e.swingT>0){e.swingT--;
if(e.mesh.userData.rArm){const pct=e.swingT/12;e.mesh.userData.rArm.rotation.x=(-1.5+pct*3)*Math.max(0,1-pct);e.mesh.userData.rArm.rotation.z=-.4*(1-pct)}}
else if(e.mesh.userData.rArm&&e.windUp<=0){e.mesh.userData.rArm.rotation.x*=.85;e.mesh.userData.rArm.rotation.z*=.85}
}
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
const lh=meshTerrainH(l.position.x,l.position.z)+1.5;if(l.position.y<lh){l.position.y=lh;l.userData.vy*=-.4}
if(l.userData.life<=0){scene.remove(l);lootArr.splice(i,1);continue}
if(Math.hypot(l.position.x-player.x,l.position.z-player.z)<9){
if(l.userData.gear){const g=l.userData.gear;equipped[g.slot]=g;updateEqUI();log('EQUIPPED: '+g.name+' [ATK+'+g.atk+' DEF+'+g.def+' STR+'+g.str+']','#0ff')}
if(inventory.length<28){inventory.push(l.userData.item);updateInvUI();log('Picked up: '+l.userData.item,'#ff4');
// Auto-grant skill XP for skill items
const si=skillItems[l.userData.item];if(si){skills[si.skill].xp+=si.xp;
const lv=Math.max(skills[si.skill].lvl,Math.floor(1+Math.sqrt(skills[si.skill].xp/50)));
if(lv>skills[si.skill].lvl){skills[si.skill].lvl=lv;log(si.skill+' level up! Now '+lv,'#ff0')}
log(si.skill+' +'+si.xp+'xp','#cc4');updateSkillUI()}}else log('Inventory full!','#f44');
scene.remove(l);lootArr.splice(i,1)}}

for(let i=particles.length-1;i>=0;i--){let p=particles[i];
// Enemy projectiles move straight (no gravity) and check player hit
if(p.userData.dmg){p.position.x+=p.userData.vx;p.position.z+=p.userData.vz;p.userData.life--;
const pd=Math.hypot(p.position.x-player.x,p.position.z-player.z);
if(pd<4&&!player.rolling){const gd=totalGear();let blockMult=player.blocking?.65:.3;const blocked=Math.floor(gd.def*blockMult);const realDmg=Math.max(1,p.userData.dmg-blocked);
player.hp-=realDmg;hitFX(player.x,player.y+8,player.z,0x8844ff);
if(player.blocking)log(`BLOCKED projectile! -${realDmg}`,'#48f');else log(`Hit by projectile! -${realDmg}`,'#f44');
p.userData.life=0}
if(p.userData.life<=0){scene.remove(p);particles.splice(i,1)}}
else{p.position.x+=p.userData.vx*.14;p.position.y+=p.userData.vy*.14;p.position.z+=p.userData.vz*.14;p.userData.vy-=.5;p.userData.life--;p.scale.setScalar(Math.max(0,p.userData.life/22));if(p.userData.life<=0){scene.remove(p);particles.splice(i,1)}}}

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
// Player frame
const cLv=Math.floor((skills.Attack.lvl+skills.Strength.lvl+skills.Defence.lvl+skills.Hitpoints.lvl+skills.Prayer.lvl+skills.Magic.lvl+skills.Ranged.lvl)/4);
const pfLv=document.getElementById('pf-level');if(pfLv)pfLv.textContent='Lv '+cLv;
// XP bar (next combat level progress)
const totalCmbXp=skills.Attack.xp+skills.Strength.xp+skills.Defence.xp+skills.Hitpoints.xp;
const xpFill=document.getElementById('xp-bar-fill');const xpText=document.getElementById('xp-bar-text');
if(xpFill){const nxt=Math.pow((cLv+1)*4-skills.Prayer.lvl-skills.Magic.lvl-skills.Ranged.lvl,2)*50;const cur=Math.pow(cLv*4-skills.Prayer.lvl-skills.Magic.lvl-skills.Ranged.lvl,2)*50;const pct=Math.min(100,Math.max(0,(totalCmbXp-cur)/(Math.max(1,nxt-cur))*100));xpFill.style.width=pct+'%'}
if(xpText)xpText.textContent='Combat XP: '+totalCmbXp+' \u00B7 Combat Lv '+cLv;
// Action bar cooldowns
const abSlots=document.querySelectorAll('.ab-slot');
abSlots.forEach(s=>{const a=s.dataset.action;let cd=false;
if(a==='attack')cd=player.atkCD>0;
else if(a==='heal')cd=player._estusCD>0;
else if(a==='parry')cd=player._parryCD>0;
else if(a==='roll')cd=player.rolling;
if(cd)s.classList.add('on-cd');else s.classList.remove('on-cd')});
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
const k=e.key.toLowerCase();keys[k]=true;keys[e.code]=true;
if(k==='tab'){e.preventDefault();cycleLock()}
if(k==='i'){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="inventory"]').classList.add('active');document.getElementById('tp-inventory').classList.add('active')}
if(k==='k'){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="skills"]').classList.add('active');document.getElementById('tp-skills').classList.add('active')}
if(k==='f5'){e.preventDefault();if(gameStarted)saveGame()}
if(k==='2'&&!player._parryCD){parry();player._parryCD=15}
if(k==='3'&&!player._estusCD){const heal=Math.round(player.maxHp*.3);player.hp=Math.min(player.hp+heal,player.maxHp);log('Used Estus Flask: +'+heal+' HP','#0f0');player._estusCD=90}
if(k==='4'){// Use first skill item from inventory
let usedItem=false;
for(let si=0;si<inventory.length;si++){const itm=inventory[si];if(skillItems[itm]){const sk=skillItems[itm];
inventory.splice(si,1);updateInvUI();
skills[sk.skill].xp+=sk.xp;
const oldLv=skills[sk.skill].lvl;const newLv=Math.max(oldLv,Math.floor(sk.xp>0?1+Math.sqrt(skills[sk.skill].xp/50):1));
if(newLv>oldLv){skills[sk.skill].lvl=newLv;log(sk.skill+' level up! Now '+newLv,'#ff0')}
log('Used '+itm+': '+sk.skill+' +'+sk.xp+'xp','#cc4');updateSkillUI();usedItem=true;break}}
if(!usedItem)log('No usable skill items in inventory','#887')}
if(k==='q'){e.preventDefault();document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="prayer"]').classList.add('active');document.getElementById('tp-prayer').classList.add('active')}
if(k==='t'&&gameStarted){e.preventDefault();showTeleport=!showTeleport;
let tp=document.getElementById('teleport-menu');
if(!tp){tp=document.createElement('div');tp.id='teleport-menu';tp.style.cssText='position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(10,10,20,0.92);border:2px solid #aa8833;border-radius:8px;padding:12px;z-index:999;max-height:70vh;overflow-y:auto;min-width:260px;color:#ddd;font-family:monospace;';
tp.innerHTML='<div style="color:#ffd700;font-size:16px;font-weight:bold;margin-bottom:8px;text-align:center">⚡ ELEPORTTAY ⚡</div>';
teleports.forEach((t,idx)=>{const btn=document.createElement('div');
btn.style.cssText='padding:6px 10px;margin:3px 0;cursor:pointer;border:1px solid #554422;border-radius:4px;background:rgba(40,30,15,0.8);transition:background 0.2s;';
btn.textContent=t.name+(t.unlocked?'':' 🔒');
btn.onmouseenter=()=>btn.style.background='rgba(80,60,20,0.9)';
btn.onmouseleave=()=>btn.style.background='rgba(40,30,15,0.8)';
btn.onclick=()=>{if(t.unlocked){player.x=t.x;player.z=t.z;log('Teleported to '+t.name+'!','#ffd700');showTeleport=false;tp.style.display='none'}else{log('Location locked!','#f44')}};
tp.appendChild(btn)});
const closeBtn=document.createElement('div');closeBtn.style.cssText='padding:6px;text-align:center;margin-top:8px;cursor:pointer;color:#f44;border:1px solid #f44;border-radius:4px;';
closeBtn.textContent='Close (T)';closeBtn.onclick=()=>{showTeleport=false;tp.style.display='none'};tp.appendChild(closeBtn);
document.body.appendChild(tp)}
else{tp.style.display=showTeleport?'block':'none'}}
if(k==='m'){const wm=document.getElementById('world-map');if(wm.classList.contains('active')){wm.classList.remove('active')}else{wm.classList.add('active');drawWorldMap()}}
if(k==='escape'){const wm=document.getElementById('world-map');if(wm.classList.contains('active'))wm.classList.remove('active');const tp=document.getElementById('teleport-menu');if(tp&&showTeleport){showTeleport=false;tp.style.display='none'}else{lockOn=null;lockIdx=-1;log('Target cleared','#887')}}
if(k==='f'&&gameStarted){e.preventDefault();const nT=Math.hypot(player.x+100,player.z-50)<50;const nR=Math.hypot(player.x+70,player.z+80)<40;const nM=Math.hypot(player.x-300,player.z+100)<60;
if(nT){skills.Woodcutting.xp+=18;log('Woodcutting +18xp','#6a4')}
else if(nR){skills.Fishing.xp+=22;log('Fishing +22xp','#48f')}
else if(nM){skills.Mining.xp+=20;log('Mining +20xp','#a86')}
else log('Nothing to gather here','#887')}
});
window.addEventListener('beforeunload',()=>{if(gameStarted&&!player.dead)saveGame()});
window.addEventListener('keyup',e=>{keys[e.key.toLowerCase()]=false;keys[e.code]=false});
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
skills:{},inventory:[...inventory],equipped:{},opts:{...gameOpts},playerClass:playerClass,ver:3};
skillDefs.forEach(s=>data.skills[s]={lvl:skills[s].lvl,xp:skills[s].xp});
gearSlots.forEach(s=>data.equipped[s]={...equipped[s]});
localStorage.setItem(SAVE_KEY,JSON.stringify(data));
log('Game saved!','#0f0');return true}catch(e){log('Save failed: '+e.message,'#f44');return false}}

function loadGame(){
try{const raw=localStorage.getItem(SAVE_KEY);if(!raw)return false;
const data=JSON.parse(raw);
player.x=data.player.x;player.z=data.player.z;player.hp=data.player.hp;player.maxHp=data.player.maxHp;
player.sta=data.player.sta;player.maxSta=data.player.maxSta;player.poi=data.player.poi;player.maxPoi=data.player.maxPoi;
player.speed=data.player.speed||.42;player.y=meshTerrainH(player.x,player.z);
skillDefs.forEach(s=>{if(data.skills[s]){skills[s].lvl=data.skills[s].lvl;skills[s].xp=data.skills[s].xp}});
if(data.inventory){inventory.length=0;data.inventory.forEach(i=>inventory.push(i));updateInvUI()}
if(data.equipped){gearSlots.forEach(s=>{if(data.equipped[s])equipped[s]=data.equipped[s]})}
if(data.opts){Object.assign(gameOpts,data.opts)}
if(data.playerClass){playerClass=data.playerClass}
updateSkillUI();updateEqUI();refreshPlayerModel();
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
document.getElementById('action-bar').classList.add('active');
document.getElementById('xp-bar-wrap').classList.add('active');
document.body.style.cursor='crosshair';
if(!gameStarted){gameStarted=true;
try{init();if(isLoad)loadGame();updateSkillUI();updateEqUI();loop();connectMP()}catch(err){const cl=document.getElementById('chat-log');if(cl)cl.innerHTML='<div style="color:red;font-size:14px">ERROR: '+err.message+'<br>'+err.stack+'</div>';console.error(err)}}}

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
playerClass=cls;
player.hp=s.hp;player.maxHp=s.hp;player.sta=s.sta;player.maxSta=s.sta;player.poi=s.poi;player.maxPoi=s.poi;
document.getElementById('hpT').textContent=s.hp+'/'+s.hp;document.getElementById('stT').textContent=s.sta+'/'+s.sta;document.getElementById('poT').textContent=s.poi+'/'+s.poi;
const classIcons={warrior:'\u2694',knight:'\u2694',sorcerer:'\u2728',deprived:'\uD83D\uDC64'};
document.getElementById('pf-name').textContent=cls.charAt(0).toUpperCase()+cls.slice(1);
document.getElementById('pf-portrait').textContent=classIcons[cls]||'\u2694';
// Set starting equipment per class
const none={name:'None',atk:0,def:0,str:0};
if(cls==='knight'){
equipped.Helm={name:'Iron Full Helm',atk:1,def:8,str:0};equipped.Chest={name:'Iron Platebody',atk:1,def:12,str:2};
equipped.Legs={name:'Iron Platelegs',atk:0,def:10,str:1};equipped.Boots={name:'Iron Boots',atk:0,def:4,str:0};
equipped.Gloves={name:'Iron Gauntlets',atk:1,def:3,str:1};equipped.Shield={name:'Iron Kiteshield',atk:0,def:10,str:0};
equipped.Weapon={name:'Iron Longsword',atk:10,def:2,str:5};equipped.Ring=none;
}else if(cls==='warrior'){
equipped.Helm=none;equipped.Chest={name:'Chainmail Shirt',atk:0,def:8,str:2};
equipped.Legs={name:'Leather Chaps',atk:0,def:5,str:1};equipped.Boots={name:'Leather Boots',atk:0,def:2,str:0};
equipped.Gloves={name:'Leather Gloves',atk:0,def:2,str:1};equipped.Shield=none;
equipped.Weapon={name:'Iron Scimitar',atk:8,def:0,str:7};equipped.Ring=none;
}else if(cls==='sorcerer'){
equipped.Helm=none;equipped.Chest={name:'Wizard Robe Top',atk:8,def:2,str:0};
equipped.Legs={name:'Wizard Robe Bottom',atk:5,def:2,str:0};equipped.Boots={name:'Wizard Boots',atk:3,def:1,str:0};
equipped.Gloves=none;equipped.Shield=none;
equipped.Weapon={name:'Staff of Air',atk:12,def:3,str:0};equipped.Ring=none;
}else if(cls==='deprived'){
gearSlots.forEach(s=>equipped[s]=none);
}
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
