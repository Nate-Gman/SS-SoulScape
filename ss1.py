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
/* ESC button in HUD */
#esc-hud-btn{position:fixed;top:8px;left:8px;z-index:400;display:none;background:linear-gradient(180deg,rgba(40,32,20,.92),rgba(25,20,12,.95));border:1px solid #5a4a32;border-radius:5px;padding:5px 12px;font-family:'Times New Roman',serif;font-size:11px;color:#c8a96e;cursor:pointer;letter-spacing:2px;transition:all .15s;pointer-events:auto;user-select:none}
#esc-hud-btn:hover{border-color:#c8a96e;color:#ffd700;background:linear-gradient(180deg,rgba(60,48,28,.95),rgba(40,32,16,.98))}
#esc-hud-btn.active{display:block}
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
#xp-bar-wrap{position:fixed;top:32px;left:50%;transform:translateX(-50%);z-index:350;width:500px;display:none;pointer-events:none}
#xp-bar-wrap.active{display:block}
#xp-bar-bg{width:100%;height:14px;background:rgba(0,0,0,.7);border:2px solid #5a4a32;border-radius:7px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.5)}
#xp-bar-fill{height:100%;background:linear-gradient(90deg,#6a3acc,#aa66ff);border-radius:5px;transition:width .3s;width:0%}
#xp-bar-text{text-align:center;font-size:12px;color:#c8a96e;margin-top:3px;text-shadow:0 1px 3px rgba(0,0,0,.9);white-space:nowrap;font-weight:600}
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
.inv-slot{width:52px;height:52px;background:linear-gradient(180deg,#2e2418,#1e1810);border:2px solid #3a2a1a;border-radius:4px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:7px;color:#aa9;text-align:center;line-height:1.1;cursor:pointer;transition:all .15s;overflow:hidden;position:relative}
.inv-slot:hover{border-color:#c8a96e;background:linear-gradient(180deg,#3a3020,#2a2418);box-shadow:0 0 6px rgba(200,169,110,.2)}
.inv-ico{font-size:20px;line-height:1;pointer-events:none}
.inv-name{font-size:6px;color:#cc9;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:48px;pointer-events:none}
#item-tooltip{position:fixed;z-index:9999;display:none;background:linear-gradient(180deg,rgba(30,24,16,.97),rgba(20,16,10,.98));border:2px solid #c8a96e;border-radius:6px;padding:8px 12px;min-width:160px;max-width:250px;pointer-events:none;box-shadow:0 4px 16px rgba(0,0,0,.7);font-family:'Times New Roman',serif}
#item-tooltip .tt-name{font-size:14px;font-weight:700;color:#ffd700;margin-bottom:4px;text-shadow:0 1px 3px rgba(0,0,0,.6)}
#item-tooltip .tt-ico{font-size:24px;float:left;margin-right:8px}
#item-tooltip .tt-desc{font-size:10px;color:#aa9;line-height:1.4}
#item-tooltip .tt-stats{font-size:10px;color:#4c4;margin-top:3px}
#item-tooltip .tt-use{font-size:9px;color:#88c;margin-top:2px;font-style:italic}
/* Inventory context menu */
#inv-context-menu{position:fixed;z-index:10000;display:none;background:linear-gradient(180deg,#3b3020,#2a2018);border:2px solid #c8a96e;border-radius:4px;padding:4px 0;min-width:120px;box-shadow:0 4px 12px rgba(0,0,0,.6);font-family:'Times New Roman',serif;font-size:11px}
#inv-context-menu .ctx-item{padding:6px 12px;color:#e8d4a8;cursor:pointer;transition:background .15s}
#inv-context-menu .ctx-item:hover{background:#4a3a28;color:#ffd700}
#inv-context-menu .ctx-divider{height:1px;background:#5a4a32;margin:4px 0}
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
/* === ESC PAUSE / OPTIONS MENU === */
#esc-menu{position:fixed;inset:0;z-index:950;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.75);backdrop-filter:blur(3px);font-family:'Times New Roman',serif}
#esc-menu.active{display:flex}
#esc-box{background:linear-gradient(180deg,rgba(28,22,14,.99),rgba(18,14,9,.99));border:2px solid #c8a96e;border-radius:10px;width:680px;max-height:88vh;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 12px 48px rgba(0,0,0,.9)}
#esc-title{background:linear-gradient(180deg,rgba(80,60,30,.5),rgba(40,30,15,.5));padding:12px 20px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #5a4a32}
#esc-title h2{margin:0;font-size:22px;color:#ffd700;letter-spacing:4px;text-shadow:0 2px 8px rgba(255,215,0,.3)}
#esc-version{font-size:10px;color:#554;letter-spacing:1px}
#esc-nav{display:flex;gap:2px;padding:6px 10px;border-bottom:1px solid #3a2a1a;background:rgba(20,16,10,.4)}
.esc-nav-btn{padding:6px 14px;font-size:11px;cursor:pointer;border:1px solid #3a2a1a;border-radius:4px;color:#aa9;background:#1a1610;transition:all .15s;font-family:'Times New Roman',serif;letter-spacing:1px}
.esc-nav-btn.active,.esc-nav-btn:hover{border-color:#c8a96e;color:#ffd700;background:#2a2418}
#esc-body{flex:1;overflow-y:auto;padding:14px 18px}
#esc-body::-webkit-scrollbar{width:5px}#esc-body::-webkit-scrollbar-thumb{background:#6a5a42;border-radius:3px}
.esc-page{display:none}.esc-page.active{display:block}
.esc-section{margin-bottom:14px}
.esc-section h3{font-size:13px;color:#c8a96e;letter-spacing:2px;margin:0 0 8px;border-bottom:1px solid #3a2a1a;padding-bottom:4px}
.esc-row{display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid rgba(90,74,50,.2)}
.esc-row:last-child{border-bottom:0}
.esc-label{font-size:11px;color:#aa9}
.esc-val{font-size:11px;color:#ffd700;cursor:pointer;border:1px solid #3a2a1a;padding:2px 8px;border-radius:3px;background:#1a1610;transition:all .15s;min-width:80px;text-align:center}
.esc-val:hover{border-color:#c8a96e;background:#2a2418}
.esc-slider{width:140px;cursor:pointer;accent-color:#c8a96e}
.esc-keybind{font-size:10px;background:#1a1610;border:1px solid #3a2a1a;color:#ffd700;padding:2px 8px;border-radius:3px;cursor:pointer;min-width:60px;text-align:center;transition:all .15s;font-family:monospace}
.esc-keybind:hover,.esc-keybind.listening{border-color:#c8a96e;background:#2a2418;color:#fff}
.esc-keybind.listening{animation:esc-blink .5s infinite alternate}
@keyframes esc-blink{from{border-color:#c8a96e}to{border-color:#ffd700}}
.ctrl-grid{display:grid;grid-template-columns:1fr 1fr;gap:4px 16px}
.ctrl-entry{display:flex;justify-content:space-between;align-items:center;padding:3px 0}
.ctrl-key{font-size:9px;background:#2a2418;border:1px solid #5a4a32;color:#ffd700;padding:1px 6px;border-radius:3px;font-family:monospace;white-space:nowrap}
.ctrl-desc{font-size:9px;color:#887}
#esc-footer{padding:10px 18px;border-top:1px solid #3a2a1a;display:flex;gap:8px;justify-content:center;background:rgba(20,16,10,.4)}
.esc-btn{padding:8px 22px;font-size:12px;cursor:pointer;border:1px solid #5a4a32;border-radius:5px;color:#c8a96e;background:linear-gradient(180deg,#2a2418,#1a1610);font-family:'Times New Roman',serif;letter-spacing:1px;transition:all .15s}
.esc-btn:hover{border-color:#c8a96e;background:linear-gradient(180deg,#3a3020,#2a2418);color:#ffd700}
.esc-btn.danger{border-color:#5a2020;color:#cc4444}.esc-btn.danger:hover{border-color:#cc4444;background:linear-gradient(180deg,#3a2020,#2a1010)}
/* Ability Browser */
#ability-browser{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:900;display:none;background:linear-gradient(180deg,rgba(20,16,10,.97),rgba(15,12,8,.98));border:2px solid #c8a96e;border-radius:8px;width:500px;max-height:70vh;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.8);font-family:'Times New Roman',serif}
#ability-browser.active{display:flex;flex-direction:column}
#ab-header{display:flex;justify-content:space-between;align-items:center;padding:8px 14px;border-bottom:1px solid #5a4a32;background:rgba(40,32,20,.5)}
#ab-header h3{margin:0;font-size:16px;color:#ffd700;letter-spacing:2px}
#ab-close{cursor:pointer;font-size:20px;color:#887}#ab-close:hover{color:#f44}
#ab-cats{display:flex;gap:2px;padding:6px 10px;border-bottom:1px solid #3a2a1a;flex-wrap:wrap}
.ab-cat{padding:4px 10px;font-size:10px;cursor:pointer;border:1px solid #3a2a1a;border-radius:3px;color:#aa9;background:#1a1610;transition:all .15s}
.ab-cat.active,.ab-cat:hover{border-color:#c8a96e;color:#ffd700;background:#2a2418}
#ab-list{flex:1;overflow-y:auto;padding:8px;display:grid;grid-template-columns:repeat(5,1fr);gap:4px}
#ab-list::-webkit-scrollbar{width:5px}#ab-list::-webkit-scrollbar-thumb{background:#6a5a42;border-radius:3px}
.ab-item{width:80px;height:64px;background:linear-gradient(180deg,#2a2418,#1a1610);border:2px solid #3a2a1a;border-radius:4px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:grab;transition:all .15s;padding:2px}
.ab-item:hover{border-color:#c8a96e;transform:scale(1.05);box-shadow:0 0 8px rgba(200,169,110,.3)}
.ab-item .abi-ico{font-size:22px;line-height:1}
.ab-item .abi-name{font-size:7px;color:#cc9;text-align:center;white-space:nowrap;overflow:hidden;max-width:74px}
.ab-item .abi-desc{font-size:6px;color:#887;text-align:center}
.ab-slot.drag-over{border-color:#ffd700!important;box-shadow:0 0 12px rgba(255,215,0,.5)!important}
#ab-hint{padding:6px;text-align:center;font-size:9px;color:#665;border-top:1px solid #3a2a1a}
/* Spell Book */
#spell-book{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:900;display:none;background:linear-gradient(180deg,rgba(20,10,30,.97),rgba(15,8,25,.98));border:2px solid #8a4ac8;border-radius:8px;width:500px;max-height:70vh;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.8);font-family:'Times New Roman',serif}
#spell-book.active{display:flex;flex-direction:column}
#sb-header{display:flex;justify-content:space-between;align-items:center;padding:8px 14px;border-bottom:1px solid #5a2a8a;background:rgba(40,20,60,.5)}
#sb-header h3{margin:0;font-size:16px;color:#c88aff;letter-spacing:2px}
#sb-close{cursor:pointer;font-size:20px;color:#a87acc}#sb-close:hover{color:#f44}
#sb-cats{display:flex;gap:2px;padding:6px 10px;border-bottom:1px solid #3a1a5a;flex-wrap:wrap}
.sb-cat{padding:4px 10px;font-size:10px;cursor:pointer;border:1px solid #3a1a5a;border-radius:3px;color:#a98acc;background:#1a1018;transition:all .15s}
.sb-cat.active,.sb-cat:hover{border-color:#a84aff;color:#c88aff;background:#2a1828}
#sb-list{flex:1;overflow-y:auto;padding:8px;display:grid;grid-template-columns:repeat(5,1fr);gap:4px}
#sb-list::-webkit-scrollbar{width:5px}#sb-list::-webkit-scrollbar-thumb{background:#6a4282;border-radius:3px}
.sb-item{width:80px;height:64px;background:linear-gradient(180deg,#2a1828,#1a1018);border:2px solid #3a1a5a;border-radius:4px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:grab;transition:all .15s;padding:2px}
.sb-item:hover{border-color:#a84aff;transform:scale(1.05);box-shadow:0 0 8px rgba(168,74,255,.3)}
.sb-item .sbi-ico{font-size:22px;line-height:1}
.sb-item .sbi-name{font-size:7px;color:#c98aff;text-align:center;white-space:nowrap;overflow:hidden;max-width:74px}
.sb-item .sbi-desc{font-size:6px;color:#987acc;text-align:center}
#sb-hint{padding:6px;text-align:center;font-size:9px;color:#876;border-top:1px solid #3a1a5a}
#loot-prompt{position:fixed;bottom:180px;left:50%;transform:translateX(-50%);z-index:300;display:none;flex-direction:column;align-items:center;pointer-events:none;font-family:'Times New Roman',serif}
#loot-prompt.active{display:flex}
#loot-prompt .lp-title{font-size:18px;color:#ffd700;text-shadow:0 0 12px rgba(255,215,0,.6),0 2px 4px rgba(0,0,0,.8);letter-spacing:2px;margin-bottom:4px}
#loot-prompt .lp-key{font-size:13px;color:#c8a96e;text-shadow:0 1px 3px #000;letter-spacing:1px;opacity:.8}
#loot-label-canvas{position:fixed;inset:0;z-index:200;pointer-events:none}
#death-overlay{position:absolute;inset:0;background:rgba(0,0,0,0);z-index:500;display:flex;align-items:center;justify-content:center;pointer-events:none;transition:background .8s}
#death-overlay.active{background:rgba(0,0,0,.85)}
#death-text{font-size:52px;color:#8b0000;font-family:'Times New Roman',serif;letter-spacing:12px;opacity:0;transition:opacity 1s;text-shadow:0 0 30px rgba(139,0,0,.6)}
#death-overlay.active #death-text{opacity:1}
#controls{position:absolute;bottom:78px;left:50%;transform:translateX(-50%);z-index:100;font-size:9px;color:#bba;text-align:center;pointer-events:none;background:rgba(10,8,6,.92);padding:5px 14px;border-radius:10px;letter-spacing:.5px;opacity:1;transition:opacity .3s;border:1px solid rgba(200,169,110,.3);text-shadow:0 1px 2px rgba(0,0,0,.8)}
#controls:hover{opacity:1}
#locbar{position:absolute;top:62px;left:50%;transform:translateX(-50%);z-index:150;font-size:13px;color:#c8a96e;pointer-events:none;background:linear-gradient(90deg,transparent,rgba(20,16,10,.9),transparent);padding:6px 40px;letter-spacing:2px;font-family:'Times New Roman',serif;text-shadow:0 1px 4px rgba(0,0,0,.6);border-bottom:1px solid rgba(200,169,110,.3)}
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
<div class="class-card" data-c="ranger"><h3>Ranger</h3><p>Expert marksman hunter.</p><div class="cst">RNG 16 AGI 14<br>HP 120 STA 100</div></div>
</div></div>
<div id="game-ui">
<div id="esc-hud-btn" onclick="document.getElementById('esc-menu').classList.toggle('active')">&#9776; MENU</div>
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
<div class="ab-slot" data-action="attack" title="Attack (1)"><span class="ab-ico">&#9876;</span><span class="ab-name">Attack</span><span class="ab-key">1</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="parry" title="Parry/Block (2)"><span class="ab-ico">&#128737;</span><span class="ab-name">Parry</span><span class="ab-key">2</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="heal" title="Estus Flask (3)"><span class="ab-ico">&#127863;</span><span class="ab-name">Heal</span><span class="ab-key">3</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="shoot" title="Shoot Arrow (4)"><span class="ab-ico">&#127993;</span><span class="ab-name">Shoot</span><span class="ab-key">4</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="prayer" title="Prayer (5)"><span class="ab-ico">&#10013;</span><span class="ab-name">Prayer</span><span class="ab-key">5</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="gather" title="Gather (6)"><span class="ab-ico">&#9935;</span><span class="ab-name">Gather</span><span class="ab-key">6</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="roll" title="Dodge Roll (7)"><span class="ab-ico">&#128168;</span><span class="ab-name">Roll</span><span class="ab-key">7</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="lock" title="Lock-On (8)"><span class="ab-ico">&#127919;</span><span class="ab-name">Lock</span><span class="ab-key">8</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="map" title="World Map (9)"><span class="ab-ico">&#128506;</span><span class="ab-name">Map</span><span class="ab-key">9</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="inv" title="Inventory (0)"><span class="ab-ico">&#127890;</span><span class="ab-name">Bag</span><span class="ab-key">10</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="skills" title="Skills (-)"><span class="ab-ico">&#9733;</span><span class="ab-name">Skills</span><span class="ab-key">11</span><div class="ab-cd"></div></div>
<div class="ab-slot" data-action="save" title="Quick Save (=)"><span class="ab-ico">&#128190;</span><span class="ab-name">Save</span><span class="ab-key">12</span><div class="ab-cd"></div></div>
<!-- Dash abilities (Q/E) - hidden from bar but active via keys -->
<div class="ab-slot" data-action="dash_left" style="display:none"></div>
<div class="ab-slot" data-action="dash_right" style="display:none"></div>
</div></div>
<!-- XP BAR -->
<div id="xp-bar-wrap"><div id="xp-bar-bg"><div id="xp-bar-fill"></div></div><div id="xp-bar-text">Combat Lv 1 (0%) - 0/100 XP</div></div>
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
<div class="eq-row"><div class="eq-slot" id="eq-Weapon"><span class="eq-ico">&#9876;</span><span class="eq-name">Weapon</span></div><div class="eq-slot" id="eq-Chest"><span class="eq-ico">&#128085;</span><span class="eq-name">Chest</span></div><div class="eq-slot" id="eq-Shield"><span class="eq-ico">&#128737;</span><span class="eq-name">Shield</span></div><div class="eq-slot" id="eq-OffHand"><span class="eq-ico">&#128299;</span><span class="eq-name">OffHand</span></div></div>
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
<div class="tab-page" id="tp-settings"><div style="padding:8px;font-size:10px;color:#aa9"><b style="color:#cc9944">Controls</b><br><br><b style="color:#cc9944">Mouse:</b><br>LClick - Attack / Target<br>RClick - Block / Parry<br>MClick+Drag - Camera<br>Scroll - Zoom<br><br><b style="color:#cc9944">Keys:</b><br>WASD - Move<br>Z - Jump<br>L-Shift - Sprint (hold)<br>Space - Roll<br>W/A/S/D + Space - Directional Roll<br>Tab - Cycle Lock-on<br>1 - Attack<br>2 - Parry<br>3 - Heal (Estus)<br>4 - Bury Bones<br>Q - Prayer Tab<br>E - Pickup / Interact<br>F - Lock-On Toggle<br>G - Gather / Skill<br>M - World Map<br>P - Abilities<br>U - Dungeon<br>Esc - Menu / Close<br>I - Inventory<br>K - Skills<br>F5 - Save<br><br><b style="color:#cc9944">Gamepad (Dark Souls):</b><br>LStick - Move<br>RStick - Camera<br>RT - Light Attack<br>RB - Parry / Heavy<br>LT - Block / Guard (hold)<br>B/○ - Roll (with LStick for direction)<br>A/✕ - Heal (Estus)<br>X/□ - Use Item / Pickup<br>Y/△ - Jump<br>L3 - Sprint (hold LStick)<br>R3 - Lock-on Toggle<br>D-Pad Up - Prayer Tab<br>D-Pad Down - Skills Tab<br>D-Pad Left - Inventory Tab<br>Start - Inventory<br>Back/Select - Skills</div></div>
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
<div id="controls"><b style="color:#ffd700">ESC</b> Options &#183; WASD Move &#183; <b style="color:#ffd700">Q/E</b> Dash Left/Right &#183; <b style="color:#ffd700">L-Shift</b> Sprint (L3) &#183; <b style="color:#ffd700">Space</b> Jump/Roll &#183; <b style="color:#ffd700">1-4</b> Combat &#183; <b style="color:#ffd700">5</b> Prayer &#183; <b style="color:#ffd700">6</b> Gather &#183; <b style="color:#ffd700">7</b> Roll &#183; <b style="color:#ffd700">8</b> Lock &#183; <b style="color:#ffd700">9</b> Map &#183; <b style="color:#ffd700">0</b> Inv &#183; <b style="color:#ffd700">-</b> Skills &#183; <b style="color:#ffd700">=</b> Save &#183; F Lock-On &#183; Tab Cycle &#183; P Abilities &#183; Insert Editor</div>
<div id="target-frame"><div id="tf-icon">👹</div><div id="tf-info"><div><span id="tf-name">Enemy</span><span id="tf-lv">Lv 1</span></div><div id="tf-hp-bg"><div id="tf-hp-fill" style="width:100%"></div></div><div id="tf-hp-text">100/100</div></div></div>
<div id="world-map"><div id="wm-title">WORLD MAP</div><canvas id="wm-canvas" width="900" height="700"></canvas><div id="wm-coords">Player: 0, 0</div><div id="wm-close">&times;</div></div>
<canvas id="loot-label-canvas"></canvas>
<div id="loot-prompt"><span class="lp-title">—</span><span class="lp-key">Press E (or X/□) to pick up</span></div>
<div id="item-tooltip"><span class="tt-ico"></span><div class="tt-name"></div><div class="tt-desc"></div><div class="tt-stats"></div><div class="tt-use"></div></div>
<!-- Inventory Context Menu -->
<div id="inv-context-menu">
<div class="ctx-item" id="ctx-equip">Equip</div>
<div class="ctx-item" id="ctx-drop">Drop</div>
</div>
<div id="ability-browser"><div id="ab-header"><h3>ABILITIES &amp; ACTIONS</h3><span id="ab-close">&times;</span></div><div id="ab-cats"></div><div id="ab-list"></div><div id="ab-hint">Drag an ability onto an action bar slot to assign it. Press P to close.</div></div>

<!-- === SPELL BOOK === -->
<div id="spell-book"><div id="sb-header"><h3>SPELL BOOK</h3><span id="sb-close">&times;</span></div><div id="sb-cats"></div><div id="sb-list"></div><div id="sb-hint">Drag a spell onto an action bar slot to assign it. Press O to close.</div></div>

<!-- === EDITOR MODE UI === -->
<div id="editor-mode" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:transparent;z-index:9999;pointer-events:none;">
<!-- Editor Panel - only UI element blocks clicks -->
<div id="editor-panel" style="position:absolute;top:10px;left:10px;width:360px;max-height:90vh;background:rgba(20,15,10,0.98);border:2px solid #aa8833;border-radius:8px;padding:12px;overflow-y:auto;color:#ddd;font-family:monospace;font-size:11px;pointer-events:auto;box-shadow:0 4px 20px rgba(0,0,0,0.8);">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;border-bottom:1px solid #554422;padding-bottom:8px;">
<h3 style="margin:0;color:#ffd700;font-size:14px;">🛠️ EDITOR MODE</h3>
<span style="color:#887;font-size:10px;">Insert to toggle</span>
</div>
<!-- Camera Controls -->
<div style="margin-bottom:12px;padding:8px;background:rgba(60,45,20,0.6);border-radius:4px;">
<div style="color:#aa8833;margin-bottom:6px;font-size:10px;text-transform:uppercase;">Camera View</div>
<div style="display:flex;gap:4px;">
<button onclick="editorSetCamera('normal')" id="btn-cam-normal" style="flex:1;background:#554422;color:#ffd700;border:1px solid #aa8833;padding:4px;cursor:pointer;border-radius:3px;font-size:10px;">🎮 Normal</button>
<button onclick="editorSetCamera('bird')" id="btn-cam-bird" style="flex:1;background:#332211;color:#aa8833;border:1px solid #554422;padding:4px;cursor:pointer;border-radius:3px;font-size:10px;">🦅 Bird's Eye</button>
<button onclick="editorSetCamera('top')" id="btn-cam-top" style="flex:1;background:#332211;color:#aa8833;border:1px solid #554422;padding:4px;cursor:pointer;border-radius:3px;font-size:10px;">📐 Top Down</button>
</div>
</div>
<!-- Object List -->
<div style="margin-bottom:12px;">
<div style="color:#aa8833;margin-bottom:6px;font-size:10px;text-transform:uppercase;">Selected Object</div>
<div id="editor-selected-info" style="background:rgba(40,30,20,0.8);padding:8px;border-radius:4px;font-size:10px;">
<span style="color:#887;">Click an object to select</span>
</div>
<div id="editor-controls" style="display:none;margin-top:8px;">
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px;">
<button onclick="editorMove('up')" style="background:#443322;color:#ffd700;border:1px solid #aa8833;padding:6px;cursor:pointer;border-radius:3px;font-size:10px;">↑ Y+</button>
<button onclick="editorFocusSelected()" style="background:#224455;color:#8bf;border:1px solid #458;padding:6px;cursor:pointer;border-radius:3px;font-size:10px;">👁 Focus</button>
<button onclick="editorMove('down')" style="background:#443322;color:#ffd700;border:1px solid #aa8833;padding:6px;cursor:pointer;border-radius:3px;font-size:10px;">↓ Y-</button>
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-top:4px;">
<button onclick="editorMove('left')" style="background:#443322;color:#ffd700;border:1px solid #aa8833;padding:6px;cursor:pointer;border-radius:3px;font-size:10px;">← X-</button>
<button onclick="editorMove('forward')" style="background:#443322;color:#ffd700;border:1px solid #aa8833;padding:6px;cursor:pointer;border-radius:3px;font-size:10px;">↑ Z-</button>
<button onclick="editorMove('right')" style="background:#443322;color:#ffd700;border:1px solid #aa8833;padding:6px;cursor:pointer;border-radius:3px;font-size:10px;">X+ →</button>
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-top:4px;">
<button onclick="editorMove('back')" style="background:#443322;color:#ffd700;border:1px solid #aa8833;padding:6px;cursor:pointer;border-radius:3px;font-size:10px;">↓ Z+</button>
<button onclick="editorDelete()" style="background:#442222;color:#ff4444;border:1px solid #aa3333;padding:6px;cursor:pointer;border-radius:3px;font-size:10px;">🗑 Delete</button>
<button onclick="editorSpawnAtSelected()" style="background:#335522;color:#8f8;border:1px solid #5a5;padding:6px;cursor:pointer;border-radius:3px;font-size:10px;">📍 Spawn Here</button>
</div>
<div style="margin-top:6px;padding:4px;background:rgba(50,40,30,0.8);border-radius:3px;font-size:9px;color:#aa8833;">
💡 <b>Drag Mode:</b> Hold <b>Shift</b> and drag mouse to move selected object
</div>
</div>
</div>
<!-- Spawn Section -->
<div style="margin-bottom:12px;">
<div style="color:#aa8833;margin-bottom:6px;font-size:10px;text-transform:uppercase;">Spawn Object</div>
<div style="display:flex;gap:4px;margin-bottom:6px;">
<button onclick="setEditorType('enemy')" id="btn-enemy" class="editor-type-btn" style="flex:1;background:#554422;color:#ffd700;border:2px solid #aa8833;padding:6px;cursor:pointer;border-radius:4px;font-size:11px;font-weight:bold;">Enemy</button>
<button onclick="setEditorType('building')" id="btn-building" class="editor-type-btn" style="flex:1;background:#332211;color:#aa8833;border:1px solid #554422;padding:6px;cursor:pointer;border-radius:4px;font-size:11px;">Building</button>
<button onclick="setEditorType('loot')" id="btn-loot" class="editor-type-btn" style="flex:1;background:#332211;color:#aa8833;border:1px solid #554422;padding:6px;cursor:pointer;border-radius:4px;font-size:11px;">Loot</button>
</div>
<select id="editor-spawn-select" style="width:100%;background:#221100;color:#ffd700;border:2px solid #554422;padding:6px;border-radius:4px;font-size:11px;margin-bottom:6px;cursor:pointer;">
</select>
<button onclick="editorSpawn()" style="width:100%;background:#335522;color:#8f8;border:2px solid #5a5;padding:8px;cursor:pointer;border-radius:4px;font-size:12px;font-weight:bold;">📍 Spawn at Player Position</button>
</div>
<!-- World Objects List -->
<div style="margin-bottom:12px;">
<div style="color:#aa8833;margin-bottom:6px;font-size:10px;text-transform:uppercase;display:flex;justify-content:space-between;align-items:center;">
<span>World Objects (<span id="editor-count">0</span>)</span>
<button onclick="editorRefreshList()" style="background:#443322;color:#ffd700;border:1px solid #aa8833;padding:4px 8px;cursor:pointer;border-radius:3px;font-size:9px;">Refresh</button>
</div>
<div id="editor-object-list" style="background:rgba(40,30,20,0.8);padding:6px;border-radius:4px;font-size:10px;max-height:200px;overflow-y:auto;border:1px solid #554422;">
<span style="color:#665;">No objects loaded...</span>
</div>
</div>
<!-- Snap & Save -->
<div style="border-top:1px solid #554422;padding-top:10px;display:flex;gap:8px;flex-wrap:wrap;">
<button onclick="editorSnapToggle()" id="btn-snap" style="background:#332211;color:#887;border:2px solid #554422;padding:6px 12px;cursor:pointer;border-radius:4px;font-size:10px;font-weight:bold;">📐 Snap: OFF</button>
<button onclick="editorSaveWorld()" style="background:#335522;color:#8f8;border:2px solid #5a5;padding:6px 12px;cursor:pointer;border-radius:4px;font-size:10px;font-weight:bold;">💾 Save World</button>
<button onclick="editorLoadWorld()" style="background:#443322;color:#ffd700;border:2px solid #aa8833;padding:6px 12px;cursor:pointer;border-radius:4px;font-size:10px;font-weight:bold;">📂 Load World</button>
<button onclick="editorExport()" style="background:#224455;color:#8bf;border:2px solid #458;padding:6px 12px;cursor:pointer;border-radius:4px;font-size:10px;font-weight:bold;">📤 Export</button>
</div>
<div style="margin-top:10px;padding:8px;background:rgba(50,40,20,0.9);border-radius:4px;font-size:9px;color:#aa8833;line-height:1.5;border:1px solid #554422;">
<b style="color:#ffd700;">📖 Editor Controls:</b><br>
• <b>Click</b> object to select & focus camera<br>
• <b>Shift+Drag</b> to move selected object<br>
• <b>Arrow buttons</b> for precise movement<br>
• <b>WASD</b> moves player, <b>Scroll</b> zooms<br>
• Use <b>Bird's Eye</b> view for easy placement
</div>
</div>
<!-- Visual indicator when editor active -->
<div id="editor-cursor" style="position:fixed;top:50%;left:50%;width:24px;height:24px;transform:translate(-50%,-50%);pointer-events:none;z-index:10000;display:none;">
<div style="width:2px;height:24px;background:#ffd700;position:absolute;left:11px;top:0;box-shadow:0 0 4px #000;"></div>
<div style="width:24px;height:2px;background:#ffd700;position:absolute;left:0;top:11px;box-shadow:0 0 4px #000;"></div>
</div>
</div>

<!-- === ESC PAUSE / OPTIONS MENU === -->
<div id="esc-menu">
<div id="esc-box">
<div id="esc-title"><h2>&#9876; SOULSCAPE</h2><span id="esc-version">v4.0 — OSRS Souls</span></div>
<div id="esc-nav">
<div class="esc-nav-btn active" data-page="resume">&#9654; Resume</div>
<div class="esc-nav-btn" data-page="controls">&#9874; Controls</div>
<div class="esc-nav-btn" data-page="settings">&#9881; Settings</div>
<div class="esc-nav-btn" data-page="interface">&#9783; Interface</div>
<div class="esc-nav-btn" data-page="keybinds">&#9000; Keybinds</div>
</div>
<div id="esc-body">
<!-- RESUME page -->
<div class="esc-page active" id="ep-resume">
<div class="esc-section"><h3>PAUSED</h3>
<p style="color:#887;font-size:12px;line-height:1.7">Press <span class="ctrl-key">ESC</span> or click <b style="color:#ffd700">Resume</b> below to return to the game.<br>Use the tabs above to configure controls, graphics, and interface options.</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px">
<div class="esc-btn" id="esc-save-btn">&#128190; Save Game</div>
<div class="esc-btn" id="esc-map-btn">&#9788; World Map</div>
<div class="esc-btn" id="esc-tele-btn">&#9711; Teleport</div>
<div class="esc-btn" id="esc-inv-btn">&#127984; Inventory</div>
<div class="esc-btn" id="esc-skills-btn">&#9994; Skills</div>
<div class="esc-btn" id="esc-ab-btn">&#128218; Abilities</div>
</div>
</div>
</div>
<!-- CONTROLS page -->
<div class="esc-page" id="ep-controls">
<div class="esc-section"><h3>KEYBOARD &amp; MOUSE</h3>
<div class="ctrl-grid">
<div class="ctrl-entry"><span class="ctrl-desc">Move Forward</span><span class="ctrl-key">W</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Move Back</span><span class="ctrl-key">S</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Strafe Left</span><span class="ctrl-key">A</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Strafe Right</span><span class="ctrl-key">D</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Jump</span><span class="ctrl-key">Z</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Roll / Dodge (W/A/S/D + Space for directional)</span><span class="ctrl-key">Space</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Attack</span><span class="ctrl-key">1 / LMB</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Parry / Block</span><span class="ctrl-key">2 / RMB</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Heal (Estus)</span><span class="ctrl-key">3</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Gather / Chop</span><span class="ctrl-key">G</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Sprint</span><span class="ctrl-key">L-Shift (hold)</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Interact / Pickup</span><span class="ctrl-key">E</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Lock-On Toggle</span><span class="ctrl-key">F</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Lock-On Cycle</span><span class="ctrl-key">Tab</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Inventory</span><span class="ctrl-key">I</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Skills</span><span class="ctrl-key">K</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">World Map</span><span class="ctrl-key">M</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Teleport Menu</span><span class="ctrl-key">T</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Dungeon / Gauntlet</span><span class="ctrl-key">U</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Ability Browser</span><span class="ctrl-key">P</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Spell Book</span><span class="ctrl-key">O</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Options Menu</span><span class="ctrl-key">ESC</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Quick Save</span><span class="ctrl-key">F5</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Prayer</span><span class="ctrl-key">5</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Bury Bones</span><span class="ctrl-key">6</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Auto Loot</span><span class="ctrl-key">L</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Minimap Toggle</span><span class="ctrl-key">N</span></div>
</div></div>
<div class="esc-section"><h3>GAMEPAD (DARK SOULS LAYOUT)</h3>
<div class="ctrl-grid">
<div class="ctrl-entry"><span class="ctrl-desc">Move</span><span class="ctrl-key">L-Stick</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Camera</span><span class="ctrl-key">R-Stick</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Attack</span><span class="ctrl-key">RT</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Heavy / Parry</span><span class="ctrl-key">RB</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Block / Guard</span><span class="ctrl-key">LT</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Lock-On Toggle</span><span class="ctrl-key">R3 / RS Click</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Lock-On Cycle</span><span class="ctrl-key">L3 / LS Click</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Heal (Estus)</span><span class="ctrl-key">A / Cross</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Roll / Dodge (B + Left Stick direction)</span><span class="ctrl-key">B / Circle</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Sprint</span><span class="ctrl-key">L3 (hold L-Stick)</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Jump</span><span class="ctrl-key">Y / Triangle</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Interact</span><span class="ctrl-key">X / Square</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Inventory</span><span class="ctrl-key">Start</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">Skills</span><span class="ctrl-key">Back / Select</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">D-Pad</span><span class="ctrl-key">Move / Strafe</span></div>
<div class="ctrl-entry"><span class="ctrl-desc">LB+RT Combo</span><span class="ctrl-key">Ability Combo</span></div>
</div></div>
</div>
<!-- SETTINGS page -->
<div class="esc-page" id="ep-settings">
<div class="esc-section"><h3>VIDEO</h3>
<div class="esc-row"><span class="esc-label">Brightness</span><input type="range" class="esc-slider" min="5" max="30" value="20" id="opt-bright" oninput="if(typeof gameOpts!=='undefined'){gameOpts.bright=this.value/10;if(renderer)renderer.toneMappingExposure=gameOpts.bright}"></div>
<div class="esc-row"><span class="esc-label">Shadow Quality</span><div class="esc-val" id="opt-shadow">High</div></div>
<div class="esc-row"><span class="esc-label">Bloom / Glow Effects</span><div class="esc-val" id="opt-bloom">On</div></div>
<div class="esc-row"><span class="esc-label">Fog</span><div class="esc-val" id="opt-fog">On</div></div>
</div>
<div class="esc-section"><h3>CAMERA</h3>
<div class="esc-row"><span class="esc-label">Sensitivity</span><input type="range" class="esc-slider" min="1" max="20" value="5" id="opt-sens" oninput="if(typeof gameOpts!=='undefined')gameOpts.sens=+this.value;document.getElementById('opt-sens-v').textContent=this.value"> <span id="opt-sens-v" style="color:#ffd700;font-size:11px;min-width:16px;text-align:right">5</span></div>
<div class="esc-row"><span class="esc-label">Invert X-Axis</span><div class="esc-val" id="opt-flipx">Normal</div></div>
<div class="esc-row"><span class="esc-label">Invert Y-Axis</span><div class="esc-val" id="opt-flipy">Normal</div></div>
</div>
<div class="esc-section"><h3>AUDIO</h3>
<div class="esc-row"><span class="esc-label">Music Volume</span><input type="range" class="esc-slider" min="0" max="100" value="70" id="opt-music"></div>
<div class="esc-row"><span class="esc-label">SFX Volume</span><input type="range" class="esc-slider" min="0" max="100" value="80" id="opt-sfx"></div>
</div>
<div class="esc-section"><h3>GAMEPLAY</h3>
<div class="esc-row"><span class="esc-label">Auto Loot</span><div class="esc-val" id="opt-autoloot">Off</div></div>
<div class="esc-row"><span class="esc-label">Auto Lock-On</span><div class="esc-val" id="opt-autolk">On</div></div>
<div class="esc-row"><span class="esc-label">Show Damage Numbers</span><div class="esc-val" id="opt-dmgnum">On</div></div>
<div class="esc-row"><span class="esc-label">HUD Opacity</span><input type="range" class="esc-slider" min="20" max="100" value="95" id="opt-hudop" oninput="document.getElementById('game-ui').style.opacity=(this.value/100)"></div>
</div>
</div>
<!-- INTERFACE page -->
<div class="esc-page" id="ep-interface">
<div class="esc-section"><h3>HUD ELEMENTS</h3>
<div class="esc-row"><span class="esc-label">Action Bar</span><div class="esc-val" id="ui-actionbar">Visible</div></div>
<div class="esc-row"><span class="esc-label">XP Bar</span><div class="esc-val" id="ui-xpbar">Visible</div></div>
<div class="esc-row"><span class="esc-label">Right Panel (Stats/Inventory)</span><div class="esc-val" id="ui-rpanel">Visible</div></div>
<div class="esc-row"><span class="esc-label">Minimap</span><div class="esc-val" id="ui-mmap">Visible</div></div>
<div class="esc-row"><span class="esc-label">Combat Log</span><div class="esc-val" id="ui-clog">Visible</div></div>
<div class="esc-row"><span class="esc-label">Loot Labels</span><div class="esc-val" id="ui-lootlbl">Visible</div></div>
<div class="esc-row"><span class="esc-label">Target Frame</span><div class="esc-val" id="ui-tframe">Visible</div></div>
</div>
<div class="esc-section"><h3>ACTION BAR CUSTOMIZATION</h3>
<p style="color:#887;font-size:11px;line-height:1.6">Press <span class="ctrl-key">P</span> to open the Ability Browser. <b style="color:#ffd700">Drag any ability</b> from the browser onto an action bar slot to assign it.<br>Gamepad combos: hold LB or RB then press face buttons for extra bindings.</p>
<div class="esc-btn" id="esc-openab-btn" style="margin-top:8px;display:inline-block">Open Ability Browser (P)</div>
</div>
<div class="esc-section"><h3>PANEL LAYOUT</h3>
<div class="esc-row"><span class="esc-label">Right Panel Position</span><div class="esc-val" id="ui-rpos">Right</div></div>
<div class="esc-row"><span class="esc-label">Action Bar Position</span><div class="esc-val" id="ui-abpos">Bottom Center</div></div>
<div class="esc-row"><span class="esc-label">Font Size</span><div class="esc-val" id="ui-font">Normal</div></div>
</div>
</div>
<!-- KEYBINDS page -->
<div class="esc-page" id="ep-keybinds">
<div class="esc-section"><h3>REBIND KEYS — click a key to reassign</h3>
<p style="color:#554;font-size:10px;margin-bottom:8px">Click any key button, then press the new key on your keyboard.</p>
<div id="kb-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:4px 16px"></div>
</div>
</div>
</div><!-- esc-body -->
<div id="esc-footer">
<div class="esc-btn" id="esc-resume-btn">&#9654; Resume Game</div>
<div class="esc-btn" id="esc-savequit-btn">&#128190; Save</div>
<div class="esc-btn danger" id="esc-quit-btn">&#9633; Quit to Menu</div>
</div>
</div><!-- esc-box -->
</div><!-- esc-menu -->

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

const skillDefs=['Attack','Strength','Defence','Hitpoints','Ranged','Prayer','Magic','Cooking','Woodcutting','Fishing','Mining','Smithing','Crafting','Firemaking','Herblore','Agility','Thieving','Slayer','Runecraft','Farming'];
const skillIcons={Attack:'\u2694',Strength:'\uD83D\uDCAA',Defence:'\uD83D\uDEE1',Hitpoints:'\u2764',Ranged:'\uD83C\uDFF9',Prayer:'\u271D',Magic:'\u2728',Cooking:'\uD83C\uDF56',Woodcutting:'\uD83E\uDE93',Fishing:'\uD83C\uDFA3',Mining:'\u26CF',Smithing:'\uD83D\uDD28',Crafting:'\u2702',Firemaking:'\uD83D\uDD25',Herblore:'\uD83C\uDF3F',Agility:'\uD83C\uDFC3',Thieving:'\uD83D\uDC4B',Slayer:'\uD83D\uDC80',Runecraft:'\uD83D\uDD2E',Farming:'\uD83C\uDF3E'};
const skills={};skillDefs.forEach(s=>skills[s]={lvl:1,xp:0});skills.Hitpoints.lvl=10;skills.Hitpoints.xp=1154;skills.Attack.lvl=3;skills.Attack.xp=174;skills.Strength.lvl=2;skills.Strength.xp=83;skills.Defence.lvl=2;skills.Defence.xp=83;
const sgEl=document.getElementById('skill-grid');
skillDefs.forEach(s=>{const d=document.createElement('div');d.className='sk-cell';d.id='sk-'+s;d.innerHTML=`<span class="sk-ico">${skillIcons[s]||''}</span><span class="sk-name">${s}</span><span class="sk-lv">${skills[s].lvl}</span><span class="sk-xp">${skills[s].xp}xp</span>`;sgEl.appendChild(d)});
const invEl=document.getElementById('inv-grid');
for(let i=0;i<28;i++){const d=document.createElement('div');d.className='inv-slot';d.id='inv-'+i;invEl.appendChild(d)}
const inventory=[];
// Item icon map: keyword->emoji. Checks item name for keyword match.
const itemIcoMap=[
['Ordssway','⚔'],['Ieldshay','🛡'],['Elmhay','⛑'],['Atebodypay','🦺'],['Atelegspay','👖'],['Ootsbay','👢'],['Ovesglay','🧤'],['Ingray','💍'],['Amuleway','📿'],['Ecklacenay','📿'],
['Ickaxepay','⛏'],['Atchethay','🪓'],['Ammerhay','🔨'],['Owbay','🏹'],['Arrowway','➡'],['Affstay','🪄'],['Aggerdray','🗡'],['Iphway','🪢'],['Earspay','🔱'],['Acemay','🔨'],
['Onesbay','🦴'],['Igbay Onesbay','💀'],['Agondray Onesbay','🐉'],['Ydrahay Onesbay','🐍'],
['Oinscay','🪙'],['Okkultay','🪙'],['Oldgay','🥇'],
['Eefbay','🥩'],['Ickenchay','🍗'],['Eatmay','🥩'],['Almonsay','🐟'],['Arkshay','🦈'],['Ordfishsway','🐟'],['Unatay','🐟'],['Ompychay','🍗'],['Eggway','🥚'],['Ananabay','🍌'],['Eadbray','🍞'],['Ilkmay','🥛'],['Ookbay','📖'],
['Uneray','🔮'],['Aturenay','🟢'],['Eathday','💀'],['Oodblay','🩸'],['Oulsay','👻'],['Aoscay','🌀'],['Irefay','🔥'],['Awlay','⚖'],['Indmay','🧠'],['Athwray','💢'],
['Erbhay','🌿'],['Arlicgay','🧄'],['Otionpay','🧪'],['Antidoteway','🧪'],['Antipoisonway','🧪'],
['Ishingfay','🎣'],['Odray','🎣'],['Arpoonhay','🎣'],
['Inderboxtay','🔥'],['Iselchay','🔧'],['Eedlenay','🪡'],['Ockpicklay','🔓'],
['Idehay','🟤'],['Agonhidedray','🐉'],['Eatherlay','👝'],['Urfay','🧥'],['Ilksay','🕸'],['Inskay','🟫'],
['Apecay','🧣'],['Oberay','👘'],['Armorway','🦺'],['Ainchay','⛓'],['Ainbodychay','🦺'],
['Ashway','✨'],['Ustday','🌫'],['Essenceay','💎'],['Agmentfray','🔷'],['Ystalcray','💎'],['Orbway','🔮'],
['Eadhay','💀'],['Awclay','🦂'],['Angfay','🦷'],['Entacletay','🐙'],['Awjay','🦷'],['Isage','🐲'],
['Igillsay','✨'],['Iltshay','⚔'],['Eedsay','🌱'],['Elixirway','✨'],
['Ollscray','📜'],['Ournaljay','📓'],['Apmay','🗺'],['Eykay','🔑'],['Askmay','🎭'],
['Ossilfay','🪨'],['Ellshay','🐚'],['Orbhay','🧬'],['Arbay','🟤'],
['Athay','🎩'],['Aptchay','🎩'],
['Irefay Apecay','🔥'],['Infernalway Apecay','🔥'],
// Food items - fruits and crops
['Apple','🍎'],['Redberry','🍒'],['Dwellberry','🫐'],['Jangerberry','🍇'],['Wildberry','🍓'],
['Banana','🍌'],['Orange','🍊'],['Lemon','🍋'],['Pineapple','🍍'],
['Cabbage','🥬'],['Potato','🥔'],['Onion','🧅'],['Grain','🌾']
];
function getItemIco(name){for(const[kw,ico]of itemIcoMap){if(name.indexOf(kw)>=0)return ico}return'📦'}
function getItemDesc(name,uid){
// Check itemDB for unique stats first
if(uid&&typeof itemDB!=='undefined'&&itemDB[uid]){const u=itemDB[uid];
if(u.slot)return{desc:'Equippable gear — '+u.slot+' ['+u.uid+']',stats:'ATK +'+u.atk+' DEF +'+u.def+' STR +'+u.str,use:'Click to equip (stats vary per drop!)'};
if(u.atk||u.def||u.str)return{desc:'Item ['+u.uid+']',stats:'ATK +'+u.atk+' DEF +'+u.def+' STR +'+u.str,use:''}}
const sl=typeof specialLoot!=='undefined'?specialLoot.find(l=>l.name===name):null;
if(sl)return{desc:'Equippable gear — '+sl.slot,stats:'ATK +'+sl.atk+' DEF +'+sl.def+' STR +'+sl.str,use:'Click to equip'};
// Check name-based gear detection
const gearInfo=getGearSlotFromName(name);
if(gearInfo)return{desc:'Equippable gear — '+gearInfo.slot,stats:'ATK +'+gearInfo.atk+' DEF +'+gearInfo.def+' STR +'+gearInfo.str,use:'Click to equip'};
if(typeof skillItems!=='undefined'&&skillItems[name]){const sk=skillItems[name];const healInfo=sk.heal?'Heal '+sk.heal+' HP':'';return{desc:sk.skill+' resource'+(sk.heal?' — Food item':''),stats:healInfo+' +'+(sk.xp||10)+' '+sk.skill+' XP',use:sk.heal?'Click to eat and heal':'Click to use'}}
if(name.indexOf('Oinscay')>=0)return{desc:'Currency',stats:'',use:'Gold coins'};
if(name.indexOf('Onesbay')>=0)return{desc:'Prayer item — bury for XP',stats:'',use:'Click to bury'};
if(name.indexOf('Uneray')>=0)return{desc:'Magic rune for spellcasting',stats:'',use:'Used in spells'};
if(name.indexOf('Awray')>=0)return{desc:'Raw food — cook for better healing',stats:'',use:'Click to cook'};
return{desc:'Miscellaneous item',stats:'',use:''}}
const ttEl=document.getElementById('item-tooltip');
function showTooltip(e,item,uid){
const ico=getItemIco(item);const info=getItemDesc(item,uid||null);
ttEl.querySelector('.tt-ico').textContent=ico;
ttEl.querySelector('.tt-name').textContent=item;
ttEl.querySelector('.tt-desc').textContent=info.desc;
ttEl.querySelector('.tt-stats').textContent=info.stats;
ttEl.querySelector('.tt-use').textContent=info.use;
ttEl.style.display='block';
const x=Math.min(e.clientX+12,innerWidth-270);const y=Math.max(e.clientY-80,8);
ttEl.style.left=x+'px';ttEl.style.top=y+'px'}
function hideTooltip(){ttEl.style.display='none'}
// Inventory context menu handlers
const ctxMenu=document.getElementById('inv-context-menu');
const ctxEquip=document.getElementById('ctx-equip');
const ctxDrop=document.getElementById('ctx-drop');
let ctxSlotIndex=null;
function hideContextMenu(){ctxMenu.style.display='none';ctxSlotIndex=null}
function getGearSlotFromName(name){
const n=name.toLowerCase();
// Helmets
if(n.includes('helm')||n.includes('coif')||n.includes('hat')||n.includes('hood')||n.includes('cowl'))return{slot:'Helm',atk:0,def:3,str:0};
// Chest
if(n.includes('platebody')||n.includes('chainbody')||n.includes('robe top')||n.includes('shirt')||n.includes('chest'))return{slot:'Chest',atk:0,def:5,str:0};
// Legs
if(n.includes('platelegs')||n.includes('plateskirt')||n.includes('chaps')||n.includes('robe bottom')||n.includes('tassets')||n.includes('legs'))return{slot:'Legs',atk:0,def:4,str:0};
// Weapon
if(n.includes('sword')||n.includes('scimitar')||n.includes('dagger')||n.includes('mace')||n.includes('battleaxe')||n.includes('halberd')||n.includes('spear')||n.includes('whip')||n.includes('claws'))return{slot:'Weapon',atk:5,def:0,str:3};
// Shield
if(n.includes('shield')||n.includes('defender')||n.includes('buckler'))return{slot:'Shield',atk:0,def:5,str:0};
// Boots
if(n.includes('boots')||n.includes('shoes')||n.includes('sandals'))return{slot:'Boots',atk:0,def:1,str:0};
// Gloves
if(n.includes('gloves')||n.includes('gauntlets')||n.includes('vambraces')||n.includes('bracelet'))return{slot:'Gloves',atk:0,def:1,str:0};
// Ring
if(n.includes('ring')||n.includes('seers')||n.includes('warrior')||n.includes('archers'))return{slot:'Ring',atk:0,def:0,str:0};
// Offhand
if(n.includes('offhand')||n.includes('orb')||n.includes('book')||n.includes('torch'))return{slot:'OffHand',atk:0,def:2,str:0};
// Cape
if(n.includes('cape')||n.includes('cloak'))return{slot:'Cape',atk:0,def:1,str:0};
// Ammo
if(n.includes('arrow')||n.includes('bolt')||n.includes('dart')||n.includes('knife')||n.includes('throwing'))return{slot:'Ammo',atk:2,def:0,str:0};
return null}
function equipItem(index){
const raw=inventory[index];if(!raw)return;
const itemName=typeof raw==='string'?raw:raw.name;const itemUID=typeof raw==='object'?raw.uid:null;
// Check itemDB for gear
if(itemUID&&typeof itemDB!=='undefined'&&itemDB[itemUID]&&itemDB[itemUID].slot){
const u=itemDB[itemUID];const old=equipped[u.slot];
equipped[u.slot]={name:u.name,atk:u.atk,def:u.def,str:u.str};
inventory.splice(index,1);
if(old&&old.name!=='None')inventory.push({name:old.name,uid:null});
log('Equipped '+u.name+' [ATK+'+u.atk+' DEF+'+u.def+' STR+'+u.str+']','#0ff');updateInvUI();updateEqUI();return true}
// Check specialLoot
const sl=typeof specialLoot!=='undefined'?specialLoot.find(l=>l.name===itemName):null;
if(sl){const old=equipped[sl.slot];equipped[sl.slot]={name:sl.name,atk:sl.atk,def:sl.def,str:sl.str};
inventory.splice(index,1);
if(old&&old.name!=='None')inventory.push({name:old.name,uid:null});
log('Equipped '+sl.name+' [ATK+'+sl.atk+' DEF+'+sl.def+' STR+'+sl.str+']','#0ff');updateInvUI();updateEqUI();return true}
// Check name-based gear detection
const gearInfo=getGearSlotFromName(itemName);
if(gearInfo){const old=equipped[gearInfo.slot];equipped[gearInfo.slot]={name:itemName,atk:gearInfo.atk,def:gearInfo.def,str:gearInfo.str};
inventory.splice(index,1);
if(old&&old.name!=='None')inventory.push({name:old.name,uid:null});
log('Equipped '+itemName+' [ATK+'+gearInfo.atk+' DEF+'+gearInfo.def+' STR+'+gearInfo.str+']','#0ff');updateInvUI();updateEqUI();return true}
return false}
function dropItem(index){
const raw=inventory[index];if(!raw)return;
const itemName=typeof raw==='string'?raw:raw.name;
inventory.splice(index,1);
log('Dropped '+itemName,'#f80');
// Spawn loot on ground near player
const dropX=player.x+(Math.random()-.5)*8;
const dropZ=player.z+(Math.random()-.5)*8;
spawnLoot(dropX,dropZ,{lv:1,type:'drop'});
updateInvUI()}
// Context menu click handlers
ctxEquip.onclick=()=>{if(ctxSlotIndex!==null){equipItem(ctxSlotIndex);hideContextMenu();}}
ctxDrop.onclick=()=>{if(ctxSlotIndex!==null){dropItem(ctxSlotIndex);hideContextMenu();}}
// Close context menu on click elsewhere
document.addEventListener('click',(e)=>{if(!ctxMenu.contains(e.target))hideContextMenu();});
function updateInvUI(){for(let i=0;i<28;i++){const el=document.getElementById('inv-'+i);
el.innerHTML='';el.onclick=null;el.onmouseenter=null;el.onmouseleave=null;el.onmousemove=null;el.oncontextmenu=null;
if(inventory[i]){
const raw=inventory[i];const itemName=typeof raw==='string'?raw:raw.name;const itemUID=typeof raw==='object'?raw.uid:null;
const ico=getItemIco(itemName);
el.innerHTML='<span class="inv-ico">'+ico+'</span><span class="inv-name">'+itemName+'</span>';
el.onmouseenter=(ev)=>{const d=getItemDesc(itemName,itemUID);ttEl.querySelector('.tt-ico').textContent=ico;ttEl.querySelector('.tt-name').textContent=itemName;
ttEl.querySelector('.tt-desc').textContent=d.desc;ttEl.querySelector('.tt-stats').textContent=d.stats;ttEl.querySelector('.tt-use').textContent=d.use;
ttEl.style.display='block';const x=Math.min(ev.clientX+12,innerWidth-270);const y=Math.max(ev.clientY-80,8);ttEl.style.left=x+'px';ttEl.style.top=y+'px'};
el.onmouseleave=hideTooltip;
el.onmousemove=(ev)=>{const x=Math.min(ev.clientX+12,innerWidth-270);const y=Math.max(ev.clientY-80,8);ttEl.style.left=x+'px';ttEl.style.top=y+'px'};
// Right-click context menu
el.oncontextmenu=(ev)=>{ev.preventDefault();ctxSlotIndex=i;
const isGear=(itemUID&&typeof itemDB!=='undefined'&&itemDB[itemUID]&&itemDB[itemUID].slot)||(typeof specialLoot!=='undefined'&&specialLoot.find(l=>l.name===itemName))||getGearSlotFromName(itemName);
ctxEquip.style.display=isGear?'block':'none';
const x=Math.min(ev.clientX,innerWidth-140);const y=Math.min(ev.clientY,innerHeight-60);
ctxMenu.style.left=x+'px';ctxMenu.style.top=y+'px';ctxMenu.style.display='block';};
// Left-click quick equip for gear, use for skill items
el.onclick=()=>{
// Check itemDB for gear
if(itemUID&&typeof itemDB!=='undefined'&&itemDB[itemUID]&&itemDB[itemUID].slot){
const u=itemDB[itemUID];const old=equipped[u.slot];
equipped[u.slot]={name:u.name,atk:u.atk,def:u.def,str:u.str};
inventory.splice(i,1);
if(old&&old.name!=='None')inventory.push({name:old.name,uid:null});
log('Equipped '+u.name+' [ATK+'+u.atk+' DEF+'+u.def+' STR+'+u.str+']','#0ff');hideTooltip();updateInvUI();updateEqUI();return}
const sl=typeof specialLoot!=='undefined'?specialLoot.find(l=>l.name===itemName):null;
if(sl){const old=equipped[sl.slot];equipped[sl.slot]={name:sl.name,atk:sl.atk,def:sl.def,str:sl.str};
inventory.splice(i,1);
if(old&&old.name!=='None')inventory.push({name:old.name,uid:null});
log('Equipped '+sl.name+' [ATK+'+sl.atk+' DEF+'+sl.def+' STR+'+sl.str+']','#0ff');hideTooltip();updateInvUI();updateEqUI();return}
// Check name-based gear detection
const gearInfo=getGearSlotFromName(itemName);
if(gearInfo){const old=equipped[gearInfo.slot];equipped[gearInfo.slot]={name:itemName,atk:gearInfo.atk,def:gearInfo.def,str:gearInfo.str};
inventory.splice(i,1);
if(old&&old.name!=='None')inventory.push({name:old.name,uid:null});
log('Equipped '+itemName+' [ATK+'+gearInfo.atk+' DEF+'+gearInfo.def+' STR+'+gearInfo.str+']','#0ff');hideTooltip();updateInvUI();updateEqUI();return}
if(typeof skillItems!=='undefined'&&skillItems[itemName]){const sk=skillItems[itemName];inventory.splice(i,1);
// If food item with heal, restore HP
if(sk.heal&&player.hp<player.maxHp){player.hp=Math.min(player.hp+sk.heal,player.maxHp);hitFX(player.x,player.y+6,player.z,0x44cc44);log('Ate '+itemName+' +'+sk.heal+' HP','#4c4');}
skills[sk.skill].xp+=sk.xp;const lv=Math.max(skills[sk.skill].lvl,Math.floor(1+Math.sqrt(skills[sk.skill].xp/50)));
if(lv>skills[sk.skill].lvl){skills[sk.skill].lvl=lv;log(sk.skill+' level up! Lv '+lv,'#ff0')}
log('Used '+itemName+': '+sk.skill+' +'+sk.xp+'xp'+(sk.heal?' +'+sk.heal+'HP':''),'#cc4');hideTooltip();updateInvUI();if(typeof updateSkillUI==='function')updateSkillUI();updateXpBar();return}
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

// === ABILITY BROWSER + CUSTOMIZABLE ACTION BAR ===
const allAbilities=[
{id:'attack',name:'Attack',ico:'⚔',cat:'Combat',desc:'Melee attack',key:'1'},
{id:'parry',name:'Parry',ico:'🛡',cat:'Combat',desc:'Block/riposte',key:'2'},
{id:'heal',name:'Heal',ico:'🍷',cat:'Combat',desc:'Estus Flask heal',key:'3'},
{id:'bones',name:'Bury Bones',ico:'🦴',cat:'Prayer',desc:'Bury bones for XP',key:'4'},
{id:'prayer',name:'Prayer',ico:'✝',cat:'Prayer',desc:'Open prayer tab',key:'5'},
{id:'gather',name:'Gather',ico:'⛏',cat:'Skilling',desc:'Gather resources',key:'6'},
{id:'roll',name:'Roll',ico:'💨',cat:'Combat',desc:'Dodge roll',key:'7'},
{id:'lock',name:'Lock On',ico:'🎯',cat:'Combat',desc:'Cycle target lock',key:'8'},
{id:'map',name:'Map',ico:'🗺',cat:'Utility',desc:'World map',key:'9'},
{id:'inv',name:'Inventory',ico:'🎒',cat:'Utility',desc:'Open inventory',key:'10'},
{id:'skills',name:'Skills',ico:'⭐',cat:'Utility',desc:'Open skills',key:'11'},
{id:'save',name:'Save',ico:'💾',cat:'Utility',desc:'Quick save',key:'12'},
{id:'jump',name:'Jump',ico:'⬆',cat:'Combat',desc:'Jump',key:'Z'},
{id:'dash_left',name:'Dash Left',ico:'⬅',cat:'Combat',desc:'Quick dash left',key:'Q'},
{id:'dash_right',name:'Dash Right',ico:'➡',cat:'Combat',desc:'Quick dash right',key:'E'},
{id:'teleport',name:'Teleport',ico:'⚡',cat:'Magic',desc:'Open teleport menu',key:'T'},
{id:'autoloot',name:'Auto-Loot',ico:'💰',cat:'Utility',desc:'Toggle auto-loot',key:'L'},
{id:'wind_strike',name:'Wind Strike',ico:'🌬',cat:'Magic',desc:'Lv1 wind spell',key:''},
{id:'water_strike',name:'Water Strike',ico:'💧',cat:'Magic',desc:'Lv5 water spell',key:''},
{id:'earth_strike',name:'Earth Strike',ico:'🌍',cat:'Magic',desc:'Lv9 earth spell',key:''},
{id:'fire_strike',name:'Fire Strike',ico:'🔥',cat:'Magic',desc:'Lv13 fire spell',key:''},
{id:'wind_bolt',name:'Wind Bolt',ico:'🌪',cat:'Magic',desc:'Lv17 wind bolt',key:''},
{id:'water_bolt',name:'Water Bolt',ico:'🌊',cat:'Magic',desc:'Lv23 water bolt',key:''},
{id:'earth_bolt',name:'Earth Bolt',ico:'⛰',cat:'Magic',desc:'Lv29 earth bolt',key:''},
{id:'fire_bolt',name:'Fire Bolt',ico:'☄',cat:'Magic',desc:'Lv35 fire bolt',key:''},
{id:'wind_blast',name:'Wind Blast',ico:'🌬',cat:'Magic',desc:'Lv41 wind blast',key:''},
{id:'fire_blast',name:'Fire Blast',ico:'💥',cat:'Magic',desc:'Lv59 fire blast',key:''},
{id:'confuse',name:'Confuse',ico:'💫',cat:'Magic',desc:'Lower enemy accuracy',key:''},
{id:'weaken',name:'Weaken',ico:'💀',cat:'Magic',desc:'Lower enemy strength',key:''},
{id:'curse',name:'Curse',ico:'😈',cat:'Magic',desc:'Lower enemy defence',key:''},
{id:'low_alch',name:'Low Alchemy',ico:'🪙',cat:'Magic',desc:'Turn item to gold',key:''},
{id:'high_alch',name:'High Alchemy',ico:'🥇',cat:'Magic',desc:'Turn item to more gold',key:''},
{id:'bones2ban',name:'Bones to Bananas',ico:'🍌',cat:'Magic',desc:'Convert bones to food',key:''},
{id:'enchant1',name:'Enchant Lv1',ico:'💎',cat:'Magic',desc:'Enchant sapphire jewelry',key:''},
{id:'spec_atk',name:'Special Attack',ico:'⚡',cat:'Combat',desc:'Weapon special attack',key:''},
{id:'shoot',name:'Shoot Arrow',ico:'🏹',cat:'Combat',desc:'Fire arrow at cursor',key:'4'},
{id:'protect_melee',name:'Protect Melee',ico:'⚔',cat:'Prayer',desc:'50% melee reduction',key:''},
{id:'protect_magic',name:'Protect Magic',ico:'🔮',cat:'Prayer',desc:'50% magic reduction',key:''},
{id:'protect_range',name:'Protect Range',ico:'🏹',cat:'Prayer',desc:'50% range reduction',key:''},
{id:'smite',name:'Smite',ico:'💢',cat:'Prayer',desc:'Drain enemy prayer',key:''},
{id:'piety',name:'Piety',ico:'🙏',cat:'Prayer',desc:'Boost atk/str/def',key:''},
{id:'rigour',name:'Rigour',ico:'🎯',cat:'Prayer',desc:'Boost ranged/def',key:''},
{id:'augury',name:'Augury',ico:'✨',cat:'Prayer',desc:'Boost magic/def',key:''},
{id:'fish',name:'Fish',ico:'🎣',cat:'Skilling',desc:'Fish at fishing spots',key:''},
{id:'cook',name:'Cook',ico:'🍳',cat:'Skilling',desc:'Cook raw food',key:''},
{id:'woodcut',name:'Woodcut',ico:'🪓',cat:'Skilling',desc:'Chop trees',key:''},
{id:'mine',name:'Mine',ico:'⛏',cat:'Skilling',desc:'Mine rocks',key:''},
{id:'smith',name:'Smith',ico:'🔨',cat:'Skilling',desc:'Smith bars at anvil',key:''},
{id:'craft',name:'Craft',ico:'✂',cat:'Skilling',desc:'Craft items',key:''},
{id:'fletch',name:'Fletch',ico:'🏹',cat:'Skilling',desc:'Fletch bows/arrows',key:''},
// === WARRIOR ABILITIES (10) ===
{id:'heroic_strike',name:'Heroic Strike',ico:'⚔',cat:'Combat',desc:'Warrior: Powerful melee strike',key:''},
{id:'cleave',name:'Cleave',ico:'🪓',cat:'Combat',desc:'Warrior: Attack multiple enemies',key:''},
{id:'whirlwind',name:'Whirlwind',ico:'🌪',cat:'Combat',desc:'Warrior: Spinning blade attack',key:''},
{id:'thunder_clap',name:'Thunder Clap',ico:'⛈',cat:'Combat',desc:'Warrior: AoE thunder damage',key:''},
{id:'battle_shout',name:'Battle Shout',ico:'📢',cat:'Combat',desc:'Warrior: Boost attack power',key:''},
{id:'execute',name:'Execute',ico:'💀',cat:'Combat',desc:'Warrior: Finishing blow',key:''},
{id:'slam',name:'Slam',ico:'🔨',cat:'Combat',desc:'Warrior: Heavy weapon slam',key:''},
{id:'overpower',name:'Overpower',ico:'💪',cat:'Combat',desc:'Warrior: Counter attack',key:''},
{id:'shield_slam',name:'Shield Slam',ico:'🛡',cat:'Combat',desc:'Warrior: Shield bash attack',key:''},
{id:'recklessness',name:'Recklessness',ico:'😤',cat:'Combat',desc:'Warrior: Critical strike boost',key:''},
// === KNIGHT ABILITIES (10) ===
{id:'judgment',name:'Judgment',ico:'⚖',cat:'Combat',desc:'Knight: Holy strike',key:''},
{id:'crusader_strike',name:'Crusader Strike',ico:'✝',cat:'Combat',desc:'Knight: Righteous attack',key:''},
{id:'divine_protection',name:'Divine Protection',ico:'🛡',cat:'Combat',desc:'Knight: Damage reduction',key:''},
{id:'consecration',name:'Consecration',ico:'✨',cat:'Combat',desc:'Knight: Holy ground AoE',key:''},
{id:'holy_light',name:'Holy Light',ico:'💡',cat:'Combat',desc:'Knight: Heal spell',key:''},
{id:'flash_light',name:'Flash of Light',ico:'⚡',cat:'Combat',desc:'Knight: Quick heal',key:''},
{id:'blessing_might',name:'Blessing of Might',ico:'💪',cat:'Combat',desc:'Knight: Attack buff',key:''},
{id:'divine_shield',name:'Divine Shield',ico:'🔮',cat:'Combat',desc:'Knight: Invulnerability',key:''},
{id:'hammer_justice',name:'Hammer of Justice',ico:'🔨',cat:'Combat',desc:'Knight: Stun attack',key:''},
{id:'exorcism',name:'Exorcism',ico:'👻',cat:'Combat',desc:'Knight: Undead damage',key:''},
// === SORCERER ABILITIES (10) ===
{id:'fireball',name:'Fireball',ico:'🔥',cat:'Magic',desc:'Sorcerer: Fire projectile',key:''},
{id:'frostbolt',name:'Frostbolt',ico:'❄',cat:'Magic',desc:'Sorcerer: Ice slow spell',key:''},
{id:'arcane_missiles',name:'Arcane Missiles',ico:'✦',cat:'Magic',desc:'Sorcerer: Multi-missile',key:''},
{id:'blizzard',name:'Blizzard',ico:'🌨',cat:'Magic',desc:'Sorcerer: Ice storm AoE',key:''},
{id:'sorc_fire_blast',name:'Fire Blast',ico:'💥',cat:'Magic',desc:'Sorcerer: Instant fire',key:''},
{id:'pyroblast',name:'Pyroblast',ico:'☄',cat:'Magic',desc:'Sorcerer: Massive fireball',key:''},
{id:'frost_nova',name:'Frost Nova',ico:'❄',cat:'Magic',desc:'Sorcerer: Ice nova root',key:''},
{id:'blink',name:'Blink',ico:'💫',cat:'Magic',desc:'Sorcerer: Teleport dash',key:''},
{id:'polymorph',name:'Polymorph',ico:'🐑',cat:'Magic',desc:'Sorcerer: Transform enemy',key:''},
{id:'counterspell',name:'Counterspell',ico:'🚫',cat:'Magic',desc:'Sorcerer: Silence enemy',key:''},
// === RANGER ABILITIES (10) ===
{id:'steady_shot',name:'Steady Shot',ico:'🏹',cat:'Combat',desc:'Ranger: Precise arrow',key:''},
{id:'aimed_shot',name:'Aimed Shot',ico:'🎯',cat:'Combat',desc:'Ranger: High damage shot',key:''},
{id:'multi_shot',name:'Multi-Shot',ico:'📐',cat:'Combat',desc:'Ranger: Three arrows',key:''},
{id:'arcane_shot',name:'Arcane Shot',ico:'⚡',cat:'Combat',desc:'Ranger: Magic arrow',key:''},
{id:'serpent_sting',name:'Serpent Sting',ico:'🐍',cat:'Combat',desc:'Ranger: Poison arrow',key:''},
{id:'hunters_mark',name:'Hunters Mark',ico:'👁',cat:'Combat',desc:'Ranger: Mark target',key:''},
{id:'distracting_shot',name:'Distracting Shot',ico:'👋',cat:'Combat',desc:'Ranger: Taunt shot',key:''},
{id:'rapid_fire',name:'Rapid Fire',ico:'🔥',cat:'Combat',desc:'Ranger: Speed boost',key:''},
{id:'feign_death',name:'Feign Death',ico:'💀',cat:'Combat',desc:'Ranger: Drop aggro',key:''},
{id:'explosive_trap',name:'Explosive Trap',ico:'💣',cat:'Combat',desc:'Ranger: Fire trap',key:''},
// === GENERAL ABILITIES (10) ===
{id:'first_aid',name:'First Aid',ico:'🩹',cat:'Utility',desc:'Heal over time',key:''},
{id:'bandage',name:'Bandage',ico:'🤕',cat:'Utility',desc:'Quick heal',key:''},
{id:'sharpen_weapon',name:'Sharpen Weapon',ico:'🔪',cat:'Utility',desc:'Weapon buff',key:''},
{id:'mining_strike',name:'Mining Strike',ico:'⛏',cat:'Skilling',desc:'Strong mining hit',key:''},
{id:'lumber_up',name:'Lumber Up',ico:'🌲',cat:'Skilling',desc:'Woodcutting boost',key:''},
{id:'cooking_fire',name:'Cooking Fire',ico:'🔥',cat:'Skilling',desc:'Create campfire',key:''},
{id:'fishing_cast',name:'Fishing Cast',ico:'🎣',cat:'Skilling',desc:'Long cast bonus',key:''},
{id:'runecraft_focus',name:'Runecraft Focus',ico:'🔮',cat:'Skilling',desc:'Rune bonus XP',key:''},
{id:'sneak_attack',name:'Sneak Attack',ico:'🗡',cat:'Combat',desc:'Thief backstab',key:''},
{id:'agility_roll',name:'Agility Roll',ico:'🤸',cat:'Utility',desc:'Fast escape roll',key:''}
];
const abCategories=['All','Combat','Magic','Prayer','Skilling','Utility'];
// Action bar slot assignments (customizable)
const abSlots=document.querySelectorAll('#ab-wrap .ab-slot');
let abAssign=[];abSlots.forEach(s=>abAssign.push(s.dataset.action));
// Update slot 4 to shoot for ranger or if shoot ability is available
abAssign[3]='shoot';
// Build ability browser
const abBrowser=document.getElementById('ability-browser');
const abCatsEl=document.getElementById('ab-cats');
const abListEl=document.getElementById('ab-list');
document.getElementById('ab-close').onclick=()=>abBrowser.classList.remove('active');
let abCurCat='All';
function buildAbCats(){abCatsEl.innerHTML='';abCategories.forEach(c=>{
const d=document.createElement('div');d.className='ab-cat'+(c===abCurCat?' active':'');d.textContent=c;
d.onclick=()=>{abCurCat=c;buildAbCats();buildAbList()};abCatsEl.appendChild(d)})}
function buildAbList(){abListEl.innerHTML='';
const filtered=abCurCat==='All'?allAbilities:allAbilities.filter(a=>a.cat===abCurCat);
filtered.forEach(ab=>{const d=document.createElement('div');d.className='ab-item';d.draggable=true;
d.innerHTML='<span class="abi-ico">'+ab.ico+'</span><span class="abi-name">'+ab.name+'</span><span class="abi-desc">'+ab.desc+'</span>';
d.addEventListener('dragstart',e=>{e.dataTransfer.setData('text/plain',ab.id);e.dataTransfer.effectAllowed='copy'});
abListEl.appendChild(d)})}
buildAbCats();buildAbList();

// === SPELL BOOK ===
const allSpells=allAbilities.filter(a=>a.cat==='Magic');
const sbCats=['All Magic','Fire','Frost','Arcane','Strike','Bolt','Blast','Utility'];
const sbBrowser=document.getElementById('spell-book');
const sbCatsEl=document.getElementById('sb-cats');
const sbListEl=document.getElementById('sb-list');
document.getElementById('sb-close').onclick=()=>sbBrowser.classList.remove('active');
let sbCurCat='All Magic';
function buildSbCats(){sbCatsEl.innerHTML='';sbCats.forEach(c=>{
const d=document.createElement('div');d.className='sb-cat'+(c===sbCurCat?' active':'');d.textContent=c;
d.onclick=()=>{sbCurCat=c;buildSbCats();buildSbList()};sbCatsEl.appendChild(d)})}
function buildSbList(){sbListEl.innerHTML='';
let filtered;
if(sbCurCat==='All Magic')filtered=allSpells;
else if(sbCurCat==='Utility')filtered=allSpells.filter(s=>['low_alch','high_alch','confuse','weaken','curse','bind','snare','entangle'].includes(s.id));
else if(sbCurCat==='Fire')filtered=allSpells.filter(s=>['fire_strike','fire_bolt','fire_blast','fireball','sorc_fire_blast','pyroblast'].includes(s.id));
else if(sbCurCat==='Frost')filtered=allSpells.filter(s=>['frostbolt','blizzard','frost_nova','ice_barrage'].includes(s.id));
else if(sbCurCat==='Arcane')filtered=allSpells.filter(s=>['arcane_missiles','blink','polymorph','counterspell'].includes(s.id));
else filtered=allSpells.filter(s=>s.id.indexOf(sbCurCat.toLowerCase())>=0);
filtered.forEach(sp=>{const d=document.createElement('div');d.className='sb-item';d.draggable=true;
d.innerHTML='<span class="sbi-ico">'+sp.ico+'</span><span class="sbi-name">'+sp.name+'</span><span class="sbi-desc">'+sp.desc+'</span>';
d.addEventListener('dragstart',e=>{e.dataTransfer.setData('text/plain',sp.id);e.dataTransfer.effectAllowed='copy'});
sbListEl.appendChild(d)})}
buildSbCats();buildSbList();

// Make action bar slots accept drops
abSlots.forEach((slot,idx)=>{
slot.addEventListener('dragover',e=>{e.preventDefault();e.dataTransfer.dropEffect='copy';slot.classList.add('drag-over')});
slot.addEventListener('dragleave',()=>slot.classList.remove('drag-over'));
slot.addEventListener('drop',e=>{e.preventDefault();slot.classList.remove('drag-over');
const abId=e.dataTransfer.getData('text/plain');const ab=allAbilities.find(a=>a.id===abId);
if(ab){abAssign[idx]=ab.id;slot.dataset.action=ab.id;
slot.querySelector('.ab-ico').textContent=ab.ico;
slot.querySelector('.ab-name').textContent=ab.name;
slot.querySelector('.ab-key').textContent=ab.key||(idx<9?(idx+1)+'':'');
log('Assigned '+ab.name+' to slot '+(idx+1),'#ffd700')}})});
// Execute ability by action ID
// Helper: get world position under the mouse cursor (ground plane intersection)
function getCursorWorldPos(){
if(!cam)return null;
const rc=new THREE.Raycaster();
rc.setFromCamera({x:mouse.x,y:mouse.y},cam);
const planeY=meshTerrainH(player.x,player.z);
const plane=new THREE.Plane(new THREE.Vector3(0,1,0),-planeY);
const target=new THREE.Vector3();
if(!rc.ray.intersectPlane(plane,target))return null;
return{x:target.x,z:target.z,y:planeY};}
function execAbility(id){
if(id==='attack')document.dispatchEvent(new KeyboardEvent('keydown',{key:'1'}));
else if(id==='parry')document.dispatchEvent(new KeyboardEvent('keydown',{key:'2'}));
else if(id==='heal')document.dispatchEvent(new KeyboardEvent('keydown',{key:'3'}));
else if(id==='bones')document.dispatchEvent(new KeyboardEvent('keydown',{key:'4'}));
else if(id==='prayer')switchTab('prayer');
else if(id==='gather')document.dispatchEvent(new KeyboardEvent('keydown',{key:'g'}));
else if(id==='roll')document.dispatchEvent(new KeyboardEvent('keydown',{key:' '}));
else if(id==='lock'){if(typeof toggleLock==='function')toggleLock()}
else if(id==='map')document.dispatchEvent(new KeyboardEvent('keydown',{key:'m'}));
else if(id==='inv')switchTab('inventory');
else if(id==='skills')switchTab('skills');
else if(id==='save')document.dispatchEvent(new KeyboardEvent('keydown',{key:'F5'}));
else if(id==='jump'){if(typeof player!=='undefined'&&player.grounded&&player.sta>10){player.vy=6.5;player.grounded=false;player.sta-=10}}
else if(id==='dash_left'){if(typeof player!=='undefined'&&player.sta>15&&!player.dashing){
const dashDist=6;
const right=new THREE.Vector3(-Math.cos(camYaw),0,Math.sin(camYaw));
player.x+=right.x*dashDist;player.z+=right.z*dashDist;
player.sta-=15;player.dashing=true;player.dashT=12;player.dashDir=-1;
hitFX(player.x+right.x*2,player.y+4,player.z+right.z*2,0x00ffff);
hitFX(player.x+right.x*3,player.y+2,player.z+right.z*3,0x0088ff);
log('Dash left!','#0ff');setTimeout(()=>player.dashing=false,200);}}
else if(id==='dash_right'){if(typeof player!=='undefined'&&player.sta>15&&!player.dashing){
const dashDist=6;
const right=new THREE.Vector3(-Math.cos(camYaw),0,Math.sin(camYaw));
player.x-=right.x*dashDist;player.z-=right.z*dashDist;
player.sta-=15;player.dashing=true;player.dashT=12;player.dashDir=1;
hitFX(player.x-right.x*2,player.y+4,player.z-right.z*2,0x00ffff);
hitFX(player.x-right.x*3,player.y+2,player.z-right.z*3,0x0088ff);
log('Dash right!','#0ff');setTimeout(()=>player.dashing=false,200);}}
else if(id==='teleport')document.dispatchEvent(new KeyboardEvent('keydown',{key:'t'}));
else if(id==='autoloot')document.dispatchEvent(new KeyboardEvent('keydown',{key:'l'}));
else if(id==='spec_atk'){if(typeof player!=='undefined'&&!player._specCD){log('Special Attack!','#ff0');player._specCD=120}}
else if(id==='shoot'){if(typeof player!=='undefined'&&!player._shootCD){const cd=player._rapidFireActive?24:40;player._shootCD=cd;shootProjectile('arrow',12+skills.Ranged.lvl);log('Shot arrow!','#8a4');}}
else if(id.indexOf('protect_')===0||id==='smite'||id==='piety'||id==='rigour'||id==='augury'){log('Activated: '+id.replace(/_/g,' '),'#4cf')}
else if((id.indexOf('strike')>=0||id.indexOf('bolt')>=0||id.indexOf('blast')>=0||id.indexOf('wave')>=0||id.indexOf('surge')>=0)&&!['heroic_strike','crusader_strike','frostbolt','sorc_fire_blast','mining_strike'].includes(id)){
// Magic combat spells - fire projectile toward cursor (excludes warrior/knight/sorcerer/general abilities)
const manaCost=id.indexOf('strike')>=0?5:id.indexOf('bolt')>=0?10:id.indexOf('blast')>=0?15:id.indexOf('wave')>=0?20:25;
if(player.poi<manaCost){log('Not enough mana! ('+manaCost+' needed)','#f44');return;}
player.poi-=manaCost;
const spellCol=id.indexOf('wind')>=0?0x88aabb:id.indexOf('water')>=0?0x2288ff:id.indexOf('earth')>=0?0x664422:id.indexOf('fire')>=0?0xff4400:0x6644ff;
const baseDmg=id.indexOf('strike')>=0?12:id.indexOf('bolt')>=0?20:id.indexOf('blast')>=0?28:id.indexOf('wave')>=0?36:45;
shootProjectile('spell',baseDmg+skills.Magic.lvl,spellCol);
log('Cast '+id.replace(/_/g,' ')+'! (-'+manaCost+' mana)','#48f');}
else if(id==='low_alch'||id==='high_alch'){const gold=id==='high_alch'?'60':'30';log('Alchemy: +'+gold+' gold','#ff0');skills.Magic.xp+=25;updateXpBar();}
else if(id==='confuse'||id==='weaken'||id==='curse'){if(player.poi<8){log('Not enough mana! (8 needed)','#f44');return;}player.poi-=8;shootProjectile('spell',5,0x6644aa);if(typeof lockOn!=='undefined'&&lockOn){lockOn.poi=Math.max(0,lockOn.poi-20);log('Cast '+id+'! Enemy weakened (-8 mana)','#48f');skills.Magic.xp+=20;updateXpBar();}}
else if(id==='bind'||id==='snare'||id==='entangle'){if(player.poi<12){log('Not enough mana! (12 needed)','#f44');return;}player.poi-=12;shootProjectile('spell',5,0x00aa44);if(typeof lockOn!=='undefined'&&lockOn){lockOn.staggered=true;lockOn.staggerT=60;log('Cast '+id+'! Enemy immobilized (-12 mana)','#48f');skills.Magic.xp+=30;updateXpBar();}}
else if(id==='telegrab'){shootProjectile('spell',0,0xaa44ff);log('Telegrab spell cast','#48f');skills.Magic.xp+=15;updateXpBar();}
else if(id==='superheat'){shootProjectile('spell',0,0xff8800);log('Superheat spell cast','#ff0');skills.Magic.xp+=35;updateXpBar();}
else if(id==='bones2ban'){shootProjectile('spell',0,0xffdd44);log('Bones converted to bananas!','#ff0');skills.Magic.xp+=20;updateXpBar();}
// === WARRIOR ABILITY EXECUTIONS ===
else if(id==='heroic_strike'){if(typeof player!=='undefined'&&!player._heroicCD&&lockOn){player._heroicCD=60;const dmg=15+skills.Attack.lvl+skills.Strength.lvl;lockOn.hp-=dmg;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+5,lockOn.mesh.position.z,0xff4400);log('Heroic Strike! '+dmg+' damage','#f44');skills.Attack.xp+=20;skills.Strength.xp+=15;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='cleave'){if(typeof player!=='undefined'&&!player._cleaveCD){player._cleaveCD=80;let hitCount=0;enemies.forEach(e=>{const dist=Math.hypot(e.x-player.x,e.z-player.z);if(dist<15){const dmg=8+skills.Strength.lvl;e.hp-=dmg;hitFX(e.mesh.position.x,e.mesh.position.y+5,e.mesh.position.z,0xff6600);hitCount++;}});log('Cleave hit '+hitCount+' enemies!','#f84');skills.Attack.xp+=15*hitCount;skills.Strength.xp+=10*hitCount;updateXpBar();}}
else if(id==='whirlwind'){if(typeof player!=='undefined'&&!player._whirlCD&&player.sta>20){player._whirlCD=100;player.sta-=20;for(let i=0;i<3;i++){setTimeout(()=>{hitFX(player.x+Math.random()*8-4,player.y+3,player.z+Math.random()*8-4,0xffaa00);enemies.forEach(e=>{const dist=Math.hypot(e.x-player.x,e.z-player.z);if(dist<12){const dmg=5+skills.Attack.lvl;e.hp-=dmg;}});},i*200);}log('Whirlwind!','#fa0');skills.Attack.xp+=25;skills.Strength.xp+=20;updateXpBar();}}
else if(id==='thunder_clap'){if(typeof player!=='undefined'&&!player._thunderCD){player._thunderCD=120;for(let i=0;i<20;i++){const ang=i*Math.PI*2/20;const tx=player.x+Math.cos(ang)*10;const tz=player.z+Math.sin(ang)*10;hitFX(tx,player.y+2,tz,0x4488ff);}enemies.forEach(e=>{const dist=Math.hypot(e.x-player.x,e.z-player.z);if(dist<12){const dmg=10+skills.Strength.lvl;e.hp-=dmg;e.staggered=true;e.staggerT=40;}});log('Thunder Clap! Enemies stunned','#48f');skills.Attack.xp+=20;skills.Strength.xp+=20;updateXpBar();}}
else if(id==='battle_shout'){if(typeof player!=='undefined'&&!player._shoutCD){player._shoutCD=600;player._battleShoutActive=true;setTimeout(()=>player._battleShoutActive=false,30000);for(let i=0;i<15;i++){hitFX(player.x+Math.random()*6-3,player.y+8+i,player.z+Math.random()*6-3,0xffdd00);}log('Battle Shout! Attack power +20% for 30s','#fd0');skills.Attack.xp+=30;updateXpBar();}}
else if(id==='execute'){if(typeof player!=='undefined'&&!player._executeCD&&lockOn){const enemyPct=lockOn.hp/lockOn.maxHp;if(enemyPct>0.2){log('Execute only works on enemies below 20% HP','#f80');}else{player._executeCD=90;const dmg=50+skills.Strength.lvl*2;lockOn.hp-=dmg;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+5,lockOn.mesh.position.z,0x880000);log('EXECUTE! '+dmg+' damage!','#f00');skills.Attack.xp+=35;skills.Strength.xp+=30;updateXpBar();}}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='slam'){if(typeof player!=='undefined'&&!player._slamCD&&lockOn){player._slamCD=70;const dmg=20+skills.Strength.lvl*1.5;lockOn.hp-=dmg;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y,lockOn.mesh.position.z,0x884422);log('Slam! '+dmg+' damage','#a62');skills.Attack.xp+=22;skills.Strength.xp+=18;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='overpower'){if(typeof player!=='undefined'&&!player._overpowerCD&&lockOn){player._overpowerCD=50;const dmg=12+skills.Attack.lvl;lockOn.hp-=dmg;lockOn.staggered=true;lockOn.staggerT=30;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+5,lockOn.mesh.position.z,0xff8800);log('Overpower! Counter attack '+dmg,'#f80');skills.Attack.xp+=18;skills.Strength.xp+=12;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='shield_slam'){if(typeof player!=='undefined'&&!player._shieldCD&&lockOn){player._shieldCD=80;const dmg=15+skills.Defence.lvl;lockOn.hp-=dmg;lockOn.staggered=true;lockOn.staggerT=40;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+5,lockOn.mesh.position.z,0x6666aa);log('Shield Slam! '+dmg+' damage, enemy stunned','#66a');skills.Attack.xp+=20;skills.Defence.xp+=15;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='recklessness'){if(typeof player!=='undefined'&&!player._reckCD){player._reckCD=900;player._reckActive=true;setTimeout(()=>player._reckActive=false,15000);for(let i=0;i<20;i++){hitFX(player.x+Math.random()*4-2,player.y+10+i*2,player.z+Math.random()*4-2,0xff0000);}log('Recklessness! Critical strikes +50% for 15s','#f00');skills.Attack.xp+=40;skills.Strength.xp+=20;updateXpBar();}}
// === KNIGHT ABILITY EXECUTIONS ===
else if(id==='judgment'){if(typeof player!=='undefined'&&!player._judgmentCD&&lockOn){player._judgmentCD=80;const dmg=18+skills.Attack.lvl+skills.Prayer.lvl;lockOn.hp-=dmg;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+6,lockOn.mesh.position.z,0xffdd44);log('Judgment! Holy damage '+dmg,'#fd4');skills.Attack.xp+=20;skills.Prayer.xp+=15;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='crusader_strike'){if(typeof player!=='undefined'&&!player._crusaderCD&&lockOn){player._crusaderCD=60;const dmg=14+skills.Attack.lvl;lockOn.hp-=dmg;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+5,lockOn.mesh.position.z,0xffeeaa);log('Crusader Strike! '+dmg,'#fea');skills.Attack.xp+=18;skills.Prayer.xp+=12;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='divine_protection'){if(typeof player!=='undefined'&&!player._divineProtCD){player._divineProtCD=300;player._divineProtActive=true;setTimeout(()=>player._divineProtActive=false,20000);for(let i=0;i<20;i++){hitFX(player.x+Math.random()*5-2.5,player.y+5+i,player.z+Math.random()*5-2.5,0xffff88);}log('Divine Protection! -50% damage for 20s','#ff8');skills.Defence.xp+=25;skills.Prayer.xp+=20;updateXpBar();}}
else if(id==='consecration'){if(typeof player!=='undefined'&&!player._consecrateCD){player._consecrateCD=240;const cur=getCursorWorldPos();const cx=cur?cur.x:player.x,cz=cur?cur.z:player.z;for(let i=0;i<30;i++){setTimeout(()=>{hitFX(cx+Math.random()*16-8,meshTerrainH(cx,cz)+1,cz+Math.random()*16-8,0xffff44);enemies.forEach(e=>{const dist=Math.hypot(e.x-cx,e.z-cz);if(dist<12){const dmg=3+skills.Prayer.lvl*0.5;e.hp-=dmg;}});},i*100);}log('Consecration! Holy ground at cursor','#ff4');skills.Prayer.xp+=30;updateXpBar();}}
else if(id==='holy_light'){if(typeof player!=='undefined'&&!player._holyLightCD){player._holyLightCD=120;const heal=Math.round(player.maxHp*0.4+skills.Prayer.lvl*3);player.hp=Math.min(player.hp+heal,player.maxHp);for(let i=0;i<15;i++){hitFX(player.x,player.y+5+i,player.z,0xffffaa);}log('Holy Light! +'+heal+' HP','#ffa');skills.Prayer.xp+=25;updateXpBar();}}
else if(id==='flash_light'){if(typeof player!=='undefined'&&!player._flashLightCD){player._flashLightCD=60;const heal=Math.round(player.maxHp*0.25+skills.Prayer.lvl*2);player.hp=Math.min(player.hp+heal,player.maxHp);hitFX(player.x,player.y+8,player.z,0xffffee);log('Flash of Light! +'+heal+' HP','#ffe');skills.Prayer.xp+=15;updateXpBar();}}
else if(id==='blessing_might'){if(typeof player!=='undefined'&&!player._blessingCD){player._blessingCD=600;player._blessingActive=true;setTimeout(()=>player._blessingActive=false,60000);for(let i=0;i<15;i++){hitFX(player.x+Math.random()*4-2,player.y+12+i*2,player.z+Math.random()*4-2,0xffaa44);}log('Blessing of Might! +15% damage for 60s','#fa4');skills.Prayer.xp+=35;skills.Strength.xp+=10;updateXpBar();}}
else if(id==='divine_shield'){if(typeof player!=='undefined'&&!player._bubbleCD){player._bubbleCD=600;player._bubbleActive=true;setTimeout(()=>player._bubbleActive=false,12000);for(let i=0;i<25;i++){hitFX(player.x+Math.cos(i*Math.PI*2/20)*6,player.y+5+Math.sin(i)*2,player.z+Math.sin(i*Math.PI*2/20)*6,0xffffdd);}log('Divine Shield! Invulnerable for 12s','#ffd');skills.Defence.xp+=30;skills.Prayer.xp+=35;updateXpBar();}}
else if(id==='hammer_justice'){if(typeof player!=='undefined'&&!player._hammerCD&&lockOn){player._hammerCD=90;const dmg=12+skills.Attack.lvl+skills.Prayer.lvl;lockOn.hp-=dmg;lockOn.staggered=true;lockOn.staggerT=90;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+8,lockOn.mesh.position.z,0xffdd22);log('Hammer of Justice! Stunned for 3s','#fd2');skills.Attack.xp+=20;skills.Prayer.xp+=18;updateXpBar();}}
else if(id==='exorcism'){if(typeof player!=='undefined'&&!player._exorcismCD&&lockOn){player._exorcismCD=70;const isUndead=lockOn.type.includes('skeleton')||lockOn.type.includes('zombie')||lockOn.type.includes('ghost')||lockOn.type.includes('shade');const dmg=(isUndead?40:20)+skills.Prayer.lvl*2;lockOn.hp-=dmg;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+6,lockOn.mesh.position.z,0xffff00);log('Exorcism! '+dmg+(isUndead?' HOLY DAMAGE to undead!':' damage'),'#ff0');skills.Prayer.xp+=30;updateXpBar();}}
// === SORCERER ABILITY EXECUTIONS ===
else if(id==='fireball'){if(typeof player!=='undefined'&&!player._fireballCD){if(player.poi<15){log('Not enough mana! (15 needed)','#f44');return;}player._fireballCD=50;player.poi-=15;shootProjectile('spell',25+skills.Magic.lvl*1.5,0xff4400);log('Fireball! (-15 mana)','#f40');skills.Magic.xp+=25;updateXpBar();}}
else if(id==='frostbolt'){if(typeof player!=='undefined'&&!player._frostboltCD&&lockOn){if(player.poi<12){log('Not enough mana! (12 needed)','#f44');return;}player._frostboltCD=40;player.poi-=12;const dmg=18+skills.Magic.lvl;lockOn.hp-=dmg;lockOn.slowed=true;lockOn.slowT=180;shootProjectile('spell',dmg,0x88ccff);hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y,lockOn.mesh.position.z,0xaaddff);log('Frostbolt! '+dmg+' (-12 mana)','#acf');skills.Magic.xp+=22;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='arcane_missiles'){if(typeof player!=='undefined'&&!player._missilesCD&&lockOn){if(player.poi<20){log('Not enough mana! (20 needed)','#f44');return;}player._missilesCD=90;player.poi-=20;let missiles=0;const int=setInterval(()=>{if(++missiles>3||!lockOn||lockOn.hp<=0){clearInterval(int);return;}const dmg=8+skills.Magic.lvl*0.8;lockOn.hp-=dmg;hitFX(lockOn.mesh.position.x+Math.random()*2-1,lockOn.mesh.position.y+5+Math.random()*3,lockOn.mesh.position.z+Math.random()*2-1,0xaa66ff);log('Arcane Missile '+missiles+'! '+dmg,'#a6f');},400);log('Arcane Missiles! (-20 mana)','#a6f');skills.Magic.xp+=30;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='blizzard'){if(typeof player!=='undefined'&&!player._blizzardCD){if(player.poi<35){log('Not enough mana! (35 needed)','#f44');return;}player._blizzardCD=200;player.poi-=35;const cur=getCursorWorldPos();const cx=cur?cur.x:player.x,cz=cur?cur.z:player.z;for(let i=0;i<50;i++){setTimeout(()=>{const tx=cx+(Math.random()-.5)*40;const tz=cz+(Math.random()-.5)*40;hitFX(tx,meshTerrainH(tx,tz)+15,tz,0xaaddff);enemies.forEach(e=>{const dist=Math.hypot(e.x-tx,e.z-tz);if(dist<8){const dmg=5+skills.Magic.lvl*0.5;e.hp-=dmg;}});},i*80);}log('Blizzard! Ice storm at cursor','#adf');skills.Magic.xp+=40;updateXpBar();}}
else if(id==='sorc_fire_blast'){if(typeof player!=='undefined'&&!player._fireblastCD&&lockOn){if(player.poi<10){log('Not enough mana! (10 needed)','#f44');return;}player._fireblastCD=30;player.poi-=10;const dmg=15+skills.Magic.lvl;lockOn.hp-=dmg;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+5,lockOn.mesh.position.z,0xff6600);log('Fire Blast! '+dmg+' (-10 mana)','#f60');skills.Magic.xp+=18;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='pyroblast'){if(typeof player!=='undefined'&&!player._pyroCD){if(player.poi<40){log('Not enough mana! (40 needed)','#f44');return;}player._pyroCD=180;player.poi-=40;log('Pyroblast casting... (-40 mana)','#f40');setTimeout(()=>{if(lockOn){const dmg=60+skills.Magic.lvl*2;lockOn.hp-=dmg;for(let i=0;i<30;i++){hitFX(lockOn.mesh.position.x+Math.random()*6-3,lockOn.mesh.position.y+5+Math.random()*8,lockOn.mesh.position.z+Math.random()*6-3,0xff2200);}log('PYROBLAST! '+dmg+' DAMAGE!','#f20');skills.Magic.xp+=50;updateXpBar();}},3000);}}
else if(id==='frost_nova'){if(typeof player!=='undefined'&&!player._novaCD){if(player.poi<25){log('Not enough mana! (25 needed)','#f44');return;}player._novaCD=150;player.poi-=25;for(let i=0;i<20;i++){const ang=i*Math.PI*2/20;hitFX(player.x+Math.cos(ang)*8,player.y+2,player.z+Math.sin(ang)*8,0x88ddff);}let rooted=0;enemies.forEach(e=>{const dist=Math.hypot(e.x-player.x,e.z-player.z);if(dist<12){e.staggered=true;e.staggerT=180;rooted++;}});log('Frost Nova! '+rooted+' enemies rooted','#8df');skills.Magic.xp+=30;updateXpBar();}}
else if(id==='blink'){if(typeof player!=='undefined'&&!player._blinkCD){if(player.poi<15){log('Not enough mana! (15 needed)','#f44');return;}player._blinkCD=90;player.poi-=15;const right=new THREE.Vector3(-Math.cos(camYaw),0,Math.sin(camYaw));const forward=new THREE.Vector3(Math.sin(camYaw),0,Math.cos(camYaw));player.x+=forward.x*20+right.x*5;player.z+=forward.z*20+right.z*5;for(let i=0;i<15;i++){hitFX(player.x-Math.cos(camYaw)*i*1.5,player.y+3,player.z+Math.sin(camYaw)*i*1.5,0xaa66ff);}log('Blink! Teleported','#a6f');skills.Magic.xp+=20;updateXpBar();}}
else if(id==='polymorph'){if(typeof player!=='undefined'&&!player._polyCD&&lockOn){if(player.poi<30){log('Not enough mana! (30 needed)','#f44');return;}player._polyCD=300;player.poi-=30;lockOn.polymorphed=true;lockOn.polyT=600;lockOn.mesh.visible=false;const sheep=new THREE.Mesh(new THREE.BoxGeometry(2,1.5,3),new THREE.MeshStandardMaterial({color:0xffffff}));sheep.position.copy(lockOn.mesh.position);scene.add(sheep);lockOn.sheepMesh=sheep;log('Polymorph! Enemy is now a sheep','#fff');skills.Magic.xp+=35;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='counterspell'){if(typeof player!=='undefined'&&!player._counterCD&&lockOn){if(player.poi<20){log('Not enough mana! (20 needed)','#f44');return;}player._counterCD=120;player.poi-=20;lockOn.counterspelled=true;lockOn.counterT=60;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+8,lockOn.mesh.position.z,0xff0000);log('Counterspell! Enemy casting interrupted','#f00');skills.Magic.xp+=25;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
// === RANGER ABILITY EXECUTIONS ===
else if(id==='steady_shot'){if(typeof player!=='undefined'&&!player._steadyCD){const cd=player._rapidFireActive?21:35;player._steadyCD=cd;shootProjectile('arrow',18+skills.Ranged.lvl*1.2,0xccaa88);log('Steady Shot!','#ca8');skills.Ranged.xp+=18;updateXpBar();}}
else if(id==='aimed_shot'){if(typeof player!=='undefined'&&!player._aimedCD&&lockOn){const cd=player._rapidFireActive?48:80;player._aimedCD=cd;const dmg=30+skills.Ranged.lvl*1.5;lockOn.hp-=dmg;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+6,lockOn.mesh.position.z,0xffaa44);log('Aimed Shot! '+dmg+' damage','#fa4');skills.Ranged.xp+=25;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='multi_shot'){if(typeof player!=='undefined'&&!player._multiCD){const cd=player._rapidFireActive?60:100;player._multiCD=cd;for(let i=0;i<3;i++){setTimeout(()=>{shootProjectile('arrow',12+skills.Ranged.lvl,0xccaa88);},i*150);}log('Multi-Shot! Three arrows','#ca8');skills.Ranged.xp+=22;updateXpBar();}}
else if(id==='arcane_shot'){if(typeof player!=='undefined'&&!player._arcaneCD){if(player.poi<10){log('Not enough mana! (10 needed)','#f44');return;}player._arcaneCD=50;player.poi-=10;shootProjectile('spell',20+skills.Ranged.lvl+skills.Magic.lvl,0xaa66ff);log('Arcane Shot! (-10 mana)','#a6f');skills.Ranged.xp+=20;skills.Magic.xp+=10;updateXpBar();}}
else if(id==='serpent_sting'){if(typeof player!=='undefined'&&!player._stingCD&&lockOn){player._stingCD=70;lockOn.serpentSting=true;lockOn.stingT=300;lockOn.stingDmg=3+skills.Ranged.lvl*0.3;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+5,lockOn.mesh.position.z,0x00aa44);log('Serpent Sting! Poison applied','#0a4');skills.Ranged.xp+=20;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='hunters_mark'){if(typeof player!=='undefined'&&!player._markCD&&lockOn){player._markCD=180;lockOn.huntersMark=true;lockOn.markT=600;for(let i=0;i<10;i++){hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+12+i,lockOn.mesh.position.z,0xff0000);}log('Hunters Mark! +15% damage vs target','#f00');skills.Ranged.xp+=18;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='distracting_shot'){if(typeof player!=='undefined'&&!player._distractCD&&lockOn){player._distractCD=60;lockOn.aggro=200;lockOn.target=player;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+8,lockOn.mesh.position.z,0xffff00);log('Distracting Shot! Taunted enemy','#ff0');skills.Ranged.xp+=15;skills.Defence.xp+=10;updateXpBar();}}
else if(id==='rapid_fire'){if(typeof player!=='undefined'&&!player._rapidCD){player._rapidCD=300;player._rapidFireActive=true;setTimeout(()=>player._rapidFireActive=false,15000);for(let i=0;i<20;i++){hitFX(player.x+Math.random()*4-2,player.y+10+i*2,player.z+Math.random()*4-2,0xff6600);}log('Rapid Fire! +40% attack speed for 15s','#f60');skills.Ranged.xp+=30;updateXpBar();}}
else if(id==='feign_death'){if(typeof player!=='undefined'&&!player._feignCD){player._feignCD=180;player._feignActive=true;enemies.forEach(e=>{if(e.target===player)e.target=null;e.aggro=0;});setTimeout(()=>player._feignActive=false,5000);for(let i=0;i<15;i++){hitFX(player.x,player.y+i,player.z,0x888888);}log('Feign Death! Enemies lost interest','#888');skills.Ranged.xp+=20;skills.Defence.xp+=15;updateXpBar();}}
else if(id==='explosive_trap'){if(typeof player!=='undefined'&&!player._trapCD){player._trapCD=150;const cur=getCursorWorldPos();const tx=cur?cur.x:(player.x+Math.sin(camYaw)*8);const tz=cur?cur.z:(player.z+Math.cos(camYaw)*8);const trap={x:tx,z:tz,life:600,dmg:25+skills.Ranged.lvl};player.explosiveTrap=trap;hitFX(tx,meshTerrainH(tx,tz)+2,tz,0xff4400);log('Explosive Trap set at cursor!','#f40');skills.Ranged.xp+=22;updateXpBar();}}
// === GENERAL ABILITY EXECUTIONS ===
else if(id==='first_aid'){if(typeof player!=='undefined'&&!player._aidCD){player._aidCD=300;player._firstAidActive=true;let ticks=0;const int=setInterval(()=>{if(++ticks>10||player.hp<=0){clearInterval(int);player._firstAidActive=false;return;}const heal=5+skills.Hitpoints.lvl*0.5;player.hp=Math.min(player.hp+heal,player.maxHp);hitFX(player.x,player.y+5,player.z,0x88ff88);},1000);log('First Aid! Healing over 10s','#8f8');skills.Hitpoints.xp+=20;updateXpBar();}}
else if(id==='bandage'){if(typeof player!=='undefined'&&!player._bandageCD){player._bandageCD=120;const heal=15+skills.Hitpoints.lvl*2;player.hp=Math.min(player.hp+heal,player.maxHp);hitFX(player.x,player.y+6,player.z,0xffffff);log('Bandage! +'+heal+' HP','#fff');skills.Hitpoints.xp+=15;updateXpBar();}}
else if(id==='sharpen_weapon'){if(typeof player!=='undefined'&&!player._sharpenCD){player._sharpenCD=300;player._sharpenActive=true;setTimeout(()=>player._sharpenActive=false,180000);for(let i=0;i<12;i++){hitFX(player.x+Math.random()*4-2,player.y+8+i,player.z+Math.random()*4-2,0xffaa00);}log('Sharpen Weapon! +10% melee damage for 3min','#fa0');skills.Attack.xp+=20;updateXpBar();}}
else if(id==='mining_strike'){if(typeof player!=='undefined'&&!player._mineStrikeCD){player._mineStrikeCD=60;hitFX(player.x+Math.sin(camYaw)*4,player.y+2,player.z+Math.cos(camYaw)*4,0x664422);log('Mining Strike! Strong mining hit','#642');skills.Mining.xp+=25;updateXpBar();}}
else if(id==='lumber_up'){if(typeof player!=='undefined'&&!player._lumberCD){player._lumberCD=120;player._lumberActive=true;setTimeout(()=>player._lumberActive=false,60000);for(let i=0;i<10;i++){hitFX(player.x+Math.random()*3-1.5,player.y+8+i*2,player.z+Math.random()*3-1.5,0x44aa44);}log('Lumber Up! +20% woodcutting speed for 60s','#4a4');skills.Woodcutting.xp+=20;updateXpBar();}}
else if(id==='cooking_fire'){if(typeof player!=='undefined'&&!player._campfireCD){player._campfireCD=300;const cur=getCursorWorldPos();const tx=cur?cur.x:(player.x+Math.sin(camYaw)*5);const tz=cur?cur.z:(player.z+Math.cos(camYaw)*5);const fy=meshTerrainH(tx,tz);const fire=new THREE.Mesh(new THREE.CylinderGeometry(2,1,4,8),new THREE.MeshStandardMaterial({color:0xff4400,emissive:0xff2200,emissiveIntensity:2}));fire.position.set(tx,fy,tz);scene.add(fire);setTimeout(()=>scene.remove(fire),60000);for(let i=0;i<20;i++){hitFX(tx,fy+i*2,tz,0xff6600);}log('Cooking Fire at cursor!','#f60');skills.Cooking.xp+=15;skills.Firemaking.xp+=20;updateXpBar();}}
else if(id==='fishing_cast'){if(typeof player!=='undefined'&&!player._fishCastCD){player._fishCastCD=90;hitFX(player.x,player.y+10,player.z,0x4488ff);log('Fishing Cast! Long cast bonus XP','#48f');skills.Fishing.xp+=25;updateXpBar();}}
else if(id==='runecraft_focus'){if(typeof player!=='undefined'&&!player._focusCD){player._focusCD=180;player._runecraftActive=true;setTimeout(()=>player._runecraftActive=false,60000);for(let i=0;i<15;i++){hitFX(player.x+Math.random()*3-1.5,player.y+10+i*2,player.z+Math.random()*3-1.5,0xaa44ff);}log('Runecraft Focus! +30% Runecraft XP for 60s','#a4f');skills.Runecraft.xp+=30;updateXpBar();}}
else if(id==='sneak_attack'){if(typeof player!=='undefined'&&!player._sneakCD&&lockOn){player._sneakCD=90;const dist=Math.hypot(lockOn.x-player.x,lockOn.z-player.z);const dmg=dist<8?(35+skills.Attack.lvl*2):(15+skills.Attack.lvl);lockOn.hp-=dmg;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+5,lockOn.mesh.position.z,0x444444);log('Sneak Attack! '+dmg+(dist<8?' BACKSTAB!':' damage'),'#444');skills.Attack.xp+=25;skills.Thieving.xp+=15;updateXpBar();}else if(!lockOn){log('No target! Press F to lock on','#f80');}}
else if(id==='agility_roll'){if(typeof player!=='undefined'&&!player._agiRollCD&&player.sta>15){player._agiRollCD=80;player.sta-=15;const rollDir=new THREE.Vector3(Math.sin(camYaw),0,Math.cos(camYaw));player.x+=rollDir.x*15;player.z+=rollDir.z*15;for(let i=0;i<10;i++){hitFX(player.x-rollDir.x*i*1.5,player.y+2,player.z-rollDir.z*i*1.5,0x44ffaa);}log('Agility Roll! Quick escape','#4fa');skills.Agility.xp+=20;updateXpBar();}}
else log('Used ability: '+id,'#aa9')}
// === SHOOT PROJECTILE (Arrow or Spell) ===
function shootProjectile(type='arrow',dmg=15,col=0xccaa88){
if(!cam||!scene)return;
// Check for ammo if shooting arrow (Ranger class has unlimited arrows)
if(type==='arrow'&&playerClass!=='ranger'){
let hasAmmo=false;
for(let i=0;i<inventory.length;i++){
const raw=inventory[i];const itemName=typeof raw==='string'?raw:raw.name;
if(itemName.toLowerCase().includes('arrow')){
hasAmmo=true;inventory.splice(i,1);updateInvUI();break;}}
if(!hasAmmo){log('No arrows! Craft or retrieve arrows.','#f44');return;}}
// Ranger gets infinite arrows - no ammo check needed
// Calculate aim direction: arrows auto-aim at locked target, spells always use cursor
let targetX,targetZ;
if(type==='arrow'&&lockOn&&lockOn.mesh){
// Arrows: auto-aim at locked target
const ePos=lockOn.mesh.position;
targetX=ePos.x;targetZ=ePos.z;
}else{
// Spells AND arrows without lock: use mouse cursor for precise aiming
const rc=new THREE.Raycaster();
rc.setFromCamera({x:mouse.x,y:mouse.y},cam);
// Find ground intersection point for aiming
const planeY=meshTerrainH(player.x,player.z);
const plane=new THREE.Plane(new THREE.Vector3(0,1,0),-planeY);
const target=new THREE.Vector3();
rc.ray.intersectPlane(plane,target);
if(!target)return;
targetX=target.x;targetZ=target.z;}
// Calculate direction and angle
const dx=targetX-player.x;const dz=targetZ-player.z;
const dist=Math.hypot(dx,dz);
if(dist<1)return;
// Create projectile (arrow or spell orb)
let proj;
if(type==='arrow'){
// Arrow shaft + fletching
const arrowGrp=new THREE.Group();
const shaft=new THREE.Mesh(new THREE.CylinderGeometry(.03,.03,2.2,4),new MS({color:0xaa8855,roughness:.8}));shaft.position.y=1.1;shaft.rotation.x=Math.PI/2;arrowGrp.add(shaft);
const tip=new THREE.Mesh(new THREE.ConeGeometry(.06,.3,4),new MS({color:0x666666,roughness:.4,metalness:.8}));tip.position.set(0,0,2.2);tip.rotation.x=Math.PI/2;arrowGrp.add(tip);
const fletch=new THREE.Mesh(new THREE.BoxGeometry(.12,.02,.3),new MS({color:0xaa2222,roughness:.9}));fletch.position.set(0,0,.2);arrowGrp.add(fletch);
proj=arrowGrp;
}else{
// Spell orb - larger and more visible
proj=new THREE.Mesh(new THREE.SphereGeometry(.6,12,12),new MS({color:col,emissive:col,emissiveIntensity:3,transparent:true,opacity:.9}));
}
// Position at player
const startH=meshTerrainH(player.x,player.z);
proj.position.set(player.x,startH+8,player.z);
// Calculate velocity - different physics for arrows vs spells
const angle=Math.atan2(dx,dz);
if(type==='arrow'){
// Arrows: slower with gravity arc
const speed=0.8;const arcHeight=dist*0.15;
proj.userData={vx:Math.sin(angle)*speed,vz:Math.cos(angle)*speed,vy:arcHeight*0.02,life:80,dmg:dmg,type:type,gravity:0.015};
proj.rotation.y=angle;proj.rotation.z=-.3;
}else{
// Spells: faster, less gravity, longer life, more accurate straight shot
const speed=2.5;const arcHeight=dist*0.05;
proj.userData={vx:Math.sin(angle)*speed,vz:Math.cos(angle)*speed,vy:arcHeight*0.01,life:120,dmg:dmg,type:type,gravity:0.008};
// Add bright trail for spells
for(let i=0;i<8;i++){const tr=new THREE.Mesh(new THREE.SphereGeometry(.25,6,6),new MS({color:col,emissive:col,emissiveIntensity:2,transparent:true,opacity:.6}));tr.position.copy(proj.position);tr.userData={trail:true,idx:i,life:30};scene.add(tr);particles.push(tr);}}
scene.add(proj);
particles.push(proj);
// Animation
playerGroup.userData.animState='attack';
setTimeout(()=>{if(playerGroup)playerGroup.userData.animState='idle';},300);
// Ranged XP
if(type==='arrow'){skills.Ranged.xp+=12;updateXpBar();}else{skills.Magic.xp+=15;updateXpBar();}}
// Override action bar click to use execAbility
abSlots.forEach((slot,idx)=>{slot.onclick=()=>execAbility(abAssign[idx])});
// === GAMEPAD DUAL-BUTTON COMBOS ===
const gpCombos={};let gpHeld={};
function registerCombo(b1,b2,action){gpCombos[b1+'+'+b2]=action;gpCombos[b2+'+'+b1]=action}
registerCombo('lt','a','heal');registerCombo('lt','b','roll');
registerCombo('lt','x','spec_atk');registerCombo('lt','y','jump');
registerCombo('rt','a','prayer');registerCombo('rt','b','bones');
registerCombo('rt','x','gather');registerCombo('rt','y','map');
registerCombo('lb','a','wind_strike');registerCombo('lb','b','fire_strike');
registerCombo('lb','x','water_strike');registerCombo('lb','y','earth_strike');
registerCombo('rb','a','protect_melee');registerCombo('rb','b','protect_magic');
registerCombo('rb','x','protect_range');registerCombo('rb','y','piety');
function checkGpCombos(){const held=Object.keys(gpButtons).filter(k=>gpButtons[k]);
if(held.length>=2){for(let i=0;i<held.length;i++){for(let j=i+1;j<held.length;j++){
const key=held[i]+'+'+held[j];if(gpCombos[key]&&!gpHeld[key]){gpHeld[key]=true;execAbility(gpCombos[key])}}}}
for(const k in gpHeld){const[b1,b2]=k.split('+');if(!gpButtons[b1]||!gpButtons[b2])delete gpHeld[k]}}

// === LOG -> CHAT-LOG ===
function log(msg,col){const el=document.getElementById('chat-log');if(!el)return;const d=document.createElement('div');d.style.color=col||'#887';d.textContent=msg;el.appendChild(d);el.scrollTop=el.scrollHeight}

// === EQUIPMENT UI UPDATE ===
function updateEqUI(){
const gs=totalGear();
document.getElementById('es-atk').textContent=gs.atk;
document.getElementById('es-def').textContent=gs.def;
document.getElementById('es-str').textContent=gs.str;
gearSlots.forEach(s=>{const el=document.getElementById('eq-'+s);if(el){el.querySelector('.eq-name').textContent=equipped[s].name||s;
el.onclick=()=>{if(equipped[s].name!=='None'){const old=equipped[s].name;if(inventory.length<28){inventory.push({name:old,uid:null});updateInvUI()}
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
// Lock-on indicator: floating diamond sprite above enemy head
const rGeo=new THREE.OctahedronGeometry(1.2,0);
const rMat=new THREE.MeshBasicMaterial({color:0xff2222,transparent:true,opacity:.85,depthTest:false});
targetRing=new THREE.Mesh(rGeo,rMat);targetRing.renderOrder=999;targetRing.visible=false;
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
if(targetRing&&lockOn.mesh){
// Float above enemy head and spin
targetRing.visible=true;
const ePos=lockOn.mesh.position;
const eH=(lockOn.mesh.geometry&&lockOn.mesh.geometry.parameters)?Math.max(lockOn.mesh.geometry.parameters.height||8,lockOn.mesh.geometry.parameters.radiusTop||4)*2:12;
targetRing.position.set(ePos.x,ePos.y+eH+2+Math.sin(time*3)*.6,ePos.z);
targetRing.rotation.y=time*2;targetRing.rotation.x=time*1.5;
const sc=.9+Math.sin(time*4)*.1;targetRing.scale.set(sc,sc,sc);}
}
// Animate dungeon entrance portals
function animateDungeonPortals(){
for(const d of dungeons){
if(d.portalMesh&&d.portalMesh.userData){
const {portalPlane,ring,theme}=d.portalMesh.userData;
// Pulse opacity
portalPlane.material.opacity=.5+.3*Math.sin(time*2);
// Rotate ring
ring.rotation.z+=.02;
// Color shift based on theme
const col={fire:0xff4400,undead:0x4422aa,cave:0x22aa44}[theme];
portalPlane.material.color.setHex(col);}}
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
// City/castle/dungeon markers for the world map
const mapCities=[{x:0,z:0,n:'Lumbridge',r:80},{x:555,z:50,n:'Varrock',r:70},{x:-480,z:280,n:'Falador',r:65},{x:-1200,z:100,n:'Ardougne',r:70}];
const mapCastles=[{x:900,z:-800,n:'Eastern Fortress'},{x:-2000,z:-500,n:'Western Stronghold'},{x:0,z:-1800,n:'Wilderness Castle'},{x:-800,z:600,n:'Southern Keep'},{x:1500,z:400,n:'Desert Citadel'}];
function drawWorldMap(){
const W=900,H=700;wmCtx.fillStyle='#0a0805';wmCtx.fillRect(0,0,W,H);
const scale=W/16000,ox=W/2,oy=H/2;
// Filter to show only major regions (larger areas) and wilderness zones
const majorRegions=regions.filter(r=>r.r>=150);// Only show regions with radius >=150
const wildernessRegions=regions.filter(r=>r.n.toLowerCase().includes('wilderness')||r.n.toLowerCase().includes('deep')||r.lv>=50);
// Draw wilderness/RNG areas first (as larger background zones)
wildernessRegions.forEach(r=>{
const rx=r.x*scale+ox,ry=r.z*scale+oy;
const rr=Math.max(r.r*scale,15);
const cr=(r.fog>>16)/255,cg=((r.fog>>8)&0xff)/255,cb=(r.fog&0xff)/255;
wmCtx.fillStyle=`rgba(${~~(cr*255)},${~~(cg*255)},${~~(cb*255)},0.25)`;
wmCtx.beginPath();wmCtx.arc(rx,ry,rr*1.2,0,Math.PI*2);wmCtx.fill();
wmCtx.strokeStyle='rgba(90,74,50,0.3)';wmCtx.lineWidth=1;wmCtx.stroke();});
// Draw major regions as colored zones
majorRegions.forEach(r=>{
const rx=r.x*scale+ox,ry=r.z*scale+oy;
const rr=Math.max(r.r*scale,10);
const cr=(r.fog>>16)/255,cg=((r.fog>>8)&0xff)/255,cb=(r.fog&0xff)/255;
wmCtx.fillStyle=`rgba(${~~(cr*255)},${~~(cg*255)},${~~(cb*255)},0.5)`;
wmCtx.beginPath();wmCtx.arc(rx,ry,rr,0,Math.PI*2);wmCtx.fill();
wmCtx.strokeStyle='#5a4a32';wmCtx.lineWidth=1.5;wmCtx.stroke();
wmCtx.fillStyle='#c8a96e';wmCtx.font='bold 10px sans-serif';wmCtx.textAlign='center';
// Only show name if radius is large enough to avoid clutter
if(r.r>=200){
wmCtx.fillText(r.n,rx,ry-rr-5);
wmCtx.fillStyle='#aa8866';wmCtx.font='8px sans-serif';
wmCtx.fillText('Lv '+r.lv,rx,ry+4);}
else{wmCtx.fillStyle='#aa8866';wmCtx.font='8px sans-serif';wmCtx.fillText(r.n,rx,ry+4);}});
// Draw cities as walled circles
wmCtx.strokeStyle='#aa9060';wmCtx.lineWidth=2;
mapCities.forEach(c=>{const cx=c.x*scale+ox,cy=c.z*scale+oy,cr=c.r*scale;
wmCtx.beginPath();wmCtx.arc(cx,cy,cr,0,Math.PI*2);wmCtx.stroke();
wmCtx.fillStyle='rgba(180,160,100,.15)';wmCtx.fill();
wmCtx.fillStyle='#e8d4a8';wmCtx.font='bold 10px serif';wmCtx.textAlign='center';
wmCtx.fillText(c.n,cx,cy+3)});
// Draw castles as squares with towers
wmCtx.fillStyle='#8a7a5a';
mapCastles.forEach(c=>{const cx=c.x*scale+ox,cy=c.z*scale+oy;
wmCtx.fillRect(cx-6,cy-6,12,12);
wmCtx.strokeStyle='#aa9060';wmCtx.lineWidth=1.5;wmCtx.strokeRect(cx-6,cy-6,12,12);
// Corner tower dots
[[-1,-1],[-1,1],[1,-1],[1,1]].forEach(([sx,sz])=>{wmCtx.beginPath();wmCtx.arc(cx+sx*6,cy+sz*6,2,0,Math.PI*2);wmCtx.fill()});
wmCtx.fillStyle='#e8c878';wmCtx.font='bold 8px serif';wmCtx.textAlign='center';
wmCtx.fillText(c.n,cx,cy-10);wmCtx.fillStyle='#8a7a5a'});
// Draw dungeons as cave icons
wmCtx.fillStyle='#6a4a2a';
dungeons.forEach(d=>{const dx=d.x*scale+ox,dy=d.z*scale+oy;
wmCtx.beginPath();wmCtx.arc(dx,dy,3,0,Math.PI*2);wmCtx.fill();
wmCtx.strokeStyle='#4a3a1a';wmCtx.lineWidth=1;wmCtx.stroke()});
// Draw building footprints as dots
wmCtx.fillStyle='rgba(160,140,100,.3)';
cityFootprints.forEach(f=>{const fx=f.x*scale+ox,fy=f.z*scale+oy;
wmCtx.fillRect(fx-1,fy-1,2,2)});
// Enemies as red dots
enemies.forEach(e=>{const ex=e.mesh.position.x*scale+ox,ey=e.mesh.position.z*scale+oy;
wmCtx.fillStyle='#cc2020';wmCtx.fillRect(ex-1,ey-1,2,2)});
// Player marker
const px=player.x*scale+ox,py=player.z*scale+oy;
wmCtx.fillStyle='#fff';wmCtx.beginPath();wmCtx.arc(px,py,5,0,Math.PI*2);wmCtx.fill();
wmCtx.strokeStyle='#ffcc44';wmCtx.lineWidth=2;wmCtx.stroke();
wmCtx.fillStyle='#ffcc44';wmCtx.font='bold 11px sans-serif';wmCtx.textAlign='center';
wmCtx.fillText('YOU',px,py-9);
// Grid
wmCtx.strokeStyle='rgba(90,74,50,.15)';wmCtx.lineWidth=.5;
for(let gx=-8000;gx<=8000;gx+=1000){const sx=gx*scale+ox;wmCtx.beginPath();wmCtx.moveTo(sx,0);wmCtx.lineTo(sx,H);wmCtx.stroke()}
for(let gz=-8000;gz<=8000;gz+=1000){const sy=gz*scale+oy;wmCtx.beginPath();wmCtx.moveTo(0,sy);wmCtx.lineTo(W,sy);wmCtx.stroke()}
// Coords
document.getElementById('wm-coords').textContent='Player: '+~~player.x+', '+~~player.z+' \u00B7 '+getReg(player.x,player.z).n;
}
document.getElementById('wm-close').onclick=()=>{document.getElementById('world-map').classList.remove('active')};

let scene,cam,renderer,composer,riverMesh,playerGroup;
let playerClass='knight';
let enemies=[],lootArr=[],particles=[],torchData=[];
let autoLoot=true;
const lootLabelCanvas=document.getElementById('loot-label-canvas');const lootLabelCtx=lootLabelCanvas.getContext('2d');
function resizeLootCanvas(){lootLabelCanvas.width=innerWidth;lootLabelCanvas.height=innerHeight}
window.addEventListener('resize',resizeLootCanvas);resizeLootCanvas();
let dustPts,time=0;
const lightPool=[];const MAX_LIGHTS=8;
const torchPositions=[];
const solidMeshes=[];
const solidBoxes=[];
const circleColliders=[];
// Dungeon system globals (must be accessible from game loop)
let inDungeon=null;let dungeonGroup=null;const dungeons=[];const dungeonObjs=[];const enterableBuildings=[];let insideBuilding=null;let buildingGroup=null;
// Culling globals
let cullFrame=0;let distanceCull=null,shadowCull=null,checkInteractions=null;
// Terrain mesh reference for accurate height + door system
let groundMesh=null;const doors=[];const windmills=[];
// GPU instanced building elements (populated during init)
let _buildingInstancers=null;
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
{name:'Anarisza y',x:800,z:800,unlocked:true},
{name:'Inasmay Irithtay',x:-1500,z:2000,unlocked:true}
];
let showTeleport=false;
// Skill items: items that grant XP when used (F key near resource spots)
const skillItems={
'Onzebray Ickaxepay':{skill:'Mining',xp:15},'Ironway Ickaxepay':{skill:'Mining',xp:25},'Eelstay Ickaxepay':{skill:'Mining',xp:40},'Uneray Ickaxepay':{skill:'Mining',xp:65},
'Onzebray Atchethay':{skill:'Woodcutting',xp:15},'Ironway Atchethay':{skill:'Woodcutting',xp:25},'Eelstay Atchethay':{skill:'Woodcutting',xp:40},'Uneray Atchethay':{skill:'Woodcutting',xp:65},
'Ishingfay Odray':{skill:'Fishing',xp:30},'Yingflay Ishingfay Odray':{skill:'Fishing',xp:50},'Arpoonhay':{skill:'Fishing',xp:80},
'Inderboxtay':{skill:'Firemaking',xp:25},'Augmentedway Inderboxtay':{skill:'Firemaking',xp:60},
'Iselchay':{skill:'Crafting',xp:20},'Eedlenay':{skill:'Crafting',xp:30},
'Ammerhay':{skill:'Smithing',xp:25},'Oldengay Ammerhay':{skill:'Smithing',xp:60},
'Ifenay':{skill:'Cooking',xp:20},'Awray Eefbay':{skill:'Cooking',xp:15},'Awray Ickenchay':{skill:'Cooking',xp:10},'Awray Eatmay':{skill:'Cooking',xp:15},'Awray Almonsay':{skill:'Cooking',xp:30},'Awray Ordfishsway':{skill:'Cooking',xp:50},'Awray Unatay':{skill:'Cooking',xp:40},'Awray Earbay Eatmay':{skill:'Cooking',xp:25},'Awray Arkshay x5':{skill:'Cooking',xp:100},'Awray Ompychay':{skill:'Cooking',xp:35},
'Onesbay':{skill:'Prayer',xp:15},'Igbay Onesbay':{skill:'Prayer',xp:30},'Agondray Onesbay':{skill:'Prayer',xp:72},'Akeday Onesbay':{skill:'Prayer',xp:50},'Yrmway Onesbay':{skill:'Prayer',xp:55},'Olltray Onesbay':{skill:'Prayer',xp:40},'Olfway Onesbay':{skill:'Prayer',xp:25},'Yvernway Onesbay':{skill:'Prayer',xp:60},'Ydrahay Onesbay':{skill:'Prayer',xp:80},
'Aturenay Uneray':{skill:'Runecraft',xp:20},'Eathday Uneray':{skill:'Runecraft',xp:35},'Oodblay Uneray':{skill:'Runecraft',xp:50},'Oulsay Uneray x3':{skill:'Runecraft',xp:60},'Aoscay Uneray x5':{skill:'Runecraft',xp:40},'Irefay Uneray x20':{skill:'Runecraft',xp:30},'Awlay Uneray x3':{skill:'Runecraft',xp:45},'Indmay Uneray x15':{skill:'Runecraft',xp:25},'Athwray Uneray x5':{skill:'Runecraft',xp:70},
'Erbhay':{skill:'Herblore',xp:25},'Arlicgay':{skill:'Herblore',xp:10},'Antidoteway':{skill:'Herblore',xp:30},'Antipoisonway':{skill:'Herblore',xp:20},'Ayerpray Otionpay':{skill:'Herblore',xp:40},
'Ockpicklay':{skill:'Thieving',xp:30},'Iderspay Ilksay':{skill:'Crafting',xp:15},'Owhidecay':{skill:'Crafting',xp:10},'Akesnay Inskay':{skill:'Crafting',xp:20},'Izardlay Inskay':{skill:'Crafting',xp:25},'Agondray Idehay':{skill:'Crafting',xp:60},'Ackblay Agondray Idehay':{skill:'Crafting',xp:80},'Ydrahay Eatherlay':{skill:'Crafting',xp:70},
'Ironway Oreay':{skill:'Mining',xp:20},'Oldgay Oreay':{skill:'Mining',xp:40},'Elementalway Oreay':{skill:'Mining',xp:50},'Uniteray Oreay':{skill:'Mining',xp:80},'Anitegray x3':{skill:'Mining',xp:45},
// Farming - harvestable fruits and crops
'Apple':{skill:'Farming',xp:12,heal:5},'Redberry':{skill:'Farming',xp:8,heal:2},'Dwellberry':{skill:'Farming',xp:15,heal:6},'Jangerberry':{skill:'Farming',xp:18,heal:8},'Wildberry':{skill:'Farming',xp:6,heal:2},
'Banana':{skill:'Farming',xp:10,heal:4},'Orange':{skill:'Farming',xp:14,heal:6},'Lemon':{skill:'Farming',xp:12,heal:4},'Pineapple':{skill:'Farming',xp:25,heal:10},
'Cabbage':{skill:'Farming',xp:10,heal:4},'Potato':{skill:'Farming',xp:8,heal:3},'Onion':{skill:'Farming',xp:9,heal:3},'Grain':{skill:'Farming',xp:5,heal:1},
// Arrows - can be retrieved from ground or crafted
'Eelstay Arrowway x15':{skill:'Ranged',xp:20},'Ironway Arrowway x5':{skill:'Ranged',xp:15},'Agondray Arrowway x15':{skill:'Ranged',xp:35},'Arkday Arrowway x10':{skill:'Ranged',xp:25},
'Single Arrow':{skill:'Ranged',xp:2}
};
const PLAYER_R=2.2;
function addSolid(mesh){solidMeshes.push(mesh)}
// Oriented wall collider (stores world-space center, half-extents, and rotation for accurate thin-wall collision)
const wallColliders=[];
function addWallSolid(wx,wz,halfW,halfD,wallH,rot,baseY){
wallColliders.push({x:wx,z:wz,hw:halfW,hd:halfD,h:wallH,rot:rot||0,by:baseY||0});}
// World-space circle collider (for towers, huts, round structures)
function addCircleSolid(wx,wz,radius,minY,maxY){circleColliders.push({x:wx,z:wz,r:radius,minY:minY||0,maxY:maxY||999})}
function buildColliders(){
solidBoxes.length=0;
// FIX: Filter out invisible or invalid meshes before building colliders
const validMeshes=solidMeshes.filter(m=>m&&m.visible&&m.parent);
for(const m of validMeshes){m.updateMatrixWorld(true);
const b=new THREE.Box3().setFromObject(m);
// Skip absurdly large boxes (likely AABB artifacts from rotated meshes)
const sx=b.max.x-b.min.x,sz=b.max.z-b.min.z;
if(sx>80||sz>80)continue;
solidBoxes.push(b)}
log('Colliders: '+solidBoxes.length+' boxes, '+wallColliders.length+' walls, '+circleColliders.length+' circles','#0f0')}
function pushOut(px,py,pz){
let ox=px,oz=pz;
const pr=PLAYER_R;
// Box colliders (non-rotated meshes only)
for(let pass=0;pass<2;pass++){for(const b of solidBoxes){
// Distance cull: skip boxes far from player
const bcx=(b.min.x+b.max.x)/2,bcz=(b.min.z+b.max.z)/2;
if(Math.abs(ox-bcx)>60||Math.abs(oz-bcz)>60)continue;
const minX=b.min.x-pr,maxX=b.max.x+pr,minZ=b.min.z-pr,maxZ=b.max.z+pr;
if(py>=b.max.y-1)continue;
if(ox>minX&&ox<maxX&&oz>minZ&&oz<maxZ&&py>b.min.y-6){
const ovL=ox-minX,ovR=maxX-ox,ovB=oz-minZ,ovF=maxZ-oz;
const m=Math.min(ovL,ovR,ovB,ovF);
if(m===ovL)ox=minX;else if(m===ovR)ox=maxX;
else if(m===ovB)oz=minZ;else oz=maxZ}}}
// Oriented wall colliders (proper thin-wall collision respecting rotation)
for(const w of wallColliders){
if(Math.abs(ox-w.x)>w.hw+w.hd+pr+5&&Math.abs(oz-w.z)>w.hw+w.hd+pr+5)continue;
if(py>=w.by+w.h-1||py<w.by-6)continue;
const cosR=Math.cos(-w.rot),sinR=Math.sin(-w.rot);
const lx=(ox-w.x)*cosR-(oz-w.z)*sinR;
const lz=(ox-w.x)*sinR+(oz-w.z)*cosR;
const hw=w.hw+pr,hd=w.hd+pr;
if(lx>-hw&&lx<hw&&lz>-hd&&lz<hd){
const ovL=lx+hw,ovR=hw-lx,ovB=lz+hd,ovF=hd-lz;
const mn=Math.min(ovL,ovR,ovB,ovF);
let plx=lx,plz=lz;
if(mn===ovL)plx=-hw;else if(mn===ovR)plx=hw;
else if(mn===ovB)plz=-hd;else plz=hd;
const cosR2=Math.cos(w.rot),sinR2=Math.sin(w.rot);
ox=w.x+plx*cosR2-plz*sinR2;
oz=w.z+plx*sinR2+plz*cosR2;}}
// Circle colliders (towers, huts, buildings)
for(const c of circleColliders){
if(py>=c.maxY-1||py<c.minY-6)continue;
const dx=ox-c.x,dz=oz-c.z;
const dist=Math.hypot(dx,dz);
if(dist>c.r+pr+10)continue;
const minDist=c.r+pr;
if(dist<minDist&&dist>0.01){const push=minDist-dist;
ox+=dx/dist*push;oz+=dz/dist*push}}
return{x:ox,z:oz}}
// Debug collision visualization
let collisionDebugMeshes=[];let collisionDebugActive=false;
function toggleCollisionDebug(){
if(collisionDebugActive){
collisionDebugMeshes.forEach(m=>scene.remove(m));collisionDebugMeshes=[];collisionDebugActive=false;log('Collision debug OFF','#f80');return}
collisionDebugActive=true;
// Show box colliders as wireframes
for(const b of solidBoxes){
const geo=new THREE.BoxGeometry(b.max.x-b.min.x,Math.max(1,b.max.y-b.min.y),b.max.z-b.min.z);
const mat=new THREE.MeshBasicMaterial({color:0xff0000,wireframe:true,transparent:true,opacity:0.5});
const mesh=new THREE.Mesh(geo,mat);
mesh.position.set((b.min.x+b.max.x)/2,(b.min.y+b.max.y)/2,(b.min.z+b.max.z)/2);
scene.add(mesh);collisionDebugMeshes.push(mesh)}
// Show circle colliders as rings
for(const c of circleColliders){
const geo=new THREE.RingGeometry(c.r-0.2,c.r+0.2,32);
const mat=new THREE.MeshBasicMaterial({color:0x00ff00,side:THREE.DoubleSide,transparent:true,opacity:0.6});
const mesh=new THREE.Mesh(geo,mat);
mesh.rotation.x=-Math.PI/2;
mesh.position.set(c.x,Math.max(c.minY+1,c.maxY-2),c.z);
scene.add(mesh);collisionDebugMeshes.push(mesh)}
// Show wall colliders as oriented wireframes
for(const w of wallColliders){
const geo=new THREE.BoxGeometry(w.hw*2,w.h,w.hd*2);
const mat=new THREE.MeshBasicMaterial({color:0xffff00,wireframe:true,transparent:true,opacity:0.6});
const mesh=new THREE.Mesh(geo,mat);
mesh.position.set(w.x,w.by+w.h/2,w.z);mesh.rotation.y=w.rot;
scene.add(mesh);collisionDebugMeshes.push(mesh)}
log('Collision debug ON - Red=Boxes, Yellow=Walls, Green=Rings','#0f0');}
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
const segs=250,size=80000,half=size/2,cell=size/segs,cols=segs+1;
const fi=(wx+half)/cell,fj=(half+wz)/cell;
const i0=Math.max(0,Math.min(segs-1,Math.floor(fi))),j0=Math.max(0,Math.min(segs-1,Math.floor(fj)));
const fx=fi-i0,fz=fj-j0;
const h00=pos.getZ(j0*cols+i0),h10=pos.getZ(j0*cols+i0+1),h01=pos.getZ((j0+1)*cols+i0),h11=pos.getZ((j0+1)*cols+i0+1);
// Triangle interpolation matching GPU rendering (PlaneGeometry diagonal: bottom-left to top-right)
if(fx+fz<=1)return(1-fx-fz)*h00+fx*h10+fz*h01;
return(1-fx)*h01+(fx+fz-1)*h11+(1-fz)*h10}
let keys={},mouse={x:0,y:0,dx:0,dy:0,down:false,right:false,mid:false};
let camYaw=0,camPitch=.35,camDist=60;
let player={x:0,z:0,y:2,vx:0,vz:0,vy:0,speed:.42,hp:142,maxHp:142,sta:100,maxSta:100,poi:68,maxPoi:68,ang:0,rolling:false,rollT:0,atkCD:0,dead:false,deadTimer:0,blocking:false,grounded:true,isSprinting:false};
let lockOn=null,lockIdx=-1;
let showSkills=false,showInv=false;

// === EDITOR MODE SYSTEM ===
let editorMode=false;
let editorSelected=null;
let editorObjType='enemy';
let editorSpawnList=[
'goblin','skeleton','wolf','bear','spider','guard','mage','knight',
'greendragon','bluedragon','reddragon','blackdragon',
'barbarian','dwarf','elf','troll','ogre','demon','ghost',
'hillgiant','mossgiant','chaos_ele','revenant','vampire'
];
let editorBuildings=['hut','house','tower','castle','tavern','forge','church','mill','barn'];
let editorLoot=['Onzebray Ordssway','Ironway Ordssway','Eelstay Ordssway','Oinscay x100','Onesbay','Eadbray','Awray Eatmay','Ockpicklay'];
let editorSnap=false;
let gpAxes=[0,0,0,0],gpButtons={};

const drops={goblin:[{i:"Onzebray Ordssway",c:.42},{i:"Oinscay x17",c:.68},{i:"Onesbay",c:1},{i:"Oblingay Ailmay",c:.08},{i:"Onzebray Ickaxepay",c:.05},{i:"Aturenay Uneray",c:.12},{i:"Efchay Athay",c:.03},{i:"Oblingay Ookbay",c:.02}],
cow:[{i:"Awray Eefbay",c:1},{i:"Owhidecay",c:.85},{i:"Oinscay x5",c:.4},{i:"Ucketbay ofway Ilkmay",c:.3},{i:"Owcay Ornhay",c:.1}],
chicken:[{i:"Awray Ickenchay",c:1},{i:"Eathersfay x12",c:.9},{i:"Onesbay",c:1},{i:"Eggway",c:.4}],
guard:[{i:"Ironway Ordssway",c:.3},{i:"Oinscay x45",c:.8},{i:"Eadbray",c:.5},{i:"Eelstay Ainbodychay",c:.08},{i:"Ironway Ickaxepay",c:.04},{i:"Uardgay Ournaljay",c:.02},{i:"Ironway Atchethay",c:.06}],
skeleton:[{i:"Onesbay",c:1},{i:"Ironway Arrowway x5",c:.6},{i:"Ancientway Oincay",c:.1},{i:"Ullskay Agmentfray",c:.15},{i:"Eathday Uneray",c:.08},{i:"Eletalsway Ootsbay",c:.03}],
pirate:[{i:"Oinscay x30",c:.7},{i:"Umray",c:.4},{i:"Eyeway Atchpay",c:.05},{i:"Utlasscay",c:.1},{i:"Ishingfay Odray",c:.06},{i:"Awray Ordfishsway",c:.15},{i:"Easuretray Apmay",c:.02},{i:"Annoncay Allbay x5",c:.08}],
barbarian:[{i:"Awray Eatmay",c:.8},{i:"Oinscay x12",c:.6},{i:"Earbay Urfay",c:.3},{i:"Eelstay Atchethay",c:.08},{i:"Inderboxtay",c:.1},{i:"Awray Almonsay",c:.2},{i:"Arbariansbay Elmhay",c:.04}],
vampire:[{i:"Oodblay Uneray",c:.4},{i:"Oinscay x60",c:.5},{i:"Arlicgay",c:.2},{i:"Ampyrevay Ustday",c:.7},{i:"Oodblay Ardsshay",c:.03},{i:"Arkday Owbay",c:.02},{i:"Ubyray Ingray",c:.05}],
demon:[{i:"Agondray Onesbay",c:.8},{i:"Uneray Imitarscay",c:.05},{i:"Oinscay x200",c:.9},{i:"Infernalway Ashway",c:.6},{i:"Irefay Uneray x20",c:.4},{i:"Agondray Aggerdray",c:.04},{i:"Obsidianway Ardsshay",c:.03},{i:"Infernalway Apecay Ardsshay",c:.01}],
scorpion:[{i:"Oinscay x8",c:.5},{i:"Oisonpay Ingerstay",c:.3},{i:"Antidoteway",c:.1}],
zombie:[{i:"Onesbay",c:1},{i:"Ombiezay Ampionchay Ollscray",c:.01},{i:"Ottenray Oodfay",c:.5},{i:"Ironway Ailsnay x8",c:.3}],
wolf:[{i:"Olfway Onesbay",c:.8},{i:"Olfway Urfay",c:.6},{i:"Awray Eatmay",c:.7},{i:"Awsclay",c:.1}],
bear:[{i:"Earbay Urfay",c:.8},{i:"Awray Earbay Eatmay",c:.7},{i:"Igbay Onesbay",c:.5},{i:"Earbay Awpay",c:.04}],
spider:[{i:"Iderspay Ilksay",c:.6},{i:"Oinscay x3",c:.5},{i:"Edray Iderspay Eggsway",c:.2},{i:"Iderspay Angfay",c:.08}],
drake:[{i:"Akeday Onesbay",c:.8},{i:"Agondray Alescay",c:.15},{i:"Oinscay x80",c:.6},{i:"Akeday Awclay",c:.03},{i:"Athwray Uneray x5",c:.1}],
ghost:[{i:"Ostghay Essenceay",c:.5},{i:"Oinscay x20",c:.4},{i:"Eathday Uneray",c:.2},{i:"Ectoplasmway",c:.3},{i:"Ostghay Oberay Optay",c:.04}],
shade:[{i:"Adeshay Oberay",c:.1},{i:"Oinscay x40",c:.5},{i:"Eathday Uneray x3",c:.15},{i:"Adowshay Eykay",c:.02}],
troll:[{i:"Olltray Onesbay",c:.8},{i:"Anitegray x3",c:.5},{i:"Oinscay x35",c:.6},{i:"Owingtray Ockray x10",c:.3},{i:"Anitegray Aulmay",c:.02}],
ogre:[{i:"Igbay Onesbay",c:.8},{i:"Oinscay x25",c:.6},{i:"Ogreway Owbay",c:.05},{i:"Awray Ompychay",c:.3}],
knight:[{i:"Eelstay Atebodyplay",c:.1},{i:"Oinscay x55",c:.7},{i:"Eelstay Ordssway",c:.15},{i:"Eelstay Ieldshay",c:.08}],
mage:[{i:"Awlay Uneray x3",c:.3},{i:"Oinscay x40",c:.6},{i:"Affstay ofway Airway",c:.06},{i:"Izardway Oberay",c:.04},{i:"Ysticmay Ovesglay",c:.02}],
thief:[{i:"Oinscay x35",c:.8},{i:"Ockpicklay",c:.2},{i:"Iamondday",c:.04},{i:"Ievingtay Apecay Ardsshay",c:.01}],
dwarf:[{i:"Oinscay x20",c:.7},{i:"Ironway Oreay",c:.5},{i:"Eelstay Ickaxepay",c:.06},{i:"Arvendway Outstay",c:.2},{i:"Oldgay Oreay",c:.08}],
whiteknight:[{i:"Ithrilmay Ordssway",c:.1},{i:"Oinscay x65",c:.7},{i:"Iteway Ieldshay",c:.05},{i:"Ayerpray Otionpay",c:.08}],
darkwiz:[{i:"Aoscay Uneray x5",c:.4},{i:"Oinscay x30",c:.6},{i:"Izardway Athay",c:.1},{i:"Indmay Uneray x15",c:.5},{i:"Ysticmay Oberay Ottombay",c:.03}],
revenant:[{i:"Evenantray Ethereay x10",c:.6},{i:"Oinscay x150",c:.5},{i:"Ancientway Atuettestay",c:.02},{i:"Awcray Owbay",c:.01},{i:"Amuleway ofway Avariceway",c:.005}],
hellhound:[{i:"Igbay Onesbay",c:.8},{i:"Oinscay x80",c:.5},{i:"Oulderingsmay Onesay",c:.02},{i:"Ellhoundhay Angfay",c:.05},{i:"Ueclay Ollscray",c:.08}],
imp:[{i:"Oinscay x3",c:.5},{i:"Impway Eadbay",c:.8},{i:"Irelighterfay",c:.15}],
tzhaar:[{i:"Obsidianway Ardsshay",c:.4},{i:"Okkulay x50",c:.8},{i:"Obsidianway Aulmay",c:.02},{i:"Obsidianway Ieldshay",c:.03},{i:"Irefay Apecay Ardsshay",c:.01}],
elf:[{i:"Ystalcray Ardsshay",c:.5},{i:"Oinscay x100",c:.6},{i:"Ystalcray Owbay Eedsay",c:.02},{i:"Elvenway Ignetsay",c:.01},{i:"Awray Unatay",c:.3}],
mummy:[{i:"Oinscay x50",c:.6},{i:"Araohsphay Eptresay Ardsshay",c:.01},{i:"Oldgay Eaflay",c:.1},{i:"Andagebay",c:.4}],
scarab:[{i:"Oinscay x15",c:.5},{i:"Arabscay Arapacecay",c:.3},{i:"Eriskay Ardsshay",c:.02}],
tribesman:[{i:"Oinscay x10",c:.5},{i:"Oisonedpay Earspay",c:.15},{i:"Ibaltray Askmay",c:.03}],
fairy:[{i:"Airyfay Ustday",c:.6},{i:"Aturenay Uneray x3",c:.4},{i:"Airyfay Ingray Iecepay",c:.02}],
mugger:[{i:"Oinscay x8",c:.8},{i:"Onzebray Aggerdray",c:.3}],
rat:[{i:"Onesbay",c:.5},{i:"Atray Ailtay",c:.3}],
snake:[{i:"Akesnay Inskay",c:.5},{i:"Oinscay x6",c:.4},{i:"Antipoisonway",c:.1}],
lizard:[{i:"Izardlay Inskay",c:.5},{i:"Oinscay x10",c:.4}],
elemental:[{i:"Elementalway Oreay",c:.4},{i:"Oinscay x70",c:.5},{i:"Elementalway Ieldshay Ardsshay",c:.03}],
archer:[{i:"Eelstay Arrowway x15",c:.6},{i:"Oinscay x30",c:.5},{i:"Aplemay Owbay",c:.08}],
cultist:[{i:"Oulsay Uneray x3",c:.3},{i:"Arkday Otemtay Iecepay",c:.05},{i:"Oinscay x40",c:.5}],
gargoyle:[{i:"Anitegray Ustday",c:.5},{i:"Oinscay x100",c:.6},{i:"Anitegray Aulmay",c:.03}],
bandit:[{i:"Oinscay x25",c:.8},{i:"Esertday Amuleway",c:.05}],
golem:[{i:"Uniteray Oreay",c:.15},{i:"Oinscay x120",c:.5},{i:"Olemgay Earthay",c:.02}],
wyrm:[{i:"Yrmway Onesbay",c:.8},{i:"Agondray Ifenay",c:.03},{i:"Oinscay x90",c:.5}]};

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
{n:'Aartzhay Itycay',x:1800,z:1200,r:250,lv:60,c:[.48,.16,.08],en:['tzhaar','imp','elemental'],fog:0x8a2010},
// === EXPANDED WORLD REGIONS ===
{n:'Ayercay Undergroundway',x:300,z:150,r:200,lv:20,c:[.15,.12,.10],en:['cavebug','cavecrawler','rockslug','cave_spider'],fog:0x2a2018},
{n:'Elayerscay Undergroundway',x:-100,z:-500,r:300,lv:35,c:[.12,.10,.08],en:['cavehorror','cavekraken','wallbeast','crawhand'],fog:0x1a1810},
{n:'Ayerscay Owerslay',x:400,z:-800,r:250,lv:50,c:[.14,.11,.09],en:['dustdevil','smokdevil','gargoyle2','grotguard'],fog:0x2a2218},
{n:'Irefay Undergroundway',x:800,z:-1200,r:280,lv:60,c:[.20,.08,.05],en:['firegiant','pyrefiend','infernalmage','firefiend','fire_demon'],fog:0x3a1008},
{n:'Iceway Undergroundway',x:-600,z:-2500,r:260,lv:55,c:[.10,.15,.20],en:['icegiant','icefiend','ice_warrior','ice_demon','glacor'],fog:0x1a2a3a},
{n:'Agondray Airslay',x:1500,z:-900,r:350,lv:70,c:[.15,.18,.10],en:['greendragon','bluedragon','bronzedragon'],fog:0x2a3018},
{n:'Agondray Eepday Airslay',x:2000,z:-1200,r:300,lv:85,c:[.10,.08,.06],en:['reddragon','blackdragon','steeldragon','irondragon'],fog:0x1a1008},
{n:'Etalmay Agondray Avescay',x:2500,z:-2000,r:250,lv:95,c:[.08,.08,.10],en:['mithdragon','adamdragon','runedragon'],fog:0x101018},
{n:'Iantsgay Enday',x:-400,z:600,r:250,lv:25,c:[.35,.30,.20],en:['hillgiant','mossgiant','hobgoblin','moss_giant'],fog:0x6a5a38},
{n:'Emonday Airslay',x:600,z:-1500,r:300,lv:60,c:[.12,.06,.08],en:['lessdemon','greatdemon','blackdemon','blood_demon'],fog:0x1a0a10},
{n:'Ellyfjay Avescay',x:-900,z:-600,r:200,lv:40,c:[.15,.18,.12],en:['jelly','jellymut','fungalbeast','zygomite'],fog:0x2a3020},
{n:'Aberrantway Avescay',x:-1100,z:-800,r:220,lv:45,c:[.12,.14,.10],en:['aberspec','devspec','spectre','banshee'],fog:0x1a2218},
{n:'Abyssalway Exusway',x:0,z:-2500,r:300,lv:75,c:[.08,.04,.10],en:['abyssal','abyssaldemon','darkbeast','abyssal_sire'],fog:0x100820},
{n:'Ankouway Ryptcay',x:-300,z:-1200,r:200,lv:50,c:[.08,.08,.08],en:['ankou','shade_lv2','shade_lv3','tortured'],fog:0x101010},
{n:'Avianseway Estroostaay',x:-1800,z:-500,r:250,lv:50,c:[.30,.35,.25],en:['aviansie','spiritual_war','spiritual_mage','spiritual_rang'],fog:0x5a6a48},
{n:'Aterwayfiendway Aircavay',x:-700,z:900,r:200,lv:40,c:[.12,.18,.22],en:['waterfiend','sea_snake','kraken_spawn','siren'],fog:0x1a3040},
{n:'Unglejay Eepthsday',x:-400,z:2800,r:350,lv:30,c:[.20,.40,.12],en:['jungle_demon','jungle_horror','harpie','monkey','venom_spider'],fog:0x3a7a20},
{n:'Abcray Orescay',x:900,z:300,r:180,lv:5,c:[.45,.40,.30],en:['rockcrabs','sandcrabs','ammonite','seagull'],fog:0x8a7a5a},
{n:'Ildernesway Orebay',x:-200,z:-1400,r:280,lv:70,c:[.10,.08,.06],en:['chaos_ele','vetion','callisto','venenatis','revenant2'],fog:0x181008},
{n:'Orkathvay Airslay',x:3200,z:-800,r:250,lv:90,c:[.08,.12,.14],en:['vorkath','wyvern','skeletalwyvern'],fog:0x101a20},
{n:'Orpway Eastbay Airslay',x:3500,z:0,r:200,lv:95,c:[.06,.06,.06],en:['corp_beast','bandos_avatar','sara_avatar','zammy_avatar'],fog:0x0a0a0a},
{n:'Odgay Arsway Ungeonday',x:0,z:-5000,r:400,lv:90,c:[.10,.06,.14],en:['zilyana','graardor','kreearra','kril','nex'],fog:0x180a28},
{n:'Ombstay Ofway Amuthosoray',x:3000,z:1000,r:300,lv:80,c:[.50,.40,.20],en:['tomb_guard','tomb_mage','tomb_ranger','tomb_lord','mummy'],fog:0x907838},
{n:'Uqahsay Islandway',x:-3000,z:-1500,r:200,lv:45,c:[.28,.24,.28],en:['suqah','muspaah','gorak'],fog:0x484048},
{n:'Ystalcray Ealmray',x:-4500,z:-800,r:300,lv:75,c:[.35,.45,.50],en:['crystal_spider','crystal_wolf','dark_elf','elf_warrior','hunllef'],fog:0x6a8a9a},
{n:'Otizoskay Airslay',x:-1500,z:-2000,r:250,lv:65,c:[.06,.04,.10],en:['skotizo','skotos','warped_terror','corrupt_beast','phantom'],fog:0x0a0818},
{n:'Inasmay Irithtay',x:-1500,z:2000,r:300,lv:80,c:[.55,.52,.48],en:['whiteknight','guard','knight','tomb_guard','spiritual_war','elf_warrior'],fog:0xb0a890}
];
const eHP={goblin:32,cow:45,chicken:18,guard:80,darkwiz:65,revenant:120,skeleton:60,demon:160,scorpion:40,warrior:55,whiteknight:90,dwarf:70,barbarian:50,vampire:85,zombie:45,pirate:55,mugger:30,
troll:140,ogre:110,drake:180,bear:95,wolf:65,spider:50,bat:28,ghost:75,golem:200,wyrm:220,shade:90,hellhound:150,imp:35,bandit:70,rat:15,snake:40,lizard:45,elemental:160,gargoyle:190,knight:100,mage:85,archer:70,cultist:95,thief:40,tribesman:55,mummy:130,scarab:60,elf:120,fairy:30,tzhaar:250,
// EXISTING BOSSES
dragon:400,blackdragon:550,hydra:480,kraken:420,cerberus:500,basilisk:180,cockatrice:120,wyvern:280,abyssal:200,dagannoth:160,kalphite:220,jad:650,zuk:900,nightmare:750,vorkath:800,zilyana:600,graardor:700,kreearra:550,kril:650,nex:1000,mimic:300,bloodveld:140,kurask:170,turoth:130,nechryael:200,abyssaldemon:240,darkbeast:260,skeletalwyvern:300,brutalblue:200,brutalred:350,brutalblack:450,
// === 100+ NEW ENEMY TYPES ===
hobgoblin:48,hillgiant:85,mossgiant:95,firegiant:150,icegiant:160,lessdemon:120,greatdemon:200,blackdemon:260,
jelly:110,crawhand:55,wallbeast:65,cavebug:30,cavecrawler:40,cavehorror:130,cavekraken:180,
rockslug:60,desertlizard:50,dustdevil:130,smokdevil:140,gargoyle2:190,grotguard:250,
steeldragon:350,irondragon:280,bronzedragon:200,mithdragon:300,runedragon:500,adamdragon:400,
greendragon:250,bluedragon:280,reddragon:380,
fungalbeast:90,pyrefiend:100,infernalmage:110,jellymut:160,
terrordog:120,banshee:80,spectre:100,aberspec:130,devspec:150,
ankou:75,aviansie:130,spiritual_war:100,spiritual_mage:120,spiritual_rang:110,
waterfiend:140,icefiend:60,firefiend:90,
moss_giant:95,bryophyta:380,obor:350,
chaosdruid:55,dagking_rex:320,dagking_prime:350,dagking_supreme:330,
crazy_arch:60,ent:100,zygomite:85,suqah:140,
jungle_demon:280,jungle_horror:100,harpie:70,
chaos_ele:600,vetion:450,callisto:500,venenatis:480,fanatic:300,scorpia_boss:350,
sarachnis:400,grotguardian:600,skotizo:500,siren:250,
krakenlet:80,seagull:10,penguin:20,monkey:25,terrorbird:60,
chompy:40,jubbly:55,zogre:80,mogre:70,
rockgolem:180,icegolem:200,firegolem:220,
brine_rat:45,cave_eel:30,rockcrabs:35,sandcrabs:30,ammonite:40,
dark_warrior:75,moss_warrior:65,ice_warrior:80,chaos_warrior:90,
black_guard:100,white_wolf:70,dire_wolf:100,ice_troll:160,
rock_troll:150,river_troll:110,mountain_troll:180,
plague_rat:25,giant_rat:35,moss_rat:30,
shade_lv2:120,shade_lv3:160,tortured:200,
abyssal_sire:700,alch_hydra:850,gauntlet:750,hunllef:800,
corp_beast:900,bandos_avatar:300,sara_avatar:300,zammy_avatar:300,
thermy:400,skotos:180,mimic2:280,deranged_arch:180,
warped_terror:160,corrupt_beast:200,phantom:140,
cave_spider:35,shadow_spider:60,venom_spider:85,
tomb_guard:150,tomb_mage:130,tomb_ranger:110,tomb_lord:400,
sea_snake:90,kraken_spawn:60,tentacle:100,
glacor:180,muspaah:200,shadow_leech:50,
crystal_spider:120,crystal_wolf:100,dark_elf:130,elf_warrior:140,
ice_demon:200,fire_demon:200,blood_demon:230,
anc_zygomite:130,gorak:150,revenant2:180,rev_dragon:350,rev_knight:200};
const eCol={goblin:0x2a5a28,cow:0x7a4a2a,chicken:0xcca855,guard:0x4444aa,darkwiz:0x2a0a3a,revenant:0x1a4a3a,skeleton:0xccccaa,demon:0x5a1010,scorpion:0x4a3a10,warrior:0x886830,whiteknight:0xcccccc,dwarf:0x886644,barbarian:0x8a5a30,vampire:0x2a0a1a,zombie:0x3a5a30,pirate:0x554430,mugger:0x3a3a3a,
troll:0x5a5a4a,ogre:0x4a6a30,drake:0x6a3020,bear:0x4a3020,wolf:0x555555,spider:0x2a2a20,bat:0x3a3040,ghost:0x6a8aaa,golem:0x5a5a60,wyrm:0x4a2040,shade:0x2a2a3a,hellhound:0x5a2010,imp:0x8a2020,bandit:0x4a4030,rat:0x5a4a3a,snake:0x2a4a20,lizard:0x4a6a30,elemental:0x2a4a6a,gargoyle:0x5a5a5a,knight:0x6a6a7a,mage:0x3a3a6a,archer:0x4a5a3a,cultist:0x3a1a3a,thief:0x3a3a3a,tribesman:0x5a4a2a,mummy:0x8a7a5a,scarab:0x2a3a1a,elf:0x4a6a5a,fairy:0x6a8aaa,tzhaar:0x8a3010,
dragon:0x2a6a1a,blackdragon:0x1a1a1a,hydra:0x4a6a3a,kraken:0x1a3a5a,cerberus:0x5a1a1a,basilisk:0x5a6a3a,cockatrice:0x6a7a2a,wyvern:0x3a4a5a,abyssal:0x2a0a2a,dagannoth:0x4a5a2a,kalphite:0x5a4a1a,jad:0x8a2a00,zuk:0xaa3a10,nightmare:0x2a1a3a,vorkath:0x2a5a6a,zilyana:0xaaaacc,graardor:0x5a4a3a,kreearra:0x3a5a3a,kril:0x5a1a2a,nex:0x4a0a3a,mimic:0x6a5a2a,bloodveld:0x6a2a2a,kurask:0x4a6a2a,turoth:0x3a5a2a,nechryael:0x4a2a4a,abyssaldemon:0x3a1a3a,darkbeast:0x1a1a2a,skeletalwyvern:0x8a8a7a,brutalblue:0x2a3a6a,brutalred:0x6a2a1a,brutalblack:0x1a1a1a,
hobgoblin:0x3a6a30,hillgiant:0x6a5a3a,mossgiant:0x3a6a2a,firegiant:0x8a3a1a,icegiant:0x4a6a8a,lessdemon:0x6a2a1a,greatdemon:0x5a1a1a,blackdemon:0x1a1a1a,
jelly:0x5a7a5a,crawhand:0x5a4a3a,wallbeast:0x3a3a2a,cavebug:0x4a5a3a,cavecrawler:0x5a5a3a,cavehorror:0x2a1a2a,cavekraken:0x2a3a4a,
rockslug:0x6a6a5a,desertlizard:0x8a7a4a,dustdevil:0x7a6a4a,smokdevil:0x4a4a4a,gargoyle2:0x5a5a5a,grotguard:0x4a4a3a,
steeldragon:0x7a7a8a,irondragon:0x5a5a6a,bronzedragon:0x7a5a2a,mithdragon:0x3a3a6a,runedragon:0x2a5a6a,adamdragon:0x2a5a2a,
greendragon:0x2a6a1a,bluedragon:0x2a3a7a,reddragon:0x7a1a1a,
fungalbeast:0x6a7a5a,pyrefiend:0x7a3a1a,infernalmage:0x6a1a1a,jellymut:0x4a6a4a,
terrordog:0x5a3a2a,banshee:0x7a8a8a,spectre:0x5a6a5a,aberspec:0x4a5a4a,devspec:0x3a4a3a,
ankou:0x1a1a2a,aviansie:0x5a6a3a,spiritual_war:0x5a5a6a,spiritual_mage:0x4a3a6a,spiritual_rang:0x3a5a3a,
waterfiend:0x2a4a7a,icefiend:0x5a7a9a,firefiend:0x8a3a0a,
moss_giant:0x3a6a2a,bryophyta:0x2a5a1a,obor:0x7a5a3a,
chaosdruid:0x3a2a3a,dagking_rex:0x5a3a1a,dagking_prime:0x2a3a5a,dagking_supreme:0x3a5a2a,
crazy_arch:0x5a4a3a,ent:0x4a5a2a,zygomite:0x6a7a4a,suqah:0x5a4a5a,
jungle_demon:0x2a5a2a,jungle_horror:0x3a4a2a,harpie:0x5a4a3a,
chaos_ele:0x5a1a5a,vetion:0x2a1a2a,callisto:0x4a2a1a,venenatis:0x2a3a1a,fanatic:0x3a1a1a,scorpia_boss:0x4a3a1a,
sarachnis:0x6a3a1a,grotguardian:0x4a4a3a,skotizo:0x1a0a2a,siren:0x3a5a7a,
krakenlet:0x2a3a5a,seagull:0x8a8a8a,penguin:0x1a1a2a,monkey:0x6a4a2a,terrorbird:0x5a5a4a,
chompy:0x5a6a3a,jubbly:0x6a5a3a,zogre:0x4a5a2a,mogre:0x3a5a4a,
rockgolem:0x6a6a6a,icegolem:0x5a7a9a,firegolem:0x8a3a1a,
brine_rat:0x5a5a4a,cave_eel:0x3a4a4a,rockcrabs:0x7a6a5a,sandcrabs:0x8a7a5a,ammonite:0x6a5a4a,
dark_warrior:0x2a2a3a,moss_warrior:0x3a5a2a,ice_warrior:0x4a6a8a,chaos_warrior:0x5a2a2a,
black_guard:0x1a1a2a,white_wolf:0x9a9a9a,dire_wolf:0x3a3a3a,ice_troll:0x5a7a8a,
rock_troll:0x6a5a4a,river_troll:0x3a5a5a,mountain_troll:0x5a5a4a,
plague_rat:0x4a5a2a,giant_rat:0x5a4a3a,moss_rat:0x3a5a2a,
shade_lv2:0x2a2a3a,shade_lv3:0x1a1a2a,tortured:0x3a1a1a,
abyssal_sire:0x3a1a3a,alch_hydra:0x5a6a4a,gauntlet:0x4a5a5a,hunllef:0x5a6a5a,
corp_beast:0x2a2a2a,bandos_avatar:0x5a4a2a,sara_avatar:0x7a8aaa,zammy_avatar:0x5a1a1a,
thermy:0x5a5a5a,skotos:0x1a0a1a,mimic2:0x6a5a2a,deranged_arch:0x5a4a3a,
warped_terror:0x4a3a4a,corrupt_beast:0x3a2a3a,phantom:0x5a6a7a,
cave_spider:0x2a2a1a,shadow_spider:0x1a1a2a,venom_spider:0x2a4a1a,
tomb_guard:0x7a6a3a,tomb_mage:0x4a3a5a,tomb_ranger:0x5a5a3a,tomb_lord:0x6a4a1a,
sea_snake:0x2a5a5a,kraken_spawn:0x2a3a5a,tentacle:0x3a2a4a,
glacor:0x6a8aaa,muspaah:0x5a3a5a,shadow_leech:0x1a1a1a,
crystal_spider:0x6a8a9a,crystal_wolf:0x5a7a8a,dark_elf:0x2a3a3a,elf_warrior:0x4a6a4a,
ice_demon:0x4a6a8a,fire_demon:0x8a2a0a,blood_demon:0x5a0a0a,
anc_zygomite:0x5a6a3a,gorak:0x3a2a2a,revenant2:0x2a5a4a,rev_dragon:0x1a4a3a,rev_knight:0x2a4a3a};
// === ALL DROP TABLES (pig latin) ===
drops.dragon=[{i:"Agondray Onesbay",c:1},{i:"Agondray Idehay",c:.9},{i:"Oinscay x500",c:.8},{i:"Agondray Atelegspay",c:.04},{i:"Agondray Edmay Elmhay",c:.06},{i:"Aconicray Isagevay",c:.005}];
drops.blackdragon=[{i:"Agondray Onesbay",c:1},{i:"Ackblay Agondray Idehay",c:.9},{i:"Oinscay x800",c:.7},{i:"Agondray Atebodypay",c:.01},{i:"Aconicray Isagevay",c:.01}];
drops.hydra=[{i:"Ydrahay Onesbay",c:1},{i:"Ydrahay Eatherlay",c:.3},{i:"Ydrahay Awclay",c:.02},{i:"Oinscay x600",c:.7},{i:"Imstonebray Ingray Iecepay",c:.03}];
drops.kraken=[{i:"Akenkray Entacletay",c:.08},{i:"Identtray ofway Eassay",c:.02},{i:"Oinscay x400",c:.6},{i:"Awray Arkshay x5",c:.4}];
drops.cerberus=[{i:"Imordialypray Ystalcray",c:.015},{i:"Egasianpay Ystalcray",c:.015},{i:"Ernaltay Ystalcray",c:.015},{i:"Oulderingsmay Onesay",c:.02},{i:"Oinscay x700",c:.6}];
drops.basilisk=[{i:"Asiliskbay Awjay",c:.02},{i:"Oinscay x150",c:.5},{i:"Ysticmay Athay",c:.04}];
drops.wyvern=[{i:"Yvernway Onesbay",c:.8},{i:"Agondray Atelegspay",c:.02},{i:"Attlestaffbay",c:.08},{i:"Oinscay x350",c:.6}];
drops.abyssal=[{i:"Abyssalway Iphway",c:.015},{i:"Oinscay x200",c:.5},{i:"Eathday Uneray x8",c:.3}];
drops.kalphite=[{i:"Oinscay x100",c:.6},{i:"Otatopay Actuscay",c:.3},{i:"Agondray Ainchay",c:.005}];
drops.jad=[{i:"Irefay Apecay",c:.5},{i:"Okkultay x200",c:.8},{i:"Obsidianway Aulmay",c:.1},{i:"Oinscay x2000",c:.9}];
drops.zuk=[{i:"Infernalway Apecay",c:.4},{i:"Okkultay x500",c:.9},{i:"Oinscay x5000",c:1},{i:"Alkaltay Apecay Ardsshay",c:.1}];
drops.vorkath=[{i:"Orkathvay Eadhay",c:.05},{i:"Agonebonedray Ecklacenay",c:.03},{i:"Agondray Oltsbay x20",c:.3},{i:"Oinscay x3000",c:.8}];
drops.nightmare=[{i:"Ightmarenay Affstay",c:.02},{i:"Inquisitorway Acemay",c:.01},{i:"Oinscay x4000",c:.7},{i:"Orbway ofway Arknessdray",c:.008}];
drops.nex=[{i:"Orvatay Atebodypay",c:.008},{i:"Orvatay Atelegspay",c:.008},{i:"Orvatay Elmhay",c:.008},{i:"Arytezay Ossbowcray",c:.005},{i:"Oinscay x8000",c:.9}];
// Giants
drops.hobgoblin=[{i:"Oinscay x12",c:.7},{i:"Iminithay Ordssway",c:.05},{i:"Imphay",c:.3},{i:"Onesbay",c:.8}];
drops.hillgiant=[{i:"Igbay Onesbay",c:1},{i:"Oinscay x25",c:.6},{i:"Iantgay Eykay",c:.02},{i:"Iminithay Elmhay",c:.05}];
drops.mossgiant=[{i:"Igbay Onesbay",c:1},{i:"Oinscay x30",c:.6},{i:"Ossmay Iantgay Inskay",c:.1},{i:"Aturenay Uneray x3",c:.2}];
drops.firegiant=[{i:"Igbay Onesbay",c:1},{i:"Oinscay x60",c:.7},{i:"Uneray Imitarscay",c:.02},{i:"Irefay Attlestaffbay",c:.03},{i:"Agondray Edmay Elmhay",c:.01}];
drops.icegiant=[{i:"Igbay Onesbay",c:1},{i:"Oinscay x50",c:.6},{i:"Iceway Ordssway",c:.04},{i:"Ozendfray Eykay",c:.02}];
// Demons
drops.lessdemon=[{i:"Oinscay x40",c:.6},{i:"Onesbay",c:.8},{i:"Uneray Edmay Elmhay",c:.01},{i:"Ackblay Atchethay",c:.02}];
drops.greatdemon=[{i:"Oinscay x80",c:.7},{i:"Eathday Uneray x5",c:.2},{i:"Agondray Edmay Elmhay",c:.02},{i:"Irefay Apecay Ardsshay",c:.005}];
drops.blackdemon=[{i:"Oinscay x100",c:.7},{i:"Igbay Onesbay",c:.8},{i:"Eathday Uneray x8",c:.15},{i:"Ackblay Emonday Ashway",c:.02}];
// Slayer creatures
drops.jelly=[{i:"Oinscay x30",c:.5},{i:"Ellyjay Ashway",c:.3},{i:"Uneray Ullnay Agicmay",c:.04}];
drops.crawhand=[{i:"Oinscay x10",c:.5},{i:"Awlingcray Andhay Ashway",c:.2}];
drops.wallbeast=[{i:"Oinscay x15",c:.5},{i:"Allway Eastbay Ashway",c:.3}];
drops.cavebug=[{i:"Oinscay x5",c:.5},{i:"Avecay Ugbay Ingway",c:.2}];
drops.cavecrawler=[{i:"Oinscay x8",c:.5},{i:"Avecay Awlercray Ashway",c:.15}];
drops.cavehorror=[{i:"Oinscay x60",c:.6},{i:"Ackblay Askmay",c:.02},{i:"Enseedimshay",c:.1},{i:"Avecay Orrorphay Ashway",c:.3}];
drops.cavekraken=[{i:"Oinscay x50",c:.5},{i:"Entacletay Ashway",c:.2},{i:"Identtray Ardsshay",c:.01}];
drops.rockslug=[{i:"Oinscay x10",c:.5},{i:"Ockray Ugslay Ashway",c:.2},{i:"Altrock say",c:.1}];
drops.desertlizard=[{i:"Oinscay x8",c:.5},{i:"Esertday Izardlay Inskay",c:.3}];
drops.dustdevil=[{i:"Oinscay x50",c:.6},{i:"Ustday Evilday Ashway",c:.3},{i:"Agondray Ainchay",c:.003},{i:"Ustday Attlestaffbay",c:.02}];
drops.smokdevil=[{i:"Oinscay x60",c:.6},{i:"Okesmay Attlestaffbay",c:.03},{i:"Occultway Ecklacenay",c:.005}];
drops.gargoyle2=[{i:"Oinscay x100",c:.6},{i:"Anitegray Aulmay",c:.02},{i:"Ysticmay Oberay Optay",c:.03},{i:"Anitegray Ustday",c:.5}];
drops.grotguard=[{i:"Oinscay x120",c:.6},{i:"Otesquegray Uardiangay Ashway",c:.3},{i:"Anitegray Ustday",c:.6},{i:"Anitekray Ammerhay",c:.01}];
// Metal dragons
drops.steeldragon=[{i:"Agondray Onesbay",c:1},{i:"Oinscay x300",c:.6},{i:"Agondray Atelegspay",c:.02},{i:"Eelstay Arbay",c:.3}];
drops.irondragon=[{i:"Agondray Onesbay",c:1},{i:"Oinscay x200",c:.6},{i:"Ironway Arbay x5",c:.3},{i:"Agondray Edmay Elmhay",c:.01}];
drops.bronzedragon=[{i:"Agondray Onesbay",c:1},{i:"Oinscay x120",c:.6},{i:"Onzebray Arbay x10",c:.4}];
drops.mithdragon=[{i:"Agondray Onesbay",c:1},{i:"Oinscay x350",c:.6},{i:"Ithrilmay Arbay x5",c:.3}];
drops.runedragon=[{i:"Agondray Onesbay",c:1},{i:"Oinscay x800",c:.7},{i:"Agondray Onebay Ecklacenay",c:.01},{i:"Uneray Arbay x3",c:.2},{i:"Agonitedray Etalmay Icepay",c:.05}];
drops.adamdragon=[{i:"Agondray Onesbay",c:1},{i:"Oinscay x500",c:.6},{i:"Adamantway Arbay x5",c:.3}];
// Chromatic dragons
drops.greendragon=[{i:"Agondray Onesbay",c:1},{i:"Eengray Agonhidedray",c:.85},{i:"Oinscay x150",c:.6}];
drops.bluedragon=[{i:"Agondray Onesbay",c:1},{i:"Ueblay Agonhidedray",c:.85},{i:"Oinscay x200",c:.6}];
drops.reddragon=[{i:"Agondray Onesbay",c:1},{i:"Edray Agonhidedray",c:.85},{i:"Oinscay x350",c:.6},{i:"Agondray Ordssway",c:.01}];
// Other slayer/misc
drops.fungalbeast=[{i:"Oinscay x20",c:.5},{i:"Ungalfay Ashway",c:.3},{i:"Oompshray",c:.1}];
drops.pyrefiend=[{i:"Oinscay x25",c:.5},{i:"Yrepay Ashway",c:.2},{i:"Irefay Uneray x10",c:.15}];
drops.infernalmage=[{i:"Oinscay x35",c:.5},{i:"Irefay Uneray x15",c:.2},{i:"Ysticmay Oberay Optay",c:.03}];
drops.jellymut=[{i:"Oinscay x45",c:.5},{i:"Utatedmay Ellyjay Ashway",c:.3},{i:"Eathday Uneray x5",c:.15}];
drops.terrordog=[{i:"Oinscay x40",c:.5},{i:"Errorday Ogday Ashway",c:.3}];
drops.banshee=[{i:"Oinscay x15",c:.5},{i:"Ansheebay Ashway",c:.3},{i:"Ysticmay Ovesglay",c:.01}];
drops.spectre=[{i:"Oinscay x20",c:.5},{i:"Ectrespay Ashway",c:.2}];
drops.aberspec=[{i:"Oinscay x40",c:.5},{i:"Aberrantway Ectrespay Ashway",c:.3}];
drops.devspec=[{i:"Oinscay x50",c:.5},{i:"Eviantday Ectrespay Ashway",c:.3}];
drops.ankou=[{i:"Oinscay x30",c:.6},{i:"Eathday Uneray x3",c:.3},{i:"Ankouway Ashway",c:.2}];
drops.aviansie=[{i:"Oinscay x50",c:.5},{i:"Adamantway Arbay x3",c:.3},{i:"Avianseway Ashway",c:.2}];
drops.waterfiend=[{i:"Oinscay x30",c:.5},{i:"Aterway Orbway",c:.15},{i:"Aterwayfiendway Ashway",c:.2}];
drops.icefiend=[{i:"Oinscay x10",c:.5},{i:"Iceway Ustday",c:.3}];
drops.firefiend=[{i:"Oinscay x20",c:.5},{i:"Irefay Orbway",c:.1}];
drops.bryophyta=[{i:"Yophytabray Essenceay",c:.5},{i:"Oinscay x300",c:.8},{i:"Uneray Essenceay x50",c:.3}];
drops.obor=[{i:"Illhay Iantgay Ubclay",c:.3},{i:"Oinscay x250",c:.8},{i:"Iantgay Eykay",c:.5}];
drops.chaosdruid=[{i:"Erbhay",c:.6},{i:"Oinscay x10",c:.5},{i:"Aturenay Uneray x2",c:.2}];
drops.dagking_rex=[{i:"Agannothday Onesbay",c:1},{i:"Eserkersbay Ingray",c:.02},{i:"Oinscay x400",c:.7}];
drops.dagking_prime=[{i:"Agannothday Onesbay",c:1},{i:"Eerssay Ingray",c:.02},{i:"Oinscay x400",c:.7}];
drops.dagking_supreme=[{i:"Agannothday Onesbay",c:1},{i:"Archersway Ingray",c:.02},{i:"Oinscay x400",c:.7}];
// Wilderness bosses
drops.chaos_ele=[{i:"Oinscay x600",c:.7},{i:"Agondray Ickaxepay",c:.02},{i:"Etpay Aoscay Elementalay",c:.005}];
drops.vetion=[{i:"Oinscay x500",c:.7},{i:"Ingray ofway Egodstay",c:.01},{i:"Arkday Awclay",c:.02}];
drops.callisto=[{i:"Oinscay x500",c:.7},{i:"Ingray ofway Egodstay",c:.01},{i:"Allistocay Ubcay",c:.05}];
drops.venenatis=[{i:"Oinscay x500",c:.7},{i:"Ingray ofway Egodstay",c:.01},{i:"Reblightcay Eethlay",c:.02}];
drops.fanatic=[{i:"Oinscay x300",c:.7},{i:"Anaticclifay Ashway",c:.3}];
drops.scorpia_boss=[{i:"Oinscay x350",c:.7},{i:"Orpiascay Ashway",c:.3},{i:"Odiumway Ardsshay",c:.01}];
// Medium bosses
drops.sarachnis=[{i:"Arachniscay Uddycay",c:.03},{i:"Oinscay x200",c:.6},{i:"Iantgay Eggway Acksay",c:.1}];
drops.grotguardian=[{i:"Anitegray Ustday x500",c:.8},{i:"Oinscay x300",c:.7},{i:"Anitekray Ammerhay",c:.02}];
drops.skotizo=[{i:"Arkday Otemtay",c:.1},{i:"Oinscay x500",c:.7},{i:"Arkday Awclay",c:.05}];
drops.siren=[{i:"Irensay Earltay",c:.05},{i:"Oinscay x200",c:.6},{i:"Istyway Aterway",c:.3}];
// Small creatures
drops.krakenlet=[{i:"Oinscay x15",c:.5},{i:"Entacletay Ashway",c:.3}];
drops.seagull=[{i:"Eathersfay",c:.8},{i:"Onesbay",c:.5}];
drops.penguin=[{i:"Oinscay x5",c:.6},{i:"Enguinpay Eathersfay",c:.3}];
drops.monkey=[{i:"Onkeymay Onesbay",c:.5},{i:"Ananabay",c:.4}];
drops.terrorbird=[{i:"Errorbirdtay Eathersfay",c:.7},{i:"Awray Eatmay",c:.5}];
drops.chompy=[{i:"Ompychay Eatmay",c:.8},{i:"Oinscay x10",c:.4}];
drops.jubbly=[{i:"Ubblyjay Eatmay",c:.8},{i:"Eathersfay x5",c:.5}];
drops.zogre=[{i:"Ogrezay Onesbay",c:.7},{i:"Oinscay x20",c:.5}];
drops.mogre=[{i:"Ogremay Onesbay",c:.6},{i:"Udelmay Iepay",c:.3}];
// Golems
drops.rockgolem=[{i:"Ockray Agmentfray x5",c:.5},{i:"Oinscay x80",c:.5}];
drops.icegolem=[{i:"Iceway Agmentfray x5",c:.5},{i:"Oinscay x100",c:.5}];
drops.firegolem=[{i:"Irefay Agmentfray x5",c:.5},{i:"Oinscay x100",c:.5}];
// Crabs
drops.rockcrabs=[{i:"Oinscay x3",c:.5},{i:"Ockray Ellshay",c:.2}];
drops.sandcrabs=[{i:"Oinscay x3",c:.5},{i:"Andsay Ellshay",c:.2}];
drops.ammonite=[{i:"Oinscay x5",c:.5},{i:"Ossilfay",c:.15}];
drops.brine_rat=[{i:"Inebray Abresay",c:.02},{i:"Oinscay x8",c:.5}];
// Warriors
drops.dark_warrior=[{i:"Oinscay x20",c:.6},{i:"Ackblay Ordssway",c:.04}];
drops.moss_warrior=[{i:"Oinscay x15",c:.6},{i:"Ossmay Ordssway",c:.04}];
drops.ice_warrior=[{i:"Oinscay x25",c:.6},{i:"Iceway Ordssway",c:.04},{i:"Iceway Ardsshay",c:.01}];
drops.chaos_warrior=[{i:"Oinscay x30",c:.6},{i:"Aoscay Ordssway",c:.04}];
drops.black_guard=[{i:"Oinscay x40",c:.6},{i:"Ackblay Armorway",c:.02}];
// Wolves
drops.white_wolf=[{i:"Olfway Onesbay",c:.7},{i:"Iteway Urfay",c:.5}];
drops.dire_wolf=[{i:"Olfway Onesbay",c:.8},{i:"Arkday Urfay",c:.4},{i:"Angfay",c:.08}];
// Trolls
drops.ice_troll=[{i:"Olltray Onesbay",c:.8},{i:"Oinscay x50",c:.6},{i:"Anitegray x5",c:.3}];
drops.rock_troll=[{i:"Olltray Onesbay",c:.8},{i:"Oinscay x45",c:.6},{i:"Anitegray x3",c:.4}];
drops.river_troll=[{i:"Olltray Onesbay",c:.7},{i:"Oinscay x30",c:.5},{i:"Ishingfay Otionpay",c:.05}];
drops.mountain_troll=[{i:"Olltray Onesbay",c:.8},{i:"Oinscay x60",c:.6},{i:"Anitegray x5",c:.4}];
// Rats
drops.plague_rat=[{i:"Oinscay x3",c:.5},{i:"Agueplay Ampleexay",c:.1}];
drops.giant_rat=[{i:"Oinscay x5",c:.5},{i:"Atray Ailtay",c:.3}];
drops.moss_rat=[{i:"Oinscay x3",c:.5},{i:"Ossmay Agmentfray",c:.2}];
// Shades
drops.shade_lv2=[{i:"Adeshay Ashway",c:.3},{i:"Oinscay x40",c:.5},{i:"Eathday Uneray x3",c:.2}];
drops.shade_lv3=[{i:"Adeshay Ashway",c:.4},{i:"Oinscay x60",c:.5},{i:"Eathday Uneray x5",c:.2}];
drops.tortured=[{i:"Orturedtay Ashway",c:.3},{i:"Oinscay x80",c:.5},{i:"Oodblay Uneray x3",c:.15}];
// End-game bosses
drops.abyssal_sire=[{i:"Abyssalway Iphway",c:.1},{i:"Abyssalway Aggerdray",c:.03},{i:"Abyssalway Orphanway",c:.02},{i:"Oinscay x600",c:.7}];
drops.alch_hydra=[{i:"Ydrahay Awclay",c:.05},{i:"Ydrahay Eatherlay",c:.2},{i:"Oinscay x1500",c:.8},{i:"Imstonebray Ingray",c:.02}];
drops.gauntlet=[{i:"Ystalcray Armorway Eedsay",c:.08},{i:"Ystalcray Eaponway Eedsay",c:.08},{i:"Oinscay x800",c:.7}];
drops.hunllef=[{i:"Enhancedway Ystalcray Eaponway Eedsay",c:.04},{i:"Oinscay x1200",c:.8}];
drops.corp_beast=[{i:"Oulsay Igillsay",c:.01},{i:"Elysianway Igillsay",c:.003},{i:"Oinscay x5000",c:.9},{i:"Olyway Elixirway",c:.01}];
drops.thermy=[{i:"Okesmay Attlestaffbay",c:.04},{i:"Etpay Okesmay Evilday",c:.003},{i:"Oinscay x500",c:.7}];
drops.skotizo=[{i:"Arkday Awclay",c:.05},{i:"Arkday Otemtay",c:.1},{i:"Oinscay x500",c:.7}];
// Tomb enemies
drops.tomb_guard=[{i:"Ombstay Oldgay",c:.3},{i:"Oinscay x100",c:.5},{i:"Arahsphay Eptresay",c:.02}];
drops.tomb_mage=[{i:"Ombstay Oldgay",c:.3},{i:"Eathday Uneray x5",c:.3},{i:"Oinscay x80",c:.5}];
drops.tomb_ranger=[{i:"Ombstay Oldgay",c:.3},{i:"Agondray Arrowway x15",c:.2},{i:"Oinscay x80",c:.5}];
drops.tomb_lord=[{i:"Angfay ofway Amuthosoray",c:.02},{i:"Oinscay x1000",c:.8},{i:"Ombstay Oldgay x10",c:.5}];
// Misc
drops.cave_spider=[{i:"Iderspay Ilksay",c:.4},{i:"Oinscay x3",c:.5}];
drops.shadow_spider=[{i:"Iderspay Ilksay",c:.5},{i:"Adowshay Ilksay",c:.15}];
drops.venom_spider=[{i:"Iderspay Ilksay",c:.5},{i:"Enomvay",c:.2},{i:"Antipoisonway",c:.1}];
drops.sea_snake=[{i:"Akesnay Inskay",c:.4},{i:"Awray Almonsay",c:.3}];
drops.glacor=[{i:"Acialglay Agmentfray",c:.2},{i:"Oinscay x100",c:.5}];
drops.muspaah=[{i:"Uspahmay Inespay",c:.15},{i:"Oinscay x120",c:.5}];
drops.crystal_spider=[{i:"Ystalcray Agmentfray",c:.15},{i:"Oinscay x60",c:.5}];
drops.crystal_wolf=[{i:"Ystalcray Agmentfray",c:.1},{i:"Oinscay x50",c:.5}];
drops.dark_elf=[{i:"Arkday Arrowway x10",c:.3},{i:"Oinscay x50",c:.5}];
drops.elf_warrior=[{i:"Ystalcray Ardsshay",c:.3},{i:"Oinscay x60",c:.5}];
drops.ice_demon=[{i:"Iceway Agmentfray x3",c:.3},{i:"Oinscay x100",c:.5}];
drops.fire_demon=[{i:"Irefay Agmentfray x3",c:.3},{i:"Oinscay x100",c:.5}];
drops.blood_demon=[{i:"Oodblay Agmentfray x3",c:.3},{i:"Oinscay x120",c:.5}];
drops.revenant2=[{i:"Evenantray Ethereay x15",c:.5},{i:"Oinscay x200",c:.5}];
drops.rev_dragon=[{i:"Evenantray Ethereay x30",c:.5},{i:"Oinscay x500",c:.6},{i:"Aconicray Isagevay",c:.003}];
drops.rev_knight=[{i:"Evenantray Ethereay x20",c:.5},{i:"Oinscay x300",c:.6}];
drops.spiritual_war=[{i:"Oinscay x30",c:.5},{i:"Adamantway Ootsbay",c:.04}];
drops.spiritual_mage=[{i:"Oinscay x40",c:.5},{i:"Agondray Ootsbay",c:.02}];
drops.spiritual_rang=[{i:"Oinscay x35",c:.5},{i:"Uneray Ootsbay",c:.03}];
drops.cave_eel=[{i:"Awray Avecay Eelway",c:.8},{i:"Oinscay x3",c:.4}];
drops.shadow_leech=[{i:"Adowshay Essenceay",c:.3},{i:"Oinscay x8",c:.5}];
drops.phantom=[{i:"Antomphay Ashway",c:.3},{i:"Oinscay x50",c:.5}];
drops.warped_terror=[{i:"Arpedway Ashway",c:.3},{i:"Oinscay x60",c:.5}];
drops.corrupt_beast=[{i:"Orruptcay Ashway",c:.3},{i:"Oinscay x80",c:.5}];
drops.deranged_arch=[{i:"Oinscay x100",c:.5},{i:"Ockpicklay",c:.1}];
drops.crazy_arch=[{i:"Oinscay x20",c:.5},{i:"Ockpicklay",c:.08}];
drops.ent=[{i:"Oinscay x15",c:.5},{i:"Ogway x3",c:.4}];
drops.zygomite=[{i:"Oinscay x20",c:.5},{i:"Ygomitezay Ashway",c:.2}];
drops.suqah=[{i:"Oinscay x50",c:.5},{i:"Uqahsay Idetay",c:.15}];
drops.jungle_demon=[{i:"Oinscay x150",c:.6},{i:"Unglejay Emonday Ashway",c:.3}];
drops.jungle_horror=[{i:"Oinscay x30",c:.5},{i:"Unglejay Orrorphay Ashway",c:.2}];
drops.harpie=[{i:"Oinscay x15",c:.5},{i:"Arpiehay Eathersfay",c:.3}];
drops.gorak=[{i:"Oinscay x80",c:.5},{i:"Orakgay Ashway",c:.2}];
drops.anc_zygomite=[{i:"Oinscay x40",c:.5},{i:"Ygomitezay Essenceay",c:.15}];
drops.mimic2=[{i:"Oinscay x200",c:.7},{i:"Imicmay Asketbay",c:.1},{i:"Irdway Aff stay",c:.03}];
drops.skotos=[{i:"Arkday Awclay",c:.1},{i:"Oinscay x100",c:.5}];
drops.bandos_avatar=[{i:"Oinscay x200",c:.6},{i:"Andosbay Agmentfray",c:.3}];
drops.sara_avatar=[{i:"Oinscay x200",c:.6},{i:"Aradominsay Agmentfray",c:.3}];
drops.zammy_avatar=[{i:"Oinscay x200",c:.6},{i:"Amorakzay Agmentfray",c:.3}];
drops.zilyana=[{i:"Aradominsay Ordssway",c:.02},{i:"Oinscay x500",c:.7},{i:"Araminsay Ightlay",c:.003}];
drops.graardor=[{i:"Andosbay Estplatechay",c:.02},{i:"Oinscay x600",c:.7},{i:"Andosbay Iltshay",c:.005}];
drops.kreearra=[{i:"Armadylway Estplatechay",c:.02},{i:"Oinscay x500",c:.7},{i:"Armadylway Iltshay",c:.005}];
drops.kril=[{i:"Amorakzay Earspay",c:.02},{i:"Oinscay x500",c:.7},{i:"Amorakzay Iltshay",c:.005}];
drops.cockatrice=[{i:"Oinscay x20",c:.5},{i:"Ockatricecay Eadhay",c:.1}];
drops.dagannoth=[{i:"Agannothday Idehay",c:.3},{i:"Oinscay x30",c:.5}];
drops.bloodveld=[{i:"Oinscay x40",c:.5},{i:"Oodblay Uneray x3",c:.2},{i:"Oodveldblayashway",c:.3}];
drops.kurask=[{i:"Oinscay x60",c:.5},{i:"Uraskay Eaflay",c:.2},{i:"Atureay Ordssway",c:.005}];
drops.turoth=[{i:"Oinscay x30",c:.5},{i:"Urothway Eaflay",c:.2}];
drops.nechryael=[{i:"Oinscay x80",c:.5},{i:"Uneray Ootsbay",c:.03},{i:"Echryaelnay Ashway",c:.2}];
drops.abyssaldemon=[{i:"Abyssalway Iphway",c:.004},{i:"Oinscay x100",c:.5},{i:"Abyssalway Eadhay",c:.1}];
drops.darkbeast=[{i:"Arkday Owbay",c:.01},{i:"Oinscay x120",c:.5},{i:"Arkbeastday Ashway",c:.2}];
drops.skeletalwyvern=[{i:"Yvernway Onesbay",c:.8},{i:"Oinscay x200",c:.5},{i:"Agondray Atelegspay",c:.015}];
drops.brutalblue=[{i:"Agondray Onesbay",c:1},{i:"Ueblay Agonhidedray x2",c:.6},{i:"Oinscay x150",c:.5}];
drops.brutalred=[{i:"Agondray Onesbay",c:1},{i:"Edray Agonhidedray x2",c:.6},{i:"Oinscay x250",c:.5}];
drops.brutalblack=[{i:"Agondray Onesbay",c:1},{i:"Ackblay Agonhidedray x2",c:.6},{i:"Oinscay x400",c:.6}];
drops.kraken_spawn=[{i:"Oinscay x10",c:.5}];drops.tentacle=[{i:"Oinscay x15",c:.5}];
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
// Eyes - store references for animation
const eyeMat=new MS({color:0x111111,roughness:1});
const eyes=[];
[-1,1].forEach(s=>{const eye=new THREE.Mesh(new THREE.SphereGeometry(.15,5,5),eyeMat);eye.position.set(s*.45,10,1.15);body.add(eye);eyes.push(eye)});
// Neck
const neck=new THREE.Mesh(new THREE.CylinderGeometry(.5,.6,.8,8),mt_skinBase);neck.position.y=8.5;body.add(neck);
// Torso
const torso=new THREE.Mesh(new THREE.BoxGeometry(3.2,4,1.8),mt_skinBase);torso.position.y=5.8;body.add(torso);
// Arms with elbow joints for proper articulation
const buildArm=(side)=>{
const arm=new THREE.Group();arm.position.set(side*2.4,7.8,0);
// Upper arm (shoulder to elbow)
const ua=new THREE.Mesh(new THREE.CylinderGeometry(.4,.38,2.8,8),mt_skinBase);ua.position.y=-1.4;arm.add(ua);
// Elbow group - pivot point for forearm
const elbow=new THREE.Group();elbow.position.y=-2.8;arm.add(elbow);
// Forearm (elbow to wrist)
const fa=new THREE.Mesh(new THREE.CylinderGeometry(.38,.32,2.6,8),mt_skinBase);fa.position.y=-1.3;elbow.add(fa);
// Hand
const hand=new THREE.Mesh(new THREE.BoxGeometry(.6,.4,.7),mt_skinBase);hand.position.y=-2.8;elbow.add(hand);
// Store elbow reference for animation
arm.userData.elbow=elbow;
return arm};
const lArm=buildArm(-1);body.add(lArm);
const rArm=buildArm(1);body.add(rArm);
// Legs (bare) - using Groups for animation
const buildLeg=(side)=>{
const leg=new THREE.Group();leg.position.set(side*.8,2.5,0);
// Thigh (upper leg)
const thigh=new THREE.Mesh(new THREE.CylinderGeometry(.5,.45,3,8),mt_skinBase);thigh.position.y=-1.5;leg.add(thigh);
// Knee group for lower leg animation
const knee=new THREE.Group();knee.position.y=-3;leg.add(knee);
// Shin (lower leg)
const shin=new THREE.Mesh(new THREE.CylinderGeometry(.42,.35,3,8),mt_skinBase);shin.position.y=-1.5;knee.add(shin);
// Foot
const foot=new THREE.Mesh(new THREE.BoxGeometry(.7,.5,1.3),mt_skinBase);foot.position.set(0,-3,.15);knee.add(foot);
leg.userData.knee=knee; // Store reference for animation
return leg;
};
const lLeg=buildLeg(-1);body.add(lLeg);
const rLeg=buildLeg(1);body.add(rLeg);
// Body center for breathing animation
const bodyCenter=new THREE.Group();bodyCenter.position.y=5;body.add(bodyCenter);
// Head group for looking/idle animation
const headGroup=new THREE.Group();headGroup.position.y=10;body.add(headGroup);
// Re-parent head meshes to headGroup
head.position.set(0,0,0);headGroup.add(head);
eyes.forEach(eye=>{eye.position.set(eye.position.x-0,eye.position.y-10,eye.position.z-0);headGroup.add(eye)});
// Store references for animation
return{lArm,rArm,lLeg,rLeg,bodyCenter,headGroup};
}

function addHelm_Knight(headGroup){
// Helm perfectly covers head sphere (radius 1.2)
const helmBase=new THREE.Mesh(new THREE.SphereGeometry(1.65,12,12),mt.armorDk);helmBase.position.y=0;helmBase.scale.set(1,1.28,1);headGroup.add(helmBase);
const faceplate=new THREE.Mesh(new THREE.BoxGeometry(2.4,1.9,.3),mt.armorLt);faceplate.position.set(0,-.25,.62);headGroup.add(faceplate);
const visorMat=new MS({color:0x040404,roughness:1});
for(let i=0;i<3;i++){const vs=new THREE.Mesh(new THREE.BoxGeometry(1.5+(.3-i*.15),.1,.35),visorMat);vs.position.set(0,0.05-i*.26,.72);headGroup.add(vs)}
const nasal=new THREE.Mesh(new THREE.BoxGeometry(.2,1.7,.35),mt.armorLt);nasal.position.set(0,-.2,.75);headGroup.add(nasal);
const crest=new THREE.Mesh(new THREE.BoxGeometry(.3,1.1,.9),mt.armorDk);crest.position.set(0,1.3,-.55);headGroup.add(crest);
const aventail=new THREE.Mesh(new THREE.CylinderGeometry(1.75,1.95,1.5,10,1,true),mt.chainmail);aventail.position.y=-1.2;headGroup.add(aventail);
const plume=new THREE.Mesh(new THREE.BoxGeometry(.35,2.4,.6),mt.cape);plume.position.set(0,1.6,-.55);plume.rotation.x=.15;headGroup.add(plume);
}
function addChest_Knight(bodyCenter){
// Gorget - neck protection, flush with helm aventail
const gorget=new THREE.Mesh(new THREE.CylinderGeometry(1.25,1.35,1.2,10),mt.armorLt);gorget.position.y=2.8;bodyCenter.add(gorget);
// Torso - main chest plate, covers body cylinder
const torso=new THREE.Mesh(new THREE.BoxGeometry(3.7,4.2,2.4),mt.armorDk);torso.position.y=.6;bodyCenter.add(torso);
const ridge=new THREE.Mesh(new THREE.BoxGeometry(.35,3.6,.4),mt.armorLt);ridge.position.set(0,.6,1.25);bodyCenter.add(ridge);
[-1,1].forEach(s=>{const cp=new THREE.Mesh(new THREE.BoxGeometry(1.5,1.8,.35),mt.armorLt);cp.position.set(s*.75,1.6,1.25);bodyCenter.add(cp)});
for(let i=0;i<6;i++){const rv=new THREE.Mesh(new THREE.SphereGeometry(.1,4,4),mt.gold);rv.position.set(-.65+i*.26,2.4,1.4);bodyCenter.add(rv)}
// Fauld - lower torso protection
const fauld=new THREE.Mesh(new THREE.BoxGeometry(3.9,1.4,2.5),mt.armorWorn);fauld.position.y=-1.6;bodyCenter.add(fauld);
const belt=new THREE.Mesh(new THREE.BoxGeometry(4.1,.7,2.5),mt.leather);belt.position.y=-1.3;bodyCenter.add(belt);
const buckle=new THREE.Mesh(new THREE.BoxGeometry(.8,.55,.35),mt.gold);buckle.position.set(0,-1.3,1.3);bodyCenter.add(buckle);
}
function addLegs_Knight(lLeg,rLeg,bodyCenter){
// Tassets - thigh protection plates, attach to body center
[-1.3,-.4,.4,1.3].forEach(x=>{const tas=new THREE.Mesh(new THREE.BoxGeometry(1,2,.25),mt.armorDk);tas.position.set(x,-2.6,1.15);bodyCenter.add(tas)});
// Mail skirt - flexible protection between torso and legs
const mailSkirt=new THREE.Mesh(new THREE.CylinderGeometry(1.7,2.1,2.2,10,1,true),mt.chainmail);mailSkirt.position.y=-2.8;bodyCenter.add(mailSkirt);
// Upper leg armor (cuisse) attaches to leg groups (moves with thigh)
// Thigh mesh is at leg y=-1.5, height 3, radius 0.5-0.45
const addLegArmor=(leg)=>{
const cuisse=new THREE.Mesh(new THREE.CylinderGeometry(.68,.62,3.2,8),mt.armorWorn);cuisse.position.y=-1.5;leg.add(cuisse);
// Poleyn - knee armor
const poleyn=new THREE.Mesh(new THREE.SphereGeometry(.65,8,6),mt.armorDk);poleyn.position.y=-3;leg.add(poleyn);
};
addLegArmor(lLeg);addLegArmor(rLeg);
}
function addBoots_Knight(lKnee,rKnee){
// Boots attach to knee groups (lower leg) so they move with shin animation
// Shin mesh is at knee y=-1.5, height 3, radius 0.42-0.35
const addBoot=(knee)=>{
// Sabaton - foot armor, covers foot mesh at knee y=-3
const boot=new THREE.Mesh(new THREE.BoxGeometry(1.1,.9,1.8),mt.armorDk);boot.position.set(0,-.4,.15);knee.add(boot);
const toe=new THREE.Mesh(new THREE.BoxGeometry(.9,.35,.7),mt.armorLt);toe.position.set(0,-.65,.85);knee.add(toe);
const sole=new THREE.Mesh(new THREE.BoxGeometry(1.15,.18,1.9),mt.leather);sole.position.set(0,-.85,.15);knee.add(sole);
// Greave - lower leg armor, covers shin
const greave=new THREE.Mesh(new THREE.CylinderGeometry(.48,.42,3.1,8),mt.armorDk);greave.position.y=-1.5;knee.add(greave);
};
addBoot(lKnee);addBoot(rKnee);
}
function addShield(lArm){
// Shield attaches to forearm (elbow group) so it moves with arm rotation
if(lArm.userData&&lArm.userData.elbow){
const shield=new THREE.Mesh(new THREE.BoxGeometry(.35,4,2.8),mt.armorDk);shield.position.set(-.5,-1.7,.3);lArm.userData.elbow.add(shield);
const shBordV=new THREE.Mesh(new THREE.BoxGeometry(.38,.3,2.9),mt.armorLt);shBordV.position.set(-.5,.6,.3);lArm.userData.elbow.add(shBordV);
const shBordB=new THREE.Mesh(new THREE.BoxGeometry(.38,.3,2.9),mt.armorLt);shBordB.position.set(-.5,-3.8,.3);lArm.userData.elbow.add(shBordB);
const sBoss=new THREE.Mesh(new THREE.SphereGeometry(.45,8,8),mt.gold);sBoss.position.set(-.7,-1.7,.3);lArm.userData.elbow.add(sBoss);
}else{
// Fallback to arm if no elbow
const shield=new THREE.Mesh(new THREE.BoxGeometry(.35,4,2.8),mt.armorDk);shield.position.set(-.5,-4.5,.3);lArm.add(shield);
const shBordV=new THREE.Mesh(new THREE.BoxGeometry(.38,.3,2.9),mt.armorLt);shBordV.position.set(-.5,-2.6,.3);lArm.add(shBordV);
const shBordB=new THREE.Mesh(new THREE.BoxGeometry(.38,.3,2.9),mt.armorLt);shBordB.position.set(-.5,-6.4,.3);lArm.add(shBordB);
const sBoss=new THREE.Mesh(new THREE.SphereGeometry(.45,8,8),mt.gold);sBoss.position.set(-.7,-4.5,.3);lArm.add(sBoss);}
}
function addSword(rArm){
// Sword attaches to hand (elbow group) so it rotates naturally with hand
const attachTo=rArm.userData&&rArm.userData.elbow?rArm.userData.elbow:rArm;
const handY=rArm.userData&&rArm.userData.elbow?-2.8:-6.5;
const blade=new THREE.Mesh(new THREE.BoxGeometry(.2,.18,7.5),mt.swordBlade);blade.position.set(0,handY+4,3.8);blade.rotation.x=.06;attachTo.add(blade);
const fuller=new THREE.Mesh(new THREE.BoxGeometry(.06,.1,5.5),new MS({color:0x556,roughness:.15,metalness:.9}));fuller.position.set(0,handY+4.1,3.8);fuller.rotation.x=.06;attachTo.add(fuller);
const xguard=new THREE.Mesh(new THREE.BoxGeometry(1.6,.25,.25),mt.swordHilt);xguard.position.set(0,handY,.15);attachTo.add(xguard);
[-1,1].forEach(s=>{const tip=new THREE.Mesh(new THREE.SphereGeometry(.12,5,5),mt.gold);tip.position.set(s*.8,handY,.15);attachTo.add(tip)});
const hilt=new THREE.Mesh(new THREE.CylinderGeometry(.14,.14,1.4,6),mt.leather);hilt.position.set(0,handY,-.4);hilt.rotation.x=Math.PI/2;attachTo.add(hilt);
const pommel=new THREE.Mesh(new THREE.SphereGeometry(.2,6,6),mt.gold);pommel.position.set(0,handY,-1.1);attachTo.add(pommel);
// FIX: Reposition sword to actually be held in hand - blade extends outward from hand
blade.position.set(0,handY-3.5,0.3);blade.rotation.set(Math.PI/2,0,0);
fuller.position.set(0,handY-3.5,0.35);fuller.rotation.set(Math.PI/2,0,0);
xguard.position.set(0,handY,0.3);
[-1,1].forEach(s=>{const tip=attachTo.children[attachTo.children.length-4+s];if(tip)tip.position.set(s*.8,handY,0.3);});
hilt.position.set(0,handY+0.2,0.3);hilt.rotation.set(Math.PI/2,0,0);
pommel.position.set(0,handY+0.9,0.3);
}
function addStaff(rArm){
// Staff attaches to hand (elbow group) for natural hand rotation
const attachTo=rArm.userData&&rArm.userData.elbow?rArm.userData.elbow:rArm;
// Staff properly held in hand
const staffGrp=new THREE.Group();staffGrp.position.set(0,-2.8,.3);staffGrp.rotation.x=0.2;attachTo.add(staffGrp);
// Shaft extends upward from hand
const shaft=new THREE.Mesh(new THREE.CylinderGeometry(.1,.08,7,6),mt.wd);shaft.position.set(0,3.5,0);staffGrp.add(shaft);
// Glowing orb at top of staff
const orb=new THREE.Mesh(new THREE.SphereGeometry(.45,8,8),new MS({color:0x6644cc,emissive:0x4422aa,emissiveIntensity:1.2,roughness:.3}));orb.position.set(0,7,0);staffGrp.add(orb);
// Gold ring around orb
const orbRing=new THREE.Mesh(new THREE.TorusGeometry(.5,.05,6,12),mt.gold);orbRing.position.set(0,7,0);orbRing.rotation.x=Math.PI/2;staffGrp.add(orbRing);
// Small gems on shaft
for(let i=0;i<3;i++){const gem=new THREE.Mesh(new THREE.SphereGeometry(.08,6,6),new MS({color:0xaa88ff,emissive:0x6644cc,emissiveIntensity:.5}));gem.position.set(0,2+i*2,0);staffGrp.add(gem);}
}
function addBow(rArm){
// Bow held in right hand - attaches to elbow group for natural rotation
const attachTo=rArm.userData&&rArm.userData.elbow?rArm.userData.elbow:rArm;
const handY=rArm.userData&&rArm.userData.elbow?-2.8:-6;
const bowCurve=new THREE.Mesh(new THREE.TorusGeometry(1.2,.08,6,16,Math.PI),new MS({color:0x8a5a3a,roughness:.85}));bowCurve.position.set(0,handY+3.2,1);bowCurve.rotation.set(Math.PI/2,0,0);attachTo.add(bowCurve);
const bowString=new THREE.Mesh(new THREE.CylinderGeometry(.015,.015,2.4,4),new MS({color:0xdddddd,roughness:.9}));bowString.position.set(0,handY+3.2,1.85);bowString.rotation.x=Math.PI/2;attachTo.add(bowString);
const bowGrip=new THREE.Mesh(new THREE.CylinderGeometry(.1,.12,.8,6),new MS({color:0x5a3a2a,roughness:.9}));bowGrip.position.set(0,handY+2.5,.5);bowGrip.rotation.x=Math.PI/2;attachTo.add(bowGrip);
}
function addCrossbow(rArm){
// Crossbow - attaches to hand (elbow group) for natural rotation
const attachTo=rArm.userData&&rArm.userData.elbow?rArm.userData.elbow:rArm;
const handY=rArm.userData&&rArm.userData.elbow?-2.8:-6;
const stock=new THREE.Mesh(new THREE.BoxGeometry(.5,.4,3),new MS({color:0x5a3a2a,roughness:.85}));stock.position.set(0,handY+3.2,1);stock.rotation.x=Math.PI/2;attachTo.add(stock);
const prod=new THREE.Mesh(new THREE.CylinderGeometry(.06,.06,2.2,4),new MS({color:0x666666,roughness:.5}));prod.position.set(0,handY+3.2,2.2);prod.rotation.z=Math.PI/2;attachTo.add(prod);
const stringV=new THREE.Mesh(new THREE.CylinderGeometry(.015,.015,.8,4),new MS({color:0xdddddd,roughness:.9}));stringV.position.set(-.9,handY+3.2,2.2);stringV.rotation.x=Math.PI/2;attachTo.add(stringV);
const stringH=new THREE.Mesh(new THREE.CylinderGeometry(.015,.015,.8,4),new MS({color:0xdddddd,roughness:.9}));stringH.position.set(.9,handY+3.2,2.2);stringH.rotation.x=Math.PI/2;attachTo.add(stringH);
}
function addSwordLeft(lArm){
// Left hand sword (shorter for dual wielding) - attaches to hand
const attachTo=lArm.userData&&lArm.userData.elbow?lArm.userData.elbow:lArm;
const handY=lArm.userData&&lArm.userData.elbow?-2.8:-6.5;
const blade=new THREE.Mesh(new THREE.BoxGeometry(.18,.16,5.5),mt.swordBlade);blade.position.set(0,handY+2.8,2.8);blade.rotation.x=.06;attachTo.add(blade);
const fuller=new THREE.Mesh(new THREE.BoxGeometry(.05,.08,4),new MS({color:0x556,roughness:.15,metalness:.9}));fuller.position.set(0,handY+2.9,2.8);fuller.rotation.x=.06;attachTo.add(fuller);
const xguard=new THREE.Mesh(new THREE.BoxGeometry(1.2,.2,.2),mt.swordHilt);xguard.position.set(0,handY,.1);attachTo.add(xguard);
const hilt=new THREE.Mesh(new THREE.CylinderGeometry(.12,.12,1.2,6),mt.leather);hilt.position.set(0,handY,-.3);hilt.rotation.x=Math.PI/2;attachTo.add(hilt);
const pommel=new THREE.Mesh(new THREE.SphereGeometry(.18,6,6),mt.gold);pommel.position.set(0,handY,-.9);attachTo.add(pommel);
// FIX: Reposition left sword to properly extend from hand
blade.position.set(0,handY-2.5,0.3);blade.rotation.set(Math.PI/2,0,0);
fuller.position.set(0,handY-2.5,0.35);fuller.rotation.set(Math.PI/2,0,0);
xguard.position.set(0,handY,0.3);
hilt.position.set(0,handY+0.2,0.3);hilt.rotation.set(Math.PI/2,0,0);
pommel.position.set(0,handY+0.8,0.3);
}
function addDaggerLeft(lArm){
// Left hand dagger for dual wield - attaches to hand
const attachTo=lArm.userData&&lArm.userData.elbow?lArm.userData.elbow:lArm;
const handY=lArm.userData&&lArm.userData.elbow?-2.8:-6.8;
const blade=new THREE.Mesh(new THREE.ConeGeometry(.12,.8,4),mt.swordBlade);blade.position.set(0,handY,.4);blade.rotation.x=-Math.PI/2;attachTo.add(blade);
const guard=new THREE.Mesh(new THREE.CylinderGeometry(.3,.3,.1,6),mt.swordHilt);guard.position.set(0,handY,-.1);attachTo.add(guard);
const hilt=new THREE.Mesh(new THREE.CylinderGeometry(.1,.1,.6,6),mt.leather);hilt.position.set(0,handY,-.45);hilt.rotation.x=Math.PI/2;attachTo.add(hilt);
const pommel=new THREE.Mesh(new THREE.SphereGeometry(.15,6,6),mt.gold);pommel.position.set(0,handY,-.8);attachTo.add(pommel);
}
function addQuiver(back){
// Quiver with arrows on back
const quiver=new THREE.Mesh(new THREE.CylinderGeometry(.25,.3,1.8,6),new MS({color:0x5a3a2a,roughness:.9}));quiver.position.set(0,-1,-.8);quiver.rotation.x=-.3;back.add(quiver);
// Arrow fletchings visible
for(let i=0;i<4;i++){const fletch=new THREE.Mesh(new THREE.BoxGeometry(.15,.02,.25),new MS({color:0xaa2222,roughness:.8}));fletch.position.set((Math.random()-.5)*.3,.6+i*.15,-.8);fletch.rotation.x=-.3;back.add(fletch);}
}
function addPauldrons_Knight(lArm,rArm){
[lArm,rArm].forEach(arm=>{
// Pauldron (shoulder armor) - attaches to shoulder, moves with upper arm
const paul=new THREE.Mesh(new THREE.SphereGeometry(1.3,10,8),mt.armorLt);paul.scale.set(1.1,.8,.95);arm.add(paul);
const paulRim=new THREE.Mesh(new THREE.BoxGeometry(1.8,.2,1.6),mt.armorDk);paulRim.position.y=-.5;arm.add(paulRim);
// Upper arm armor (rerebrace) - covers upper arm only
const ua=new THREE.Mesh(new THREE.CylinderGeometry(.55,.5,2.6,8),mt.armorWorn);ua.position.y=-1.4;arm.add(ua);
// Elbow couter - attaches to elbow pivot
if(arm.userData.elbow){
const el=new THREE.Mesh(new THREE.SphereGeometry(.55,8,6),mt.armorDk);arm.userData.elbow.add(el);
// Lower arm armor (vambrace) - attaches to forearm
const fa=new THREE.Mesh(new THREE.CylinderGeometry(.5,.44,2.4,8),mt.armorDk);fa.position.y=-1.2;arm.userData.elbow.add(fa);
// Gauntlet (hand armor)
const gt=new THREE.Mesh(new THREE.BoxGeometry(.85,.5,1.1),mt.armorDk);gt.position.y=-2.8;arm.userData.elbow.add(gt);}
});}
function addGloves_Knight(lArm,rArm){
[lArm,rArm].forEach(arm=>{
// Gauntlets attach to elbow group (hand level)
if(arm.userData.elbow){
const gt=new THREE.Mesh(new THREE.BoxGeometry(.85,.6,1.1),mt.armorDk);gt.position.y=-2.8;arm.userData.elbow.add(gt);
const knk=new THREE.Mesh(new THREE.BoxGeometry(.85,.15,.5),mt.armorLt);knk.position.set(0,0,.3);arm.userData.elbow.add(knk);}
});}
function addCape(bodyCenter,mat){
mat=mat||mt.cape;
// Cape attaches to body center so it moves with breathing animation
for(let i=0;i<5;i++){const cw=3-i*.25,ch=1.8+i*.2;const cMat=i>2?mt.capeTattered:mat;const seg=new THREE.Mesh(new THREE.PlaneGeometry(cw,ch,2,3),cMat);seg.position.set(0,1.5-i*1.7,-1.15-i*.12);bodyCenter.add(seg)}
const clasp=new THREE.Mesh(new THREE.SphereGeometry(.15,5,5),mt.gold);clasp.position.set(0,2.5,-1.1);bodyCenter.add(clasp);
}

function buildPlayerModel(cls){
const g=new THREE.Group();const body=new THREE.Group();
const{lArm,rArm,lLeg,rLeg,bodyCenter,headGroup}=buildBaseBody(body);
const lKnee=lLeg.userData.knee,rKnee=rLeg.userData.knee;
const eq=typeof equipped!=='undefined'?equipped:null;
const hasHelm=eq&&eq.Helm&&eq.Helm.name!=='None';
const hasChest=eq&&eq.Chest&&eq.Chest.name!=='None';
const hasLegs=eq&&eq.Legs&&eq.Legs.name!=='None';
const hasBoots=eq&&eq.Boots&&eq.Boots.name!=='None';
const hasGloves=eq&&eq.Gloves&&eq.Gloves.name!=='None';
const hasWeapon=eq&&eq.Weapon&&eq.Weapon.name!=='None';
const hasShield=eq&&eq.Shield&&eq.Shield.name!=='None';
const hasOffHand=eq&&eq.OffHand&&eq.OffHand.name!=='None';
const hasCape=eq&&eq.Cape&&eq.Cape.name!=='None';
// Determine weapon types for dual wield logic
const weaponName=hasWeapon?eq.Weapon.name.toLowerCase():'';
const offHandName=hasOffHand?eq.OffHand.name.toLowerCase():'';
const isCrossbow=weaponName.includes('crossbow')||weaponName.includes('xbow');
const isLongBow=weaponName.includes('longbow')||weaponName.includes('shortbow');
const isBow=weaponName.includes('bow')&&!isCrossbow;
const isSword=weaponName.includes('sword')||weaponName.includes('blade')||weaponName.includes('scimitar')||weaponName.includes('dagger');
const offIsSword=offHandName.includes('sword')||offHandName.includes('blade')||offHandName.includes('scimitar')||offHandName.includes('dagger');
const offIsCrossbow=offHandName.includes('crossbow')||offHandName.includes('xbow');
// Dual wield rules: can dual wield swords OR crossbows, but NOT long/short bows
const canDualWield=!isLongBow;// Crossbows and swords can dual wield
const isDualWielding=hasOffHand&&canDualWield&&(!isBow||isCrossbow);
if(cls==='knight'){
// Knight: DEPRIVED when no gear equipped, only shows what IS equipped
// Hair only shows when NO helm equipped
if(!hasHelm){
const hair=new THREE.Mesh(new THREE.SphereGeometry(1.3,8,8),mt_hairDk);hair.position.y=.4;hair.scale.set(1.05,.5,1.05);headGroup.add(hair);}
// Armor ONLY if equipped in that slot
if(hasHelm)addHelm_Knight(headGroup);
if(hasChest)addChest_Knight(bodyCenter);
if(hasChest)addPauldrons_Knight(lArm,rArm); // Pauldrons are part of chest armor
if(hasLegs)addLegs_Knight(lLeg,rLeg,bodyCenter);
if(hasBoots)addBoots_Knight(lKnee,rKnee);
if(hasGloves)addGloves_Knight(lArm,rArm);
// Cape ONLY if equipped
if(hasCape)addCape(bodyCenter);
// Right hand weapon ONLY if equipped
if(hasWeapon){
if(isCrossbow)addCrossbow(rArm);
else if(isBow)addBow(rArm);
else addSword(rArm);}
// Left hand: shield OR off-hand weapon ONLY if equipped
if(hasShield&&!isDualWielding)addShield(lArm);
else if(isDualWielding&&hasOffHand){
if(offIsCrossbow)addCrossbow(lArm);
else if(offHandName.includes('dagger'))addDaggerLeft(lArm);
else addSwordLeft(lArm);}
}else if(cls==='warrior'){
// Warrior: DEPRIVED when no gear equipped, only shows what IS equipped
// Hair only shows when NO helm equipped
if(!hasHelm){
const hair=new THREE.Mesh(new THREE.SphereGeometry(1.35,8,8),mt_hairDk);hair.position.y=.4;hair.scale.set(1.05,.55,1.05);headGroup.add(hair);}
// Helm ONLY if equipped
if(hasHelm){
const wHelm=new THREE.Mesh(new THREE.SphereGeometry(1.45,10,10),mt.armorWorn);wHelm.position.y=.1;wHelm.scale.set(1.02,1.08,.92);headGroup.add(wHelm);
const noseguard=new THREE.Mesh(new THREE.BoxGeometry(.18,1.6,.25),mt.armorLt);noseguard.position.set(0,-.25,.32);headGroup.add(noseguard);
}
// Chainmail chest - ONLY if equipped
if(hasChest){
const chainTorso=new THREE.Mesh(new THREE.BoxGeometry(3.5,4.2,2.1),mt_warChain);chainTorso.position.y=.6;bodyCenter.add(chainTorso);
const belt=new THREE.Mesh(new THREE.BoxGeometry(3.7,.55,2.2),mt.leather);belt.position.y=-1.3;bodyCenter.add(belt);
const buckle=new THREE.Mesh(new THREE.BoxGeometry(.65,.45,.3),mt.gold);buckle.position.set(0,-1.3,1.15);bodyCenter.add(buckle);
}
// Pauldrons (shoulders) - ONLY if hasChest (part of chest set)
if(hasChest){
[lArm,rArm].forEach(arm=>{
const paul=new THREE.Mesh(new THREE.SphereGeometry(1.05,8,6),mt_warLeather);paul.scale.set(1.05,.75,.92);arm.add(paul);});
}
// Upper arm + elbow + forearm + gloves - ONLY if hasGloves
if(hasGloves){
[lArm,rArm].forEach(arm=>{
const ua=new THREE.Mesh(new THREE.CylinderGeometry(.52,.48,2.6,8),mt_warLeather);ua.position.y=-1.4;arm.add(ua);
if(arm.userData.elbow){
const elb=new THREE.Mesh(new THREE.SphereGeometry(.52,8,6),mt_warLeather);arm.userData.elbow.add(elb);
const fa=new THREE.Mesh(new THREE.CylinderGeometry(.48,.42,2.4,8),mt_warChain);fa.position.y=-1.2;arm.userData.elbow.add(fa);
const glv=new THREE.Mesh(new THREE.BoxGeometry(.75,.55,.9),mt_warLeather);glv.position.y=-2.8;arm.userData.elbow.add(glv);}
});
}
// Warrior legs - ONLY if hasLegs
if(hasLegs){
const addWarriorLeg=(leg)=>{
const cuisse=new THREE.Mesh(new THREE.CylinderGeometry(.58,.52,3.1,8),mt_warChain);cuisse.position.y=-1.5;leg.add(cuisse);
const poleyn=new THREE.Mesh(new THREE.SphereGeometry(.55,8,6),mt_warLeather);poleyn.position.y=-3;leg.add(poleyn);
const shin=new THREE.Mesh(new THREE.CylinderGeometry(.5,.42,2.9,8),mt_warLeather);shin.position.y=-1.45;leg.userData.knee.add(shin);
};
addWarriorLeg(lLeg);addWarriorLeg(rLeg);
}
// Boots - ONLY if hasBoots
if(hasBoots){
const addWarriorBoot=(knee)=>{
const boot=new THREE.Mesh(new THREE.BoxGeometry(.95,.75,1.6),mt_warLeather);boot.position.set(0,-.4,.1);knee.add(boot);
const toe=new THREE.Mesh(new THREE.BoxGeometry(.75,.3,.6),mt_warLeather);toe.position.set(0,-.55,.75);knee.add(toe);
};
addWarriorBoot(lKnee);addWarriorBoot(rKnee);
}
// Right hand weapon ONLY if equipped
if(hasWeapon){
if(isCrossbow)addCrossbow(rArm);
else if(isBow)addBow(rArm);
else addSword(rArm);}
// Left hand: shield OR off-hand weapon ONLY if equipped
if(hasShield&&!isDualWielding)addShield(lArm);
else if(isDualWielding&&hasOffHand){
if(offIsCrossbow)addCrossbow(lArm);
else if(offHandName.includes('dagger'))addDaggerLeft(lArm);
else addSwordLeft(lArm);}
}else if(cls==='sorcerer'){
// Sorcerer: DEPRIVED when no gear, shows robes/hood only when equipped
// Hood ONLY if hasHelm (hood counts as head armor)
if(hasHelm){
const hood=new THREE.Mesh(new THREE.SphereGeometry(1.65,10,10),mt_robeHood);hood.position.y=.1;hood.scale.set(1.02,1.18,.97);headGroup.add(hood);
const faceShadow=new THREE.Mesh(new THREE.SphereGeometry(1,8,8),new MS({color:0x0a0a0a,roughness:1}));faceShadow.position.set(0,-.45,.05);faceShadow.scale.set(.6,.5,.3);headGroup.add(faceShadow);
const glowEye=new MS({color:0x6644ff,emissive:0x6644ff,emissiveIntensity:2});
[-1,1].forEach(s=>{const eye=new THREE.Mesh(new THREE.SphereGeometry(.12,5,5),glowEye);eye.position.set(s*.35,-.35,.15);headGroup.add(eye)});
}
// Robes ONLY if hasChest (robes count as chest armor)
if(hasChest){
// Robe torso
const robeTorso=new THREE.Mesh(new THREE.BoxGeometry(3.5,4.6,2.1),mt_robe);robeTorso.position.y=.4;bodyCenter.add(robeTorso);
const trim1=new THREE.Mesh(new THREE.BoxGeometry(3.55,.18,2.12),mt_robeGold);trim1.position.y=2.6;bodyCenter.add(trim1);
const trim2=new THREE.Mesh(new THREE.BoxGeometry(.22,4.6,.18),mt_robeGold);trim2.position.set(0,.4,1.08);bodyCenter.add(trim2);
// Segmented robe skirt
const robeSkirtSegs=[];
const skirtTop=new THREE.Mesh(new THREE.CylinderGeometry(1.15,1.5,1.8,10),mt_robe);skirtTop.position.y=-2.2;bodyCenter.add(skirtTop);
const skirtTopTrim=new THREE.Mesh(new THREE.TorusGeometry(1.5,.06,6,12),mt_robeGold);skirtTopTrim.position.y=-3.1;skirtTopTrim.rotation.x=Math.PI/2;bodyCenter.add(skirtTopTrim);
const skirtMid=new THREE.Mesh(new THREE.CylinderGeometry(1.5,2,1.8,10),mt_robe);skirtMid.position.y=-4.0;bodyCenter.add(skirtMid);
const skirtMidTrim=new THREE.Mesh(new THREE.TorusGeometry(2,.07,6,14),mt_robeGold);skirtMidTrim.position.y=-4.9;skirtMidTrim.rotation.x=Math.PI/2;bodyCenter.add(skirtMidTrim);
const skirtBot=new THREE.Mesh(new THREE.CylinderGeometry(2,2.6,1.8,10),mt_robe);skirtBot.position.y=-5.8;bodyCenter.add(skirtBot);
const skirtBotTrim=new THREE.Mesh(new THREE.TorusGeometry(2.6,.08,6,16),mt_robeGold);skirtBotTrim.position.y=-6.7;skirtBotTrim.rotation.x=Math.PI/2;bodyCenter.add(skirtBotTrim);
robeSkirtSegs.push({mesh:skirtMid,swayAmt:.03},{mesh:skirtBot,swayAmt:.06});
bodyCenter.userData.robeSkirtSegs=robeSkirtSegs;bodyCenter.userData.robeSkirt=skirtBot;
bodyCenter.userData.robeTorso=robeTorso;
// Sash/belt
const sash=new THREE.Mesh(new THREE.BoxGeometry(3.65,.45,2.15),mt_robeGold);sash.position.y=-1.6;bodyCenter.add(sash);
}
// Robe sleeves - ONLY if hasGloves (sleeve armor)
if(hasGloves){
const robeSleeves=[];
[lArm,rArm].forEach((arm,side)=>{
const upSleeve=new THREE.Mesh(new THREE.CylinderGeometry(.72,.65,2.6,8),mt_robe);upSleeve.position.y=-1.4;arm.add(upSleeve);
const upTrim=new THREE.Mesh(new THREE.TorusGeometry(.68,.06,6,10),mt_robeGold);upTrim.position.y=-2.7;upTrim.rotation.x=Math.PI/2;arm.add(upTrim);
if(arm.userData.elbow){
const loSleeve=new THREE.Mesh(new THREE.CylinderGeometry(.82,.9,2.4,8),mt_robe);loSleeve.position.y=-1.2;arm.userData.elbow.add(loSleeve);
const cuff=new THREE.Mesh(new THREE.TorusGeometry(.88,.07,6,10),mt_robeGold);cuff.position.y=-2.4;cuff.rotation.x=Math.PI/2;arm.userData.elbow.add(cuff);
const sleeveEnd=new THREE.Mesh(new THREE.CylinderGeometry(.9,1.2,.8,8),mt_robe);sleeveEnd.position.y=-2.8;arm.userData.elbow.add(sleeveEnd);
robeSleeves.push(upSleeve,loSleeve,sleeveEnd);}
});
bodyCenter.userData.robeSleeves=robeSleeves;
}
// Staff ONLY if weapon equipped
if(hasWeapon)addStaff(rArm);
// Left hand: off-hand weapon ONLY if equipped (no default book)
if(isDualWielding&&hasOffHand){
if(offIsCrossbow)addCrossbow(lArm);
else if(offHandName.includes('dagger'))addDaggerLeft(lArm);
else addSwordLeft(lArm);}
}else if(cls==='ranger'){
// Ranger: DEPRIVED when no gear, shows gear only when equipped
// Hood ONLY if hasHelm equipped
if(hasHelm){
const hood=new THREE.Mesh(new THREE.SphereGeometry(1.4,10,10),mt_robeHood);hood.position.y=.1;hood.scale.set(1.02,1.1,.97);headGroup.add(hood);}
// Leather tunic - ONLY if hasChest
if(hasChest){
const tunic=new THREE.Mesh(new THREE.BoxGeometry(3.2,4,1.8),mt_warLeather);tunic.position.y=.6;bodyCenter.add(tunic);
const belt=new THREE.Mesh(new THREE.BoxGeometry(3.4,.4,1.9),new MS({color:0x3a2a1a,roughness:.9}));belt.position.y=-1.4;bodyCenter.add(belt);
}
// Leather shoulders - ONLY if hasChest
if(hasChest){
[lArm,rArm].forEach(arm=>{
const vam=new THREE.Mesh(new THREE.SphereGeometry(1.0,8,6),mt_warLeather);vam.scale.set(1.05,.75,.92);arm.add(vam);});
}
// Vambraces and gloves - ONLY if hasGloves
if(hasGloves){
[lArm,rArm].forEach(arm=>{
const ua=new THREE.Mesh(new THREE.CylinderGeometry(.45,.42,2.6,8),mt_warLeather);ua.position.y=-1.4;arm.add(ua);
if(arm.userData.elbow){
const glv=new THREE.Mesh(new THREE.BoxGeometry(.7,.5,.85),mt_warLeather);glv.position.y=-2.8;arm.userData.elbow.add(glv);}
});
}
// Ranger legs - ONLY if hasLegs
if(hasLegs){
const addRangerLeg=(leg)=>{
const cuisse=new THREE.Mesh(new THREE.CylinderGeometry(.55,.5,3.1,8),mt_warLeather);cuisse.position.y=-1.5;leg.add(cuisse);
const poleyn=new THREE.Mesh(new THREE.SphereGeometry(.52,8,6),mt_warLeather);poleyn.position.y=-3;leg.add(poleyn);
const shin=new THREE.Mesh(new THREE.CylinderGeometry(.48,.42,2.9,8),mt_warLeather);shin.position.y=-1.45;leg.userData.knee.add(shin);
};
addRangerLeg(lLeg);addRangerLeg(rLeg);
}
// Boots - ONLY if hasBoots
if(hasBoots){
const addRangerBoot=(knee)=>{
const boot=new THREE.Mesh(new THREE.BoxGeometry(.9,.7,1.5),mt_warLeather);boot.position.set(0,-.4,.1);knee.add(boot);
const toe=new THREE.Mesh(new THREE.BoxGeometry(.7,.28,.55),mt_warLeather);toe.position.set(0,-.52,.72);knee.add(toe);
};
addRangerBoot(lKnee);addRangerBoot(rKnee);
}
// Bow/crossbow - ONLY if weapon equipped (no default)
if(hasWeapon){
if(isCrossbow)addCrossbow(rArm);
else if(isBow)addBow(rArm);
else addSword(rArm);}
// Quiver ONLY if hasBow equipped
if(hasWeapon&&isBow)addQuiver(bodyCenter);
// Left hand: shield OR off-hand weapon ONLY if equipped
if(hasShield&&!isDualWielding)addShield(lArm);
else if(isDualWielding&&hasOffHand){
if(offIsCrossbow)addCrossbow(lArm);
else if(offHandName.includes('dagger'))addDaggerLeft(lArm);
else addSwordLeft(lArm);}
}else if(cls==='deprived'){
// Deprived: bare skin, loincloth only
// Hair (messy) - attaches to headGroup
const hair=new THREE.Mesh(new THREE.SphereGeometry(1.3,8,8),mt_hairDk);hair.position.y=.45;hair.scale.set(1.08,.52,1.08);headGroup.add(hair);
// Loincloth - attaches to bodyCenter
const loin=new THREE.Mesh(new THREE.BoxGeometry(2.6,1.3,1.9),mt_cloth);loin.position.y=-2.1;bodyCenter.add(loin);
// Simple wrap on arms - attach to animated arms
[lArm,rArm].forEach(arm=>{
const wrap=new THREE.Mesh(new THREE.CylinderGeometry(.36,.32,1.3,6),mt_cloth);wrap.position.y=-5.4;arm.add(wrap);
});
// Right hand weapon
if(hasWeapon){
if(isCrossbow)addCrossbow(rArm);
else if(isBow)addBow(rArm);
else addSword(rArm);}
// Left hand: shield OR off-hand weapon for dual wield
if(hasShield&&!isDualWielding)addShield(lArm);
else if(isDualWielding){
if(offIsCrossbow)addCrossbow(lArm);
else if(offHandName.includes('dagger'))addDaggerLeft(lArm);
else addSwordLeft(lArm);}
// Bare feet by default
// If gear is equipped, add it visually to animated groups
if(hasHelm){const headband=new THREE.Mesh(new THREE.TorusGeometry(1.32,.12,6,12),mt_cloth);headband.position.y=-.05;headband.rotation.x=Math.PI/2;headGroup.add(headband);}
if(hasChest){const vest=new THREE.Mesh(new THREE.BoxGeometry(3.4,3.6,2),mt_warLeather);vest.position.y=.7;vest.material=vest.material.clone();vest.material.transparent=true;vest.material.opacity=.8;bodyCenter.add(vest);}
}
body.traverse(c=>{if(c.isMesh)c.castShadow=true});
g.add(body);
// Store all animation references in userData
g.userData.body=body;
g.userData.lArm=lArm;g.userData.rArm=rArm;
g.userData.lLeg=lLeg;g.userData.rLeg=rLeg;
g.userData.bodyCenter=bodyCenter;
g.userData.headGroup=headGroup;
g.userData.lKnee=lLeg.userData.knee;
g.userData.rKnee=rLeg.userData.knee;
// Animation state
g.userData.animState='idle';
g.userData.animTime=0;
g.scale.setScalar(.55);
return g;
}

// Keep buildKnight for multiplayer other-player models
function buildKnight(){return buildPlayerModel('knight')}

// === COMPREHENSIVE CHARACTER ANIMATION SYSTEM ===
// Unified animation for Player, Enemies, and NPCs

// Animation state types: 'idle', 'walk', 'run', 'attack', 'block', 'hit', 'die', 'jump', 'fall'

function animateCharacter(mesh,dt){
if(!mesh||!mesh.userData)return;
const d=mesh.userData;
if(!d.bodyCenter)return; // Not a character with animation rig

// Update animation time
d.animTime=(d.animTime||0)+dt;
const t=d.animTime;

// Get speed for movement state detection
const isPlayer=mesh===playerGroup;
const speed=isPlayer?Math.hypot(player.vx||0,player.vz||0):0;
const isMoving=speed>0.02; // Lower threshold for more responsive walking
const isRunning=isPlayer?(player.isSprinting||false):(isMoving&&speed>0.15);
const onGround=isPlayer?player.grounded:true;
// Animation speed multiplier based on actual movement speed
// For enemies, use their stored animSpeed; for player, use sprint multiplier
const animSpeed=isPlayer?(player.isSprinting?1.8:1.0):(d.animSpeed||1.0);

// Determine animation state
let state=d.animState||'idle';
if(isPlayer){
if(player.dead)state='die';
else if(player.rolling)state='roll';
else if(!onGround)state='jump';
else if(player.atkCD>0)state='attack';
else if(d.animState==='parry')state='parry';// Parry animation takes priority
else if(player.blocking)state='block';
else if(isRunning)state='run';
else if(isMoving)state='walk';
else state='idle';
}

// Reset to neutral pose first (smoothly)
const resetSpd=0.15;
d.lArm.rotation.x*=(1-resetSpd);d.lArm.rotation.z*=(1-resetSpd);
d.rArm.rotation.x*=(1-resetSpd);d.rArm.rotation.z*=(1-resetSpd);
d.lLeg.rotation.x*=(1-resetSpd);
d.rLeg.rotation.x*=(1-resetSpd);
d.lKnee.rotation.x*=(1-resetSpd);
d.rKnee.rotation.x*=(1-resetSpd);
d.bodyCenter.position.y=5+(d.bodyCenter.position.y-5)*(1-resetSpd);
d.bodyCenter.rotation.x*=(1-resetSpd);

// Apply state-specific animations
switch(state){
case 'idle':{
// Breathing - subtle chest movement
const breath=Math.sin(t*2)*0.03;
d.bodyCenter.position.y=5+breath;
d.bodyCenter.rotation.x=breath*0.5;
// Slight arm sway
const sway=Math.sin(t*1.5)*0.05;
d.lArm.rotation.z=0.1+sway;
d.rArm.rotation.z=-0.1-sway;
// Head bob with breath
if(d.headGroup)d.headGroup.rotation.x=breath*0.3;
// Robe/skirt sway for sorcerer
if(d.bodyCenter.userData.robeSkirt){
const skirt=d.bodyCenter.userData.robeSkirt;
skirt.rotation.x=breath*0.3;
skirt.rotation.z=Math.sin(t*1.2)*0.02;}
if(d.bodyCenter.userData.robeTorso){
d.bodyCenter.userData.robeTorso.rotation.x=breath*0.2;}
break;}
case 'walk':{
const walkCycle=t*8*animSpeed; // Speed-matched animation
const legAmp=0.6;
const armAmp=0.4;
// Legs - opposite phases with speed-adjusted amplitude
const walkFactor=Math.min(1,speed/0.15); // Scale animation intensity by actual speed
d.lLeg.rotation.x=Math.sin(walkCycle)*legAmp*walkFactor;
d.rLeg.rotation.x=Math.sin(walkCycle+Math.PI)*legAmp*walkFactor;
// Knee bend during stride - more bend at higher speeds
d.lKnee.rotation.x=Math.max(0,Math.sin(walkCycle-0.5)*0.8*walkFactor);
d.rKnee.rotation.x=Math.max(0,Math.sin(walkCycle+Math.PI-0.5)*0.8*walkFactor);
// Arms - opposite to legs
const lArmRot=Math.sin(walkCycle+Math.PI)*armAmp*walkFactor;
const rArmRot=Math.sin(walkCycle)*armAmp*walkFactor;
d.lArm.rotation.x=lArmRot;
d.rArm.rotation.x=rArmRot;
// Elbow bend - arms flex at elbow when swinging
if(d.lArm.userData&&d.lArm.userData.elbow)d.lArm.userData.elbow.rotation.x=Math.abs(lArmRot)*0.5;
if(d.rArm.userData&&d.rArm.userData.elbow)d.rArm.userData.elbow.rotation.x=Math.abs(rArmRot)*0.5;
// Body bounce proportional to speed
const bounce=Math.abs(Math.sin(walkCycle))*0.15*walkFactor;
d.bodyCenter.position.y=5+bounce;
d.bodyCenter.rotation.x=bounce*0.3;
// Robe/skirt sway with leg movement - segmented skirt animation
if(d.bodyCenter.userData.robeSkirt){
d.bodyCenter.userData.robeSkirt.rotation.x=bounce*0.5+Math.sin(walkCycle)*0.05;
d.bodyCenter.userData.robeSkirt.rotation.z=Math.sin(walkCycle*0.5)*0.03;}
if(d.bodyCenter.userData.robeSkirtSegs){
d.bodyCenter.userData.robeSkirtSegs.forEach((seg,si)=>{
if(seg&&seg.mesh)seg.mesh.rotation.z=Math.sin(walkCycle*0.5+si*0.5)*seg.swayAmt;});}
if(d.bodyCenter.userData.robeSleeves){
d.bodyCenter.userData.robeSleeves.forEach((sleeve,si)=>{
if(sleeve)sleeve.rotation.x=Math.sin(walkCycle+si*Math.PI)*0.1*walkFactor;});}
break;}
case 'run':{
const runCycle=t*12*animSpeed; // Speed-matched animation
const legAmp=0.9;
const armAmp=0.7;
// Faster, more extreme leg movement
d.lLeg.rotation.x=Math.sin(runCycle)*legAmp;
d.rLeg.rotation.x=Math.sin(runCycle+Math.PI)*legAmp;
// More knee bend
d.lKnee.rotation.x=Math.max(0,Math.sin(runCycle-0.3)*1.2);
d.rKnee.rotation.x=Math.max(0,Math.sin(runCycle+Math.PI-0.3)*1.2);
// Arms pumping
const lRunArm=Math.sin(runCycle+Math.PI)*armAmp;
const rRunArm=Math.sin(runCycle)*armAmp;
d.lArm.rotation.x=lRunArm;
d.rArm.rotation.x=rRunArm;
d.lArm.rotation.z=0.2;
d.rArm.rotation.z=-0.2;
// Elbow bend more when running
if(d.lArm.userData&&d.lArm.userData.elbow)d.lArm.userData.elbow.rotation.x=0.3+Math.abs(lRunArm)*0.4;
if(d.rArm.userData&&d.rArm.userData.elbow)d.rArm.userData.elbow.rotation.x=0.3+Math.abs(rRunArm)*0.4;
// Body lean forward
const lean=0.3;
d.bodyCenter.rotation.x=lean;
d.bodyCenter.position.y=5+Math.sin(runCycle*2)*0.1;
// Robe/skirt flows back when running - segmented animation
if(d.bodyCenter.userData.robeSkirt){
d.bodyCenter.userData.robeSkirt.rotation.x=lean*0.8+Math.sin(runCycle)*0.1;
d.bodyCenter.userData.robeSkirt.rotation.z=Math.sin(runCycle*0.7)*0.05;}
if(d.bodyCenter.userData.robeSkirtSegs){
d.bodyCenter.userData.robeSkirtSegs.forEach((seg,si)=>{
if(seg&&seg.mesh){seg.mesh.rotation.x=lean*(0.2+si*0.15);
seg.mesh.rotation.z=Math.sin(runCycle*0.7+si*0.3)*seg.swayAmt*1.5;}});}
if(d.bodyCenter.userData.robeSleeves){
d.bodyCenter.userData.robeSleeves.forEach((sleeve,si)=>{
if(sleeve)sleeve.rotation.x=Math.sin(runCycle+si*Math.PI)*0.15;});}
break;}
case 'attack':{
// Attack handled separately per-weapon, this is generic
const attackT=isPlayer?player.atkCD/14:1; // Normalized 1->0
if(attackT>0.5){
// Wind up
const wind=(attackT-0.5)*2;
d.rArm.rotation.x=-1.5*wind;
d.rArm.rotation.z=-0.3*wind;
d.bodyCenter.rotation.x=-0.2*wind;
}else{
// Swing through
const swing=(0.5-attackT)*2;
d.rArm.rotation.x=1.2*Math.sin(swing*Math.PI);
d.rArm.rotation.z=-0.3*(1-swing);
}
break;}
case 'parry':{
// Quick parry motion - shield flicks outward then settles into block
const parryT=Math.max(0,1-(d._parryAnimT||0)/10);
d._parryAnimT=(d._parryAnimT||0)+1;
// Sharp outward flick
d.lArm.rotation.x=-1.4+Math.sin(parryT*Math.PI)*0.4;
d.lArm.rotation.z=0.9-Math.sin(parryT*Math.PI)*0.3;
// Body leans into parry
d.bodyCenter.position.y=4.3+Math.sin(parryT*Math.PI)*0.3;
d.bodyCenter.rotation.x=0.25-Math.sin(parryT*Math.PI)*0.1;
// Right arm tucked back
d.rArm.rotation.x=0.1;
d.rArm.rotation.z=-0.3;
if(parryT<=0.1)d.animState='block';// Transition to block stance
break;}
case 'block':{
// Shield raised, solid stance - left arm forward with shield
const blkSpd=0.25;
d.lArm.rotation.x+=(-1.2-d.lArm.rotation.x)*blkSpd;// Arm raised forward
if(d.lArm.userData&&d.lArm.userData.shield){d.lArm.rotation.z+=(0.8-d.lArm.rotation.z)*blkSpd}// Shield angled outward
else{d.lArm.rotation.z+=(0.4-d.lArm.rotation.z)*blkSpd}
d.lArm.position.x+=(-0.6-d.lArm.position.x)*blkSpd;// Slightly forward
// Right arm ready with weapon back
d.rArm.rotation.x+=(0.3-d.rArm.rotation.x)*blkSpd;
d.rArm.rotation.z+=(-0.2-d.rArm.rotation.z)*blkSpd;
// Solid crouch stance
d.bodyCenter.position.y+=(4.5-d.bodyCenter.position.y)*blkSpd;
d.bodyCenter.rotation.x+=(0.2-d.bodyCenter.rotation.x)*blkSpd;
// Legs braced
d.lLeg.rotation.x+=(0.1-d.lLeg.rotation.x)*blkSpd;
d.rLeg.rotation.x+=(0.1-d.rLeg.rotation.x)*blkSpd;
break;}
case 'hit':{
// Flinch reaction
d.bodyCenter.rotation.x=-0.4;
d.bodyCenter.position.y=4.5;
d.lArm.rotation.x=0.5;
d.rArm.rotation.x=0.5;
break;}
case 'jump':{
// Legs tucked
d.lLeg.rotation.x=-0.8;
d.rLeg.rotation.x=-0.8;
d.lKnee.rotation.x=1.2;
d.rKnee.rotation.x=1.2;
// Arms raised for balance
d.lArm.rotation.x=-2;
d.rArm.rotation.x=-2;
// Body upright
d.bodyCenter.rotation.x=-0.1;
break;}
case 'roll':{
// Rolling animation handled separately by rolling state
break;}
case 'die':{
// Collapse forward
d.bodyCenter.rotation.x=1.57; // 90 degrees
if(d.headGroup)d.headGroup.rotation.x=0.3;
break;}
}

// Store current state
d.animState=state;}

// Apply hit reaction to any character
function animateHit(mesh,duration=0.3){
if(!mesh||!mesh.userData)return;
mesh.userData.animState='hit';
mesh.userData.hitEnd=time+duration;}

// Apply death animation
function animateDeath(mesh){
if(!mesh||!mesh.userData)return;
mesh.userData.animState='die';}

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
// Initialize GPU instancers for building elements
initBuildingInstancers();
scene=new THREE.Scene();scene.background=new THREE.Color(0xaaccee);scene.fog=new THREE.FogExp2(0xaaccee,.00015);
cam=new THREE.PerspectiveCamera(62,innerWidth/innerHeight,1,8000);
renderer=new THREE.WebGLRenderer({antialias:false,powerPreference:'high-performance',stencil:false,depth:true});
renderer.setSize(innerWidth,innerHeight);renderer.setPixelRatio(1);
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.BasicShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=gameOpts?gameOpts.bright:2.0;
renderer.outputColorSpace=THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);

// Bright outdoor lighting
scene.add(new THREE.AmbientLight(0x8899aa,1.2));
const sun=new THREE.DirectionalLight(0xfff5e0,3.0);sun.position.set(200,350,-100);sun.castShadow=true;
sun.shadow.mapSize.set(1024,1024);sun.shadow.camera.near=10;sun.shadow.camera.far=800;
sun.shadow.camera.left=-250;sun.shadow.camera.right=250;sun.shadow.camera.top=250;sun.shadow.camera.bottom=-250;
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
const gGeo=new THREE.PlaneGeometry(80000,80000,250,250);
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
const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,3),mt.st);m.position.y=h/2;m.castShadow=true;g.add(m);
// Oriented wall collider: center at (x,z), half-extents (w/2, 1.5), height h, rotation rot
addWallSolid(x,z,w/2,1.5,h,rot||0,bY);
// Crenellations
const cN=Math.max(2,Math.floor(w/4));for(let i=0;i<cN;i++){if(i%2===0){const cr=new THREE.Mesh(new THREE.BoxGeometry(w/cN*.8,2,3.2),mt.stD);cr.position.set(-w/2+w/cN*(i+.5),h+1,0);cr.castShadow=true;g.add(cr)}}
// Arrow slits
const slitN=Math.max(1,Math.floor(w/8));for(let i=0;i<slitN;i++){const sl=new THREE.Mesh(new THREE.BoxGeometry(.4,2,.2),new MS({color:0x0a0a0a,roughness:1}));sl.position.set(-w/2+w/(slitN+1)*(i+1),h*.6,1.6);g.add(sl)}
// Base molding
const base=new THREE.Mesh(new THREE.BoxGeometry(w+1,1,3.8),mt.stD);base.position.y=.5;g.add(base);
g.position.set(x,bY,z);g.rotation.y=rot||0;scene.add(g)}
function wallW(x,z,w,h,rot){const bY=meshTerrainH(x,z);const g=new THREE.Group();
const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,3),mt.stW);m.position.y=h/2;m.castShadow=true;g.add(m);
// Oriented wall collider: center at (x,z), half-extents (w/2, 1.5), height h, rotation rot
addWallSolid(x,z,w/2,1.5,h,rot||0,bY);
const cN=Math.max(2,Math.floor(w/4));for(let i=0;i<cN;i++){if(i%2===0){const cr=new THREE.Mesh(new THREE.BoxGeometry(w/cN*.8,2,3.2),mt.stW);cr.position.set(-w/2+w/cN*(i+.5),h+1,0);cr.castShadow=true;g.add(cr)}}
const slitN=Math.max(1,Math.floor(w/8));for(let i=0;i<slitN;i++){const sl=new THREE.Mesh(new THREE.BoxGeometry(.4,2,.2),new MS({color:0x0a0a0a,roughness:1}));sl.position.set(-w/2+w/(slitN+1)*(i+1),h*.6,1.6);g.add(sl)}
const base=new THREE.Mesh(new THREE.BoxGeometry(w+1,1,3.8),mt.stD);base.position.y=.5;g.add(base);
g.position.set(x,bY,z);g.rotation.y=rot||0;scene.add(g)}
function hut(x,z,rot,s){s=(s||1)*4;const h=meshTerrainH(x,z);const g=new THREE.Group();
// RNG variation per hut
const hseed=Math.abs(Math.sin(x*73.7+z*157.3)*43758.5453)%1;
const wW=(10+hseed*8)*s,wD=(8+hseed*6)*s,wH=(7+hseed*5)*s,wallT=(.5+hseed*.3)*s;const doorW=(2.5+hseed)*s,doorH2=(4.5+hseed*2)*s;
const hutRoofStyle=Math.floor(hseed*3); // 0=pyramid,1=gable,2=flat
const doorMat=new MS({color:0x3a2818,roughness:.85,metalness:.05});
const intFloorMat=new MS({color:0x5a4a38,roughness:.92});
const winGlassMat=new MS({color:0x2a4a6a,roughness:.15,metalness:.3,emissive:0x1a3a5a,emissiveIntensity:.5,transparent:true,opacity:.5});
// Foundation
const found=new THREE.Mesh(new THREE.BoxGeometry(wW+2*s,1.5*s,wD+2*s),mt.st);found.position.y=.75*s;found.castShadow=true;g.add(found);
// Circle collider removed — entry handled by makeEnterable + enterBuilding system
// Interior floor
const intFloor=new THREE.Mesh(new THREE.BoxGeometry(wW-.5*s,.2*s,wD-.5*s),intFloorMat);intFloor.position.y=1.6*s;intFloor.receiveShadow=true;g.add(intFloor);
// Back wall (solid)
const backW=new THREE.Mesh(new THREE.BoxGeometry(wW,wH,wallT),mt.wd);backW.position.set(0,wH/2+1.5*s,-wD/2);backW.castShadow=true;g.add(backW);
// Left wall (solid)
const leftW=new THREE.Mesh(new THREE.BoxGeometry(wallT,wH,wD),mt.wd);leftW.position.set(-wW/2,wH/2+1.5*s,0);leftW.castShadow=true;g.add(leftW);
// Right wall (solid)
const rightW=leftW.clone();rightW.position.x=wW/2;g.add(rightW);
// Front wall — two sections flanking doorway
const fwSideW=(wW-doorW)/2;
const fwL=new THREE.Mesh(new THREE.BoxGeometry(fwSideW,wH,wallT),mt.wd);fwL.position.set(-(doorW+fwSideW)/2,wH/2+1.5*s,wD/2);fwL.castShadow=true;g.add(fwL);
const fwR=fwL.clone();fwR.position.x=(doorW+fwSideW)/2;g.add(fwR);
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
// Roof with overhang (variable style)
if(hutRoofStyle===0){// Pyramid
const roof=new THREE.Mesh(new THREE.ConeGeometry(Math.max(wW,wD)*.7,6*s,4),mt.rf);roof.position.y=wH+4*s;roof.rotation.y=.785;roof.castShadow=true;g.add(roof);
const ridge=new THREE.Mesh(new THREE.BoxGeometry(wW*1.1,.3*s,.3*s),mt.stD);ridge.position.y=wH+7*s;ridge.rotation.y=.785;g.add(ridge)}
else if(hutRoofStyle===1){// Gable (A-frame)
const roofL=new THREE.Mesh(new THREE.BoxGeometry(wW*1.15,wD*.6,.4*s),mt.rf);roofL.position.set(0,wH+wD*.22,wD*.15);roofL.rotation.x=-.45;roofL.castShadow=true;g.add(roofL);
const roofR=new THREE.Mesh(new THREE.BoxGeometry(wW*1.15,wD*.6,.4*s),mt.rf);roofR.position.set(0,wH+wD*.22,-wD*.15);roofR.rotation.x=.45;roofR.castShadow=true;g.add(roofR)}
else{// Flat with parapet
const flatRf=new THREE.Mesh(new THREE.BoxGeometry(wW+1*s,.5*s,wD+1*s),mt.rf);flatRf.position.y=wH+1.5*s;g.add(flatRf);
for(let pi=0;pi<8;pi++){const pa=pi/8;const px=-wW/2+pa*wW;
const mp=new THREE.Mesh(new THREE.BoxGeometry(1.2*s,1.5*s,1.2*s),mt.stD);mp.position.set(px,wH+2.5*s,wD/2);g.add(mp);
const mp2=mp.clone();mp2.position.z=-wD/2;g.add(mp2)}}
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
for(let i=0;i<4;i++){const step=new THREE.Mesh(new THREE.BoxGeometry(doorW+2*s,.4*s,1.4*s),mt.st);step.position.set(0,1.5*s-i*.4*s,wD/2+.6*s+i*1.4*s);step.receiveShadow=true;g.add(step)}
// Interior detail: table + chair
const tbl=new THREE.Mesh(new THREE.BoxGeometry(3*s,.15*s,2*s),mt.wd);tbl.position.set(0,3.5*s,-2*s);g.add(tbl);
const tblLeg1=new THREE.Mesh(new THREE.CylinderGeometry(.1*s,.1*s,2*s,4),mt.wd);
[[-1,-1],[-1,1],[1,-1],[1,1]].forEach(([lx,lz])=>{const lg=tblLeg1.clone();lg.position.set(lx*1.3*s,2.4*s,-2*s+lz*.8*s);g.add(lg)});
g.position.set(x,h,z);g.rotation.y=rot||0;scene.add(g)}
function tower(x,z,s,mat){s=(s||1)*2;mat=mat||mt.st;const h=meshTerrainH(x,z);const g=new THREE.Group();
// === RNG VARIATION per tower instance ===
const seed=Math.abs(Math.sin(x*127.1+z*311.7)*43758.5453)%1;
const bodyH=(24+seed*18)*s;  // height 24-42
const baseR=(7+seed*3)*s;    // radius 7-10
const topR=(5+seed*2.5)*s;
const nSides=8+Math.floor(seed*8);  // 8-15 sides
const roofStyle=Math.floor(seed*4);  // 0=cone,1=dome,2=flat+battlements,3=spire
const nWindows=2+Math.floor(seed*5); // 2-6
const nLevels=2+Math.floor(seed*3);  // 2-4 window levels
const hasBalcony=seed>.35;
const hasButtress=seed>.6;
const wallCol=new THREE.Color().setHSL(.07+seed*.05,.15+seed*.15,.35+seed*.15);
const tMat=new MS({color:wallCol,roughness:.8,metalness:.05});
const useMat=mat===mt.st?tMat:mat;
// Base (wider, variable)
const base=new THREE.Mesh(new THREE.CylinderGeometry(baseR*.9,baseR*1.1,4*s,nSides),useMat);base.position.y=2*s;base.castShadow=true;g.add(base);
// Main body
const b=new THREE.Mesh(new THREE.CylinderGeometry(topR,baseR,bodyH,nSides),useMat);b.position.y=bodyH/2+4*s;b.castShadow=true;g.add(b);
addCircleSolid(x,z,baseR*1.1,h,h+bodyH+8*s);
// Battlement ring
const nMerlons=nSides;
for(let i=0;i<nMerlons;i++){const a=i/nMerlons*Math.PI*2;const cr=new THREE.Mesh(new THREE.BoxGeometry(2.2*s,1.8*s+seed*1.2*s,1.4*s),mt.stD);cr.position.set(Math.cos(a)*topR*1.02,bodyH+5*s,Math.sin(a)*topR*1.02);cr.rotation.y=a;cr.castShadow=true;g.add(cr)}
// Roof based on roofStyle
const roofY=bodyH+6*s;
if(roofStyle===0){// Cone
const roof=new THREE.Mesh(new THREE.ConeGeometry(topR*1.3,(8+seed*8)*s,nSides),mt.rfSlate);roof.position.y=roofY+(4+seed*4)*s;roof.castShadow=true;g.add(roof);
const fin=new THREE.Mesh(new THREE.SphereGeometry(.5*s,5,5),mt.gold);fin.position.y=roofY+(12+seed*8)*s;g.add(fin)}
else if(roofStyle===1){// Dome
const dome=new THREE.Mesh(new THREE.SphereGeometry(topR*1.2,nSides,8,0,Math.PI*2,0,Math.PI/2),mt.rfSlate);dome.position.y=roofY;dome.castShadow=true;g.add(dome);
const fin=new THREE.Mesh(new THREE.CylinderGeometry(.2*s,.2*s,3*s,4),mt.gold);fin.position.y=roofY+topR*1.2+1.5*s;g.add(fin)}
else if(roofStyle===2){// Flat with extra battlements
const flatRf=new THREE.Mesh(new THREE.CylinderGeometry(topR*1.15,topR*1.15,.8*s,nSides),useMat);flatRf.position.y=roofY;g.add(flatRf);
for(let i=0;i<nMerlons;i++){const a=i/nMerlons*Math.PI*2;if(i%2===0){const cr2=new THREE.Mesh(new THREE.BoxGeometry(2*s,3*s,1.2*s),mt.stD);cr2.position.set(Math.cos(a)*topR*1.08,roofY+2*s,Math.sin(a)*topR*1.08);cr2.rotation.y=a;g.add(cr2)}}}
else{// Spire (tall narrow)
const spire=new THREE.Mesh(new THREE.ConeGeometry(topR*.6,(18+seed*14)*s,nSides),mt.rfSlate);spire.position.y=roofY+(9+seed*7)*s;spire.castShadow=true;g.add(spire);
const fin=new THREE.Mesh(new THREE.SphereGeometry(.4*s,4,4),mt.gold);fin.position.y=roofY+(27+seed*14)*s;g.add(fin)}
// Windows - variable count and levels
const winMat=new MS({color:0x101010,roughness:1});
for(let lv=0;lv<nLevels;lv++){for(let i=0;i<nWindows;i++){const a=i/nWindows*Math.PI*2+lv*.3;
const slit=new THREE.Mesh(new THREE.BoxGeometry(.4*s,(1.5+seed)*s,.15*s),winMat);
slit.position.set(Math.cos(a)*(topR+.5*s),6*s+lv*(bodyH/nLevels),Math.sin(a)*(topR+.5*s));slit.rotation.y=a;g.add(slit)}}
// Balcony (conditional)
if(hasBalcony){const balcY=(bodyH*.6+4)*s;
const balcRing=new THREE.Mesh(new THREE.TorusGeometry(topR*1.15,.25*s,5,nSides),useMat);balcRing.position.y=balcY;balcRing.rotation.x=Math.PI/2;g.add(balcRing);
const balcFloor=new THREE.Mesh(new THREE.CylinderGeometry(topR*1.15,topR*1.15,.25*s,nSides),useMat);balcFloor.position.y=balcY-.15*s;g.add(balcFloor)}
// Buttresses (conditional)
if(hasButtress){const nBut=3+Math.floor(seed*3);
for(let i=0;i<nBut;i++){const a=i/nBut*Math.PI*2;
const butt=new THREE.Mesh(new THREE.BoxGeometry(1.5*s,bodyH*.6,2*s),useMat);
butt.position.set(Math.cos(a)*(baseR+1*s),bodyH*.3,Math.sin(a)*(baseR+1*s));butt.rotation.y=a;butt.castShadow=true;g.add(butt)}}
// Door
{const tDoorW=3*s,tDoorH=6*s,tR=baseR*.95;
const tDoorPivot=new THREE.Group();tDoorPivot.position.set(-tDoorW/2,0,tR);
const tDoorPanel=new THREE.Mesh(new THREE.BoxGeometry(tDoorW,tDoorH,.3*s),new MS({color:0x3a2818,roughness:.85,metalness:.05}));tDoorPanel.position.set(tDoorW/2,tDoorH/2,0);tDoorPanel.castShadow=true;tDoorPivot.add(tDoorPanel);
const tDH=new THREE.Mesh(new THREE.SphereGeometry(.2*s,5,5),mt.gold);tDH.position.set(tDoorW*.8,tDoorH*.4,.2*s);tDoorPivot.add(tDH);
for(let bi=0;bi<2;bi++){const bb=new THREE.Mesh(new THREE.BoxGeometry(tDoorW-.3*s,.2*s,.35*s),mt.armorDk);bb.position.set(tDoorW/2,tDoorH*.25+bi*tDoorH*.35,0);tDoorPivot.add(bb)}
g.add(tDoorPivot);
doors.push({pivot:tDoorPivot,x:x,z:z+tR,openAng:-Math.PI/2,cur:0})}
// INTERIOR: Hollow space and spiral stairs
const innerR=topR*0.6; // Interior radius
const floorY=4*s;
// Ground floor
const floor0=new THREE.Mesh(new THREE.CylinderGeometry(innerR,innerR,.5*s,nSides),new MS({color:0x4a3a2a,roughness:.9}));floor0.position.y=floorY;g.add(floor0);
// Upper floors every 10 units
const nFloors=Math.floor(bodyH/10);
for(let fl=1;fl<nFloors;fl++){
const flY=floorY+fl*10*s;
const flMesh=new THREE.Mesh(new THREE.CylinderGeometry(innerR*.9,innerR*.9,.5*s,nSides),new MS({color:0x4a3a2a,roughness:.9}));flMesh.position.y=flY;g.add(flMesh);
// Floor hole in center for stairs
const hole=new THREE.Mesh(new THREE.CylinderGeometry(innerR*.3,innerR*.3,.6*s,nSides),new MS({color:0x2a1a0a,roughness:1}));hole.position.y=flY;g.add(hole)}
// Spiral staircase
const stairR=innerR*.7;const nSteps=Math.floor(bodyH/2);
for(let i=0;i<nSteps;i++){
const ang=i*0.5;const sy=floorY+i*2*s;
const step=new THREE.Mesh(new THREE.BoxGeometry(2*s,.4*s,1*s),new MS({color:0x5a4a3a,roughness:.85}));
step.position.set(Math.cos(ang)*stairR,sy,Math.sin(ang)*stairR);step.rotation.y=ang;g.add(step);
// Step support
const sup=new THREE.Mesh(new THREE.BoxGeometry(.3*s,sy,.3*s),new MS({color:0x4a3a2a,roughness:.9}));
sup.position.set(Math.cos(ang)*stairR,sy/2,Math.sin(ang)*stairR);g.add(sup)}
// Central stair pole
const pole=new THREE.Mesh(new THREE.CylinderGeometry(.3*s,.3*s,bodyH,nSides),new MS({color:0x3a2a1a,roughness:.9}));pole.position.y=bodyH/2+floorY;g.add(pole)
// Torch
const fm=new THREE.Mesh(new THREE.SphereGeometry(1.2,6,6),mt.fl);fm.position.y=bodyH*.8;g.add(fm);
g.position.set(x,h,z);scene.add(g);
torchPositions.push({x,y:h+bodyH*.8,z,mesh:fm,ph:Math.random()*6.28,big:false})}

// === NEW DETAILED BUILDINGS WITH INTERIORS ===

// Inn/Tavern - Two story with rooms, main hall, fireplace
function inn(x,z,rot,sc){
sc=(sc||1)*2;const h=meshTerrainH(x,z);const g=new THREE.Group();
const seed=Math.abs(Math.sin(x*83.3+z*197.7)*43758.5453)%1;
const wW=(18+seed*6)*sc,wD=(14+seed*5)*sc,wH=(12+seed*4)*sc;
const wallCol=new THREE.Color().setHSL(.12+seed*.06,.25+seed*.15,.4+seed*.15);
const wMat=new MS({color:wallCol,roughness:.85});
// Main structure
const body=new THREE.Mesh(new THREE.BoxGeometry(wW,wH,wD),wMat);body.position.y=wH/2;body.castShadow=true;g.add(body);
// Upper floor overhang
const upper=new THREE.Mesh(new THREE.BoxGeometry(wW+2*sc,4*sc,wD+2*sc),wMat);upper.position.y=wH+2*sc;upper.castShadow=true;g.add(upper);
// Roof
const roof=new THREE.Mesh(new THREE.ConeGeometry(Math.max(wW,wD)*.7,6*sc,4),mt.rf);roof.position.y=wH+5*sc;roof.rotation.y=rot||0;g.add(roof);
// Working door
const dW=3.5*sc,dH=6*sc;
const dPivot=new THREE.Group();dPivot.position.set(-dW/2,0,wD/2);
const dPanel=new THREE.Mesh(new THREE.BoxGeometry(dW,dH,.3*sc),new MS({color:0x4a3a2a,roughness:.9}));dPanel.position.set(dW/2,dH/2,0);dPanel.castShadow=true;dPivot.add(dPanel);
// Iron hinges
const hinge=new THREE.Mesh(new THREE.CylinderGeometry(.2*sc,.2*sc,.4*sc,6),mt.iron);hinge.position.set(0,dH*.25,.2*sc);dPivot.add(hinge);
const hinge2=hinge.clone();hinge2.position.set(0,dH*.75,.2*sc);dPivot.add(hinge2);
g.add(dPivot);
doors.push({pivot:dPivot,x:x,z:z+wD/2,openAng:-Math.PI/2,cur:0});
// Interior - ground floor
const flG=new THREE.Mesh(new THREE.BoxGeometry(wW*.8,.3*sc,wD*.8),new MS({color:0x5a4a3a,roughness:.9}));flG.position.y=0.2*sc;g.add(flG);
// Upper floor
const flU=new THREE.Mesh(new THREE.BoxGeometry(wW*.75,.3*sc,wD*.75),new MS({color:0x5a4a3a,roughness:.9}));flU.position.y=wH*.6;g.add(flU);
// Staircase
const stairW=2*sc,stairD=6*sc;
for(let si=0;si<8;si++){
const step=new THREE.Mesh(new THREE.BoxGeometry(stairW,.3*sc,1*sc),new MS({color:0x4a3a2a,roughness:.85}));
step.position.set(wW*.25,si*(wH*.6/8),-wD*.25+si*(stairD/8));g.add(step);}
// Chimney
const chim=new THREE.Mesh(new THREE.BoxGeometry(2*sc,wH+8*sc,2*sc),new MS({color:0x3a3a3a,roughness:.9}));
chim.position.set(-wW*.3,wH/2+4*sc,-wD*.3);g.add(chim);
// Chimney top smoke
const smoke=new THREE.Mesh(new THREE.SphereGeometry(1.5*sc,6,6),new MS({color:0x666666,transparent:true,opacity:.4}));
smoke.position.set(-wW*.3,wH+8*sc,-wD*.3);g.add(smoke);
// Window boxes with flower boxes
[-1,1].forEach(sx=>{
const win=new THREE.Mesh(new THREE.BoxGeometry(2*sc,3*sc,.3*sc),new MS({color:0x2a2a3a,emissive:0x1a1a2a,emissiveIntensity:.5}));
win.position.set(sx*(wW/2+.15),wH*.3,0);g.add(win);
const flowerBox=new THREE.Mesh(new THREE.BoxGeometry(2.5*sc,.5*sc,.8*sc),new MS({color:0x3a5a2a,roughness:.9}));
flowerBox.position.set(sx*(wW/2+.2),wH*.3-1.5*sc,.5*sc);g.add(flowerBox);});
g.position.set(x,h,z);g.rotation.y=rot||0;scene.add(g);
addCircleSolid(x,z,Math.max(wW,wD)/2+2,h,h+wH+10*sc);
markPlace(x,z,Math.max(wW,wD)/2+4);
makeEnterable(x,z,'inn','Tavern & Inn',Math.max(wW,wD)/2+3);}

// Blacksmith/Forge - Workshop with forge, anvil, loft
function forge(x,z,rot,sc){
sc=(sc||1)*2;const h=meshTerrainH(x,z);const g=new THREE.Group();
const seed=Math.abs(Math.sin(x*63.7+z*283.3)*43758.5453)%1;
const wW=(16+seed*5)*sc,wD=(12+seed*4)*sc,wH=(10+seed*3)*sc;
const wallCol=new THREE.Color().setHSL(.08+seed*.04,.2+seed*.1,.35+seed*.1);
const wMat=new MS({color:wallCol,roughness:.9});
// Main building
const body=new THREE.Mesh(new THREE.BoxGeometry(wW,wH,wD),wMat);body.position.y=wH/2;body.castShadow=true;g.add(body);
// High roof for smoke
const roof=new THREE.Mesh(new THREE.CylinderGeometry(wW*.4,wW*.6,8*sc,4),mt.rfDark);roof.position.y=wH+4*sc;g.add(roof);
// Large working door (wide for carts)
const dW=5*sc,dH=5.5*sc;
const dPivot=new THREE.Group();dPivot.position.set(-dW/2,0,wD/2);
const dPanel=new THREE.Mesh(new THREE.BoxGeometry(dW,dH,.4*sc),new MS({color:0x3a2a1a,roughness:.9}));
const dBand=new THREE.Mesh(new THREE.BoxGeometry(dW,.3*sc,.5*sc),mt.iron);dBand.position.set(dW/2,dH*.3,0);dPanel.add(dBand);
dPanel.position.set(dW/2,dH/2,0);dPanel.castShadow=true;dPivot.add(dPanel);
g.add(dPivot);
doors.push({pivot:dPivot,x:x,z:z+wD/2,openAng:-Math.PI/2,cur:0});
// Interior floor
const fl=new THREE.Mesh(new THREE.BoxGeometry(wW*.85,.3*sc,wD*.85),new MS({color:0x4a3a2a,roughness:.85}));fl.position.y=0.2*sc;g.add(fl);
// Forge (glowing)
const forge=new THREE.Mesh(new THREE.BoxGeometry(3*sc,4*sc,3*sc),new MS({color:0x2a1a0a,roughness:1}));
forge.position.set(-wW*.25,2*sc,-wD*.25);g.add(forge);
const forgeGlow=new THREE.Mesh(new THREE.SphereGeometry(1.2*sc,8,8),new MS({color:0xff4400,emissive:0xff2200,emissiveIntensity:2}));
forgeGlow.position.set(-wW*.25,3*sc,-wD*.25);g.add(forgeGlow);
// Anvil
const anvil=new THREE.Mesh(new THREE.BoxGeometry(1.5*sc,1.5*sc,1*sc),mt.iron);anvil.position.set(0,0.8*sc,0);g.add(anvil);
const anvilTop=new THREE.Mesh(new THREE.CylinderGeometry(.6*sc,.4*sc,.5*sc,8),mt.iron);anvilTop.position.set(0,1.6*sc,0);g.add(anvilTop);
// Storage loft
const loft=new THREE.Mesh(new THREE.BoxGeometry(wW*.7,.3*sc,wD*.4),new MS({color:0x4a3a2a,roughness:.9}));
loft.position.set(0,wH*.7,wD*.15);g.add(loft);
// Ladder to loft
const ladSide=new THREE.Mesh(new THREE.BoxGeometry(.3*sc,wH*.7,.1*sc),mt.wd);ladSide.position.set(wW*.2,wH*.35,-wD*.2);g.add(ladSide);
const ladSide2=ladSide.clone();ladSide2.position.x=wW*.25;g.add(ladSide2);
for(let li=0;li<6;li++){
const rung=new THREE.Mesh(new THREE.BoxGeometry(wW*.06,.1*sc,.12*sc),mt.wd);
rung.position.set(wW*.225,li*(wH*.7/6),-wD*.2);g.add(rung);}
// Chimney with smoke
const chim=new THREE.Mesh(new THREE.CylinderGeometry(1.5*sc,2*sc,wH+10*sc,6),new MS({color:0x3a3a3a}));
chim.position.set(-wW*.3,wH/2+5*sc,-wD*.3);g.add(chim);
// Smoke puff
const smoke=new THREE.Mesh(new THREE.SphereGeometry(2*sc,6,6),new MS({color:0x444444,transparent:true,opacity:.3}));
smoke.position.set(-wW*.3,wH+10*sc,-wD*.3);g.add(smoke);
g.position.set(x,h,z);g.rotation.y=rot||0;scene.add(g);
addCircleSolid(x,z,Math.max(wW,wD)/2+2,h,h+wH+12*sc);
markPlace(x,z,Math.max(wW,wD)/2+4);
makeEnterable(x,z,'forge','Blacksmith Forge',Math.max(wW,wD)/2+3);}

// Windmill - Rotating blades, internal ladder to top
function windmill(x,z,rot,sc){
sc=(sc||1)*2;const h=meshTerrainH(x,z);const g=new THREE.Group();
const seed=Math.abs(Math.sin(x*91.7+z*173.3)*43758.5453)%1;
const tR=(6+seed*2)*sc,tH=(28+seed*8)*sc;
const wallCol=new THREE.Color().setHSL(.15+seed*.05,.2+seed*.1,.5+seed*.15);
const tMat=new MS({color:wallCol,roughness:.85});
// Tower body (tapered cylinder)
const body=new THREE.Mesh(new THREE.CylinderGeometry(tR*.8,tR,tH,8),tMat);body.position.y=tH/2;body.castShadow=true;g.add(body);
// Domed cap
const cap=new THREE.Mesh(new THREE.SphereGeometry(tR*.9,8,8,0,Math.PI*2,0,Math.PI/2),mt.rf);cap.position.y=tH;g.add(cap);
// Entry door
const dW=2.5*sc,dH=5*sc;
const dPivot=new THREE.Group();dPivot.position.set(-dW/2,0,tR*.9);
const dPanel=new THREE.Mesh(new THREE.BoxGeometry(dW,dH,.3*sc),new MS({color:0x4a3a2a,roughness:.9}));
dPanel.position.set(dW/2,dH/2,0);dPanel.castShadow=true;dPivot.add(dPanel);
g.add(dPivot);
doors.push({pivot:dPivot,x:x,z:z+tR*.9,openAng:-Math.PI/2,cur:0});
// Interior floors (3 levels)
for(let fi=1;fi<=3;fi++){
const flY=fi*(tH/4);
const fl=new THREE.Mesh(new THREE.CircleGeometry(tR*.6,8),new MS({color:0x5a4a3a,roughness:.9}));
fl.rotation.x=-Math.PI/2;fl.position.y=flY;g.add(fl);
// Center hole for ladder
const hole=new THREE.Mesh(new THREE.CircleGeometry(tR*.2,8),new MS({color:0x2a1a0a,roughness:1}));
hole.rotation.x=-Math.PI/2;hole.position.y=flY+.02;g.add(hole);}
// Central ladder
const ladPole=new THREE.Mesh(new THREE.CylinderGeometry(.15*sc,.15*sc,tH,6),mt.wd);ladPole.position.y=tH/2;g.add(ladPole);
for(let li=0;li<15;li++){
const rung=new THREE.Mesh(new THREE.BoxGeometry(1*sc,.1*sc,.15*sc),mt.wd);
rung.position.y=li*(tH/15);g.add(rung);}
// Rotating blades group
const bladeGroup=new THREE.Group();bladeGroup.position.set(0,tH+tR*.3,0);
// Hub
const hub=new THREE.Mesh(new THREE.CylinderGeometry(1*sc,1*sc,2*sc,8),mt.wd);hub.rotation.x=Math.PI/2;bladeGroup.add(hub);
// 4 blades
for(let bi=0;bi<4;bi++){
const a=bi*Math.PI/2;
const bladeArm=new THREE.Mesh(new THREE.BoxGeometry(1*sc,.5*sc,12*sc),mt.wd);
bladeArm.position.set(Math.sin(a)*6*sc,Math.cos(a)*6*sc,0);bladeArm.rotation.z=-a;bladeGroup.add(bladeArm);
const bladeSail=new THREE.Mesh(new THREE.BoxGeometry(2.5*sc,.1*sc,9*sc),new MS({color:0xddddcc,roughness:.9}));
bladeSail.position.set(Math.sin(a)*6*sc,Math.cos(a)*10*sc,1*sc);bladeSail.rotation.z=-a;bladeGroup.add(bladeSail);}
g.add(bladeGroup);
// Store reference for animation
windmills.push({mesh:bladeGroup,x:x,z:z});
// Millstone at bottom (grinding)
const mill=new THREE.Mesh(new THREE.CylinderGeometry(2*sc,.3*sc,2*sc,8),mt.st);mill.position.set(0,2*sc,0);g.add(mill);
g.position.set(x,h,z);g.rotation.y=rot||0;scene.add(g);
addCircleSolid(x,z,tR*1.2,h,h+tH+5*sc);
markPlace(x,z,tR*1.5);
makeEnterable(x,z,'windmill','Windmill',tR+3);}

// Watchtower - Military tower with battlements, multiple floors
function watchtower(x,z,rot,sc){
sc=(sc||1)*2;const h=meshTerrainH(x,z);const g=new THREE.Group();
const seed=Math.abs(Math.sin(x*71.3+z*241.7)*43758.5453)%1;
const tW=(8+seed*3)*sc,tH=(35+seed*12)*sc;
const wallCol=new THREE.Color().setHSL(.1+seed*.04,.15+seed*.1,.4+seed*.1);
const wMat=new MS({color:wallCol,roughness:.8});
// Main tower (square)
const body=new THREE.Mesh(new THREE.BoxGeometry(tW,tH,tW),wMat);body.position.y=tH/2;body.castShadow=true;g.add(body);
// Crenellated top
const crenW=tW+1*sc;
for(let ci=0;ci<8;ci++){
const cx=(ci<4?1:-1)*((ci%2===0?crenW/2:crenW/2-1.5*sc));
const cz=(ci<4?-1:1)*((ci%2===1?crenW/2:crenW/2-1.5*sc));
const cren=new THREE.Mesh(new THREE.BoxGeometry(1.5*sc,2*sc,1.5*sc),wMat);
cren.position.set(cx,tH+1*sc,cz);g.add(cren);}
// Roof platform
const roofPlat=new THREE.Mesh(new THREE.BoxGeometry(tW,.5*sc,tW),new MS({color:0x4a4a4a}));
roofPlat.position.y=tH;g.add(roofPlat);
// Working door at base
const dW=2.5*sc,dH=5*sc;
const dPivot=new THREE.Group();dPivot.position.set(-dW/2,0,tW/2);
const dPanel=new THREE.Mesh(new THREE.BoxGeometry(dW,dH,.3*sc),new MS({color:0x3a2a1a,roughness:.9}));
dPanel.position.set(dW/2,dH/2,0);dPanel.castShadow=true;dPivot.add(dPanel);
// Iron reinforcement
const ironB=new THREE.Mesh(new THREE.BoxGeometry(dW,.2*sc,.35*sc),mt.iron);ironB.position.set(dW/2,dH*.3,0);dPivot.add(ironB);
const ironB2=ironB.clone();ironB2.position.y=dH*.7;dPivot.add(ironB2);
g.add(dPivot);
doors.push({pivot:dPivot,x:x,z:z+tW/2,openAng:-Math.PI/2,cur:0});
// Interior floors (4 levels)
for(let fl=1;fl<=4;fl++){
const flY=fl*(tH/5);
const floor=new THREE.Mesh(new THREE.BoxGeometry(tW*.8,.2*sc,tW*.8),new MS({color:0x4a4a4a,roughness:.9}));
floor.position.y=flY;g.add(floor);
// Center hole for ladder
const hole=new THREE.Mesh(new THREE.BoxGeometry(tW*.25,.25*sc,tW*.25),new MS({color:0x1a1a1a}));
hole.position.y=flY;g.add(hole);}
// Central ladder shaft
const ladPole=new THREE.Mesh(new THREE.CylinderGeometry(.2*sc,.2*sc,tH,6),mt.iron);ladPole.position.y=tH/2;g.add(ladPole);
for(let li=0;li<20;li++){
const rung=new THREE.Mesh(new THREE.BoxGeometry(1.2*sc,.1*sc,.15*sc),mt.iron);
rung.position.y=li*(tH/20);g.add(rung);}
// Arrow slits
for(let si=0;si<3;si++){
const slitH=tH*.25+si*tH*.25;
[-1,1].forEach(sx=>{
const slit=new THREE.Mesh(new THREE.BoxGeometry(.3*sc,2*sc,.2*sc),new MS({color:0x0a0a0a}));
slit.position.set(sx*(tW/2+.1),slitH,0);g.add(slit);});}
// Torch sconces
[-1,1].forEach(sx=>{
const sconce=new THREE.Mesh(new THREE.CylinderGeometry(.3*sc,.4*sc,.8*sc,6),mt.iron);
sconce.position.set(sx*(tW/2+.2),tH*.5,tW/2+.2);g.add(sconce);
const flame=new THREE.Mesh(new THREE.SphereGeometry(.4*sc,6,6),mt.fl);flame.position.set(sx*(tW/2+.2),tH*.5+.6*sc,tW/2+.2);g.add(flame);
torchPositions.push({x:x+sx*(tW/2+.2)*Math.cos(rot||0),y:h+tH*.5+.6*sc,z:z+sx*(tW/2+.2)*Math.sin(rot||0),mesh:flame,ph:Math.random()*6.28,big:false});});
g.position.set(x,h,z);g.rotation.y=rot||0;scene.add(g);
addCircleSolid(x,z,tW*.7,h,h+tH+3*sc);
markPlace(x,z,tW);
makeEnterable(x,z,'watchtower','Watchtower',tW);}

// Mansion - Large multi-story house with grand staircase
function mansion(x,z,rot,sc){
sc=(sc||1)*2;const h=meshTerrainH(x,z);const g=new THREE.Group();
const seed=Math.abs(Math.sin(x*113.7+z*257.3)*43758.5453)%1;
const wW=(24+seed*8)*sc,wD=(18+seed*6)*sc,wH=(16+seed*6)*sc;
const wallCol=new THREE.Color().setHSL(.15+seed*.06,.22+seed*.12,.45+seed*.12);
const wMat=new MS({color:wallCol,roughness:.8});
// Main body
const body=new THREE.Mesh(new THREE.BoxGeometry(wW,wH,wD),wMat);body.position.y=wH/2;body.castShadow=true;g.add(body);
// Fancy roof (hipped)
const roof=new THREE.Mesh(new THREE.CylinderGeometry(wW*.5,wD*.6,6*sc,4),mt.rf);roof.position.y=wH+3*sc;roof.rotation.y=(rot||0)+.785;g.add(roof);
// Portico with columns
const portW=wW*.6,portD=4*sc;
const portCeil=new THREE.Mesh(new THREE.BoxGeometry(portW,.5*sc,portD),wMat);
portCeil.position.set(0,wH*.7,wD/2+portD/2);g.add(portCeil);
// Columns
[-1,0,1].forEach(c=>{
const col=new THREE.Mesh(new THREE.CylinderGeometry(.6*sc,.6*sc,wH*.7,8),new MS({color:0xdddddd,roughness:.7}));
col.position.set(c*portW*.4,wH*.35,wD/2+portD/2);g.add(col);});
// Grand double doors
const dW=4*sc,dH=7*sc;
const dPivot=new THREE.Group();dPivot.position.set(-dW/2,0,wD/2+portD);
const dPanel=new THREE.Mesh(new THREE.BoxGeometry(dW,dH,.3*sc),new MS({color:0x4a3a2a,roughness:.85}));
// Door panels split
const leftPanel=new THREE.Mesh(new THREE.BoxGeometry(dW/2-.1*sc,dH,.25*sc),new MS({color:0x4a3a2a,roughness:.85}));
leftPanel.position.set(dW/4,dH/2,0);leftPanel.castShadow=true;dPivot.add(leftPanel);
const rightPanel=leftPanel.clone();rightPanel.position.x=3*dW/4;dPivot.add(rightPanel);
// Gold handles
const handle=new THREE.Mesh(new THREE.SphereGeometry(.25*sc,6,6),mt.gold);handle.position.set(dW*.35,dH*.5,.2*sc);dPivot.add(handle);
const handle2=handle.clone();handle2.position.x=dW*.65;dPivot.add(handle2);
g.add(dPivot);
doors.push({pivot:dPivot,x:x,z:z+wD/2+portD,openAng:-Math.PI/2,cur:0});
// Interior - ground floor (marble)
const flG=new THREE.Mesh(new THREE.BoxGeometry(wW*.85,.2*sc,wD*.85),new MS({color:0x8a8a8a,roughness:.6}));flG.position.y=0.15*sc;g.add(flG);
// Second floor
const fl2=new THREE.Mesh(new THREE.BoxGeometry(wW*.8,.2*sc,wD*.8),new MS({color:0x7a6a5a,roughness:.85}));fl2.position.y=wH*.5;g.add(fl2);
// Third floor/attic
const fl3=new THREE.Mesh(new THREE.BoxGeometry(wW*.7,.2*sc,wD*.6),new MS({color:0x6a5a4a,roughness:.9}));fl3.position.y=wH*.8;g.add(fl3);
// Grand staircase
for(let si=0;si<12;si++){
const stepW=3*sc;
const step=new THREE.Mesh(new THREE.BoxGeometry(stepW,.3*sc,1*sc),new MS({color:0x5a4a3a,roughness:.85}));
step.position.set(0,si*(wH*.5/12),-wD*.2+si*(wD*.3/12));g.add(step);
// Stair railing
const rail=new THREE.Mesh(new THREE.CylinderGeometry(.1*sc,.1*sc,wH*.5,6),mt.gold);
rail.position.set(stepW/2,si*(wH*.5/12)+wH*.25,0);g.add(rail);}
// Windows with shutters
[-1,1].forEach(sx=>{
for(let wi=0;wi<2;wi++){
const wy=wH*.25+wi*wH*.35;
const winFrame=new THREE.Mesh(new THREE.BoxGeometry(.3*sc,3*sc,2*sc),mt.wd);winFrame.position.set(sx*(wW/2+.15),wy,wD*.2);g.add(winFrame);
const winGlass=new THREE.Mesh(new THREE.BoxGeometry(.15*sc,2.5*sc,1.5*sc),new MS({color:0x2a3a4a,emissive:0x1a2a3a,emissiveIntensity:.4}));
winGlass.position.set(sx*(wW/2+.2),wy,wD*.2);g.add(winGlass);}});
// Balcony on front
const balc=new THREE.Mesh(new THREE.BoxGeometry(wW*.5,.3*sc,2*sc),new MS({color:0x5a4a3a}));
balc.position.set(0,wH*.5,wD/2+1*sc);g.add(balc);
// Chimneys
[-wW*.3,wW*.3].forEach(cx=>{
const chim=new THREE.Mesh(new THREE.BoxGeometry(1.5*sc,wH+6*sc,1.5*sc),new MS({color:0x4a4a4a}));
chim.position.set(cx,wH/2+3*sc,-wD*.3);g.add(chim);});
g.position.set(x,h,z);g.rotation.y=rot||0;scene.add(g);
addCircleSolid(x,z,Math.max(wW,wD)/2+3,h,h+wH+8*sc);
markPlace(x,z,Math.max(wW,wD)/2+5);
makeEnterable(x,z,'mansion','Mansion Estate',Math.max(wW,wD)/2+4);}

// Chapel - Small church with nave, altar, bell tower
function chapel(x,z,rot,sc){
sc=(sc||1)*2;const h=meshTerrainH(x,z);const g=new THREE.Group();
const seed=Math.abs(Math.sin(x*101.3+z*223.7)*43758.5453)%1;
const nW=(10+seed*3)*sc,nL=(18+seed*5)*sc,nH=(10+seed*3)*sc;
const wallCol=new THREE.Color().setHSL(.12+seed*.05,.2+seed*.1,.42+seed*.1);
const wMat=new MS({color:wallCol,roughness:.85});
// Nave (main hall)
const nave=new THREE.Mesh(new THREE.BoxGeometry(nW,nH,nL),wMat);nave.position.y=nH/2;nave.castShadow=true;g.add(nave);
// Steep roof
const roof=new THREE.Mesh(new THREE.CylinderGeometry(nW*.7,nL*.5,5*sc,3),mt.rf);roof.position.y=nH+2.5*sc;roof.rotation.x=-Math.PI/2;roof.rotation.z=(rot||0);g.add(roof);
// Bell tower at front
const tW=4*sc,tH=12*sc;
const tower=new THREE.Mesh(new THREE.BoxGeometry(tW,tH,tW),wMat);tower.position.set(0,tH/2,nL/2+tW/2);tower.castShadow=true;g.add(tower);
// Tower roof (spire)
const spire=new THREE.Mesh(new THREE.ConeGeometry(tW*.8,8*sc,4),mt.st);spire.position.set(0,tH+4*sc,nL/2+tW/2);g.add(spire);
// Bell visible in tower
const bell=new THREE.Mesh(new THREE.ConeGeometry(.8*sc,1.2*sc,8),mt.gold);bell.position.set(0,tH*.7,nL/2+tW/2);g.add(bell);
// Working church doors
const dW=3*sc,dH=6*sc;
const dPivot=new THREE.Group();dPivot.position.set(-dW/2,0,nL/2);
const dPanel=new THREE.Mesh(new THREE.BoxGeometry(dW,dH,.3*sc),new MS({color:0x4a3a2a,roughness:.9}));
dPanel.position.set(dW/2,dH/2,0);dPanel.castShadow=true;dPivot.add(dPanel);
// Iron hinges
const hinge=new THREE.Mesh(new THREE.CylinderGeometry(.15*sc,.15*sc,.4*sc,6),mt.iron);hinge.rotation.z=Math.PI/2;hinge.position.set(0,dH*.25,.2*sc);dPivot.add(hinge);
const hinge2=hinge.clone();hinge2.position.set(0,dH*.75,.2*sc);dPivot.add(hinge2);
g.add(dPivot);
doors.push({pivot:dPivot,x:x,z:z+nL/2,openAng:-Math.PI/2,cur:0});
// Interior floor
const fl=new THREE.Mesh(new THREE.BoxGeometry(nW*.9,.2*sc,nL*.9),new MS({color:0x5a4a3a,roughness:.9}));fl.position.y=0.15*sc;g.add(fl);
// Altar at far end
const altar=new THREE.Mesh(new THREE.BoxGeometry(2*sc,2*sc,1*sc),mt.st);altar.position.set(0,1*sc,-nL*.35);g.add(altar);
const altarCloth=new THREE.Mesh(new THREE.BoxGeometry(2.2*sc,.1*sc,1.2*sc),new MS({color:0x8a2020}));
altarCloth.position.set(0,2*sc,-nL*.35);g.add(altarCloth);
// Pews ( benches)
for(let pi=0;pi<4;pi++){
const pew=new THREE.Mesh(new THREE.BoxGeometry(nW*.6,.8*sc,1*sc),mt.wd);
pew.position.set(0,.4*sc,-nL*.1+pi*2.5*sc);g.add(pew);
const pewBack=new THREE.Mesh(new THREE.BoxGeometry(nW*.6,1.5*sc,.2*sc),mt.wd);
pewBack.position.set(0,1*sc,-nL*.1+pi*2.5*sc-.4*sc);g.add(pewBack);}
// Stained glass windows
[-1,1].forEach(sx=>{
const win=new THREE.Mesh(new THREE.BoxGeometry(.2*sc,3*sc,2*sc),new MS({color:0x6a2a8a,emissive:0x4a1a6a,emissiveIntensity:.6}));
win.position.set(sx*(nW/2+.1),nH*.5,0);g.add(win);});
// Cross on spire top
const crossV=new THREE.Mesh(new THREE.BoxGeometry(.2*sc,2*sc,.2*sc),mt.gold);crossV.position.set(0,tH+8*sc,nL/2+tW/2);g.add(crossV);
const crossH=new THREE.Mesh(new THREE.BoxGeometry(1.5*sc,.2*sc,.2*sc),mt.gold);crossH.position.set(0,tH+8.5*sc,nL/2+tW/2);g.add(crossH);
g.position.set(x,h,z);g.rotation.y=rot||0;scene.add(g);
addCircleSolid(x,z,Math.max(nW,nL)/2+2,h,h+nH+15*sc);
markPlace(x,z,Math.max(nW,nL)/2+3);
makeEnterable(x,z,'chapel','Village Chapel',Math.max(nW,nL)/2+2);}

// Barn/Stable - Long building with stalls, hay loft
function barn(x,z,rot,sc){
sc=(sc||1)*2;const h=meshTerrainH(x,z);const g=new THREE.Group();
const seed=Math.abs(Math.sin(x*87.7+z*191.3)*43758.5453)%1;
const bW=(10+seed*3)*sc,bL=(24+seed*8)*sc,bH=(10+seed*3)*sc;
const wallCol=new THREE.Color().setHSL(.13+seed*.05,.35+seed*.15,.42+seed*.1);
const wMat=new MS({color:wallCol,roughness:.9});
// Main barn body
const body=new THREE.Mesh(new THREE.BoxGeometry(bW,bH,bL),wMat);body.position.y=bH/2;body.castShadow=true;g.add(body);
// Gable roof
const roof=new THREE.Mesh(new THREE.CylinderGeometry(bW*.7,bL*.6,5*sc,3),mt.rf);roof.position.y=bH+2.5*sc;roof.rotation.x=-Math.PI/2;roof.rotation.z=(rot||0);g.add(roof);
// Large barn doors (double sliding style - visual only, use regular door for entry)
const dW=4*sc,dH=6*sc;
const dPivot=new THREE.Group();dPivot.position.set(-dW/2,0,bL/2);
const dPanel=new THREE.Mesh(new THREE.BoxGeometry(dW,dH,.3*sc),new MS({color:0x5a4a3a,roughness:.9}));
// X brace pattern
const brace1=new THREE.Mesh(new THREE.BoxGeometry(dW*.8,.3*sc,.32*sc),mt.wd);brace1.position.set(dW/2,dH/2,0);brace1.rotation.z=.785;dPivot.add(brace1);
const brace2=brace1.clone();brace2.rotation.z=-.785;dPivot.add(brace2);
dPanel.position.set(dW/2,dH/2,0);dPanel.castShadow=true;dPivot.add(dPanel);
g.add(dPivot);
doors.push({pivot:dPivot,x:x,z:z+bL/2,openAng:-Math.PI/2,cur:0});
// Interior floor (dirt)
const fl=new THREE.Mesh(new THREE.BoxGeometry(bW*.9,.1*sc,bL*.9),new MS({color:0x4a3a2a,roughness:1}));fl.position.y=0.1*sc;g.add(fl);
// Hay loft
const loft=new THREE.Mesh(new THREE.BoxGeometry(bW*.85,.3*sc,bL*.7),new MS({color:0x8a7a4a,roughness:.95}));
loft.position.y=bH*.65;g.add(loft);
// Ladder to loft
const ladSide=new THREE.Mesh(new THREE.BoxGeometry(.3*sc,bH*.65,.1*sc),mt.wd);
ladSide.position.set(bW*.3,bH*.325,-bL*.3);g.add(ladSide);
const ladSide2=ladSide.clone();ladSide2.position.x=bW*.35;g.add(ladSide2);
for(let li=0;li<8;li++){
const rung=new THREE.Mesh(new THREE.BoxGeometry(bW*.06,.1*sc,.12*sc),mt.wd);
rung.position.set(bW*.325,li*(bH*.65/8),-bL*.3);g.add(rung);}
// Stalls/dividers
for(let si=0;si<3;si++){
const stall=new THREE.Mesh(new THREE.BoxGeometry(bW*.8,4*sc,.3*sc),mt.wd);
stall.position.set(0,2*sc,-bL*.25+si*bL*.25);g.add(stall);
// Hay bales
const bale=new THREE.Mesh(new THREE.BoxGeometry(1.5*sc,1*sc,2*sc),new MS({color:0x9a8a3a}));
bale.position.set(bW*.2,0.5*sc,-bL*.25+si*bL*.25+bL*.1);g.add(bale);}
// Windows (high up)
const win=new THREE.Mesh(new THREE.BoxGeometry(1.5*sc,1.5*sc,.2*sc),new MS({color:0x2a3a4a,emissive:0x1a2a3a,emissiveIntensity:.3}));
win.position.set(0,bH*.7,bL/2+.1);g.add(win);
// Exterior hay pile
const hayPile=new THREE.Mesh(new THREE.ConeGeometry(3*sc,4*sc,8),new MS({color:0x8a7a3a}));
hayPile.position.set(bW*.8,2*sc,-bL*.4);g.add(hayPile);
g.position.set(x,h,z);g.rotation.y=rot||0;scene.add(g);
addCircleSolid(x,z,Math.max(bW,bL)/2+2,h,h+bH+5*sc);
markPlace(x,z,Math.max(bW,bL)/2+3);
makeEnterable(x,z,'barn','Barn & Stables',Math.max(bW,bL)/2+2);}


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
const bridgeDeck=new THREE.Mesh(new THREE.BoxGeometry(5.5,.4,len),mt.bridge);bridgeDeck.position.set(0,2.1,0);bridgeDeck.receiveShadow=true;g.add(bridgeDeck);
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
for(let i=0;i<3;i++){const w=new THREE.Mesh(new THREE.BoxGeometry(3+Math.random()*5,8+Math.random()*16,2.5),mt.stD);w.position.set((Math.random()-.5)*18,5+Math.random()*4,(Math.random()-.5)*18);w.rotation.set(Math.random()*.15,Math.random(),Math.random()*.15);w.castShadow=true;g.add(w)}
addCircleSolid(x,z,12,h,h+25);
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
function gothicSpire(x,z,h,sc){sc=(sc||1)*2;const bY=meshTerrainH(x,z);const g=new THREE.Group();
// Base pillar (octagonal)
const base=new THREE.Mesh(new THREE.CylinderGeometry(4*sc,5*sc,h*.6,8),mt.stGoth);base.position.y=h*.3;base.castShadow=true;g.add(base);
addCircleSolid(x,z,5*sc,bY,bY+h*1.2);
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

function gothicArch(x,z,rot,sc){sc=(sc||1)*2;const bY=meshTerrainH(x,z);const g=new THREE.Group();
// Two pillars
addCircleSolid(x,z,10*sc,bY,bY+30*sc);
[-1,1].forEach(s=>{const p=new THREE.Mesh(new THREE.BoxGeometry(3*sc,24*sc,3*sc),mt.stGoth);p.position.set(s*7*sc,12*sc,0);p.castShadow=true;g.add(p);
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

function flyingButtress(x,z,rot,sc){sc=(sc||1)*2;const bY=meshTerrainH(x,z);const g=new THREE.Group();
// Base pier
const pier=new THREE.Mesh(new THREE.BoxGeometry(2.5*sc,18*sc,2.5*sc),mt.stGoth);pier.position.set(0,9*sc,0);pier.castShadow=true;g.add(pier);
// Arch arm (angled)
const arm=new THREE.Mesh(new THREE.BoxGeometry(1.5*sc,2*sc,14*sc),mt.st);arm.position.set(0,16*sc,6*sc);arm.rotation.x=-.35;arm.castShadow=true;g.add(arm);
// Pinnacle on top
const pin=new THREE.Mesh(new THREE.ConeGeometry(1.5*sc,6*sc,6),mt.stD);pin.position.set(0,21*sc,0);pin.castShadow=true;g.add(pin);
g.position.set(x,bY,z);g.rotation.y=rot||0;scene.add(g)}

function cathedral(x,z,rot,sc){sc=(sc||1)*2;const bY=meshTerrainH(x,z);const g=new THREE.Group();
// Main nave
const nave=new THREE.Mesh(new THREE.BoxGeometry(20*sc,25*sc,40*sc),mt.stGoth);nave.position.y=12.5*sc;nave.castShadow=true;g.add(nave);
addCircleSolid(x,z,22*sc,bY,bY+50*sc);
// Peaked roof
const roof=new THREE.Mesh(new THREE.BoxGeometry(22*sc,3*sc,42*sc),mt.rfSlate);roof.position.y=26*sc;roof.rotation.z=0;roof.castShadow=true;g.add(roof);
const roofPeak=new THREE.Mesh(new THREE.BoxGeometry(4*sc,8*sc,42*sc),mt.rfSlate);roofPeak.position.y=30*sc;roofPeak.castShadow=true;g.add(roofPeak);
// Front face with pointed entrance
const front=new THREE.Mesh(new THREE.BoxGeometry(22*sc,30*sc,2*sc),mt.st);front.position.set(0,15*sc,21*sc);front.castShadow=true;g.add(front);
// Working cathedral door
const catDoorW=5*sc,catDoorH=10*sc;
const catDoorPivot=new THREE.Group();catDoorPivot.position.set(-catDoorW/2,0,21*sc);
const catDoorPanel=new THREE.Mesh(new THREE.BoxGeometry(catDoorW,catDoorH,.3*sc),new MS({color:0x4a3a2a,roughness:.85}));catDoorPanel.position.set(catDoorW/2,catDoorH/2,0);catDoorPanel.castShadow=true;catDoorPivot.add(catDoorPanel);
// Iron bands on door
for(let bi=0;bi<3;bi++){const band=new THREE.Mesh(new THREE.BoxGeometry(catDoorW,.2*sc,.35*sc),mt.iron);band.position.set(catDoorW/2,(bi+1)*catDoorH*.25,0);catDoorPivot.add(band)}
// Door handle
const dH=new THREE.Mesh(new THREE.SphereGeometry(.25*sc,5,5),mt.gold);dH.position.set(catDoorW*.7,catDoorH*.5,.2*sc);catDoorPivot.add(dH);
g.add(catDoorPivot);
doors.push({pivot:catDoorPivot,x:x,z:z+21*sc,openAng:-Math.PI/2,cur:0});
// Interior floors and stairs to bell towers
const catInnerW=14*sc,catInnerD=32*sc;
for(let cl=1;cl<3;cl++){
const cflY=cl*10*sc;
const cFloor=new THREE.Mesh(new THREE.BoxGeometry(catInnerW,1*sc,catInnerD),new MS({color:0x3a2a1a,roughness:.9}));
cFloor.position.set(0,cflY,0);g.add(cFloor);
// Hole for stairs
const cHole=new THREE.Mesh(new THREE.BoxGeometry(catInnerW*.3,1.2*sc,catInnerD*.3),new MS({color:0x1a0a0a,roughness:1}));
cHole.position.set(0,cflY,0);g.add(cHole)}
// Stairs to bell towers
[-1,1].forEach(s=>{
const bStairR=5*sc;const bNSteps=20;
for(let bs=0;bs<bNSteps;bs++){
const bang=bs*0.3+s*Math.PI;const bsy=bs*1.5*sc;
const bstep=new THREE.Mesh(new THREE.BoxGeometry(1.5*sc,.3*sc,.8*sc),new MS({color:0x4a3a2a,roughness:.85}));
bstep.position.set(s*14*sc+Math.cos(bang)*bStairR,bsy,19*sc+Math.sin(bang)*bStairR);bstep.rotation.y=bang;g.add(bstep)}});
// Pointed gable
const gable=new THREE.Mesh(new THREE.ConeGeometry(12*sc,14*sc,4),mt.stGoth);gable.position.set(0,37*sc,21*sc);gable.rotation.y=Math.PI/4;gable.castShadow=true;g.add(gable);
// Rose window (circle of small arches)
for(let i=0;i<8;i++){const a=i/8*Math.PI*2;const spoke=new THREE.Mesh(new THREE.BoxGeometry(.3*sc,3*sc,.3),mt.stD);spoke.position.set(Math.cos(a)*3.5*sc,22*sc+Math.sin(a)*3.5*sc,22*sc);spoke.rotation.z=a;g.add(spoke)}
const rwRing=new THREE.Mesh(new THREE.TorusGeometry(3.5*sc,.4*sc,6,16),mt.st);rwRing.position.set(0,22*sc,22*sc);g.add(rwRing);
const rwGlow=new THREE.Mesh(new THREE.CircleGeometry(3*sc,12),new MS({color:0x2a3a5a,emissive:0x1a2a4a,emissiveIntensity:.8,side:THREE.DoubleSide}));rwGlow.position.set(0,22*sc,21.8*sc);g.add(rwGlow);
// Bell towers (twin spires)
[-1,1].forEach(s=>{const tw=new THREE.Mesh(new THREE.BoxGeometry(6*sc,35*sc,6*sc),mt.stGoth);tw.position.set(s*14*sc,17.5*sc,19*sc);tw.castShadow=true;g.add(tw);
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

function grandStairs(x,z,rot,steps,w,sc){sc=(sc||1)*2;steps=steps||12;w=w||10;const bY=meshTerrainH(x,z);const g=new THREE.Group();
for(let i=0;i<steps;i++){const step=new THREE.Mesh(new THREE.BoxGeometry(w*sc,1.2*sc,2.5*sc),mt.stGoth);step.position.set(0,i*1.1*sc,i*2.2*sc);step.castShadow=true;step.receiveShadow=true;g.add(step)}
// Balustrades
[-1,1].forEach(s=>{for(let i=0;i<steps;i+=2){const post=new THREE.Mesh(new THREE.CylinderGeometry(.3*sc,.35*sc,4*sc,5),mt.st);post.position.set(s*(w/2+.5)*sc,i*1.1*sc+2*sc,i*2.2*sc);post.castShadow=true;g.add(post)}});
g.position.set(x,bY,z);g.rotation.y=rot||0;scene.add(g)}

// Footprint tracking to prevent building overlap (defined early for hand-placed structures)
const cityFootprints=[];
function canPlace(bx,bz,rad){for(const f of cityFootprints){if(Math.hypot(bx-f.x,bz-f.z)<rad+f.r)return false}return true}
function markPlace(bx,bz,rad){cityFootprints.push({x:bx,z:bz,r:rad})}

// ========== LUMBRIDGE (0,0) — minimal hand-placed, procCity handles bulk ==========
gothicArch(0,10,0,1.2);markPlace(0,10,12);bonfire(0,5);
cathedral(120,80,-.3,.8);markPlace(120,80,60);makeEnterable(120,80,'cathedral','Lumbridge Cathedral');
torch(30,20);torch(55,35);torch(0,-40);

// ========== VARROCK (550,50) ==========
cathedral(555,50,0,1.2);markPlace(555,50,70);bonfire(555,50);makeEnterable(555,50,'cathedral','Varrock Cathedral');
torch(490,90);torch(620,10);

// ========== WILDERNESS (0,-650) ==========
for(let i=0;i<5;i++){const rx=(Math.random()-.5)*300,rz=-550-Math.random()*200;if(canPlace(rx,rz,20)){ruin(rx,rz);markPlace(rx,rz,20)}}
for(let i=0;i<3;i++){const lx=(Math.random()-.5)*200,lz=-600-Math.random()*150;const lv=new THREE.Mesh(new THREE.CircleGeometry(6+Math.random()*8,8),mt.lava);lv.rotation.x=-Math.PI/2;lv.position.set(lx,meshTerrainH(lx,lz)+.5,lz);scene.add(lv);torchPositions.push({x:lx,y:meshTerrainH(lx,lz)+4,z:lz,mesh:lv,ph:Math.random()*6.28,big:true,col:0xff4400})}
tower(-45,-580,1.5);markPlace(-45,-580,28);makeEnterable(-45,-580,'tower','Wilderness Tower');tower(55,-580,1.5);markPlace(55,-580,28);makeEnterable(55,-580,'tower','Wilderness Tower');

// ========== AL KHARID (580,400) ==========
tower(525,350,1.2);markPlace(525,350,28);makeEnterable(525,350,'tower','Al Kharid Tower');tower(640,450,1.2);markPlace(640,450,28);makeEnterable(640,450,'tower','Al Kharid Tower');bonfire(580,400);

// ========== FALADOR (-480,280) ==========
cathedral(-480,280,Math.PI/2,1);markPlace(-480,280,60);bonfire(-480,260);makeEnterable(-480,280,'cathedral','Falador Cathedral');

// ========== BARBARIAN VILLAGE (280,-250) ==========
hut(260,-240,.3,1.2);markPlace(260,-240,24);hut(300,-260,-.5,1);markPlace(300,-260,20);bonfire(280,-250);

// ========== DRAYNOR (-300,-150) ==========
hut(-320,-160,1,.8);markPlace(-320,-160,20);hut(-280,-180,-.5,.9);markPlace(-280,-180,20);tower(-315,-100,1.2);markPlace(-315,-100,28);makeEnterable(-315,-100,'tower','Draynor Tower');bonfire(-300,-150);

// ========== PORT SARIM (-160,480) ==========
hut(-190,460,.5,1);markPlace(-190,460,20);hut(-150,470,.8,1);markPlace(-150,470,20);bridge(-160,420,0,40);
const hull=new THREE.Mesh(new THREE.BoxGeometry(14,6,30),mt.wd);hull.position.set(-30,meshTerrainH(-30,510)+3,510);hull.castShadow=true;scene.add(hull);markPlace(-30,510,36);
bonfire(-160,470);

// ========== EDGEVILLE (150,-350) ==========
hut(140,-340,.5,1);markPlace(140,-340,20);hut(170,-345,-.3,1);markPlace(170,-345,20);bonfire(155,-350);

// ========== CATHERBY (-500,-400) ==========
hut(-520,-390,.3,.9);markPlace(-520,-390,20);hut(-505,-395,-.5,.9);markPlace(-505,-395,20);bonfire(-500,-400);

// ========== ARDOUGNE (-1200,100) ==========
cathedral(-1200,100,0,1);markPlace(-1200,100,60);bonfire(-1200,100);torch(-1250,100);torch(-1150,100);

// ========== CANIFIS (1300,-200) ==========
hut(1270,-210,.3,.8);markPlace(1270,-210,20);hut(1330,-205,-.4,.8);markPlace(1330,-205,20);tower(1340,-180,1.2);markPlace(1340,-180,28);makeEnterable(1340,-180,'tower','Canifis Tower');bonfire(1300,-200);

// ========== MORYTANIA (1600,-400) ==========
for(let i=0;i<3;i++){const rx=1550+Math.random()*100,rz=-450+Math.random()*80;if(canPlace(rx,rz,20)){ruin(rx,rz);markPlace(rx,rz,20)}}
tower(1600,-400,1.5);markPlace(1600,-400,28);makeEnterable(1600,-400,'tower','Morytania Tower');bonfire(1600,-400);

// ========== KARAMJA (-200,1800) ==========
hut(-230,1790,.3,1);markPlace(-230,1790,20);hut(-170,1810,-.5,1);markPlace(-170,1810,20);bonfire(-200,1800);

// ========== TROLLHEIM (-200,-3500) ==========
for(let i=0;i<3;i++){const rx=-250+Math.random()*100,rz=-3530+Math.random()*60;if(canPlace(rx,rz,20)){ruin(rx,rz);markPlace(rx,rz,20)}}
tower(-200,-3480,1.5);markPlace(-200,-3480,28);makeEnterable(-200,-3480,'tower','Trollheim Tower');bonfire(-200,-3500);

// ========== GOD WARS (0,-4500) ==========
for(let i=0;i<4;i++){const rx=-100+Math.random()*200,rz=-4550+Math.random()*100;if(canPlace(rx,rz,20)){ruin(rx,rz);markPlace(rx,rz,20)}}
tower(-50,-4500,2.5);markPlace(-50,-4500,36);makeEnterable(-50,-4500,'tower','God Wars Tower (Saradomin)');tower(50,-4500,2.5);markPlace(50,-4500,36);makeEnterable(50,-4500,'tower','God Wars Tower (Zamorak)');

// ========== DEEP WILDERNESS (0,-1800) ==========
for(let i=0;i<5;i++){const rx=-200+Math.random()*400,rz=-1900+Math.random()*200;if(canPlace(rx,rz,20)){ruin(rx,rz);markPlace(rx,rz,20)}}

// ========== SEERS VILLAGE (-800,-100) ==========
hut(-840,-110,.3,1);markPlace(-840,-110,20);hut(-770,-100,-.5,1);markPlace(-770,-100,20);tower(-820,-80,1.2);markPlace(-820,-80,28);makeEnterable(-820,-80,'tower','Seers Tower');bonfire(-800,-100);

// ========== RELLEKKA (-400,-3800) ==========
hut(-440,-3810,.3,1.2);markPlace(-440,-3810,24);hut(-370,-3800,-.5,1.2);markPlace(-370,-3800,24);bonfire(-400,-3800);

// ========== KELDAGRIM (-800,-3200) ==========
tower(-855,-3230,2);markPlace(-855,-3230,36);makeEnterable(-855,-3230,'tower','Keldagrim East Tower');tower(-740,-3230,2);markPlace(-740,-3230,36);makeEnterable(-740,-3230,'tower','Keldagrim West Tower');bonfire(-800,-3200);cave(-820,-3250,.2);

// ========== PRIFDDINAS (-4000,-300) ==========
cathedral(-4000,-300,0,1.5);markPlace(-4000,-300,70);bonfire(-4000,-300);makeEnterable(-4000,-300,'cathedral','Prifddinas Cathedral');

// ========== TZHAAR CITY (1800,1200) ==========
for(let i=0;i<3;i++){const lx=1760+Math.random()*80,lz=1160+Math.random()*80;const lv=new THREE.Mesh(new THREE.CircleGeometry(5,8),mt.lava);lv.rotation.x=-Math.PI/2;lv.position.set(lx,meshTerrainH(lx,lz)+.5,lz);scene.add(lv);torchPositions.push({x:lx,y:meshTerrainH(lx,lz)+3,z:lz,mesh:lv,ph:Math.random()*6.28,big:true,col:0xff3300})}
tower(1800,1200,1.8);markPlace(1800,1200,32);makeEnterable(1800,1200,'tower','TzHaar Tower');cave(1810,1180,.2);bonfire(1800,1200);

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

// === HARVESTABLE VEGETATION - Fruit Trees & Berry Bushes ===
// These spawn harvestable food items when player interacts with them
const harvestablePlants=[];// Store positions for gather interaction
function createAppleTree(x,z){const h=meshTerrainH(x,z);const g=new THREE.Group();
// Trunk
const trunk=new THREE.Mesh(new THREE.CylinderGeometry(.4,.7,5,6),new MS({color:0x5a4a3a,roughness:.9}));trunk.position.y=2.5;trunk.castShadow=true;g.add(trunk);
// Leaves canopy (rounded)
const canopy=new THREE.Mesh(new THREE.SphereGeometry(2.5,8,6),new MS({color:0x3a6a2a,roughness:.85}));canopy.position.y=5.5;canopy.scale.y=0.8;canopy.castShadow=true;g.add(canopy);
// Apples (red spheres in tree)
const appleMat=new MS({color:0xaa2020,roughness:.4});
for(let i=0;i<5;i++){const a=new THREE.Mesh(new THREE.SphereGeometry(.25,6,6),appleMat);const ang=i/5*Math.PI*2;a.position.set(Math.cos(ang)*1.5,4.5+Math.random()*2,Math.sin(ang)*1.5);g.add(a);}
g.position.set(x,h,z);scene.add(g);
harvestablePlants.push({x:x,z:z,y:h,type:'apple',mesh:g,item:'Apple',respawn:300});}
function createBerryBush(x,z,berryType='redberry'){const h=meshTerrainH(x,z);const g=new THREE.Group();
// Bush shape - multiple spheres
const bushMat=new MS({color:berryType==='redberry'?0x4a2a3a:berryType==='dwellberry'?0x3a2a4a:0x2a4a3a,roughness:.9});
for(let i=0;i<4;i++){const b=new THREE.Mesh(new THREE.SphereGeometry(.6+.3*Math.random(),6,6),bushMat);b.position.set((Math.random()-.5)*1.5,.6,(Math.random()-.5)*1.5);g.add(b);}
// Berries (small colored spheres)
const berryColor=berryType==='redberry'?0xcc1010:berryType==='dwellberry'?0x4422aa:berryType==='jangerberry'?0xff8800:0xaa2040;
const berryMat=new MS({color:berryColor,roughness:.3});
for(let i=0;i<8;i++){const b=new THREE.Mesh(new THREE.SphereGeometry(.12,5,5),berryMat);b.position.set((Math.random()-.5)*1.2,.8+Math.random()*.5,(Math.random()-.5)*1.2);g.add(b);}
g.position.set(x,h,z);g.scale.setScalar(1.2);scene.add(g);
const itemName=berryType==='redberry'?'Redberry':berryType==='dwellberry'?'Dwellberry':berryType==='jangerberry'?'Jangerberry':'Wildberry';
harvestablePlants.push({x:x,z:z,y:h,type:berryType,mesh:g,item:itemName,respawn:200});}
function createCropPatch(x,z,cropType='cabbage'){const h=meshTerrainH(x,z);const g=new THREE.Group();
// Crop rows
const cropMat=new MS({color:cropType==='cabbage'?0x4a6a3a:cropType==='potato'?0x5a5a40:cropType==='onion'?0x8a9a6a:0x6a5a3a,roughness:.9});
for(let row=0;row<3;row++){for(let col=0;col<3;col++){const c=new THREE.Mesh(new THREE.SphereGeometry(.25+.15*Math.random(),5,5),cropMat);c.position.set((col-1)*.6,.3,(row-1)*.6);c.scale.y=0.6;g.add(c);}}
g.position.set(x,h,z);scene.add(g);
const itemName=cropType==='cabbage'?'Cabbage':cropType==='potato'?'Potato':cropType==='onion'?'Onion':'Grain';
harvestablePlants.push({x:x,z:z,y:h,type:cropType,mesh:g,item:itemName,respawn:150});}
// Scatter harvestable vegetation across the world
{const plantLocs=[];
// Apple orchards near Lumbridge and cities
for(let i=0;i<80;i++){const ang=Math.random()*Math.PI*2;const dist=30+Math.random()*60;const ax=Math.cos(ang)*dist,az=Math.sin(ang)*dist;plantLocs.push({x:ax,z:az,type:'apple'});}
// Berry bushes NEAR SPAWN (Firelink Shrine area) for starting players
for(let i=0;i<15;i++){const ang=Math.random()*Math.PI*2;const dist=20+Math.random()*80;const bx=Math.cos(ang)*dist,bz=Math.sin(ang)*dist;plantLocs.push({x:bx,z:bz,type:'redberry'});}
for(let i=0;i<10;i++){const ang=Math.random()*Math.PI*2;const dist=30+Math.random()*100;const bx=Math.cos(ang)*dist,bz=Math.sin(ang)*dist;plantLocs.push({x:bx,z:bz,type:'dwellberry'});}
// More berry bushes in forests (distant)
for(let i=0;i<60;i++){const bx=(Math.random()-.5)*4000,bz=(Math.random()-.5)*4000;if(getReg(bx,bz).n==='Wilderness')continue;plantLocs.push({x:bx,z:bz,type:'redberry'});}
for(let i=0;i<40;i++){const bx=(Math.random()-.5)*3000,bz=(Math.random()-.5)*3000;if(getReg(bx,bz).n==='Wilderness')continue;plantLocs.push({x:bx,z:bz,type:'dwellberry'});}
for(let i=0;i<30;i++){const bx=(Math.random()-.5)*5000,bz=(Math.random()-.5)*5000;plantLocs.push({x:bx,z:bz,type:'jangerberry'});}
// Crop patches NEAR SPAWN
for(let i=0;i<12;i++){const ang=Math.random()*Math.PI*2;const dist=25+Math.random()*70;const cx=Math.cos(ang)*dist,cz=Math.sin(ang)*dist;plantLocs.push({x:cx,z:cz,type:'cabbage'});}
for(let i=0;i<8;i++){const ang=Math.random()*Math.PI*2;const dist=40+Math.random()*90;const cx=Math.cos(ang)*dist,cz=Math.sin(ang)*dist;plantLocs.push({x:cx,z:cz,type:'potato'});}
// More crop patches near farms (distant)
for(let i=0;i<50;i++){const cx=-200+Math.random()*400,cz=200+Math.random()*400;plantLocs.push({x:cx,z:cz,type:'cabbage'});}
for(let i=0;i<40;i++){const cx=-300+Math.random()*600,cz=-400+Math.random()*800;plantLocs.push({x:cx,z:cz,type:'potato'});}
// Create all plants
for(const p of plantLocs){if(isInLake(p.x,p.z))continue;const h=meshTerrainH(p.x,p.z);if(h>60||h<2)continue;
if(p.type==='apple')createAppleTree(p.x,p.z);
else if(p.type==='redberry'||p.type==='dwellberry'||p.type==='jangerberry')createBerryBush(p.x,p.z,p.type);
else createCropPatch(p.x,p.z,p.type);}}

// === GPU INSTANCED BUILDING ELEMENTS (reduces draw calls from thousands to ~10) ===
// These are populated during building generation instead of individual meshes
// _buildingInstancers is initialized in initBuildingInstancers()

// Initialize instanced meshes (created once, reused via matrix updates)
function initBuildingInstancers(){
_buildingInstancers={
// Chimneys (boxes)
chimneys:null,chimCount:0,CHIM_MAX:500,
// Windows with shutters
windows:null,winCount:0,WIN_MAX:800,
// Simple furniture (tables, stools)
furniture:null,furnCount:0,FURN_MAX:600,
// Flower boxes
flowerBoxes:null,boxCount:0,BOX_MAX:400,
// Roof details (small boxes)
roofDeets:null,roofCount:0,ROOF_MAX:600,
// Hay bales for barns
hayBales:null,hayCount:0,HAY_MAX:300,
// Ladder rungs (shared across buildings)
ladderRungs:null,rungCount:0,RUNG_MAX:1000,
// Torches on buildings
wallTorches:null,torchCount:0,WALLTORCH_MAX:400,
// Reset all counters for frame population
reset(){this.chimCount=0;this.winCount=0;this.furnCount=0;this.boxCount=0;this.roofCount=0;this.hayCount=0;this.rungCount=0;this.torchCount=0;},
// Finalize and add to scene
finalize(){
[this.chimneys,this.windows,this.furniture,this.flowerBoxes,this.roofDeets,this.hayBales,this.ladderRungs,this.wallTorches].forEach(inst=>{
if(inst&&inst.userData){inst.count=inst.userData.count||0;inst.instanceMatrix.needsUpdate=true;inst.frustumCulled=true;scene.add(inst);}});}
};
const b=_buildingInstancers;
// Chimneys - 2x2x8 boxes
const chimGeo=new THREE.BoxGeometry(2,8,2);
b.chimneys=new THREE.InstancedMesh(chimGeo,new MS({color:0x4a4a4a,roughness:.9}),b.CHIM_MAX);
b.chimneys.userData.count=0;
// Windows - 2x3x0.2 boxes with emissive
const winGeo=new THREE.BoxGeometry(2,3,.2);
b.windows=new THREE.InstancedMesh(winGeo,new MS({color:0x2a2a3a,emissive:0x1a1a2a,emissiveIntensity:.5}),b.WIN_MAX);
b.windows.userData.count=0;
// Furniture - simple cylinders for tables
const furnGeo=new THREE.CylinderGeometry(2,2,.2,8);
b.furniture=new THREE.InstancedMesh(furnGeo,new MS({color:0x4a3a2a,roughness:.9}),b.FURN_MAX);
b.furniture.userData.count=0;
// Flower boxes
const boxGeo=new THREE.BoxGeometry(2.5,.5,.8);
b.flowerBoxes=new THREE.InstancedMesh(boxGeo,new MS({color:0x3a5a2a,roughness:.9}),b.BOX_MAX);
b.flowerBoxes.userData.count=0;
// Roof details
const roofGeo=new THREE.BoxGeometry(1,1.5,1);
b.roofDeets=new THREE.InstancedMesh(roofGeo,new MS({color:0x3a3020}),b.ROOF_MAX);
b.roofDeets.userData.count=0;
// Hay bales
const hayGeo=new THREE.BoxGeometry(1.5,1,2);
b.hayBales=new THREE.InstancedMesh(hayGeo,new MS({color:0x9a8a3a}),b.HAY_MAX);
b.hayBales.userData.count=0;
// Ladder rungs
const rungGeo=new THREE.BoxGeometry(1,.1,.15);
b.ladderRungs=new THREE.InstancedMesh(rungGeo,mt.wd,b.RUNG_MAX);
b.ladderRungs.userData.count=0;
// Wall torches
const torchGeo=new THREE.CylinderGeometry(.3,.4,.8,6);
b.wallTorches=new THREE.InstancedMesh(torchGeo,mt.iron,b.WALLTORCH_MAX);
b.wallTorches.userData.count=0;}

// Helper to add instanced element
function addInstanced(type,matrix){
if(!_buildingInstancers)return;
const b=_buildingInstancers;
let inst,countProp,max;
if(type==='chimney'){inst=b.chimneys;countProp='chimCount';max=b.CHIM_MAX}
else if(type==='window'){inst=b.windows;countProp='winCount';max=b.WIN_MAX}
else if(type==='furniture'){inst=b.furniture;countProp='furnCount';max=b.FURN_MAX}
else if(type==='flowerBox'){inst=b.flowerBoxes;countProp='boxCount';max=b.BOX_MAX}
else if(type==='roof'){inst=b.roofDeets;countProp='roofCount';max=b.ROOF_MAX}
else if(type==='hay'){inst=b.hayBales;countProp='hayCount';max=b.HAY_MAX}
else if(type==='rung'){inst=b.ladderRungs;countProp='rungCount';max=b.RUNG_MAX}
else if(type==='wallTorch'){inst=b.wallTorches;countProp='torchCount';max=b.WALLTORCH_MAX}
else return;
if(b[countProp]<max){inst.setMatrixAt(b[countProp]++,matrix);inst.userData.count=b[countProp];}}

// === RURAL BUILDING SCATTER (Windmills, Barns, Watchtowers) ===
console.log('INIT: scattering rural buildings across countryside');
(function scatterRural(){
const ruralTypes=['windmill','barn','watchtower'];
const nRural=40; // Number of rural buildings to scatter
for(let i=0;i<nRural*3;i++){
const rx=(Math.random()-.5)*40000,rz=(Math.random()-.5)*35000;
// Skip lakes and city areas
if(isInLake(rx,rz))continue;
const rh=meshTerrainH(rx,rz);if(rh>90||rh<2)continue; // Avoid mountains and water
// Avoid city footprints
let tooClose=false;
for(const f of cityFootprints){if(Math.hypot(rx-f.x,rz-f.z)<f.r+80){tooClose=true;break}}
if(tooClose)continue;
const rType=ruralTypes[Math.floor(Math.random()*ruralTypes.length)];
const rSc=.8+Math.random()*.6;
const rFoot=rType==='windmill'?20*rSc:rType==='barn'?22*rSc:16*rSc;
if(!canPlace(rx,rz,rFoot))continue;
markPlace(rx,rz,rFoot);
const rRot=Math.random()*Math.PI*2;
// Place the building
if(rType==='windmill'){windmill(rx,rz,rRot,rSc)}
else if(rType==='barn'){barn(rx,rz,rRot,rSc)}
else if(rType==='watchtower'){watchtower(rx,rz,rRot,rSc)}}
})();

console.log('INIT: scatter done, starting procCity');
// === PROCEDURAL CITY GENERATION ===
function procCity(cx,cz,radius,density,style){
const bTypes=['house','shop','tavern','workshop','warehouse','manor','inn','forge','mansion','chapel'];
const nBuildings=Math.floor(density*radius/4);
// City walls — mark footprints along perimeter
const wallSegs=Math.floor(radius*2*Math.PI/30);
for(let i=0;i<wallSegs;i++){const a=i/wallSegs*Math.PI*2;
const wx=cx+Math.cos(a)*(radius+5),wz=cz+Math.sin(a)*(radius+5);
wall(wx,wz,16,18,a);markPlace(wx,wz,20)}
// Corner towers
for(let i=0;i<6;i++){const a=i/6*Math.PI*2;const tx=cx+Math.cos(a)*(radius+8),tz=cz+Math.sin(a)*(radius+8);tower(tx,tz,1.3);markPlace(tx,tz,28)}
// Gate arches
for(let i=0;i<4;i++){const a=i/4*Math.PI*2;const gx=cx+Math.cos(a)*(radius+5),gz=cz+Math.sin(a)*(radius+5);gothicArch(gx,gz,a,1);markPlace(gx,gz,16)}
// Streets
const streetMat=new MS({color:0x6a6a60,roughness:.95});
for(let i=0;i<4;i++){const a=i/4*Math.PI*2;const sLen=radius*1.8;
const st=new THREE.Mesh(new THREE.BoxGeometry(4,.1,sLen),streetMat);st.position.set(cx+Math.cos(a)*radius*.4,meshTerrainH(cx,cz)+.2,cz+Math.sin(a)*radius*.4);st.rotation.y=a;st.receiveShadow=true;scene.add(st)}
// Buildings with overlap prevention — keep away from walls
let placed=0;
for(let i=0;i<nBuildings*3&&placed<nBuildings;i++){
const a=Math.random()*Math.PI*2;const r=30+Math.random()*(radius-45);
const bx=cx+Math.cos(a)*r,bz=cz+Math.sin(a)*r;
if(isInLake(bx,bz))continue;
const bType=bTypes[Math.floor(Math.random()*bTypes.length)];
const sc=.7+Math.random()*.6;
let footprint=40*sc;
if(bType==='manor'||bType==='mansion')footprint=70*sc;
else if(bType==='warehouse')footprint=55*sc;
else if(bType==='inn'||bType==='forge')footprint=50*sc;
else if(bType==='chapel')footprint=45*sc;
if(!canPlace(bx,bz,footprint))continue;
markPlace(bx,bz,footprint);placed++;
const bRot=a+Math.PI+Math.random()*.4-.2;
if(bType==='house'||bType==='shop'){hut(bx,bz,bRot,sc);makeEnterable(bx,bz,bType==='shop'?'shop':'house',bType==='shop'?'Shop':'House',Math.max(10+8*sc,16)*sc*4);}
else if(bType==='tavern'){hut(bx,bz,bRot,sc*1.3);torch(bx+Math.cos(bRot)*8,bz+Math.sin(bRot)*8);makeEnterable(bx,bz,'tavern','Tavern',Math.max(10+8*sc,16)*sc*1.3*4);}
else if(bType==='workshop'){hut(bx,bz,bRot,sc*.9);makeEnterable(bx,bz,'shop','Workshop',Math.max(10+8*sc,16)*sc*.9*4);}
else if(bType==='warehouse'){const h=meshTerrainH(bx,bz);
const wseed=Math.abs(Math.sin(bx*41.3+bz*67.1)*43758.5453)%1;
const whW=(12+wseed*8)*sc,whH=(10+wseed*6)*sc,whD=(10+wseed*7)*sc;
const wCol=new THREE.Color().setHSL(.08+wseed*.04,.2+wseed*.15,.3+wseed*.12);
const wMat=new MS({color:wCol,roughness:.85});
const wh=new THREE.Mesh(new THREE.BoxGeometry(whW,whH,whD),wMat);wh.position.set(bx,h+whH/2,bz);wh.rotation.y=bRot;wh.castShadow=true;scene.add(wh);
const wrStyle=Math.floor(wseed*3);
if(wrStyle===0){const rf=new THREE.Mesh(new THREE.BoxGeometry(whW+2*sc,1*sc,whD+2*sc),mt.rf);rf.position.set(bx,h+whH+.5*sc,bz);rf.rotation.y=bRot;scene.add(rf)}
else if(wrStyle===1){const rf=new THREE.Mesh(new THREE.ConeGeometry(Math.max(whW,whD)*.6,5*sc,4),mt.rf);rf.position.set(bx,h+whH+2.5*sc,bz);rf.rotation.y=bRot+.785;scene.add(rf)}
else{const rfL=new THREE.Mesh(new THREE.BoxGeometry(whW+1*sc,whD*.55,.5*sc),mt.rf);rfL.position.set(bx,h+whH+whD*.18,bz+whD*.12);rfL.rotation.set(-.42,bRot,0);scene.add(rfL);
const rfR=rfL.clone();rfR.position.z=bz-whD*.12;rfR.rotation.x=.42;scene.add(rfR)}
// Warehouse door (large)
const wdoor=new THREE.Mesh(new THREE.BoxGeometry(3.5*sc,5*sc,.3*sc),new MS({color:0x3a2a18,roughness:.85}));
wdoor.position.set(bx+Math.cos(bRot)*whD/2,h+2.5*sc,bz+Math.sin(bRot)*whD/2);wdoor.rotation.y=bRot;scene.add(wdoor);
addCircleSolid(bx,bz,Math.max(whW,whD)/2+1,h,h+whH+1);makeEnterable(bx,bz,'house','Warehouse',Math.max(whW,whD)/2+5);}
else if(bType==='manor'){hut(bx,bz,bRot,sc*1.5);makeEnterable(bx,bz,'mansion','Manor',Math.max(10+8*sc,16)*sc*1.5*4);
for(let f=0;f<4;f++){const fa=bRot+f/4*Math.PI*2;const fx=bx+Math.cos(fa)*12*sc,fz=bz+Math.sin(fa)*12*sc;
const fence=new THREE.Mesh(new THREE.BoxGeometry(8*sc,3,.2),mt.wd);fence.position.set(fx,meshTerrainH(fx,fz)+1.5,fz);fence.rotation.y=fa;scene.add(fence)}}
else if(bType==='inn'){inn(bx,bz,bRot,sc);torch(bx+Math.cos(bRot)*10,bz+Math.sin(bRot)*10);torch(bx+Math.cos(bRot+Math.PI)*10,bz+Math.sin(bRot+Math.PI)*10);makeEnterable(bx,bz,'inn','Inn',20);}
else if(bType==='forge'){forge(bx,bz,bRot,sc);makeEnterable(bx,bz,'forge','Forge',20);}
else if(bType==='mansion'){mansion(bx,bz,bRot,sc);makeEnterable(bx,bz,'mansion','Mansion',30);}
else if(bType==='chapel'){chapel(bx,bz,bRot,sc);makeEnterable(bx,bz,'chapel','Chapel',25);}}
// Market square at center (reserve footprint)
markPlace(cx,cz,44);
for(let i=0;i<6;i++){const a=i/6*Math.PI*2;const sx=cx+Math.cos(a)*15,sz=cz+Math.sin(a)*15;
const sseed=Math.abs(Math.sin(sx*19.3+sz*37.7)*43758.5453)%1;
const sW=3+sseed*3,sH=2.5+sseed*2,sD=2.5+sseed*2;
const stall=new THREE.Mesh(new THREE.BoxGeometry(sW,sH,sD),mt.wd);stall.position.set(sx,meshTerrainH(sx,sz)+sH/2,sz);stall.rotation.y=a;scene.add(stall);addCircleSolid(sx,sz,Math.max(sW,sD)/2+1,meshTerrainH(sx,sz),meshTerrainH(sx,sz)+sH+2);
const canopy=new THREE.Mesh(new THREE.BoxGeometry(sW+1.5,.15,sD+1.5),new MS({color:[0x8a2020,0x203a8a,0x2a6a2a,0x8a6a20,0x6a2a6a,0x2a6a6a][i],roughness:.9}));canopy.position.set(sx,meshTerrainH(sx,sz)+sH+.8,sz);canopy.rotation.y=a;scene.add(canopy)}
const fountain=new THREE.Mesh(new THREE.CylinderGeometry(4,5,2,12),mt.st);fountain.position.set(cx,meshTerrainH(cx,cz)+1,cz);scene.add(fountain);addCircleSolid(cx,cz,5,meshTerrainH(cx,cz),meshTerrainH(cx,cz)+4);
const fWater=new THREE.Mesh(new THREE.CylinderGeometry(3.5,3.5,.5,12),mt.lakeMat);fWater.position.set(cx,meshTerrainH(cx,cz)+2.3,cz);scene.add(fWater);
bonfire(cx+20,cz+20);bonfire(cx-20,cz-20);
}

// === MASSIVE CASTLE GENERATOR ===
function castle(cx,cz,sc,rot){
sc=sc||1;rot=rot||0;const bY=meshTerrainH(cx,cz);const g=new THREE.Group();
addCircleSolid(cx,cz,125*sc,bY,bY+80*sc);
// --- OUTER CURTAIN WALL (huge perimeter) ---
const wallR=120*sc,wallH=40*sc,wallT=6*sc;
const wallSegs=20;
for(let i=0;i<wallSegs;i++){const a=i/wallSegs*Math.PI*2;const a2=(i+1)/wallSegs*Math.PI*2;
const wx=Math.cos(a)*wallR,wz=Math.sin(a)*wallR;
const segLen=wallR*2*Math.PI/wallSegs;
const wm=new THREE.Mesh(new THREE.BoxGeometry(segLen,wallH,wallT),mt.stGoth);
wm.position.set((Math.cos(a)+Math.cos(a2))/2*wallR,wallH/2,(Math.sin(a)+Math.sin(a2))/2*wallR);
wm.rotation.y=-(a+a2)/2+Math.PI/2;wm.castShadow=true;g.add(wm);
// Battlements on top
for(let b=0;b<3;b++){const bOff=(b-1)*segLen/3;
const merlon=new THREE.Mesh(new THREE.BoxGeometry(3*sc,4*sc,wallT+1),mt.stD);
merlon.position.set(wm.position.x+Math.cos(-(a+a2)/2+Math.PI/2)*bOff,wallH+2*sc,wm.position.z+Math.sin(-(a+a2)/2+Math.PI/2)*bOff);
merlon.rotation.y=wm.rotation.y;g.add(merlon)}}
// --- CORNER TOWERS (8 massive towers, each unique) ---
for(let i=0;i<8;i++){const a=i/8*Math.PI*2;const tx=Math.cos(a)*(wallR+4*sc),tz=Math.sin(a)*(wallR+4*sc);
const cseed=Math.abs(Math.sin(i*127.1+cx*31.7+cz*47.3)*43758.5453)%1;
const tH=(45+cseed*25)*sc;const tR=(9+cseed*4)*sc;const tTopR=(8+cseed*3)*sc;
const tSides=8+Math.floor(cseed*8);const cRoofStyle=Math.floor(cseed*3);
const tBase=new THREE.Mesh(new THREE.CylinderGeometry(tTopR,tR+2*sc,tH,tSides),mt.stGoth);tBase.position.set(tx,tH/2,tz);tBase.castShadow=true;g.add(tBase);
if(cRoofStyle===0){const tRoof=new THREE.Mesh(new THREE.ConeGeometry(tTopR+2*sc,(14+cseed*10)*sc,tSides),mt.rfSlate);tRoof.position.set(tx,tH+(7+cseed*5)*sc,tz);tRoof.castShadow=true;g.add(tRoof)}
else if(cRoofStyle===1){const dome=new THREE.Mesh(new THREE.SphereGeometry(tTopR+1*sc,tSides,8,0,Math.PI*2,0,Math.PI/2),mt.rfSlate);dome.position.set(tx,tH,tz);g.add(dome)}
else{const flatR=new THREE.Mesh(new THREE.CylinderGeometry(tTopR+1*sc,tTopR+1*sc,.8*sc,tSides),mt.stD);flatR.position.set(tx,tH+.4*sc,tz);g.add(flatR)}
const tFin=new THREE.Mesh(new THREE.SphereGeometry(1.2*sc,5,5),mt.gold);tFin.position.set(tx,tH+(cRoofStyle===0?(21+cseed*10):4)*sc,tz);g.add(tFin);
// Tower battlements
const nMer=tSides;
for(let b=0;b<nMer;b++){const ba=b/nMer*Math.PI*2;
const merlon=new THREE.Mesh(new THREE.BoxGeometry(2.5*sc,3.5*sc,2.5*sc),mt.stD);
merlon.position.set(tx+Math.cos(ba)*(tTopR+.5*sc),tH+2*sc,tz+Math.sin(ba)*(tTopR+.5*sc));g.add(merlon)}}
// --- KEEP (central massive tower) ---
const keepW=50*sc,keepD=40*sc,keepH=80*sc;
const keep=new THREE.Mesh(new THREE.BoxGeometry(keepW,keepH,keepD),mt.stGoth);keep.position.y=keepH/2;keep.castShadow=true;g.add(keep);
// Keep roof
const keepRoof=new THREE.Mesh(new THREE.BoxGeometry(keepW+6*sc,4*sc,keepD+6*sc),mt.rfSlate);keepRoof.position.y=keepH+2*sc;keepRoof.castShadow=true;g.add(keepRoof);
// Keep battlements
for(let i=0;i<12;i++){const bx=-keepW/2+i*keepW/11;
const m1=new THREE.Mesh(new THREE.BoxGeometry(3*sc,5*sc,3*sc),mt.stD);m1.position.set(bx,keepH+4.5*sc,keepD/2);m1.castShadow=true;g.add(m1);
const m2=m1.clone();m2.position.z=-keepD/2;g.add(m2)}
for(let i=0;i<8;i++){const bz=-keepD/2+i*keepD/7;
const m1=new THREE.Mesh(new THREE.BoxGeometry(3*sc,5*sc,3*sc),mt.stD);m1.position.set(keepW/2,keepH+4.5*sc,bz);g.add(m1);
const m2=m1.clone();m2.position.x=-keepW/2;g.add(m2)}
// Keep interior - floors and spiral stairs
const keepInnerW=keepW*.6,keepInnerD=keepD*.6;
for(let kl=1;kl<4;kl++){
const kflY=kl*20*sc;
const kFloor=new THREE.Mesh(new THREE.BoxGeometry(keepInnerW,1*sc,keepInnerD),new MS({color:0x4a3a2a,roughness:.9}));
kFloor.position.set(0,kflY,0);g.add(kFloor);
// Floor hole for stairs
const kHole=new THREE.Mesh(new THREE.BoxGeometry(keepInnerW*.3,1.2*sc,keepInnerD*.3),new MS({color:0x2a1a0a,roughness:1}));
kHole.position.set(0,kflY,0);g.add(kHole)}
// Spiral stairs in keep
const kStairR=Math.min(keepInnerW,keepInnerD)*.35;
const kNSteps=Math.floor(keepH/3);
for(let ks=0;ks<kNSteps;ks++){
const kang=ks*0.4;const ksy=5*sc+ks*3*sc;
const kstep=new THREE.Mesh(new THREE.BoxGeometry(2*sc,.5*sc,1*sc),new MS({color:0x5a4a3a,roughness:.85}));
kstep.position.set(Math.cos(kang)*kStairR,ksy,Math.sin(kang)*kStairR);kstep.rotation.y=kang;g.add(kstep)}
// Keep windows (rows of tall gothic windows)
for(let lv=0;lv<3;lv++){for(let i=0;i<6;i++){const wx=-keepW/2+keepW/(6+1)*(i+1);
const win=new THREE.Mesh(new THREE.BoxGeometry(2*sc,8*sc,.5),new MS({color:0x1a2a4a,emissive:0x0a1a3a,emissiveIntensity:.6,transparent:true,opacity:.5}));
win.position.set(wx,20*sc+lv*22*sc,keepD/2+.5);g.add(win);
const wFrame=new THREE.Mesh(new THREE.BoxGeometry(3*sc,9*sc,.3),mt.stD);wFrame.position.set(wx,20*sc+lv*22*sc,keepD/2+.7);g.add(wFrame)}}
// --- GATEHOUSE (front entrance with working portcullis) ---
const ghW=20*sc,ghH=35*sc,ghD=14*sc;
const ghL=new THREE.Mesh(new THREE.BoxGeometry(ghW/2-3*sc,ghH,ghD),mt.stGoth);ghL.position.set(-ghW/4-1.5*sc,ghH/2,wallR);ghL.castShadow=true;g.add(ghL);
const ghR=ghL.clone();ghR.position.x=ghW/4+1.5*sc;g.add(ghR);
// Portcullis arch
const ghArch=new THREE.Mesh(new THREE.BoxGeometry(7*sc,4*sc,ghD),mt.stD);ghArch.position.set(0,ghH-2*sc,wallR);g.add(ghArch);
// Working portcullis (iron gate that can be opened)
const portW=6*sc,portH=10*sc;
const portcullis=new THREE.Group();portcullis.position.set(0,portH/2,wallR);
// Portcullis grid
for(let pi=0;pi<5;pi++){
const vBar=new THREE.Mesh(new THREE.BoxGeometry(.3*sc,portH,.3*sc),mt.iron);vBar.position.set((pi-2)*1.2*sc,0,0);portcullis.add(vBar);
const hBar=new THREE.Mesh(new THREE.BoxGeometry(portW,.3*sc,.3*sc),mt.iron);hBar.position.set(0,(pi-2)*2*sc-portH*.2,0);portcullis.add(hBar)}
// Portcullis frame
const pFrame=new THREE.Mesh(new THREE.BoxGeometry(portW+.5*sc,.5*sc,.5*sc),mt.iron);pFrame.position.set(0,portH/2+.2*sc,0);portcullis.add(pFrame);
g.add(portcullis);
// Door entry for interaction
const cDoorW=5*sc,cDoorH=8*sc;
const cDoorPivot=new THREE.Group();cDoorPivot.position.set(-cDoorW/2,0,wallR);
const cDoorPanel=new THREE.Mesh(new THREE.BoxGeometry(cDoorW,cDoorH,.3*sc),new MS({color:0x3a2818,roughness:.85}));cDoorPanel.position.set(cDoorW/2,cDoorH/2,0);cDoorPanel.castShadow=true;cDoorPivot.add(cDoorPanel);
g.add(cDoorPivot);
doors.push({pivot:cDoorPivot,x:cx,z:cz+wallR,openAng:-Math.PI/2,cur:0});
// Gatehouse towers
[-1,1].forEach(s=>{const gt=new THREE.Mesh(new THREE.CylinderGeometry(7*sc,8*sc,ghH+10*sc,10),mt.stGoth);
gt.position.set(s*12*sc,(ghH+10*sc)/2,wallR);gt.castShadow=true;g.add(gt);
const gtRoof=new THREE.Mesh(new THREE.ConeGeometry(9*sc,14*sc,10),mt.rfSlate);gtRoof.position.set(s*12*sc,ghH+12*sc,wallR);g.add(gtRoof)});
// --- INNER COURTYARD FEATURES ---
// Great hall with interior
const hallW=36*sc,hallH=30*sc,hallD=60*sc;
const hall=new THREE.Mesh(new THREE.BoxGeometry(hallW,hallH,hallD),mt.stD);hall.position.set(0,hallH/2,-30*sc);hall.castShadow=true;g.add(hall);
const hallRoof=new THREE.Mesh(new THREE.BoxGeometry(hallW+4*sc,3*sc,hallD+4*sc),mt.rfSlate);hallRoof.position.set(0,hallH+1.5*sc,-30*sc);g.add(hallRoof);
// Hall door
const hDoorW=6*sc,hDoorH=8*sc;
const hDoorPivot=new THREE.Group();hDoorPivot.position.set(-hDoorW/2,0,-.5);
const hDoorPanel=new THREE.Mesh(new THREE.BoxGeometry(hDoorW,hDoorH,.3*sc),new MS({color:0x3a2818,roughness:.85}));hDoorPanel.position.set(hDoorW/2,hDoorH/2,0);hDoorPanel.castShadow=true;hDoorPivot.add(hDoorPanel);
hall.add(hDoorPivot);
doors.push({pivot:hDoorPivot,x:cx,z:cz-0.5,openAng:-Math.PI/2,cur:0});
// Hall interior floors
for(let hl=1;hl<3;hl++){
const hflY=hl*10*sc;
const hFloor=new THREE.Mesh(new THREE.BoxGeometry(hallW*.7,1*sc,hallD*.7),new MS({color:0x4a3a2a,roughness:.9}));
hFloor.position.set(0,hflY-hallH/2,0);hall.add(hFloor)}
// Chapel spire
const chapel=new THREE.Mesh(new THREE.BoxGeometry(16*sc,25*sc,20*sc),mt.st);chapel.position.set(40*sc,12.5*sc,-20*sc);chapel.castShadow=true;g.add(chapel);
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
markPlace(cx,cz,(wallR+20*sc)*2);
}

console.log('INIT: procCity defined, generating cities');
// Generate cities at major regions
procCity(0,0,80,1,'medieval');          // Lumbridge
procCity(555,50,70,1.2,'medieval');      // Varrock
procCity(-480,280,65,1,'white');        // Falador
procCity(-1200,100,70,1,'medieval');    // Ardougne

// === MASSIVE CASTLES ===
castle(900,-800,1.2,0);       // Eastern Fortress
makeEnterable(900,-800,'castle','Eastern Fortress',170);
castle(-2000,-500,1.5,.5);    // Western Stronghold
makeEnterable(-2000,-500,'castle','Western Stronghold',210);
castle(0,-1800,1.8,Math.PI/6);// Wilderness Castle (huge)
makeEnterable(0,-1800,'castle','Wilderness Castle',250);
castle(-800,600,1,-.3);       // Southern Keep
makeEnterable(-800,600,'castle','Southern Keep',150);
castle(1500,400,1.3,.8);      // Desert Citadel
makeEnterable(1500,400,'castle','Desert Citadel',190);

// === MINAS TIRITH CLIFFSIDE CASTLE ===
function minasTirith(cx,cz,sc){
sc=sc||1;const bY=meshTerrainH(cx,cz);const g=new THREE.Group();
const tiers=7;const baseR=180*sc;const tierH=35*sc;const totalH=tiers*tierH;
const cliffMat=new MS({color:0x9a9a90,roughness:.85,metalness:.05});
const whiteMat=new MS({color:0xd8d4c8,roughness:.65,metalness:.08});
const floorMat=new MS({color:0x8a8478,roughness:.9});
const winMat=new MS({color:0x1a2a4a,emissive:0x0a1a3a,emissiveIntensity:.4,transparent:true,opacity:.5});
const doorMat=new MS({color:0x3a2a18,roughness:.85});
// === CLIFF FACE (conical base) ===
const cliff=new THREE.Mesh(new THREE.CylinderGeometry(baseR*.15,baseR*1.1,totalH+40*sc,24),cliffMat);
cliff.position.y=(totalH+40*sc)/2-20*sc;cliff.castShadow=true;g.add(cliff);
addCircleSolid(cx,cz,baseR*1.15,bY,bY+totalH+80*sc);
// === TIERED CITY LEVELS ===
for(let t=0;t<tiers;t++){
const tierR=baseR*(1-t/tiers*.7);const tierY=t*tierH;
const nextR=baseR*(1-(t+1)/tiers*.7);
// Tier wall (outer ring)
const wallH=tierH*.8;const wallSegs=16+t*2;
for(let i=0;i<wallSegs;i++){const a=i/wallSegs*Math.PI*2;const a2=(i+1)/wallSegs*Math.PI*2;
const segLen=tierR*2*Math.PI/wallSegs;
const wm=new THREE.Mesh(new THREE.BoxGeometry(segLen,wallH,4*sc),whiteMat);
const mx=(Math.cos(a)+Math.cos(a2))/2*tierR;const mz=(Math.sin(a)+Math.sin(a2))/2*tierR;
wm.position.set(mx,tierY+wallH/2,mz);wm.rotation.y=-(a+a2)/2+Math.PI/2;wm.castShadow=true;g.add(wm);
// Battlements every other
if(i%2===0){const mer=new THREE.Mesh(new THREE.BoxGeometry(3*sc,3*sc,4.5*sc),whiteMat);
mer.position.set(mx,tierY+wallH+1.5*sc,mz);mer.rotation.y=wm.rotation.y;g.add(mer)}}
// Tier floor/platform
const tFloor=new THREE.Mesh(new THREE.CylinderGeometry(tierR*.95,tierR,2*sc,24),floorMat);
tFloor.position.y=tierY+1*sc;tFloor.receiveShadow=true;g.add(tFloor);
// Buildings on each tier (unique per tier)
const nBuildings=Math.max(2,6-t);
for(let b=0;b<nBuildings;b++){
const ba=b/nBuildings*Math.PI*2+t*.5;
const br=tierR*.55+Math.sin(ba*3+t)*(tierR*.2);
const bx=Math.cos(ba)*br,bz=Math.sin(ba)*br;
const bW=(8+Math.sin(b*7+t*13)*4)*sc;const bD=(6+Math.cos(b*11+t*7)*3)*sc;const bH=(8+t*2+Math.sin(b*3)*3)*sc;
const bld=new THREE.Mesh(new THREE.BoxGeometry(bW,bH,bD),whiteMat);
bld.position.set(bx,tierY+bH/2+2*sc,bz);bld.rotation.y=ba+Math.PI;bld.castShadow=true;g.add(bld);
// Roof
const roofType=Math.floor(Math.abs(Math.sin(bx*31+bz*17)*3));
if(roofType===0){const rf=new THREE.Mesh(new THREE.ConeGeometry(Math.max(bW,bD)*.6,5*sc,6),mt.rfSlate);rf.position.set(bx,tierY+bH+4.5*sc,bz);g.add(rf)}
else if(roofType===1){const rf=new THREE.Mesh(new THREE.BoxGeometry(bW+2*sc,1.5*sc,bD+2*sc),mt.rfSlate);rf.position.set(bx,tierY+bH+2.8*sc,bz);rf.rotation.y=ba;g.add(rf)}
else{const rf=new THREE.Mesh(new THREE.SphereGeometry(Math.max(bW,bD)*.45,8,6,0,Math.PI*2,0,Math.PI/2),mt.rfSlate);rf.position.set(bx,tierY+bH+2*sc,bz);g.add(rf)}
// Windows
const nWin=2+Math.floor(Math.abs(Math.sin(bx*7)*3));
for(let w=0;w<nWin;w++){const wa=ba+Math.PI+(w/(nWin-1||1)-.5)*.8;
const wx=bx+Math.cos(wa)*(bD/2+.2);const wz=bz+Math.sin(wa)*(bD/2+.2);
const win=new THREE.Mesh(new THREE.BoxGeometry(1.2*sc,2.5*sc,.2*sc),winMat);
win.position.set(wx,tierY+bH*.5+2*sc,wz);win.rotation.y=wa;g.add(win)}}
// Doorway on each tier (gate in wall)
{const ga=t/tiers*Math.PI*2+.5;
const gx=Math.cos(ga)*tierR;const gz=Math.sin(ga)*tierR;
const gateW=6*sc,gateH=10*sc;
const gL=new THREE.Mesh(new THREE.BoxGeometry(3*sc,gateH,5*sc),whiteMat);gL.position.set(gx-gateW*.4,tierY+gateH/2,gz);gL.rotation.y=ga;g.add(gL);
const gR=gL.clone();gR.position.set(gx+gateW*.4,tierY+gateH/2,gz);g.add(gR);
const gArch=new THREE.Mesh(new THREE.BoxGeometry(gateW+2*sc,2*sc,5*sc),whiteMat);gArch.position.set(gx,tierY+gateH+1*sc,gz);gArch.rotation.y=ga;g.add(gArch)}
// Tier torches
for(let ti=0;ti<4;ti++){const ta=ti/4*Math.PI*2+t*.7;const ttx=Math.cos(ta)*tierR*.7,ttz=Math.sin(ta)*tierR*.7;
const tPost=new THREE.Mesh(new THREE.CylinderGeometry(.3*sc,.4*sc,8*sc,5),mt.wd);tPost.position.set(ttx,tierY+5*sc,ttz);g.add(tPost);
const tFlm=new THREE.Mesh(new THREE.SphereGeometry(.8*sc,6,6),mt.fl);tFlm.position.set(ttx,tierY+10*sc,ttz);g.add(tFlm);
torchPositions.push({x:cx+ttx,y:bY+tierY+10*sc,z:cz+ttz,mesh:tFlm,ph:ti+t*4,big:true})}
}
// === WINDING PATH (spiral ramp up the cliff) ===
const rampW=8*sc;const rampSegs=tiers*16;
for(let i=0;i<rampSegs;i++){
const t=i/rampSegs;const a=t*tiers*Math.PI*2;
const r=baseR*(1-t*.55);const y=t*totalH;
const rx=Math.cos(a)*r,rz=Math.sin(a)*r;
const rLen=r*Math.PI*2/rampSegs*1.2;
const ramp=new THREE.Mesh(new THREE.BoxGeometry(rLen,1.5*sc,rampW),floorMat);
ramp.position.set(rx,y+.75*sc,rz);ramp.rotation.y=-a+Math.PI/2;ramp.receiveShadow=true;g.add(ramp);
// Path railing
if(i%3===0){const rail=new THREE.Mesh(new THREE.BoxGeometry(.5*sc,4*sc,.5*sc),whiteMat);
rail.position.set(rx+Math.cos(a+Math.PI/2)*rampW*.4,y+3*sc,rz+Math.sin(a+Math.PI/2)*rampW*.4);g.add(rail)}}
// === TOP TIER: THRONE ROOM & CORONATION COURT ===
const topY=tiers*tierH;const topR=baseR*.25;
// Throne room building
const thrW=30*sc,thrH=25*sc,thrD=20*sc;
const throne=new THREE.Mesh(new THREE.BoxGeometry(thrW,thrH,thrD),whiteMat);
throne.position.y=topY+thrH/2+2*sc;throne.castShadow=true;g.add(throne);
// Throne room interior floor
const thrFloor=new THREE.Mesh(new THREE.BoxGeometry(thrW-2*sc,.3*sc,thrD-2*sc),new MS({color:0x4a3828,roughness:.85}));
thrFloor.position.y=topY+2.2*sc;g.add(thrFloor);
// Throne chair
const chairBack=new THREE.Mesh(new THREE.BoxGeometry(4*sc,10*sc,1*sc),mt.gold);chairBack.position.set(0,topY+7*sc,-thrD/2+3*sc);g.add(chairBack);
const chairSeat=new THREE.Mesh(new THREE.BoxGeometry(4*sc,1*sc,3*sc),mt.gold);chairSeat.position.set(0,topY+4*sc,-thrD/2+4*sc);g.add(chairSeat);
// Throne room tall windows (gothic)
for(let w=0;w<4;w++){const wx=-thrW/2+thrW/5*(w+1);
const gWin=new THREE.Mesh(new THREE.BoxGeometry(2*sc,12*sc,.3*sc),winMat);gWin.position.set(wx,topY+12*sc,thrD/2+.3);g.add(gWin);
const gFrame=new THREE.Mesh(new THREE.BoxGeometry(2.8*sc,13*sc,.2*sc),whiteMat);gFrame.position.set(wx,topY+12*sc,thrD/2+.5);g.add(gFrame)}
// Grand entrance door to throne room
const thrDoorPivot=new THREE.Group();thrDoorPivot.position.set(-3*sc,topY+2*sc,thrD/2);
const thrDoorP=new THREE.Mesh(new THREE.BoxGeometry(6*sc,12*sc,.4*sc),doorMat);thrDoorP.position.set(3*sc,6*sc,0);thrDoorP.castShadow=true;thrDoorPivot.add(thrDoorP);
// Door iron bands
for(let bi=0;bi<4;bi++){const bb=new THREE.Mesh(new THREE.BoxGeometry(5.5*sc,.2*sc,.45*sc),mt.armorDk);bb.position.set(3*sc,2*sc+bi*3*sc,0);thrDoorPivot.add(bb)}
g.add(thrDoorPivot);
doors.push({pivot:thrDoorPivot,x:cx,z:cz+thrD/2,openAng:-Math.PI/2,cur:0});
// Throne room roof (peaked)
const thrRoof=new THREE.Mesh(new THREE.ConeGeometry(thrW*.7,12*sc,4),mt.rfSlate);thrRoof.position.y=topY+thrH+8*sc;thrRoof.rotation.y=Math.PI/4;thrRoof.castShadow=true;g.add(thrRoof);
// === CORONATION COURTYARD (the famous LOTR promontory) ===
const promLen=60*sc;const promW=16*sc;
const prom=new THREE.Mesh(new THREE.BoxGeometry(promW,4*sc,promLen),whiteMat);
prom.position.set(0,topY,thrD/2+promLen/2);prom.castShadow=true;g.add(prom);
// Side railings on promontory
[-1,1].forEach(sd=>{for(let p=0;p<8;p++){
const pz=thrD/2+5*sc+p*(promLen-10*sc)/7;
const post=new THREE.Mesh(new THREE.CylinderGeometry(.3*sc,.4*sc,5*sc,5),whiteMat);
post.position.set(sd*promW/2,topY+3.5*sc,pz);g.add(post)}
const rail=new THREE.Mesh(new THREE.BoxGeometry(.4*sc,1*sc,promLen-4*sc),whiteMat);
rail.position.set(sd*promW/2,topY+5.5*sc,thrD/2+promLen/2);g.add(rail)});
// White Tree of Gondor (dead tree at promontory)
const treeY=topY+4*sc;
const treeTrunk=new THREE.Mesh(new THREE.CylinderGeometry(.5*sc,1.2*sc,14*sc,6),new MS({color:0xd8d0c0,roughness:.8}));
treeTrunk.position.set(0,treeY+7*sc,thrD/2+promLen-15*sc);g.add(treeTrunk);
for(let b=0;b<6;b++){const ba=b/6*Math.PI*2;
const branch=new THREE.Mesh(new THREE.CylinderGeometry(.1*sc,.25*sc,5*sc,4),new MS({color:0xc8c0b0,roughness:.85}));
branch.position.set(Math.cos(ba)*1.5*sc,treeY+10*sc+b*1.5*sc,thrD/2+promLen-15*sc+Math.sin(ba)*1.5*sc);
branch.rotation.set(Math.sin(ba)*.5,ba,.4+b*.1);g.add(branch)}
// Spire above throne (citadel tower)
const spireH=60*sc;
const spire=new THREE.Mesh(new THREE.CylinderGeometry(3*sc,8*sc,spireH,10),whiteMat);
spire.position.y=topY+thrH+spireH/2;spire.castShadow=true;g.add(spire);
const spireRoof=new THREE.Mesh(new THREE.ConeGeometry(4*sc,15*sc,10),mt.rfSlate);
spireRoof.position.y=topY+thrH+spireH+7.5*sc;g.add(spireRoof);
const beacon=new THREE.Mesh(new THREE.SphereGeometry(2*sc,8,8),mt.fl);
beacon.position.y=topY+thrH+spireH+16*sc;g.add(beacon);
torchPositions.push({x:cx,y:bY+topY+thrH+spireH+16*sc,z:cz,mesh:beacon,ph:0,big:true});
// Place the whole structure
g.position.set(cx,bY,cz);scene.add(g);
markPlace(cx,cz,(baseR+20*sc)*2);
log('Minas Tirith loaded','#ffd700');
}
// Spawn Minas Tirith
minasTirith(-1500,2000,1);

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

// === ADVENTURER'S GUILD HALL (Spawn Hub at 0,5) — Welcoming Courtyard ===
const fH=meshTerrainH(0,5);
// Main courtyard - octagonal paved plaza
const plazaR=35;
const plaza=new THREE.Mesh(new THREE.CylinderGeometry(plazaR,plazaR+2,2,8),mt.st);plaza.position.set(0,fH+1,5);plaza.receiveShadow=true;scene.add(plaza);
// Patterned center circle
const plazaCenter=new THREE.Mesh(new THREE.CylinderGeometry(15,15,2.2,16),new MS({color:0x6a5a4a,roughness:.8}));plazaCenter.position.set(0,fH+1.1,5);scene.add(plazaCenter);
// Decorative ring inlay
const plazaRing=new THREE.Mesh(new THREE.TorusGeometry(12,.8,8,32),new MS({color:0x8a7a6a,roughness:.9}));plazaRing.rotation.x=-Math.PI/2;plazaRing.position.set(0,fH+2.2,5);scene.add(plazaRing);
// Guild Hall building (front entrance)
const hallW=30,hallD=20,hallH=18;
const guildHall=new THREE.Mesh(new THREE.BoxGeometry(hallW,hallH,hallD),mt.stGoth);guildHall.position.set(0,fH+hallH/2,5-25);guildHall.castShadow=true;scene.add(guildHall);
// Hall roof (peaked)
const hallRoof=new THREE.Mesh(new THREE.ConeGeometry(hallW*.7,10,4),mt.rfSlate);hallRoof.position.set(0,fH+hallH+5,5-25);hallRoof.rotation.y=Math.PI/4;hallRoof.castShadow=true;scene.add(hallRoof);
// Grand entrance archway
const archW=12,archH=14;
const archFrame=new THREE.Mesh(new THREE.BoxGeometry(archW,archH,4),mt.st);archFrame.position.set(0,fH+archH/2,5-11);scene.add(archFrame);
// Open doorway (negative space visual)
const doorway=new THREE.Mesh(new THREE.BoxGeometry(8,10,4.2),new MS({color:0x1a1510,roughness:1}));doorway.position.set(0,fH+5,5-11);scene.add(doorway);
// Wooden double doors (open)
[-1,1].forEach(s=>{
const doorPanel=new THREE.Mesh(new THREE.BoxGeometry(3.5,9,.3),mt.wd);doorPanel.position.set(s*4,fH+5,5-8.5);doorPanel.rotation.y=s*.5;scene.add(doorPanel);});
// Guild banner/sign
const signY=fH+hallH+2;
const signBoard=new THREE.Mesh(new THREE.BoxGeometry(16,4,1),mt.wd);signBoard.position.set(0,signY,5-34);scene.add(signBoard);
// Pillars framing the entrance (4 symmetrical columns)
[[-12,-12],[12,-12],[-12,12],[12,12]].forEach(([px,pz])=>{
const pillar=new THREE.Mesh(new THREE.CylinderGeometry(1.2,1.5,14,8),mt.stGoth);pillar.position.set(px,fH+8,5+pz);pillar.castShadow=true;scene.add(pillar);
const pCapital=new THREE.Mesh(new THREE.BoxGeometry(3,1.8,3),mt.st);pCapital.position.set(px,fH+15.5,5+pz);scene.add(pCapital);});
// Central Bonfire Altar - welcoming spawn point
const altarBase=new THREE.Mesh(new THREE.CylinderGeometry(5,6,3,8),mt.st);altarBase.position.set(0,fH+1.5,5);scene.add(altarBase);
const altar=new THREE.Mesh(new THREE.CylinderGeometry(3.5,3.5,1.5,8),new MS({color:0x5a4a3a,roughness:.9}));altar.position.set(0,fH+3.5,5);scene.add(altar);
// The bonfire (player spawn/respawn point)
const bonfireLogs=new THREE.Mesh(new THREE.CylinderGeometry(2,2.2,1.5,6),mt.wd);bonfireLogs.position.set(0,fH+4.2,5);scene.add(bonfireLogs);
const bfFlame=new THREE.Mesh(new THREE.SphereGeometry(2.5,12,12),mt.fl);bfFlame.position.set(0,fH+6,5);scene.add(bfFlame);
const bfCore=new THREE.Mesh(new THREE.SphereGeometry(1.5,8,8),mt.flEmber);bfCore.position.set(0,fH+5.5,5);scene.add(bfCore);
torchPositions.push({x:0,y:fH+8,z:5,mesh:bfFlame,ph:0,big:true});
// Animated embers around bonfire
for(let i=0;i<6;i++){const ember=new THREE.Mesh(new THREE.SphereGeometry(.3,4,4),mt.flEmber);
const ang=i/6*Math.PI*2;ember.position.set(Math.cos(ang)*2.5,fH+5+Math.random(),5+Math.sin(ang)*2.5);scene.add(ember);}
// Training dummies (for new players to practice)
[[-20,15],[20,15]].forEach(([dx,dz])=>{
const dummyBase=new THREE.Mesh(new THREE.CylinderGeometry(1.5,2,1,6),mt.st);dummyBase.position.set(dx,fH+.5,5+dz);scene.add(dummyBase);
const dummyPost=new THREE.Mesh(new THREE.CylinderGeometry(.4,.5,8,6),mt.wd);dummyPost.position.set(dx,fH+4.5,5+dz);scene.add(dummyPost);
const dummyBody=new THREE.Mesh(new THREE.CylinderGeometry(1.8,1.5,4,8),new MS({color:0x8a7a5a,roughness:.9}));dummyBody.position.set(dx,fH+8,5+dz);scene.add(dummyBody);
const dummyHead=new THREE.Mesh(new THREE.SphereGeometry(1.2,8,8),new MS({color:0x9a8a6a,roughness:.9}));dummyHead.position.set(dx,fH+11,5+dz);scene.add(dummyHead);
// Target circle painted on ground
const targetRing=new THREE.Mesh(new THREE.RingGeometry(3,3.2,32),new MS({color:0xaa4444}));targetRing.rotation.x=-Math.PI/2;targetRing.position.set(dx,fH+.05,5+dz);scene.add(targetRing);});
// Weapon racks along sides
[-1,1].forEach(s=>{
const rack=new THREE.Mesh(new THREE.BoxGeometry(1,6,8),mt.wd);rack.position.set(s*28,fH+4,5-5);rack.castShadow=true;scene.add(rack);
for(let i=0;i<4;i++){
const weapon=new THREE.Mesh(new THREE.BoxGeometry(.2,3,.1),mt.armorLt);weapon.position.set(s*28+.6,fH+5+i*.5,5-8+i*2);weapon.rotation.z=s*.3;weapon.rotation.x=.2;scene.add(weapon);}});
// Info signposts
[[-25,0],[25,0]].forEach(([sx,sz])=>{
const post=new THREE.Mesh(new THREE.CylinderGeometry(.3,.3,5,6),mt.wd);post.position.set(sx,fH+2.5,5+sz);scene.add(post);
const sign=new THREE.Mesh(new THREE.BoxGeometry(4,3,.2),mt.wd);sign.position.set(sx,fH+5,5+sz);sign.rotation.y=sx>0?-.3:.3;scene.add(sign);});
// Lantern posts around perimeter (8 lanterns)
for(let i=0;i<8;i++){const ang=i/8*Math.PI*2;
const lx=Math.cos(ang)*30,lz=Math.sin(ang)*30;
const lPost=new THREE.Mesh(new THREE.CylinderGeometry(.3,.4,8,6),mt.iron);lPost.position.set(lx,fH+5,5+lz);scene.add(lPost);
const lantern=new THREE.Mesh(new THREE.BoxGeometry(1.2,1.5,1.2),mt.iron);lantern.position.set(lx,fH+9,5+lz);scene.add(lantern);
const lGlass=new THREE.Mesh(new THREE.SphereGeometry(.6,6,6),new MS({color:0xffaa44,emissive:0xff8800,emissiveIntensity:1.5}));lGlass.position.set(lx,fH+9,5+lz);scene.add(lGlass);
torchPositions.push({x:lx,y:fH+10,z:5+lz,mesh:lGlass,ph:i,big:false});}
// Decorative planters with flowers
[[-15,-15],[15,-15],[-15,20],[15,20]].forEach(([px,pz])=>{
const planter=new THREE.Mesh(new THREE.BoxGeometry(4,2,4),mt.st);planter.position.set(px,fH+1,5+pz);scene.add(planter);
const bush=new THREE.Mesh(new THREE.SphereGeometry(2,6,6),mt.lf);bush.position.set(px,fH+3,5+pz);scene.add(bush);});
// Welcome mat text area (visual only - different colored stones)
for(let i=0;i<5;i++){const stone=new THREE.Mesh(new THREE.BoxGeometry(2,.3,1),new MS({color:0x7a6a5a}));
stone.position.set(-4+i*2,fH+2.2,5+18);scene.add(stone);}
// Register Guild Hall solids
addSolid(plaza);addSolid(guildHall);addSolid(archFrame);addSolid(altarBase);addSolid(altar);

// === DUNGEON SYSTEM ===
console.log('INIT: cities+waterfalls+caves+bones done, starting dungeons');
const bossTypes={demon:{hp:500,dmg:35,col:0x8a1010,name:'Infernal Lord'},golem:{hp:600,dmg:30,col:0x5a5a60,name:'Ancient Golem'},wyrm:{hp:450,dmg:40,col:0x4a2050,name:'Shadow Wyrm'},tzhaar:{hp:700,dmg:45,col:0xaa4010,name:'TzTok-Xil'},vampire:{hp:400,dmg:35,col:0x3a0a1a,name:'Blood Count'},elf:{hp:350,dmg:50,col:0x4a6a5a,name:'Crystal Guardian'},
dragon:{hp:800,dmg:50,col:0x2a6a1a,name:'King Black Dragon'},hydra:{hp:900,dmg:55,col:0x4a6a3a,name:'Alchemical Hydra'},kraken:{hp:650,dmg:40,col:0x1a3a5a,name:'Cave Kraken'},cerberus:{hp:750,dmg:60,col:0x5a1a1a,name:'Cerberus'},vorkath:{hp:1000,dmg:65,col:0x2a5a6a,name:'Vorkath'},nightmare:{hp:1200,dmg:70,col:0x2a1a3a,name:'The Nightmare'},nex:{hp:1500,dmg:80,col:0x4a0a3a,name:'Nex'},jad:{hp:850,dmg:55,col:0x8a2a00,name:'TzTok-Jad'},zuk:{hp:2000,dmg:90,col:0xaa3a10,name:'TzKal-Zuk'}};
const specialLoot=[
// ===== WEAPONS — RUNESCAPE (pig latin) =====
{name:'Agondray Ongswordlay',atk:45,def:5,str:30,slot:'Weapon',rarity:'rare'},
{name:'Abyssalay Ipwhay',atk:55,def:0,str:40,slot:'Weapon',rarity:'rare'},
{name:'Agondray Imitarscay',atk:40,def:3,str:28,slot:'Weapon',rarity:'rare'},
{name:'Odswordgay (Armadylway)',atk:75,def:5,str:55,slot:'Weapon',rarity:'legendary'},
{name:'Odswordgay (Andosbay)',atk:70,def:5,str:65,slot:'Weapon',rarity:'legendary'},
{name:'Odswordgay (Aradominsay)',atk:72,def:10,str:50,slot:'Weapon',rarity:'legendary'},
{name:'Odswordgay (Amorakzay)',atk:78,def:3,str:58,slot:'Weapon',rarity:'legendary'},
{name:'Ythescay ofway Iturvay',atk:90,def:0,str:70,slot:'Weapon',rarity:'mythic'},
{name:'Istedtway Owbay',atk:85,def:0,str:60,slot:'Weapon',rarity:'mythic'},
{name:'Azighray Apierray',atk:65,def:0,str:50,slot:'Weapon',rarity:'legendary'},
{name:'Adeblay ofway Aeldorsay',atk:62,def:5,str:48,slot:'Weapon',rarity:'legendary'},
{name:'Inquisitorway Acemay',atk:60,def:0,str:55,slot:'Weapon',rarity:'legendary'},
{name:'Ightmarenay Affstay',atk:55,def:5,str:35,slot:'Weapon',rarity:'legendary'},
{name:'Identtray ofway ethay Ampsway',atk:50,def:3,str:30,slot:'Weapon',rarity:'rare'},
{name:'Oxictay Owpipeblay',atk:48,def:0,str:35,slot:'Weapon',rarity:'rare'},
{name:'Agondray Awsclay',atk:52,def:5,str:42,slot:'Weapon',rarity:'rare'},
{name:'Elderway Aulmay',atk:58,def:0,str:60,slot:'Weapon',rarity:'legendary'},
{name:'Arytezay Ossbowcray',atk:80,def:0,str:55,slot:'Weapon',rarity:'mythic'},
{name:'Aplemay Owbay',atk:20,def:0,str:15,slot:'Weapon',rarity:'common'},
{name:'Oakway Owbay',atk:12,def:0,str:8,slot:'Weapon',rarity:'common'},
{name:'Wilowway Owbay',atk:18,def:0,str:12,slot:'Weapon',rarity:'uncommon'},
{name:'Apablemay Owbay',atk:35,def:0,str:25,slot:'Weapon',rarity:'rare'},
{name:'Iverway Owbay',atk:55,def:0,str:40,slot:'Weapon',rarity:'rare'},
{name:'Agicmay Ilfay Ossbowlay',atk:65,def:0,str:50,slot:'Weapon',rarity:'rare'},
{name:'Umekentay Adowshay',atk:95,def:0,str:75,slot:'Weapon',rarity:'mythic'},
{name:'Uneray Imitarscay',atk:42,def:2,str:25,slot:'Weapon',rarity:'rare'},
{name:'Ithrilmay Alberdahay',atk:35,def:4,str:22,slot:'Weapon',rarity:'rare'},
{name:'Anicday Axeway',atk:68,def:3,str:52,slot:'Weapon',rarity:'legendary'},
// ===== WEAPONS — DARK SOULS (pig latin) =====
{name:'Aysclay Oreymay Eatswordsay',atk:98,def:8,str:80,slot:'Weapon',rarity:'mythic'},
{name:'Oonlightmay Eatswordsay',atk:88,def:5,str:65,slot:'Weapon',rarity:'mythic'},
{name:'Arkday Oonmay Eatswordsay',atk:82,def:3,str:60,slot:'Weapon',rarity:'legendary'},
{name:'Ackblay Ightknight Eatswordsay',atk:70,def:5,str:55,slot:'Weapon',rarity:'legendary'},
{name:'Ukesday Ordssway ofway Osscray Ightknight',atk:65,def:8,str:50,slot:'Weapon',rarity:'legendary'},
{name:'Assdway Aithfurlssay Ordssway',atk:60,def:3,str:48,slot:'Weapon',rarity:'rare'},
{name:'Oldway Acedmay Ordssway',atk:92,def:0,str:72,slot:'Weapon',rarity:'mythic'},
{name:'Avelinsay Ordssway Earspay',atk:58,def:5,str:45,slot:'Weapon',rarity:'rare'},
{name:'Uttingpay Ordssway Urbancay Urvecay',atk:56,def:0,str:48,slot:'Weapon',rarity:'rare'},
{name:'Ingedray Ightknight Ordssway',atk:50,def:8,str:40,slot:'Weapon',rarity:'rare'},
{name:'Assdday Orkfay Aitsay',atk:45,def:3,str:35,slot:'Weapon',rarity:'rare'},
{name:'Aymoreway Ansientray Ordssway',atk:75,def:0,str:58,slot:'Weapon',rarity:'legendary'},
{name:'Ormsstay Urvecay Eatswordsay',atk:72,def:5,str:55,slot:'Weapon',rarity:'legendary'},
{name:'Anelessday Ordssway Aikenfray',atk:68,def:0,str:50,slot:'Weapon',rarity:'legendary'},
{name:'Uqueendayway Assway',atk:55,def:15,str:40,slot:'Weapon',rarity:'rare'},
// ===== HELMS — RUNESCAPE (pig latin) =====
{name:'Agondray Ullfay Elmhay',atk:3,def:35,str:5,slot:'Helm',rarity:'rare'},
{name:'Orvatay Ullfay Elmhay',atk:5,def:55,str:10,slot:'Helm',rarity:'mythic'},
{name:'Eitiznotnay Aceguardfay',atk:8,def:40,str:12,slot:'Helm',rarity:'legendary'},
{name:'Erpentinesay Elmhay',atk:3,def:45,str:8,slot:'Helm',rarity:'rare'},
{name:'Usticiarjay Aceguardfay',atk:0,def:50,str:3,slot:'Helm',rarity:'legendary'},
{name:'Ancestralway Athay',atk:25,def:8,str:0,slot:'Helm',rarity:'legendary'},
{name:'Ayerslay Elmhay (i)',atk:12,def:30,str:10,slot:'Helm',rarity:'rare'},
// ===== HELMS — DARK SOULS (pig latin) =====
{name:'Avelsay Elmhay ofway Enway',atk:10,def:42,str:8,slot:'Helm',rarity:'legendary'},
{name:'Ornsteinway Elmhay',atk:6,def:48,str:12,slot:'Helm',rarity:'legendary'},
{name:'Avel Ordlay Ownscray',atk:15,def:55,str:5,slot:'Helm',rarity:'mythic'},
{name:'Atcherwayay Elmhay',atk:5,def:38,str:6,slot:'Helm',rarity:'rare'},
{name:'Arfaronway Etshay',atk:8,def:44,str:10,slot:'Helm',rarity:'legendary'},
{name:'Assway Ookflay Oodshay',atk:20,def:20,str:15,slot:'Helm',rarity:'rare'},
// ===== CHEST — RUNESCAPE (pig latin) =====
{name:'Andosbay Estplatechay',atk:5,def:45,str:15,slot:'Chest',rarity:'rare'},
{name:'Ancestralway Oberay Optay',atk:30,def:10,str:0,slot:'Chest',rarity:'legendary'},
{name:'Orvatay Atebodyplay',atk:8,def:65,str:15,slot:'Chest',rarity:'mythic'},
{name:'Usticiarjay Estguardchay',atk:0,def:60,str:5,slot:'Chest',rarity:'legendary'},
{name:'Inquisitorway Auberkhay',atk:10,def:50,str:18,slot:'Chest',rarity:'legendary'},
{name:'Ystalcray Odybay',atk:20,def:35,str:8,slot:'Chest',rarity:'rare'},
{name:'Arilkay Eathertopplay',atk:18,def:30,str:5,slot:'Chest',rarity:'rare'},
{name:'Armadylway Estplatechay',atk:15,def:42,str:8,slot:'Chest',rarity:'rare'},
// ===== CHEST — DARK SOULS (pig latin) =====
{name:'Avelsay Armoray ofway Enway',atk:8,def:58,str:12,slot:'Chest',rarity:'legendary'},
{name:'Ornsteinway Armoray',atk:12,def:62,str:10,slot:'Chest',rarity:'mythic'},
{name:'Ackblay Ironway Etshay',atk:5,def:52,str:15,slot:'Chest',rarity:'legendary'},
{name:'Aintssay Estvestchay',atk:0,def:48,str:20,slot:'Chest',rarity:'rare'},
{name:'Avorsway Armoray',atk:10,def:55,str:14,slot:'Chest',rarity:'legendary'},
{name:'Ilverbay Ightknight Armoray',atk:6,def:50,str:12,slot:'Chest',rarity:'rare'},
// ===== LEGS — RUNESCAPE (pig latin) =====
{name:'Armadylway Ainskirtchay',atk:5,def:40,str:10,slot:'Legs',rarity:'rare'},
{name:'Orvatay Ateleggsplay',atk:5,def:58,str:12,slot:'Legs',rarity:'mythic'},
{name:'Andosbay Assetstay',atk:4,def:42,str:14,slot:'Legs',rarity:'rare'},
{name:'Usticiarjay Egguardslay',atk:0,def:55,str:3,slot:'Legs',rarity:'legendary'},
{name:'Ancestralway Oberay Ottombay',atk:25,def:8,str:0,slot:'Legs',rarity:'legendary'},
{name:'Agondray Ateleggsplay',atk:3,def:35,str:5,slot:'Legs',rarity:'rare'},
// ===== LEGS — DARK SOULS (pig latin) =====
{name:'Avelsay Eggingslay ofway Enway',atk:4,def:45,str:8,slot:'Legs',rarity:'legendary'},
{name:'Ornsteinway Eggingslay',atk:6,def:52,str:10,slot:'Legs',rarity:'legendary'},
{name:'Ackblay Ironway Eggingslay',atk:3,def:48,str:12,slot:'Legs',rarity:'rare'},
{name:'Averway Ardsguay',atk:2,def:40,str:8,slot:'Legs',rarity:'rare'},
// ===== SHIELDS — RUNESCAPE (pig latin) =====
{name:'Agonfiredray Ieldshay',atk:5,def:50,str:5,slot:'Shield',rarity:'legendary'},
{name:'Avernicway Efenderdray',atk:18,def:35,str:12,slot:'Shield',rarity:'legendary'},
{name:'Elysianway Iritspay Ieldshay',atk:0,def:65,str:0,slot:'Shield',rarity:'mythic'},
{name:'Arcaneway Iritspay Ieldshay',atk:25,def:40,str:0,slot:'Shield',rarity:'mythic'},
{name:'Ectralspay Iritspay Ieldshay',atk:15,def:45,str:0,slot:'Shield',rarity:'legendary'},
{name:'Ystalcray Ieldshay',atk:5,def:38,str:3,slot:'Shield',rarity:'rare'},
// ===== SHIELDS — DARK SOULS (pig latin) =====
{name:'Assway Ieldshay ofway Anterway',atk:0,def:60,str:0,slot:'Shield',rarity:'legendary'},
{name:'Assiesgray Eatshieldgray',atk:5,def:55,str:5,slot:'Shield',rarity:'legendary'},
{name:'Ilverbay Ightknight Ieldshay',atk:3,def:48,str:3,slot:'Shield',rarity:'rare'},
{name:'Eidhay Ieldshay',atk:0,def:70,str:0,slot:'Shield',rarity:'mythic'},
{name:'Olfiray Esttray',atk:8,def:42,str:8,slot:'Shield',rarity:'rare'},
// ===== BOOTS — RUNESCAPE (pig latin) =====
{name:'Imordialspray Ootsbay',atk:2,def:25,str:10,slot:'Boots',rarity:'rare'},
{name:'Egasianpay Ootsbay',atk:12,def:18,str:5,slot:'Boots',rarity:'rare'},
{name:'Eternaway Ootsbay',atk:18,def:10,str:0,slot:'Boots',rarity:'rare'},
{name:'Agondray Ootsbay',atk:2,def:20,str:8,slot:'Boots',rarity:'rare'},
{name:'Uardiansgay Ootsbay',atk:0,def:28,str:3,slot:'Boots',rarity:'legendary'},
// ===== BOOTS — DARK SOULS (pig latin) =====
{name:'Avelsay Ootsbay ofway Enway',atk:3,def:30,str:8,slot:'Boots',rarity:'legendary'},
{name:'Ornsteinway Ootsbay',atk:5,def:32,str:10,slot:'Boots',rarity:'legendary'},
{name:'Avel Ordlay Appersway',atk:8,def:25,str:5,slot:'Boots',rarity:'rare'},
{name:'Ironway Eadstray',atk:2,def:22,str:6,slot:'Boots',rarity:'rare'},
// ===== GLOVES — RUNESCAPE (pig latin) =====
{name:'Arrowsbay Ovesglay',atk:10,def:15,str:10,slot:'Gloves',rarity:'rare'},
{name:'Erociousfay Ovesglay',atk:14,def:12,str:14,slot:'Gloves',rarity:'legendary'},
{name:'Ormentedtay Aceletbray',atk:18,def:5,str:2,slot:'Gloves',rarity:'legendary'},
{name:'Arytezay Ambracesyay',atk:15,def:10,str:5,slot:'Gloves',rarity:'mythic'},
// ===== GLOVES — DARK SOULS (pig latin) =====
{name:'Avelsay Auntletsgay ofway Enway',atk:8,def:18,str:10,slot:'Gloves',rarity:'legendary'},
{name:'Ornsteinway Auntletsgay',atk:10,def:20,str:8,slot:'Gloves',rarity:'legendary'},
{name:'Avel Ordlay Aceletbray',atk:6,def:15,str:12,slot:'Gloves',rarity:'rare'},
// ===== RINGS — RUNESCAPE (pig latin) =====
{name:'Erserkersbay Ingray',atk:15,def:5,str:20,slot:'Ring',rarity:'legendary'},
{name:'Ingray ofway Ufferingsay',atk:0,def:22,str:0,slot:'Ring',rarity:'legendary'},
{name:'Imstonebray Ingray',atk:12,def:12,str:12,slot:'Ring',rarity:'legendary'},
{name:'Ultorway Ingray',atk:18,def:3,str:22,slot:'Ring',rarity:'mythic'},
{name:'Ellatorbay Ingray',atk:20,def:5,str:18,slot:'Ring',rarity:'mythic'},
{name:'Enatorvay Ingray',atk:16,def:3,str:15,slot:'Ring',rarity:'mythic'},
// ===== RINGS — DARK SOULS (pig latin) =====
{name:'Avelsay Ingray ofway Avorsfay',atk:12,def:12,str:18,slot:'Ring',rarity:'legendary'},
{name:'Avelhay Ingray',atk:8,def:5,str:25,slot:'Ring',rarity:'legendary'},
{name:'Oridanchlay Ingray',atk:0,def:30,str:0,slot:'Ring',rarity:'legendary'},
{name:'Ingray ofway Eel Andinglay',atk:5,def:5,str:5,slot:'Ring',rarity:'rare'},
{name:'Eoway Ingray',atk:10,def:10,str:10,slot:'Ring',rarity:'rare'},
{name:'Olfway Ingray',atk:18,def:0,str:20,slot:'Ring',rarity:'legendary'},
// ===== OFFHAND — DUAL WIELD =====
// Off-hand daggers for dual wield
{name:'Off-ay Aggerday',atk:15,def:0,str:12,slot:'OffHand',rarity:'common'},
{name:'Off-ay Onedgeday',atk:22,def:0,str:18,slot:'OffHand',rarity:'uncommon'},
{name:'Off-ay Orpoisepay',atk:35,def:0,str:28,slot:'OffHand',rarity:'rare'},
{name:'Off-ay Aserbay Daggerlay',atk:48,def:0,str:38,slot:'OffHand',rarity:'rare'},
{name:'Off-ay Alemorianchay Daggerlay',atk:55,def:0,str:45,slot:'OffHand',rarity:'legendary'},
{name:'Off-ay Azilithclay Ipwhay',atk:62,def:0,str:50,slot:'OffHand',rarity:'legendary'},
// Off-hand swords for dual wield
{name:'Off-ay Ongswordlay',atk:25,def:3,str:20,slot:'OffHand',rarity:'uncommon'},
{name:'Off-ay Impscimitarstay',atk:32,def:2,str:26,slot:'OffHand',rarity:'rare'},
{name:'Off-ay Addonray Ongswordlay',atk:42,def:5,str:35,slot:'OffHand',rarity:'rare'},
{name:'Off-ay Uneray Ongswordlay',atk:50,def:4,str:42,slot:'OffHand',rarity:'rare'},
// Off-hand crossbows for dual wield
{name:'Off-ay Crossbowway',atk:30,def:0,str:25,slot:'OffHand',rarity:'uncommon'},
{name:'Oenixpay Crossbowway',atk:45,def:0,str:38,slot:'OffHand',rarity:'rare'},
{name:'Off-ay Zarytezay Ossbowcray',atk:65,def:0,str:50,slot:'OffHand',rarity:'mythic'},
{name:'Off-ay Onyxway Ossbowcray',atk:55,def:0,str:42,slot:'OffHand',rarity:'legendary'}
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
// Create visible dungeon entrance portal
const portalGroup=new THREE.Group();
// Stone arch frame
const archGeo=new THREE.BoxGeometry(8,10,2);
const archMat=new MS({color:0x3a3028,roughness:.9});
const leftPillar=new THREE.Mesh(archGeo,archMat);leftPillar.position.set(-5,5,0);portalGroup.add(leftPillar);
const rightPillar=new THREE.Mesh(archGeo,archMat);rightPillar.position.set(5,5,0);portalGroup.add(rightPillar);
const topLint=new THREE.Mesh(new THREE.BoxGeometry(18,4,2),archMat);topLint.position.set(0,11,0);portalGroup.add(topLint);
// Glowing portal center
const portalGeo=new THREE.PlaneGeometry(8,8);
const portalMat=new THREE.MeshBasicMaterial({color:d.theme==='fire'?0xff4400:d.theme==='undead'?0x4422aa:0x22aa44,side:THREE.DoubleSide,transparent:true,opacity:.7});
const portalPlane=new THREE.Mesh(portalGeo,portalMat);portalPlane.position.set(0,5,0);portalGroup.add(portalPlane);
// Particle ring effect
const ringGeo=new THREE.TorusGeometry(4,.3,8,16);
const ringMat=new THREE.MeshBasicMaterial({color:0xffd700,transparent:true,opacity:.8});
const ring=new THREE.Mesh(ringGeo,ringMat);ring.position.set(0,5,0);ring.rotation.x=Math.PI/2;portalGroup.add(ring);
// Point light glow
const pLight=new THREE.PointLight(d.theme==='fire'?0xff4400:d.theme==='undead'?0x4422aa:0x22aa44,2,25);pLight.position.set(0,6,2);portalGroup.add(pLight);
// Position portal at entrance
portalGroup.position.set(entranceX,0,entranceZ);
// Store reference for animation
portalGroup.userData={portalPlane,ring,light:pLight,theme:d.theme};
d.portalMesh=portalGroup;scene.add(portalGroup);
dungeonObjs.push(portalGroup);
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
// Spawn enemies in room (skip room 0 - safe spawn zone)
if(idx>0){rm.enemies.forEach(e=>{spawnE(e.type,rm.x+(Math.random()-.5)*rm.w*.5,rm.z+(Math.random()-.5)*rm.l*.5,e.lv)});}
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
player.x=d.rooms[0].x;player.z=d.rooms[0].z;player.y=-d.depth*50+2;
// Hide portal while inside dungeon
if(d.portalMesh)d.portalMesh.visible=false;
log('Entered dungeon! Depth: '+d.depth+' — defeat the boss for special loot!','#f80')}

function exitDungeon(){if(!inDungeon)return;
// Show portal again
if(inDungeon.portalMesh)inDungeon.portalMesh.visible=true;
if(dungeonGroup){scene.remove(dungeonGroup);dungeonGroup=null}
player.x=inDungeon.x;player.z=inDungeon.z+10;player.y=meshTerrainH(player.x,player.z)+2;inDungeon=null;
// FIX: Rebuild colliders to remove dungeon walls and prevent invisible barriers
buildColliders();
log('Exited dungeon.','#0f0')}

// === BUILDING INTERIOR SYSTEM ===
function enterBuilding(b){
if(insideBuilding)return;insideBuilding=b;
// Store outside position for return
b.outsideX=player.x;b.outsideZ=player.z;
// Create building interior
buildingGroup=new THREE.Group();
const floorMat=new MS({color:0x5a4a3a,roughness:.95});
const wallMat=new MS({color:b.type==='tavern'||b.type==='inn'?0x3a2a1a:b.type==='shop'||b.type==='forge'?0x4a4a5a:b.type==='mansion'?0x6a5a4a:b.type==='chapel'?0x5a4a6a:0x4a3a2a,roughness:.9});
const ceilMat=new MS({color:0x2a2a2a,roughness:1});
// Room dimensions based on type
let w=16,l=14,h=12;
if(b.type==='tavern'||b.type==='inn'){w=24;l=20;h=14}
else if(b.type==='shop'){w=18;l=14;h=12}
else if(b.type==='forge'){w=20;l=16;h=14}
else if(b.type==='mansion'){w=28;l=22;h=18}
else if(b.type==='chapel'){w=16;l=24;h=20}
else if(b.type==='tower'||b.type==='watchtower'){w=10;l=10;h=30}
else if(b.type==='windmill'){w=8;l=8;h=25}
else if(b.type==='barn'){w=16;l=28;h=14}
// Floor
const fl=new THREE.Mesh(new THREE.BoxGeometry(w,.5,l),floorMat);fl.position.set(0,1000,0);fl.receiveShadow=true;buildingGroup.add(fl);
// Walls
const wN=new THREE.Mesh(new THREE.BoxGeometry(w,h,1),wallMat);wN.position.set(0,1000+h/2,-l/2);wN.castShadow=true;buildingGroup.add(wN);
const wS=new THREE.Mesh(new THREE.BoxGeometry(w,h,1),wallMat);wS.position.set(0,1000+h/2,l/2);wS.castShadow=true;buildingGroup.add(wS);
const wE=new THREE.Mesh(new THREE.BoxGeometry(1,h,l),wallMat);wE.position.set(w/2,1000+h/2,0);wE.castShadow=true;buildingGroup.add(wE);
const wW=new THREE.Mesh(new THREE.BoxGeometry(1,h,l),wallMat);wW.position.set(-w/2,1000+h/2,0);wW.castShadow=true;buildingGroup.add(wW);
// Ceiling
const ceil=new THREE.Mesh(new THREE.BoxGeometry(w,1,l),ceilMat);ceil.position.set(0,1000+h,0);buildingGroup.add(ceil);
// Door opening (visual only - actual door is behind player)
const doorFrame=new THREE.Mesh(new THREE.BoxGeometry(4,6,.2),new MS({color:0x3a2818}));doorFrame.position.set(0,1000+3,l/2-.1);buildingGroup.add(doorFrame);
// Interior contents based on type
if(b.type==='tavern'||b.type==='inn'){
// Bar counter
const bar=new THREE.Mesh(new THREE.BoxGeometry(10,3.5,2.5),new MS({color:0x5a4a3a}));bar.position.set(0,1000+1.75,-l/4);buildingGroup.add(bar);
// Tables with chairs
for(let i=0;i<4;i++){
const tbl=new THREE.Mesh(new THREE.CylinderGeometry(2.2,2.2,1.5,8),new MS({color:0x4a3a2a}));tbl.position.set(-6+i*4,1000+.75,l/5+i);buildingGroup.add(tbl);
// Chairs
for(let c=0;c<3;c++){const ang=c*2.09;
const chair=new THREE.Mesh(new THREE.BoxGeometry(1,1.5,.1),mt.wd);chair.position.set(-6+i*4+Math.cos(ang)*2.5,1000+.75,l/5+i+Math.sin(ang)*2.5);chair.rotation.y=ang+Math.PI/2;buildingGroup.add(chair);}}
// Fireplace
const fire=new THREE.Mesh(new THREE.SphereGeometry(1.8,8,8),mt.fl);fire.position.set(w/3.5,1000+2.5,-l/3.5);buildingGroup.add(fire);
// Second floor (rooms)
const fl2=new THREE.Mesh(new THREE.BoxGeometry(w*.9,.3,l*.7),new MS({color:0x5a4a3a}));fl2.position.set(0,1000+h*.6,0);buildingGroup.add(fl2);
// Stairs
for(let si=0;si<8;si++){const step=new THREE.Mesh(new THREE.BoxGeometry(2,.2,1),new MS({color:0x4a3a2a}));step.position.set(-w*.3,1000+si*(h*.6/8),-l*.2+si*(l*.3/8));buildingGroup.add(step);}}
else if(b.type==='shop'){
// Counters
const cnt1=new THREE.Mesh(new THREE.BoxGeometry(3,2.5,8),new MS({color:0x6a5a4a}));cnt1.position.set(-w/4,1000+1.25,0);buildingGroup.add(cnt1);
const cnt2=new THREE.Mesh(new THREE.BoxGeometry(3,2.5,8),new MS({color:0x6a5a4a}));cnt2.position.set(w/4,1000+1.25,0);buildingGroup.add(cnt2);
// Shelves
for(let i=0;i<4;i++){const shf=new THREE.Mesh(new THREE.BoxGeometry(.3,6,2),new MS({color:0x5a4a3a}));shf.position.set(-w/2+.5,1000+3,-l/3+i*l/4);buildingGroup.add(shf);}}
else if(b.type==='forge'){
// Anvil
const anvil=new THREE.Mesh(new THREE.BoxGeometry(2,2,1.5),mt.iron);anvil.position.set(0,1000+1,l/4);buildingGroup.add(anvil);
// Forge (glowing)
const forge=new THREE.Mesh(new THREE.BoxGeometry(4,5,4),new MS({color:0x1a0a0a}));forge.position.set(-w/4,1000+2.5,-l/4);buildingGroup.add(forge);
const glow=new THREE.Mesh(new THREE.SphereGeometry(1.5,8,8),new MS({color:0xff4400,emissive:0xff2200,emissiveIntensity:2}));glow.position.set(-w/4,1000+4,-l/4);buildingGroup.add(glow);
// Workbenches
for(let i=0;i<3;i++){const bench=new THREE.Mesh(new THREE.BoxGeometry(3,2,8),mt.wd);bench.position.set(w/3,1000+1,-l/4+i*4);buildingGroup.add(bench);}
// Tools rack
const rack=new THREE.Mesh(new THREE.BoxGeometry(1,6,10),mt.iron);rack.position.set(w/2-.5,1000+3,0);buildingGroup.add(rack);
// Chimney light
const chimLight=new THREE.PointLight(0xff6600,.5,15);chimLight.position.set(-w/4,1000+6,-l/4);buildingGroup.add(chimLight);}
else if(b.type==='mansion'){
// Grand hall floor (marble pattern)
const flG=new THREE.Mesh(new THREE.BoxGeometry(w*.95,.3,l*.95),new MS({color:0x7a7a7a,roughness:.6}));flG.position.set(0,1000.2,0);buildingGroup.add(flG);
// Second and third floors
const fl2=new THREE.Mesh(new THREE.BoxGeometry(w*.9,.2,l*.8),new MS({color:0x6a5a4a}));fl2.position.set(0,1000+h*.35,0);buildingGroup.add(fl2);
const fl3=new THREE.Mesh(new THREE.BoxGeometry(w*.85,.2,l*.6),new MS({color:0x6a5a4a}));fl3.position.set(0,1000+h*.7,0);buildingGroup.add(fl3);
// Grand staircase
for(let si=0;si<12;si++){const step=new THREE.Mesh(new THREE.BoxGeometry(4,.25,1),new MS({color:0x5a4a3a}));step.position.set(0,1000+si*(h*.35/12),-l*.25+si*(l*.4/12));buildingGroup.add(step);}
// Furniture
const diningTable=new THREE.Mesh(new THREE.CylinderGeometry(3,3,1.5,8),new MS({color:0x4a3a2a}));diningTable.position.set(0,1000+.75,l*.3);buildingGroup.add(diningTable);
// Chairs around table
for(let c=0;c<6;c++){const ang=c*1.05;const chair=new THREE.Mesh(new THREE.BoxGeometry(1.2,2,.2),mt.wd);chair.position.set(Math.cos(ang)*4,1000+1,l*.3+Math.sin(ang)*4);chair.rotation.y=-ang;buildingGroup.add(chair);}
// Fireplace (grand)
const fp=new THREE.Mesh(new THREE.BoxGeometry(5,6,2),mt.st);fp.position.set(0,1000+3,-l/2+1);buildingGroup.add(fp);
const fire=new THREE.Mesh(new THREE.SphereGeometry(2,8,8),mt.fl);fire.position.set(0,1000+2,-l/2+2);buildingGroup.add(fire);}
else if(b.type==='chapel'){
// Nave floor
const navFl=new THREE.Mesh(new THREE.BoxGeometry(w*.9,.3,l*.95),new MS({color:0x5a4a4a,roughness:.9}));navFl.position.set(0,1000.2,0);buildingGroup.add(navFl);
// Altar at far end
const altar=new THREE.Mesh(new THREE.BoxGeometry(4,3,2),mt.st);altar.position.set(0,1000+1.5,-l*.4);buildingGroup.add(altar);
const cloth=new THREE.Mesh(new THREE.BoxGeometry(4.2,.1,2.2),new MS({color:0x8a2020}));cloth.position.set(0,1000+3,-l*.4);buildingGroup.add(cloth);
// Pews
for(let pi=0;pi<5;pi++){
const pew=new THREE.Mesh(new THREE.BoxGeometry(w*.6,.8,1.2),mt.wd);pew.position.set(0,1000+.4,-l*.15+pi*3);buildingGroup.add(pew);
const pewBack=new THREE.Mesh(new THREE.BoxGeometry(w*.6,1.5,.1),mt.wd);pewBack.position.set(0,1000+1,-l*.15+pi*3-.6);buildingGroup.add(pewBack);}
// Bell rope
const rope=new THREE.Mesh(new THREE.CylinderGeometry(.1,.1,h*.7,6),new MS({color:0x8a6a3a}));rope.position.set(0,1000+h*.65,0);buildingGroup.add(rope);
// Stained glass windows (colored light)
const winLight=new THREE.PointLight(0x6a2a8a,.4,20);winLight.position.set(0,1000+h*.5,0);buildingGroup.add(winLight);}
else if(b.type==='tower'||b.type==='watchtower'){
// Multiple floors connected by ladder
for(let fl=1;fl<=4;fl++){
const flY=fl*(h/5);
const floor=new THREE.Mesh(new THREE.BoxGeometry(w*.8,.2,l*.8),new MS({color:0x4a4a4a}));floor.position.set(0,1000+flY,0);buildingGroup.add(floor);
// Center hole for ladder
const hole=new THREE.Mesh(new THREE.BoxGeometry(w*.25,.25,l*.25),new MS({color:0x1a1a1a}));hole.position.set(0,1000+flY,0);buildingGroup.add(hole);}
// Central ladder
const ladPole=new THREE.Mesh(new THREE.CylinderGeometry(.2,.2,h,6),mt.iron);ladPole.position.set(0,1000+h/2,0);buildingGroup.add(ladPole);
for(let li=0;li<20;li++){const rung=new THREE.Mesh(new THREE.BoxGeometry(1.2,.1,.15),mt.iron);rung.position.set(0,1000+li*(h/20),0);buildingGroup.add(rung);}
// Archery slots on upper levels
for(let si=0;si<3;si++){const slit=new THREE.Mesh(new THREE.BoxGeometry(.2,1.5,.1),new MS({color:0x0a0a0a}));slit.position.set(w/2+.05,1000+h*.6+si*h*.15,0);buildingGroup.add(slit);}}
else if(b.type==='windmill'){
// Millstone at bottom
const mill=new THREE.Mesh(new THREE.CylinderGeometry(2.5,.3,2,8),mt.st);mill.position.set(0,1000+1,0);buildingGroup.add(mill);
// Grain sacks
for(let gi=0;gi<6;gi++){const sack=new THREE.Mesh(new THREE.SphereGeometry(1,8,8),new MS({color:0x9a8a4a}));
sack.position.set((gi%2===0?-1:1)*2.5,1000+.8,-2+gi*1.2);buildingGroup.add(sack);}
// Ladder to upper levels
const lad=new THREE.Mesh(new THREE.CylinderGeometry(.15,.15,h*.8,6),mt.wd);lad.position.set(0,1000+h*.4,0);buildingGroup.add(lad);
// Grinding mechanism glow
const mechLight=new THREE.PointLight(0xffaa44,.3,10);mechLight.position.set(0,1000+2,0);buildingGroup.add(mechLight);}
else if(b.type==='barn'){
// Dirt floor
const flD=new THREE.Mesh(new THREE.BoxGeometry(w,.2,l),new MS({color:0x4a3a2a,roughness:1}));flD.position.set(0,1000.1,0);buildingGroup.add(flD);
// Hay loft
const loft=new THREE.Mesh(new THREE.BoxGeometry(w*.9,.3,l*.7),new MS({color:0x8a7a4a}));loft.position.set(0,1000+h*.65,0);buildingGroup.add(loft);
// Ladder to loft
const lad=new THREE.Mesh(new THREE.CylinderGeometry(.15,.15,h*.65,6),mt.wd);lad.position.set(w*.3,1000+h*.325,-l*.3);buildingGroup.add(lad);
// Stalls/dividers
for(let si=0;si<4;si++){const stall=new THREE.Mesh(new THREE.BoxGeometry(w*.8,3,.2),mt.wd);stall.position.set(0,1000+1.5,-l*.3+si*l*.2);buildingGroup.add(stall);}
// Hay bales
for(let bi=0;bi<8;bi++){const bale=new THREE.Mesh(new THREE.BoxGeometry(1.5,1,2),new MS({color:0x9a8a3a}));bale.position.set(w*.25+(bi%2)*.5,1000+.5,-l*.25+Math.floor(bi/2)*3);buildingGroup.add(bale);}}
else{
// Default house furniture
const bed=new THREE.Mesh(new THREE.BoxGeometry(4,2,6),new MS({color:0x3a4a5a}));bed.position.set(-w/3,1000+1,-l/3);buildingGroup.add(bed);
const table=new THREE.Mesh(new THREE.CylinderGeometry(2,2,1.5,6),new MS({color:0x4a3a2a}));table.position.set(w/4,1000+.75,l/4);buildingGroup.add(table);
// Fireplace
const fp=new THREE.Mesh(new THREE.BoxGeometry(3,4,1),new MS({color:0x2a2a2a}));fp.position.set(0,1000+2,-l/2+.5);buildingGroup.add(fp);
const fire=new THREE.Mesh(new THREE.SphereGeometry(1,6,6),mt.fl);fire.position.set(0,1000+1.5,-l/2+1);buildingGroup.add(fire);}
// Lighting
const inLight=new THREE.PointLight(0xffaa66,.8,Math.max(w,l)*.8,1.5);inLight.position.set(0,1000+h-2,0);buildingGroup.add(inLight);
scene.add(buildingGroup);
// Position player inside
player.x=0;player.y=1002;player.z=l/4;
// FIX: Rebuild colliders to set up interior collision properly
buildColliders();
log('Entered '+b.name,'#0f0');}

function exitBuilding(){if(!insideBuilding)return;
if(buildingGroup){scene.remove(buildingGroup);buildingGroup=null}
// Return to outside position
player.x=insideBuilding.outsideX;player.z=insideBuilding.outsideZ+3;player.y=meshTerrainH(player.x,player.z)+2;
// FIX: Rebuild colliders to remove interior walls and prevent invisible barriers
buildColliders();
log('Exited '+insideBuilding.name,'#0f0');insideBuilding=null;}

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
function makeEnterable(x,z,type,name,r){
// Larger radius for castles and towers
const radius=r||(type==='castle'?50:type==='cathedral'?40:type==='tower'?30:20);
enterableBuildings.push({x,z,type,name,r:radius});
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
const interactBtn=keys['KeyE']||gpButtons.x;// E key or gamepad X
// Dungeon entry
if(!inDungeon){for(const d of dungeons){if(Math.hypot(px-d.x,pz-d.z)<12){
const portalNames={fire:'🔥 Fire',undead:'💀 Undead',cave:'🐸 Cave'};
log('⚡ APPROACH THE PORTAL → Press E (or X/□) to enter '+portalNames[d.theme]+' Dungeon (Depth '+d.depth+')','#ff0');
if(interactBtn){enterDungeon(d);break}}}}
else{// Check if at entrance room
const rm0=inDungeon.rooms[0];
if(Math.hypot(px-rm0.x,pz-rm0.z)<8&&interactBtn)exitDungeon();
// Check boss room for loot
const bossRoom=inDungeon.rooms[inDungeon.rooms.length-1];
if(Math.hypot(px-bossRoom.x,pz-bossRoom.z)<6){
const bossAlive=enemies.some(e=>e.type===inDungeon.bossType&&Math.hypot(e.x-bossRoom.x,e.z-bossRoom.z)<20);
if(!bossAlive){log('Boss defeated! Press E (or X/□) to loot chest','#ff0');
if(interactBtn){const loot=specialLoot[Math.floor(Math.random()*specialLoot.length)];
log('★ Found: '+loot.name+' ('+loot.rarity+') ATK:'+loot.atk+' DEF:'+loot.def+' STR:'+loot.str,'#ffd700');
if(loot.atk>equipped[loot.slot].atk||loot.def>equipped[loot.slot].def){equipped[loot.slot]={name:loot.name,atk:loot.atk,def:loot.def,str:loot.str};log('Equipped '+loot.name+' to '+loot.slot+'!','#0f0')}
else{log('Added to inventory','#aaa')}
exitDungeon()}}}}
// Building entry
for(const b of enterableBuildings){if(Math.hypot(px-b.x,pz-b.z)<b.r){
if(!insideBuilding){log('Press E (or X/□) to enter '+b.name,'#ff0');
if(interactBtn){enterBuilding(b);break}}
else if(insideBuilding&&insideBuilding.name===b.name){log('Press E (or X/□) to exit '+b.name,'#ff0');
if(interactBtn){exitBuilding();break}}}};};

console.log('INIT: dungeons done, spawning enemies');
// === MIGRATE OLD SAVES TO NEW SLOT SYSTEM ===
migrateOldSave();
// === SPAWN ENEMIES PER REGION ===
regions.forEach(rg=>{rg.en.forEach(et=>{const cnt=Math.max(2,Math.round(rg.r/80));for(let i=0;i<cnt;i++){const ex=rg.x+(Math.random()-.5)*rg.r*1.4,ez=rg.z+(Math.random()-.5)*rg.r*1.4;spawnE(et,ex,ez,rg.lv)}})});
// === SPAWN VISIBLE DRAGONS NEAR START ===
// Add a few dragons flying near spawn so players see them immediately
const dragonTypes=['greendragon','bluedragon','reddragon'];
for(let i=0;i<3;i++){
const angle=(i/3)*Math.PI*2;
const dist=200+Math.random()*100;
const dx=Math.cos(angle)*dist;
const dz=Math.sin(angle)*dist;
const dType=dragonTypes[i%dragonTypes.length];
spawnE(dType,dx,dz,15);
console.log('Spawned '+dType+' at ('+dx.toFixed(0)+','+dz.toFixed(0)+')');}
log('Dragons spotted flying in the distance...','#f84');

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
const bloomPass=new UnrealBloomPass(new THREE.Vector2(innerWidth/2,innerHeight/2),0.4,0.4,0.85);composer.addPass(bloomPass);
const dsGrade=new ShaderPass(DSColorGradeShader);composer.addPass(dsGrade);
window.addEventListener('resize',()=>{cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);composer.setSize(innerWidth,innerHeight)});
initTargetRing();scene.add(targetRing);
// Finalize GPU instanced building elements
if(typeof _buildingInstancers!=='undefined')_buildingInstancers.finalize();
buildColliders();
log('World loaded: '+torchPositions.length+' lights, '+enemies.length+' enemies, '+solidBoxes.length+' colliders','#0f0');
console.log('INIT COMPLETE: scene children='+scene.children.length+', enemies='+enemies.length);

// === GPU PERFORMANCE: Distance culling system ===
const CULL_DIST=400;const CULL_DIST_SQ=CULL_DIST*CULL_DIST;
const noCull=new Set();
scene.traverse(c=>{
if(c===ground||c===riverMesh||c===dustPts||c===playerGroup||c.isLight||c.isPoints||c.isInstancedMesh)noCull.add(c);
if(c.parent&&noCull.has(c.parent))noCull.add(c);
});
scene.children.forEach(c=>{if(c.geometry&&c.geometry.type==='SphereGeometry'&&c.geometry.parameters.radius>=4000)noCull.add(c)});
// Dragons should never be culled - they need to be visible flying from far away
// Mark all enemy meshes with isDragon flag for no-culling
const originalBuildEnemy=buildEnemy;buildEnemy=function(type,lv){
const g=originalBuildEnemy(type,lv);
const isDragon=type==='dragon'||type==='bluedragon'||type==='greendragon'||type==='reddragon'||type==='blackdragon'||type==='irondragon'||type==='steeldragon'||type==='mithdragon'||type==='bronzedragon'||type==='runedragon'||type==='adamdragon'||type==='hydra'||type==='vorkath'||type==='rev_dragon';
if(isDragon){g.traverse(c=>{if(c.isMesh)c.userData.isDragon=true;});noCull.add(g);}
return g;}

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
const gearSlots=['Helm','Chest','Legs','Weapon','Shield','Boots','Gloves','Ring','OffHand'];
const equipped={};gearSlots.forEach(s=>equipped[s]={name:'None',atk:1,def:1,str:1});
equipped.Weapon={name:'Arterstay Ordssway',atk:10,def:0,str:5};equipped.Shield={name:'Arterstay Ieldshay',atk:0,def:5,str:0};
function totalGear(){let a=0,d=0,s=0;gearSlots.forEach(sl=>{if(equipped[sl]){a+=equipped[sl].atk;d+=equipped[sl].def;s+=equipped[sl].str}});return{atk:a,def:d,str:s}}

function buildEnemy(type,lv){
const g=new THREE.Group();const col=eCol[type]||0x888888;const mat=new MS({color:col,roughness:.7});const matD=new MS({color:col,roughness:.55,metalness:.2});const matLt=new MS({color:col,roughness:.6,metalness:.1});
const isArmored=type==='guard'||type==='whiteknight'||type==='knight'||type==='warrior'||type==='barbarian'||type==='black_guard'||type==='dark_warrior'||type==='moss_warrior'||type==='ice_warrior'||type==='chaos_warrior'||type==='tomb_guard'||type==='tomb_ranger'||type==='spiritual_war'||type==='spiritual_rang'||type==='rev_knight'||type==='elf_warrior';
const isUndead=type==='skeleton'||type==='zombie'||type==='ghost'||type==='shade'||type==='revenant'||type==='ankou'||type==='shade_lv2'||type==='shade_lv3'||type==='tortured'||type==='revenant2'||type==='phantom'||type==='banshee'||type==='spectre'||type==='aberspec'||type==='devspec';
const isBeast=type==='wolf'||type==='bear'||type==='spider'||type==='snake'||type==='bat'||type==='cow'||type==='chicken'||type==='rat'||type==='lizard'||type==='scarab'||type==='hellhound'||type==='white_wolf'||type==='dire_wolf'||type==='cave_spider'||type==='shadow_spider'||type==='venom_spider'||type==='crystal_spider'||type==='crystal_wolf'||type==='terrorbird'||type==='chompy'||type==='jubbly'||type==='sea_snake'||type==='brine_rat'||type==='cave_eel'||type==='rockcrabs'||type==='sandcrabs'||type==='ammonite'||type==='plague_rat'||type==='giant_rat'||type==='moss_rat'||type==='monkey'||type==='seagull'||type==='penguin'||type==='desertlizard'||type==='harpie'||type==='terrordog'||type==='shadow_leech';
const isDemon=type==='demon'||type==='tzhaar'||type==='elemental'||type==='lessdemon'||type==='greatdemon'||type==='blackdemon'||type==='ice_demon'||type==='fire_demon'||type==='blood_demon'||type==='pyrefiend'||type==='infernalmage'||type==='jungle_demon';
const isDragon=type==='dragon'||type==='blackdragon'||type==='greendragon'||type==='bluedragon'||type==='reddragon'||type==='steeldragon'||type==='irondragon'||type==='bronzedragon'||type==='mithdragon'||type==='runedragon'||type==='adamdragon'||type==='hydra'||type==='vorkath'||type==='rev_dragon';
const isGiant=type==='hillgiant'||type==='mossgiant'||type==='firegiant'||type==='icegiant'||type==='obor'||type==='troll'||type==='ogre'||type==='ice_troll'||type==='rock_troll'||type==='river_troll'||type==='mountain_troll';
let sc=.4+lv*.006;if(isDragon)sc=.7+lv*.008;if(isGiant)sc=.6+lv*.007;
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
else g.userData.lArm=armGrp;
});
} else {
// Beast legs - 4 animated legs for wolf/bear/spider
const beastLegs=[];
[[-1,1.5],[1,1.5],[-1,-1.5],[1,-1.5]].forEach(([sx,sz],idx)=>{
const legGrp=new THREE.Group();legGrp.position.set(sx,1.5,sz);
const upperLeg=new THREE.Mesh(new THREE.CylinderGeometry(.3,.25,1.5,5),mat);upperLeg.position.y=-.75;upperLeg.castShadow=true;legGrp.add(upperLeg);
const kneeGrp=new THREE.Group();kneeGrp.position.y=-1.5;legGrp.add(kneeGrp);
const lowerLeg=new THREE.Mesh(new THREE.CylinderGeometry(.25,.2,1.5,5),mat);lowerLeg.position.y=-.75;lowerLeg.castShadow=true;kneeGrp.add(lowerLeg);
const paw=new THREE.Mesh(new THREE.SphereGeometry(.3,5,5),matD);paw.position.y=-1.5;kneeGrp.add(paw);
g.add(legGrp);
legGrp.userData.knee=kneeGrp;
beastLegs.push(legGrp);
});
// Store leg references for animation (front left, front right, back left, back right)
g.userData.lArm=beastLegs[0];// Front left leg treated as "left arm"
g.userData.rArm=beastLegs[1];// Front right leg treated as "right arm"
g.userData.lLeg=beastLegs[2];// Back left leg treated as "left leg"
g.userData.rLeg=beastLegs[3];// Back right leg treated as "right leg"
g.userData.lKnee=beastLegs[2].userData.knee;
g.userData.rKnee=beastLegs[3].userData.knee;
// Body center for breathing animation
const bodyCenter=new THREE.Group();bodyCenter.position.y=3.5;g.add(bodyCenter);
g.userData.bodyCenter=bodyCenter;
// Head group for animation
const headGroup=new THREE.Group();headGroup.position.set(0,4.5,2.5);g.add(headGroup);
g.userData.headGroup=headGroup;
// Animation state init
g.userData.animState='idle';g.userData.animTime=0;
}
// === LEGS (humanoids) - Animated groups for walk/run cycles ===
if(!isBeast){
const buildEnemyLeg=(side)=>{
const leg=new THREE.Group();leg.position.set(side*.65,2.5,0);
// Thigh
const thigh=new THREE.Mesh(new THREE.CylinderGeometry(.45,.4,2.5,6),mat);thigh.position.y=-1.25;thigh.castShadow=true;leg.add(thigh);
// Knee group
const knee=new THREE.Group();knee.position.y=-2.5;leg.add(knee);
// Shin
const shin=new THREE.Mesh(new THREE.CylinderGeometry(.38,.32,2.2,6),mat);shin.position.y=-1.1;shin.castShadow=true;knee.add(shin);
// Boot/foot
const boot=new THREE.Mesh(new THREE.BoxGeometry(.7,.5,1.2),matD);boot.position.set(0,-2.2,.1);knee.add(boot);
if(isArmored){
const greave=new THREE.Mesh(new THREE.BoxGeometry(.4,1.8,.2),matLt);greave.position.set(0,-.8,.4);knee.add(greave);
const kneePad=new THREE.Mesh(new THREE.BoxGeometry(.4,.4,.3),matD);kneePad.position.set(0,.5,.35);leg.add(kneePad)}
leg.userData.knee=knee;
return leg;
};
const lLeg=buildEnemyLeg(-1);g.add(lLeg);
const rLeg=buildEnemyLeg(1);g.add(rLeg);
g.userData.lLeg=lLeg;g.userData.rLeg=rLeg;
g.userData.lKnee=lLeg.userData.knee;
g.userData.rKnee=rLeg.userData.knee;
// Body center for breathing/bob animation
const bodyCenter=new THREE.Group();bodyCenter.position.y=4.5;g.add(bodyCenter);
g.userData.bodyCenter=bodyCenter;
// Animation state init
g.userData.animState='idle';g.userData.animTime=0;}
// === ENEMY EQUIPMENT SYSTEM ===
// Store equipped gear for loot drops
g.userData.equippedGear=[];
// Weapon attachment helper - attaches to right hand for proper animation
const attachToHand=(mesh,rotX=0,rotY=0,rotZ=0)=>{
if(g.userData.rArm){
mesh.position.set(.3,-5.5,0);// Relative to hand position
mesh.rotation.set(rotX,rotY,rotZ);
g.userData.rArm.children[3].add(mesh);// Add to hand mesh
return true;}return false;};
// === WEAPONS (per type) - Attached to hand for animation ===
if(type==='demon'||type==='revenant'||type==='whiteknight'||type==='guard'||type==='knight'||type==='skeleton'||type==='warrior'){
// Sword with crossguard - attached to hand
const swordGrp=new THREE.Group();
const blade=new THREE.Mesh(new THREE.BoxGeometry(.15,.12,5.5),mt.swordBlade);blade.position.set(0,0,2.5);swordGrp.add(blade);
const xguard=new THREE.Mesh(new THREE.BoxGeometry(1,.15,.15),mt.swordHilt);xguard.position.set(0,0,-.2);swordGrp.add(xguard);
const hilt=new THREE.Mesh(new THREE.CylinderGeometry(.08,.08,.9,5),mt.swordHilt);hilt.position.set(0,0,-.9);hilt.rotation.x=Math.PI/2;swordGrp.add(hilt);
const pommel=new THREE.Mesh(new THREE.SphereGeometry(.12,6,6),mt.gold);pommel.position.set(0,0,-1.4);swordGrp.add(pommel);
attachToHand(swordGrp,0.3,0,0);
// Shield for knights/guards - attached to left arm
if(type==='whiteknight'||type==='guard'||type==='knight'){
const shieldGrp=new THREE.Group();
const sh=new THREE.Mesh(new THREE.BoxGeometry(.25,3,2),matD);shieldGrp.add(sh);
const shBoss=new THREE.Mesh(new THREE.SphereGeometry(.3,6,6),mt.gold);shBoss.position.x=-.2;shieldGrp.add(shBoss);
const shRim=new THREE.Mesh(new THREE.BoxGeometry(.26,.2,2.1),matLt);shRim.position.y=1.9;shieldGrp.add(shRim);
// Attach to left arm
if(g.userData.lArm){shieldGrp.position.set(-.3,-5.5,.5);shieldGrp.rotation.set(0,0,-.3);g.userData.lArm.children[3].add(shieldGrp);}
g.userData.equippedGear.push({slot:'Shield',name:type==='whiteknight'?'Iteway Ieldshay':'Ironway Ieldshay',def:type==='whiteknight'?15:8,atk:0,str:0});}
g.userData.equippedGear.push({slot:'Weapon',name:type==='whiteknight'?'Ithrilmay Ordssway':type==='knight'?'Eelstay Ordssway':'Ironway Ordssway',atk:type==='whiteknight'?25:type==='knight'?18:12,def:0,str:type==='whiteknight'?15:type==='knight'?10:5});}
if(type==='barbarian'||type==='pirate'||type==='warrior'||type==='troll'||type==='ogre'||type==='hillgiant'||type==='mossgiant'){
// Axe attached to hand
const axeGrp=new THREE.Group();
const handle=new THREE.Mesh(new THREE.CylinderGeometry(.1,.12,4.5,4),mt.wd);handle.position.set(0,-1.5,0);handle.rotation.x=Math.PI/2;axeGrp.add(handle);
const axeHead=new THREE.Mesh(new THREE.BoxGeometry(1.2,1.8,.15),mt.armorLt);axeHead.position.set(0,1.2,.2);axeGrp.add(axeHead);
const axeBack=new THREE.Mesh(new THREE.BoxGeometry(.8,1.2,.15),mt.armorLt);axeBack.position.set(0,-.5,-.1);axeGrp.add(axeBack);
attachToHand(axeGrp,0.5,0,0);
g.userData.equippedGear.push({slot:'Weapon',name:'Eelstay Atchethay',atk:22,def:0,str:18});}
if(type==='mage'||type==='darkwiz'||type==='cultist'||type==='elf'||type==='mummy'||type==='tomb_mage'){
// Staff with orb - attached to hand
const staffGrp=new THREE.Group();
const staff=new THREE.Mesh(new THREE.CylinderGeometry(.08,.1,6,5),mt.wd);staff.position.set(0,1,0);staffGrp.add(staff);
const orb=new THREE.Mesh(new THREE.SphereGeometry(.35,8,8),new MS({color:type==='darkwiz'?0x6a1a8a:type==='mummy'?0xaa4400:0x2a6a8a,emissive:type==='darkwiz'?0x4a0a6a:type==='mummy'?0xff4400:0x1a4a6a,emissiveIntensity:2,roughness:.2,metalness:.5}));orb.position.set(0,4.2,0);staffGrp.add(orb);
attachToHand(staffGrp,0.2,0,0);
g.userData.equippedGear.push({slot:'Weapon',name:type==='darkwiz'?'Affstay ofway Airway':type==='mummy'?'Agicsmay Affstay':'Ierdway Affstay',atk:8,def:0,str:0,magic:type==='darkwiz'?20:type==='mummy'?15:12});}
if(type==='archer'||type==='tomb_ranger'||type==='spiritual_rang'||type==='pirate'){
// Bow attached to hand
const bowGrp=new THREE.Group();
const bowStave=new THREE.Mesh(new THREE.CylinderGeometry(.06,.08,5,4),mt.wd);bowStave.position.set(0,0,0);bowStave.rotation.z=.3;bowGrp.add(bowStave);
const bowString=new THREE.Mesh(new THREE.BoxGeometry(.02,4.2,.02),new MS({color:0xdddddd}));bowString.position.set(-.6,0,0);bowGrp.add(bowString);
attachToHand(bowGrp,0,0,.5);
g.userData.equippedGear.push({slot:'Weapon',name:'Owbay',atk:5,def:0,str:0,ranged:15});}
if(type==='thief'||type==='mugger'||type==='bandit'){
// Dagger attached to hand
const daggerGrp=new THREE.Group();
const dBlade=new THREE.Mesh(new THREE.BoxGeometry(.1,.08,2),mt.swordBlade);dBlade.position.set(0,0,.8);daggerGrp.add(dBlade);
const dHilt=new THREE.Mesh(new THREE.CylinderGeometry(.06,.05,.4,4),mt.wd);dHilt.position.set(0,0,-.3);dHilt.rotation.x=Math.PI/2;daggerGrp.add(dHilt);
attachToHand(daggerGrp,0.3,0,0);
g.userData.equippedGear.push({slot:'Weapon',name:'Aggerdray',atk:8,def:0,str:3});}
if(type==='dwarf'||type==='tribesman'){
// Pickaxe attached to hand
const pickGrp=new THREE.Group();
const pHandle=new THREE.Mesh(new THREE.CylinderGeometry(.08,.1,3.5,4),mt.wd);pHandle.position.set(0,-1,0);pHandle.rotation.x=Math.PI/2;pickGrp.add(pHandle);
const pHead=new THREE.Mesh(new THREE.ConeGeometry(.4,.8,4),mt.armorDk);pHead.position.set(0,1,.3);pHead.rotation.x=-.5;pickGrp.add(pHead);
attachToHand(pickGrp,0.4,0,0);
g.userData.equippedGear.push({slot:'Weapon',name:'Onzebray Ickaxepay',atk:10,def:0,str:8});}
if(type==='skeleton'){
// Add shield for skeleton warriors
if(Math.random()>.5){
const skShield=new THREE.Mesh(new THREE.BoxGeometry(.2,2.5,1.8),matD);
if(g.userData.lArm){skShield.position.set(-.3,-5.5,.3);skShield.rotation.set(0,0,-.2);g.userData.lArm.children[3].add(skShield);}
g.userData.equippedGear.push({slot:'Shield',name:'Ullskay Uckbray',def:5,atk:0,str:0});}}
if(type==='spider'){
// Extra legs
for(let i=0;i<4;i++){[-1,1].forEach(s=>{const sleg=new THREE.Mesh(new THREE.CylinderGeometry(.1,.08,3,4),matD);sleg.position.set(s*1.5,2.5,-1+i*.8);sleg.rotation.z=s*.8;sleg.rotation.x=(i-.5)*.2;g.add(sleg)})}}
// === TAIL for beasts ===
if(type==='wolf'||type==='bear'||type==='lizard'||type==='hellhound'){
const tail=new THREE.Mesh(new THREE.CylinderGeometry(.15,.08,2.5,4),mat);tail.position.set(0,3,-3);tail.rotation.x=-.5;g.add(tail)}
// === WINGS for bat/demon ===
if(type==='bat'||isDemon){
[-1,1].forEach(s=>{const wing=new THREE.Mesh(new THREE.PlaneGeometry(3,2.5),new MS({color:col,roughness:.8,side:THREE.DoubleSide,transparent:true,opacity:.7}));wing.position.set(s*2.5,5.5,-.5);wing.rotation.y=s*.4;g.add(wing)})}
// === FULL DRAGON ANATOMY ===
if(isDragon){
// Dragon color scheme based on type
let dCol=col,dGlow=0xff4400;
if(type==='bluedragon'||type==='dragon'){dCol=0x2244aa;dGlow=0x4488ff;}
else if(type==='greendragon'){dCol=0x228822;dGlow=0x44ff44;}
else if(type==='reddragon'||type==='dragon'){dCol=0xaa2222;dGlow=0xff4444;}
else if(type==='blackdragon'){dCol=0x1a1a1a;dGlow=0x440000;}
else if(type==='irondragon'){dCol=0x666666;dGlow=0xffaa44;}
else if(type==='steeldragon'){dCol=0x444466;dGlow=0x8888aa;}
else if(type==='mithdragon'){dCol=0x4466aa;dGlow=0x88aaff;}
else if(type==='bronzedragon'){dCol=0x8b4513;dGlow=0xcd853f;}
else if(type==='runedragon'){dCol=0x4a0066;dGlow=0xaa44ff;}
else if(type==='adamdragon'){dCol=0x228b22;dGlow=0x90ee90;}
const dMat=new MS({color:dCol,roughness:.6,metalness:.2});
const dMatBelly=new MS({color:0xddccaa,roughness:.7});
const dMatGlow=new MS({color:dGlow,emissive:dGlow,emissiveIntensity:1.5});
// Large scaled body (elongated)
const body=new THREE.Mesh(new THREE.CylinderGeometry(1.8,1.4,6,8),dMat);body.position.set(0,4,0);body.rotation.x=Math.PI/2;body.scale.set(1,1.4,1);body.castShadow=true;g.add(body);
// Belly scales (lighter underbelly)
const belly=new THREE.Mesh(new THREE.CylinderGeometry(1.2,1,5,8),dMatBelly);belly.position.set(0,3.5,0);belly.rotation.x=Math.PI/2;belly.scale.set(1,1.35,1);g.add(belly);
// Body spikes along spine
for(let i=0;i<6;i++){const spike=new THREE.Mesh(new THREE.ConeGeometry(.3,1.2,4),dMat);spike.position.set(0,5.5,-2.5+i*.9);spike.rotation.x=-.3;g.add(spike);}
// Large articulated wings
const wingGroups=[];
[-1,1].forEach((s,wi)=>{
const wRoot=new THREE.Group();wRoot.position.set(s*2,5,.5);wRoot.rotation.y=s*.3;g.add(wRoot);
// Wing arm (thick bone)
const wArm=new THREE.Mesh(new THREE.CylinderGeometry(.25,.2,3,5),dMat);wArm.position.set(s*1.5,0,-1);wArm.rotation.z=s*.4;wArm.rotation.x=-.3;wRoot.add(wArm);
// Wing membrane segments
for(let i=0;i<3;i++){
const membrane=new THREE.Mesh(new THREE.PlaneGeometry(2.5,1.8),new MS({color:dCol,roughness:.7,side:THREE.DoubleSide,transparent:true,opacity:.75}));
membrane.position.set(s*(3+i*1.2),-.5-i*.3,-1.5-i*.8);
membrane.rotation.y=s*.2;membrane.rotation.x=-.4;wRoot.add(membrane);}
// Wing tip
const wTip=new THREE.Mesh(new THREE.ConeGeometry(.15,.8,4),dMat);wTip.position.set(s*4.5,-1.2,-3.5);wTip.rotation.z=s*.5;wRoot.add(wTip);
wingGroups.push(wRoot);g.userData['wing'+wi]=wRoot;});
g.userData.wings=wingGroups;
// Long serpentine neck
const neckGroup=new THREE.Group();neckGroup.position.set(0,4.5,4);g.add(neckGroup);g.userData.neck=neckGroup;
const neckSegs=[];
for(let i=0;i<5;i++){
const nSeg=new THREE.Mesh(new THREE.CylinderGeometry(.8-i*.1,.9-i*.1,1.5,6),dMat);nSeg.position.set(0,i*.6,i*.8);nSeg.rotation.x=-.4;neckGroup.add(nSeg);neckSegs.push(nSeg);
// Small neck spikes
if(i<4){const nSpike=new THREE.Mesh(new THREE.ConeGeometry(.2,.6,4),dMat);nSpike.position.set(0,i*.6+1,i*.8-.3);nSpike.rotation.x=-.5;neckGroup.add(nSpike);}}
// Dragon head
const headG=new THREE.Group();headG.position.set(0,3.5,4.5);neckGroup.add(headG);g.userData.head=headG;
const headBase=new THREE.Mesh(new THREE.SphereGeometry(1.3,10,8),dMat);headBase.position.y=0;headBase.scale.set(1,.8,1.4);headG.add(headBase);
// Snout
const snout=new THREE.Mesh(new THREE.CylinderGeometry(.7,.5,1.8,6),dMat);snout.position.set(0,-.2,1.8);snout.rotation.x=Math.PI/2;headG.add(snout);
// Jaw (lower)
const jaw=new THREE.Mesh(new THREE.BoxGeometry(1,1.2,.8),dMat);jaw.position.set(0,-.8,1.2);headG.add(jaw);g.userData.jaw=jaw;
// Eyes (glowing)
[-1,1].forEach(s=>{const eye=new THREE.Mesh(new THREE.SphereGeometry(.25,6,6),dMatGlow);eye.position.set(s*.6,.3,.8);headG.add(eye);});
// Horns
[-1,1].forEach(s=>{const horn=new THREE.Mesh(new THREE.ConeGeometry(.2,1.5,5),dMat);horn.position.set(s*.7,.8,-.2);horn.rotation.z=s*.4;horn.rotation.x=-.3;headG.add(horn);});
// Long tail (segmented)
const tailGroup=new THREE.Group();tailGroup.position.set(0,3,-3);g.add(tailGroup);g.userData.tail=tailGroup;
const tailSegs=[];
for(let i=0;i<8;i++){
const tSeg=new THREE.Mesh(new THREE.CylinderGeometry(.9-i*.1,.8-i*.1,1.2,6),dMat);tSeg.position.set(0,-i*.15,-1-i*.9);tSeg.rotation.x=-.2+i*.05;tailGroup.add(tSeg);tailSegs.push(tSeg);
if(i%2===0){const tSpike=new THREE.Mesh(new THREE.ConeGeometry(.25,.8,4),dMat);tSpike.position.set(0,-i*.15+.8,-1-i*.9);tSpike.rotation.x=-.5;tailGroup.add(tSpike);}}
// Tail tip
const tailTip=new THREE.Mesh(new THREE.ConeGeometry(.3,1.2,4),dMat);tailTip.position.set(0,-1.2,-8);tailTip.rotation.x=-.8;tailGroup.add(tailTip);
// Four sturdy legs
const dLegs=[];
[[-1.5,2],[1.5,2],[-1.5,-1],[1.5,-1]].forEach(([lx,lz],li)=>{
const lGroup=new THREE.Group();lGroup.position.set(lx,2,lz);g.add(lGroup);
const thigh=new THREE.Mesh(new THREE.CylinderGeometry(.5,.4,2,6),dMat);thigh.position.y=-1;thigh.castShadow=true;lGroup.add(thigh);
const knee=new THREE.Group();knee.position.y=-2;lGroup.add(knee);
const shin=new THREE.Mesh(new THREE.CylinderGeometry(.4,.3,1.8,6),dMat);shin.position.y=-.9;shin.castShadow=true;knee.add(shin);
const claw=new THREE.Mesh(new THREE.BoxGeometry(.6,.3,1),dMat);claw.position.set(0,-1.8,.2);knee.add(claw);
lGroup.userData.knee=knee;dLegs.push(lGroup);
if(li<2)g.userData['frontLeg'+(li===0?'L':'R')]=lGroup;
else g.userData['backLeg'+(li===2?'L':'R')]=lGroup;});
g.userData.dragonLegs=dLegs;
// Store animation parts
g.userData.neckSegs=neckSegs;g.userData.tailSegs=tailSegs;
// Dragon is flying by default
g.userData.isFlying=true;g.userData.flyHeight=40+Math.random()*20;}
if(isGiant){const club=new THREE.Mesh(new THREE.CylinderGeometry(.3,.5,5,5),new MS({color:0x5a4020,roughness:.9}));club.position.set(2,4,.5);club.rotation.x=.3;g.add(club)}
// === GHOST transparency ===
if(type==='ghost'||type==='shade'){
g.traverse(c=>{if(c.isMesh&&c.material){c.material=c.material.clone();c.material.transparent=true;c.material.opacity=.5}})}
// HP bar above head
const barY=isDragon?14:isBeast?6:10.5;
const barBg=new THREE.Mesh(new THREE.PlaneGeometry(3,.35),new MS({color:0x220000,side:THREE.DoubleSide}));barBg.position.y=barY;g.add(barBg);
const barFg=new THREE.Mesh(new THREE.PlaneGeometry(3,.3),new MS({color:0x00cc00,side:THREE.DoubleSide}));barFg.position.y=barY;barFg.position.z=.01;g.add(barFg);
g.userData.hpBar=barFg;
// Name label above HP bar
const nameCanvas=document.createElement('canvas');nameCanvas.width=256;nameCanvas.height=64;const nCtx=nameCanvas.getContext('2d');
nCtx.fillStyle='rgba(0,0,0,0)';nCtx.clearRect(0,0,256,64);
nCtx.font='bold 24px "Times New Roman",serif';nCtx.textAlign='center';nCtx.textBaseline='middle';
nCtx.fillStyle='#ffdd88';nCtx.fillText(type.replace(/_/g,' ').toUpperCase()+' (Lv'+(lv||1)+')',128,32);
const nameTex=new THREE.CanvasTexture(nameCanvas);nameTex.magFilter=THREE.NearestFilter;
const nameSprite=new THREE.Sprite(new THREE.SpriteMaterial({map:nameTex,transparent:true}));
nameSprite.position.y=isDragon?15:barY+0.8;nameSprite.scale.set(isDragon?6:4,isDragon?1.5:1,1);g.add(nameSprite);g.userData.nameLabel=nameSprite;
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
troll:'smash',ogre:'smash',dragon:'breath',hydra:'breath',cerberus:'bite',vorkath:'breath',nightmare:'magic',nex:'magic',jad:'magic',zuk:'breath',kraken:'smash',
// New enemies
hobgoblin:'slash',hillgiant:'smash',mossgiant:'smash',firegiant:'smash',icegiant:'smash',
lessdemon:'smash',greatdemon:'smash',blackdemon:'smash',
jelly:'smash',crawhand:'bite',wallbeast:'bite',cavebug:'bite',cavecrawler:'bite',cavehorror:'slash',cavekraken:'smash',
rockslug:'smash',desertlizard:'bite',dustdevil:'magic',smokdevil:'magic',gargoyle2:'smash',grotguard:'smash',
steeldragon:'breath',irondragon:'breath',bronzedragon:'breath',mithdragon:'breath',runedragon:'breath',adamdragon:'breath',
greendragon:'breath',bluedragon:'breath',reddragon:'breath',
fungalbeast:'smash',pyrefiend:'magic',infernalmage:'magic',jellymut:'smash',
terrordog:'bite',banshee:'magic',spectre:'magic',aberspec:'magic',devspec:'magic',
ankou:'slash',aviansie:'slash',spiritual_war:'slash',spiritual_mage:'magic',spiritual_rang:'slash',
waterfiend:'magic',icefiend:'magic',firefiend:'magic',
moss_giant:'smash',bryophyta:'magic',obor:'smash',
chaosdruid:'magic',dagking_rex:'smash',dagking_prime:'magic',dagking_supreme:'slash',
crazy_arch:'slash',ent:'smash',zygomite:'magic',suqah:'smash',
jungle_demon:'smash',jungle_horror:'slash',harpie:'bite',
chaos_ele:'magic',vetion:'smash',callisto:'swipe',venenatis:'magic',fanatic:'magic',scorpia_boss:'bite',
sarachnis:'bite',grotguardian:'smash',skotizo:'smash',siren:'magic',
krakenlet:'bite',seagull:'peck',penguin:'peck',monkey:'bite',terrorbird:'peck',
chompy:'peck',jubbly:'peck',zogre:'smash',mogre:'smash',
rockgolem:'smash',icegolem:'smash',firegolem:'smash',
brine_rat:'bite',cave_eel:'bite',rockcrabs:'bite',sandcrabs:'bite',ammonite:'bite',
dark_warrior:'slash',moss_warrior:'slash',ice_warrior:'slash',chaos_warrior:'slash',
black_guard:'slash',white_wolf:'bite',dire_wolf:'bite',ice_troll:'smash',
rock_troll:'smash',river_troll:'smash',mountain_troll:'smash',
plague_rat:'bite',giant_rat:'bite',moss_rat:'bite',
shade_lv2:'magic',shade_lv3:'magic',tortured:'magic',
abyssal_sire:'smash',alch_hydra:'breath',gauntlet:'slash',hunllef:'magic',
corp_beast:'smash',bandos_avatar:'smash',sara_avatar:'magic',zammy_avatar:'magic',
thermy:'magic',skotos:'smash',mimic2:'smash',deranged_arch:'slash',
warped_terror:'magic',corrupt_beast:'smash',phantom:'magic',
cave_spider:'bite',shadow_spider:'bite',venom_spider:'bite',
tomb_guard:'slash',tomb_mage:'magic',tomb_ranger:'slash',tomb_lord:'magic',
sea_snake:'bite',kraken_spawn:'bite',tentacle:'smash',
glacor:'magic',muspaah:'magic',shadow_leech:'bite',
crystal_spider:'bite',crystal_wolf:'bite',dark_elf:'magic',elf_warrior:'slash',
ice_demon:'magic',fire_demon:'magic',blood_demon:'magic',
anc_zygomite:'magic',gorak:'smash',revenant2:'magic',rev_dragon:'breath',rev_knight:'slash'
};
const eAtkRange={slash:10,chop:11,smash:12,bite:8,swipe:10,charge:14,peck:6,magic:28,breath:22};
function spawnE(type,x,z,lv){const hp=eHP[type]||40;const mesh=buildEnemy(type,lv||1);
const style=eAtkStyles[type]||'slash';const range=eAtkRange[style]||10;
const isDragon=type==='dragon'||type==='bluedragon'||type==='greendragon'||type==='reddragon'||type==='blackdragon'||type==='irondragon'||type==='steeldragon'||type==='mithdragon'||type==='bronzedragon'||type==='runedragon'||type==='adamdragon'||type==='hydra'||type==='vorkath'||type==='rev_dragon';
const e={mesh,hp,maxHp:hp,poi:30,x,z,type,lv:lv||1,atkCD:0,aggro:50+(lv||1)*2,dmg:Math.max(5,8+(lv||1)*2),
atkStyle:style,atkRange:range,windUp:0,swingT:0,strafeAng:Math.random()*Math.PI*2,strafeCW:Math.random()>.5?1:-1,
staggered:false,staggerT:0,target:null};
const h=meshTerrainH(x,z);
// Dragons spawn flying high above ground
if(isDragon){
const flyHeight=50+Math.random()*30;e.mesh.userData.isFlying=true;e.mesh.userData.flyHeight=flyHeight;
e.mesh.userData.landing=false;e.mesh.userData.landTimer=0;e.mesh.userData.flyAng=Math.random()*Math.PI*2;
e.mesh.position.set(x,h+flyHeight,z);
log(type+' (Lv'+(lv||1)+') appears flying overhead!','#f84');}
else{e.mesh.position.set(x,h,z);}
scene.add(e.mesh);enemies.push(e)}

function calcHit(a,d){const g=totalGear();const ab=a===player?40+g.atk:22+((a.lv||1)*1.5);const db=d===player?30+g.def:15;return Math.random()<Math.max(.08,Math.min(.94,(ab/(db+12))*.82))}

function makeLootMesh(col,sz){
const g=new THREE.Group();
// Glowing orb
const orb=new THREE.Mesh(new THREE.SphereGeometry(sz,8,8),new MS({color:col,emissive:col,emissiveIntensity:1.2,roughness:.2,metalness:.4,transparent:true,opacity:.85}));
g.add(orb);
// Vertical light pillar (DS style)
const pillar=new THREE.Mesh(new THREE.CylinderGeometry(.15,.15,12,6),new MS({color:col,emissive:col,emissiveIntensity:2,transparent:true,opacity:.35,side:THREE.DoubleSide}));
pillar.position.y=4;g.add(pillar);
// Soft halo ring on ground
const halo=new THREE.Mesh(new THREE.RingGeometry(1.5,3,16),new MS({color:col,emissive:col,emissiveIntensity:.8,transparent:true,opacity:.25,side:THREE.DoubleSide}));
halo.rotation.x=-Math.PI/2;halo.position.y=-.5;g.add(halo);
return g}
// === UNIQUE ITEM ID SYSTEM ===
let nextItemUID=1;
function genUID(){return 'item_'+(nextItemUID++)}
function rollStatVar(base){// RNG stat variation: +-20%
const mult=.8+Math.random()*.4;return Math.max(1,Math.round(base*mult))}
// itemDB stores unique items by UID: {uid,name,atk,def,str,slot,rarity}
const itemDB={};
function createUniqueItem(name,atk,def,str,slot,rarity){
const uid=genUID();const item={uid,name,atk:rollStatVar(atk),def:rollStatVar(def),str:rollStatVar(str),slot:slot||null,rarity:rarity||'common'};
itemDB[uid]=item;return item}
function createDropItem(name,rarity){
const uid=genUID();const item={uid,name,atk:0,def:0,str:0,slot:null,rarity:rarity||'common'};
itemDB[uid]=item;return item}
function spawnLoot(x,z,e){
// === EQUIPPED GEAR DROPS ===
// Drop the enemy's visible equipped weapons/shields as loot
if(e.mesh.userData.equippedGear&&e.mesh.userData.equippedGear.length>0){
for(const gear of e.mesh.userData.equippedGear){
const ox=x+(Math.random()-.5)*8,oz=z+(Math.random()-.5)*8;
const gearItem=createUniqueItem(gear.name,gear.atk||1,gear.def||0,gear.str||0,gear.slot,'gear');
const col=gear.slot==='Weapon'?0xffaa00:gear.slot==='Shield'?0x4488ff:0xffd700;
const mGear=makeLootMesh(col,1.0);
mGear.position.set(ox,meshTerrainH(ox,oz)+4,oz);
mGear.userData={vx:(Math.random()-.5)*4,vz:(Math.random()-.5)*4,vy:8,life:1800,item:gear.name,uid:gearItem.uid,gear:gearItem,rarity:'gear',settled:false};
scene.add(mGear);lootArr.push(mGear);
log(e.type+' dropped '+gear.name+'!','#ff0');}}
// Standard gear drop with unique ID
const slot=gearSlots[Math.floor(Math.random()*gearSlots.length)];
const cur=equipped[slot];const boost=1.01;
const baseAtk=Math.ceil(Math.max(cur.atk*boost,cur.atk+1));
const baseDef=Math.ceil(Math.max(cur.def*boost,cur.def+1));
const baseStr=Math.ceil(Math.max(cur.str*boost,cur.str+1));
const gearItem=createUniqueItem(e.type+' '+slot+' Lv'+(e.lv||1),baseAtk,baseDef,baseStr,slot,'gear');
const m=makeLootMesh(0xffd700,1.2);
m.position.set(x,meshTerrainH(x,z)+4,z);m.userData={vx:(Math.random()-.5)*5,vz:(Math.random()-.5)*5,vy:8,life:1800,item:gearItem.name,uid:gearItem.uid,gear:gearItem,rarity:'gear',settled:false};scene.add(m);lootArr.push(m);
// Drop table items - each with unique ID
const dt=drops[e.type];if(dt){for(const d of dt){if(Math.random()<d.c){
const ox=x+(Math.random()-.5)*6,oz=z+(Math.random()-.5)*6;
const dropItem=createDropItem(d.i,'common');
const m2=makeLootMesh(0xccccaa,.7);
m2.position.set(ox,meshTerrainH(ox,oz)+3,oz);m2.userData={vx:(Math.random()-.5)*4,vz:(Math.random()-.5)*4,vy:7,life:1200,item:d.i,uid:dropItem.uid,rarity:'common',settled:false};scene.add(m2);lootArr.push(m2);break}}}
// Bones always with unique ID
const bx=x+2,bz=z+2;const boneItem=createDropItem('Onesbay','common');
const m3=makeLootMesh(0x998877,.5);
m3.position.set(bx,meshTerrainH(bx,bz)+3,bz);m3.userData={vx:(Math.random()-.5)*3,vz:(Math.random()-.5)*3,vy:6,life:1200,item:'Onesbay',uid:boneItem.uid,rarity:'common',settled:false};scene.add(m3);lootArr.push(m3);
}
function hitFX(x,y,z,col=0xff4400){for(let i=0;i<25;i++){const p=new THREE.Mesh(new THREE.SphereGeometry(.3,4,4),new MS({color:col,emissive:col,emissiveIntensity:1.5,roughness:1}));p.position.set(x,y,z);p.userData={vx:(Math.random()-.5)*10,vy:(Math.random()-.5)*10+4,vz:(Math.random()-.5)*10,life:22};scene.add(p);particles.push(p)}}
function cycleLock(){
// If no enemies, bail
if(!enemies.length){lockOn=null;lockIdx=-1;log('No targets','#887');return}
// Find nearest enemies to cycle through (prefer closer ones)
const sorted=[...enemies].sort((a,b)=>Math.hypot(a.mesh.position.x-player.x,a.mesh.position.z-player.z)-Math.hypot(b.mesh.position.x-player.x,b.mesh.position.z-player.z));
const curSortedIdx=lockOn?sorted.indexOf(lockOn):-1;
const nextIdx=(curSortedIdx+1)%sorted.length;
// Toggle off if cycling back to same target (only one enemy)
if(sorted.length===1&&lockOn===sorted[0]){lockOn=null;lockIdx=-1;log('Lock-on released','#887');return}
lockOn=sorted[nextIdx];lockIdx=enemies.indexOf(lockOn);
log('Locked: '+lockOn.type+' (Lv'+(lockOn.lv||1)+') — press Tab/F again to cycle','#f84')}
function toggleLock(){
// Nearest enemy toggle — press again to release
if(lockOn){lockOn=null;lockIdx=-1;log('Lock-on released','#887');return}
if(!enemies.length){log('No targets nearby','#887');return}
// Pick nearest enemy within 120 units
let best=null,bestD=120;
for(const e of enemies){const d=Math.hypot(e.mesh.position.x-player.x,e.mesh.position.z-player.z);if(d<bestD){bestD=d;best=e}}
if(best){lockOn=best;lockIdx=enemies.indexOf(best);log('Locked: '+best.type+' (Lv'+(best.lv||1)+')','#f84')}
else log('No targets in range (120u)','#887')}
// Proper Dark Souls style parry system
// Hold RMB/LT/LB to BLOCK (reduces damage, drains stamina slowly)
// Press 2/RB to PARRY (creates brief parry window, costs stamina)
// If enemy attacks during parry window = riposte opportunity
function startBlock(){player.blocking=true}
function endBlock(){if(!player._parryWindow)player.blocking=false}
function parry(){if(player.sta<15){log('Not enough stamina to parry!','#f84');return}
player.sta-=15;player._parryCD=20;player._parryWindow=12;// 12 frames (~200ms) parry window
player.blocking=true;// Parry puts you in blocking stance
// Trigger parry animation
if(playerGroup&&playerGroup.userData){playerGroup.userData._parryAnimT=0;playerGroup.userData.animState='parry'}
hitFX(player.x,player.y+5,player.z,0x44ffff);// Parry flash effect
log('PARRY!','#0ff');
// Check for successful parry against locked enemy
if(lockOn){const d=Math.hypot(lockOn.mesh.position.x-player.x,lockOn.mesh.position.z-player.z);
// Enemy must be close AND winding up attack
if(d<12&&lockOn.windUp>0){successfulParry(lockOn)}}}
function successfulParry(enemy){enemy.staggered=true;enemy.staggerT=60;// 1 second stagger
enemy.windUp=0;enemy.atkCD=40;// Stagger enemy
hitFX(enemy.mesh.position.x,enemy.mesh.position.y+6,enemy.mesh.position.z,0x00ffff);
player._riposteWindow=45;// ~750ms to riposte
log('PARRY SUCCESS! RIPOSTE AVAILABLE','#0ff');
// Auto-riposte if close enough
const d=Math.hypot(enemy.mesh.position.x-player.x,enemy.mesh.position.z-player.z);
if(d<8){const riposteDmg=25+Math.floor(totalGear().atk*1.5);enemy.hp-=riposteDmg;
hitFX(enemy.mesh.position.x,enemy.mesh.position.y+4,enemy.mesh.position.z,0xff0000);
player.sta=Math.min(player.sta+35,player.maxSta);skills.Defence.xp+=15;updateXpBar();
log('RIPOSTE! '+riposteDmg+' damage','#f00')}}
function updateParrySystem(){
// Decay parry window
if(player._parryWindow>0){player._parryWindow--;if(player._parryWindow===0&&!mouse.right&&!gpButtons.lt&&!gpButtons.lb)player.blocking=false}
// Decay riposte window
if(player._riposteWindow>0)player._riposteWindow--;
// Stamina drain while blocking (3 per second, more during parry window)
if(player.blocking){const drain=player._parryWindow>0?0.08:0.05;player.sta=Math.max(0,player.sta-drain)}
// If stamina depleted, stop blocking
if(player.blocking&&player.sta<=0){player.blocking=false;log('Stamina depleted! Block broken!','#f84')}}
// Legacy parry function - redirect to new system
function doParry(){parry()}

let gpIndex=-1;
// Dark Souls-style gamepad mapping (customizable)
// Maps action names to gamepad button indices. Standard: A=0 B=1 X=2 Y=3 LB=4 RB=5 LT=6 RT=7 Back=8 Start=9 LSClick=10 RSClick=11 DUp=12 DDown=13 DLeft=14 DRight=15
const gpMap={
roll:1,     // B/Circle = Roll (Dark Souls default)
attack:7,   // RT = Light Attack
parry:5,    // RB = Parry/Heavy Attack
block:6,    // LT = Block/Guard
lockon:11,  // R3 / RS Click = Lock-on toggle (DS3 style)
lockonCycle:10, // L3 / LS Click = Cycle through targets
sprint:10,  // L3 / LS Click = Sprint (hold)
heal:0,     // A/Cross = Heal (Estus)
useItem:2,  // X/Square = Use item / Pickup
twoHand:3,  // Y/Triangle = Jump
inventory:9,// Start = Inventory/Menu
skills:8,   // Back/Select = Skills
dUp:12,     // D-Pad Up = Prayer Tab
dDown:13,   // D-Pad Down = Skills Tab
dLeft:14,   // D-Pad Left = Inventory Tab
dRight:15   // D-Pad Right = Map or unused
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
// L3/R3 stick clicks
const lsbIdx=gpMap.sprint||10;const rsbIdx=gpMap.rsb||11;
gpButtons.lsb=isP(lsbIdx);gpButtons.rsb=isP(rsbIdx);
// R3 = toggle lock (on/off nearest)
if(isP(gpMap.lockon)&&!player._lkCD){toggleLock();player._lkCD=25}
// L3 = cycle through targets (also used for sprint hold)
if(isP(gpMap.lockonCycle)&&!player._lkCycleCD){cycleLock();player._lkCycleCD=25}
if(player._lkCD)player._lkCD--;
if(player._lkCycleCD)player._lkCycleCD--;
if(typeof checkGpCombos==='function')checkGpCombos();
}

function loop(){
requestAnimationFrame(loop);time+=.016;pollGamepad();
if(player.dead){player.deadTimer-=.016;if(player.deadTimer<=0){player.dead=false;player.hp=player.maxHp;player.sta=player.maxSta;player.x=0;player.z=5;player.y=meshTerrainH(0,5);document.getElementById('death-overlay').classList.remove('active');log('Respawned at bonfire','#cc4')}composer.render();return}

const gSens=(gameOpts?gameOpts.sens:5)/5;camYaw+=gpAxes[2]*.35*gSens*(gameOpts?gameOpts.flipx:1);camPitch=Math.max(.05,Math.min(1.2,camPitch-gpAxes[3]*.25*gSens*(gameOpts?gameOpts.flipy:1)));
// Camera orientation: face target when locked on, otherwise auto-follow behind player
if(!mouse.mid){
if(lockOn&&lockOn.mesh){
// When locked on, camera faces the target (Dark Souls style)
const tx=lockOn.mesh.position.x,tz=lockOn.mesh.position.z;
// Calculate angle FROM target TO player (so camera orbits behind player facing target)
const targetYaw=Math.atan2(player.x-tx,player.z-tz);
let yd=targetYaw-camYaw;while(yd>Math.PI)yd-=Math.PI*2;while(yd<-Math.PI)yd+=Math.PI*2;
camYaw+=yd*.08 // Smoothly turn toward target
}else{
// Auto-camera: lerp camYaw behind player when not locked on
let targetYaw=player.ang+Math.PI;while(targetYaw>Math.PI)targetYaw-=Math.PI*2;while(targetYaw<-Math.PI)targetYaw+=Math.PI*2;let yd=targetYaw-camYaw;while(yd>Math.PI)yd-=Math.PI*2;while(yd<-Math.PI)yd+=Math.PI*2;camYaw+=yd*.03}}

const fwd=new THREE.Vector3(-Math.sin(camYaw),0,-Math.cos(camYaw));
const right=new THREE.Vector3(fwd.z,0,-fwd.x);
let moveDir=new THREE.Vector3();
if(keys['w']||gpButtons.dUp)moveDir.add(fwd);if(keys['s']||gpButtons.dDown)moveDir.sub(fwd);
if(keys['a']||gpButtons.dLeft)moveDir.add(right);if(keys['d']||gpButtons.dRight)moveDir.sub(right);
if(gpAxes[0]||gpAxes[1]){moveDir.sub(right.clone().multiplyScalar(gpAxes[0]));moveDir.sub(fwd.clone().multiplyScalar(gpAxes[1]))}

// Sprint detection (Left Shift or L3 gamepad)
const isSprinting=(keys['shift']||keys['ShiftLeft']||keys['ShiftRight']||gpButtons.lsb)&&player.sta>0;
if(isSprinting)player.sta=Math.max(0,player.sta-0.05);

let spd=player.speed;
if(player.rolling){player.rollT--;if(player.rollT<=0)player.rolling=false;spd*=3.6}
else if(player.dashing){player.dashT--;if(player.dashT<=0)player.dashing=false;spd*=4}
else if(isSprinting){spd*=1.8} // Sprint 80% faster

// Track previous position for velocity calculation
const prevX=player.x,prevZ=player.z;

if(moveDir.lengthSq()>.001){moveDir.normalize();
const steps=spd>1?4:2;const stepSpd=spd/steps;
for(let st=0;st<steps;st++){player.x+=moveDir.x*stepSpd;player.z+=moveDir.z*stepSpd;
const co=pushOut(player.x,player.y,player.z);player.x=co.x;player.z=co.z}
// When locked on, player always faces the target regardless of movement direction
if(lockOn&&lockOn.mesh){
const la=Math.atan2(lockOn.mesh.position.x-player.x,lockOn.mesh.position.z-player.z);
let ld=la-player.ang;while(ld>Math.PI)ld-=Math.PI*2;while(ld<-Math.PI)ld+=Math.PI*2;
player.ang+=ld*.18
}else{
const targetAng=Math.atan2(moveDir.x,moveDir.z);
let diff=targetAng-player.ang;while(diff>Math.PI)diff-=Math.PI*2;while(diff<-Math.PI)diff+=Math.PI*2;
player.ang+=diff*.15}}
else{const co=pushOut(player.x,player.y,player.z);player.x=co.x;player.z=co.z}

// Calculate actual velocity for animation
player.vx=player.x-prevX;
player.vz=player.z-prevZ;
player.isSprinting=isSprinting&&moveDir.lengthSq()>.001;
// Decay velocity when not moving so animation stops smoothly
if(moveDir.lengthSq()<=.001){player.vx*=0.5;player.vz*=0.5;}

// Jump physics
{const groundY=inDungeon?-inDungeon.depth*50+2:surfaceH(player.x,player.z,player.y);
player.vy-=.55;player.y+=player.vy;
if(player.y<=groundY+.15){player.y=groundY+.15;player.vy=0;player.grounded=true}
else{player.grounded=false}}
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

// Animate windmill blades
windmills.forEach(w=>{if(w.mesh)w.mesh.rotation.z+=.015});

// GPU perf: distance cull every 4 frames, shadow cull every 20, sun follows player
cullFrame++;
if(cullFrame%2===0&&distanceCull)distanceCull();
if(cullFrame%30===0&&shadowCull)shadowCull();
{
// Move sun shadow camera to follow player for tight shadow coverage
if(!window._sunRef)window._sunRef=scene.children.find(c=>c.isDirectionalLight&&c.castShadow);
if(window._sunRef){window._sunRef.position.set(player.x+200,350,player.z-100);window._sunRef.target.position.set(player.x,player.y,player.z);window._sunRef.target.updateMatrixWorld()}}

// Stamina regeneration (slower when sprinting)
if(player.isSprinting)player.sta=Math.max(0,player.sta-0.05);
else player.sta=Math.min(player.sta+1,player.maxSta);
// Mana regeneration — base % of max mana per frame (not flat); consumables give burst regen
player.poi=Math.min(player.poi+player.maxPoi*0.003,player.maxPoi);
// Heal with A/Cross or key 3
if((keys['3']||gpButtons.a)&&!player._healCD&&player.hp<player.maxHp){player.hp=Math.min(player.hp+40,player.maxHp);player._healCD=60;log('Healed with Estus Flask','#4c4');hitFX(player.x,player.y+6,player.z,0x44cc44)}
if(player._healCD)player._healCD--;

if((keys[' ']||keys['KeySpace']||gpButtons.b)&&!player.rolling&&player.sta>24){player.rolling=true;player.rollT=22;player.sta-=24;skills.Agility.xp+=2;updateXpBar()}
if((keys['z']||keys['KeyZ']||gpButtons.y)&&player.grounded&&player.sta>10&&!player._jumpCD){player.vy=6.5;player.grounded=false;player.sta-=10;player._jumpCD=15;skills.Agility.xp+=1;updateXpBar()}
if(player._jumpCD)player._jumpCD--;
if(mouse.right||gpButtons.lt||gpButtons.lb){startBlock()}else{endBlock()}
// Gamepad: RB=parry riposte
if(gpButtons.rb&&!player._rbCD){doParry();player._rbCD=12}
if(player._rbCD)player._rbCD--;
if(gpButtons.start&&!player._stCD){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="inventory"]').classList.add('active');document.getElementById('tp-inventory').classList.add('active');player._stCD=20}
if(player._stCD)player._stCD--;
if(gpButtons.back&&!player._bkCD){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="skills"]').classList.add('active');document.getElementById('tp-skills').classList.add('active');player._bkCD=20}
if(player._bkCD)player._bkCD--;
// D-Pad tab switching
if(gpButtons.dUp&&!player._dUpCD){switchTab('prayer');player._dUpCD=20}
if(player._dUpCD)player._dUpCD--;
if(gpButtons.dDown&&!player._dDownCD){switchTab('skills');player._dDownCD=20}
if(player._dDownCD)player._dDownCD--;
if(gpButtons.dLeft&&!player._dLeftCD){switchTab('inventory');player._dLeftCD=20}
if(player._dLeftCD)player._dLeftCD--;
if(gpButtons.dRight&&!player._dRightCD){switchTab('combat');player._dRightCD=20}
if(player._dRightCD)player._dRightCD--;

playerGroup.position.set(player.x,player.y+1,player.z);playerGroup.rotation.y=player.ang;
// Rolling: full forward tumble (full body animation)
if(player.rolling){
const rPct=1-player.rollT/22;
playerGroup.rotation.x=rPct*Math.PI*2;
playerGroup.position.y+=Math.sin(rPct*Math.PI)*3;
// Tucked legs during roll
if(playerGroup.userData.lLeg)playerGroup.userData.lLeg.rotation.x=-0.5;
if(playerGroup.userData.rLeg)playerGroup.userData.rLeg.rotation.x=-0.5;
if(playerGroup.userData.lKnee)playerGroup.userData.lKnee.rotation.x=1.0;
if(playerGroup.userData.rKnee)playerGroup.userData.rKnee.rotation.x=1.0;
}else if(player.dashing){
// Dash animation - side tilt with lean
const dPct=1-player.dashT/12;
const leanDir=player.dashDir||1;
playerGroup.rotation.z=leanDir*Math.sin(dPct*Math.PI)*0.4;
playerGroup.position.y+=Math.sin(dPct*Math.PI)*0.5;
// Legs in running pose
if(playerGroup.userData.lLeg)playerGroup.userData.lLeg.rotation.x=leanDir*0.8;
if(playerGroup.userData.rLeg)playerGroup.userData.rLeg.rotation.x=-leanDir*0.8;
}else{
// New unified character animation system
animateCharacter(playerGroup,0.016);}

// Camera: always orbits behind player, player is always in frame
const camX=player.x+Math.sin(camYaw)*Math.cos(camPitch)*camDist;
const camZ=player.z+Math.cos(camYaw)*Math.cos(camPitch)*camDist;
const camY=player.y+Math.sin(camPitch)*camDist;
cam.position.x+=(camX-cam.position.x)*.1;cam.position.z+=(camZ-cam.position.z)*.1;cam.position.y+=(camY-cam.position.y)*.1;
// Camera always looks at player — lock-on does NOT move the camera
cam.lookAt(player.x,player.y+8,player.z);

for(let i=enemies.length-1;i>=0;i--){let e=enemies[i];
// Skip full AI for far-away enemies (performance: only process nearby)
const _edx=player.x-e.mesh.position.x,_edz=player.z-e.mesh.position.z,_eDist2=_edx*_edx+_edz*_edz;
if(_eDist2>250000){if(e.hp<=0){scene.remove(e.mesh);enemies.splice(i,1);if(lockOn===e)lockOn=null;const rt=e.type,rx=e.x,rz=e.z,rlv=getReg(rx,rz).lv;setTimeout(()=>{if(scene)spawnE(rt,rx+(Math.random()-.5)*30,rz+(Math.random()-.5)*30,rlv)},15000)}continue;}
// === STATUS EFFECTS PROCESSING ===
// Serpent Sting DoT
if(e.serpentSting&&e.stingT>0){e.stingT--;if(e.stingT%60===0){e.hp-=e.stingDmg||3;hitFX(e.mesh.position.x,e.mesh.position.y+6,e.mesh.position.z,0x00aa44);}if(e.stingT<=0)e.serpentSting=false;}
// Polymorph (sheep transform)
if(e.polymorphed&&e.polyT>0){e.polyT--;if(e.polyT<=0){e.polymorphed=false;if(e.sheepMesh){scene.remove(e.sheepMesh);e.sheepMesh=null;}e.mesh.visible=true;}}
// Slow effect from frostbolt
if(e.slowed&&e.slowT>0){e.slowT--;if(e.slowT<=0)e.slowed=false;}
// Counterspell silence
if(e.counterspelled&&e.counterT>0){e.counterT--;if(e.counterT<=0)e.counterspelled=false;}
// Hunter's Mark damage bonus tracking
if(e.huntersMark&&e.markT>0){e.markT--;if(e.markT<=0)e.huntersMark=false;}
// Skip movement/AI if enemy is staggered from parry (but still animate/draw)
if(e.staggered&&e.staggerT>0){e.staggerT--;e.mesh.position.y=Math.sin(time*20)*0.2;// Stagger shake
if(e.staggerT<=0)e.staggered=false;e.mesh.userData.animState='hit';animateCharacter(e.mesh,0.016);continue}
let dx=player.x-e.mesh.position.x,dz=player.z-e.mesh.position.z,dist=Math.hypot(dx,dz);
const faceAng=Math.atan2(dx,dz);
// === DRAGON AI: Flying and NPC Hunting ===
const isDragon=e.type==='dragon'||e.type==='bluedragon'||e.type==='greendragon'||e.type==='reddragon'||e.type==='blackdragon'||e.type==='irondragon'||e.type==='steeldragon'||e.type==='mithdragon'||e.type==='bronzedragon'||e.type==='runedragon'||e.type==='adamdragon'||e.type==='hydra'||e.type==='vorkath'||e.type==='rev_dragon';
if(isDragon){
const ud=e.mesh.userData;
// Initialize dragon state
if(typeof ud.isFlying==='undefined'){ud.isFlying=true;ud.flyHeight=40+Math.random()*20;ud.landing=false;ud.landTimer=0;}
const groundY=meshTerrainH(e.mesh.position.x,e.mesh.position.z);
// Dragons hunt NPCs - find nearest enemy target (not player, not other dragons)
let target=null;let targetDist=Infinity;
for(const other of enemies){
if(other===e)continue;// Skip self
const isOtherDragon=other.type==='dragon'||other.type==='bluedragon'||other.type==='greendragon'||other.type==='reddragon'||other.type==='blackdragon'||other.type==='irondragon'||other.type==='steeldragon'||other.type==='mithdragon'||other.type==='bronzedragon'||other.type==='runedragon'||other.type==='adamdragon'||other.type==='hydra'||other.type==='vorkath'||other.type==='rev_dragon';
if(isOtherDragon)continue;// Skip other dragons
const odx=other.mesh.position.x-e.mesh.position.x,odz=other.mesh.position.z-e.mesh.position.z;
const odist=Math.hypot(odx,odz);
if(odist<targetDist&&odist<150){targetDist=odist;target=other;}}
// Also consider player as target if no NPC found or player is closer
if(!target||dist<targetDist){target={mesh:{position:{x:player.x,y:player.y,z:player.z}},hp:player.hp,type:'player'};targetDist=dist;}
// Calculate direction to target
let tdx=target.mesh.position.x-e.mesh.position.x,tdz=target.mesh.position.z-e.mesh.position.z;
let tDist=Math.hypot(tdx,tdz);const tFaceAng=Math.atan2(tdx,tdz);
// Flying behavior - ALWAYS ACTIVE regardless of player distance
if(ud.isFlying){
const flyY=groundY+ud.flyHeight;e.mesh.position.y+=(flyY-e.mesh.position.y)*.05;
e.mesh.position.y+=Math.sin(time*2)*.2;// Bobbing
// Dragons always roam/patrol - expanded patrol radius and speed
ud.flyAng=(ud.flyAng||0)+.01; // Constant rotation
const patrolRadius=80+Math.sin(ud.flyAng*0.3)*40; // Varying radius
// Large roaming circle centered on spawn point
const targetX=e.x+Math.cos(ud.flyAng)*patrolRadius;
const targetZ=e.z+Math.sin(ud.flyAng)*patrolRadius;
// Smooth movement toward patrol point
const moveSpd=.12;
e.mesh.position.x+=(targetX-e.mesh.position.x)*moveSpd;
e.mesh.position.z+=(targetZ-e.mesh.position.z)*moveSpd;
// Face movement direction
const moveAng=Math.atan2(targetX-e.mesh.position.x,targetZ-e.mesh.position.z);
e.mesh.rotation.y+=((moveAng-e.mesh.rotation.y)*.05);
// If target in range, chase it while maintaining altitude
if(tDist<e.aggro*1.5){
const chaseSpd=.18;e.mesh.position.x+=Math.cos(tFaceAng)*chaseSpd;e.mesh.position.z+=Math.sin(tFaceAng)*chaseSpd;
e.mesh.rotation.y+=((tFaceAng-e.mesh.rotation.y)*.08);}}
// Wing animation
if(ud.wings){
const flapSpeed=ud.isFlying?10:4;const flapAmp=ud.isFlying?.8:.2;
ud.wings.forEach((w,wi)=>{w.rotation.z=(wi===0?1:-1)*Math.sin(time*flapSpeed)*flapAmp;});}
// Neck and tail animation
if(ud.neckSegs){ud.neckSegs.forEach((ns,ni)=>{ns.rotation.x=-.4+Math.sin(time*3+ni*.5)*.1;});}
if(ud.tailSegs){ud.tailSegs.forEach((ts,ti)=>{ts.rotation.x=-.2+ti*.05+Math.sin(time*2+ti*.3)*.15;});}
// Aerial fire breath attack
if(ud.isFlying&&tDist<e.atkRange&&e.atkCD<=0&&e.swingT<=0){
e.windUp++;
const windUpTime=25;
if(e.windUp>=windUpTime){
e.swingT=12;e.windUp=0;e.atkCD=40+Math.floor(Math.random()*20);
const dCol=e.type==='bluedragon'?0x4488ff:e.type==='greendragon'?0x44ff44:e.type==='blackdragon'?0x440000:e.type==='irondragon'?0xffaa44:e.type==='steeldragon'?0x8888aa:0xff4400;
const proj=new THREE.Mesh(new THREE.SphereGeometry(1.5,8,8),new MS({color:dCol,emissive:dCol,emissiveIntensity:3,transparent:true,opacity:.8}));
proj.position.copy(e.mesh.position);proj.position.y-=2;
const pAng=Math.atan2(target.mesh.position.z-e.mesh.position.z,target.mesh.position.x-e.mesh.position.x);
proj.userData={vx:Math.cos(pAng)*2,vz:Math.sin(pAng)*2,life:100,dmg:e.dmg*1.2,owner:e,target:target};
scene.add(proj);particles.push(proj);
hitFX(e.mesh.position.x,e.mesh.position.y-2,e.mesh.position.z,dCol);
if(target.type!=='player')log(e.type+' fire breath attacks '+target.type+'!','#f84');}}
else{// Ground combat
if(dist<e.aggro){
const stopDist=e.atkRange*.8;
// Chase player on ground
if(dist>stopDist&&e.swingT<=0){
const a=Math.atan2(dz,dx);const spd=.35;// Dragons move faster on ground
const targetX=e.mesh.position.x+Math.cos(a)*spd;
const targetZ=e.mesh.position.z+Math.sin(a)*spd;
e.mesh.position.x=targetX;e.mesh.position.z=targetZ;
// Push out of collision
const eco=pushOut(e.mesh.position.x,e.mesh.position.y,e.mesh.position.z);
e.mesh.position.x=eco.x;e.mesh.position.z=eco.z;
} else if(dist<stopDist*1.2&&e.swingT<=0){
// Circle when in melee range
e.strafeAng+=.012*e.strafeCW;
const sx=Math.cos(e.strafeAng)*.1,sz=Math.sin(e.strafeAng)*.1;
e.mesh.position.x+=sx;e.mesh.position.z+=sz;}
// Ground height adjustment
e.mesh.position.y=groundY+2;
e.mesh.rotation.y=faceAng;
// Attack logic
if(dist<e.atkRange&&e.atkCD<=0&&e.swingT<=0){
e.windUp++;
// Open jaw during windup
if(ud.jaw){ud.jaw.rotation.x=.3+Math.min(e.windUp*.02,.5);}
const windUpTime=24;
if(e.windUp>=windUpTime){
e.swingT=15;e.windUp=0;e.atkCD=40+Math.floor(Math.random()*16);
// Fire breath attack
const dCol=e.type==='bluedragon'?0x4488ff:e.type==='greendragon'?0x44ff44:e.type==='blackdragon'?0x440000:e.type==='irondragon'?0xffaa44:e.type==='steeldragon'?0x8888aa:0xff4400;
const proj=new THREE.Mesh(new THREE.SphereGeometry(1.2,8,8),new MS({color:dCol,emissive:dCol,emissiveIntensity:3,transparent:true,opacity:.8}));
proj.position.copy(e.mesh.position);proj.position.y+=3;
const pAng=Math.atan2(player.z-e.mesh.position.z,player.x-e.mesh.position.x);
proj.userData={vx:Math.cos(pAng)*1.8,vz:Math.sin(pAng)*1.8,life:90,dmg:e.dmg,owner:e};
scene.add(proj);particles.push(proj);
hitFX(e.mesh.position.x,e.mesh.position.y+3,e.mesh.position.z,dCol);
log(e.type+' breathes fire!','#f44');
// Close jaw after attack
if(ud.jaw){ud.jaw.rotation.x=0;}}}
else{e.windUp=Math.max(0,e.windUp-1);if(ud.jaw){ud.jaw.rotation.x*=0.9;}}}
// Swing animation on ground
if(e.swingT>0){e.swingT--;
if(ud.neck){ud.neck.rotation.x=.5*(1-e.swingT/15);}}}
// Update cooldowns
e.atkCD=Math.max(0,e.atkCD-1);
// HP bar positioning for dragons
if(e.mesh.userData.hpBar){const pct=Math.max(0,e.hp/e.maxHp);e.mesh.userData.hpBar.scale.x=pct;e.mesh.userData.hpBar.material.color.set(pct>.5?0x00cc00:pct>.25?0xccaa00:0xcc0000);
const barY=isDragon?14:10.5;e.mesh.userData.hpBar.position.y=barY;e.mesh.userData.hpBar.lookAt(cam.position)}
if(e.mesh.userData.nameLabel){e.mesh.userData.nameLabel.lookAt(cam.position)}
if(e.hp<=0){spawnLoot(e.mesh.position.x,e.mesh.position.z,e);scene.remove(e.mesh);enemies.splice(i,1);if(lockOn===e)lockOn=null;
const xpMult=Math.max(1,(e.lv||1)*.8);skills.Attack.xp+=Math.round(15*xpMult);skills.Strength.xp+=Math.round(12*xpMult);skills.Hitpoints.xp+=Math.round(10*xpMult);
log(e.type+' (Lv'+(e.lv||1)+') slain! +'+Math.round(37*xpMult)+'xp','#fa4');
updateXpBar();
const rt=e.type,rx=e.x,rz=e.z,rlv=getReg(rx,rz).lv;setTimeout(()=>{if(scene)spawnE(rt,rx+(Math.random()-.5)*30,rz+(Math.random()-.5)*30,rlv)},15000)}continue;}
// === END DRAGON AI ===
if(dist<e.aggro){
const isMelee=e.atkStyle==='slash'||e.atkStyle==='chop'||e.atkStyle==='smash'||e.atkStyle==='bite'||e.atkStyle==='swipe'||e.atkStyle==='charge'||e.atkStyle==='peck';
const stopDist=isMelee?e.atkRange*.7:e.atkRange*.85;
// Movement: approach until in range, then circle-strafe
if(dist>stopDist&&e.swingT<=0){
const a=Math.atan2(dz,dx);let spd=e.atkStyle==='charge'&&e.windUp>15?.6:.2;
if(e.slowed)spd*=0.5;// Frostbolt slow effect
if(e.polymorphed)spd=0;// Polymorphed enemies can't move
e.mesh.position.x+=Math.cos(a)*spd;e.mesh.position.z+=Math.sin(a)*spd;
} else if(dist<stopDist*1.3&&e.swingT<=0&&isMelee){
// Circle-strafe when in range and not attacking
let strafeSpd=e.slowed?0.007:0.015;e.strafeAng+=strafeSpd*e.strafeCW;
if(e.polymorphed){e.strafeAng+=0;}// Polymorphed enemies don't strafe
let sx=Math.cos(e.strafeAng)*.12,sz=Math.sin(e.strafeAng)*.12;
if(e.slowed){sx*=0.5;sz*=0.5;}// Slow affects strafe too
e.mesh.position.x+=sx;e.mesh.position.z+=sz;
}
const eco=pushOut(e.mesh.position.x,e.mesh.position.y,e.mesh.position.z);e.mesh.position.x=eco.x;e.mesh.position.z=eco.z;
const eh=surfaceH(e.mesh.position.x,e.mesh.position.z,e.mesh.position.y);e.mesh.position.y=eh+Math.sin(time*2+i)*.15;
e.mesh.rotation.y=faceAng;
// Animate enemy using unified character animation
// Determine enemy speed for walk/run detection
const ePrevX=e._prevX||e.mesh.position.x;const ePrevZ=e._prevZ||e.mesh.position.z;
const eSpeed=Math.hypot(e.mesh.position.x-ePrevX,e.mesh.position.z-ePrevZ);
e._prevX=e.mesh.position.x;e._prevZ=e.mesh.position.z;
// Store speed for animation scaling
e.mesh.userData.moveSpeed=eSpeed;
// Set enemy animation state based on behavior
if(e.staggered&&e.staggerT>0)e.mesh.userData.animState='hit';
else if(e.swingT>0)e.mesh.userData.animState='attack';
else if(eSpeed>0.15)e.mesh.userData.animState='run';// Fast movement = run
else if(eSpeed>0.02)e.mesh.userData.animState='walk';// Slow movement = walk
else e.mesh.userData.animState='idle';
// Animate with proper speed scaling
e.mesh.userData.animSpeed=0.5+eSpeed*2;// Speed up animation based on movement
animateCharacter(e.mesh,0.016);
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
// Check counterspell for magic attacks
if(e.counterspelled&&e.atkStyle==='magic'){hitFX(e.mesh.position.x,e.mesh.position.y+8,e.mesh.position.z,0xff0000);log('Enemy spell interrupted by Counterspell!','#f00');e.swingT=0;}
else if(e.atkStyle==='magic'||e.atkStyle==='breath'){
const pc=e.atkStyle==='magic'?0x6a1aaa:0xff4400;const pe=e.atkStyle==='magic'?0x4a0a8a:0xff2200;
const proj=new THREE.Mesh(new THREE.SphereGeometry(e.atkStyle==='breath'?1.2:.7,6,6),new MS({color:pc,emissive:pe,emissiveIntensity:3,transparent:true,opacity:.8}));
proj.position.copy(e.mesh.position);proj.position.y+=6;
const pAng=Math.atan2(player.z-e.mesh.position.z,player.x-e.mesh.position.x);
proj.userData={vx:Math.cos(pAng)*1.2,vz:Math.sin(pAng)*1.2,life:80,dmg:e.dmg,owner:e};
scene.add(proj);particles.push(proj);
} else {
// Melee: damage if still in range
if(dist<e.atkRange*1.15){
if(calcHit(e,player)){const gd=totalGear();let blockMult=player.blocking?.65:.3;const blocked=Math.floor(gd.def*blockMult);let realDmg=Math.max(1,e.dmg-blocked);
// Divine Shield makes player invulnerable
if(player._bubbleActive){hitFX(player.x,player.y+8,player.z,0xffffdd);log('Divine Shield absorbed all damage!','#ffd');}
else{
// Divine Protection reduces damage by 50%
if(player._divineProtActive)realDmg=Math.floor(realDmg*0.5);
player.hp-=realDmg;
if(player.blocking){player.sta-=8;skills.Defence.xp+=4;updateXpBar();hitFX(player.x,player.y+8,player.z,0x4488ff);log(`BLOCKED ${e.type}! -${realDmg} (absorbed ${blocked})`,'#48f')}
else{hitFX(player.x,player.y+8,player.z);log(`${e.type} hit for ${realDmg} (blocked ${blocked})`,'#f44');}}}}}
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
// Update name label to face camera
if(e.mesh.userData.nameLabel){e.mesh.userData.nameLabel.lookAt(cam.position)}
if(e.hp<=0){spawnLoot(e.mesh.position.x,e.mesh.position.z,e);scene.remove(e.mesh);enemies.splice(i,1);if(lockOn===e)lockOn=null;
const xpMult=Math.max(1,(e.lv||1)*.8);skills.Attack.xp+=Math.round(15*xpMult);skills.Strength.xp+=Math.round(12*xpMult);skills.Hitpoints.xp+=Math.round(10*xpMult);
log(e.type+' (Lv'+(e.lv||1)+') slain! +'+Math.round(37*xpMult)+'xp','#fa4');
// Immediate XP bar update
updateXpBar();
const rt=e.type,rx=e.x,rz=e.z,rlv=getReg(rx,rz).lv;setTimeout(()=>{if(scene)spawnE(rt,rx+(Math.random()-.5)*30,rz+(Math.random()-.5)*30,rlv)},15000)}}

// === DAMAGE BUFF CALCULATIONS (at attack time) ===
let dmgMult=1.0;if(player._battleShoutActive)dmgMult+=0.2;if(player._blessingActive)dmgMult+=0.15;if(player._sharpenActive)dmgMult+=0.1;if(player._reckActive)dmgMult+=0.5;
if((mouse.down||gpButtons.rt||gpButtons.x||keys['1'])&&player.atkCD<=0&&player.sta>19){player.atkCD=14;player.sta-=19;
const gStats=totalGear();let pDmg=Math.max(12,10+gStats.atk+gStats.str)*dmgMult;
if(lockOn&&lockOn.huntersMark)pDmg*=1.15;// Hunter's Mark bonus
if(lockOn&&lockOn.hp>0&&Math.hypot(lockOn.mesh.position.x-player.x,lockOn.mesh.position.z-player.z)<6){
lockOn.hp-=Math.round(pDmg);lockOn.poi-=16;hitFX(lockOn.mesh.position.x,lockOn.mesh.position.y+6,lockOn.mesh.position.z);
log('Hit '+lockOn.type+' for '+pDmg,'#ff8');
if(lockOn.poi<=0){lockOn.hp-=Math.round(pDmg*.5);lockOn.poi=30;log('POISE BREAK!','#ff4')}}
else{for(let i=enemies.length-1;i>=0;i--){let e=enemies[i],edx=e.mesh.position.x-player.x,edz=e.mesh.position.z-player.z;
if(Math.hypot(edx,edz)<6){const eAng=Math.atan2(edx,edz);let ad=eAng-player.ang;while(ad>Math.PI)ad-=Math.PI*2;while(ad<-Math.PI)ad+=Math.PI*2;
if(Math.abs(ad)<1.2&&calcHit(player,e)){let finalDmg=pDmg;if(e.huntersMark)finalDmg*=1.15;e.hp-=Math.round(finalDmg);hitFX(e.mesh.position.x,e.mesh.position.y+6,e.mesh.position.z);log('Hit '+e.type+' for '+Math.round(finalDmg),'#ff8')}}}}}
player.atkCD=Math.max(0,player.atkCD-1);if(player._parryCD)player._parryCD--;if(player._estusCD)player._estusCD--;if(player._shootCD)player._shootCD--;
// === WARRIOR COOLDOWNS ===
if(player._heroicCD)player._heroicCD--;if(player._cleaveCD)player._cleaveCD--;if(player._whirlCD)player._whirlCD--;if(player._thunderCD)player._thunderCD--;if(player._shoutCD)player._shoutCD--;if(player._executeCD)player._executeCD--;if(player._slamCD)player._slamCD--;if(player._overpowerCD)player._overpowerCD--;if(player._shieldCD)player._shieldCD--;if(player._reckCD)player._reckCD--;
// === KNIGHT COOLDOWNS ===
if(player._judgmentCD)player._judgmentCD--;if(player._crusaderCD)player._crusaderCD--;if(player._divineProtCD)player._divineProtCD--;if(player._consecrateCD)player._consecrateCD--;if(player._holyLightCD)player._holyLightCD--;if(player._flashLightCD)player._flashLightCD--;if(player._blessingCD)player._blessingCD--;if(player._bubbleCD)player._bubbleCD--;if(player._hammerCD)player._hammerCD--;if(player._exorcismCD)player._exorcismCD--;
// === SORCERER COOLDOWNS ===
if(player._fireballCD)player._fireballCD--;if(player._frostboltCD)player._frostboltCD--;if(player._missilesCD)player._missilesCD--;if(player._blizzardCD)player._blizzardCD--;if(player._fireblastCD)player._fireblastCD--;if(player._pyroCD)player._pyroCD--;if(player._novaCD)player._novaCD--;if(player._blinkCD)player._blinkCD--;if(player._polyCD)player._polyCD--;if(player._counterCD)player._counterCD--;
// === RANGER COOLDOWNS ===
if(player._steadyCD)player._steadyCD--;if(player._aimedCD)player._aimedCD--;if(player._multiCD)player._multiCD--;if(player._arcaneCD)player._arcaneCD--;if(player._stingCD)player._stingCD--;if(player._markCD)player._markCD--;if(player._distractCD)player._distractCD--;if(player._rapidCD)player._rapidCD--;if(player._feignCD)player._feignCD--;if(player._trapCD)player._trapCD--;
// === GENERAL COOLDOWNS ===
if(player._aidCD)player._aidCD--;if(player._bandageCD)player._bandageCD--;if(player._sharpenCD)player._sharpenCD--;if(player._mineStrikeCD)player._mineStrikeCD--;if(player._lumberCD)player._lumberCD--;if(player._campfireCD)player._campfireCD--;if(player._fishCastCD)player._fishCastCD--;if(player._focusCD)player._focusCD--;if(player._sneakCD)player._sneakCD--;if(player._agiRollCD)player._agiRollCD--;
// Update parry/block system
updateParrySystem()
// === EXPLOSIVE TRAP CHECKING ===
if(player.explosiveTrap&&player.explosiveTrap.life>0){player.explosiveTrap.life--;enemies.forEach(e=>{const dist=Math.hypot(e.x-player.explosiveTrap.x,e.z-player.explosiveTrap.z);if(dist<8){e.hp-=player.explosiveTrap.dmg;hitFX(e.mesh.position.x,e.mesh.position.y+5,e.mesh.position.z,0xff4400);player.explosiveTrap.life=0;}});if(player.explosiveTrap.life<=0){player.explosiveTrap=null;log('Explosive Trap triggered!','#f40');}}
// Loot label overlay — clear each frame
lootLabelCtx.clearRect(0,0,lootLabelCanvas.width,lootLabelCanvas.height);
let closestLoot=null,closestDist=Infinity;
const lootPromptEl=document.getElementById('loot-prompt');
for(let i=lootArr.length-1;i>=0;i--){let l=lootArr[i];
// Physics
if(!l.userData.settled){l.userData.vy-=.45;l.position.x+=l.userData.vx*.6;l.position.z+=l.userData.vz*.6;l.position.y+=l.userData.vy*.6;l.userData.vx*=.92;l.userData.vz*=.92;
const lh=meshTerrainH(l.position.x,l.position.z)+1.5;if(l.position.y<lh){l.position.y=lh;l.userData.vy*=-.4;if(Math.abs(l.userData.vy)<.5){l.userData.settled=true;l.position.y=lh}}}
l.userData.life--;
// DS glow pulse
const pulse=.85+Math.sin(time*4+i)*0.15;l.children[0].scale.setScalar(pulse);
l.rotation.y+=.03;
// Vertical hover once settled
if(l.userData.settled){l.position.y=meshTerrainH(l.position.x,l.position.z)+1.5+Math.sin(time*2+i*.5)*.4}
if(l.userData.life<=0){scene.remove(l);lootArr.splice(i,1);continue}
// Screen-space label
const lPos=new THREE.Vector3(l.position.x,l.position.y+3,l.position.z);
lPos.project(cam);
const sx=(lPos.x*.5+.5)*lootLabelCanvas.width;
const sy=(-.5*lPos.y+.5)*lootLabelCanvas.height;
if(lPos.z<1&&sx>0&&sx<lootLabelCanvas.width&&sy>0&&sy<lootLabelCanvas.height){
const ldist=Math.hypot(l.position.x-player.x,l.position.z-player.z);
if(ldist<80){
const alpha=Math.min(1,Math.max(.3,(80-ldist)/60));
const col=l.userData.gear?'rgba(255,215,0,'+alpha+')':l.userData.rarity==='common'?'rgba(200,200,170,'+alpha+')':'rgba(180,180,140,'+alpha+')';
lootLabelCtx.font='bold 12px "Times New Roman",serif';lootLabelCtx.textAlign='center';
lootLabelCtx.fillStyle='rgba(0,0,0,'+alpha*.6+')';lootLabelCtx.fillText(l.userData.item,sx+1,sy+1);
lootLabelCtx.fillStyle=col;lootLabelCtx.fillText(l.userData.item,sx,sy)}}
// Pickup check
const pDist=Math.hypot(l.position.x-player.x,l.position.z-player.z);
if(pDist<12&&pDist<closestDist){closestDist=pDist;closestLoot=l}
if(autoLoot&&pDist<7){
if(l.userData.gear){const g=l.userData.gear;equipped[g.slot]=g;updateEqUI();log('EQUIPPED: '+g.name+' [ATK+'+g.atk+' DEF+'+g.def+' STR+'+g.str+']','#0ff')}
if(inventory.length<28){inventory.push({name:l.userData.item,uid:l.userData.uid||null});updateInvUI();log('Picked up: '+l.userData.item,'#ff4');
const si=skillItems[l.userData.item];if(si){skills[si.skill].xp+=si.xp;
const lv=Math.max(skills[si.skill].lvl,Math.floor(1+Math.sqrt(skills[si.skill].xp/50)));
if(lv>skills[si.skill].lvl){skills[si.skill].lvl=lv;log(si.skill+' level up! Now '+lv,'#ff0')}
log(si.skill+' +'+si.xp+'xp','#cc4');updateSkillUI();updateXpBar()}}else log('Inventory full!','#f44');
scene.remove(l);lootArr.splice(i,1)}}
// Loot prompt for manual pickup
if(!autoLoot&&closestLoot&&closestDist<12){
lootPromptEl.classList.add('active');
lootPromptEl.querySelector('.lp-title').textContent=closestLoot.userData.item;
if(keys['KeyE']||gpButtons.x){const l=closestLoot;
if(l.userData.gear){const g=l.userData.gear;equipped[g.slot]=g;updateEqUI();log('EQUIPPED: '+g.name+' [ATK+'+g.atk+' DEF+'+g.def+' STR+'+g.str+']','#0ff')}
if(inventory.length<28){inventory.push({name:l.userData.item,uid:l.userData.uid||null});updateInvUI();log('Picked up: '+l.userData.item,'#ff4');
const si=skillItems[l.userData.item];if(si){skills[si.skill].xp+=si.xp;
const lv=Math.max(skills[si.skill].lvl,Math.floor(1+Math.sqrt(skills[si.skill].xp/50)));
if(lv>skills[si.skill].lvl){skills[si.skill].lvl=lv;log(si.skill+' level up! Now '+lv,'#ff0')}
log(si.skill+' +'+si.xp+'xp','#cc4');updateSkillUI();updateXpBar()}}else log('Inventory full!','#f44');
scene.remove(l);const idx=lootArr.indexOf(l);if(idx>=0)lootArr.splice(idx,1)}}
else{lootPromptEl.classList.remove('active')}

for(let i=particles.length-1;i>=0;i--){let p=particles[i];
// Enemy projectiles move straight (no gravity) and check player/NPC hit
if(p.userData.dmg&&!p.userData.type){
p.position.x+=p.userData.vx;p.position.z+=p.userData.vz;p.userData.life--;
// Check if dragon projectile (has target in userData)
if(p.userData.target&&p.userData.target.type!=='player'){
// Dragon fire breath hitting NPC
const target=p.userData.target;
if(target.hp>0){
const hitDist=Math.hypot(p.position.x-target.mesh.position.x,p.position.z-target.mesh.position.z);
if(hitDist<5){target.hp-=p.userData.dmg||20;hitFX(target.mesh.position.x,target.mesh.position.y+6,target.mesh.position.z,0xff4400);
log(p.userData.owner.type+' fire breath hits '+target.type+'!','#f84');
p.userData.life=0;}}}
// Check player hit
const pd=Math.hypot(p.position.x-player.x,p.position.z-player.z);
if(pd<4&&!player.rolling){const gd=totalGear();let blockMult=player.blocking?.65:.3;const blocked=Math.floor(gd.def*blockMult);const realDmg=Math.max(1,p.userData.dmg-blocked);
player.hp-=realDmg;hitFX(player.x,player.y+8,player.z,0x8844ff);
if(player.blocking)log(`BLOCKED projectile! -${realDmg}`,'#48f');else log(`Hit by projectile! -${realDmg}`,'#f44');
p.userData.life=0}
if(p.userData.life<=0){scene.remove(p);particles.splice(i,1)}}
// Player projectiles (arrows and spells) with gravity and enemy collision
else if(p.userData.type==='arrow'||p.userData.type==='spell'){
// Move with velocity and gravity
p.position.x+=p.userData.vx;p.position.z+=p.userData.vz;
p.position.y+=p.userData.vy;p.userData.vy-=p.userData.gravity;
// Orient arrow to face direction
if(p.userData.type==='arrow'){
const speed=Math.hypot(p.userData.vx,p.userData.vz);
if(speed>0.01){p.rotation.z=-Math.atan2(p.userData.vy,speed);}}
p.userData.life--;
// Ground collision
const groundH=meshTerrainH(p.position.x,p.position.z);
if(p.position.y<=groundH+0.5){
// Hit ground - stick for a moment then disappear
if(p.userData.type==='arrow'){
// Chance to retrieve arrow (50%)
if(Math.random()<0.5&&p.userData.life>5){
// Spawn retrievable arrow
const arrowLoot=makeLootMesh(0xaa8855,0.4);
arrowLoot.position.copy(p.position);arrowLoot.position.y=groundH+1;
arrowLoot.userData={item:'Single Arrow',life:3000,settled:true,uid:null};
scene.add(arrowLoot);lootArr.push(arrowLoot);}
p.userData.life=Math.min(p.userData.life,15);p.position.y=groundH+0.3;}
else{p.userData.life=0;}}
// Enemy collision check
for(const e of enemies){
const ex=e.mesh.position.x,ey=e.mesh.position.y+6,ez=e.mesh.position.z;
const dist=Math.hypot(p.position.x-ex,p.position.y-ey,p.position.z-ez);
if(dist<4&&e.hp>0){
// Hit enemy
let dmg=p.userData.dmg||15;
// Apply damage buffs to arrows
if(p.userData.type==='arrow'){let dmgMult=1.0;if(player._battleShoutActive)dmgMult+=0.2;if(player._blessingActive)dmgMult+=0.15;if(player._sharpenActive)dmgMult+=0.1;if(player._reckActive)dmgMult+=0.5;if(player._rapidFireActive)dmgMult+=0.2;if(e.huntersMark)dmgMult*=1.15;dmg=Math.round(dmg*dmgMult);}
e.hp-=dmg;e.poi-=10;hitFX(ex,ey,ez,0xff4400);
log((p.userData.type==='arrow'?'Arrow':'Spell')+' hit '+e.type+'! -'+dmg,'#8a4');
p.userData.life=0;break;}}
// Remove if life expired
if(p.userData.life<=0){scene.remove(p);particles.splice(i,1);}}
// Trail particles for spells
else if(p.userData.trail){
p.userData.life--;
if(p.userData.life<=0){scene.remove(p);particles.splice(i,1);}}
// Physics particles
else{p.position.x+=p.userData.vx*.14;p.position.y+=p.userData.vy*.14;p.position.z+=p.userData.vz*.14;p.userData.vy-=.5;p.userData.life--;p.scale.setScalar(Math.max(0,p.userData.life/22));if(p.userData.life<=0){scene.remove(p);particles.splice(i,1)}}}

// Animate torch meshes + assign 8 nearest PointLights
const sorted=torchPositions.map(t=>({...t,d:Math.hypot(t.x-player.x,t.z-player.z)})).sort((a,b)=>a.d-b.d);
for(let i=0;i<MAX_LIGHTS;i++){const l=lightPool[i];if(i<sorted.length&&sorted[i].d<200){const t=sorted[i];l.position.set(t.x,t.y,t.z);l.intensity=(t.big?3.5:1.8)+Math.sin(time*8+t.ph)*(t.big?1.2:.5);l.color.set(t.col||0xff8833);l.distance=t.big?50:40}else{l.intensity=0}}
torchPositions.forEach(t=>{if(t.mesh){t.mesh.position.y+=Math.sin(time*6+t.ph)*.015;t.mesh.scale.setScalar((t.big?1:.7)+Math.sin(time*10+t.ph)*(t.big?.25:.12))}});

if(dustPts){const dp=dustPts.geometry.attributes.position;for(let i=0;i<dp.count;i++){let y=dp.getY(i);y+=.012;if(y>55)y=5;dp.setY(i,y)}dp.needsUpdate=true;dustPts.position.set(player.x,0,player.z)}

if(riverMesh&&cullFrame%3===0){const wp=riverMesh.geometry.attributes.position;for(let i=0;i<wp.count;i++){wp.setZ(i,Math.sin(wp.getX(i)*.3+time*2)*.5+Math.cos(wp.getY(i)*.2+time*1.4)*.3)}wp.needsUpdate=true}

if(keys['f']||gpButtons.lb){const nT=Math.hypot(player.x+100,player.z-50)<50;const nR=Math.hypot(player.x+70,player.z+80)<40;
if(nT){skills.Woodcutting.xp+=18;hitFX(player.x,player.y+8,player.z,0x44aa22);log('Woodcutting +18xp','#6a4');updateXpBar()}
else if(nR){skills.Fishing.xp+=22;hitFX(player.x,player.y+8,player.z,0x2288ff);log('Fishing +22xp','#48f');updateXpBar()}}

// XP bar update function (for immediate updates)
// Uses proper OSRS-style combat level formula
function updateXpBar(){
// Check if combat skills need to level up (when XP exceeds threshold)
const cmbSkills=['Attack','Strength','Defence','Hitpoints','Prayer','Magic','Ranged'];
let leveledUp=false;
let combatLeveledUp=false;
// Store old combat level before checking individual skills
const oldBaseLvl=Math.floor((skills.Attack.lvl+skills.Strength.lvl+skills.Defence.lvl+skills.Hitpoints.lvl+skills.Prayer.lvl+skills.Magic.lvl+skills.Ranged.lvl)/4);
for(const skName of cmbSkills){
const sk=skills[skName];
// Calculate the actual level this skill should be at based on its XP
// Formula: Level = 1 + sqrt(XP/50)
const calculatedLvl=Math.min(99,Math.floor(1+Math.sqrt(sk.xp/50)));
if(calculatedLvl>sk.lvl){
const oldLvl=sk.lvl;
sk.lvl=calculatedLvl;
leveledUp=true;
log(skName+' leveled up to '+sk.lvl+'!','#ff0');
}
}
// Check if combat level increased
const newBaseLvl=Math.floor((skills.Attack.lvl+skills.Strength.lvl+skills.Defence.lvl+skills.Hitpoints.lvl+skills.Prayer.lvl+skills.Magic.lvl+skills.Ranged.lvl)/4);
if(newBaseLvl>oldBaseLvl){
combatLeveledUp=true;
log('Combat Level Up! Now Lv '+newBaseLvl,'#ffd700');
}
if(leveledUp||combatLeveledUp)updateSkillUI();
// Total combat XP is sum of all combat skill XP
const totalCmbXp=skills.Attack.xp+skills.Strength.xp+skills.Defence.xp+skills.Hitpoints.xp+skills.Prayer.xp+skills.Magic.xp+skills.Ranged.xp;
// Calculate combat level
const curCL=Math.max(1,newBaseLvl);
// XP formula: XP for level L = ((L-1)^2) * 50
// For combat level, it's based on average of 7 skills, so total XP needed = 7 * ((avgSkill-1)^2 * 50)
// Where avgSkill = combatLevel * 4 / 7 (OSRS formula)
function getTotalXpForCombatLevel(cmbLv){
const avgSkill=(cmbLv*4)/7;
return Math.floor(7*Math.pow(Math.max(0,avgSkill-1),2)*50);}
// Get XP thresholds
const curLevelXpNeeded=getTotalXpForCombatLevel(curCL);
const nextLevelXpNeeded=getTotalXpForCombatLevel(curCL+1);
// Calculate progress
let xpInCurrentLevel=Math.max(0,totalCmbXp-curLevelXpNeeded);
let xpNeededForNextLevel=Math.max(1,nextLevelXpNeeded-curLevelXpNeeded);
// Handle case where player has enough XP for next level but level hasn't updated yet
if(totalCmbXp>=nextLevelXpNeeded&&curCL<99){xpInCurrentLevel=0;xpNeededForNextLevel=1;}
// Calculate percentage
let pct=Math.min(100,Math.max(0,xpInCurrentLevel/xpNeededForNextLevel*100));
// If we're at 100% or more, force level up check for next iteration
if(pct>=99.9&&curCL<99){pct=100;}
// Update display
const xpFill=document.getElementById('xp-bar-fill');const xpText=document.getElementById('xp-bar-text');
if(xpFill)xpFill.style.width=pct+'%';
if(xpText){const displayHave=Math.floor(xpInCurrentLevel);const displayNeed=Math.floor(xpNeededForNextLevel);xpText.textContent='Combat Lv '+curCL+' ('+Math.floor(pct)+'%) - '+displayHave+'/'+displayNeed+' XP'}}

// Periodic UI updates (no level checks - handled in updateXpBar)
if(time*60%30<1){updateSkillUI();updateEqUI();
document.getElementById('orb-hp').textContent=Math.max(0,~~player.hp);
document.getElementById('orb-pray').textContent=skills.Prayer.lvl;
document.getElementById('orb-run').textContent=~~(player.sta/player.maxSta*100);
// Player frame
const cLv=Math.floor((skills.Attack.lvl+skills.Strength.lvl+skills.Defence.lvl+skills.Hitpoints.lvl+skills.Prayer.lvl+skills.Magic.lvl+skills.Ranged.lvl)/4);
const pfLv=document.getElementById('pf-level');if(pfLv)pfLv.textContent='Lv '+cLv;
// XP bar update
updateXpBar()
drawMinimap();}

// Action bar cooldowns — runs every frame for instant visual feedback
{const _abCDMap={attack:'atkCD',heal:'_estusCD',parry:'_parryCD',shoot:'_shootCD',spec_atk:'_specCD',
heroic_strike:'_heroicCD',cleave:'_cleaveCD',whirlwind:'_whirlCD',thunder_clap:'_thunderCD',battle_shout:'_shoutCD',execute:'_executeCD',slam:'_slamCD',overpower:'_overpowerCD',shield_slam:'_shieldCD',recklessness:'_reckCD',
judgment:'_judgmentCD',crusader_strike:'_crusaderCD',divine_protection:'_divineProtCD',consecration:'_consecrateCD',holy_light:'_holyLightCD',flash_light:'_flashLightCD',blessing_might:'_blessingCD',divine_shield:'_bubbleCD',hammer_justice:'_hammerCD',exorcism:'_exorcismCD',
fireball:'_fireballCD',frostbolt:'_frostboltCD',arcane_missiles:'_missilesCD',blizzard:'_blizzardCD',sorc_fire_blast:'_fireblastCD',pyroblast:'_pyroCD',frost_nova:'_novaCD',blink:'_blinkCD',polymorph:'_polyCD',counterspell:'_counterCD',
steady_shot:'_steadyCD',aimed_shot:'_aimedCD',multi_shot:'_multiCD',arcane_shot:'_arcaneCD',serpent_sting:'_stingCD',hunters_mark:'_markCD',distracting_shot:'_distractCD',rapid_fire:'_rapidCD',feign_death:'_feignCD',explosive_trap:'_trapCD',
first_aid:'_aidCD',bandage:'_bandageCD',sharpen_weapon:'_sharpenCD',mining_strike:'_mineStrikeCD',lumber_up:'_lumberCD',cooking_fire:'_campfireCD',fishing_cast:'_fishCastCD',runecraft_focus:'_focusCD',sneak_attack:'_sneakCD',agility_roll:'_agiRollCD'};
const abSlots=document.querySelectorAll('.ab-slot');
abSlots.forEach(s=>{const a=s.dataset.action;let cd=false;
if(a==='roll')cd=player.rolling;
else if(a==='dash_left'||a==='dash_right')cd=player.dashing;
else if(_abCDMap[a])cd=player[_abCDMap[a]]>0;
if(cd)s.classList.add('on-cd');else s.classList.remove('on-cd')});}

const hp=Math.max(0,player.hp/player.maxHp*100),st=player.sta/player.maxSta*100,po=player.poi/player.maxPoi*100;
document.getElementById('hpB').style.width=hp+'%';document.getElementById('stB').style.width=st+'%';document.getElementById('poB').style.width=po+'%';
document.getElementById('hpT').textContent=Math.max(0,~~player.hp)+'/'+player.maxHp;
document.getElementById('stT').textContent=~~player.sta+'/'+player.maxSta;document.getElementById('poT').textContent=~~player.poi+'/'+player.maxPoi;

if(player.hp<=0&&!player.dead){player.dead=true;player.deadTimer=3;document.getElementById('death-overlay').classList.add('active');log('YOU DIED','#f00')}

updateTargetFrame();
animateDungeonPortals();
if(ws&&ws.readyState===1&&++sendCt%3===0){ws.send(JSON.stringify({t:'p',id:myId,x:player.x,y:player.y,z:player.z,a:player.ang}))}

composer.render()}

window.addEventListener('keydown',e=>{
const k=e.key.toLowerCase();keys[k]=true;keys[e.code]=true;
if(k==='tab'){e.preventDefault();cycleLock()}
if(k==='f'&&gameStarted){e.preventDefault();toggleLock()}
if(k==='i'){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="inventory"]').classList.add('active');document.getElementById('tp-inventory').classList.add('active')}
if(k==='k'){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="skills"]').classList.add('active');document.getElementById('tp-skills').classList.add('active')}
if(k==='f5'){e.preventDefault();if(gameStarted)openSaveSlotMenu()}
// Action bar hotkeys 1-9 and 0(=10) for abilities
if(k>='1'&&k<='9'){
const slotIdx=parseInt(k)-1;// Convert '1' to slot 0, '2' to slot 1, etc.
if(typeof abAssign!=='undefined'&&abAssign[slotIdx]){
const abilityId=abAssign[slotIdx];
if(abilityId&&typeof execAbility==='function'){execAbility(abilityId);}}}
// Key 0 = slot 10 (Inventory)
if(k==='0'){if(typeof abAssign!=='undefined'&&abAssign[9]){execAbility(abAssign[9]);}}
// Key - = slot 11 (Skills)
if(k==='-'||k==='_'){if(typeof abAssign!=='undefined'&&abAssign[10]){execAbility(abAssign[10]);}}
// Key = = slot 12 (Save)
if(k==='='||k==='+'){if(typeof abAssign!=='undefined'&&abAssign[11]){execAbility(abAssign[11]);}}
// Legacy hardcoded keys for backwards compatibility (only if slot not assigned)
if(k==='2'&&!player._parryCD&&(!abAssign[1]||abAssign[1]==='parry')){doParry()}
if(k==='3'&&!player._estusCD&&(!abAssign[2]||abAssign[2]==='heal')){const heal=Math.round(player.maxHp*.3);player.hp=Math.min(player.hp+heal,player.maxHp);log('Used Estus Flask: +'+heal+' HP','#0f0');player._estusCD=90}
// Key 4 now defaults to shoot if not assigned
if(k==='4'&&(!abAssign[3]||abAssign[3]==='bones')){
if(typeof player!=='undefined'&&!player._shootCD){player._shootCD=40;shootProjectile('arrow',12+skills.Ranged.lvl);log('Shot arrow!','#8a4');}
else if(player._shootCD){log('Arrow on cooldown','#887');}}
if(k==='l'){autoLoot=!autoLoot;log('Auto-Loot: '+(autoLoot?'ON — items picked up automatically':'OFF — press E near items to pick up'),'#ffd700')}
// Debug: Toggle collision visualization with backslash
if(k==='\\'||k==='|'){toggleCollisionDebug();}
// FIX: Rebuild colliders to fix invisible barriers (Ctrl+R)
if(k==='r'&&e.ctrlKey){e.preventDefault();buildColliders();log('Colliders rebuilt - invisible barriers should be fixed','#0f0');}
// Q = Dash Left, E = Dash Right
if(k==='q'){e.preventDefault();execAbility('dash_left');}
if(k==='e'){e.preventDefault();execAbility('dash_right');}
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
if(k==='p'){const ab=document.getElementById('ability-browser');const sb=document.getElementById('spell-book');sb.classList.remove('active');ab.classList.toggle('active');if(ab.classList.contains('active')){buildAbCats();buildAbList()}}
if(k==='o'){const sb=document.getElementById('spell-book');const ab=document.getElementById('ability-browser');ab.classList.remove('active');sb.classList.toggle('active');if(sb.classList.contains('active')){buildSbCats();buildSbList()}}
if(k==='m'){const wm=document.getElementById('world-map');if(wm.classList.contains('active')){wm.classList.remove('active')}else{wm.classList.add('active');drawWorldMap()}}
if(k==='insert'){e.preventDefault();toggleEditorMode()}
if(k==='escape'){
const ed=document.getElementById('editor-mode');if(ed&&ed.style.display==='block'){toggleEditorMode();return}
const wm=document.getElementById('world-map');if(wm.classList.contains('active')){wm.classList.remove('active');return}
const sbr=document.getElementById('spell-book');if(sbr&&sbr.classList.contains('active')){sbr.classList.remove('active');return}
const abr=document.getElementById('ability-browser');if(abr&&abr.classList.contains('active')){abr.classList.remove('active');return}
const tp=document.getElementById('teleport-menu');if(tp&&showTeleport){showTeleport=false;tp.style.display='none';return}
const em=document.getElementById('esc-menu');em.classList.toggle('active');
if(em.classList.contains('active'))e.preventDefault()}
if(k==='g'&&gameStarted){e.preventDefault();const nT=Math.hypot(player.x+100,player.z-50)<50;const nR=Math.hypot(player.x+70,player.z+80)<40;const nM=Math.hypot(player.x-300,player.z+100)<60;
// Check for nearby harvestable plants first
let harvested=false;
if(typeof harvestablePlants!=='undefined'){
for(const p of harvestablePlants){if(Math.hypot(player.x-p.x,player.z-p.z)<10){
// Harvest the plant
if(inventory.length<28){inventory.push({name:p.item,uid:null});updateInvUI();}
const sk=skillItems[p.item]||{skill:'Farming',xp:10};
skills.Farming.xp+=sk.xp;updateXpBar();
hitFX(player.x,player.y+8,player.z,0x44aa22);
log('Harvested '+p.item+' +'+sk.xp+' Farming XP','#6a4');
// Remove plant temporarily (will respawn)
if(p.mesh){p.mesh.visible=false;}
setTimeout(()=>{if(p.mesh)p.mesh.visible=true;},p.respawn*1000);
harvested=true;break;}}}
if(!harvested){
if(nT){skills.Woodcutting.xp+=18;updateXpBar();log('Woodcutting +18xp','#6a4')}
else if(nR){skills.Fishing.xp+=22;updateXpBar();log('Fishing +22xp','#48f')}
else if(nM){skills.Mining.xp+=20;updateXpBar();log('Mining +20xp','#a86')}
else log('Nothing to gather here','#887')}}
});
// === ESC MENU LOGIC ===
{
const em=document.getElementById('esc-menu');
// Nav tab switching
document.querySelectorAll('.esc-nav-btn').forEach(btn=>{
btn.addEventListener('click',()=>{
document.querySelectorAll('.esc-nav-btn').forEach(b=>b.classList.remove('active'));
document.querySelectorAll('.esc-page').forEach(p=>p.classList.remove('active'));
btn.classList.add('active');
document.getElementById('ep-'+btn.dataset.page).classList.add('active')})});
// Resume
function closeEscMenu(){em.classList.remove('active')}
document.getElementById('esc-resume-btn').onclick=closeEscMenu;
document.getElementById('esc-save-btn').onclick=()=>{openSaveSlotMenu()};
document.getElementById('esc-savequit-btn').onclick=()=>{openSaveSlotMenu(true)};
document.getElementById('esc-quit-btn').onclick=()=>{if(typeof saveGame==='function')saveGame();location.reload()};
document.getElementById('esc-map-btn').onclick=()=>{closeEscMenu();const wm=document.getElementById('world-map');wm.classList.add('active');if(typeof drawWorldMap==='function')drawWorldMap()};
document.getElementById('esc-tele-btn').onclick=()=>{closeEscMenu();const t=document.getElementById('teleport-menu');if(t)t.style.display='block'};
document.getElementById('esc-inv-btn').onclick=()=>{closeEscMenu();document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="inventory"]').classList.add('active');document.getElementById('tp-inventory').classList.add('active')};
document.getElementById('esc-skills-btn').onclick=()=>{closeEscMenu();document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="skills"]').classList.add('active');document.getElementById('tp-skills').classList.add('active')};
document.getElementById('esc-ab-btn').onclick=()=>{closeEscMenu();document.getElementById('ability-browser').classList.add('active')};
document.getElementById('esc-openab-btn').onclick=()=>{closeEscMenu();document.getElementById('ability-browser').classList.add('active')};
// Toggle helpers
function makeToggle(id,values,onChange){const el=document.getElementById(id);let idx=0;el.addEventListener('click',()=>{idx=(idx+1)%values.length;el.textContent=values[idx];if(onChange)onChange(idx,values[idx])});return el}
// Settings toggles
makeToggle('opt-shadow',['High','Medium','Low'],(i)=>{if(renderer){renderer.shadowMap.enabled=i<2;renderer.shadowMap.type=i===0?THREE.PCFSoftShadowMap:THREE.BasicShadowMap}});
makeToggle('opt-bloom',['On','Off'],(i)=>{if(typeof bloomPass!=='undefined'&&bloomPass)bloomPass.strength=i===0?1.2:0});
makeToggle('opt-fog',['On','Off'],(i)=>{if(scene.fog)scene.fog.far=i===0?2200:99999});
makeToggle('opt-flipx',['Normal','Inverted'],(i)=>{if(typeof gameOpts!=='undefined')gameOpts.flipx=i===0?1:-1});
makeToggle('opt-flipy',['Normal','Inverted'],(i)=>{if(typeof gameOpts!=='undefined')gameOpts.flipy=i===0?1:-1});
makeToggle('opt-autoloot',['Off','On'],(i)=>{if(typeof autoLoot!=='undefined'){autoLoot=i===1;log('Auto-Loot '+(i===1?'ON':'OFF'),'#ffd700')}});
makeToggle('opt-autolk',['On','Off']);
makeToggle('opt-dmgnum',['On','Off']);
// Interface toggles
function makeHudToggle(id,targetSel){makeToggle(id,['Visible','Hidden'],(i)=>{const el=document.querySelector(targetSel);if(el)el.style.display=i===0?'':'none'})}
makeHudToggle('ui-actionbar','#action-bar');
makeHudToggle('ui-xpbar','#xp-bar-wrap');
makeHudToggle('ui-rpanel','#osrs-panel');
makeHudToggle('ui-mmap','#minimap-wrap');
makeHudToggle('ui-clog','#chat-log');
makeHudToggle('ui-lootlbl','#loot-label-canvas');
makeHudToggle('ui-tframe','#target-frame');
makeToggle('ui-rpos',['Right','Left'],(i)=>{const rp=document.getElementById('osrs-panel');if(rp){rp.style.right=i===0?'0':'auto';rp.style.left=i===0?'auto':'0'}});
makeToggle('ui-abpos',['Bottom Center','Bottom Left','Bottom Right'],(i)=>{const ab=document.getElementById('action-bar');if(ab){ab.style.left=i===0?'50%':i===1?'8px':'auto';ab.style.right=i===2?'8px':'auto';ab.style.transform=i===0?'translateX(-50%)':'none'}});
makeToggle('ui-font',['Normal','Large','Small'],(i)=>{document.documentElement.style.fontSize=i===0?'':''+[16,19,13][i]+'px'});

// === ACTION BAR CLICK HANDLERS ===
document.querySelectorAll('.ab-slot').forEach(slot=>{
slot.addEventListener('click',()=>{
const action=slot.dataset.action;
if(action==='save'&&gameStarted){openSaveSlotMenu();}
else if(action==='map'){const wm=document.getElementById('world-map');if(wm.classList.contains('active')){wm.classList.remove('active')}else{wm.classList.add('active');if(typeof drawWorldMap==='function')drawWorldMap()}}
else if(action==='inv'){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="inventory"]').classList.add('active');document.getElementById('tp-inventory').classList.add('active')}
else if(action==='skills'){document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-page').forEach(p=>p.classList.remove('active'));document.querySelector('[data-tab="skills"]').classList.add('active');document.getElementById('tp-skills').classList.add('active')}
});
});

// Keybind rebinder
const kbDefs=[['move_fwd','Move Forward','w'],['move_back','Move Back','s'],['move_left','Strafe Left','a'],['move_right','Strafe Right','d'],['jump','Jump','shift'],['roll','Roll / Dodge',' '],['attack','Attack','1'],['parry','Parry / Block','2'],['heal','Heal (Estus)','3'],['gather','Gather','g'],['lockon','Lock-On Toggle','f'],['interact','Interact','e'],['lockoncycle','Lock-On Cycle','tab'],['inventory','Inventory','i'],['skills','Skills','k'],['map','World Map','m'],['teleport','Teleport','t'],['abilities','Ability Browser','p'],['autoloot','Auto-Loot','l'],['sprint','Sprint','q'],['prayer','Prayer','5'],['dungeon','Dungeon / Gauntlet','u'],['save','Quick Save','f5']];
const kbMap={};kbDefs.forEach(([id,desc,def])=>{kbMap[id]={desc,key:def}});
const kbGrid=document.getElementById('kb-grid');
function buildKbGrid(){kbGrid.innerHTML='';kbDefs.forEach(([id,desc])=>{const entry=document.createElement('div');entry.className='ctrl-entry';const d=document.createElement('span');d.className='ctrl-desc';d.textContent=desc;const k=document.createElement('span');k.className='esc-keybind';k.textContent=kbMap[id].key.toUpperCase();k.dataset.id=id;
k.addEventListener('click',()=>{document.querySelectorAll('.esc-keybind.listening').forEach(el=>el.classList.remove('listening'));k.classList.add('listening');k.textContent='Press key…';
const onKey=(ev)=>{ev.preventDefault();const newKey=ev.key.toLowerCase();kbMap[id].key=newKey;k.textContent=newKey.toUpperCase();k.classList.remove('listening');window.removeEventListener('keydown',onKey,true)};window.addEventListener('keydown',onKey,true)});
entry.append(d,k);kbGrid.appendChild(entry)})}
buildKbGrid();
}
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
// === SAVE / LOAD SYSTEM (localStorage) with Multiple Slots ===
// Slots 1-10 = Manual saves, A = Auto-save 1, B = Auto-save 2
const SAVE_SLOTS=['1','2','3','4','5','6','7','8','9','10','A','B'];
const AUTO_SAVE_SLOTS=['A','B'];
const SAVE_PREFIX='soulscape_save_';
const SAVE_META_KEY='soulscape_save_meta';
let currentSaveSlot='1';
let lastAutoSaveSlot='A';

function getSaveKey(slot){return SAVE_PREFIX+slot}

function saveGame(slot){
slot=slot||currentSaveSlot;
try{const data={player:{x:player.x,z:player.z,hp:player.hp,maxHp:player.maxHp,sta:player.sta,maxSta:player.maxSta,poi:player.poi,maxPoi:player.maxPoi,speed:player.speed},
skills:{},inventory:[...inventory],equipped:{},opts:{...gameOpts},playerClass:playerClass,timestamp:Date.now(),slot:slot,ver:4};
skillDefs.forEach(s=>data.skills[s]={lvl:skills[s].lvl,xp:skills[s].xp});
gearSlots.forEach(s=>data.equipped[s]={...equipped[s]});
localStorage.setItem(getSaveKey(slot),JSON.stringify(data));
updateSaveMeta(slot,data);
log('Game saved to Slot '+slot+'!','#0f0');return true}catch(e){log('Save failed: '+e.message,'#f44');return false}}

function loadGame(slot){
slot=slot||currentSaveSlot;
try{const raw=localStorage.getItem(getSaveKey(slot));if(!raw)return false;
const data=JSON.parse(raw);
player.x=data.player.x;player.z=data.player.z;player.hp=data.player.hp;player.maxHp=data.player.maxHp;
player.sta=data.player.sta;player.maxSta=data.player.maxSta;player.poi=data.player.poi;player.maxPoi=data.player.maxPoi;
player.speed=data.player.speed||.42;player.y=meshTerrainH(player.x,player.z);
skillDefs.forEach(s=>{if(data.skills[s]){skills[s].lvl=data.skills[s].lvl;skills[s].xp=data.skills[s].xp}});
if(data.inventory){inventory.length=0;data.inventory.forEach(i=>inventory.push(i));updateInvUI()}
if(data.equipped){gearSlots.forEach(s=>{if(data.equipped[s])equipped[s]=data.equipped[s]})}
if(data.opts){Object.assign(gameOpts,data.opts)}
if(data.playerClass){playerClass=data.playerClass;currentSaveSlot=slot;}
updateSkillUI();updateEqUI();refreshPlayerModel();
document.getElementById('hpT').textContent=Math.round(player.hp)+'/'+player.maxHp;
document.getElementById('stT').textContent=Math.round(player.sta)+'/'+player.maxSta;
document.getElementById('poT').textContent=Math.round(player.poi)+'/'+player.maxPoi;
log('Loaded Slot '+slot+'! Pos: '+Math.round(player.x)+','+Math.round(player.z),'#0f0');
return true}catch(e){log('Load failed: '+e.message,'#f44');return false}}

function hasSave(slot){return !!localStorage.getItem(getSaveKey(slot||'1'))}
function hasAnySave(){return SAVE_SLOTS.some(s=>!!localStorage.getItem(getSaveKey(s)))}

function updateSaveMeta(slot,data){
try{
const metaRaw=localStorage.getItem(SAVE_META_KEY);
const meta=metaRaw?JSON.parse(metaRaw):{};
meta[slot]={
timestamp:data.timestamp||Date.now(),
playerClass:data.playerClass||'Unknown',
hp:data.player.hp,
maxHp:data.player.maxHp,
level:Math.max(...Object.values(data.skills).map(s=>s.lvl)),
playTime:Math.floor((Date.now()-(data.timestamp||Date.now()))/60000)
};
localStorage.setItem(SAVE_META_KEY,JSON.stringify(meta));
}catch(e){}}

function getSaveMeta(){
try{
const metaRaw=localStorage.getItem(SAVE_META_KEY);
return metaRaw?JSON.parse(metaRaw):{};
}catch(e){return{}}
}

function deleteSaveSlot(slot){
localStorage.removeItem(getSaveKey(slot));
const meta=getSaveMeta();
delete meta[slot];
localStorage.setItem(SAVE_META_KEY,JSON.stringify(meta));
log('Slot '+slot+' deleted','#f44');
}

// Auto-save every 30 seconds (alternates between A and B)
setInterval(()=>{
if(gameStarted&&!player.dead){
lastAutoSaveSlot=lastAutoSaveSlot==='A'?'B':'A';
saveGame(lastAutoSaveSlot);
}
},30000);

// Legacy compatibility - check for old save format
function migrateOldSave(){
const oldSave=localStorage.getItem('soulscape_save');
if(oldSave){
localStorage.setItem(getSaveKey('1'),oldSave);
localStorage.removeItem('soulscape_save');
updateSaveMeta('1',JSON.parse(oldSave));
log('Migrated old save to Slot 1','#0f0');
}
}

// === SAVE/LOAD SLOT MENU UI ===
function openSaveSlotMenu(quitAfter=false){
const existing=document.getElementById('save-slot-menu');
if(existing)existing.remove();
const menu=document.createElement('div');
menu.id='save-slot-menu';
menu.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:10000;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#ddd;font-family:monospace;';
const meta=getSaveMeta();
let html='<div style="background:rgba(20,15,10,0.95);border:2px solid #aa8833;border-radius:12px;padding:20px;max-width:600px;max-height:85vh;overflow-y:auto;">';
html+='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;border-bottom:2px solid #554422;padding-bottom:10px;">';
html+='<h2 style="margin:0;color:#ffd700;font-size:20px;">💾 Save Game</h2>';
html+='<span style="color:#887;font-size:12px;">Select a slot</span>';
html+='</div>';
// Manual saves (1-10)
html+='<div style="margin-bottom:15px;"><div style="color:#aa8833;font-size:12px;margin-bottom:8px;text-transform:uppercase;">Manual Saves</div>';
html+='<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;">';
for(let i=1;i<=10;i++){
const slot=i.toString();
const m=meta[slot];
const hasData=!!localStorage.getItem(getSaveKey(slot));
const classIcon={warrior:'⚔️',knight:'🛡️',sorcerer:'✨',deprived:'👤',ranger:'🏹'}[m?.playerClass]||'📄';
html+='<div onclick="selectSaveSlot(\''+slot+'\','+quitAfter+')" style="';
html+=hasData?'background:rgba(60,45,20,0.9);border:2px solid #aa8833;':'background:rgba(30,25,15,0.8);border:2px dashed #554422;';
html+='padding:10px;border-radius:8px;cursor:pointer;transition:all 0.2s;text-align:center;" onmouseover="this.style.background=\'rgba(80,65,30,0.95)\'" onmouseout="this.style.background='+(hasData?'\'rgba(60,45,20,0.9)\'':'\'rgba(30,25,15,0.8)\'')+'">';
html+='<div style="font-size:18px;color:#ffd700;font-weight:bold;">'+slot+'</div>';
if(hasData&&m){
html+='<div style="font-size:10px;color:#aa8833;">'+classIcon+' '+m.playerClass+'</div>';
html+='<div style="font-size:9px;color:#887;">Lv'+m.level+' HP:'+Math.round(m.hp)+'/'+m.maxHp+'</div>';
html+='<div style="font-size:8px;color:#665;">'+(new Date(m.timestamp).toLocaleDateString())+'</div>';
}else{
html+='<div style="font-size:10px;color:#554;">Empty</div>';
}
html+='</div>';
}
html+='</div></div>';
// Auto saves (A, B)
html+='<div style="margin-bottom:15px;"><div style="color:#aa8833;font-size:12px;margin-bottom:8px;text-transform:uppercase;">Auto-Save Slots</div>';
html+='<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;">';
['A','B'].forEach(slot=>{
const m=meta[slot];
const hasData=!!localStorage.getItem(getSaveKey(slot));
const classIcon={warrior:'⚔️',knight:'🛡️',sorcerer:'✨',deprived:'👤',ranger:'🏹'}[m?.playerClass]||'📄';
html+='<div onclick="selectSaveSlot(\''+slot+'\','+quitAfter+')" style="';
html+=hasData?'background:rgba(40,50,60,0.9);border:2px solid #458;':'background:rgba(20,25,30,0.8);border:2px dashed #335;';
html+='padding:12px;border-radius:8px;cursor:pointer;text-align:center;">';
html+='<div style="font-size:16px;color:#8bf;font-weight:bold;">🔄 Auto '+slot+'</div>';
if(hasData&&m){
html+='<div style="font-size:10px;color:#8af;">'+classIcon+' '+m.playerClass+'</div>';
html+='<div style="font-size:9px;color:#668;">Lv'+m.level+'</div>';
html+='<div style="font-size:8px;color:#446;">'+new Date(m.timestamp).toLocaleTimeString()+'</div>';
}else{
html+='<div style="font-size:10px;color:#335;">Empty</div>';
}
html+='</div>';
});
html+='</div></div>';
html+='<div style="display:flex;gap:10px;justify-content:center;">';
html+='<button onclick="closeSaveSlotMenu()" style="background:#443322;color:#ffd700;border:2px solid #aa8833;padding:8px 20px;cursor:pointer;border-radius:6px;font-size:12px;">Cancel</button>';
html+='</div>';
html+='</div>';
menu.innerHTML=html;
document.body.appendChild(menu);
}

function openLoadSlotMenu(){
const existing=document.getElementById('save-slot-menu');
if(existing)existing.remove();
const menu=document.createElement('div');
menu.id='save-slot-menu';
menu.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:10000;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#ddd;font-family:monospace;';
const meta=getSaveMeta();
let html='<div style="background:rgba(20,15,10,0.95);border:2px solid #aa8833;border-radius:12px;padding:20px;max-width:600px;max-height:85vh;overflow-y:auto;">';
html+='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;border-bottom:2px solid #554422;padding-bottom:10px;">';
html+='<h2 style="margin:0;color:#ffd700;font-size:20px;">📂 Load Game</h2>';
html+='<span style="color:#887;font-size:12px;">Select a save to continue</span>';
html+='</div>';
// Show all slots that have data
const availableSlots=SAVE_SLOTS.filter(s=>!!localStorage.getItem(getSaveKey(s)));
if(availableSlots.length===0){
html+='<div style="text-align:center;padding:40px;color:#665;"><div style="font-size:48px;margin-bottom:10px;">📭</div><div>No save files found</div></div>';
}else{
// Manual saves
const manual=availableSlots.filter(s=>!AUTO_SAVE_SLOTS.includes(s));
if(manual.length>0){
html+='<div style="margin-bottom:15px;"><div style="color:#aa8833;font-size:12px;margin-bottom:8px;text-transform:uppercase;">Manual Saves</div>';
html+='<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;">';
manual.forEach(slot=>{
const m=meta[slot];
const classIcon={warrior:'⚔️',knight:'🛡️',sorcerer:'✨',deprived:'👤',ranger:'🏹'}[m?.playerClass]||'📄';
html+='<div onclick="loadFromSlot(\''+slot+'\')" style="background:rgba(60,45,20,0.9);border:2px solid #aa8833;padding:10px;border-radius:8px;cursor:pointer;transition:all 0.2s;text-align:center;" onmouseover="this.style.background=\'rgba(80,65,30,0.95)\'" onmouseout="this.style.background=\'rgba(60,45,20,0.9)\'">';
html+='<div style="font-size:18px;color:#ffd700;font-weight:bold;">'+slot+'</div>';
html+='<div style="font-size:10px;color:#aa8833;">'+classIcon+' '+m.playerClass+'</div>';
html+='<div style="font-size:9px;color:#887;">Lv'+m.level+' HP:'+Math.round(m.hp)+'/'+m.maxHp+'</div>';
html+='<div style="font-size:8px;color:#665;">'+(new Date(m.timestamp).toLocaleDateString())+'</div>';
html+='<button onclick="event.stopPropagation();deleteSlotPrompt(\''+slot+'\')" style="background:#442222;color:#f44;border:1px solid #a33;padding:2px 6px;margin-top:5px;cursor:pointer;border-radius:3px;font-size:8px;">🗑️</button>';
html+='</div>';
});
html+='</div></div>';
}
// Auto saves
const auto=availableSlots.filter(s=>AUTO_SAVE_SLOTS.includes(s));
if(auto.length>0){
html+='<div style="margin-bottom:15px;"><div style="color:#aa8833;font-size:12px;margin-bottom:8px;text-transform:uppercase;">Auto-Saves</div>';
html+='<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;">';
auto.forEach(slot=>{
const m=meta[slot];
const classIcon={warrior:'⚔️',knight:'🛡️',sorcerer:'✨',deprived:'👤',ranger:'🏹'}[m?.playerClass]||'📄';
html+='<div onclick="loadFromSlot(\''+slot+'\')" style="background:rgba(40,50,60,0.9);border:2px solid #458;padding:12px;border-radius:8px;cursor:pointer;text-align:center;">';
html+='<div style="font-size:16px;color:#8bf;font-weight:bold;">🔄 Auto '+slot+'</div>';
html+='<div style="font-size:10px;color:#8af;">'+classIcon+' '+m.playerClass+'</div>';
html+='<div style="font-size:9px;color:#668;">Lv'+m.level+'</div>';
html+='<div style="font-size:8px;color:#446;">'+new Date(m.timestamp).toLocaleTimeString()+'</div>';
html+='</div>';
});
html+='</div></div>';
}
}
html+='<div style="display:flex;gap:10px;justify-content:center;">';
html+='<button onclick="closeSaveSlotMenu()" style="background:#443322;color:#ffd700;border:2px solid #aa8833;padding:8px 20px;cursor:pointer;border-radius:6px;font-size:12px;">Cancel</button>';
html+='</div>';
html+='</div>';
menu.innerHTML=html;
document.body.appendChild(menu);
}

function selectSaveSlot(slot,quitAfter){
if(confirm('Save to Slot '+slot+'?')){
saveGame(slot);
closeSaveSlotMenu();
if(quitAfter){
log('Saved to Slot '+slot+' — Quitting...','#0f0');
setTimeout(()=>location.reload(),500);
}
}
}

function loadFromSlot(slot){
if(confirm('Load from Slot '+slot+'? Unsaved progress will be lost.')){
closeSaveSlotMenu();
if(loadGame(slot)){
setTimeout(()=>{
if(!gameStarted)startGame(true);
},100);
}
}
}

function deleteSlotPrompt(slot){
if(confirm('Delete save in Slot '+slot+'? This cannot be undone!')){
deleteSaveSlot(slot);
closeSaveSlotMenu();
setTimeout(openLoadSlotMenu,100);
}
}

function closeSaveSlotMenu(){
const menu=document.getElementById('save-slot-menu');
if(menu)menu.remove();
}

// Expose to global scope
window.selectSaveSlot=selectSaveSlot;
window.loadFromSlot=loadFromSlot;
window.deleteSlotPrompt=deleteSlotPrompt;
window.closeSaveSlotMenu=closeSaveSlotMenu;

// === MENU & OPTIONS LOGIC ===
const gameOpts={blood:true,particles:true,flipy:1,flipx:1,sens:5,bloom:true,bright:1.15};
const classStats={warrior:{hp:160,sta:110,poi:60},knight:{hp:180,sta:90,poi:68},sorcerer:{hp:100,sta:80,poi:140},deprived:{hp:80,sta:80,poi:80},ranger:{hp:120,sta:100,poi:90}};
let gameStarted=false;

function startGame(isLoad){
document.getElementById('main-menu').classList.add('hidden');
document.getElementById('char-create').classList.remove('show');
document.getElementById('game-ui').style.display='block';
document.getElementById('osrs-panel').style.display='flex';
document.getElementById('chatbox').style.display='flex';
document.getElementById('action-bar').classList.add('active');
document.getElementById('xp-bar-wrap').classList.add('active');
document.getElementById('esc-hud-btn').classList.add('active');
document.body.style.cursor='crosshair';
if(!gameStarted){gameStarted=true;
try{init();if(isLoad)loadGame();updateSkillUI();updateEqUI();loop();connectMP()}catch(err){const cl=document.getElementById('chat-log');if(cl)cl.innerHTML='<div style="color:red;font-size:14px">ERROR: '+err.message+'<br>'+err.stack+'</div>';console.error(err)}}}

document.querySelectorAll('.mi').forEach(el=>el.addEventListener('click',()=>{
const a=el.dataset.a;
if(a==='new'){document.getElementById('main-menu').classList.add('hidden');document.getElementById('char-create').classList.add('show')}
else if(a==='cont'){migrateOldSave();if(hasAnySave()){openLoadSlotMenu()}else{log('No save files found!','#f44')}}
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
const classIcons={warrior:'\u2694',knight:'\u2694',sorcerer:'\u2728',deprived:'\uD83D\uDC64',ranger:'\uD83C\uDFF9'};
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
}else if(cls==='ranger'){
equipped.Helm=none;equipped.Chest={name:'Leather Body',atk:0,def:6,str:1};
equipped.Legs={name:'Leather Chaps',atk:0,def:5,str:1};equipped.Boots={name:'Leather Boots',atk:0,def:2,str:0};
equipped.Gloves={name:'Leather Vambraces',atk:2,def:2,str:1};equipped.Shield=none;
equipped.Weapon={name:'Maple Shortbow',atk:15,def:0,str:0};equipped.Ring=none;
}
setTimeout(()=>{startGame(false)},500)}));

// ============================================================
// === CORRUPTED GAUNTLET — Complete Dungeon System ============
// ============================================================
const GAU_X=-2000,GAU_Z=-2000; // Surface location in wilderness (behind walls)
let gau=null; // active gauntlet state

// --- Gauntlet HUD elements (created once) ---
let gauHud=null;
function _mkGauHud(){
if(gauHud)return;
gauHud=document.createElement('div');
gauHud.id='gau-hud';
gauHud.style.cssText='position:fixed;left:50%;transform:translateX(-50%);top:8px;z-index:8000;display:none;font-family:"Times New Roman",serif;pointer-events:none;text-align:center;min-width:360px';
gauHud.innerHTML=
'<div id="gau-phase" style="font-size:13px;color:#e040fb;letter-spacing:2px;text-transform:uppercase;text-shadow:0 0 12px #e040fb88;margin-bottom:2px"></div>'+
'<div id="gau-timer" style="font-size:22px;color:#ffd700;font-weight:700;text-shadow:0 2px 8px #000;margin-bottom:2px"></div>'+
'<div id="gau-hint-wrap" style="background:rgba(14,10,6,.88);border:1px solid #5a4a32;border-radius:5px;padding:4px 12px;margin:0 auto;max-width:440px;pointer-events:auto">'+
'<div id="gau-hint" style="font-size:11px;color:#c8a96e;line-height:1.5"></div>'+
'</div>'+
'<div id="gau-atk-tracker" style="margin-top:4px;font-size:10px;color:#aaa;display:flex;justify-content:center;gap:4px"></div>'+
'<div id="gau-style-ind" style="margin-top:3px;font-size:11px;color:#8af;letter-spacing:1px">⚔ Melee &nbsp;|&nbsp; Press <b style=\'color:#ffd700\'>R</b> to switch style</div>'+
'<div id="gau-res" style="margin-top:3px;font-size:10px;color:#88c;letter-spacing:1px"></div>';
document.body.appendChild(gauHud);}

// --- Step hints per phase ---
const GAU_HINTS={
intro:[
'Welcome to the Corrupted Gauntlet! You have 9 minutes to prepare and defeat the Hunllef.',
'START: Explore the 7x7 dungeon grid. Kill weak monsters for Corrupted Shards & a Weapon Frame.',
'Tip: Make a clockwise loop around the starting room to hit all adjacent resource nodes.'
],
gather:[
'GATHER PHASE: Kill Corrupted creatures — collect Shards, Ore, Bark, and Linum.',
'Visit the Singing Bowl in the start room to craft Tier-2 weapons and armour.',
'Find Fishing Spots for Raw Paddlefish (food). Cook them at a fire before the boss!',
'Hunt the 3 Demi-Bosses: Corrupted Bear (Spike), Dark Beast (Bowstring), Dragon (Orb).',
'Use the Teleport Crystal to return to start room when ready.',
'Craft Tier-3 weapons (Perfected Bow + Staff), Armour (120 shards), 2 Egniol Potions.'
],
boss:[
'BOSS: The Corrupted Hunllef — Lv 674. Switch prayer every 4 attacks!',
'It STARTS with Ranged (green orb). Use Protect from Missiles first.',
'After 4 attacks it switches to Magic (purple orb). Switch to Protect from Magic.',
'Every 6 attacks YOU deal, Hunllef switches its protection prayer — change attack style!',
'TORNADOES appear — RUN from purple spinning orbs. They deal ~15 dmg/tick on contact.',
'FLOOR TILES turn orange — avoid them! Move constantly around the arena.',
'Below 300 HP: more tornadoes, faster tile changes. Stay mobile!',
'TRAMPLE: Never stand directly underneath the Hunllef — it deals 50+ damage.',
'Drink Egniol Potion if HP drops below 40. Keep prayer points above 0!'
],
complete:[
'VICTORY! The Hunllef is slain. Claim your reward from the Reward Chest!',
'Enhanced Crystal seeds have a rare chance to drop. Keep running for the best loot!'
]};

function _gauHint(msg,col){
const el=document.getElementById('gau-hint');if(!el)return;
if(!dungeonHintsOn){el.textContent='';return}
el.style.color=col||'#c8a96e';el.textContent=msg;}
function _gauPhase(txt){const el=document.getElementById('gau-phase');if(el)el.textContent=txt;}
function _gauRes(){
if(!gau)return;
const el=document.getElementById('gau-res');if(!el)return;
el.textContent='Shards:'+gau.shards+' Ore:'+gau.ore+' Bark:'+gau.bark+' Linum:'+gau.linum+' Fish:'+gau.fish+' Frame:'+(gau.frames>0?'✓':'✗')+' Vials:'+gau.vials;}
function _gauAtkTracker(){
if(!gau||!gauntletAtkOn)return;
const el=document.getElementById('gau-atk-tracker');if(!el)return;
if(gau.phase!=='boss'){el.innerHTML='';return}
const h=gau.hunllef;
let html='<span style="color:#aaa;margin-right:4px">Hunllef atks:</span>';
for(let i=0;i<4;i++){const done=i<h.atkCount;html+='<span style="color:'+(done?'#f44':'#444')+';font-size:14px">●</span>'}
html+='<span style="color:#aaa;margin:0 6px">|</span>';
html+='<span style="color:#aaa;margin-right:4px">Your style-switch:</span>';
for(let i=0;i<6;i++){const done=i<h.playerAtkCount;html+='<span style="color:'+(done?'#4cf':'#444')+';font-size:14px">●</span>'}
html+='<span style="color:#ffd700;margin-left:8px">Prayer: '+(h.mode==='ranged'?'🏹 Missiles':'🔮 Magic')+'</span>';
el.innerHTML=html;}

// Build the Gauntlet 3D scene
function _buildGauntletArena(){
const g=new THREE.Group();g.name='gauntlet_arena';
const corrupted=new MS({color:0x3a0a5a,roughness:.8,metalness:.1});
const corruptedLt=new MS({color:0x5a1a7a,roughness:.7,metalness:.15});
const crystalMat=new MS({color:0x9a40cc,emissive:0x5a10aa,emissiveIntensity:.4,roughness:.3,metalness:.3,transparent:true,opacity:.9});
const floorMat=new MS({color:0x1a0a2a,roughness:.95});
// Arena size: 7x7 rooms of 14x14 each = ~100x100 units total
const CELL=16,COLS=7,ROWS=7;
const offX=GAU_X-COLS*CELL/2,offZ=GAU_Z-ROWS*CELL/2;
// Floor - raised platform so it's clearly above ground
const platformH=2;
const floor=new THREE.Mesh(new THREE.BoxGeometry(COLS*CELL,platformH,ROWS*CELL),floorMat);
floor.position.set(GAU_X,platformH/2,GAU_Z);floor.receiveShadow=true;g.add(floor);
// Low outer barriers (waist height) - not walls - so player can see sky
const barrierH=3;const barrierMat=corrupted;
[[GAU_X,GAU_Z-ROWS*CELL/2,COLS*CELL,barrierH,1],[GAU_X,GAU_Z+ROWS*CELL/2,COLS*CELL,barrierH,1],
[GAU_X-COLS*CELL/2,GAU_Z,1,barrierH,ROWS*CELL],[GAU_X+COLS*CELL/2,GAU_Z,1,barrierH,ROWS*CELL]].forEach(([x,z,w,h,d])=>{
const bm=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),barrierMat);bm.position.set(x,platformH+h/2,z);bm.castShadow=true;g.add(bm)});
// Low room dividers - corrupted crystal barriers (waist height, not full walls)
for(let row=0;row<ROWS;row++){for(let col=0;col<COLS;col++){
const cx=offX+col*CELL+CELL/2,cz=offZ+row*CELL+CELL/2;
// Low E barrier
if(col<COLS-1&&Math.random()>.4){const bm=new THREE.Mesh(new THREE.BoxGeometry(.5,2,3),barrierMat);bm.position.set(cx+CELL/2,platformH+1,cz);g.add(bm)}
// Low N barrier
if(row<ROWS-1&&Math.random()>.4){const bm=new THREE.Mesh(new THREE.BoxGeometry(3,2,.5),barrierMat);bm.position.set(cx,platformH+1,cz+CELL/2);g.add(bm)}
// Crystal decor
if(Math.random()<.18){const cr=new THREE.Mesh(new THREE.ConeGeometry(.3+Math.random()*.5,1.5+Math.random(),5),crystalMat);cr.position.set(cx+(Math.random()-.5)*CELL*.7,platformH+1+Math.random()*2,cz+(Math.random()-.5)*CELL*.7);cr.rotation.set(Math.random()*.3,Math.random()*Math.PI,Math.random()*.3);cr.castShadow=true;g.add(cr)}}}
// Corner pillars (tall but thin - like corrupted obelisks)
[[-1,-1],[-1,1],[1,-1],[1,1]].forEach(([sx,sz])=>{
const px=GAU_X+sx*COLS*CELL/2,pz=GAU_Z+sz*ROWS*CELL/2;
const pillar=new THREE.Mesh(new THREE.CylinderGeometry(1.5,2,12,6),new MS({color:0x3a0a5a,emissive:0x1a0050,emissiveIntensity:.3}));
pillar.position.set(px,platformH+6,pz);g.add(pillar);});
// Boss chamber — center (3,3) — mark with purple glow floor on platform
const bcx=offX+3*CELL+CELL/2,bcz=offZ+3*CELL+CELL/2;
const bossFl=new THREE.Mesh(new THREE.BoxGeometry(CELL-1,0.2,CELL-1),new MS({color:0x5a0a8a,emissive:0x3a0070,emissiveIntensity:.6}));
bossFl.position.set(bcx,platformH+.1,bcz);g.add(bossFl);
// Starting room — top-left corner with Singing Bowl
const startX=offX+0*CELL+CELL/2,startZ=offZ+0*CELL+CELL/2;
// Singing Bowl on platform
const bowlY=platformH+1;
const bowl=new THREE.Mesh(new THREE.TorusGeometry(1.8,.4,8,16),new MS({color:0xcc88ff,emissive:0x8844cc,emissiveIntensity:.8}));
bowl.position.set(startX+3,bowlY,startZ+3);bowl.rotation.x=Math.PI/2;g.add(bowl);
const bowlBase=new THREE.Mesh(new THREE.CylinderGeometry(.5,.7,1.2,8),new MS({color:0x8844aa,roughness:.4}));
bowlBase.position.set(startX+3,bowlY-.4,startZ+3);g.add(bowlBase);
// Ambient corrupt lighting
const aLight=new THREE.PointLight(0x8822cc,.6,120);aLight.position.set(GAU_X,8,GAU_Z);g.add(aLight);
const bLight=new THREE.PointLight(0xcc2288,.4,80);bLight.position.set(startX,6,startZ);g.add(bLight);
// Store key positions in group userdata
g.userData={startX,startZ,bcx,bcz,CELL,COLS,ROWS,offX,offZ,bowlPos:{x:startX+3,z:startZ+3}};
return g;}

// Resource node meshes scattered in grid - placed on platform
function _buildGauntletResources(arenaGroup){
const {CELL,COLS,ROWS,offX,offZ,startX,startZ,bcx,bcz}=arenaGroup.userData;
const nodes=[];
const platformH=2; // Same as arena platform
const ore=new MS({color:0x4a2a6a,emissive:0x2a1040,emissiveIntensity:.3,roughness:.6});
const tree=new MS({color:0x2a4a1a,roughness:.9});
const fish=new MS({color:0x1a3a5a,emissive:0x0a1a3a,emissiveIntensity:.2});
for(let row=0;row<ROWS;row++){for(let col=0;col<COLS;col++){
const cx=offX+col*CELL+CELL/2,cz=offZ+row*CELL+CELL/2;
const isBoss=(col===3&&row===3),isStart=(col===0&&row===0);
if(isBoss||isStart)continue;
const r=Math.random();
let mesh,type;
if(r<.25){// Ore rock - sits on platform
mesh=new THREE.Mesh(new THREE.DodecahedronGeometry(1.2,0),ore);
mesh.position.set(cx+(Math.random()-.5)*6,platformH+1,cz+(Math.random()-.5)*6);
type='ore';
}else if(r<.48){// Tree/bark - on platform
mesh=new THREE.Mesh(new THREE.CylinderGeometry(.4,.55,3.5,7),new MS({color:0x3a2a1a,roughness:.9}));
mesh.position.set(cx+(Math.random()-.5)*6,platformH+1.75,cz+(Math.random()-.5)*6);
const leaves=new THREE.Mesh(new THREE.ConeGeometry(1.8,2.5,7),new MS({color:0x1a3a2a,roughness:.85}));
leaves.position.set(0,3,0);mesh.add(leaves);
type='bark';
}else if(r<.65){// Fishing spot - on platform
mesh=new THREE.Mesh(new THREE.CylinderGeometry(1.2,1.4,.2,12),fish);
mesh.position.set(cx+(Math.random()-.5)*4,platformH+.1,cz+(Math.random()-.5)*4);
type='fishing';
}else if(r<.78){// Linum plant - on platform
mesh=new THREE.Mesh(new THREE.SphereGeometry(.7,5,5),new MS({color:0x4a5a2a,roughness:.9}));
mesh.position.set(cx+(Math.random()-.5)*7,platformH+.7,cz+(Math.random()-.5)*7);
type='linum';
}else continue;
mesh.castShadow=true;arenaGroup.add(mesh);
nodes.push({mesh,type,depleted:false,col,row});}
}return nodes;}

// Mini-boss types
const GAU_DEMIBOSS=[
{type:'bear',name:'Corrupted Bear',hp:180,col:0x5a3a8a,reward:{item:'Corrupted Spike',type:'spike'},weapon:'melee'},
{type:'darkbeast',name:'Corrupted Dark Beast',hp:220,col:0x4a1a6a,reward:{item:'Crystalline Bowstring',type:'bow'},weapon:'ranged'},
{type:'dragon',name:'Corrupted Dragon',hp:260,col:0x3a0a5a,reward:{item:'Crystal Orb',type:'magic'},weapon:'magic'}];

// Main entry point
function enterCorruptedGauntlet(){
if(gau&&gau.active){log('Already in the Gauntlet!','#f44');return}
_mkGauHud();
// Build arena
const arena=_buildGauntletArena();
scene.add(arena);
const nodes=_buildGauntletResources(arena);
const {startX,startZ,bcx,bcz,bowlPos}=arena.userData;
// Teleport player in at platform level (platform is at height 2)
player.x=startX;player.z=startZ;player.y=2+2; // platformH + player offset
// Init state
gau={
active:true,arena,nodes,
phase:'gather', // gather | boss | complete
shards:0,ore:0,bark:0,linum:0,fish:0,frames:0,vials:0,cookedFish:0,
weaponTier:0, // 0=none, 1=attuned(t2), 2=perfected(t3)
armourPieces:0,
demiBossesKilled:[],
demiBossEnemies:[],
weakEnemies:[],
hunllef:null,
hunllefMesh:null,
tornados:[],
floorTiles:[],
floorTileTimers:[],
playerAtkStyleIdx:0, // 0=melee, 1=ranged, 2=magic
timeLeft:9*60, // 9 minutes
timerInterval:null,
hintIdx:0,
complete:false};
// Spawn weak monsters around arena
_gauSpawnWeakMonsters();
// Spawn demi-bosses on perimeter
_gauSpawnDemiBosses();
// Start timer
gau.timerInterval=setInterval(()=>{
if(!gau||!gau.active)return;
gau.timeLeft--;
const m=Math.floor(gau.timeLeft/60),s=gau.timeLeft%60;
const timerEl=document.getElementById('gau-timer');
if(timerEl)timerEl.textContent=m+':'+(s<10?'0':'')+s;
if(gau.timeLeft<=0){_gauFail('Time ran out! The Gauntlet resets...')}
else if(gau.timeLeft===120&&dungeonHintsOn)_gauHint('⚠ 2 minutes left! Enter the boss room now!','#f80')
else if(gau.timeLeft===300&&dungeonHintsOn)_gauHint('5 minutes left — finish crafting and head to the boss room.','#ffd700')},1000);
// Show HUD
gauHud.style.display='block';
_gauPhase('⚔ CORRUPTED GAUNTLET — GATHER PHASE');
_gauHint(GAU_HINTS.gather[0],'#c8a96e');
_gauRes();
log('Entered the Corrupted Gauntlet! You have 9 minutes. Gather resources and defeat the Hunllef!','#e040fb');
_gauCycleHints();}

function _gauCycleHints(){
if(!gau||!dungeonHintsOn)return;
let idx=0;const hints=gau.phase==='boss'?GAU_HINTS.boss:GAU_HINTS.gather;
const cycle=()=>{if(!gau||!dungeonHintsOn)return;if(gau.phase==='complete')return;
_gauHint(hints[idx%hints.length]);idx++;setTimeout(cycle,8000)};
setTimeout(cycle,3000);}

function _gauSpawnWeakMonsters(){
if(!gau)return;
const {CELL,COLS,ROWS,offX,offZ}=gau.arena.userData;
// Scale enemy level to player combat level
const playerLv=player.level||1;
for(let i=0;i<8;i++){
const col=2+Math.floor(Math.random()*(COLS-2)),row=Math.floor(Math.random()*ROWS);
// SAFE ZONE: Don't spawn near player start (0,0), bowl (3,3), or edges
if((col<2&&row<2)||(col===3&&row===3)||col<1||col>=COLS-1)continue;
const cx=offX+col*CELL+CELL/2+(Math.random()-.5)*8;
const cz=offZ+row*CELL+CELL/2+(Math.random()-.5)*8;
// Spawn on platform at height 3 (platform is at 2)
const cy=3;
// Scale enemy level: player level ±2 (min 1)
const enemyLv=Math.max(1,playerLv-2+Math.floor(Math.random()*5));
const e=spawnE('bat',cx,cz,enemyLv);
if(e){e.mesh.position.y=cy;e._gauWeak=true;e._gauDrops=true;e.aggro=20;gau.weakEnemies.push(e)}}}

function _gauSpawnDemiBosses(){
if(!gau)return;
const {CELL,COLS,ROWS,offX,offZ}=gau.arena.userData;
// Move demi-bosses away from safe zone at (0,0)
const positions=[[COLS-2,0],[COLS-1,ROWS-2],[COLS-2,ROWS-2]];
// Scale demi-boss levels to player (player level + 5 to +10)
const playerLv=player.level||1;
GAU_DEMIBOSS.forEach((db,i)=>{
const [col,row]=positions[i];
const cx=offX+col*CELL+CELL/2,cz=offZ+row*CELL+CELL/2;
// Spawn on platform at height 3 (platform is at 2)
const cy=3;
// Scale enemy level: player level + 5-10
const enemyLv=Math.max(5,playerLv+5+i*3);
const e=spawnE('golem',cx,cz,enemyLv);
if(e){e.mesh.position.y=cy;e._gauDemi=db;e._gauDemiKilled=false;e.aggro=30;gau.demiBossEnemies.push(e)}});}

// Called from main game loop enemy death handler
function onGauEnemyDeath(e){
if(!gau||!gau.active)return;
if(e._gauWeak){// Drop shards + chance weapon frame
const shards=30+Math.floor(Math.random()*40);gau.shards+=shards;
if(Math.random()<.35||gau.frames===0){gau.frames++;log('Corrupted Weapon Frame received!','#e040fb')}
log('+'+shards+' Corrupted Shards','#cc88ff');_gauRes();}
if(e._gauDemi&&!e._gauDemiKilled){
e._gauDemiKilled=true;const db=e._gauDemi;
gau.demiBossesKilled.push(db.type);
gau.shards+=80;
// Award weapon upgrade
const upgMap={spike:'weaponSpike',bow:'weaponBow',magic:'weaponOrb'};
gau[upgMap[db.reward.type]]=true;
log('DEMI-BOSS SLAIN: '+db.name+' — dropped '+db.reward.item+'!','#e040fb');
if(bossWarnOn)_gauHint('Demi-boss drop: '+db.reward.item+'! Return to Singing Bowl to upgrade.','#cc88ff');
gau.shards+=80;_gauRes();
if(gau.demiBossesKilled.length>=3){_gauHint('All 3 Demi-Bosses slain! Craft Tier-3 weapons & return to start.','#ffd700')}}
_gauCheckCraftReady();}

function _gauCheckCraftReady(){
if(!gau)return;
const readyT2=gau.frames>=1&&gau.shards>=100;
const readyT3=gau.demiBossesKilled.length>=2&&gau.shards>=220;
if(readyT3&&gau.weaponTier<2&&dungeonHintsOn)_gauHint('Return to Singing Bowl — craft Tier-3 weapon (Perfected Corrupted Bow)!','#ffd700');
else if(readyT2&&gau.weaponTier<1&&dungeonHintsOn)_gauHint('Return to Singing Bowl — craft Tier-2 Corrupted Staff!','#c8a96e');}

// Near-singing-bowl interaction (E key check)
function gauCheckInteract(){
if(!gau||!gau.active||gau.phase!=='gather')return;
const bp=gau.arena.userData.bowlPos;
if(Math.hypot(player.x-bp.x,player.z-bp.z)>8)return;
_gauCraft();}

function _gauCraft(){
if(!gau)return;
if(gau.frames<1){log('Need a Weapon Frame to craft!','#f44');return}
if(gau.shards<100){log('Need 100+ Corrupted Shards to craft Tier-2 weapon.','#f44');return}
if(gau.weaponTier===0){
gau.shards-=100;gau.weaponTier=1;gau.vials=2;
log('Crafted: Corrupted Staff (Attuned) Tier-2 + 2 Vials of Water!','#e040fb');
_gauHint('Tier-2 weapon crafted! Now gather fish, ore, bark, linum and kill demi-bosses for Tier-3.','#c8a96e');
_gauRes();return}
if(gau.weaponTier===1&&gau.demiBossesKilled.length>=2&&gau.shards>=120){
gau.shards-=120;gau.weaponTier=2;gau.armourPieces=3;gau.cookedFish=Math.max(gau.fish,6);
log('Crafted: Perfected Corrupted Bow (Tier-3) + Full Armour Set!','#e040fb');
log('Also crafted: 2 Egniol Potions (from shards).','#cc88ff');
_gauHint('READY! Enter the boss chamber (center of arena). Switch prayers every 4 attacks!','#ffd700');
_gauRes();return}
log('Not enough resources yet to upgrade further.','#887');}

// Enter boss room trigger
function _gauEnterBossRoom(){
if(!gau||gau.phase!=='gather')return;
if(gau.weaponTier<1){
_gauHint('⚠ You are NOT ready — craft weapons first at the Singing Bowl!','#f44');
log('Warning: entering boss room without Tier-2+ weapon — this will be very hard!','#f80');}
gau.phase='boss';
_gauPhase('☠ CORRUPTED HUNLLEF — BOSS FIGHT');
_gauSpawnHunllef();
log('You enter the boss chamber... The Corrupted Hunllef awakens!','#e040fb');
if(dungeonHintsOn){_gauHint(GAU_HINTS.boss[0],'#f44');_gauCycleHints();}}

function _gauSpawnHunllef(){
if(!gau)return;
const {bcx,bcz}=gau.arena.userData;
// Build Hunllef mesh — corrupted crystal spider/wolf hybrid
const hg=new THREE.Group();
const bodyMat=new MS({color:0x5a0a8a,emissive:0x3a0070,emissiveIntensity:.6,roughness:.5,metalness:.2});
const crystMat=new MS({color:0xcc44ff,emissive:0xaa22ee,emissiveIntensity:1,transparent:true,opacity:.85});
// Body
const body=new THREE.Mesh(new THREE.SphereGeometry(3.5,12,10),bodyMat);body.scale.set(1.1,.8,1.3);hg.add(body);
// Head
const head=new THREE.Mesh(new THREE.SphereGeometry(2,10,8),bodyMat);head.position.set(0,2.5,3.5);hg.add(head);
// Crystal horns
[-1,1].forEach(s=>{const horn=new THREE.Mesh(new THREE.ConeGeometry(.4,3.5,5),crystMat);horn.position.set(s*1.2,4.5,3.2);horn.rotation.set(.3,0,s*.3);hg.add(horn)});
// 6 legs
for(let i=0;i<6;i++){const a=i/6*Math.PI*2;const leg=new THREE.Mesh(new THREE.CylinderGeometry(.2,.15,4,5),bodyMat);leg.position.set(Math.cos(a)*3.5,0,Math.sin(a)*3.5);leg.rotation.set(Math.cos(a)*.7,0,Math.sin(a)*.7);hg.add(leg)}
// Glowing eyes
[-1,1].forEach(s=>{const eye=new THREE.Mesh(new THREE.SphereGeometry(.35,6,6),new MS({color:0xffaa00,emissive:0xff6600,emissiveIntensity:3}));eye.position.set(s*.8,3.2,5);hg.add(eye)});
// Crystal spine cluster
for(let i=0;i<8;i++){const sp=new THREE.Mesh(new THREE.ConeGeometry(.25,.5+Math.random()*1.5,4),crystMat);sp.position.set((Math.random()-.5)*5,1.5+Math.random()*2,(Math.random()-.5)*4);sp.rotation.set(Math.random()-.5,0,Math.random()-.5);hg.add(sp)}
hg.scale.setScalar(.7);
hg.position.set(bcx,3.5,bcz);hg.castShadow=true; // On platform (platform at 2, boss at 3.5)
scene.add(hg);
gau.hunllefMesh=hg;
// Combat state
gau.hunllef={
hp:600,maxHp:600,
mode:'ranged', // ranged | magic
atkCount:0,playerAtkCount:0,
protPrayer:'melee', // what it protects against
phase:1, // 1,2,3 based on HP
lastAtkTick:0,atkInterval:90,
x:bcx,z:bcz,
tornados:[],tileTimers:[],
dead:false};
// Target it
if(typeof lockOn!=='undefined')lockOn=null; // clear lock-on, player targets manually
_gauSpawnFloorTiles();}

function _gauSpawnFloorTiles(){
if(!gau||!gau.hunllef)return;
const {bcx,bcz,CELL}=gau.arena.userData;
const tileSize=2.2;const gridN=6;
gau.floorTiles=[];
for(let row=0;row<gridN;row++){for(let col=0;col<gridN;col++){
const tx=bcx+(col-gridN/2+.5)*tileSize,tz=bcz+(row-gridN/2+.5)*tileSize;
const tile=new THREE.Mesh(new THREE.BoxGeometry(tileSize-.15,.08,tileSize-.15),new MS({color:0x1a0a2a,transparent:true,opacity:.8}));
tile.position.set(tx,2.06,tz);scene.add(tile); // On platform
gau.floorTiles.push({mesh:tile,tx,tz,state:'safe',timer:0,danger:false})}}
}

// Called from main game update loop tick
function updateGauntlet(dt){
if(!gau||!gau.active)return;
// Check if player actually entered the center boss room (col 3, row 3)
const {bcx,bcz,CELL}=gau.arena.userData;
const roomHalf=CELL/2;
// Must be inside the center room boundaries, not just nearby
if(gau.phase==='gather'&&
Math.abs(player.x-bcx)<roomHalf&&Math.abs(player.z-bcz)<roomHalf){
_gauEnterBossRoom()}
// Singing bowl check
gauCheckInteract();
if(gau.phase==='boss'){_updateHunllef(dt)}_gauAtkTracker();}

function _updateHunllef(dt){
if(!gau||!gau.hunllef||gau.hunllef.dead)return;
const h=gau.hunllef;const hm=gau.hunllefMesh;
if(!hm)return;
// Floating bob on platform (platform at 2, boss base at 3.5)
hm.position.y=3.5+Math.sin(Date.now()*.001)*0.4;
hm.rotation.y+=.008;
// Attack timer
h.lastAtkTick=(h.lastAtkTick||0)+1;
const interval=h.phase>=3?55:h.phase>=2?72:h.atkInterval;
if(h.lastAtkTick>=interval){h.lastAtkTick=0;_hunllefAttack();}
// Tornado movement
gau.tornados.forEach((t,i)=>{
if(!t.mesh)return;
const dx=player.x-t.x,dz=player.z-t.z,dist=Math.hypot(dx,dz);
if(dist>0.5){t.x+=dx/dist*0.55;t.z+=dz/dist*0.55}
t.mesh.position.set(t.x,3.5+Math.sin(Date.now()*.003+i)*0.3,t.z); // On platform
t.mesh.rotation.y+=0.12;
if(dist<3){// Hit player
const dmg=bossWarnOn?12:18;player.hp=Math.max(0,player.hp-dmg);
log('Tornado hits you! -'+dmg+' HP','#f44');
if(bossWarnOn)_gauHint('TORNADO — keep running!','#f44');}});
// Floor tile pulsing
const speed=h.phase>=3?18:h.phase>=2?30:50;
gau.floorTiles.forEach(t=>{
t.timer=(t.timer||0)+1;
if(t.timer>speed+Math.random()*20){t.timer=0;
if(t.state==='safe'){t.state='warn';t.mesh.material.color.set(0x2244aa);t.mesh.material.emissive&&t.mesh.material.emissive.set(0x1133aa)}
else if(t.state==='warn'){t.state='hot';t.mesh.material.color.set(0xff5500)}
else{t.state='safe';t.mesh.material.color.set(0x1a0a2a)}}
// Damage player on hot tile
if(t.state==='hot'){const dx=player.x-t.tx,dz=player.z-t.tz;
if(Math.abs(dx)<1.2&&Math.abs(dz)<1.2){player.hp=Math.max(0,player.hp-8);}}});
// Phase transitions
const hpPct=h.hp/h.maxHp;
const newPhase=hpPct<.33?3:hpPct<.66?2:1;
if(newPhase>h.phase){h.phase=newPhase;
_gauSpawnTornados(newPhase);
if(bossWarnOn)_gauHint('Hunllef Phase '+newPhase+'! More tornadoes, faster attacks!','#f44');
log('Hunllef enters Phase '+newPhase+'!','#e040fb')}
// Trample check — player directly under boss
if(Math.hypot(player.x-h.x,player.z-h.z)<2.5){
player.hp=Math.max(0,player.hp-25);
if(bossWarnOn)_gauHint('MOVE! You are being trampled! (-25 HP)','#f44');}
// Death check
if(player.hp<=0){_gauFail('You were slain by the Corrupted Hunllef...')}
if(h.hp<=0){_gauVictory()}}

function _hunllefAttack(){
if(!gau||!gau.hunllef)return;
const h=gau.hunllef;
// Tornadoes count as one attack in cycle
if(h.atkCount%4===3&&h.phase>=2){// Tornado attack
_gauSpawnTornados(1);h.atkCount++;return}
// Determine attack type
const dmg=h.mode==='ranged'?18:22;const pen=h.phase>=3?.7:h.phase>=2?.85:1;
// Check player prayer
let mitigated=false;
if(h.mode==='ranged'&&typeof player._prayRanged!=='undefined'&&player._prayRanged)mitigated=true;
if(h.mode==='magic'&&typeof player._prayMagic!=='undefined'&&player._prayMagic)mitigated=true;
const finalDmg=mitigated?Math.floor(dmg*.1):Math.floor(dmg*pen);
player.hp=Math.max(0,player.hp-finalDmg);
if(finalDmg>0)log('Hunllef '+(h.mode==='ranged'?'🏹':'🔮')+' hit: -'+finalDmg+' HP'+(mitigated?' (prayer)':''),'#f44');
h.atkCount++;
// Switch attack mode every 4 attacks
if(h.atkCount%4===0){h.mode=h.mode==='ranged'?'magic':'ranged';
if(bossWarnOn)_gauHint('Hunllef switches to '+(h.mode==='ranged'?'RANGED 🏹':'MAGIC 🔮')+'! Switch prayer!','#f80');
log('Hunllef attack style: '+(h.mode==='ranged'?'Ranged':'Magic'),'#cc44ff');}
// Drain prayer occasionally
if(h.mode==='magic'&&Math.random()<.12){skills.Prayer.xp=Math.max(0,skills.Prayer.xp-20);
log('Prayer drained! -20 Prayer pts','#cc44ff');}}

function _gauSpawnTornados(count){
if(!gau)return;
const {bcx,bcz,CELL}=gau.arena.userData;
for(let i=0;i<count;i++){
const a=Math.random()*Math.PI*2,r=5+Math.random()*8;
const tx=bcx+Math.cos(a)*r,tz=bcz+Math.sin(a)*r;
const tmesh=new THREE.Mesh(new THREE.ConeGeometry(.8,3,6),new MS({color:0xaa44ff,emissive:0x8822ee,emissiveIntensity:1.5,transparent:true,opacity:.75,wireframe:true}));
tmesh.position.set(tx,3.5,tz);scene.add(tmesh); // On platform
gau.tornados.push({mesh:tmesh,x:tx,z:tz});}}

// Player attacks the Hunllef (called when player presses attack near boss)
function gauPlayerAttack(){
if(!gau||gau.phase!=='boss'||!gau.hunllef||gau.hunllef.dead)return false;
const h=gau.hunllef;
const dist=Math.hypot(player.x-h.x,player.z-h.z);
// Use playerCombatStyle globally for style — melee needs range 22, ranged/magic up to 80
const styleNames=['melee','ranged','magic'];
const style=styleNames[playerCombatStyle%3];
gau.playerAtkStyleIdx=playerCombatStyle;
const maxRange=style==='melee'?22:80;
if(dist>maxRange)return false;
// Check if blocked by Hunllef protection prayer
if(style===h.protPrayer){log('Hunllef blocks '+style+' with protection prayer! 0 damage.','#f80');
if(dungeonHintsOn)_gauHint('Switch attack style — Hunllef protects from '+style+'!','#f80');}
else{
const gs=totalGear();const base=gau.weaponTier===2?45:gau.weaponTier===1?25:12;
const dmg=Math.floor((base+gs.atk/3)*(0.7+Math.random()*.6));
h.hp=Math.max(0,h.hp-dmg);
log('You hit Hunllef ('+style+'): -'+dmg+' HP — Boss: '+h.hp+'/'+h.maxHp,'#0f0');
// Update boss health bar effect
if(gau.hunllefMesh)gau.hunllefMesh.children[0]&&(gau.hunllefMesh.children[0].scale.y=Math.max(0.05,h.hp/h.maxHp));}
h.playerAtkCount++;
// Every 6 player attacks, Hunllef switches protection prayer
if(h.playerAtkCount%6===0){
const newProt=styleNames[Math.floor(Math.random()*3)];h.protPrayer=newProt;
log('Hunllef switches protection to: '+newProt,'#cc44ff');
if(bossWarnOn)_gauHint('Hunllef now protects from '+newProt+'! Switch your attack style.','#f80');}
_gauAtkTracker();
if(h.hp<=0){_gauVictory()}
return true;}

function _gauVictory(){
if(!gau||gau.complete)return;
gau.complete=true;gau.phase='complete';
clearInterval(gau.timerInterval);
_gauPhase('🏆 VICTORY! HUNLLEF DEFEATED!');
_gauHint(GAU_HINTS.complete[0],'#ffd700');
// Remove boss + effects
if(gau.hunllefMesh){scene.remove(gau.hunllefMesh);gau.hunllefMesh=null}
gau.tornados.forEach(t=>{if(t.mesh)scene.remove(t.mesh)});gau.tornados=[];
gau.floorTiles.forEach(t=>{if(t.mesh)scene.remove(t.mesh)});gau.floorTiles=[];
// Reward chest
const {bcx,bcz}=gau.arena.userData;
const chest=new THREE.Mesh(new THREE.BoxGeometry(3,2.5,3),new MS({color:0xcc88ff,emissive:0x8844aa,emissiveIntensity:.8}));
chest.position.set(bcx,1.25,bcz);scene.add(chest);
log('╔══════════════════════════════════╗','#ffd700');
log('║  CORRUPTED GAUNTLET COMPLETE!    ║','#ffd700');
log('╚══════════════════════════════════╝','#ffd700');
// Determine loot
const lootTable=[
{item:'Ystalcray Armorway Eedsay',chance:.04,label:'Crystal Armour Seed'},
{item:'Ystalcray Eaponway Eedsay',chance:.04,label:'Crystal Weapon Seed'},
{item:'Enhancedway Ystalcray Eedsay',chance:.005,label:'ENHANCED Crystal Seed ★'},
{item:'Etaidpay Ystalcray Elmhay',chance:.12,label:'Corrupted Crystal Helm'},
{item:'Etaidpay Ystalcray Odybay',chance:.12,label:'Corrupted Crystal Body'},
{item:'Etaidpay Ystalcray Egslay',chance:.12,label:'Corrupted Crystal Legs'},
{item:'Oinscay x500',chance:.6,label:'500 Gold Coins'}];
lootTable.forEach(l=>{if(Math.random()<l.chance){
log('LOOT: '+l.label,'#e040fb');
inventory.push({name:l.item,uid:null});updateInvUI();}});
// Skill XP rewards
skills.Slayer.xp+=2000;skills.Attack.xp+=1500;skills.Strength.xp+=1500;skills.Defence.xp+=1500;updateSkillUI();updateXpBar();
log('Slayer +2000 XP, Combat +1500 XP each','#cc88ff');
setTimeout(()=>{_gauExit()},8000);}

function _gauFail(msg){
if(!gau)return;clearInterval(gau.timerInterval);
gau.phase='complete';gau.complete=true;
_gauPhase('💀 DEFEATED');
_gauHint(msg,'#f44');
log(msg,'#f44');
setTimeout(()=>{_gauExit()},4000);}

function _gauExit(){
if(!gau)return;
clearInterval(gau.timerInterval);
// Cleanup 3D
if(gau.arena)scene.remove(gau.arena);
gau.tornados.forEach(t=>{if(t.mesh)scene.remove(t.mesh)});
gau.floorTiles.forEach(t=>{if(t.mesh)scene.remove(t.mesh)});
if(gau.hunllefMesh)scene.remove(gau.hunllefMesh);
// Return player to world
player.x=GAU_X;player.z=GAU_Z+60;player.y=meshTerrainH(GAU_X,GAU_Z+60)+2;
gau={active:false};gauHud.style.display='none';
log('You leave the Corrupted Gauntlet.','#cc88ff');}

// Hook into main game update loop — called each frame
const _origGameLoop=typeof loop==='function'?loop:null;
// Patch attack key (1) to check gauntlet boss targeting
const _gauKeyHandler=function(e){
if(!gau||!gau.active||gau.phase!=='boss')return;
const k=e.key?e.key.toLowerCase():e.code;
if(k==='1'||k==='digit1'){gauPlayerAttack()}};
document.addEventListener('keydown',_gauKeyHandler,true);

// Expose updateGauntlet to main loop (called at top of frame)
// The main loop already calls named per-tick functions; hook via requestAnimationFrame proxy
const _gauLoopHook=(function(){
const orig=window.requestAnimationFrame;
let lastT=0;
window.requestAnimationFrame=function(cb){
return orig.call(window,function(t){
const dt=(t-lastT)/16;lastT=t;
try{updateGauntlet(dt)}catch(ex){}
cb(t);})};})();
// Dungeon key — open dungeoning menu (shows gauntlet entry prompt)
// Uses configurable key from kbMap (default: 'u')
function openDungeonMenu(){
if(typeof gameStarted==='undefined'||!gameStarted)return;
const existing=document.getElementById('dungeon-menu');
if(existing){existing.remove();return}
const dm=document.createElement('div');
dm.id='dungeon-menu';
dm.style.cssText='position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(10,5,20,.96);border:2px solid #8822cc;border-radius:8px;padding:16px 20px;z-index:8001;min-width:320px;font-family:"Times New Roman",serif;color:#cc88ff;box-shadow:0 0 30px #8822cc88';
// Get the current dungeon key from keybinds
const dungeonKey=(typeof kbMap!=='undefined'&&kbMap.dungeon)?kbMap.dungeon.key.toUpperCase():'U';
dm.innerHTML='<div style="font-size:18px;color:#e040fb;font-weight:700;text-align:center;letter-spacing:2px;margin-bottom:10px">⚔ DUNGEONING</div>'+
'<div style="font-size:11px;color:#aa88cc;margin-bottom:10px;text-align:center">Solo Challenges — Prepare, Gather, Conquer</div>'+
'<div style="border:1px solid #5a2a8a;border-radius:5px;padding:10px;margin-bottom:8px;cursor:pointer;background:rgba(90,20,140,.2);transition:background .15s" '+
'onmouseenter="this.style.background=\'rgba(120,40,180,.35)\'" onmouseleave="this.style.background=\'rgba(90,20,140,.2)\'" '+
'onclick="teleportToDungeonEntrance()">'+
'<div style="color:#e040fb;font-weight:700;font-size:14px">🏰 Teleport to Dungeon Entrance</div>'+
'<div style="color:#9a6aaa;font-size:10px;margin-top:3px">Instant travel to the nearest dungeon entrance.</div>'+
'</div>'+
'<div style="border:1px solid #5a2a8a;border-radius:5px;padding:10px;margin-bottom:8px;cursor:pointer;background:rgba(90,20,140,.2);transition:background .15s" '+
'onmouseenter="this.style.background=\'rgba(120,40,180,.35)\'" onmouseleave="this.style.background=\'rgba(90,20,140,.2)\'" '+
'onclick="document.getElementById(\'dungeon-menu\').remove();enterCorruptedGauntlet()">'+
'<div style="color:#e040fb;font-weight:700;font-size:14px">☠ Enter Corrupted Gauntlet</div>'+
'<div style="color:#9a6aaa;font-size:10px;margin-top:3px">Solo 9-minute minigame — Gather resources, craft weapons, defeat the Corrupted Hunllef.</div>'+
'<div style="color:#887;font-size:9px;margin-top:2px">Recommended: Combat 80+ • Rewards: Crystal Seeds, Armour</div>'+
'</div>'+
'<div style="text-align:center;margin-top:6px"><span style="cursor:pointer;color:#887;font-size:10px;border:1px solid #442244;padding:3px 10px;border-radius:3px" onclick="document.getElementById(\'dungeon-menu\').remove()">Close ('+dungeonKey+')</span></div>';
document.body.appendChild(dm);}
document.addEventListener('keydown',function(e){
const dungeonKey=(typeof kbMap!=='undefined'&&kbMap.dungeon)?kbMap.dungeon.key:'u';
if(e.key&&e.key.toLowerCase()===dungeonKey&&typeof gameStarted!=='undefined'&&gameStarted){
e.preventDefault();
openDungeonMenu();}});
// Teleport to nearest dungeon entrance
function teleportToDungeonEntrance(){
// Close menu first
const dm=document.getElementById('dungeon-menu');
if(dm)dm.remove();
// Find nearest dungeon
let nearest=null;let minDist=Infinity;
if(typeof dungeons!=='undefined'){
for(const d of dungeons){
const dist=Math.hypot(player.x-d.x,player.z-d.z);
if(dist<minDist){minDist=dist;nearest=d;}}}
if(nearest){
player.x=nearest.x;player.z=nearest.z+15;player.y=2;
log('Teleported to dungeon entrance at ('+~~nearest.x+', '+~~nearest.z+')','#e040fb');
if(typeof cam!=='undefined'){cam.x=player.x;cam.z=player.z+30;}}
else{// No dungeon found - teleport to a default location
player.x=500;player.z=500;player.y=2;
log('No dungeon found. Teleported to wilderness hub.','#f80');}
if(typeof saveGame==='function')saveGame();}
// Expose dungeon functions to global scope for HTML onclick handlers
window.teleportToDungeonEntrance=teleportToDungeonEntrance;
window.openDungeonMenu=openDungeonMenu;

// Expose editor functions
window.editorSetCamera=editorSetCamera;
window.editorFocusSelected=editorFocusSelected;
window.editorSpawnAtSelected=editorSpawnAtSelected;

// === EDITOR MODE FUNCTIONS ===
let editorCameraMode='normal';
let editorDragStart=null;
let editorDragObj=null;
let editorOriginalPos=null;

function toggleEditorMode(){
editorMode=!editorMode;
const ed=document.getElementById('editor-mode');
const cursor=document.getElementById('editor-cursor');
if(editorMode){
ed.style.display='block';
cursor.style.display='block';
editorRefreshList();
editorPopulateSpawnList();
editorSetCamera('normal');
log('EDITOR MODE ENABLED — Insert key to exit','#ffd700');
}else{
ed.style.display='none';
cursor.style.display='none';
editorSelected=null;
editorUpdateSelection();
editorSetCamera('normal');
log('Editor mode disabled','#887');
}
}

function editorSetCamera(mode){
editorCameraMode=mode;
const groundY=meshTerrainH(player.x,player.z);
// Update button styles
['normal','bird','top'].forEach(m=>{
const btn=document.getElementById('btn-cam-'+m);
if(btn){
if(m===mode){
btn.style.background='#554422';
btn.style.color='#ffd700';
btn.style.border='2px solid #aa8833';
}else{
btn.style.background='#332211';
btn.style.color='#aa8833';
btn.style.border='1px solid #554422';
}
}
});
// Apply camera mode
if(mode==='normal'){
cam.position.set(player.x,groundY+40,player.z+60);
cam.lookAt(player.x,groundY+5,player.z);
}else if(mode==='bird'){
cam.position.set(player.x,groundY+120,player.z+80);
cam.lookAt(player.x,groundY+5,player.z);
}else if(mode==='top'){
cam.position.set(player.x,groundY+200,player.z);
cam.lookAt(player.x,groundY,player.z);
}
}

function editorFocusSelected(){
if(!editorSelected)return;
const s=editorSelected;
let targetX,targetZ;
// Handle buildings with meshes
if(s.type==='building'&&s.obj.mesh){
targetX=s.obj.mesh.position.x;
targetZ=s.obj.mesh.position.z;
}else if(s.obj.mesh){targetX=s.obj.mesh.position.x;targetZ=s.obj.mesh.position.z;}
else if(s.obj.x!==undefined){targetX=s.obj.x;targetZ=s.obj.z;}
else return;
const groundY=meshTerrainH(targetX,targetZ);
if(editorCameraMode==='normal'){
cam.position.set(targetX,groundY+40,targetZ+60);
}else if(editorCameraMode==='bird'){
cam.position.set(targetX,groundY+120,targetZ+80);
}else if(editorCameraMode==='top'){
cam.position.set(targetX,groundY+200,targetZ);
}
cam.lookAt(targetX,groundY+5,targetZ);
player.x=targetX;
player.z=targetZ;
player.y=groundY+2;
log('Camera focused on '+s.type,'#0f0');
}

function editorSpawnAtSelected(){
if(!editorSelected)return;
const s=editorSelected;
let x,z;
if(s.obj.mesh){x=s.obj.mesh.position.x;z=s.obj.mesh.position.z;}
else if(s.obj.x!==undefined){x=s.obj.x;z=s.obj.z;}
else return;
const sel=document.getElementById('editor-spawn-select');
const type=sel.value;
if(!type)return;
if(editorObjType==='enemy'){
const lv=Math.max(1,Math.round(x/100+z/100+10));
spawnE(type,x+(Math.random()-0.5)*10,z+(Math.random()-0.5)*10,lv);
log('Spawned '+type+' near selection','#0f0');
}else if(editorObjType==='loot'){
const item={name:type,uid:'ed_'+Date.now()};
const mesh=spawnLootItem(item,x+(Math.random()-0.5)*8,z+(Math.random()-0.5)*8);
if(mesh){
mesh.userData.editorSpawn=true;
lootArr.push({x:mesh.position.x,z:mesh.position.z,item:item,mesh:mesh});
}
log('Spawned loot: '+type,'#0f0');
}else if(editorObjType==='building'){
const h=meshTerrainH(x,z);
if(type==='hut'){hut(x,z,Math.random()*Math.PI*2,1);}
else if(type==='tower'){tower(x,z,1);}
else if(type==='house'){const g=new THREE.Group();const hm=new THREE.Mesh(new THREE.BoxGeometry(12,8,10),mt.wd);hm.position.y=4;g.add(hm);g.position.set(x,h,z);scene.add(g);g.userData={isBuilding:true};}
else if(type==='tavern'){makeEnterable(x,z,'tavern','Tavern');}
else if(type==='forge'){makeEnterable(x,z,'forge','Forge');}
else if(type==='church'){makeEnterable(x,z,'chapel','Church');}
else if(type==='mill'){makeEnterable(x,z,'windmill','Mill');}
else if(type==='barn'){makeEnterable(x,z,'barn','Barn');}
log('Spawned '+type+' near selection','#0f0');
}
editorRefreshList();
}

function setEditorType(type){
editorObjType=type;
document.querySelectorAll('.editor-type-btn').forEach(btn=>{
btn.style.background='#332211';
btn.style.color='#aa8833';
btn.style.borderColor='#554422';
});
const activeBtn=document.getElementById('btn-'+type);
if(activeBtn){
activeBtn.style.background='#554422';
activeBtn.style.color='#ffd700';
activeBtn.style.borderColor='#aa8833';
}
editorPopulateSpawnList();
}

function editorPopulateSpawnList(){
const sel=document.getElementById('editor-spawn-select');
sel.innerHTML='';
let items=[];
if(editorObjType==='enemy')items=editorSpawnList;
else if(editorObjType==='building')items=editorBuildings;
else if(editorObjType==='loot')items=editorLoot;
items.forEach(item=>{
const opt=document.createElement('option');
opt.value=item;opt.textContent=item;
sel.appendChild(opt);
});
}

function editorSpawn(){
const sel=document.getElementById('editor-spawn-select');
const type=sel.value;
if(!type)return;
const x=player.x+(Math.random()-0.5)*20;
const z=player.z+(Math.random()-0.5)*20;
if(editorObjType==='enemy'){
const lv=Math.max(1,Math.round(player.x/100+player.z/100+10));
spawnE(type,x,z,lv);
log('Spawned '+type+' at '+Math.round(x)+','+Math.round(z),'#0f0');
}else if(editorObjType==='loot'){
const item={name:type,uid:'ed_'+Date.now()};
const mesh=spawnLootItem(item,x,z);
if(mesh){
mesh.userData.editorSpawn=true;
lootArr.push({x:x,z:z,item:item,mesh:mesh});
}
log('Spawned loot: '+type,'#0f0');
}else if(editorObjType==='building'){
// Spawn building at player position
const h=meshTerrainH(x,z);
if(type==='hut'){hut(x,z,Math.random()*Math.PI*2,1);}
else if(type==='tower'){tower(x,z,1);}
else if(type==='house'){const g=new THREE.Group();const hm=new THREE.Mesh(new THREE.BoxGeometry(12,8,10),mt.wd);hm.position.y=4;g.add(hm);g.position.set(x,h,z);scene.add(g);g.userData={isBuilding:true};}
else if(type==='tavern'){makeEnterable(x,z,'tavern','Tavern');}
else if(type==='forge'){makeEnterable(x,z,'forge','Forge');}
else if(type==='church'){makeEnterable(x,z,'chapel','Church');}
else if(type==='mill'){makeEnterable(x,z,'windmill','Mill');}
else if(type==='barn'){makeEnterable(x,z,'barn','Barn');}
log('Spawned '+type+' at '+Math.round(x)+','+Math.round(z),'#0f0');
}
editorRefreshList();
}

function spawnLootItem(item,x,z){
const mesh=new THREE.Group();
const box=new THREE.Mesh(new THREE.BoxGeometry(0.8,0.8,0.8),new THREE.MeshStandardMaterial({color:0xffd700,roughness:0.3,metalness:0.8}));
box.position.y=0.4;mesh.add(box);
mesh.position.set(x,meshTerrainH(x,z)+0.5,z);
mesh.userData={isLoot:true,item:item,editorSpawn:true};
scene.add(mesh);return mesh;
}

function editorRefreshList(){
const list=document.getElementById('editor-object-list');
const count=document.getElementById('editor-count');
list.innerHTML='';
let total=0;
// Enemies
enemies.forEach((e,idx)=>{
total++;
const div=document.createElement('div');
div.style.cssText='padding:4px;margin:2px 0;background:rgba(60,40,20,0.6);cursor:pointer;border-radius:3px;display:flex;justify-content:space-between;align-items:center;';
div.innerHTML='<span>👹 '+e.type+' Lv'+e.lv+'</span><span style="color:#887;font-size:9px;">'+Math.round(e.mesh.position.x)+','+Math.round(e.mesh.position.z)+'</span>';
div.onclick=()=>editorSelectObject(e,'enemy',idx);
if(editorSelected&&editorSelected.type==='enemy'&&editorSelected.idx===idx){
div.style.background='rgba(170,136,51,0.4)';
div.style.border='1px solid #aa8833';
}
list.appendChild(div);
});
// Buildings/Enterable
// Castles and towers from scene
scene.children.forEach(c=>{
if(c.userData&&(c.userData.isCastle||c.userData.isTower||c.userData.isBuilding)){
total++;
const div=document.createElement('div');
div.style.cssText='padding:4px;margin:2px 0;background:rgba(60,50,40,0.6);cursor:pointer;border-radius:3px;display:flex;justify-content:space-between;align-items:center;';
div.innerHTML='<span>🏰 Structure at '+Math.round(c.position.x)+','+Math.round(c.position.z)+'</span><span style="color:#887;font-size:9px;">Building</span>';
div.onclick=()=>{
// Create a pseudo-building object for selection
const b={name:'Castle/Tower Structure',x:c.position.x,z:c.position.z,r:50,mesh:c,type:'structure'};
editorSelectObject(b,'building',-1);
};
list.appendChild(div);
}
});
// Enterable buildings
enterableBuildings.forEach((b,idx)=>{
total++;
const div=document.createElement('div');
div.style.cssText='padding:4px;margin:2px 0;background:rgba(40,50,60,0.6);cursor:pointer;border-radius:3px;display:flex;justify-content:space-between;align-items:center;';
const icon=b.type==='castle'?'🏰':b.type==='tower'?'🗼':b.type==='tavern'?'🍺':b.type==='shop'?'🏪':b.type==='chapel'?'⛪':'🏠';
div.innerHTML='<span>'+icon+' '+b.name+' ('+b.type+')</span><span style="color:#887;font-size:9px;">'+Math.round(b.x)+','+Math.round(b.z)+'</span>';
div.onclick=()=>editorSelectObject(b,'building',idx);
list.appendChild(div);
});
// Loot
lootArr.forEach((l,idx)=>{
if(!l.mesh) return;
total++;
const div=document.createElement('div');
div.style.cssText='padding:4px;margin:2px 0;background:rgba(80,70,20,0.6);cursor:pointer;border-radius:3px;display:flex;justify-content:space-between;align-items:center;';
div.innerHTML='<span>💰 '+l.item.name+'</span><span style="color:#887;font-size:9px;">'+Math.round(l.mesh.position.x)+','+Math.round(l.mesh.position.z)+'</span>';
div.onclick=()=>editorSelectObject(l,'loot',idx);
list.appendChild(div);
});
if(total===0)list.innerHTML='<span style="color:#665;">No objects in world</span>';
count.textContent=total;
}

function editorSelectObject(obj,type,idx){
editorSelected={obj:obj,type:type,idx:idx};
editorUpdateSelection();
editorFocusSelected();
}

function editorUpdateSelection(){
const info=document.getElementById('editor-selected-info');
const controls=document.getElementById('editor-controls');
if(!editorSelected){
info.innerHTML='<span style="color:#887;">Click an object to select</span>';
controls.style.display='none';
return;
}
const s=editorSelected;
let html='<div style="color:#ffd700;font-weight:bold;">';
if(s.type==='enemy')html+='👹 Enemy: '+s.obj.type+' Lv'+s.obj.lv;
else if(s.type==='building')html+='🏠 Building: '+s.obj.name;
else if(s.type==='loot')html+='💰 Loot: '+s.obj.item.name;
html+='</div>';
if(s.obj.mesh||s.obj.x!==undefined){
const x=s.obj.mesh?s.obj.mesh.position.x:s.obj.x;
const y=s.obj.mesh?s.obj.mesh.position.y:(s.obj.y||0);
const z=s.obj.mesh?s.obj.mesh.position.z:s.obj.z;
html+='<div style="color:#aa8833;margin-top:4px;">Pos: '+Math.round(x)+', '+Math.round(y)+', '+Math.round(z)+'</div>';
}
info.innerHTML=html;
controls.style.display='block';
}

function editorMove(dir){
if(!editorSelected)return;
const s=editorSelected;
const step=editorSnap?10:2;
let dx=0,dy=0,dz=0;
if(dir==='left')dx=-step;
if(dir==='right')dx=step;
if(dir==='forward')dz=-step;
if(dir==='back')dz=step;
if(dir==='up')dy=step;
if(dir==='down')dy=-step;
if(s.type==='enemy'&&s.obj.mesh){
s.obj.mesh.position.x+=dx;
s.obj.mesh.position.y+=dy;
s.obj.mesh.position.z+=dz;
s.obj.x=s.obj.mesh.position.x;
s.obj.y=s.obj.mesh.position.y;
s.obj.z=s.obj.mesh.position.z;
if(s.obj.mesh.userData.hpBar)s.obj.mesh.userData.hpBar.position.x=s.obj.mesh.position.x;
if(s.obj.mesh.userData.hpBar)s.obj.mesh.userData.hpBar.position.y=s.obj.mesh.position.y+10;
if(s.obj.mesh.userData.hpBar)s.obj.mesh.userData.hpBar.position.z=s.obj.mesh.position.z;
if(s.obj.mesh.userData.nameLabel)s.obj.mesh.userData.nameLabel.position.x=s.obj.mesh.position.x;
if(s.obj.mesh.userData.nameLabel)s.obj.mesh.userData.nameLabel.position.y=s.obj.mesh.position.y+12;
if(s.obj.mesh.userData.nameLabel)s.obj.mesh.userData.nameLabel.position.z=s.obj.mesh.position.z;
}else if(s.type==='building'){
// Move building data position
s.obj.x+=dx;
s.obj.y=(s.obj.y||0)+dy;
s.obj.z+=dz;
// If building has a mesh, move the entire mesh group
if(s.obj.mesh){
s.obj.mesh.position.x+=dx;
s.obj.mesh.position.y+=dy;
s.obj.mesh.position.z+=dz;
}
// Update collision for this building's circle collider
const collider=circleColliders.find(c=>Math.hypot(c.x-(s.obj.x-dx),c.z-(s.obj.z-dz))<1);
if(collider){collider.x=s.obj.x;collider.y=s.obj.y;collider.z=s.obj.z;}
}else if(s.type==='loot'&&s.obj.mesh){
s.obj.mesh.position.x+=dx;
s.obj.mesh.position.y+=dy;
s.obj.mesh.position.z+=dz;
s.obj.x=s.obj.mesh.position.x;
s.obj.y=s.obj.mesh.position.y;
s.obj.z=s.obj.mesh.position.z;
}
editorUpdateSelection();
editorRefreshList();
log('Moved '+s.type+' '+dir,'#0f0');
}

function editorDelete(){
if(!editorSelected)return;
const s=editorSelected;
if(s.type==='enemy'){
if(s.obj.mesh){scene.remove(s.obj.mesh);}
enemies.splice(s.idx,1);
}else if(s.type==='loot'&&s.obj.mesh){
scene.remove(s.obj.mesh);
lootArr.splice(s.idx,1);
}else if(s.type==='building'){
// Remove building mesh from scene if it exists
if(s.obj.mesh){scene.remove(s.obj.mesh);}
// Remove from enterableBuildings array if it has an index
if(s.idx>=0&&s.idx<enterableBuildings.length){
enterableBuildings.splice(s.idx,1);
}
// Remove circle collider for this building
const colliderIdx=circleColliders.findIndex(c=>Math.hypot(c.x-s.obj.x,c.z-s.obj.z)<1);
if(colliderIdx>=0){circleColliders.splice(colliderIdx,1);}
}
editorSelected=null;
editorUpdateSelection();
editorRefreshList();
log('Deleted '+s.type,'#f44');
}

function editorSnapToggle(){
editorSnap=!editorSnap;
const btn=document.getElementById('btn-snap');
btn.textContent='📐 Snap: '+(editorSnap?'ON':'OFF');
btn.style.color=editorSnap?'#ffd700':'#887';
}

function editorSaveWorld(){
const worldData={
enemies:enemies.map(e=>({type:e.type,x:e.x,z:e.z,y:e.y||0,lv:e.lv,hp:e.hp,maxHp:e.maxHp})),
loot:lootArr.filter(l=>l.mesh&&l.mesh.userData.editorSpawn).map(l=>({name:l.item.name,x:l.mesh.position.x,y:l.mesh.position.y,z:l.mesh.position.z})),
buildings:enterableBuildings.map(b=>({name:b.name,x:b.x,y:b.y||0,z:b.z,r:b.r,type:b.type})),
player:{x:player.x,y:player.y,z:player.z,hp:player.hp},
timestamp:Date.now()
};
localStorage.setItem('editor_world_save',JSON.stringify(worldData));
log('World saved to localStorage!','#0f0');
}

function editorLoadWorld(){
const raw=localStorage.getItem('editor_world_save');
if(!raw){log('No saved world found!','#f44');return;}
try{
const data=JSON.parse(raw);
// Clear existing editor-spawned enemies
enemies=enemies.filter(e=>!e.mesh||!e.mesh.userData.editorSpawn);
lootArr=lootArr.filter(l=>!l.mesh||!l.mesh.userData.editorSpawn);
// Load enemies
if(data.enemies){
data.enemies.forEach(e=>{
const mesh=buildEnemy(e.type,e.lv);
mesh.position.set(e.x,e.y||meshTerrainH(e.x,e.z),e.z);
const en={type:e.type,x:e.x,z:e.z,y:e.y||0,lv:e.lv,hp:e.hp||10,maxHp:e.maxHp||10,mesh:mesh,aggro:e.lv*8,atkCD:0,windUp:0,swingT:0};
en.mesh.userData.editorSpawn=true;
enemies.push(en);
});
}
// Load loot
if(data.loot){
data.loot.forEach(l=>{
const item={name:l.name,uid:'load_'+Date.now()};
const mesh=spawnLootItem(item,l.x,l.z);
if(mesh){mesh.userData.editorSpawn=true;lootArr.push({x:l.x,z:l.z,item:item,mesh:mesh});}
});
}
// Load buildings
if(data.buildings){
data.buildings.forEach(b=>{
const h=b.y||meshTerrainH(b.x,b.z);
// Check if building already exists
const exists=enterableBuildings.some(eb=>Math.hypot(eb.x-b.x,eb.z-b.z)<5);
if(!exists){
makeEnterable(b.x,b.z,b.type||'house',b.name||'Building');
}
});
}
log('World loaded!','#0f0');
editorRefreshList();
}catch(e){log('Load failed: '+e.message,'#f44');}
}

function editorExport(){
const worldData={
enemies:enemies.map(e=>({type:e.type,x:e.x,y:e.y||0,z:e.z,lv:e.lv})),
loot:lootArr.filter(l=>l.mesh&&l.mesh.userData.editorSpawn).map(l=>({name:l.item.name,x:l.mesh.position.x,y:l.mesh.position.y,z:l.mesh.position.z})),
buildings:enterableBuildings.map(b=>({name:b.name,x:b.x,y:b.y||0,z:b.z,r:b.r,type:b.type}))
};
const json=JSON.stringify(worldData,null,2);
const blob=new Blob([json],{type:'application/json'});
const url=URL.createObjectURL(blob);
const a=document.createElement('a');
a.href=url;
a.download='soulscape_world_'+Date.now()+'.json';
a.click();
URL.revokeObjectURL(url);
log('World exported to JSON file!','#0f0');
}

// Click to select and drag in editor mode
document.addEventListener('mousedown',e=>{
if(!editorMode||e.target.closest('#editor-panel'))return;
// Start drag if shift is held and we have a selection
if(e.shiftKey&&editorSelected){
const s=editorSelected;
if(s.obj.mesh||(s.type==='building'&&s.obj.x!==undefined)){
editorDragStart={x:e.clientX,y:e.clientY};
editorDragObj=s;
if(s.obj.mesh){
editorOriginalPos={x:s.obj.mesh.position.x,z:s.obj.mesh.position.z};
}else{
editorOriginalPos={x:s.obj.x,z:s.obj.z};
}
log('Drag mode: Move mouse to reposition','#ffd700');
return;
}
}
// Otherwise select object
const raycaster=new THREE.Raycaster();
const mouseV=new THREE.Vector2((e.clientX/window.innerWidth)*2-1,-(e.clientY/window.innerHeight)*2+1);
raycaster.setFromCamera(mouseV,cam);
// Check enemies
const enemyMeshes=enemies.map((e,i)=>({mesh:e.mesh,idx:i,type:'enemy',obj:e}));
for(const em of enemyMeshes){
const intersects=raycaster.intersectObject(em.mesh,true);
if(intersects.length>0){editorSelectObject(em.obj,'enemy',em.idx);return;}
}
// Check loot
for(let i=0;i<lootArr.length;i++){
if(!lootArr[i].mesh)continue;
const intersects=raycaster.intersectObject(lootArr[i].mesh,true);
if(intersects.length>0){editorSelectObject(lootArr[i],'loot',i);return;}
}
// Check buildings in scene (castles, towers, etc.)
// First try to find actual building meshes
let foundBuilding=null,foundDist=Infinity;
scene.children.forEach(c=>{
if(c.userData&&c.userData.isBuilding){foundBuilding=c;}
// Check if it's a castle/tower mesh group
if(c.type==='Group'||c.isMesh){
const dx=c.position.x-player.x,dz=c.position.z-player.z;
if(dx*dx+dz*dz<40000){ // Within 200 units
const intersects=raycaster.intersectObject(c,true);
if(intersects.length>0&&intersects[0].distance<foundDist){
foundDist=intersects[0].distance;
foundBuilding=c;
}
}
}
});
// Check enterable buildings by proximity to click point on ground
const rayToGround=new THREE.Raycaster();
rayToGround.setFromCamera(mouseV,cam);
const groundPlane=new THREE.Plane(new THREE.Vector3(0,1,0),0);
const target=new THREE.Vector3();
rayToGround.ray.intersectPlane(groundPlane,target);
if(target){
for(let i=0;i<enterableBuildings.length;i++){
const b=enterableBuildings[i];
const dist=Math.hypot(target.x-b.x,target.z-b.z);
if(dist<b.r||dist<30){
editorSelectObject(b,'building',i);
return;
}
}
}
if(foundBuilding){
// Find closest enterable building to this mesh
let closestIdx=-1,closestDist=Infinity;
for(let i=0;i<enterableBuildings.length;i++){
const b=enterableBuildings[i];
const dist=Math.hypot(foundBuilding.position.x-b.x,foundBuilding.position.z-b.z);
if(dist<closestDist){closestDist=dist;closestIdx=i;}
}
if(closestIdx>=0&&closestDist<50){
editorSelectObject(enterableBuildings[closestIdx],'building',closestIdx);
return;
}
}
});

// Handle drag movement
document.addEventListener('mousemove',e=>{
if(!editorMode||!editorDragStart||!editorDragObj)return;
const dx=(e.clientX-editorDragStart.x)*0.5;
const dz=(e.clientY-editorDragStart.y)*0.5;
const s=editorDragObj;
const step=editorSnap?10:2;
// Calculate snapped or free movement
const moveX=editorSnap?Math.round((editorOriginalPos.x+dx)/step)*step:editorOriginalPos.x+dx;
const moveZ=editorSnap?Math.round((editorOriginalPos.z+dz)/step)*step:editorOriginalPos.z+dz;
if(s.type==='enemy'&&s.obj.mesh){
s.obj.mesh.position.x=moveX;
s.obj.mesh.position.z=moveZ;
s.obj.x=moveX;
s.obj.z=moveZ;
if(s.obj.mesh.userData.hpBar){
s.obj.mesh.userData.hpBar.position.x=moveX;
s.obj.mesh.userData.hpBar.position.z=moveZ;
}
if(s.obj.mesh.userData.nameLabel){
s.obj.mesh.userData.nameLabel.position.x=moveX;
s.obj.mesh.userData.nameLabel.position.z=moveZ;
}
}else if(s.type==='building'){
s.obj.x=moveX;
s.obj.z=moveZ;
// If building has a mesh, move the entire mesh group
if(s.obj.mesh){
s.obj.mesh.position.x=moveX;
s.obj.mesh.position.z=moveZ;
// Move all children
s.obj.mesh.traverse(child=>{
if(child.isMesh||child.isLight){
child.position.x=moveX;
child.position.z=moveZ;
}
});
}
}else if(s.type==='loot'&&s.obj.mesh){
s.obj.mesh.position.x=moveX;
s.obj.mesh.position.z=moveZ;
s.obj.x=moveX;
s.obj.z=moveZ;
}
editorUpdateSelection();
});

// End drag
document.addEventListener('mouseup',e=>{
if(!editorMode||!editorDragStart)return;
editorDragStart=null;
editorDragObj=null;
editorOriginalPos=null;
editorRefreshList();
log('Object repositioned','#0f0');
});

// Update controls hint
document.getElementById('controls').innerHTML+=' &#183; <b style="color:#ffd700">Insert</b> Editor';

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
class ThreadedHTTPServer(http.server.HTTPServer):
    allow_reuse_address = True
    def process_request(self, request, client_address):
        threading.Thread(target=self.finish_request, args=(request, client_address), daemon=True).start()
httpd = ThreadedHTTPServer(('0.0.0.0', PORT), GameHandler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
webbrowser.open(f'http://127.0.0.1:{PORT}/')
try:
    while True: threading.Event().wait(1)
except KeyboardInterrupt:
    print('\nServer stopped. Thanks for playing!')
