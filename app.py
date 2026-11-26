#!/usr/bin/env python3
# ==========================================================
#  ALFILIATOR // ATELIER NODE v5 — 31 ruang, tema, roadmap
#  python app.py   |   PORT=8888
# ==========================================================
import os, re, time, html, json, secrets, threading, http.server, socketserver
from collections import defaultdict, deque

PORT = int(os.environ.get("PORT", "8888"))
HOST = os.environ.get("HOST", "0.0.0.0")
WA   = "https://wa.me/6281292442362"
BASE = (os.environ.get("BASE") or "http://localhost:%d" % PORT).rstrip("/")
RATE_LIMIT, RATE_WINDOW = 90, 60     # jendela panjang
BURST_LIMIT, BURST_WINDOW = 18, 10   # jendela pendek
MAX_PATH = 120
MAX_CONCURRENT = 64
_hits = defaultdict(deque)
_burst = defaultdict(deque)
_sem = threading.Semaphore(MAX_CONCURRENT)
BAD_UA = ("sqlmap", "nikto", "masscan", "zgrab", "nmap", "curl/7.4")
SEC_TXT = ("Contact: mailto:support@alfiliator.id\n"
           "Expires: 2027-12-31T23:59:00.000Z\n"
           "Preferred-Languages: id, en\n"
           "Canonical: %s/.well-known/security.txt\n" % BASE)

CSS = r"""
:root{
  --bg:#07070a;--panel:#0a0a10;--panel2:#10101a;
  --ink:#f4f1ea;--muted:#8f8b81;--dim:#5f5c55;
  --gold:#d4af7a;--gold2:#f0d9b0;--glow:rgba(212,175,122,.4);
  --line:rgba(212,175,122,.16);--line2:rgba(255,255,255,.07);
  --fs:1;--grain:.05;--ease:cubic-bezier(.16,1,.3,1);
}
html[data-theme="sian"]{--gold:#38d6e8;--gold2:#a8f0f8;--glow:rgba(56,214,232,.4);
  --line:rgba(56,214,232,.18)}
html[data-theme="violet"]{--gold:#a48bff;--gold2:#d9ccff;--glow:rgba(164,139,255,.4);
  --line:rgba(164,139,255,.18)}
html[data-theme="zamrud"]{--gold:#3fdb9a;--gold2:#a9f5d2;--glow:rgba(63,219,154,.4);
  --line:rgba(63,219,154,.18)}
html[data-theme="rose"]{--gold:#f0799c;--gold2:#ffc3d4;--glow:rgba(240,121,156,.4);
  --line:rgba(240,121,156,.18)}
html[data-theme="mono"]{--gold:#cfcfcf;--gold2:#ffffff;--glow:rgba(207,207,207,.35);
  --line:rgba(207,207,207,.18)}
html[data-theme="indigo"]{--gold:#7d8cff;--gold2:#c9d0ff;--glow:rgba(125,140,255,.4);--line:rgba(125,140,255,.18)}
html[data-theme="toska"]{--gold:#3fd6c4;--gold2:#a8f2e8;--glow:rgba(63,214,196,.4);--line:rgba(63,214,196,.18)}
html[data-theme="kuning"]{--gold:#f0c04a;--gold2:#ffe6a6;--glow:rgba(240,192,74,.4);--line:rgba(240,192,74,.18)}
html[data-theme="merah"]{--gold:#f0685f;--gold2:#ffb3ad;--glow:rgba(240,104,95,.4);--line:rgba(240,104,95,.18)}
html[data-theme="langit"]{--gold:#5cb8f5;--gold2:#b6e2ff;--glow:rgba(92,184,245,.4);--line:rgba(92,184,245,.18)}
html[data-theme="limau"]{--gold:#a8e05a;--gold2:#dcf7b0;--glow:rgba(168,224,90,.4);--line:rgba(168,224,90,.18)}
html[data-theme="magenta"]{--gold:#ef6ad4;--gold2:#ffc2f2;--glow:rgba(239,106,212,.4);--line:rgba(239,106,212,.18)}
html[data-theme="baja"]{--gold:#9fb0c4;--gold2:#dbe6f0;--glow:rgba(159,176,196,.38);--line:rgba(159,176,196,.18)}
html[data-fs="s"]{--fs:.94}
html[data-fs="l"]{--fs:1.1}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html{scroll-behavior:smooth;scroll-padding-top:96px}
body{font-family:'Sora',sans-serif;background:var(--bg);color:var(--ink);
  font-size:calc(16px * var(--fs));line-height:1.7;overflow-x:hidden;
  -webkit-font-smoothing:antialiased;animation:pg .55s var(--ease)}
@keyframes pg{from{opacity:0;transform:translateY(6px)}}
a{color:inherit;text-decoration:none}img{max-width:100%;display:block}
.wrap{width:min(1200px,100% - 44px);margin-inline:auto}
.mono{font-family:'JetBrains Mono',monospace}

#prog{position:fixed;top:0;left:0;height:2px;width:0;z-index:95;
  background:linear-gradient(90deg,var(--gold),var(--gold2));box-shadow:0 0 14px var(--glow)}
#cur{position:fixed;top:0;left:0;width:360px;height:360px;border-radius:50%;z-index:0;
  pointer-events:none;opacity:0;transition:opacity .5s;
  background:radial-gradient(circle,var(--line),transparent 62%);transform:translate(-50%,-50%)}
@media(pointer:fine){#cur{opacity:1}}
#scan{position:fixed;left:0;right:0;height:120px;z-index:1;pointer-events:none;
  background:linear-gradient(to bottom,transparent,var(--line),transparent);
  opacity:.5;animation:sc 9s linear infinite}
@keyframes sc{0%{top:-140px}100%{top:100%}}

.bgfx{position:fixed;inset:0;z-index:-3;pointer-events:none;overflow:hidden}
.bgfx .orb{position:absolute;border-radius:50%;filter:blur(100px);opacity:.32;will-change:transform}
.bgfx .o1{width:50vmax;height:50vmax;left:-16%;top:-20%;background:radial-gradient(circle,var(--gold),transparent 70%)}
.bgfx .o2{width:44vmax;height:44vmax;right:-18%;top:30%;background:radial-gradient(circle,#2a3f52,transparent 70%)}
.bgfx .o3{width:38vmax;height:38vmax;left:30%;bottom:-24%;background:radial-gradient(circle,var(--gold),transparent 72%)}
.bgfx .mesh{position:absolute;inset:0;opacity:.2;
  background-image:linear-gradient(var(--line2) 1px,transparent 1px),linear-gradient(90deg,var(--line2) 1px,transparent 1px);
  background-size:84px 84px;
  mask-image:radial-gradient(ellipse at 50% 0%,#000 8%,transparent 76%);
  -webkit-mask-image:radial-gradient(ellipse at 50% 0%,#000 8%,transparent 76%)}
.grain{position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:var(--grain);
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='150' height='150'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3'/%3E%3C/filter%3E%3Crect width='150' height='150' filter='url(%23n)'/%3E%3C/svg%3E")}
html[data-grain="off"] .grain{display:none}
html[data-motion="off"] *{animation-duration:.01ms!important;animation-iteration-count:1!important;
  transition-duration:.01ms!important}

header{position:sticky;top:0;z-index:60;backdrop-filter:blur(20px);
  background:rgba(7,7,10,.5);border-bottom:1px solid transparent;transition:.35s}
header.stuck{background:rgba(7,7,10,.94);border-bottom-color:var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:12px;height:72px}
.brand{display:flex;align-items:center;gap:11px;font-size:12px;font-weight:600;letter-spacing:.26em}
.brand b{width:30px;height:30px;display:grid;place-items:center;border:1px solid var(--gold);
  color:var(--gold);font-size:12px;font-family:'Playfair Display',serif;font-weight:700;
  animation:bp 4s ease-in-out infinite}
@keyframes bp{50%{box-shadow:0 0 22px var(--glow)}}
.nl{display:none;gap:22px;font-size:12px;letter-spacing:.09em;color:var(--muted)}
.nl a{position:relative;padding-block:5px;transition:color .25s}
.nl a::after{content:"";position:absolute;left:0;bottom:0;height:1px;width:0;background:var(--gold);transition:width .3s var(--ease)}
.nl a:hover,.nl a.on{color:var(--gold2)}
.nl a:hover::after,.nl a.on::after{width:100%}
.navtools{display:flex;gap:8px;align-items:center}
.iconbtn{width:38px;height:38px;display:grid;place-items:center;border:1px solid var(--line);
  background:none;color:var(--gold);font-size:13px;cursor:pointer;transition:.25s}
.iconbtn:hover{background:var(--panel2)}
.ncta{display:none}
#drawer{position:fixed;inset:72px 0 auto;max-height:calc(100vh - 72px);overflow:auto;z-index:59;
  background:rgba(7,7,10,.985);border-bottom:1px solid var(--line);display:none;
  flex-direction:column;padding:10px 22px 24px;backdrop-filter:blur(20px)}
#drawer.open{display:flex}
#drawer a{padding:13px 0;border-bottom:1px solid var(--line2);font-size:12.6px;
  letter-spacing:.1em;color:var(--muted);display:flex;gap:12px}
#drawer a:hover{color:var(--gold2)}
#drawer a span{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--gold);opacity:.6}
.dhead{font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.24em;
  color:var(--dim);padding:16px 0 8px;text-transform:uppercase}

#panel{position:fixed;top:0;right:0;bottom:0;width:min(340px,86vw);z-index:80;
  background:rgba(9,9,14,.98);border-left:1px solid var(--line);backdrop-filter:blur(24px);
  transform:translateX(102%);transition:transform .4s var(--ease);padding:26px 22px;overflow:auto}
#panel.open{transform:none}
#panel h3{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);margin:26px 0 12px}
#panel h3:first-of-type{margin-top:8px}
.sw{display:flex;gap:10px;flex-wrap:wrap}
.sw button{width:38px;height:38px;border-radius:50%;border:2px solid transparent;cursor:pointer;
  transition:.25s var(--ease)}
.sw button:hover{transform:scale(1.1)}
.sw button[aria-pressed="true"]{border-color:#fff;box-shadow:0 0 0 3px rgba(255,255,255,.12)}
.seg{display:flex;gap:6px}
.seg button{flex:1;padding:9px;border:1px solid var(--line);background:none;color:var(--muted);
  font-size:11px;cursor:pointer;transition:.25s;letter-spacing:.08em}
.seg button[aria-pressed="true"]{border-color:var(--gold);color:var(--gold2);background:var(--panel2)}
#panel .close{position:absolute;top:16px;right:16px}
#panel .note{font-size:11px;color:var(--dim);margin-top:22px;line-height:1.6}

.btn{position:relative;display:inline-flex;align-items:center;justify-content:center;gap:9px;
  padding:13px 26px;font-size:12px;font-weight:600;letter-spacing:.13em;text-transform:uppercase;
  border:1px solid var(--gold);color:var(--gold);overflow:hidden;cursor:pointer;
  transition:.3s var(--ease);white-space:nowrap;background:none}
.btn::before{content:"";position:absolute;inset:0;z-index:-1;
  background:linear-gradient(135deg,var(--gold),var(--gold2));transform:translateY(101%);transition:transform .35s var(--ease)}
.btn:hover{color:#0a0a0e;border-color:var(--gold2)}
.btn:hover::before{transform:translateY(0)}
.btn.solid{background:linear-gradient(135deg,var(--gold),var(--gold2));color:#0a0a0e;border-color:transparent}
.btn.solid::before{background:linear-gradient(135deg,var(--gold2),#fff8e8)}
.btn.ghost{border-color:var(--line);color:var(--ink)}
.btn.ghost:hover{color:#0a0a0e;border-color:var(--gold2)}

.kick{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.32em;
  color:var(--gold);margin-bottom:18px;display:flex;align-items:center;gap:12px;text-transform:uppercase}
.kick::before{content:"";width:30px;height:1px;background:var(--gold)}
h1{font-family:'Playfair Display',serif;font-size:clamp(32px,7vw,64px);font-weight:400;
  line-height:1.06;letter-spacing:-.02em;margin-bottom:22px}
h1 em{font-style:italic;color:var(--gold2)}
h2{font-family:'Playfair Display',serif;font-size:clamp(23px,4.6vw,37px);font-weight:400;
  line-height:1.18;margin-bottom:16px}
h3{font-size:15px;font-weight:600;margin-bottom:9px}
.lead{color:var(--muted);font-size:clamp(14px,2.3vw,16px);max-width:640px}
.hr{height:1px;background:linear-gradient(90deg,var(--gold),transparent);margin:0 0 40px}
.hero{padding:74px 0 84px}.hero .lead{margin-bottom:34px}
.hact{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:46px}
.tags{display:flex;flex-wrap:wrap;gap:20px;font-size:11px;letter-spacing:.1em;color:var(--dim)}
.tags span{display:inline-flex;align-items:center;gap:7px}
.tags i{color:var(--gold);font-size:10px}
.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line2);
  border:1px solid var(--line2);margin-top:48px}
.stat{background:var(--panel);padding:24px 18px;transition:background .3s}
.stat:hover{background:var(--panel2)}
.stat b{display:block;font-family:'Playfair Display',serif;font-size:clamp(22px,5vw,32px);color:var(--gold2)}
.stat span{font-size:9.5px;letter-spacing:.19em;color:var(--dim);text-transform:uppercase}

.rooms{display:grid;gap:1px;background:var(--line2);border:1px solid var(--line2);grid-template-columns:1fr}
.room{position:relative;display:block;background:var(--panel);padding:24px 20px;overflow:hidden;transition:.35s var(--ease)}
.room::after{content:"";position:absolute;inset:0;opacity:0;transition:.35s;pointer-events:none;
  background:radial-gradient(400px circle at var(--mx,50%) var(--my,50%),var(--line),transparent 70%)}
.room:hover{background:var(--panel2)}
.room:hover::after{opacity:1}
.room .no{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--gold);letter-spacing:.2em}
.room h3{margin:12px 0 7px;font-size:13.5px;transition:color .3s}
.room:hover h3{color:var(--gold2)}
.room p{font-size:12px;color:var(--muted)}
.room .ar{position:absolute;right:18px;top:22px;font-size:10px;color:var(--dim);transition:.3s var(--ease)}
.room:hover .ar{color:var(--gold);transform:translate(3px,-3px)}

.grid{display:grid;gap:1px;background:var(--line2);border:1px solid var(--line2);grid-template-columns:1fr}
.cell{position:relative;background:var(--panel);padding:26px 22px;overflow:hidden;transition:.35s var(--ease)}
.cell::after{content:"";position:absolute;inset:0;opacity:0;transition:.35s;pointer-events:none;
  background:radial-gradient(380px circle at var(--mx,50%) var(--my,50%),var(--line),transparent 70%)}
.cell:hover::after{opacity:1}
.cell .ic{width:40px;height:40px;display:grid;place-items:center;border:1px solid var(--line);
  color:var(--gold);font-size:15px;margin-bottom:18px;transition:.35s var(--ease)}
.cell:hover .ic{border-color:var(--gold);transform:translateY(-3px)}
.cell p{font-size:12.6px;color:var(--muted)}
.cell .from{display:inline-block;margin-top:16px;font-family:'JetBrains Mono',monospace;
  font-size:11px;color:var(--gold);letter-spacing:.08em}
.cell::before{content:"";position:absolute;top:0;left:0;width:14px;height:14px;
  border-top:1px solid var(--gold);border-left:1px solid var(--gold);opacity:.5}

.plans{display:grid;gap:1px;background:var(--line2);border:1px solid var(--line2);grid-template-columns:1fr}
.plan{display:flex;flex-direction:column;background:var(--panel);padding:30px 24px;position:relative;transition:.35s}
.plan:hover{background:var(--panel2)}
.plan.hot{background:linear-gradient(175deg,var(--line),var(--panel) 45%)}
.plan .tag{position:absolute;top:0;right:0;padding:5px 12px;background:var(--gold);color:#0a0a0e;
  font-size:8.5px;font-weight:700;letter-spacing:.16em}
.plan h3{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);margin-bottom:14px}
.price{font-family:'Playfair Display',serif;font-size:clamp(25px,5.2vw,32px);color:var(--gold2);line-height:1.1}
.price small{display:block;font-family:'Sora',sans-serif;font-size:10px;color:var(--dim);letter-spacing:.1em;margin-top:6px}
.eta{display:inline-flex;align-items:center;gap:7px;font-family:'JetBrains Mono',monospace;
  font-size:10px;color:var(--gold);border:1px solid var(--line);padding:4px 10px;margin:16px 0 0;letter-spacing:.08em}
.plan ul{list-style:none;margin:20px 0 24px;display:grid;gap:10px;font-size:12.4px;color:#b3afa6}
.plan li{display:flex;gap:9px}.plan li i{color:var(--gold);font-size:10px;margin-top:6px}
.plan li.off{color:var(--dim)}.plan li.off i{color:#3a3730}
.plan .btn{width:100%;margin-top:auto}

.tbl{width:100%;border-collapse:collapse;font-size:12.4px;border:1px solid var(--line2)}
.tbl th,.tbl td{padding:13px 16px;text-align:left;border-bottom:1px solid var(--line2)}
.tbl th{font-size:9.5px;letter-spacing:.17em;text-transform:uppercase;color:var(--gold);
  background:var(--panel2);font-weight:600}
.tbl tr:last-child td{border-bottom:0}.tbl td{color:#b3afa6}.tbl td:first-child{color:var(--ink)}
.sev{display:inline-block;padding:2px 9px;font-size:9.5px;letter-spacing:.12em;border:1px solid}
.sev.c{color:#ff8f8f;border-color:rgba(255,143,143,.4);background:rgba(255,143,143,.08)}
.sev.h{color:#ffc27a;border-color:rgba(255,194,122,.4);background:rgba(255,194,122,.08)}
.sev.m{color:#ffe08a;border-color:rgba(255,224,138,.35);background:rgba(255,224,138,.07)}
.sev.l{color:#9fe0b0;border-color:rgba(159,224,176,.35);background:rgba(159,224,176,.07)}

.steps{display:grid;gap:1px;background:var(--line2);border:1px solid var(--line2);grid-template-columns:1fr;counter-reset:s}
.step{position:relative;background:var(--panel);padding:26px 22px 26px 64px;transition:.3s}
.step:hover{background:var(--panel2)}
.step::before{counter-increment:s;content:"0" counter(s);position:absolute;left:22px;top:26px;
  font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--gold)}
.step p{font-size:12.4px;color:var(--muted)}

.skills{display:grid;gap:22px;grid-template-columns:1fr}
.skill .top{display:flex;justify-content:space-between;font-size:12px;margin-bottom:9px}
.skill .top b{font-family:'JetBrains Mono',monospace;color:var(--gold);font-weight:400}
.bar{height:2px;background:rgba(255,255,255,.08);overflow:hidden}
.bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--gold),var(--gold2));transition:width 1.4s var(--ease)}

.quotes{display:grid;gap:1px;background:var(--line2);border:1px solid var(--line2);grid-template-columns:1fr}
.quote{background:var(--panel);padding:28px 24px}
.quote .st{color:var(--gold);font-size:10px;letter-spacing:3px;margin-bottom:14px}
.quote p{font-family:'Playfair Display',serif;font-size:15px;font-style:italic;color:#ddd8ce;margin-bottom:18px}
.who{display:flex;align-items:center;gap:11px}
.who .av{width:32px;height:32px;display:grid;place-items:center;border:1px solid var(--line);
  color:var(--gold);font-size:11px;font-family:'Playfair Display',serif}
.who b{display:block;font-size:12px}.who span{font-size:10.5px;color:var(--dim)}

details{border:1px solid var(--line2);background:var(--panel);margin-bottom:1px;overflow:hidden;transition:border-color .25s}
details[open]{border-color:var(--line)}
summary{padding:18px 22px;cursor:pointer;font-size:13.2px;list-style:none;display:flex;
  justify-content:space-between;gap:16px;align-items:center}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-family:'JetBrains Mono',monospace;color:var(--gold);font-size:16px;transition:transform .3s var(--ease)}
details[open] summary::after{transform:rotate(45deg)}
.bd{display:grid;grid-template-rows:0fr;transition:grid-template-rows .35s var(--ease)}
details[open] .bd{grid-template-rows:1fr}
.bd>div{overflow:hidden}
.bd p{padding:0 22px 20px;font-size:12.6px;color:var(--muted)}

/* roadmap celah */
.weeks{display:grid;gap:12px;grid-template-columns:1fr}
.wk{position:relative;border:1px solid var(--line2);background:var(--panel);padding:22px 20px 22px 56px;overflow:hidden}
.wk::before{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;background:var(--gold);
  transform:scaleY(0);transform-origin:top;transition:transform .8s var(--ease)}
.wk.on::before{transform:scaleY(1)}
.wk .wn{position:absolute;left:18px;top:22px;font-family:'JetBrains Mono',monospace;font-size:10px;
  color:var(--gold);letter-spacing:.1em}
.wk h4{font-size:13.5px;margin-bottom:6px}
.wk p{font-size:12.2px;color:var(--muted);margin-bottom:14px}
.wk .track{height:3px;background:rgba(255,255,255,.07);overflow:hidden}
.wk .track i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--gold),var(--gold2));transition:width 1.5s var(--ease)}
.wk .st{position:absolute;right:18px;top:20px;font-family:'JetBrains Mono',monospace;
  font-size:9px;letter-spacing:.12em;padding:2px 8px;border:1px solid}
.wk .st.done{color:#9fe0b0;border-color:rgba(159,224,176,.35)}
.wk .st.run{color:var(--gold2);border-color:var(--line);animation:pulse 1.8s ease-in-out infinite}
.wk .st.plan{color:var(--dim);border-color:rgba(255,255,255,.1)}
@keyframes pulse{50%{box-shadow:0 0 16px var(--glow)}}
.wk .arrow{position:absolute;right:16px;bottom:14px;color:var(--gold);font-size:11px;
  animation:ar 1.6s ease-in-out infinite}
@keyframes ar{50%{transform:translate(4px,-4px)}}
.wk.flag{border-color:var(--gold);background:linear-gradient(160deg,var(--line),var(--panel) 60%)}

.cta{border:1px solid var(--line);padding:clamp(36px,6vw,64px) clamp(24px,5vw,54px);
  text-align:center;background:linear-gradient(160deg,var(--line),var(--panel) 62%);position:relative;overflow:hidden}
.cta::after{content:"";position:absolute;inset:-50%;pointer-events:none;
  background:conic-gradient(from 0deg,transparent,var(--line),transparent 38%);animation:sp 11s linear infinite}
@keyframes sp{to{transform:rotate(360deg)}}
.cta>*{position:relative;z-index:1}
.cta p{color:var(--muted);max-width:520px;margin:0 auto 30px;font-size:13.4px}
.cta .row{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}

.cgrid{display:grid;gap:1px;background:var(--line2);border:1px solid var(--line2);grid-template-columns:repeat(2,1fr)}
.clink{display:flex;align-items:center;gap:11px;padding:17px 18px;background:var(--panel);font-size:12.2px;transition:.25s}
.clink:hover{background:var(--panel2);color:var(--gold2)}
.clink i{color:var(--gold);font-size:13px;width:16px}

footer{border-top:1px solid var(--line2);padding:40px 0 50px;margin-top:50px}
.fg{display:flex;flex-wrap:wrap;gap:20px;justify-content:space-between;font-size:11px;color:var(--dim)}

.fab{position:fixed;right:16px;bottom:calc(18px + env(safe-area-inset-bottom));z-index:70;
  width:50px;height:50px;border-radius:50%;display:grid;place-items:center;font-size:20px;
  background:linear-gradient(135deg,var(--gold),var(--gold2));color:#0a0a0e;
  box-shadow:0 14px 36px -12px var(--glow);transition:.25s var(--ease)}
.fab:hover{transform:scale(1.08)}
#top{position:fixed;left:16px;bottom:calc(18px + env(safe-area-inset-bottom));z-index:70;
  width:42px;height:42px;border-radius:50%;display:grid;place-items:center;font-size:12px;
  border:1px solid var(--line);background:rgba(10,10,16,.9);color:var(--muted);
  opacity:0;pointer-events:none;transition:.3s}
#top.on{opacity:1;pointer-events:auto}
#top:hover{color:var(--gold);border-color:var(--gold)}

.rv{opacity:0;transform:translateY(22px);transition:opacity .8s var(--ease),transform .8s var(--ease)}
.rv.on{opacity:1;transform:none}
.pghead{padding:54px 0 40px}

@media(min-width:640px){
  .stats{grid-template-columns:repeat(4,1fr)}
  .rooms,.grid,.quotes{grid-template-columns:repeat(2,1fr)}
  .skills,.cgrid{grid-template-columns:repeat(2,1fr)}
  .steps{grid-template-columns:repeat(2,1fr)}
  .weeks{grid-template-columns:repeat(2,1fr)}
}
@media(min-width:960px){
  .nl,.ncta{display:flex}.burger{display:none}
  .rooms{grid-template-columns:repeat(5,1fr)}
  .grid{grid-template-columns:repeat(3,1fr)}
  .plans{grid-template-columns:repeat(3,1fr)}
  .quotes{grid-template-columns:repeat(3,1fr)}
  .steps{grid-template-columns:repeat(4,1fr)}
  .weeks{grid-template-columns:repeat(4,1fr)}
  .cgrid{grid-template-columns:repeat(4,1fr)}
  .hero{padding:96px 0 100px}
}
"""

JS = r"""
(function(){
  var R=document.documentElement, reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
  var prog=document.getElementById('prog'),hdr=document.getElementById('hdr'),top=document.getElementById('top'),raf=0;
  addEventListener('scroll',function(){
    if(raf)return;
    raf=requestAnimationFrame(function(){
      var h=R.scrollHeight-innerHeight;
      prog.style.width=(h>0?(scrollY/h)*100:0)+'%';
      hdr.classList.toggle('stuck',scrollY>12);
      top.classList.toggle('on',scrollY>640);
      if(!reduce)document.querySelectorAll('.orb').forEach(function(o){
        o.style.transform='translateY('+scrollY*parseFloat(o.dataset.px||0)+'px)'});
      raf=0;
    });
  },{passive:true});
  top.addEventListener('click',function(){scrollTo({top:0,behavior:'smooth'})});
  var bg=document.getElementById('burger'),dr=document.getElementById('drawer');
  if(bg)bg.addEventListener('click',function(){dr.classList.toggle('open')});

  var pn=document.getElementById('panel'),po=document.getElementById('popener');
  if(po)po.addEventListener('click',function(){pn.classList.add('open')});
  var pc=document.getElementById('pclose');
  if(pc)pc.addEventListener('click',function(){pn.classList.remove('open')});

  document.querySelectorAll('.sw button').forEach(function(b){
    b.addEventListener('click',function(){
      R.setAttribute('data-theme',b.dataset.t);
      localStorage.setItem('alf.theme',b.dataset.t);
      document.querySelectorAll('.sw button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});
    });
  });
  document.querySelectorAll('.seg button[data-fs]').forEach(function(b){
    b.addEventListener('click',function(){
      R.setAttribute('data-fs',b.dataset.fs);localStorage.setItem('alf.fs',b.dataset.fs);
      document.querySelectorAll('.seg button[data-fs]').forEach(function(x){x.setAttribute('aria-pressed',x===b)});
    });
  });
  document.querySelectorAll('.seg button[data-mt]').forEach(function(b){
    b.addEventListener('click',function(){
      R.setAttribute('data-motion',b.dataset.mt);localStorage.setItem('alf.motion',b.dataset.mt);
      document.querySelectorAll('.seg button[data-mt]').forEach(function(x){x.setAttribute('aria-pressed',x===b)});
    });
  });
  document.querySelectorAll('.seg button[data-gr]').forEach(function(b){
    b.addEventListener('click',function(){
      R.setAttribute('data-grain',b.dataset.gr);localStorage.setItem('alf.grain',b.dataset.gr);
      document.querySelectorAll('.seg button[data-gr]').forEach(function(x){x.setAttribute('aria-pressed',x===b)});
    });
  });
  var rst=document.getElementById('preset');
  if(rst)rst.addEventListener('click',function(){
    R.setAttribute('data-theme','emas');R.setAttribute('data-fs','m');
    R.setAttribute('data-motion','on');R.setAttribute('data-grain','on');
    localStorage.clear();location.reload();
  });

  if(matchMedia('(pointer:fine)').matches && !reduce){
    var cur=document.getElementById('cur'),cx=innerWidth/2,cy=innerHeight/2,tx=cx,ty=cy;
    addEventListener('pointermove',function(e){tx=e.clientX;ty=e.clientY},{passive:true});
    (function f(){cx+=(tx-cx)*.12;cy+=(ty-cy)*.12;cur.style.left=cx+'px';cur.style.top=cy+'px';requestAnimationFrame(f)})();
    document.querySelectorAll('.btn').forEach(function(b){
      b.addEventListener('pointermove',function(e){var r=b.getBoundingClientRect();
        b.style.transform='translate('+((e.clientX-r.left-r.width/2)/r.width)*5+'px,'+((e.clientY-r.top-r.height/2)/r.height)*4+'px)'});
      b.addEventListener('pointerleave',function(){b.style.transform=''});
    });
  }
  document.querySelectorAll('.cell,.room').forEach(function(el){
    el.addEventListener('pointermove',function(e){var r=el.getBoundingClientRect();
      el.style.setProperty('--mx',(e.clientX-r.left)+'px');
      el.style.setProperty('--my',(e.clientY-r.top)+'px')},{passive:true});
  });

  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      e.target.classList.add('on');
      var b=e.target.querySelector&&e.target.querySelector('b[data-c]');
      if(b&&!b.dataset.done){b.dataset.done=1;
        var end=+b.dataset.c,pre=b.dataset.p||'',suf=b.dataset.s||'',t0=null;b.textContent=pre+suf;
        (function st(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1300);
          b.textContent=pre+Math.floor(end*(1-Math.pow(1-p,3)))+suf;
          if(p<1)requestAnimationFrame(st);else b.textContent=pre+end+suf})(performance.now());}
      e.target.querySelectorAll&&e.target.querySelectorAll('.bar i,.track i').forEach(function(x){x.style.width=x.dataset.w+'%'});
      io.unobserve(e.target);
    });
  },{threshold:.15,rootMargin:'0px 0px -40px'});
  document.querySelectorAll('.rv,.wk').forEach(function(el){io.observe(el)});

  /* ---- bunyi antarmuka ---- */
  var snd = localStorage.getItem('alf.sound') !== 'off';
  var ACX = null;
  function actx(){ if(!ACX){ var C = window.AudioContext || window.webkitAudioContext; if(!C) return null; ACX = new C(); } return ACX; }
  function tone(f, d, type, vol){
    if(!snd) return; var c = actx(); if(!c) return;
    try{
      var o = c.createOscillator(), g = c.createGain(), t = c.currentTime;
      o.type = type || 'sine'; o.frequency.setValueAtTime(f, t);
      g.gain.setValueAtTime(0.0001, t);
      var VV=(+localStorage.getItem('alf.vol')||45)/100;
      g.gain.exponentialRampToValueAtTime(Math.max(0.0002,(vol||0.045)*VV), t + 0.012);
      g.gain.exponentialRampToValueAtTime(0.0001, t + d);
      o.connect(g); g.connect(c.destination); o.start(t); o.stop(t + d + 0.03);
    }catch(e){}
  }
  function PKT(){ return localStorage.getItem('alf.pack')||'lembut'; }
  function sHover(){ var p=PKT(); tone(p==='tajam'?1720:p==='rendah'?720:1180, 0.06, 'triangle', 0.022); }
  function sClick(){ var p=PKT(), f=p==='tajam'?820:p==='rendah'?340:520;
    tone(f, 0.09, 'sine', 0.05); setTimeout(function(){ tone(f*1.5, 0.1, 'sine', 0.04); }, 70); }
  function sGood(){ var p=PKT(), f=p==='tajam'?980:p==='rendah'?420:660;
    tone(f, 0.12, 'sine', 0.05); setTimeout(function(){ tone(f*1.5, 0.16, 'sine', 0.045); }, 90); }
  if(matchMedia('(pointer:fine)').matches && !reduce){
    var hv = 0;
    document.querySelectorAll('a,button,summary,.cell,.room').forEach(function(el){
      el.addEventListener('pointerenter', function(){ var n=Date.now(); if(n-hv<70) return; hv=n; sHover(); });
    });
  }
  document.querySelectorAll('a,button,summary').forEach(function(el){
    el.addEventListener('click', function(e){
      if(el.classList.contains('fab') || el.classList.contains('btn')) sGood(); else sClick();
    });
  });
  document.querySelectorAll('.seg button[data-sd]').forEach(function(b){
    b.addEventListener('click', function(){
      snd = b.dataset.sd === 'on';
      localStorage.setItem('alf.sound', b.dataset.sd);
      document.querySelectorAll('.seg button[data-sd]').forEach(function(x){ x.setAttribute('aria-pressed', x === b); });
      if(snd) sGood();
    });
  });


  function wire(a, k){
    document.querySelectorAll('#panel [data-' + a + ']').forEach(function(b){
      b.addEventListener('click', function(){
        R.setAttribute('data-' + a, b.dataset[a]);
        localStorage.setItem('alf.' + k, b.dataset[a]);
        document.querySelectorAll('#panel [data-' + a + ']').forEach(function(x){ x.setAttribute('aria-pressed', x === b); });
      });
    });
  }

  var PK={atelier:{theme:'emas',rd:'k',dn:'n',cn:'n',wd:'n'},
    editorial:{theme:'kertas',rd:'k',dn:'l',cn:'n',wd:'s'},
    terminal:{theme:'zamrud',rd:'k',dn:'r',cn:'t',wd:'n'},
    lembut:{theme:'anggur',rd:'b',dn:'l',cn:'n',wd:'n'},
    tegas:{theme:'mono',rd:'k',dn:'n',cn:'t',wd:'l'}};
  document.querySelectorAll('#panel [data-pk]').forEach(function(b){
    b.addEventListener('click', function(){
      var cfg=PK[b.dataset.pk]; if(!cfg) return;
      R.setAttribute('data-pk', b.dataset.pk);
      ['theme','rd','dn','cn','wd'].forEach(function(k){
        var v=cfg[k], attr = k==='theme' ? 'data-theme' : 'data-'+k;
        R.setAttribute(attr, v);
        localStorage.setItem('alf.'+(k==='theme'?'theme':k), v);
      });
      document.querySelectorAll('#panel [data-pk]').forEach(function(x){ x.setAttribute('aria-pressed', x===b); });
      document.querySelectorAll('#panel [data-rd],#panel [data-dn],#panel [data-cn],#panel [data-wd]').forEach(function(x){
        var a=x.dataset.rd?'rd':x.dataset.dn?'dn':x.dataset.cn?'cn':x.dataset.wd?'wd':null;
        if(a) x.setAttribute('aria-pressed', String(x.dataset[a]===cfg[a]));
      });
      document.querySelectorAll('#panel [data-t]').forEach(function(x){
        x.setAttribute('aria-pressed', String(x.dataset.t===cfg.theme));
      });
      localStorage.setItem('alf.pk', b.dataset.pk);
    });
  });
  wire('gd','grid');
  wire('wd','wide'); wire('rd','rad'); wire('dn','dense'); wire('cn','con'); wire('tr','tr');

  /* bahasa & mata uang */
  var LGS=[['id','Indonesia'],['en','English'],['ms','Melayu'],['zh','中文'],['ja','日本語'],['ar','العربية']];
  var CRS=[['IDR','Rupiah'],['USD','Dolar AS'],['EUR','Euro'],['SGD','Dolar SG']];
  var UN={rb:1e3,jt:1e6,miliar:1e9}, sL=document.getElementById('lang'), sC=document.getElementById('cur');
  if(sL) LGS.forEach(function(o){ var e=document.createElement('option'); e.value=o[0]; e.textContent=o[1]; sL.appendChild(e); });
  if(sC) CRS.forEach(function(o){ var e=document.createElement('option'); e.value=o[0]; e.textContent=o[1]; sC.appendChild(e); });
  var TR={en:{'Beranda':'Home','Layanan':'Services','Harga':'Pricing','Portofolio':'Portfolio','Proses':'Process','Keamanan':'Security','Ketentuan':'Terms','Tanya':'FAQ','Kontak':'Contact','Mulai':'Start','Matriks':'Comparison','Teknologi Web':'Web Tech','Teknologi Mobile':'Mobile Tech','Integrasi':'Integrations','Infrastruktur':'Infrastructure','Perawatan':'Maintenance','Garansi':'Warranty','Legal':'Legal','Privasi':'Privacy','Syarat':'Terms of Use','Catatan':'Notes','Glosarium':'Glossary','Roadmap Celah':'Gap Roadmap','Kapasitas':'Capacity','Mitra':'Partners','Kolaborasi':'Collaboration','Status':'Status','Dokumentasi':'Docs','Cari':'Search','Proyek Selesai':'Projects Delivered','Klien Kembali':'Returning Clients','Respon':'Response','Kirim Brief':'Send Brief','Lihat Tarif':'See Rates','Konsultasi':'Consult','Formulir':'Form','Perangkat lunak yang dibuat ':'Software built ','benda mahal':'expensive things'},
  ms:{'Beranda':'Utama','Layanan':'Perkhidmatan','Harga':'Harga','Portofolio':'Portfolio','Proses':'Proses','Keamanan':'Keselamatan','Ketentuan':'Terma','Tanya':'Soalan','Kontak':'Hubungi','Mulai':'Mula','Matriks':'Perbandingan','Teknologi Web':'Teknologi Web','Teknologi Mobile':'Teknologi Mudah Alih','Integrasi':'Integrasi','Infrastruktur':'Infrastruktur','Perawatan':'Penyelenggaraan','Garansi':'Jaminan','Legal':'Perundangan','Privasi':'Privasi','Syarat':'Syarat Guna','Catatan':'Nota','Glosarium':'Glosari','Roadmap Celah':'Peta Jurang','Kapasitas':'Kapasiti','Mitra':'Rakan','Kolaborasi':'Kerjasama','Status':'Status','Dokumentasi':'Dokumentasi','Cari':'Cari','Proyek Selesai':'Projek Siap','Klien Kembali':'Klien Berulang','Respon':'Respons','Kirim Brief':'Hantar Brief','Lihat Tarif':'Lihat Kadar','Konsultasi':'Rundingan','Formulir':'Borang','Perangkat lunak yang dibuat ':'Perisian yang dibina ','benda mahal':'barang mahal'},
  zh:{'Beranda':'首页','Layanan':'服务','Harga':'价格','Portofolio':'作品','Proses':'流程','Keamanan':'安全','Ketentuan':'条款','Tanya':'常见问题','Kontak':'联系','Mulai':'开始','Matriks':'对比','Teknologi Web':'Web 技术','Teknologi Mobile':'移动技术','Integrasi':'集成','Infrastruktur':'基础设施','Perawatan':'维护','Garansi':'保修','Legal':'法律','Privasi':'隐私','Syarat':'使用条款','Catatan':'笔记','Glosarium':'术语表','Roadmap Celah':'差距路线图','Kapasitas':'产能','Mitra':'合作伙伴','Kolaborasi':'合作','Status':'状态','Dokumentasi':'文档','Cari':'搜索','Proyek Selesai':'完成项目','Klien Kembali':'回头客','Respon':'响应','Kirim Brief':'发送简报','Lihat Tarif':'查看费率','Konsultasi':'咨询','Formulir':'表单','Perangkat lunak yang dibuat ':'像昂贵物件一样打造的软件','benda mahal':'昂贵物件'},
  ja:{'Beranda':'ホーム','Layanan':'サービス','Harga':'料金','Portofolio':'実績','Proses':'進め方','Keamanan':'セキュリティ','Ketentuan':'規約','Tanya':'よくある質問','Kontak':'お問い合わせ','Mulai':'はじめる','Matriks':'比較','Teknologi Web':'Web技術','Teknologi Mobile':'モバイル技術','Integrasi':'連携','Infrastruktur':'インフラ','Perawatan':'保守','Garansi':'保証','Legal':'法務','Privasi':'プライバシー','Syarat':'利用規約','Catatan':'記録','Glosarium':'用語集','Roadmap Celah':'改善ロードマップ','Kapasitas':'対応枠','Mitra':'パートナー','Kolaborasi':'協業','Status':'稼働状況','Dokumentasi':'ドキュメント','Cari':'検索','Proyek Selesai':'完了案件','Klien Kembali':'リピート顧客','Respon':'返信','Kirim Brief':'ブリーフを送る','Lihat Tarif':'料金を見る','Konsultasi':'相談','Formulir':'フォーム','Perangkat lunak yang dibuat ':'高級品のように作られたソフトウェア','benda mahal':'高級品'},
  ar:{'Beranda':'الرئيسية','Layanan':'الخدمات','Harga':'الأسعار','Portofolio':'الأعمال','Proses':'سير العمل','Keamanan':'الأمان','Ketentuan':'الشروط','Tanya':'الأسئلة','Kontak':'اتصل','Mulai':'ابدأ','Matriks':'المقارنة','Teknologi Web':'تقنيات الويب','Teknologi Mobile':'تقنيات الجوال','Integrasi':'التكامل','Infrastruktur':'البنية التحتية','Perawatan':'الصيانة','Garansi':'الضمان','Legal':'القانوني','Privasi':'الخصوصية','Syarat':'شروط الاستخدام','Catatan':'ملاحظات','Glosarium':'المصطلحات','Roadmap Celah':'خطة الثغرات','Kapasitas':'الطاقة','Mitra':'الشركاء','Kolaborasi':'التعاون','Status':'الحالة','Dokumentasi':'الوثائق','Cari':'بحث','Proyek Selesai':'مشاريع منجزة','Klien Kembali':'عملاء عائدون','Respon':'الاستجابة','Kirim Brief':'أرسل موجزاً','Lihat Tarif':'انظر الأسعار','Konsultasi':'استشارة','Formulir':'نموذج','Perangkat lunak yang dibuat ':'برمجيات تُصنع كأنها قطعة فاخرة','benda mahal':'قطعة فاخرة'}};
  var TX=[], PR=[];
  (function walk(n){
    if(n.nodeType===3){ var v=n.nodeValue; if(v && v.trim()){ n.__o=v; TX.push(n);
      if(/Rp\.?\s?[\d.,]+\s?(miliar|jt|rb)?/i.test(v)){ n.__p=v; PR.push(n); } } return; }
    if(n.nodeType!==1) return; var t=n.tagName;
    if(t==='SCRIPT'||t==='STYLE'||t==='NOSCRIPT') return;
    if(n.id==='panel') return;
    for(var i=0;i<n.childNodes.length;i++) walk(n.childNodes[i]);
  })(document.body);
  function aL(){ var p=(navigator.language||'id').slice(0,2); return LGS.some(function(x){return x[0]===p}) ? p : 'id'; }
  function aC(){ var z=Intl.DateTimeFormat().resolvedOptions().timeZone||'';
    if(/Jakarta|Makassar|Jayapura|Pontianak/.test(z)) return 'IDR';
    if(/Europe\//.test(z)) return 'EUR'; if(/Singapore|Kuala/.test(z)) return 'SGD'; return 'USD'; }
  function fmt(v){ var r=+(localStorage.getItem('alf.rate')||16300);
    var x = CURV==='IDR' ? v : (CURV==='USD' ? v/r : (CURV==='EUR' ? v/r/1.08 : v/r*1.35));
    if(CURV==='IDR') return 'Rp ' + Math.round(x).toLocaleString('id-ID');
    return (CURV==='USD'?'$':CURV==='EUR'?'€':'S$') + Math.round(x).toLocaleString('en-US'); }
  var LNG='id', CURV='IDR';
  function paint(){
    var mp = TR[LNG] || {};
    TX.forEach(function(n){ var k=n.__o.trim(), tr=mp[k]; n.nodeValue = tr ? n.__o.replace(k,tr) : n.__o; });
    PR.forEach(function(n){ n.nodeValue = n.__p.replace(/Rp\.?\s?([\d.,]+)\s?(miliar|jt|rb)?/gi, function(_, d, u){
      return fmt(parseFloat(d.replace(/\./g,'').replace(',','.')) * (UN[(u||'').toLowerCase()]||1)); }); });
    R.lang = LNG; R.dir = LNG === 'ar' ? 'rtl' : 'ltr';
  }
  function save(){ localStorage.setItem('alf.lang', LNG); localStorage.setItem('alf.cur', CURV); }
  if(sL){ sL.value = localStorage.getItem('alf.lang') || 'id'; sL.addEventListener('change', function(){ LNG = sL.value; paint(); save(); }); }
  if(sC){ sC.value = localStorage.getItem('alf.cur') || 'IDR'; sC.addEventListener('change', function(){ CURV = sC.value; paint(); save(); }); }
  var la=document.getElementById('langauto'), ca=document.getElementById('curauto');
  if(la) la.addEventListener('click', function(){ LNG = aL(); if(sL) sL.value = LNG; paint(); save(); });
  if(ca) ca.addEventListener('click', function(){ CURV = aC(); if(sC) sC.value = CURV; paint(); save(); });
  var rt=document.getElementById('rate');
  if(rt){ rt.value = localStorage.getItem('alf.rate') || 16300;
    rt.addEventListener('change', function(){ localStorage.setItem('alf.rate', +rt.value || 16300); paint(); }); }
  LNG = localStorage.getItem('alf.lang') || 'id';
  CURV = localStorage.getItem('alf.cur') || 'IDR';
  paint();

  var ds=document.querySelectorAll('details');
  ds.forEach(function(d){d.addEventListener('toggle',function(){if(d.open)ds.forEach(function(o){if(o!==d)o.close()})})});

  /* ================= lapis gerak v2 ================= */
  (function(){
    var RR=document.documentElement;
    if(matchMedia('(prefers-reduced-motion:reduce)').matches) return;
    var fine=matchMedia('(pointer:fine)').matches;
    function on(){ return RR.getAttribute('data-motion')!=='off'; }

    var veil=document.createElement('div'); veil.id='veil'; document.body.appendChild(veil);
    document.addEventListener('click',function(e){
      var a=e.target.closest?e.target.closest('a'):null; if(!a) return;
      if(a.target==='_blank'||a.hasAttribute('download')) return;
      if(e.metaKey||e.ctrlKey||e.shiftKey) return;
      var h=a.getAttribute('href')||'';
      if(!h||h.charAt(0)==='#'||/^(https?:|mailto:|tel:)/i.test(h)) return;
      if(!on()) return;
      e.preventDefault();
      document.body.classList.add('leaving');
      setTimeout(function(){location.href=h},300);
    });
    addEventListener('pageshow',function(){ document.body.classList.remove('leaving'); });

    document.addEventListener('pointerdown',function(e){
      if(!on()) return;
      var t=e.target.closest?e.target.closest('.btn,.iconbtn,.cell,.room,.plan,.clink,.chip,.fab,.m14-item'):null;
      if(!t) return;
      var r=t.getBoundingClientRect(), d=Math.max(r.width,r.height)*1.8;
      if(getComputedStyle(t).position==='static') t.style.position='relative';
      var sp=document.createElement('span'); sp.className='rip';
      sp.style.cssText='width:'+d+'px;height:'+d+'px;left:'+(e.clientX-r.left)+'px;top:'+(e.clientY-r.top)+'px';
      t.appendChild(sp); setTimeout(function(){sp.remove()},680);
    },{passive:true});

    document.querySelectorAll('.grid,.rooms,.plans,.steps,.cgrid,.weeks,.m14-ledger').forEach(function(p){
      Array.prototype.forEach.call(p.children,function(c,i){
        if(c.style) c.style.transitionDelay=(i*55)+'ms';
      });
    });

    if(fine){
      document.querySelectorAll('.cell,.plan,.quote,.stat').forEach(function(el){
        el.addEventListener('pointermove',function(e){
          if(!on()) return;
          var r=el.getBoundingClientRect();
          var px=(e.clientX-r.left)/r.width-.5, py=(e.clientY-r.top)/r.height-.5;
          el.style.transform='perspective(760px) rotateY('+(px*7).toFixed(2)+'deg) rotateX='.replace('=','(')+(-py*7).toFixed(2)+'deg) translateY(-3px)';
        });
        el.addEventListener('pointerleave',function(){ el.style.transform=''; });
      });
      document.querySelectorAll('.iconbtn,.fab,.chip').forEach(function(b){
        b.addEventListener('pointermove',function(e){
          var r=b.getBoundingClientRect();
          b.style.transform='translate('+((e.clientX-r.left-r.width/2)/r.width*7).toFixed(2)+'px,'+((e.clientY-r.top-r.height/2)/r.height*7).toFixed(2)+'px)';
        });
        b.addEventListener('pointerleave',function(){ b.style.transform=''; });
      });
      var last=0;
      addEventListener('pointermove',function(e){
        if(!on()) return; var n=performance.now(); if(n-last<42) return; last=n;
        var d=document.createElement('i'); d.className='tr-dot';
        d.style.cssText='left:'+e.clientX+'px;top:'+e.clientY+'px';
        document.body.appendChild(d);
        requestAnimationFrame(function(){ d.classList.add('go'); });
        setTimeout(function(){ d.remove(); },700);
      },{passive:true});
    }

    var rq=0;
    addEventListener('scroll',function(){
      if(rq) return;
      rq=requestAnimationFrame(function(){ RR.style.setProperty('--sy',scrollY); rq=0; });
    },{passive:true});
  })();


  /* ================= pusat setelan ================= */
  (function(){
    var P=document.getElementById('panel'); if(!P) return;
    var tabs=[].slice.call(P.querySelectorAll('.ptabs button')),
        grps=[].slice.call(P.querySelectorAll('.pgrp')),
        search=document.getElementById('psearch'), cur='warna';
    function show(g){
      cur=g;
      tabs.forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.tab===g)); });
      grps.forEach(function(x){ x.classList.toggle('on', x.dataset.g===g); });
    }
    tabs.forEach(function(b){ b.addEventListener('click',function(){
      if(search) search.value=''; grps.forEach(function(x){ x.style.display=''; });
      show(b.dataset.tab);
    }); });
    function filter(t){
      t=t.toLowerCase().trim();
      if(!t){ grps.forEach(function(x){ x.style.display=''; }); show(cur); return; }
      grps.forEach(function(x){
        var hit=0;
        [].forEach.call(x.querySelectorAll('.prow'), function(r){
          var ok=r.textContent.toLowerCase().indexOf(t)>-1;
          r.style.display = ok ? '' : 'none'; if(ok) hit++;
        });
        x.classList.toggle('on', hit>0);
        x.style.display = hit ? '' : 'none';
      });
    }
    if(search) search.addEventListener('input', function(){ filter(search.value); });

    wire('font','font'); wire('head','head'); wire('lh','lh'); wire('ls','ls');
    wire('bw','bw'); wire('tbl','tbl'); wire('btn','btn'); wire('nav','nav');
    wire('pat','pat'); wire('sh','sh'); wire('blur','blur'); wire('cur','cur');
    wire('par','par'); wire('acc','acc'); wire('sel','sel'); wire('link','link');
    wire('focus','focus'); wire('pk2','pack');

    var vol=document.getElementById('pvol');
    if(vol){ vol.value=localStorage.getItem('alf.vol')||45;
      vol.addEventListener('input', function(){ localStorage.setItem('alf.vol', vol.value); }); }

    var cc=document.getElementById('pcust');
    if(cc){
      cc.value=localStorage.getItem('alf.custom')||'#d4af7a';
      cc.addEventListener('input', function(){
        var c=cc.value;
        R.style.setProperty('--gold',c); R.style.setProperty('--gold2',c);
        R.style.setProperty('--glow','color-mix(in srgb,'+c+' 40%, transparent)');
        R.style.setProperty('--line','color-mix(in srgb,'+c+' 18%, transparent)');
        localStorage.setItem('alf.custom',c);
      });
    }
    P.querySelectorAll('.sw button[data-t]').forEach(function(b){
      b.addEventListener('click', function(){
        R.style.removeProperty('--gold'); R.style.removeProperty('--gold2');
        R.style.removeProperty('--glow'); R.style.removeProperty('--line');
        localStorage.removeItem('alf.custom');
      });
    });

    function keys(){ var o={}; for(var i=0;i<localStorage.length;i++){
      var k=localStorage.key(i); if(k&&k.indexOf('alf.')===0) o[k]=localStorage.getItem(k); } return o; }
    var ex=document.getElementById('pexp');
    if(ex) ex.onclick=function(){
      var b=new Blob([JSON.stringify(keys(),null,2)],{type:'application/json'}), u=URL.createObjectURL(b);
      var a=document.createElement('a'); a.href=u; a.download='setelan-alfiliator.json'; a.click();
      URL.revokeObjectURL(u);
    };
    var im=document.getElementById('pimp'), fl=document.getElementById('pfile');
    if(im&&fl){
      im.onclick=function(){ fl.click(); };
      fl.onchange=function(e){
        var f=e.target.files[0]; if(!f) return; var rd=new FileReader();
        rd.onload=function(){
          try{ var o=JSON.parse(rd.result);
            Object.keys(o).forEach(function(k){ if(k.indexOf('alf.')===0) localStorage.setItem(k,o[k]); });
            location.reload();
          }catch(x){ alert('Berkas tidak terbaca.'); }
        };
        rd.readAsText(f);
      };
    }
    var cp=document.getElementById('pcopy');
    if(cp) cp.onclick=function(){
      var u=location.origin+location.pathname+'#s='+btoa(unescape(encodeURIComponent(JSON.stringify(keys()))));
      if(navigator.clipboard) navigator.clipboard.writeText(u);
      var old=cp.textContent; cp.textContent='Tersalin';
      setTimeout(function(){ cp.textContent=old; }, 1400);
    };

    var RG={warna:['theme','custom','acc','con','tr','sel','pk'],
      huruf:['font','head','fs','lh','ls'],
      tata:['wide','dense','rad','bw','tbl','btn','nav','grid'],
      efek:['motion','par','grain','pat','sh','blur','cur','focus','link'],
      suara:['sound','vol','pack']};
    P.querySelectorAll('[data-rg]').forEach(function(b){
      b.addEventListener('click', function(){
        (RG[b.dataset.rg]||[]).forEach(function(k){ localStorage.removeItem('alf.'+k); });
        location.reload();
      });
    });

    if(location.hash.indexOf('#s=')===0){
      try{
        var o=JSON.parse(decodeURIComponent(escape(atob(location.hash.slice(3)))));
        Object.keys(o).forEach(function(k){ if(k.indexOf('alf.')===0) localStorage.setItem(k,o[k]); });
        location.replace(location.pathname);
      }catch(e){}
    }

    var hdr=document.getElementById('hdr'), ly=0;
    addEventListener('scroll', function(){
      if(!hdr) return;
      if(R.getAttribute('data-nav')!=='sembunyi'){ hdr.classList.remove('navhide'); ly=scrollY; return; }
      var y=scrollY;
      hdr.classList.toggle('navhide', y>240 && y>ly);
      ly=y;
    }, {passive:true});
  })();

  /* palet perintah */
  (function(){
    var box=document.createElement('div'); box.id='cmdk';
    box.innerHTML='<div class="box"><input id="ckq" placeholder="Cari ruang atau alat\u2026" autocomplete="off">'
      +'<div class="res" id="ckr"></div>'
      +'<div class="ft"><span>enter buka</span><span>esc tutup</span></div></div>';
    document.body.appendChild(box);
    var q=box.querySelector('#ckq'), r=box.querySelector('#ckr'), idx=[], sel=0;
    function open(){ box.classList.add('on'); q.value=''; r.innerHTML=''; q.focus(); load(); }
    function close(){ box.classList.remove('on'); }
    function load(){
      if(idx.length) return;
      fetch('/index.json').then(function(x){ return x.json(); }).then(function(d){
        idx=d.concat([
          {u:'/lab',t:'Lab',d:'Kumpulan alat'},
          {u:'/securescan',t:'SecureScan',d:'Skor URL dan DNS'},
          {u:'/passguard',t:'PassGuard',d:'Sandi dan brankas'},
          {u:'/netguard',t:'NetGuard',d:'Jaringan lokal'},
          {u:'/phishcatcher',t:'PhishCatcher',d:'Simulasi phish'},
          {u:'/osint-track',t:'OSINT-Track',d:'Jejak publik'}
        ]);
      }).catch(function(){});
    }
    function paint(){
      var t=q.value.toLowerCase().trim(); r.innerHTML=''; sel=0;
      if(!t) return;
      idx.filter(function(x){ return (x.t+' '+x.d+' '+x.u).toLowerCase().indexOf(t)>-1; })
        .slice(0,9).forEach(function(x){
          var a=document.createElement('a'); a.href=x.u;
          a.innerHTML='<b>'+x.u+'</b><span>'+x.t+'</span>';
          r.appendChild(a);
        });
      var f=r.querySelector('a'); if(f) f.classList.add('sel');
    }
    q.addEventListener('input', paint);
    q.addEventListener('keydown', function(e){
      var items=[].slice.call(r.querySelectorAll('a'));
      if(e.key==='Escape') close();
      if(e.key==='ArrowDown'||e.key==='ArrowUp'){
        e.preventDefault(); if(!items.length) return;
        items[sel].classList.remove('sel');
        sel=(sel+(e.key==='ArrowDown'?1:-1)+items.length)%items.length;
        items[sel].classList.add('sel');
      }
      if(e.key==='Enter' && items[sel]) location.href=items[sel].getAttribute('href');
    });
    box.addEventListener('click', function(e){ if(e.target===box) close(); });
    document.addEventListener('keydown', function(e){
      var tag=(e.target.tagName||'').toLowerCase();
      var typing=tag==='input'||tag==='textarea'||tag==='select';
      if((e.ctrlKey||e.metaKey) && e.key.toLowerCase()==='k'){
        e.preventDefault(); box.classList.contains('on')?close():open();
      } else if(e.key==='/' && !typing){ e.preventDefault(); open(); }
    });
  })();


  if('serviceWorker' in navigator && location.protocol==='https:'){
    addEventListener('load', function(){ navigator.serviceWorker.register('/sw.js').catch(function(){}); });
  }

})();
"""

EXTRA_CSS = r"""
.skip{position:absolute;left:-9999px;top:0;z-index:99;padding:12px 18px;background:var(--gold);color:#0a0a0e;font-size:12px}
.skip:focus{left:8px;top:8px}
:focus-visible{outline:2px solid var(--gold);outline-offset:3px}
@media print{
  header,footer,.fab,#top,#panel,#cur,#scan,.bgfx,.grain{display:none!important}
  body{background:#fff;color:#000;font-size:11pt}
  h1,h2,.price{color:#000}
  .cell,.plan,.quote,.tbl,.wk{border:1px solid #bbb;background:#fff;color:#000}
  a[href^="http"]::after{content:" (" attr(href) ")";font-size:8pt;color:#555}
}
"""

EXTRA_CSS += r"""
.showcase{display:grid;gap:40px;justify-items:center;padding:8px 0 12px;grid-template-columns:1fr}
@media(min-width:760px){.showcase{grid-template-columns:1fr 1fr}}
.dev{perspective:1100px;width:min(240px,68vw);position:relative}
.dev::after{content:"";position:absolute;inset:-16% -22%;z-index:-1;border-radius:50%;
  background:radial-gradient(circle,var(--glow),transparent 68%);filter:blur(26px);opacity:.5}
.dev-in{position:relative;transform-style:preserve-3d;border-radius:36px;padding:9px;
  background:linear-gradient(160deg,#3a3f4b,#141821 55%,#0a0d13);
  box-shadow:0 44px 80px -34px rgba(0,0,0,.92),0 0 0 1px rgba(255,255,255,.1),inset 0 0 0 1px rgba(255,255,255,.05);
  animation:sway 7.5s ease-in-out infinite}
@keyframes sway{0%,100%{transform:rotateY(-15deg) rotateX(7deg) translateY(0)}
  50%{transform:rotateY(15deg) rotateX(-5deg) translateY(-10px)}}
.scr{position:relative;border-radius:27px;overflow:hidden;aspect-ratio:9/19.5;
  background:linear-gradient(168deg,#f2fbff,#c9e8ff 34%,#ffd8ec 68%,#fff4d9)}
.scr::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(115deg,rgba(255,255,255,.85) 0%,transparent 34%,transparent 62%,rgba(255,255,255,.5) 100%);
  mix-blend-mode:screen;opacity:.55}
.dtop{position:absolute;top:0;left:0;right:0;height:46px;display:flex;align-items:center;
  justify-content:space-between;padding:0 16px;font-family:'JetBrains Mono',monospace;
  font-size:9px;color:#1b2430;z-index:3}
.island{position:absolute;top:9px;left:50%;transform:translateX(-50%);width:74px;height:20px;
  border-radius:99px;background:#0b0f16;z-index:4}
.punch{position:absolute;top:11px;left:50%;transform:translateX(-50%);width:11px;height:11px;
  border-radius:50%;background:#0b0f16;z-index:4}
.dbody{padding:56px 14px 14px;display:grid;gap:9px}
.dhero{height:62px;border-radius:13px;background:linear-gradient(120deg,#7fd0ff,#c9a6ff 60%,#ffc4e0);
  box-shadow:0 8px 20px -8px rgba(60,120,200,.5)}
.drow{display:flex;gap:7px}
.dcard{flex:1;height:44px;border-radius:10px;background:rgba(255,255,255,.78);
  box-shadow:0 4px 12px -6px rgba(40,70,110,.4)}
.dline{height:7px;border-radius:99px;background:rgba(27,36,48,.16)}
.dline.s{width:58%}
.dbtn{height:34px;border-radius:10px;margin-top:2px;
  background:linear-gradient(120deg,#1b2430,#3b4a60)}
.dbar{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);width:88px;height:4px;
  border-radius:99px;background:rgba(27,36,48,.32);z-index:3}
.side{position:absolute;right:-2px;top:88px;width:3px;height:52px;border-radius:2px;
  background:linear-gradient(#5a6272,#2a303c)}
.side.v{top:150px;height:34px}
.devlab{text-align:center;margin-top:16px;font-family:'JetBrains Mono',monospace;
  font-size:10px;letter-spacing:.24em;color:var(--gold)}
@media(prefers-reduced-motion:reduce){.dev-in{animation:none;transform:none}}

.dev.tab .dev-in{border-radius:20px;padding:13px}
.dev.tab .scr{aspect-ratio:3/4;border-radius:14px}
.dev.tab .dev-in::before{content:"";position:absolute;top:5px;left:50%;transform:translateX(-50%);
  width:6px;height:6px;border-radius:50%;background:#0b0f16;z-index:5}
.dev.lap .dev-in{border-radius:12px;padding:10px}
.dev.lap .scr{aspect-ratio:16/10;border-radius:7px}
.dev.lap .dev-in::after{content:"";position:absolute;left:-7%;right:-7%;bottom:-13px;height:11px;
  border-radius:0 0 12px 12px;background:linear-gradient(#3a3f4b,#141821)}
.dev.pc .dev-in{border-radius:9px;padding:10px}
.dev.pc .scr{aspect-ratio:16/9;border-radius:5px}
.dev.pc .dev-in::after{content:"";position:absolute;left:50%;transform:translateX(-50%);
  bottom:-30px;width:52px;height:30px;background:linear-gradient(#2a2f3a,#141821);border-radius:0 0 7px 7px}
.dev.pc .dev-in::before{content:"";position:absolute;left:50%;transform:translateX(-50%);
  bottom:-34px;width:96px;height:6px;border-radius:99px;background:#1a1d24}
"""

EXTRA_CSS += r"""
html{--rad:0px}
html[data-rd="n"]{--rad:2px}html[data-rd="b"]{--rad:14px}
.btn,.cell,.plan,.room,.tbl,.iconbtn,.seg button,.sw button,details,.cta,.wk,.quote,.step,.sel,.inp,.plan .tag{border-radius:var(--rad)}
html[data-wd="s"] .wrap{width:min(860px,100% - 44px)}
html[data-wd="l"] .wrap{width:min(1440px,100% - 30px)}
html[data-dn="r"] body{line-height:1.5}
html[data-dn="r"] .cell,html[data-dn="r"] .plan,html[data-dn="r"] .room{padding:16px 15px}
html[data-dn="r"] h1,html[data-dn="r"] h2{margin-bottom:10px}
html[data-dn="l"] .cell,html[data-dn="l"] .plan,html[data-dn="l"] .room{padding:34px 28px}
html[data-cn="t"]{--muted:#cdc8be;--dim:#a09b91}
html[data-cn="t"] .lead{color:var(--ink)}
html[data-tr="t"] .cell,html[data-tr="t"] .plan,html[data-tr="t"] .room,html[data-tr="t"] .quote,html[data-tr="t"] .stat{opacity:.84;backdrop-filter:blur(7px)}
html[data-theme="kertas"]{--bg:#f6f3ec;--panel:#fffdf8;--panel2:#efe9dd;--ink:#14130f;--muted:#5c574d;--dim:#8b857a;--gold:#a8792c;--gold2:#7d5a1d;--glow:rgba(168,121,44,.3);--line:rgba(20,19,15,.16);--line2:rgba(20,19,15,.09)}
html[data-theme="kapur"]{--bg:#eef3f7;--panel:#fbfdff;--panel2:#e2eaf1;--ink:#0f1519;--muted:#54606a;--dim:#83919c;--gold:#3b7fa6;--gold2:#255d7d;--glow:rgba(59,127,166,.3);--line:rgba(15,21,25,.16);--line2:rgba(15,21,25,.09)}
html[data-theme="senja"]{--gold:#ff8a4c;--gold2:#ffc39a;--glow:rgba(255,138,76,.4);--line:rgba(255,138,76,.18)}
html[data-theme="anggur"]{--gold:#b4527a;--gold2:#eaa6c1;--glow:rgba(180,82,122,.4);--line:rgba(180,82,122,.18)}
html[data-theme="kertas"] header{background:rgba(246,243,236,.72)}
html[data-theme="kapur"] header{background:rgba(238,243,247,.72)}
html[data-theme="kertas"] header.stuck,html[data-theme="kapur"] header.stuck{background:var(--bg)}
html[data-theme="kertas"] #drawer,html[data-theme="kapur"] #drawer{background:var(--bg)}
html[data-theme="kertas"] #panel,html[data-theme="kapur"] #panel{background:var(--panel)}
.sel,.inp{width:100%;padding:9px;border:1px solid var(--line);background:var(--panel2);color:var(--ink);font-family:inherit;font-size:11.5px}
@media(max-width:639px){
  .wk{padding-right:50px}
  .wk .st{position:static;display:inline-block;margin:0 0 8px;padding:2px 8px}
  .wk .arrow{right:14px;bottom:12px}
  .tbl{display:block;overflow-x:auto}
  .tbl th,.tbl td{white-space:nowrap}
}
"""

EXTRA_CSS += r"""
#rp{position:fixed;right:16px;bottom:calc(80px + env(safe-area-inset-bottom));z-index:75;
  height:46px;padding:0 16px;display:flex;gap:8px;align-items:center;border:0;border-radius:99px;
  background:linear-gradient(135deg,var(--gold),var(--gold2));color:#0a0a0e;cursor:pointer;
  font-family:'JetBrains Mono',monospace;font-size:10.5px;font-weight:700;letter-spacing:.16em;
  box-shadow:0 12px 30px -12px var(--glow);animation:rpulse 2.4s infinite;transition:transform .2s}
#rp:hover{transform:scale(1.05)}
#rp b{font-size:13px;line-height:1}
@keyframes rpulse{0%{box-shadow:0 0 0 0 var(--glow),0 12px 30px -12px var(--glow)}
  65%{box-shadow:0 0 0 15px transparent,0 12px 30px -12px var(--glow)}
  100%{box-shadow:0 0 0 0 transparent,0 12px 30px -12px var(--glow)}}
#rpp{position:fixed;right:12px;bottom:calc(136px + env(safe-area-inset-bottom));z-index:76;
  width:min(340px,calc(100vw - 24px));max-height:min(66vh,560px);display:none;flex-direction:column;
  border:1px solid var(--line);background:rgba(9,9,14,.975);backdrop-filter:blur(22px);
  border-radius:calc(var(--rad) + 5px);overflow:hidden;box-shadow:0 26px 64px -20px #000}
#rpp.open{display:flex}
#rph{padding:12px 14px;border-bottom:1px solid var(--line2);display:flex;justify-content:space-between;
  align-items:center;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.16em;color:var(--gold)}
#rph em{font-style:normal;color:var(--dim);font-size:8.5px;letter-spacing:.08em}
#rpx{cursor:pointer;color:var(--dim)}
.rmode{display:flex;gap:6px;padding:9px 12px;border-bottom:1px solid var(--line2)}
.rmode[hidden]{display:none}
.rmode select,.rmode input{flex:1;min-width:0;background:var(--panel2);border:1px solid var(--line2);
  color:var(--ink);font:inherit;font-size:10.5px;padding:6px 7px;border-radius:6px}
#rpb{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:9px;font-size:12.2px;line-height:1.55}
.rpm{max-width:88%;padding:9px 12px;border-radius:calc(var(--rad) + 3px);background:var(--panel2);border:1px solid var(--line2)}
.rpm.me{align-self:flex-end;background:linear-gradient(135deg,var(--gold),var(--gold2));color:#0a0a0e;
  border-color:transparent;font-weight:500}
.rpm a{color:var(--gold2);text-decoration:underline}
.rpm.me a{color:#0a0a0e}
.chips{display:flex;flex-wrap:wrap;gap:6px;padding:0 12px 10px}
.chip{font-size:10.5px;border:1px solid var(--line);background:none;color:var(--muted);
  padding:5px 10px;border-radius:99px;cursor:pointer;font:inherit}
.chip:hover{color:var(--gold2);border-color:var(--gold)}
.rthink{font-size:10.5px;color:var(--dim);font-family:'JetBrains Mono',monospace}
#rpf{display:flex;gap:7px;padding:10px;border-top:1px solid var(--line2)}
#rpi{flex:1;min-width:0;background:var(--panel2);border:1px solid var(--line2);color:var(--ink);
  padding:9px 11px;font:inherit;font-size:12px;border-radius:calc(var(--rad) + 2px)}
#rps{width:42px;border:1px solid var(--gold);background:none;color:var(--gold);cursor:pointer;
  border-radius:calc(var(--rad) + 2px);font-size:14px}
#nfilter{width:100%;padding:10px 12px;background:var(--panel2);border:1px solid var(--line2);
  color:var(--ink);font:inherit;font-size:12.4px;margin-bottom:10px;border-radius:var(--rad)}
.pk{position:absolute;left:8px;width:4px;height:14px;border-radius:2px;
  background:var(--gold2);box-shadow:0 0 12px var(--glow);animation:pk 8s linear infinite}
@keyframes pk{0%{top:-14px;opacity:0}6%{opacity:1}90%{opacity:1}100%{top:100%;opacity:0}}
@media print{#rp,#rpp{display:none!important}}
"""

EXTRA_CSS += r"""
#rp{position:fixed;right:16px;bottom:calc(80px + env(safe-area-inset-bottom));z-index:75;
  height:46px;padding:0 16px;display:flex;gap:8px;align-items:center;border:0;border-radius:99px;
  background:linear-gradient(135deg,var(--gold),var(--gold2));color:#0a0a0e;cursor:pointer;
  font-family:'JetBrains Mono',monospace;font-size:10.5px;font-weight:700;letter-spacing:.16em;
  box-shadow:0 12px 30px -12px var(--glow);animation:rpulse 2.4s infinite;transition:transform .2s}
#rp:hover{transform:scale(1.05)}
#rp b{font-size:13px;line-height:1}
@keyframes rpulse{0%{box-shadow:0 0 0 0 var(--glow),0 12px 30px -12px var(--glow)}
  65%{box-shadow:0 0 0 15px transparent,0 12px 30px -12px var(--glow)}
  100%{box-shadow:0 0 0 0 transparent,0 12px 30px -12px var(--glow)}}
#rpp{position:fixed;right:12px;bottom:calc(136px + env(safe-area-inset-bottom));z-index:76;
  width:min(340px,calc(100vw - 24px));max-height:min(66vh,560px);display:none;flex-direction:column;
  border:1px solid var(--line);background:rgba(9,9,14,.975);backdrop-filter:blur(22px);
  border-radius:calc(var(--rad) + 5px);overflow:hidden;box-shadow:0 26px 64px -20px #000}
#rpp.open{display:flex}
#rph{padding:12px 14px;border-bottom:1px solid var(--line2);display:flex;justify-content:space-between;
  align-items:center;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.16em;color:var(--gold)}
#rph em{font-style:normal;color:var(--dim);font-size:8.5px;letter-spacing:.08em}
#rpx{cursor:pointer;color:var(--dim)}
.rmode{display:flex;gap:6px;padding:9px 12px;border-bottom:1px solid var(--line2)}
.rmode[hidden]{display:none}
.rmode select,.rmode input{flex:1;min-width:0;background:var(--panel2);border:1px solid var(--line2);
  color:var(--ink);font:inherit;font-size:10.5px;padding:6px 7px;border-radius:6px}
#rpb{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:9px;font-size:12.2px;line-height:1.55}
.rpm{max-width:88%;padding:9px 12px;border-radius:calc(var(--rad) + 3px);background:var(--panel2);border:1px solid var(--line2)}
.rpm.me{align-self:flex-end;background:linear-gradient(135deg,var(--gold),var(--gold2));color:#0a0a0e;
  border-color:transparent;font-weight:500}
.rpm a{color:var(--gold2);text-decoration:underline}
.rpm.me a{color:#0a0a0e}
.chips{display:flex;flex-wrap:wrap;gap:6px;padding:0 12px 10px}
.chip{font-size:10.5px;border:1px solid var(--line);background:none;color:var(--muted);
  padding:5px 10px;border-radius:99px;cursor:pointer;font:inherit}
.chip:hover{color:var(--gold2);border-color:var(--gold)}
.rthink{font-size:10.5px;color:var(--dim);font-family:'JetBrains Mono',monospace}
#rpf{display:flex;gap:7px;padding:10px;border-top:1px solid var(--line2)}
#rpi{flex:1;min-width:0;background:var(--panel2);border:1px solid var(--line2);color:var(--ink);
  padding:9px 11px;font:inherit;font-size:12px;border-radius:calc(var(--rad) + 2px)}
#rps{width:42px;border:1px solid var(--gold);background:none;color:var(--gold);cursor:pointer;
  border-radius:calc(var(--rad) + 2px);font-size:14px}
#nfilter{width:100%;padding:10px 12px;background:var(--panel2);border:1px solid var(--line2);
  color:var(--ink);font:inherit;font-size:12.4px;margin-bottom:10px;border-radius:var(--rad)}
.pk{position:absolute;left:8px;width:4px;height:14px;border-radius:2px;
  background:var(--gold2);box-shadow:0 0 12px var(--glow);animation:pk 8s linear infinite}
@keyframes pk{0%{top:-14px;opacity:0}6%{opacity:1}90%{opacity:1}100%{top:100%;opacity:0}}
@media print{#rp,#rpp{display:none!important}}
"""

EXTRA_CSS += r"""
.flow{display:grid;gap:7px;position:relative}
.flow::before{content:"";position:absolute;left:9px;top:0;width:2px;height:100%;background:linear-gradient(var(--gold),transparent);opacity:.25}
.nd{position:relative;border:1px solid var(--line2);background:var(--panel);padding:13px 15px 13px 30px;display:flex;justify-content:space-between;gap:10px;align-items:center;font-family:'JetBrains Mono',monospace;font-size:10.5px;overflow:hidden;animation:gate 8s linear infinite}
.nd b{color:var(--gold);letter-spacing:.13em}
.nd span{color:var(--dim);font-size:9.5px;text-align:right}
.nd::after{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--gold);transform:scaleY(0);transform-origin:top;animation:gbar 8s linear infinite}
.nd:nth-child(2)::after,.nd:nth-child(2){animation-delay:.8s}
.nd:nth-child(3)::after,.nd:nth-child(3){animation-delay:1.6s}
.nd:nth-child(4)::after,.nd:nth-child(4){animation-delay:2.4s}
.nd:nth-child(5)::after,.nd:nth-child(5){animation-delay:3.2s}
.nd:nth-child(6)::after,.nd:nth-child(6){animation-delay:4s}
.nd:nth-child(7)::after,.nd:nth-child(7){animation-delay:4.8s}
@keyframes gbar{0%{transform:scaleY(0)}5%{transform:scaleY(1)}18%{transform:scaleY(1)}24%{transform:scaleY(0)}100%{transform:scaleY(0)}}
@keyframes gate{0%,24%,100%{border-color:var(--line2)}8%,16%{border-color:var(--gold);box-shadow:0 0 18px -6px var(--glow)}}
.tel{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line2);border:1px solid var(--line2);margin-top:18px}
.tel div{background:var(--panel);padding:14px 15px}
.tel b{display:block;font-family:'JetBrains Mono',monospace;font-size:15px;color:var(--gold2)}
.tel span{font-size:9px;letter-spacing:.16em;color:var(--dim);text-transform:uppercase}
.tel .live{color:#9fe0b0}

html[data-pk="editorial"] .wrap{width:min(820px,100% - 60px)}
html[data-pk="editorial"] h1{font-size:clamp(40px,7vw,76px);letter-spacing:-.03em}
html[data-pk="editorial"] .cell,html[data-pk="editorial"] .room{border-left:1px solid var(--line)}
html[data-pk="terminal"]{--rad:0px;--line:rgba(63,219,154,.22);--line2:rgba(63,219,154,.1)}
html[data-pk="terminal"] body{font-family:'JetBrains Mono',monospace;font-size:calc(14px * var(--fs))}
html[data-pk="terminal"] h1,html[data-pk="terminal"] h2{font-family:'JetBrains Mono',monospace;letter-spacing:-.04em}
html[data-pk="terminal"] .kick::before{background:#3fdb9a}
html[data-pk="lembut"]{--rad:18px}
html[data-pk="lembut"] .cell,html[data-pk="lembut"] .plan,html[data-pk="lembut"] .room{
  box-shadow:0 12px 30px -22px #000}
html[data-pk="tegas"]{--rad:0px;--line:rgba(255,255,255,.3)}
html[data-pk="tegas"] .btn{border-width:2px}
html[data-pk="tegas"] h1 em{-webkit-text-fill-color:currentColor;background:none}
html[data-grid="on"] body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:linear-gradient(var(--line2) 1px,transparent 1px),
  linear-gradient(90deg,var(--line2) 1px,transparent 1px);background-size:32px 32px;opacity:.5}

/* tata letak layar besar */
@media(min-width:768px){
  .wrap{width:min(760px,100% - 56px)}
  .hero{padding:88px 0 92px}
  h1{font-size:clamp(38px,5.4vw,60px)}
  .lead{font-size:16.5px}
  .grid,.rooms,.quotes,.steps,.cgrid{grid-template-columns:repeat(2,1fr)}
  .tbl th,.tbl td{padding:15px 18px}
  .btn{padding:15px 30px;font-size:12.5px}
  .iconbtn{width:42px;height:42px}
  .reg,.rpp{font-size:13.5px}
}
@media(min-width:1024px){
  .wrap{width:min(1000px,100% - 72px)}
  .grid,.rooms{grid-template-columns:repeat(3,1fr)}
  .steps,.weeks{grid-template-columns:repeat(2,1fr)}
  .cgrid{grid-template-columns:repeat(3,1fr)}
  .hero{padding:104px 0 108px}
  .cell,.room{padding:28px 24px}
  .stats{grid-template-columns:repeat(4,1fr)}
}
@media(min-width:1440px){
  .wrap{width:min(1240px,100% - 96px)}
  .grid,.rooms{grid-template-columns:repeat(4,1fr)}
  .quotes{grid-template-columns:repeat(3,1fr)}
  h1{font-size:64px}
}
@media(min-width:768px) and (pointer:coarse){
  .nl{gap:26px;font-size:12.5px}
  .nl a{padding-block:9px}
  .iconbtn{width:46px;height:46px}
  .seg button{padding:12px}
  .sw button{width:44px;height:44px}
  #panel{width:min(400px,70vw)}
}
@media(hover:hover){
  .room:hover .ar{transform:translate(4px,-4px)}
  .clink:hover i{transform:translateX(3px)}
  .clink i{transition:transform .25s}
}
@media(min-width:768px){#rp{height:50px;padding:0 20px}}
#rp{position:fixed;right:16px;bottom:calc(80px + env(safe-area-inset-bottom));z-index:75;width:50px;height:50px;border-radius:50%;display:grid;place-items:center;font-size:18px;border:1px solid var(--line);background:rgba(10,10,16,.92);color:var(--gold);backdrop-filter:blur(12px);cursor:pointer;transition:.25s}
#rp:hover{color:var(--gold2);border-color:var(--gold);transform:scale(1.06)}
#rpp{position:fixed;right:12px;bottom:calc(140px + env(safe-area-inset-bottom));z-index:76;width:min(330px,calc(100vw - 24px));max-height:min(62vh,520px);display:none;flex-direction:column;border:1px solid var(--line);background:rgba(9,9,14,.97);backdrop-filter:blur(20px);border-radius:calc(var(--rad) + 4px);overflow:hidden;box-shadow:0 24px 60px -20px #000}
#rpp.open{display:flex}
#rph{padding:12px 14px;border-bottom:1px solid var(--line2);display:flex;justify-content:space-between;align-items:center;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.18em;color:var(--gold)}
#rph em{font-style:normal;color:var(--dim);font-size:8.5px;letter-spacing:.1em}
#rpb{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:9px;font-size:12.2px;line-height:1.55}
.rpm{max-width:88%;padding:9px 12px;border-radius:calc(var(--rad) + 3px);background:var(--panel2);border:1px solid var(--line2)}
.rpm.me{align-self:flex-end;background:linear-gradient(135deg,var(--gold),var(--gold2));color:#0a0a0e;border-color:transparent;font-weight:500}
.rpm a{color:var(--gold2);text-decoration:underline}
#rpf{display:flex;gap:7px;padding:10px;border-top:1px solid var(--line2)}
#rpi{flex:1;background:var(--panel2);border:1px solid var(--line2);color:var(--ink);padding:9px 11px;font:inherit;font-size:12px;border-radius:calc(var(--rad) + 2px)}
#rps{width:40px;border:1px solid var(--gold);background:none;color:var(--gold);cursor:pointer;border-radius:calc(var(--rad) + 2px)}
.noteitem{display:flex;gap:10px;justify-content:space-between;align-items:flex-start;border:1px solid var(--line2);background:var(--panel);padding:12px 14px;margin-bottom:1px;font-size:12.4px}
.noteitem time{font-family:'JetBrains Mono',monospace;font-size:9.5px;color:var(--dim);display:block;margin-bottom:4px}
.noteitem button{background:none;border:1px solid var(--line2);color:var(--dim);cursor:pointer;padding:3px 8px;font-size:10px}
#ntext{width:100%;min-height:88px;background:var(--panel2);border:1px solid var(--line);color:var(--ink);padding:12px;font:inherit;font-size:12.6px;border-radius:var(--rad)}
@media print{#rp,#rpp{display:none!important}}
"""

EXTRA_CSS += r'''
/* ================= LAPIS GERAK v2 ================= */
#veil{position:fixed;inset:0;z-index:9999;pointer-events:none;opacity:0;
  background:radial-gradient(circle at 50% 46%,var(--panel2),var(--bg) 68%);
  transition:opacity .3s var(--ease)}
#veil::after{content:"";position:absolute;left:50%;top:50%;width:42px;height:42px;margin:-21px;
  border:1px solid var(--gold);border-top-color:transparent;border-radius:50%;
  animation:sp .75s linear infinite;opacity:0;transition:opacity .2s}
body.leaving #veil{opacity:1}
body.leaving #veil::after{opacity:1}
main{transition:transform .32s var(--ease),opacity .32s}
body.leaving main{transform:scale(.986);opacity:.55}

.rip{position:absolute;border-radius:50%;pointer-events:none;z-index:2;
  transform:translate(-50%,-50%) scale(0);animation:rip .66s cubic-bezier(.2,.7,.3,1) forwards;
  background:radial-gradient(circle,var(--glow),transparent 68%)}
@keyframes rip{to{transform:translate(-50%,-50%) scale(1);opacity:0}}

.tr-dot{position:fixed;width:5px;height:5px;margin:-2.5px 0 0 -2.5px;border-radius:50%;
  z-index:6;pointer-events:none;background:var(--gold);opacity:.55;
  transition:transform .62s var(--ease),opacity .62s}
.tr-dot.go{transform:scale(.15) translateY(10px);opacity:0}

.rv{transition:opacity .85s var(--ease),transform .85s var(--ease),filter .85s var(--ease),clip-path .95s var(--ease)}
.rv:not(.on){filter:blur(5px)}
h1.rv:not(.on),h2.rv:not(.on){clip-path:inset(0 100% 0 0);filter:blur(8px)}
h1.rv.on,h2.rv.on{clip-path:inset(0 -2% 0 0)}

.cell,.room,.plan,.quote,.stat{transition:transform .5s var(--ease),background .35s,border-color .35s,box-shadow .5s}
.cell:hover,.plan:hover,.quote:hover{box-shadow:0 24px 48px -30px #000,0 0 0 1px var(--line)}
.plans .plan{position:relative;overflow:hidden}
.plans .plan::after{content:"";position:absolute;inset:0;pointer-events:none;opacity:0;transition:opacity .4s;
  background:radial-gradient(300px circle at var(--mx,50%) var(--my,50%),var(--line),transparent 72%)}
.plans .plan:hover::after{opacity:1}

.hr{position:relative;overflow:hidden}
.hr::after{content:"";position:absolute;top:0;left:-45%;width:45%;height:100%;
  background:linear-gradient(90deg,transparent,var(--gold2),transparent);
  animation:sweep 5s cubic-bezier(.5,0,.5,1) infinite}
@keyframes sweep{0%{left:-45%}60%,100%{left:108%}}
.kick::before{animation:kickw 4.2s ease-in-out infinite}
@keyframes kickw{50%{width:54px}}

.hero{position:relative;isolation:isolate}
.hero::before{content:"";position:absolute;inset:-14% -22% auto;height:126%;z-index:-1;
  pointer-events:none;opacity:.5;filter:blur(34px);
  background:conic-gradient(from 0deg at 32% 38%,transparent,var(--line),transparent 34%);
  animation:sp 22s linear infinite}
.hero h1,.pghead h1{transform:translate3d(0,calc(var(--sy,0) * .028px),0)}
.hero .lead{transform:translate3d(0,calc(var(--sy,0) * .014px),0)}

.cell:hover .ic{animation:flt 1.9s ease-in-out infinite}
@keyframes flt{50%{transform:translateY(-6px)}}

#prog{overflow:hidden}
#prog::after{content:"";position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.85),transparent);
  animation:sweep 2.2s linear infinite}

::selection{background:var(--gold);color:#0a0a0e}
::-webkit-scrollbar{width:9px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--line);border-radius:99px}
::-webkit-scrollbar-thumb:hover{background:var(--gold)}

@media(prefers-reduced-motion:reduce){
  .rip,.tr-dot,.hero::before,.hr::after,.kick::before,#prog::after,.cell:hover .ic{animation:none}
  .hero h1,.pghead h1,.hero .lead{transform:none}
  .rv:not(.on),h1.rv:not(.on),h2.rv:not(.on){filter:none;clip-path:none}
}
'''
EXTRA_CSS += r'''
/* ================= PUSAT SETELAN ================= */
#panel{width:min(400px,92vw);padding:0}
#panel .ph{position:sticky;top:0;z-index:3;display:flex;justify-content:space-between;
  align-items:center;padding:18px 20px 10px;
  background:linear-gradient(var(--panel),var(--panel) 72%,transparent)}
#panel .close{position:static}
#psearch{margin:0 20px 10px;width:calc(100% - 40px);padding:9px 11px;
  background:var(--panel2);border:1px solid var(--line2);color:var(--ink);
  font:inherit;font-size:11.5px;border-radius:var(--rad)}
.ptabs{display:flex;gap:6px;overflow-x:auto;padding:0 20px 14px;scrollbar-width:none}
.ptabs::-webkit-scrollbar{display:none}
.ptabs button{flex:0 0 auto;padding:6px 12px;font-size:10px;letter-spacing:.1em;
  border:1px solid var(--line2);background:none;color:var(--muted);cursor:pointer;
  border-radius:99px;text-transform:uppercase;transition:.2s}
.ptabs button:hover{color:var(--gold2)}
.ptabs button[aria-pressed="true"]{border-color:var(--gold);color:var(--gold2);background:var(--panel2)}
#pbody{padding:0 20px 34px}
.pgrp{display:none}
.pgrp.on{display:block}
.prow{margin-bottom:20px}
.prow>h3{margin:0 0 9px;font-size:9.5px;letter-spacing:.16em;color:var(--muted);
  text-transform:uppercase;font-weight:600}
.prow .seg{flex-wrap:wrap}
.prow .seg button{flex:1 1 auto;min-width:58px}
.range{width:100%;-webkit-appearance:none;appearance:none;height:3px;border-radius:9px;
  background:var(--line2);outline:none;margin:9px 0}
.range::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;
  background:var(--gold);cursor:pointer;box-shadow:0 0 0 4px var(--glow)}
.range::-moz-range-thumb{width:14px;height:14px;border:0;border-radius:50%;background:var(--gold)}
input[type=color]{width:100%;height:36px;border:1px solid var(--line);background:var(--panel2);
  cursor:pointer;padding:2px;border-radius:var(--rad)}
.pact{display:flex;gap:7px;flex-wrap:wrap}
.pact button{flex:1 1 auto;padding:9px 12px;font-size:10.5px;letter-spacing:.1em;
  border:1px solid var(--line);background:none;color:var(--muted);cursor:pointer;
  text-transform:uppercase;border-radius:var(--rad)}
.pact button:hover{color:var(--gold2);border-color:var(--gold)}

/* huruf */
html[data-font="playfair"] body{font-family:'Playfair Display',serif}
html[data-font="playfair"] .lead,html[data-font="playfair"] .btn{font-family:'Sora',sans-serif}
html[data-font="mono"] body{font-family:'JetBrains Mono',monospace}
html[data-font="mono"] h1,html[data-font="mono"] h2{font-family:'JetBrains Mono',monospace;letter-spacing:-.05em}
html[data-font="sistem"] body{font-family:system-ui,-apple-system,'Segoe UI',sans-serif}
html[data-head="serif"] h1,html[data-head="serif"] h2{font-family:'Playfair Display',serif}
html[data-head="mono"] h1,html[data-head="mono"] h2{font-family:'JetBrains Mono',monospace;
  letter-spacing:-.05em;font-weight:400}
html[data-head="kapital"] h1,html[data-head="kapital"] h2{text-transform:uppercase;
  letter-spacing:.06em;font-family:'Sora',sans-serif;font-weight:600}
html[data-head="renggang"] h1,html[data-head="renggang"] h2{letter-spacing:.14em}
html[data-lh="rapat"] body{line-height:1.42}
html[data-lh="renggang"] body{line-height:2}
html[data-ls="renggang"] body{letter-spacing:.02em}
html[data-ls="sangat"] body{letter-spacing:.06em}

/* tata letak */
html[data-wd="p"] .wrap{width:min(1680px,100% - 20px)}
html[data-rd="p"]{--rad:999px}
html[data-bw="0"] .cell,html[data-bw="0"] .plan,html[data-bw="0"] .room,
html[data-bw="0"] details,html[data-bw="0"] .cta,html[data-bw="0"] .m14-card{border-color:transparent}
html[data-bw="2"] .cell,html[data-bw="2"] .plan,html[data-bw="2"] .room,
html[data-bw="2"] details,html[data-bw="2"] .cta,html[data-bw="2"] .m14-card{border-width:2px}
html[data-tbl="belang"] .tbl tr:nth-child(even) td{background:var(--panel2)}
html[data-tbl="minimal"] .tbl{border:0}
html[data-tbl="minimal"] .tbl th{background:none}
html[data-btn="bulat"] .btn{border-radius:10px}
html[data-btn="pil"] .btn{border-radius:999px}
html[data-nav="sembunyi"] header{transition:transform .35s var(--ease),background .35s}
html[data-nav="sembunyi"] header.navhide{transform:translateY(-104%)}
html[data-nav="diam"] header{position:static}

/* efek */
html[data-pat="mesh"] body::after{content:"";position:fixed;inset:0;z-index:-2;pointer-events:none;opacity:.45;
  background-image:linear-gradient(var(--line2) 1px,transparent 1px),linear-gradient(90deg,var(--line2) 1px,transparent 1px);
  background-size:64px 64px;mask-image:radial-gradient(ellipse at 50% 20%,#000 10%,transparent 74%);
  -webkit-mask-image:radial-gradient(ellipse at 50% 20%,#000 10%,transparent 74%)}
html[data-pat="titik"] body::after{content:"";position:fixed;inset:0;z-index:-2;pointer-events:none;opacity:.5;
  background-image:radial-gradient(var(--line) 1px,transparent 1px);background-size:26px 26px}
html[data-pat="garis"] body::after{content:"";position:fixed;inset:0;z-index:-2;pointer-events:none;opacity:.3;
  background-image:repeating-linear-gradient(135deg,var(--line2) 0 1px,transparent 1px 14px)}
html[data-sh="off"] .cell,html[data-sh="off"] .plan,html[data-sh="off"] .room{box-shadow:none}
html[data-sh="tegas"] .cell,html[data-sh="tegas"] .plan,html[data-sh="tegas"] .room{
  box-shadow:0 26px 50px -26px #000,0 0 0 1px var(--line)}
html[data-blur="off"] header,html[data-blur="off"] #panel,html[data-blur="off"] #drawer,
html[data-blur="off"] #rpp{backdrop-filter:none}
html[data-cur="titik"] #cur{width:90px;height:90px}
html[data-cur="mati"] #cur{display:none}
html[data-par="mati"] .orb{transform:none!important}
html[data-par="kuat"] .orb{opacity:.55}
html[data-acc="nyala"] .btn:hover,html[data-acc="nyala"] .fab{box-shadow:0 0 26px var(--glow)}
html[data-acc="pudar"] .btn:hover,html[data-acc="pudar"] .fab{box-shadow:none}
html[data-focus="on"] .cell,html[data-focus="on"] .room,html[data-focus="on"] .plan,
html[data-focus="on"] .quote{opacity:.5;transition:opacity .3s}
html[data-focus="on"] .cell:hover,html[data-focus="on"] .room:hover,
html[data-focus="on"] .plan:hover,html[data-focus="on"] .quote:hover{opacity:1}
html[data-sel="emas"] ::selection{background:var(--gold);color:#0a0a0e}
html[data-sel="invers"] ::selection{background:var(--ink);color:var(--bg)}
html[data-link="garis"] main a:not(.btn):not(.iconbtn):not(.brand):not(.clink):not(.room){
  text-decoration:underline;text-underline-offset:3px}
'''
EXTRA_CSS += r'''
#cmdk{position:fixed;inset:0;z-index:120;display:none;background:rgba(4,4,7,.72);
  backdrop-filter:blur(9px);padding:14vh 16px 16px}
#cmdk.on{display:block}
#cmdk .box{max-width:560px;margin:0 auto;border:1px solid var(--gold);background:var(--panel);
  box-shadow:0 40px 90px -30px #000}
#cmdk input{width:100%;padding:15px 17px;background:none;border:0;border-bottom:1px solid var(--line2);
  color:var(--ink);font:inherit;font-size:14px;outline:none}
#cmdk .res{max-height:52vh;overflow:auto}
#cmdk a{display:flex;gap:11px;padding:11px 17px;font-size:12.6px;color:var(--muted);
  border-bottom:1px solid var(--line2)}
#cmdk a:hover,#cmdk a.sel{background:var(--panel2);color:var(--gold2)}
#cmdk a b{font-family:'JetBrains Mono',monospace;font-size:9.5px;color:var(--gold);min-width:34px}
#cmdk .ft{padding:9px 17px;font-family:'JetBrains Mono',monospace;font-size:9.5px;
  letter-spacing:.14em;color:var(--dim);display:flex;justify-content:space-between}
'''

HEADBOOT = r"""
(function(){var R=document.documentElement,L=localStorage;
 R.setAttribute('data-theme',L.getItem('alf.theme')||'emas');
 R.setAttribute('data-fs',L.getItem('alf.fs')||'m');
 R.setAttribute('data-motion',L.getItem('alf.motion')||'on');
 R.setAttribute('data-grain',L.getItem('alf.grain')||'on'); R.setAttribute('data-wide',L.getItem('alf.wide')||'n'); R.setAttribute('data-rad',L.getItem('alf.rad')||'k'); R.setAttribute('data-dense',L.getItem('alf.dense')||'n'); R.setAttribute('data-con',L.getItem('alf.con')||'n'); R.setAttribute('data-tr',L.getItem('alf.tr')||'s');R.setAttribute('data-pk',L.getItem('alf.pk')||'atelier');R.setAttribute('data-font',L.getItem('alf.font')||'sora');R.setAttribute('data-head',L.getItem('alf.head')||'normal');R.setAttribute('data-lh',L.getItem('alf.lh')||'n');R.setAttribute('data-ls',L.getItem('alf.ls')||'n');R.setAttribute('data-bw',L.getItem('alf.bw')||'1');R.setAttribute('data-tbl',L.getItem('alf.tbl')||'garis');R.setAttribute('data-btn',L.getItem('alf.btn')||'kotak');R.setAttribute('data-nav',L.getItem('alf.nav')||'menempel');R.setAttribute('data-pat',L.getItem('alf.pat')||'mati');R.setAttribute('data-sh',L.getItem('alf.sh')||'lembut');R.setAttribute('data-blur',L.getItem('alf.blur')||'nyala');R.setAttribute('data-cur',L.getItem('alf.cur')||'cincin');R.setAttribute('data-par',L.getItem('alf.par')||'lembut');R.setAttribute('data-acc',L.getItem('alf.acc')||'bawaan');R.setAttribute('data-sel',L.getItem('alf.sel')||'bawaan');R.setAttribute('data-link',L.getItem('alf.link')||'biasa');R.setAttribute('data-focus',L.getItem('alf.focus')||'mati');var _cc=L.getItem('alf.custom');if(_cc){R.style.setProperty('--gold',_cc);R.style.setProperty('--gold2',_cc);R.style.setProperty('--glow','color-mix(in srgb,'+_cc+' 40%, transparent)');R.style.setProperty('--line','color-mix(in srgb,'+_cc+' 18%, transparent)');}})();
"""

ROOMS = [
    ("/","01","Beranda","Ikhtisar atelier dan pintu masuk seluruh ruang."),
    ("/layanan","02","Layanan","Tujuh disiplin kerja yang ditangani."),
    ("/harga","03","Harga","Paket web dan mobile dengan tarif terbuka."),
    ("/portofolio","04","Portofolio","Enam studi kasus beserta hasil terukurnya."),
    ("/proses","05","Proses","Alur kerja empat tahap yang bisa dipantau."),
    ("/stack","06","Stack","Perangkat, bahasa, dan tingkat penguasaan."),
    ("/keamanan","07","Keamanan","Kerentanan yang ditangani dan cara pengerasan."),
    ("/sla","08","Ketentuan","Garansi, revisi, pembayaran, dan kepemilikan."),
    ("/faq","09","Tanya","Keberatan yang paling sering muncul."),
    ("/kontak","10","Kontak","Kanal resmi dan formulir brief."),
    ("/mulai","11","Mulai","Tiga langkah membuka proyek tanpa bingung."),
    ("/matriks","12","Matriks","Perbandingan isi paket baris demi baris."),
    ("/web","13","Teknologi Web","Tumpukan kerja sisi web dan batasannya."),
    ("/mobile","14","Teknologi Mobile","Tumpukan kerja Android dan iOS."),
    ("/integrasi","15","Integrasi","Layanan pihak ketiga yang biasa disambungkan."),
    ("/hosting","16","Infrastruktur","Server, TLS, dan topologi penyebaran."),
    ("/maintenance","17","Perawatan","Paket rawat bulanan dan cakupannya."),
    ("/garansi","18","Garansi","Apa yang ditanggung dan apa yang tidak."),
    ("/legal","19","Legal","Dokumen kerja dan status badan usaha."),
    ("/privasi","20","Privasi","Data yang dikumpulkan situs ini."),
    ("/syarat","21","Syarat","Ketentuan pemakaian layanan."),
    ("/catatan","22","Catatan","Tulisan pendek soal praktik kerja."),
    ("/glosarium","23","Glosarium","Istilah teknis yang sering membingungkan."),
    ("/checklist","24","Checklist","Daftar periksa sebelum peluncuran."),
    ("/roadmap","25","Roadmap Celah","Jadwal penambalan celah per minggu."),
    ("/kapasitas","26","Kapasitas","Berapa proyek berjalan bersamaan."),
    ("/mitra","27","Mitra","Kolaborasi dan rujukan silang."),
    ("/kolaborasi","28","Kolaborasi","Peluang kerja sama jangka panjang."),
    ("/status","29","Status","Kondisi node dan riwayat kejadian."),
    ("/dokumentasi","30","Dokumentasi","Struktur berkas dan rute aplikasi."),
    ("/struktur","31","Struktur","Alur permintaan dan lapisan pengaman."),
    ("/reaper","32","REAPER","Asisten lokal, tanpa token."),
    ("/admin","33","Admin","Catatan kerja dan kendali node."),
]

import rooms80 as _r80
import rooms80b as _r80b
_EXT = _r80.DATA + _r80b.DATA
_EXT.sort(key=lambda x: int(x[1]))
for _s, _n, _t, _d, _rows in _EXT:
    ROOMS.append((_s, _n, _t, _d))
ROOMS.append(("/cari", "115", "Cari", "Pencarian cepat antar ruang."))
import lab116 as _l116, lab117 as _l117, lab118 as _l118, lab119 as _l119, lab120 as _l120
for _m in (_l116, _l117, _l118, _l119, _l120):
    ROOMS.append(_m.META)


PRIMARY = ["/","/layanan","/harga","/keamanan","/roadmap","/kontak"]

def nav(active):
    nl = "".join('<a href="%s"%s>%s</a>' % (u, ' class="on"' if u == active else "", t)
                 for u, _n, t, _d in ROOMS if u in PRIMARY)
    dr = "".join('<a href="%s"><span>%s</span>%s</a>' % (u, n, t) for u, n, t, _d in ROOMS)
    return """
<header id="hdr"><div class="wrap nav">
  <a href="/" class="brand"><b>A</b>ALFILIATOR</a>
  <nav class="nl">__NL__</nav>
  <div class="navtools">
    <a href="__WA__?text=Halo" class="btn ncta" target="_blank" rel="noopener">Konsultasi</a>
    <button class="iconbtn" id="popener" aria-label="Setelan tampilan"><i class="fas fa-sliders"></i></button>
    <button class="iconbtn burger" id="burger" aria-label="Menu"><i class="fas fa-bars"></i></button>
  </div>
</div></header>
<div id="drawer"><div class="dhead">114 Ruang</div>__DR__</div>

<aside id="panel" aria-label="Setelan tampilan">
  <div class="ph"><div class="kick">Setelan</div>
    <button class="iconbtn close" id="pclose" aria-label="Tutup"><i class="fas fa-xmark"></i></button></div>
  <input id="psearch" class="inp" type="search" placeholder="Cari setelan…" autocomplete="off">
  <div class="ptabs">
    <button data-tab="warna" aria-pressed="true">Warna</button>
    <button data-tab="huruf" aria-pressed="false">Huruf</button>
    <button data-tab="tata" aria-pressed="false">Tata</button>
    <button data-tab="efek" aria-pressed="false">Efek</button>
    <button data-tab="suara" aria-pressed="false">Suara</button>
    <button data-tab="bahasa" aria-pressed="false">Bahasa</button>
    <button data-tab="data" aria-pressed="false">Data</button>
  </div>
  <div id="pbody">
    <section class="pgrp on" data-g="warna">
      <div class="prow"><h3>Paket desain</h3><div class="seg"><button data-pk="atelier" aria-pressed="true">Atelier</button><button data-pk="editorial">Editorial</button><button data-pk="terminal">Terminal</button><button data-pk="lembut">Lembut</button><button data-pk="tegas">Tegas</button></div></div>
      <div class="prow"><h3>Warna aksen</h3><div class="sw"><button data-t="emas" style="background:#d4af7a" aria-label="emas"></button><button data-t="sian" style="background:#38d6e8" aria-label="sian"></button><button data-t="violet" style="background:#a48bff" aria-label="violet"></button><button data-t="zamrud" style="background:#3fdb9a" aria-label="zamrud"></button><button data-t="rose" style="background:#f0799c" aria-label="rose"></button><button data-t="mono" style="background:#cfcfcf" aria-label="mono"></button><button data-t="indigo" style="background:#7d8cff" aria-label="indigo"></button><button data-t="toska" style="background:#3fd6c4" aria-label="toska"></button><button data-t="kuning" style="background:#f0c04a" aria-label="kuning"></button><button data-t="merah" style="background:#f0685f" aria-label="merah"></button><button data-t="langit" style="background:#5cb8f5" aria-label="langit"></button><button data-t="limau" style="background:#a8e05a" aria-label="limau"></button><button data-t="magenta" style="background:#ef6ad4" aria-label="magenta"></button><button data-t="baja" style="background:#9fb0c4" aria-label="baja"></button><button data-t="kertas" style="background:#f6f3ec" aria-label="kertas"></button><button data-t="kapur" style="background:#eaf1f5" aria-label="kapur"></button><button data-t="senja" style="background:#ff8a4c" aria-label="senja"></button><button data-t="anggur" style="background:#b4527a" aria-label="anggur"></button></div></div>
      <div class="prow"><h3>Warna sendiri</h3><input type="color" id="pcust" value="#d4af7a" aria-label="Warna sendiri"></div>
      <div class="prow"><h3>Intensitas aksen</h3><div class="seg"><button data-acc="bawaan" aria-pressed="true">Bawaan</button><button data-acc="nyala">Nyala</button><button data-acc="pudar">Pudar</button></div></div>
      <div class="prow"><h3>Warna seleksi</h3><div class="seg"><button data-sel="bawaan" aria-pressed="true">Bawaan</button><button data-sel="emas">Emas</button><button data-sel="invers">Invers</button></div></div>
      <div class="prow"><h3>Kontras</h3><div class="seg"><button data-cn="n" aria-pressed="true">Normal</button><button data-cn="t">Tinggi</button></div></div>
      <div class="prow"><h3>Transparansi panel</h3><div class="seg"><button data-tr="s" aria-pressed="true">Solid</button><button data-tr="t">Tipis</button></div></div>
    </section>
    <section class="pgrp" data-g="huruf">
      <div class="prow"><h3>Pasangan huruf</h3><div class="seg"><button data-font="sora" aria-pressed="true">Sora</button><button data-font="playfair">Serif</button><button data-font="mono">Mono</button><button data-font="sistem">Sistem</button></div></div>
      <div class="prow"><h3>Gaya judul</h3><div class="seg"><button data-head="normal" aria-pressed="true">Normal</button><button data-head="serif">Serif</button><button data-head="mono">Mono</button><button data-head="kapital">Kapital</button><button data-head="renggang">Renggang</button></div></div>
      <div class="prow"><h3>Ukuran huruf</h3><div class="seg"><button data-fs="s">Kecil</button><button data-fs="m" aria-pressed="true">Normal</button><button data-fs="l">Besar</button></div></div>
      <div class="prow"><h3>Tinggi baris</h3><div class="seg"><button data-lh="rapat">Rapat</button><button data-lh="n" aria-pressed="true">Normal</button><button data-lh="renggang">Renggang</button></div></div>
      <div class="prow"><h3>Jarak huruf</h3><div class="seg"><button data-ls="n" aria-pressed="true">Normal</button><button data-ls="renggang">Renggang</button><button data-ls="sangat">Sangat</button></div></div>
    </section>
    <section class="pgrp" data-g="tata">
      <div class="prow"><h3>Lebar konten</h3><div class="seg"><button data-wd="s">Sempit</button><button data-wd="n" aria-pressed="true">Normal</button><button data-wd="l">Lebar</button><button data-wd="p">Penuh</button></div></div>
      <div class="prow"><h3>Kerapatan</h3><div class="seg"><button data-dn="l">Renggang</button><button data-dn="n" aria-pressed="true">Normal</button><button data-dn="r">Rapat</button></div></div>
      <div class="prow"><h3>Sudut</h3><div class="seg"><button data-rd="k" aria-pressed="true">Kotak</button><button data-rd="n">Normal</button><button data-rd="b">Bulat</button><button data-rd="p">Pil</button></div></div>
      <div class="prow"><h3>Tebal garis</h3><div class="seg"><button data-bw="0">Tanpa</button><button data-bw="1" aria-pressed="true">Normal</button><button data-bw="2">Tebal</button></div></div>
      <div class="prow"><h3>Gaya tabel</h3><div class="seg"><button data-tbl="garis" aria-pressed="true">Garis</button><button data-tbl="belang">Belang</button><button data-tbl="minimal">Minimal</button></div></div>
      <div class="prow"><h3>Bentuk tombol</h3><div class="seg"><button data-btn="kotak" aria-pressed="true">Kotak</button><button data-btn="bulat">Bulat</button><button data-btn="pil">Pil</button></div></div>
      <div class="prow"><h3>Navigasi</h3><div class="seg"><button data-nav="menempel" aria-pressed="true">Menempel</button><button data-nav="sembunyi">Sembunyi</button><button data-nav="diam">Diam</button></div></div>
      <div class="prow"><h3>Garis bantu</h3><div class="seg"><button data-gd="off" aria-pressed="true">Mati</button><button data-gd="on">Aktif</button></div></div>
    </section>
    <section class="pgrp" data-g="efek">
      <div class="prow"><h3>Animasi</h3><div class="seg"><button data-mt="on" aria-pressed="true">Aktif</button><button data-mt="off">Mati</button></div></div>
      <div class="prow"><h3>Kekuatan parallax</h3><div class="seg"><button data-par="mati">Mati</button><button data-par="lembut" aria-pressed="true">Lembut</button><button data-par="kuat">Kuat</button></div></div>
      <div class="prow"><h3>Pola latar</h3><div class="seg"><button data-pat="mati" aria-pressed="true">Mati</button><button data-pat="mesh">Mesh</button><button data-pat="titik">Titik</button><button data-pat="garis">Garis</button></div></div>
      <div class="prow"><h3>Tekstur butir</h3><div class="seg"><button data-gr="on" aria-pressed="true">Aktif</button><button data-gr="off">Mati</button></div></div>
      <div class="prow"><h3>Bayangan</h3><div class="seg"><button data-sh="off">Mati</button><button data-sh="lembut" aria-pressed="true">Lembut</button><button data-sh="tegas">Tegas</button></div></div>
      <div class="prow"><h3>Buram kaca</h3><div class="seg"><button data-blur="nyala" aria-pressed="true">Aktif</button><button data-blur="off">Mati</button></div></div>
      <div class="prow"><h3>Kursor</h3><div class="seg"><button data-cur="cincin" aria-pressed="true">Cincin</button><button data-cur="titik">Titik</button><button data-cur="mati">Mati</button></div></div>
      <div class="prow"><h3>Mode fokus</h3><div class="seg"><button data-focus="mati" aria-pressed="true">Mati</button><button data-focus="on">Aktif</button></div></div>
      <div class="prow"><h3>Gaya tautan</h3><div class="seg"><button data-link="biasa" aria-pressed="true">Biasa</button><button data-link="garis">Garis bawah</button></div></div>
    </section>
    <section class="pgrp" data-g="suara">
      <div class="prow"><h3>Bunyi antarmuka</h3><div class="seg"><button data-sd="on" aria-pressed="true">Aktif</button><button data-sd="off">Mati</button></div></div>
      <div class="prow"><h3>Volume</h3><input id="pvol" class="range" type="range" min="0" max="100" step="5" value="45" aria-label="Volume bunyi"></div>
      <div class="prow"><h3>Nada</h3><div class="seg"><button data-pk2="lembut" aria-pressed="true">Lembut</button><button data-pk2="tajam">Tajam</button><button data-pk2="rendah">Rendah</button></div></div>
    </section>
    <section class="pgrp" data-g="bahasa">
      <div class="prow"><h3>Bahasa</h3><div class="seg"><select id="lang" class="sel"></select></div>
        <div class="seg"><button id="langauto">Otomatis</button></div></div>
      <div class="prow"><h3>Mata uang</h3><div class="seg"><select id="cur" class="sel"></select></div>
        <div class="seg"><button id="curauto">Otomatis</button></div></div>
      <div class="prow"><h3>Kurs 1 USD (Rp)</h3><div class="seg"><input id="rate" class="inp" type="number" min="1" step="1" value="16300"></div></div>
    </section>
    <section class="pgrp" data-g="data">
      <div class="prow"><h3>Ekspor &amp; impor</h3><div class="pact">
        <button id="pexp">Ekspor</button><button id="pimp">Impor</button><button id="pcopy">Salin tautan</button></div>
        <input id="pfile" type="file" accept="application/json" hidden></div>
      <div class="prow"><h3>Setel ulang per kelompok</h3><div class="pact">
        <button data-rg="warna">Warna</button><button data-rg="huruf">Huruf</button><button data-rg="tata">Tata</button>
        <button data-rg="efek">Efek</button><button data-rg="suara">Suara</button></div></div>
      <div class="prow"><h3>Semua</h3><div class="pact"><button id="preset">Setel ulang semua</button></div></div>
      <p class="note">Pilihan disimpan di perangkat ini saja. Tautan setelan memuat pilihanmu di perangkat lain.</p>
    </section>
  </div>
</aside>""".replace("__NL__", nl).replace("__DR__", dr).replace("__WA__", WA)

def shell(active, title, desc, body):
    return """<!DOCTYPE html>
<html lang="id" data-theme="emas" data-fs="m" data-motion="on" data-grain="on"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#07070a">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/icon.svg">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="canonical" href="__CAN__">
<meta property="og:image" content="/icon.svg">
<meta name="twitter:card" content="summary_large_image">
<title>__T__ — ALFILIATOR</title>
<meta name="description" content="__D__">
<meta property="og:title" content="__T__ — ALFILIATOR">
<meta property="og:description" content="__D__">
<meta property="og:type" content="website">
<script nonce="__NONCE__">__HB__</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Sora:wght@300;400;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>__CSS__</style><style>__CSS2__</style>
</head><body>
<a class="skip" href="#main">Lompat ke isi</a>
<div id="prog"></div><div id="cur"></div><div id="scan"></div>
<div class="bgfx"><div class="orb o1" data-px=".10"></div><div class="orb o2" data-px="-.13"></div><div class="orb o3" data-px=".07"></div><div class="mesh"></div></div>
<div class="grain"></div>
__NAV__
<main id="main">__BODY__</main>
<footer><div class="wrap fg">
  <div>&copy; 2026 ALFILIATOR — Atelier Digital</div>
  <div class="mono">NODE v6 · 114 RUANG</div>
</div></footer>
<a class="fab" href="__WA__?text=Halo%20ALFILIATOR" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
<button id="top" aria-label="Atas"><i class="fas fa-arrow-up"></i></button>
<script nonce="__NONCE__">__JS__</script>




<!--alf:reg-->

<!--/alf:reg-->


<div id="rpp" aria-label="REAPER">
  <div id="rph"><span>REAPER <em>· nol token</em></span><span id="rpx">✕</span></div>
  <div class="rmode"><select id="rmode"><option value="lokal">Lokal — gratis</option><option value="venice">Venice — kunci API</option></select></div>
  <div class="rmode" id="rven" hidden>
    <input id="rkey" type="password" placeholder="Kunci API Venice">
    <select id="rmod">
      <option value="deepseek-v4-1-flash">DeepSeek V4.1 Flash</option>
      <option value="venice-uncensored-1-2">Venice Uncensored</option>
      <option value="llama-3.3-70b">Llama 3.3 70B</option>
      <option value="gemini-3-5-flash">Gemini 3.5 Flash</option>
      <option value="qwen-3-8-flash">Qwen 3.8 Flash</option>
    </select>
  </div>
  <div id="rpb"></div>
  <div class="chips" id="rch"></div>
  <div id="rpf"><input id="rpi" placeholder="Tulis pertanyaan…" autocomplete="off"><button id="rps" aria-label="Kirim">→</button></div>
</div>
<button id="rp" aria-label="Buka REAPER"><b>R</b>REAPER</button>
<script nonce="__NONCE__">
(function(){
  var P=document.getElementById('rpp'),O=document.getElementById('rp'),X=document.getElementById('rpx'),
      Bx=document.getElementById('rpb'),I=document.getElementById('rpi'),S=document.getElementById('rps'),
      CH=document.getElementById('rch'),MD=document.getElementById('rmode'),VW=document.getElementById('rven'),
      KY=document.getElementById('rkey'),MO=document.getElementById('rmod');
  var WA='__WA__', hist=[];
  var SYN={brp:'berapa',hrg:'harga',hargai:'harga',duit:'harga',biaya:'harga',budget:'harga',
    murah:'harga',lama:'durasi',cepat:'durasi',wa:'whatsapp',tlp:'kontak',jmin:'jaminan',
    gmn:'bagaimana',gimana:'bagaimana',bs:'bisa',tdk:'tidak',gak:'tidak',ga:'tidak',klo:'kalau'};
  var PR={landing:1750000,bisnis:6500000,toko:8500000,sistem:24000000,android:15000000,
    ios:26000000,bot:3500000,audit:5000000,payment:2750000,desain:3250000,pelatihan:1250000,rawat:750000};
  var LB={landing:'Landing page',bisnis:'Company profile',toko:'Toko online',sistem:'Sistem custom',
    android:'Aplikasi Android',ios:'Aplikasi iOS',bot:'Bot automation',audit:'Audit keamanan',
    payment:'Payment gateway',desain:'Desain UI/UX',pelatihan:'Pelatihan admin',rawat:'Perawatan 1 bulan'};
  var KB=[
    {k:['harga','tarif','paket'],a:'Tarif terbuka: landing Rp 1.750.000, bisnis Rp 6.500.000, sistem mulai Rp 24.000.000. <a href="/harga">Halaman harga</a>.'},
    {k:['android','apk','play'],a:'Android mulai Rp 15.000.000, 25–32 hari. <a href="/mobile">Detail</a>.'},
    {k:['ios','iphone','apple'],a:'iOS mulai Rp 26.000.000 karena biaya Apple Developer dan review ketat. <a href="/mobile">Penjelasan</a>.'},
    {k:['garansi','rusak','bug'],a:'Garansi 30 hari web dasar, 60 hari Enterprise, 45 hari cross-platform, hanya untuk bug. <a href="/garansi">Rincian</a>.'},
    {k:['dp','bayar','pembayaran'],a:'50 persen tanda jadi, 50 persen sebelum serah terima. <a href="/sla">Ketentuan</a>.'},
    {k:['revisi'],a:'Revisi: Starter 1x, Bisnis 2x, mobile sesuai kontrak. <a href="/sla">Baca</a>.'},
    {k:['source','kode','kepemilikan'],a:'Source code dan kredensial diserahkan penuh setelah pelunasan.'},
    {k:['nda','rahasia'],a:'NDA tersedia sebelum brief. Kirim draf atau saya siapkan versi sederhana.'},
    {k:['keamanan','audit','celah'],a:'Audit Rp 5.000.000, 3–5 hari, laporan bertingkat. <a href="/keamanan">Cakupan</a>.'},
    {k:['durasi','waktu'],a:'Landing 5–7 hari, bisnis 14–20 hari, mobile 25–60 hari.'},
    {k:['kontak','whatsapp','telegram'],a:'<a href="/kontak">Kanal resmi</a> atau <a href="'+WA+'?text=Halo" target="_blank" rel="noopener">WhatsApp</a>.'},
    {k:['bot','otomasi'],a:'Bot WhatsApp atau Telegram Rp 3.500.000. <a href="/integrasi">Integrasi</a>.'},
    {k:['perawatan','rawat','maintenance'],a:'Perawatan mulai Rp 750.000 per bulan. <a href="/maintenance">Detail</a>.'},
    {k:['token','gratis','reaper'],a:'Mode lokal tanpa API dan tanpa batas. Mode Venice memakai kunci Anda sendiri.'},
    {k:['struktur','alur'],a:'Alur permintaan melewati tujuh gerbang. <a href="/struktur">Diagram</a>.'},
    {k:['toko','online','jualan'],a:'Toko online Rp 8.500.000: katalog, keranjang, checkout, payment gateway.'},
    {k:['desain','ui','ux','figma'],a:'Desain UI/UX di Figma Rp 3.250.000, dikerjakan sebelum kode.'},
    {k:['portofolio','contoh','hasil'],a:'Enam studi kasus dengan metrik. <a href="/portofolio">Portofolio</a>.'},
    {k:['proses','tahap'],a:'Empat tahap: brief, desain, development, peluncuran. <a href="/proses">Detail</a>.'},
    {k:['lokasi','remote','domisili'],a:'Pengerjaan remote, komunikasi tertulis, preview bisa dipantau.'}
  ];
  function nrm(t){ return t.toLowerCase().replace(/[^a-z0-9 ]/g,' ').replace(/ +/g,' ').trim()
    .split(' ').map(function(w){ return SYN[w]||w; }).join(' '); }
  function lev(a,b){ if(Math.abs(a.length-b.length)>2) return 9;
    var m=[],i,j; for(i=0;i<=b.length;i++) m[i]=[i];
    for(j=0;j<=a.length;j++) m[0][j]=j;
    for(i=1;i<=b.length;i++) for(j=1;j<=a.length;j++)
      m[i][j]=Math.min(m[i-1][j]+1,m[i][j-1]+1,m[i-1][j-1]+(a[j-1]===b[i-1]?0:1));
    return m[b.length][a.length]; }
  function skor(q,e){ var ws=q.split(' '), sc=0;
    e.k.forEach(function(k){ if(q.indexOf(k)>-1) sc+=4;
      else ws.forEach(function(w){ if(w.length>3&&w.indexOf(k)===0) sc+=2;
        else if(lev(w,k)<=1) sc+=1.5; }); });
    return sc; }
  function uang(v){ var r=+(localStorage.getItem('alf.rate')||16300), c=localStorage.getItem('alf.cur')||'IDR';
    var x = c==='IDR' ? v : (c==='USD' ? v/r : (c==='EUR' ? v/r/1.08 : v/r*1.35));
    if(c==='IDR') return 'Rp '+Math.round(x).toLocaleString('id-ID');
    return (c==='USD'?'$':c==='EUR'?'€':'S$')+Math.round(x).toLocaleString('en-US'); }
  function hitung(q){ var pil=[]; Object.keys(PR).forEach(function(k){ if(q.indexOf(k)>-1) pil.push(k); });
    if(pil.length<2) return null;
    var tot=0, bar=pil.map(function(k){ tot+=PR[k]; return LB[k]+' — '+uang(PR[k]); });
    return bar.join('<br>')+'<br><b>Total '+uang(tot)+'</b><br><a href="'+WA+'?text='+encodeURIComponent('Halo, estimasi saya: '+pil.map(function(k){return LB[k]}).join(', '))+'" target="_blank" rel="noopener">Kirim sebagai brief</a>'; }
  function lokal(q){
    var h=hitung(q); if(h) return h;
    var best=null,bs=0; KB.forEach(function(e){ var v=skor(q,e); if(v>bs){bs=v;best=e} });
    if(best&&bs>=4) return best.a;
    var d=KB.slice().sort(function(a,b){return skor(q,b)-skor(q,a)}).slice(0,3)
      .filter(function(e){return skor(q,e)>0}).map(function(e){return e.k[0]});
    return 'Belum ada di basis lokal.'+(d.length?' Mungkin maksud Anda: <b>'+d.join(', ')+'</b>.':'')
      +' Atau <a href="'+WA+'?text='+encodeURIComponent(q)+'" target="_blank" rel="noopener">tanya langsung</a>.';
  }
  function api(q){
    var k=localStorage.getItem('alf.vkey')||'';
    if(!k) return Promise.reject(new Error('nokey'));
    var m=[{role:'system',content:'Anda REAPER, asisten situs ALFILIATOR (jasa web, Android, iOS, sistem custom, bot, audit keamanan). Jawab singkat dalam Bahasa Indonesia, maksimal 90 kata. Harga: landing 1.750.000, bisnis 6.500.000, toko 8.500.000, android 15.000.000, iOS 26.000.000, sistem 24.000.000, bot 3.500.000, audit 5.000.000. Arahkan ke WhatsApp untuk penawaran.'}];
    hist.slice(-6).forEach(function(x){ m.push(x) });
    m.push({role:'user',content:q});
    return fetch('https://api.venice.ai/api/v1/chat/completions',{method:'POST',
      headers:{'Content-Type':'application/json','Authorization':'Bearer '+k},
      body:JSON.stringify({model:MO.value,messages:m,max_completion_tokens:320,temperature:0.4})})
      .then(function(r){ if(!r.ok) throw new Error('HTTP '+r.status); return r.json(); })
      .then(function(d){ return d.choices[0].message.content.replace(/</g,'&lt;'); });
  }
  function add(t,me){ var d=document.createElement('div'); d.className='rpm'+(me?' me':''); d.innerHTML=t;
    Bx.appendChild(d); Bx.scrollTop=Bx.scrollHeight; return d; }
  function chips(a){ CH.innerHTML=''; a.forEach(function(t){
    var b=document.createElement('button'); b.className='chip'; b.type='button'; b.textContent=t;
    b.onclick=function(){ I.value=t; kirim(); }; CH.appendChild(b); }); }
  function kirim(){
    var q=I.value.trim(); if(!q) return;
    add(q.replace(/</g,'&lt;'),1); I.value=''; chips([]);
    if(MD.value==='venice'){
      var th=add('<span class="rthink">menghubungi api.venice.ai…</span>');
      api(q).then(function(t){ th.remove(); add(t); hist.push({role:'user',content:q}); hist.push({role:'assistant',content:t}); })
        .catch(function(e){ th.remove();
          var msg = e.message==='nokey' ? 'Kunci API belum diisi. Buka mode Venice lalu tempel kunci.' :
            e.message==='HTTP 401' ? 'Kunci ditolak (401). Periksa kembali.' :
            e.message==='HTTP 402' ? 'Saldo kredit Venice habis (402).' :
            e.message==='HTTP 403' ? 'Kunci dibatasi IP (403). Kosongkan daftar IP di dasbor Venice.' :
            'Gagal menghubungi API ('+e.message+').';
          add(msg+' <b>Jawaban lokal:</b><br>'+lokal(nrm(q)));
        });
      return;
    }
    setTimeout(function(){ add(lokal(nrm(q))); chips(['harga toko online','garansi','aplikasi iOS','audit keamanan']); }, 280);
  }
  S.onclick=kirim;
  I.addEventListener('keydown',function(e){ if(e.key==='Enter') kirim(); });
  O.onclick=function(){ P.classList.toggle('open'); if(P.classList.contains('open')) I.focus(); };
  X.onclick=function(){ P.classList.remove('open'); };
  var op=document.getElementById('rpop'); if(op) op.onclick=function(e){ e.preventDefault(); P.classList.add('open'); I.focus(); };
  MD.value=localStorage.getItem('alf.rmode')||'lokal';
  MD.onchange=function(){ VW.hidden = MD.value!=='venice'; localStorage.setItem('alf.rmode',MD.value); };
  VW.hidden = MD.value!=='venice';
  KY.value=localStorage.getItem('alf.vkey')||'';
  KY.onchange=function(){ localStorage.setItem('alf.vkey',KY.value.trim()); };
  MO.value=localStorage.getItem('alf.rmodel')||'deepseek-v4-1-flash';
  MO.onchange=function(){ localStorage.setItem('alf.rmodel',MO.value); };
  add('Halo. Saya REAPER. Mode lokal aktif, tanpa token.');
  chips(['harga toko online','garansi','aplikasi iOS','audit keamanan']);
})();
</script>
</body></html>""".replace("__T__", html.escape(title)).replace("__D__", html.escape(desc)) \
   .replace("__HB__", HEADBOOT).replace("__CSS__", CSS).replace("__NAV__", nav(active)) \
   .replace("__BODY__", body).replace("__WA__", WA).replace("__CSS2__", EXTRA_CSS).replace("__CAN__", BASE + active).replace("__JS__", JS)

def page(active, title, desc, body):
    return shell(active, title, desc, body)

# ============================================================ halaman
B = {}

for _m in (_l116, _l117, _l118, _l119, _l120):
    B[_m.META[0]] = _m.BODY
import lab121 as _l121
ROOMS.append(_l121.META)
B[_l121.META[0]] = _l121.BODY
B["/"] = """
<div class="wrap hero">
  <div class="kick">Atelier Digital · Est. 2021</div>
  <h1>Perangkat lunak yang dibuat <em>seperti benda mahal</em>.</h1>
  <p class="lead">Web, Android, iOS, sistem internal, dan bot automation. Dikerjakan dengan disiplin atelier: brief tertulis, timeline jujur, source code diserahkan, dan keamanan dihitung sejak baris pertama.</p>
  <div class="hact"><a href="/kontak" class="btn solid">Kirim Brief</a><a href="/harga" class="btn ghost">Lihat Tarif</a></div>
  <div class="tags">
    <span><i class="fas fa-check"></i> Garansi bug 30 hari</span>
    <span><i class="fas fa-check"></i> Source code milik Anda</span>
    <span><i class="fas fa-check"></i> NDA tersedia</span>
    <span><i class="fas fa-check"></i> Timeline tertulis</span>
  </div>
  <div class="stats">
    <div class="stat"><b data-c="128" data-s="+">128+</b><span>Proyek Selesai</span></div>
    <div class="stat"><b data-c="96" data-s="%">0</b><span>Klien Kembali</span></div>
    <div class="stat"><b data-c="99" data-s=".9%">0</b><span>Uptime</span></div>
    <div class="stat"><b data-c="2" data-p="&lt;" data-s=" jam">0</b><span>Respon</span></div>
  </div>
</div>
<section><div class="wrap">
  <div class="kick rv">Tiga Puluh Empat Ruang</div>
  <h2 class="rv">Jelajahi seluruh atelier</h2><div class="hr rv"></div>
  <div class="rooms rv">__ROOMS__</div>
</div></section>
<section><div class="wrap">
  <div class="kick rv">Mengapa</div>
  <h2 class="rv">Tiga hal yang jarang ditemukan</h2><div class="hr rv"></div>
  <div class="grid rv">
    <div class="cell"><div class="ic"><i class="fas fa-file-signature"></i></div><h3>Brief tertulis</h3><p>Lingkup kerja, tanggal, dan batas revisi dikunci di awal. Tidak ada "nanti ditambah".</p></div>
    <div class="cell"><div class="ic"><i class="fas fa-shield-halved"></i></div><h3>Keamanan sejak awal</h3><p>Validasi input, header, dan pembatasan akses masuk ke spesifikasi — bukan tambahan belakangan.</p></div>
    <div class="cell"><div class="ic"><i class="fas fa-key"></i></div><h3>Tanpa penguncian</h3><p>Source code dan kredensial diserahkan penuh setelah pelunasan.</p></div>
  </div>
</div></section>
<section><div class="wrap"><div class="cta rv">
  <div class="kick" style="justify-content:center">Mulai</div>
  <h2>Ceritakan proyek Anda</h2>
  <p>Konsultasi awal tanpa biaya. Balasan berisi estimasi biaya, durasi, dan cakupan yang bisa langsung Anda nilai.</p>
  <div class="row"><a href="__WA__?text=Halo" class="btn solid" target="_blank" rel="noopener">WhatsApp</a><a href="/kontak" class="btn ghost">Formulir</a></div>
</div></div></section>
""".replace("__ROOMS__", "".join(
    '<a class="room" href="%s"><span class="no">%s</span><span class="ar"><i class="fas fa-arrow-up-right-from-square"></i></span><h3>%s</h3><p>%s</p></a>' % (u, n, t, d)
    for u, n, t, d in ROOMS))

B["/layanan"] = """
<div class="wrap pghead"><div class="kick">02 · Layanan</div>
<h1>Tujuh disiplin <em>yang ditangani</em>.</h1>
<p class="lead">Setiap pekerjaan punya batas cakupan tertulis. Harga di bawah adalah titik mulai; spesifikasi akhir menyesuaikan kompleksitas.</p></div>
<section><div class="wrap"><div class="grid">
  <div class="cell rv"><div class="ic"><i class="fas fa-window-maximize"></i></div><h3>Landing Page</h3><p>Halaman promosi fokus untuk iklan berbayar dan closing cepat.</p><span class="from">mulai Rp 1.750.000</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-building"></i></div><h3>Company Profile</h3><p>Profil bisnis profesional, katalog layanan, formulir lead.</p><span class="from">mulai Rp 4.500.000</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-cart-shopping"></i></div><h3>Toko Online</h3><p>Katalog, keranjang, checkout, integrasi payment gateway.</p><span class="from">mulai Rp 8.500.000</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-diagram-project"></i></div><h3>Sistem Custom</h3><p>Dashboard, multi-peran, laporan, dan API internal.</p><span class="from">mulai Rp 24.000.000</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-mobile-screen-button"></i></div><h3>Aplikasi Mobile</h3><p>Android dan iOS, native maupun cross-platform.</p><span class="from">mulai Rp 15.000.000</span></div>
  <div class="cell rv"><div class="ic"><i class="fab fa-telegram"></i></div><h3>Bot &amp; Automation</h3><p>WhatsApp/Telegram, auto-reply, notifikasi, sinkronisasi.</p><span class="from">mulai Rp 3.500.000</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-shield-halved"></i></div><h3>Security Audit</h3><p>Pemindaian celah, pengerasan server, laporan prioritas.</p><span class="from">mulai Rp 5.000.000</span></div>
</div></div></section>
<section><div class="wrap"><div class="cta rv"><h2>Butuh kombinasi?</h2>
<p>Banyak proyek menggabungkan web dan bot sekaligus. Sebutkan semuanya, saya susun satu penawaran utuh.</p>
<div class="row"><a href="__WA__?text=Halo__2C__saya__butuh__kombinasi" class="btn solid" target="_blank" rel="noopener">Diskusikan</a><a href="/harga" class="btn ghost">Lihat Tarif</a></div></div></div></section>
"""

B["/harga"] = """
<div class="wrap pghead"><div class="kick">03 · Tarif</div>
<h1>Harga penuh, <em>tanpa nego buta</em>.</h1>
<p class="lead">Tarif di bawah mengikuti harga pasar untuk pekerjaan dengan standar atelier: brief tertulis, pengujian, keamanan, dan garansi. Pembayaran 50 persen di awal, 50 persen saat serah terima.</p>
<nav class="tags" style="margin-top:20px">
  <span><a href="#web">Web</a></span><span><a href="#mobile">Mobile</a></span>
  <span><a href="#rawat">Perawatan</a></span><span><a href="#tambah">Tambahan</a></span>
  <span><a href="#hitung">Hitung Sendiri</a></span><span><a href="#syarat-harga">Ketentuan</a></span>
</nav></div>

<section id="web"><div class="wrap">
  <h2 class="rv">Web</h2><div class="hr rv"></div>
  <div class="plans rv">
    <div class="plan"><h3>Starter</h3><div class="price">Rp 1.750.000<small>sekali bayar</small></div><div class="eta"><i class="far fa-clock"></i> 5–7 hari</div>
      <ul><li><i class="fas fa-check"></i>1 halaman landing</li><li><i class="fas fa-check"></i>Desain custom ringan</li><li><i class="fas fa-check"></i>Responsif + uji perangkat</li><li><i class="fas fa-check"></i>SEO dasar + sitemap</li><li><i class="fas fa-check"></i>1x revisi</li><li class="off"><i class="fas fa-minus"></i>CMS</li></ul>
      <a href="__WA__?text=Paket__Starter" class="btn ghost" target="_blank" rel="noopener">Ambil</a></div>
    <div class="plan hot"><span class="tag">PALING DIPILIH</span><h3>Bisnis</h3><div class="price">Rp 6.500.000<small>sekali bayar</small></div><div class="eta"><i class="far fa-clock"></i> 14–20 hari</div>
      <ul><li><i class="fas fa-check"></i>Hingga 10 halaman</li><li><i class="fas fa-check"></i>Desain custom penuh</li><li><i class="fas fa-check"></i>CMS artikel &amp; katalog</li><li><i class="fas fa-check"></i>Hosting + SSL tahun pertama</li><li><i class="fas fa-check"></i>Analytics + pemantauan uptime</li><li><i class="fas fa-check"></i>2x revisi + garansi 30 hari</li></ul>
      <a href="__WA__?text=Paket__Bisnis" class="btn solid" target="_blank" rel="noopener">Ambil</a></div>
    <div class="plan"><h3>Enterprise</h3><div class="price">Rp 24.000.000<small>mulai dari</small></div><div class="eta"><i class="far fa-clock"></i> 35–50 hari</div>
      <ul><li><i class="fas fa-check"></i>Sistem / web app custom</li><li><i class="fas fa-check"></i>Multi-peran &amp; audit akses</li><li><i class="fas fa-check"></i>API + basis data terindeks</li><li><i class="fas fa-check"></i>Uji beban &amp; pengerasan</li><li><i class="fas fa-check"></i>Deploy VPS + CI</li><li><i class="fas fa-check"></i>Garansi 60 hari + dokumentasi</li></ul>
      <a href="__WA__?text=Paket__Enterprise" class="btn ghost" target="_blank" rel="noopener">Ambil</a></div>
  </div>
</div></section>

<section id="mobile"><div class="wrap">
  <h2 class="rv">Mobile — Android dan iOS dipisah</h2>
  <p class="lead rv" style="margin-bottom:26px">iOS lebih tinggi karena Apple Developer 99 dolar per tahun, build wajib lewat Xcode, dan review App Store jauh lebih ketat.</p>
  <div class="plans rv">
    <div class="plan"><h3>Android</h3><div class="price">Rp 15.000.000<small>mulai dari</small></div><div class="eta"><i class="far fa-clock"></i> 25–32 hari</div>
      <ul><li><i class="fas fa-check"></i>Kotlin / Flutter</li><li><i class="fas fa-check"></i>UI custom + uji perangkat</li><li><i class="fas fa-check"></i>Integrasi API</li><li><i class="fas fa-check"></i>Build, signing, Play Console</li><li><i class="fas fa-check"></i>Garansi 30 hari</li></ul>
      <a href="__WA__?text=Aplikasi__Android" class="btn ghost" target="_blank" rel="noopener">Ambil</a></div>
    <div class="plan"><h3>iPhone / iOS</h3><div class="price">Rp 26.000.000<small>mulai dari</small></div><div class="eta"><i class="far fa-clock"></i> 35–45 hari</div>
      <ul><li><i class="fas fa-check"></i>Swift / Flutter</li><li><i class="fas fa-check"></i>UI sesuai HIG Apple</li><li><i class="fas fa-check"></i>Integrasi API</li><li><i class="fas fa-check"></i>TestFlight + pendampingan review</li><li><i class="fas fa-check"></i>Garansi 30 hari</li></ul>
      <a href="__WA__?text=Aplikasi__iOS" class="btn ghost" target="_blank" rel="noopener">Ambil</a></div>
    <div class="plan hot"><span class="tag">EFISIEN</span><h3>Cross-Platform</h3><div class="price">Rp 38.000.000<small>mulai dari</small></div><div class="eta"><i class="far fa-clock"></i> 45–60 hari</div>
      <ul><li><i class="fas fa-check"></i>Satu basis Flutter</li><li><i class="fas fa-check"></i>Dua build platform</li><li><i class="fas fa-check"></i>Desain adaptif per sistem</li><li><i class="fas fa-check"></i>Dua store + pendampingan</li><li><i class="fas fa-check"></i>Garansi 45 hari</li></ul>
      <a href="__WA__?text=Cross-platform" class="btn solid" target="_blank" rel="noopener">Ambil</a></div>
  </div>
</div></section>

<section id="rawat"><div class="wrap">
  <h2 class="rv">Perawatan bulanan</h2>
  <p class="lead rv" style="margin-bottom:26px">Perangkat lunak tanpa perawatan akan menua. Semua paket mencakup cadangan harian dan pembaruan keamanan mingguan.</p>
  <div class="plans rv">
    <div class="plan"><h3>Dasar</h3><div class="price">Rp 750.000<small>per bulan</small></div>
      <ul><li><i class="fas fa-check"></i>Cadangan harian</li><li><i class="fas fa-check"></i>Pembaruan keamanan</li><li><i class="fas fa-check"></i>1 jam kerja/bulan</li></ul>
      <a href="__WA__?text=Rawatan__Dasar" class="btn ghost" target="_blank" rel="noopener">Ambil</a></div>
    <div class="plan"><h3>Prioritas</h3><div class="price">Rp 1.500.000<small>per bulan</small></div>
      <ul><li><i class="fas fa-check"></i>Semua isi paket Dasar</li><li><i class="fas fa-check"></i>Tanggap 12 jam</li><li><i class="fas fa-check"></i>4 jam kerja/bulan</li></ul>
      <a href="__WA__?text=Rawatan__Prioritas" class="btn ghost" target="_blank" rel="noopener">Ambil</a></div>
    <div class="plan"><h3>Khusus</h3><div class="price">Rp 3.000.000<small>per bulan</small></div>
      <ul><li><i class="fas fa-check"></i>Semua isi paket Prioritas</li><li><i class="fas fa-check"></i>Tanggap 4 jam</li><li><i class="fas fa-check"></i>10 jam kerja/bulan</li></ul>
      <a href="__WA__?text=Rawatan__Khusus" class="btn ghost" target="_blank" rel="noopener">Ambil</a></div>
  </div>
  <p class="rv" style="margin-top:18px;font-size:12.5px;color:var(--gold)">Tarif harian untuk pekerjaan lepas: Rp 850.000/hari, minimum 3 hari.</p>
</div></section>

<section id="tambah"><div class="wrap">
  <h2 class="rv">Tambahan</h2><div class="hr rv"></div>
  <table class="tbl rv"><tr><th>Layanan</th><th>Tarif</th></tr>
    <tr><td>Bot WhatsApp / Telegram</td><td>Rp 3.500.000</td></tr>
    <tr><td>Audit keamanan + pengerasan</td><td>Rp 5.000.000</td></tr>
    <tr><td>Integrasi payment gateway</td><td>Rp 2.750.000</td></tr>
    <tr><td>Desain UI/UX di Figma</td><td>Rp 3.250.000</td></tr>
    <tr><td>SEO on-page lanjutan</td><td>Rp 2.500.000</td></tr>
    <tr><td>Multi-bahasa (ID / EN)</td><td>Rp 4.000.000</td></tr>
    <tr><td>Migrasi data lama</td><td>Rp 3.000.000</td></tr>
    <tr><td>Pelatihan admin</td><td>Rp 1.250.000</td></tr>
  </table>
</div></section>

<section id="hitung"><div class="wrap">
  <h2 class="rv">Hitung sendiri</h2>
  <p class="lead rv" style="margin-bottom:24px">Centang yang dibutuhkan. Angka muncul langsung, lalu kirim sebagai brief.</p>
  <div class="grid rv" id="hitung-box">
    <label class="cell"><h3><input type="checkbox" class="hit" data-p="1750000" data-n="Landing page"> Landing page</h3><p>1 halaman fokus konversi.</p></label>
    <label class="cell"><h3><input type="checkbox" class="hit" data-p="6500000" data-n="Company profile"> Company profile</h3><p>Hingga 10 halaman + CMS.</p></label>
    <label class="cell"><h3><input type="checkbox" class="hit" data-p="8500000" data-n="Toko online"> Toko online</h3><p>Katalog, keranjang, checkout.</p></label>
    <label class="cell"><h3><input type="checkbox" class="hit" data-p="24000000" data-n="Sistem custom"> Sistem custom</h3><p>Dashboard dan multi-peran.</p></label>
    <label class="cell"><h3><input type="checkbox" class="hit" data-p="15000000" data-n="Aplikasi Android"> Aplikasi Android</h3><p>Native atau Flutter.</p></label>
    <label class="cell"><h3><input type="checkbox" class="hit" data-p="26000000" data-n="Aplikasi iOS"> Aplikasi iOS</h3><p>Swift atau Flutter.</p></label>
    <label class="cell"><h3><input type="checkbox" class="hit" data-p="3500000" data-n="Bot automation"> Bot automation</h3><p>WhatsApp / Telegram.</p></label>
    <label class="cell"><h3><input type="checkbox" class="hit" data-p="5000000" data-n="Audit keamanan"> Audit keamanan</h3><p>Pemindaian dan pengerasan.</p></label>
    <label class="cell"><h3><input type="checkbox" class="hit" data-p="2750000" data-n="Payment gateway"> Payment gateway</h3><p>Midtrans / Xendit.</p></label>
    <label class="cell"><h3><input type="checkbox" class="hit" data-p="3250000" data-n="Desain UI/UX"> Desain UI/UX</h3><p>Figma, sebelum kode.</p></label>
    <label class="cell"><h3><input type="checkbox" class="hit" data-p="1500000" data-n="Rawatan prioritas"> Rawatan 1 bulan</h3><p>Paket Prioritas.</p></label>
    <label class="cell"><h3><input type="checkbox" class="hit" data-p="1250000" data-n="Pelatihan admin"> Pelatihan admin</h3><p>Sesi penggunaan.</p></label>
  </div>
  <div class="cta rv" style="margin-top:24px">
    <h2 id="total" style="color:var(--gold2)">Rp 0</h2>
    <p id="rincian" style="font-size:12px">Belum ada item dipilih. Angka adalah estimasi awal, bukan penawaran final.</p>
    <div class="row"><a id="kirim" href="__WA__?text=Halo__estimasi__saya" class="btn solid" target="_blank" rel="noopener">Kirim sebagai Brief</a><a href="/kontak" class="btn ghost">Kanal Lain</a></div>
  </div>
</div></section>

<section id="syarat-harga"><div class="wrap">
  <h2 class="rv">Ketentuan harga</h2><div class="hr rv"></div>
  <table class="tbl rv">
    <tr><th>Hal</th><th>Ketentuan</th></tr>
    <tr><td>DP</td><td>50 persen saat surat pesanan ditandatangani</td></tr>
    <tr><td>Pelunasan</td><td>Sebelum serah terima kode dan kredensial</td></tr>
    <tr><td>Pajak</td><td>Belum termasuk PPN bila diperlukan</td></tr>
    <tr><td>Biaya pihak ketiga</td><td>Domain, hosting, Play Console, Apple Developer ditanggung klien</td></tr>
    <tr><td>Perubahan lingkup</td><td>Dihitung per jam atau lewat surat pesanan baru</td></tr>
    <tr><td>Percepatan</td><td>Tambah 25 persen dari nilai proyek per pemangkasan sepertiga durasi</td></tr>
  </table>
</div></section>

<script>
(function(){
  var b=document.getElementById('hitung-box'),t=document.getElementById('total'),
      r=document.getElementById('rincian'),k=document.getElementById('kirim');
  function f(n){return 'Rp '+n.toLocaleString('id-ID')}
  function upd(){
    var s=0,it=[];
    b.querySelectorAll('.hit:checked').forEach(function(c){s+=+c.dataset.p;it.push(c.dataset.n)});
    t.textContent=f(s);
    r.textContent=it.length?it.join(' + ')+' — estimasi awal, bukan penawaran final.':'Belum ada item dipilih.';
    k.href='__WA__?text='+encodeURIComponent('Halo, estimasi saya: '+it.join(', ')+' (total '+f(s)+')');
  }
  b.addEventListener('change',upd);
})();
</script>
"""

B["/portofolio"] = """
<div class="wrap pghead"><div class="kick">04 · Portofolio</div>
<h1>Enam pekerjaan, <em>enam hasil terukur</em>.</h1>
<p class="lead">Nama klien disamarkan sesuai perjanjian. Metrik diambil dari data yang diberikan klien setelah peluncuran.</p></div>
<section><div class="wrap"><div class="grid">
  <div class="cell rv"><div class="ic"><i class="fas fa-store"></i></div><h3>Retail Fashion</h3><p>Toko online + integrasi kurir. Muat 1,4 detik, checkout tiga langkah.</p><span class="from">+38 persen konversi</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-notes-medical"></i></div><h3>Klinik Estetika</h3><p>Sistem booking + bot pengingat. Admin bebas dari 40 panggilan harian.</p><span class="from">−2 jam kerja/hari</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-truck-fast"></i></div><h3>Logistik Regional</h3><p>Dashboard armada dan resi. Rekap harian otomatis.</p><span class="from">±600 resi/hari</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-utensils"></i></div><h3>Jaringan Restoran</h3><p>Menu digital multi-cabang dengan stok tersinkron.</p><span class="from">7 cabang</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-graduation-cap"></i></div><h3>Lembaga Kursus</h3><p>Aplikasi Android materi dan kuis. Ulasan rata-rata 4,7.</p><span class="from">4,7 bintang</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-shield-halved"></i></div><h3>Audit Koperasi</h3><p>Pengerasan setelah insiden. 23 temuan ditutup tanpa downtime.</p><span class="from">23 celah ditutup</span></div>
</div></div></section>
<section><div class="wrap"><div class="quotes rv">
  <div class="quote"><div class="st">★★★★★</div><p>"Selesai sesuai tanggal yang ditulis di awal. Komunikasi rapi, revisi cepat."</p><div class="who"><div class="av">R</div><div><b>Rizky A.</b><span>Retail</span></div></div></div>
  <div class="quote"><div class="st">★★★★★</div><p>"Sistem yang dulu di Excel sekarang multi-pengguna dan rapi."</p><div class="who"><div class="av">D</div><div><b>Dewi P.</b><span>Operasional</span></div></div></div>
  <div class="quote"><div class="st">★★★★★</div><p>"Dokumentasi dan serah terima lengkap. Tidak ada yang disembunyikan."</p><div class="who"><div class="av">F</div><div><b>Fajar S.</b><span>Klinik</span></div></div></div>
</div></div></section>
"""

B["/proses"] = """
<div class="wrap pghead"><div class="kick">05 · Proses</div>
<h1>Empat tahap, <em>semuanya terlihat</em>.</h1>
<p class="lead">Anda tahu posisi proyek di setiap tahap. Setiap tahap punya keluaran yang harus disetujui sebelum lanjut.</p></div>
<section><div class="wrap"><div class="steps">
  <div class="step rv"><h3>Brief</h3><p>Tujuan bisnis, pengguna sasaran, referensi visual, dan batasan teknis dipetakan jadi dokumen.</p></div>
  <div class="step rv"><h3>Desain</h3><p>Mockup dikirim untuk direview. Kode belum ditulis sampai Anda menyetujui arah visual.</p></div>
  <div class="step rv"><h3>Development</h3><p>Pengerjaan bertahap dengan tautan preview yang bisa Anda pantau kapan pun.</p></div>
  <div class="step rv"><h3>Peluncuran</h3><p>Deploy, serah terima kode dan kredensial, pelatihan singkat, lalu masa garansi berjalan.</p></div>
</div></div></section>
<section><div class="wrap"><h2 class="rv">Yang perlu Anda siapkan</h2><div class="hr rv"></div>
<table class="tbl rv"><tr><th>Tahap</th><th>Materi dari Anda</th></tr>
  <tr><td>Brief</td><td>Tujuan, contoh acuan, daftar fitur wajib</td></tr>
  <tr><td>Desain</td><td>Logo, palet warna, foto produk, naskah</td></tr>
  <tr><td>Development</td><td>Akses domain/hosting, kunci API, akun uji</td></tr>
  <tr><td>Peluncuran</td><td>Persetujuan akhir dan pelunasan</td></tr>
</table></div></section>
"""

B["/stack"] = """
<div class="wrap pghead"><div class="kick">06 · Stack</div>
<h1>Perangkat dan <em>tingkat penguasaan</em>.</h1>
<p class="lead">Angka di bawah penilaian jujur, bukan klaim. Yang di bawah 80 persen dikerjakan dengan pendampingan riset tambahan.</p></div>
<section><div class="wrap"><div class="skills">
  <div class="skill rv"><div class="top"><span>Python &amp; Automation</span><b>95%</b></div><div class="bar"><i data-w="95"></i></div></div>
  <div class="skill rv"><div class="top"><span>Linux / Pengerasan VPS</span><b>93%</b></div><div class="bar"><i data-w="93"></i></div></div>
  <div class="skill rv"><div class="top"><span>JavaScript / Node.js</span><b>90%</b></div><div class="bar"><i data-w="90"></i></div></div>
  <div class="skill rv"><div class="top"><span>Cyber Security</span><b>89%</b></div><div class="bar"><i data-w="89"></i></div></div>
  <div class="skill rv"><div class="top"><span>PHP / Laravel</span><b>88%</b></div><div class="bar"><i data-w="88"></i></div></div>
  <div class="skill rv"><div class="top"><span>MySQL / PostgreSQL</span><b>87%</b></div><div class="bar"><i data-w="87"></i></div></div>
  <div class="skill rv"><div class="top"><span>UI/UX Design</span><b>86%</b></div><div class="bar"><i data-w="86"></i></div></div>
  <div class="skill rv"><div class="top"><span>Flutter / Dart</span><b>85%</b></div><div class="bar"><i data-w="85"></i></div></div>
  <div class="skill rv"><div class="top"><span>React / Next.js</span><b>84%</b></div><div class="bar"><i data-w="84"></i></div></div>
  <div class="skill rv"><div class="top"><span>Kotlin (Android)</span><b>82%</b></div><div class="bar"><i data-w="82"></i></div></div>
  <div class="skill rv"><div class="top"><span>Swift (iOS)</span><b>78%</b></div><div class="bar"><i data-w="78"></i></div></div>
  <div class="skill rv"><div class="top"><span>Docker / CI</span><b>76%</b></div><div class="bar"><i data-w="76"></i></div></div>
</div></div></section>
"""

B["/keamanan"] = """
<div class="wrap pghead"><div class="kick">07 · Keamanan</div>
<h1>Kerentanan yang <em>ditangani lebih dulu</em>.</h1>
<p class="lead">Keamanan bukan tambahan di akhir. Kategori di bawah masuk daftar periksa setiap proyek, dan bisa diuji terpisah lewat audit resmi.</p></div>
<section><div class="wrap"><h2 class="rv">Cakupan audit</h2><div class="hr rv"></div>
<table class="tbl rv"><tr><th>Kerentanan</th><th>Tingkat</th><th>Penanganan</th></tr>
  <tr><td>SQL Injection</td><td><span class="sev c">KRITIS</span></td><td>Query berparameter, ORM, validasi tipe</td></tr>
  <tr><td>Cross-Site Scripting</td><td><span class="sev c">KRITIS</span></td><td>Escaping keluaran, CSP ketat</td></tr>
  <tr><td>Broken Authentication</td><td><span class="sev c">KRITIS</span></td><td>Hash argon2, batas percobaan, MFA opsional</td></tr>
  <tr><td>IDOR / Akses Tak Sah</td><td><span class="sev h">TINGGI</span></td><td>Pemeriksaan kepemilikan per objek</td></tr>
  <tr><td>CSRF</td><td><span class="sev h">TINGGI</span></td><td>Token per sesi, SameSite, verifikasi asal</td></tr>
  <tr><td>File Upload Berbahaya</td><td><span class="sev h">TINGGI</span></td><td>Validasi MIME, batas ukuran, simpan di luar webroot</td></tr>
  <tr><td>Rate Limit Longgar</td><td><span class="sev m">SEDANG</span></td><td>Pembatasan per IP dan per akun</td></tr>
  <tr><td>Header Tidak Lengkap</td><td><span class="sev m">SEDANG</span></td><td>CSP, HSTS, X-Frame-Options, Permissions-Policy</td></tr>
  <tr><td>Kredensial di Repo</td><td><span class="sev m">SEDANG</span></td><td>Variabel lingkungan, gitignore, rotasi kunci</td></tr>
  <tr><td>Banner Versi Bocor</td><td><span class="sev l">RENDAH</span></td><td>Samarkan header server</td></tr>
  <tr><td>Direktori Terbuka</td><td><span class="sev l">RENDAH</span></td><td>Matikan listing, routing eksplisit</td></tr>
</table></div></section>
<section><div class="wrap"><div class="cta rv"><h2>Minta audit</h2>
<p>Audit berjalan 3–5 hari kerja dengan laporan bertingkat prioritas dan sesi penjelasan hasil.</p>
<div class="row"><a href="__WA__?text=Halo__saya__mau__audit" class="btn solid" target="_blank" rel="noopener">Ajukan Audit</a><a href="/roadmap" class="btn ghost">Lihat Roadmap</a></div></div></div></section>
"""

B["/sla"] = """
<div class="wrap pghead"><div class="kick">08 · Ketentuan</div>
<h1>Aturan main yang <em>jelas di depan</em>.</h1>
<p class="lead">Ditulis supaya kedua pihak tenang. Semua poin masuk ke dokumen kerja sebelum proyek dimulai.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Hal</th><th>Ketentuan</th></tr>
  <tr><td>Pembayaran</td><td>50 persen tanda jadi, 50 persen sebelum serah terima.</td></tr>
  <tr><td>Revisi</td><td>Starter 1x, Bisnis 2x, paket mobile sesuai kontrak.</td></tr>
  <tr><td>Garansi</td><td>30 hari web dasar, 60 hari Enterprise, 45 hari cross-platform. Hanya untuk bug.</td></tr>
  <tr><td>Kepemilikan</td><td>Kode dan aset menjadi milik klien setelah pelunasan.</td></tr>
  <tr><td>Kerahasiaan</td><td>NDA tersedia atas permintaan, sebelum brief.</td></tr>
  <tr><td>Pembatalan</td><td>Tanda jadi tidak kembali bila desain sudah disetujui.</td></tr>
  <tr><td>Keterlambatan</td><td>Materi klien yang telat menunda tanggal.</td></tr>
  <tr><td>Percepatan</td><td>Tersedia dengan biaya prioritas.</td></tr>
</table></div></section>
"""

B["/faq"] = """
<div class="wrap pghead"><div class="kick">09 · Tanya</div>
<h1>Yang paling sering <em>ditanyakan</em>.</h1>
<p class="lead">Kalau jawabannya belum ada di sini, tanyakan langsung — tidak ada pertanyaan yang terlalu kecil.</p></div>
<section><div class="wrap">
  <details class="rv"><summary>Berapa DP-nya?</summary><div class="bd"><div><p>50 persen tanda jadi, 50 persen sebelum serah terima. Tidak ada pelunasan di muka.</p></div></div></details>
  <details class="rv"><summary>Kenapa iOS lebih mahal?</summary><div class="bd"><div><p>Apple Developer 99 dolar per tahun, build wajib lewat Xcode, dan review App Store jauh lebih ketat.</p></div></div></details>
  <details class="rv"><summary>Bisa lebih cepat?</summary><div class="bd"><div><p>Bisa dengan biaya prioritas. Estimasi normal sengaja dilonggarkan supaya tidak jadi janji kosong.</p></div></div></details>
  <details class="rv"><summary>Source code jadi milik saya?</summary><div class="bd"><div><p>Ya, setelah pelunasan. Tanpa penguncian atau sewa lisensi.</p></div></div></details>
  <details class="rv"><summary>Garansi mencakup apa?</summary><div class="bd"><div><p>Bug dan error dari sisi pengerjaan. Fitur baru di luar brief masuk pengembangan lanjutan.</p></div></div></details>
  <details class="rv"><summary>Bisa NDA?</summary><div class="bd"><div><p>Bisa. Kirim draf Anda, atau saya siapkan versi sederhana.</p></div></div></details>
  <details class="rv"><summary>Termasuk hosting dan akun store?</summary><div class="bd"><div><p>Hosting dan SSL tahun pertama termasuk di paket Bisnis dan Enterprise. Akun store dibuat atas nama Anda.</p></div></div></details>
  <details class="rv"><summary>Bagaimana kalau hasil tidak sesuai?</summary><div class="bd"><div><p>Ada tahap persetujuan desain sebelum kode ditulis. Ketidaksesuaian di tahap itu diselesaikan tanpa biaya tambahan.</p></div></div></details>
</div></section>
"""

B["/kontak"] = """
<div class="wrap pghead"><div class="kick">10 · Kontak</div>
<h1>Mari mulai <em>percakapan</em>.</h1>
<p class="lead">Konsultasi awal tanpa biaya. Balasan berisi estimasi biaya, durasi, dan cakupan yang bisa Anda nilai langsung.</p></div>
<section><div class="wrap"><div class="cgrid rv">
  <a class="clink" href="__WA__" target="_blank" rel="noopener"><i class="fab fa-whatsapp"></i> WhatsApp</a>
  <a class="clink" href="https://t.me/WiteXCTbot" target="_blank" rel="noopener"><i class="fab fa-telegram-plane"></i> Telegram Bot</a>
  <a class="clink" href="https://t.me/wof1NBI7ObBlNzE9" target="_blank" rel="noopener"><i class="fab fa-telegram"></i> Kanal</a>
  <a class="clink" href="https://fastwork.id/user/alfiliaor_web" target="_blank" rel="noopener"><i class="fas fa-briefcase"></i> Fastwork</a>
  <a class="clink" href="https://hackerone.com/javanova?type=user" target="_blank" rel="noopener"><i class="fas fa-bug"></i> HackerOne</a>
  <a class="clink" href="https://gitlab.com/yuana448" target="_blank" rel="noopener"><i class="fab fa-gitlab"></i> GitLab</a>
  <a class="clink" href="https://www.linkedin.com/in/fidilia-salsabilla-8b18b4449/" target="_blank" rel="noopener"><i class="fab fa-linkedin-in"></i> LinkedIn</a>
  <a class="clink" href="https://github.com/yuana448" target="_blank" rel="noopener"><i class="fab fa-github"></i> GitHub</a>
  <a class="clink" href="https://web.facebook.com/zerinova112/" target="_blank" rel="noopener"><i class="fab fa-facebook-f"></i> Facebook</a>
  <a class="clink" href="https://www.instagram.com/javanova666/" target="_blank" rel="noopener"><i class="fab fa-instagram"></i> Instagram</a>
  <a class="clink" href="https://x.com/Leon63921453481" target="_blank" rel="noopener"><i class="fab fa-x-twitter"></i> Twitter / X</a>
</div></div></section>
<section><div class="wrap"><h2 class="rv">Format brief yang cepat diproses</h2><div class="hr rv"></div>
<table class="tbl rv"><tr><th>Poin</th><th>Contoh isian</th></tr>
  <tr><td>Jenis</td><td>Toko online / aplikasi Android / sistem internal</td></tr>
  <tr><td>Tujuan</td><td>Menambah penjualan daring, mengganti pencatatan manual</td></tr>
  <tr><td>Fitur wajib</td><td>Login, katalog, keranjang, laporan penjualan</td></tr>
  <tr><td>Target waktu</td><td>6 minggu, atau belum mendesak</td></tr>
  <tr><td>Anggaran</td><td>Kisaran yang Anda siapkan</td></tr>
</table>
<div style="margin-top:26px"><a href="__WA__?text=Halo__ini__brief__saya" class="btn solid" target="_blank" rel="noopener">Kirim Brief via WhatsApp</a></div>
</div></section>
"""

# ------------------------------------------------ 20 ruang baru
B["/mulai"] = """
<div class="wrap pghead"><div class="kick">11 · Mulai</div>
<h1>Tiga langkah, <em>tanpa bingung</em>.</h1>
<p class="lead">Banyak calon klien menunda karena tidak tahu harus mulai dari mana. Ini urutan paling ringkas.</p></div>
<section><div class="wrap"><div class="steps">
  <div class="step rv"><h3>Tulis kebutuhan</h3><p>Satu paragraf cukup: masalah, siapa penggunanya, hasil yang diharapkan.</p></div>
  <div class="step rv"><h3>Terima estimasi</h3><p>Balasan berisi biaya, durasi, dan cakupan. Tidak ada tagihan untuk tahap ini.</p></div>
  <div class="step rv"><h3>Kunci brief</h3><p>Setelah sepakat, dokumen kerja ditandatangani dan pengerjaan dijadwalkan.</p></div>
</div></div></section>
<section><div class="wrap"><div class="cta rv"><h2>Mulai dari paragraf pertama</h2>
<p>Kirim satu pesan singkat. Kalau belum yakin, tulis saja "belum tahu mau apa" — tetap saya bantu petakan.</p>
<div class="row"><a href="__WA__?text=Halo__saya__mau__mulai" class="btn solid" target="_blank" rel="noopener">Kirim Pesan</a><a href="/kontak" class="btn ghost">Kanal Lain</a></div></div></div></section>
"""

B["/matriks"] = """
<div class="wrap pghead"><div class="kick">12 · Matriks</div>
<h1>Bandingkan <em>baris demi baris</em>.</h1>
<p class="lead">Supaya tidak ada yang tersembunyi di balik kata menyesuaikan.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Isi</th><th>Starter</th><th>Bisnis</th><th>Enterprise</th></tr>
  <tr><td>Harga</td><td>Rp 1.750.000</td><td>Rp 6.500.000</td><td>mulai Rp 24.000.000</td></tr>
  <tr><td>Jumlah halaman</td><td>1</td><td>10</td><td>tanpa batas wajar</td></tr>
  <tr><td>Desain custom</td><td>ringan</td><td>penuh</td><td>penuh + sistem desain</td></tr>
  <tr><td>CMS</td><td>tidak</td><td>ya</td><td>ya</td></tr>
  <tr><td>Login pengguna</td><td>tidak</td><td>opsional</td><td>ya</td></tr>
  <tr><td>Multi-peran</td><td>tidak</td><td>tidak</td><td>ya</td></tr>
  <tr><td>API internal</td><td>tidak</td><td>tidak</td><td>ya</td></tr>
  <tr><td>Uji beban</td><td>tidak</td><td>dasar</td><td>penuh</td></tr>
  <tr><td>Hosting + SSL</td><td>setup saja</td><td>1 tahun</td><td>1 tahun + CI</td></tr>
  <tr><td>Revisi</td><td>1x</td><td>2x</td><td>sesuai kontrak</td></tr>
  <tr><td>Garansi</td><td>30 hari</td><td>30 hari</td><td>60 hari</td></tr>
  <tr><td>Dokumentasi</td><td>tidak</td><td>ringkas</td><td>lengkap</td></tr>
</table></div></section>
"""

B["/web"] = """
<div class="wrap pghead"><div class="kick">13 · Teknologi Web</div>
<h1>Tumpukan kerja <em>sisi web</em>.</h1>
<p class="lead">Dipilih karena mudah dirawat, bukan karena sedang populer. Semua punya jalur pindah bila proyek membesar.</p></div>
<section><div class="wrap"><div class="grid">
  <div class="cell rv"><div class="ic"><i class="fab fa-php"></i></div><h3>Laravel</h3><p>Kerangka kerja matang untuk sistem dengan banyak aturan bisnis.</p></div>
  <div class="cell rv"><div class="ic"><i class="fab fa-node-js"></i></div><h3>Node.js</h3><p>Untuk API realtime dan layanan yang butuh koneksi bersamaan.</p></div>
  <div class="cell rv"><div class="ic"><i class="fab fa-react"></i></div><h3>React / Next</h3><p>Antarmuka interaktif dengan render sisi server bila perlu.</p></div>
  <div class="cell rv"><div class="ic"><i class="fab fa-python"></i></div><h3>Python</h3><p>Skrip, pengolah data, dan layanan internal ringan.</p></div>
</div>
<h2 class="rv" style="margin-top:34px">Batasannya</h2><div class="hr rv"></div>
<table class="tbl rv"><tr><th>Hal</th><th>Sikap</th></tr>
  <tr><td>Framework baru tanpa komunitas</td><td>dihindari</td></tr>
  <tr><td>Plugin tanpa pembaruan setahun</td><td>diganti atau dipisah</td></tr>
  <tr><td>Situs tanpa uji beban</td><td>tidak diluncurkan</td></tr>
</table></div></section>
"""

B["/mobile"] = """

<div class="m14">
<style>
.m14{--ml:var(--line2)}
.m14-hero{position:relative;padding:54px 0 0;overflow:hidden;isolation:isolate}
.m14-aur{position:absolute;inset:-42% -12% 26%;z-index:-2;pointer-events:none;filter:blur(62px);opacity:.85;
  background:radial-gradient(38% 46% at 20% 34%,var(--glow),transparent 70%),
             radial-gradient(34% 42% at 82% 24%,rgba(92,184,245,.3),transparent 72%),
             radial-gradient(32% 40% at 52% 86%,rgba(240,121,156,.24),transparent 74%);
  animation:m14aur 16s ease-in-out infinite alternate}
@keyframes m14aur{to{transform:translate3d(0,-5%,0) scale(1.15) rotate(7deg)}}
.m14 h1{font-size:clamp(36px,10.5vw,78px);line-height:.97;letter-spacing:-.035em;margin:0 0 20px}
.m14 h1 em{font-style:italic;background:linear-gradient(100deg,var(--gold2),var(--gold),var(--gold2));
  background-size:230% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;
  animation:m14sh 7s linear infinite}
@keyframes m14sh{to{background-position:-230% 0}}
.m14-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:24px}
.m14-chip{display:inline-flex;align-items:baseline;gap:7px;font-family:'JetBrains Mono',monospace;
  font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);
  border:1px solid var(--ml);padding:7px 12px;border-radius:99px;background:var(--panel)}
.m14-chip b{color:var(--gold);font-size:11px}

.m14-stage{--rad:292px;position:relative;height:340px;margin:6px auto 0;max-width:860px;
  perspective:1450px;perspective-origin:50% 44%;cursor:grab;touch-action:pan-y;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 11%,#000 89%,transparent);
  mask-image:linear-gradient(90deg,transparent,#000 11%,#000 89%,transparent)}
.m14-stage:active{cursor:grabbing}
.m14-ring{position:absolute;inset:0;transform-style:preserve-3d;
  transform:rotateX(calc(-9deg + var(--tx,0deg))) rotateY(var(--ry,0deg));transition:transform .4s var(--ease)}
.m14-stage:active .m14-ring{transition:none}
.m14-spin{position:absolute;inset:0;transform-style:preserve-3d;animation:m14spin 42s linear infinite}
.m14-stage:active .m14-spin{animation-play-state:paused}
@keyframes m14spin{to{transform:rotateY(360deg)}}
.m14-item{position:absolute;left:50%;top:50%;width:154px;height:240px;margin:-120px 0 0 -77px;
  transform:rotateY(calc(var(--i) * 60deg)) translateZ(var(--rad));
  border:1px solid var(--ml);border-radius:17px;overflow:hidden;
  background:linear-gradient(170deg,var(--panel2),var(--panel) 64%);
  box-shadow:0 36px 66px -34px #000,inset 0 0 0 1px rgba(255,255,255,.03);
  display:flex;flex-direction:column;padding:10px;backface-visibility:hidden;
  transition:box-shadow .4s}
.m14-item span{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.2em;
  color:var(--gold);text-transform:uppercase;margin-bottom:7px}
.m14-item em{font-style:normal;font-family:'JetBrains Mono',monospace;font-size:8.5px;
  color:var(--dim);letter-spacing:.05em;margin-top:7px}
.m14-item:hover{box-shadow:0 0 0 1px var(--gold),0 36px 70px -30px var(--glow)}
.m14 .scr{position:relative;flex:1;border-radius:11px;overflow:hidden;background:#0b0b11;
  border:1px solid var(--ml)}
.m14 .scr.r-tab,.m14 .scr.r-lap,.m14 .scr.r-pc{flex:0 0 auto}
.m14 .scr.r-tab{aspect-ratio:3/4}
.m14 .scr.r-lap{aspect-ratio:16/10}
.m14 .scr.r-pc{aspect-ratio:16/9}
.m14-floor{height:2px;max-width:520px;margin:4px auto 0;
  background:linear-gradient(90deg,transparent,var(--line),transparent)}
@media(max-width:560px){.m14-stage{--rad:222px;height:300px}}

/* layar admin */
.ad{position:absolute;inset:0;display:flex;flex-direction:column;color:#e9e4da;
  font-family:'JetBrains Mono',monospace}
.ad-bar{display:flex;align-items:center;gap:3px;padding:5px;background:#101019;
  border-bottom:1px solid rgba(212,175,122,.2)}
.ad-dot{width:3px;height:3px;border-radius:50%;background:#d4af7a;opacity:.7}
.ad-title{margin-left:3px;font-size:4.6px;letter-spacing:.12em;color:#8f8b81;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ad-body{flex:1;display:flex;min-height:0}
.ad-side{width:22%;border-right:1px solid rgba(212,175,122,.14);padding:6px 3px;
  display:flex;flex-direction:column;gap:6px;align-items:center;background:#0d0d14}
.ad-logo{width:10px;height:10px;display:grid;place-items:center;border:1px solid #d4af7a;
  color:#d4af7a;font-size:5px}
.ad-side i{width:60%;height:2px;border-radius:2px;background:rgba(212,175,122,.28)}
.ad-side i:first-of-type{background:#d4af7a}
.ad-main{flex:1;padding:6px;display:flex;flex-direction:column;gap:4px;min-width:0}
.ad-kpi{display:flex;gap:3px}
.ad-kpi>div{flex:1;border:1px solid rgba(212,175,122,.18);border-radius:2px;padding:3px;background:#10101a}
.ad-kpi b{display:block;font-size:6.2px;color:#f0d9b0;line-height:1}
.ad-kpi span{font-size:3.2px;letter-spacing:.1em;color:#5f5c55;text-transform:uppercase}
.ad-chart{display:flex;align-items:flex-end;gap:2px;height:30px;padding:3px;border-radius:2px;
  border:1px solid rgba(255,255,255,.07);background:#0a0a10}
.ad-chart i{flex:1;height:var(--h);border-radius:1px 1px 0 0;transform-origin:bottom;
  background:linear-gradient(#f0d9b0,#d4af7a);opacity:.8;animation:adg 3.6s ease-in-out infinite}
.ad-chart i:nth-child(2n){animation-delay:.55s}
.ad-chart i:nth-child(3n){animation-delay:1.15s}
@keyframes adg{50%{transform:scaleY(.52)}}
.ad-tbl{display:flex;flex-direction:column;gap:2px}
.ad-tr{display:flex;align-items:center;gap:3px;border:1px solid rgba(255,255,255,.06);
  border-radius:2px;padding:3px;background:#0d0d14}
.ad-tr u{flex:1;height:2px;border-radius:2px;background:rgba(255,255,255,.16)}
.ad-tr em{width:13px;height:4px;border-radius:99px;background:rgba(63,219,154,.55)}
.ad-tr em.w{background:rgba(255,194,122,.55)}
.ad-nav{display:none;border-top:1px solid rgba(212,175,122,.2);padding:5px;
  justify-content:space-around}
.ad-nav i{width:7px;height:2px;border-radius:2px;background:rgba(212,175,122,.35)}
.ad-nav i:first-child{background:#d4af7a}
.compact .ad-side{display:none}
.compact .ad-nav{display:flex}
.compact .ad-kpi>div:nth-child(3){display:none}

.m14-sec{padding:48px 0 0}
.m14-ledger{display:grid;gap:1px;background:var(--line2);border:1px solid var(--line2);
  grid-template-columns:1fr}
.m14-card{position:relative;background:var(--panel);padding:22px 20px;overflow:hidden;
  transition:.35s var(--ease)}
.m14-card::before{content:"";position:absolute;top:0;left:0;width:16px;height:16px;
  border-top:1px solid var(--gold);border-left:1px solid var(--gold);opacity:.5;transition:.4s var(--ease)}
.m14-card:hover::before{width:100%;height:100%;opacity:.16}
.m14-card:hover{background:var(--panel2)}
.m14-card b{display:block;font-family:'JetBrains Mono',monospace;font-size:20px;
  color:var(--gold2);line-height:1}
.m14-card span{display:block;font-size:8.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--dim);margin-top:6px}
.m14-card p{font-size:12.2px;color:var(--muted);margin-top:12px}

.m14-route{border:1px solid var(--line2);background:var(--panel);padding:20px;
  margin-bottom:1px;transition:.3s}
.m14-route:hover{border-color:var(--line);background:var(--panel2)}
.m14-route .hd{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.m14-route .hd b{font-family:'JetBrains Mono',monospace;font-size:10.5px;color:var(--gold);
  letter-spacing:.1em}
.m14-route p{font-size:12.2px;color:var(--muted);margin:8px 0 12px}
.m14-route .bar{height:3px;background:rgba(255,255,255,.07);overflow:hidden}
.m14-route .bar i{display:block;height:100%;width:0;
  background:linear-gradient(90deg,var(--gold),var(--gold2));transition:width 1.5s var(--ease)}

.m14-pipe{display:grid;gap:1px;background:var(--line2);border:1px solid var(--line2);
  counter-reset:p;grid-template-columns:1fr}
.m14-pipe div{background:var(--panel);padding:20px 18px 20px 56px;position:relative;
  font-size:12.4px;color:var(--muted)}
.m14-pipe div::before{counter-increment:p;content:"0" counter(p);position:absolute;
  left:20px;top:20px;font-family:'JetBrains Mono',monospace;font-size:10.5px;color:var(--gold)}
.m14-pipe b{display:block;color:var(--ink);font-size:13px;margin-bottom:5px}

@media(min-width:640px){
  .m14-ledger{grid-template-columns:repeat(2,1fr)}
  .m14-pipe{grid-template-columns:repeat(2,1fr)}
}
@media(min-width:1024px){
  .m14-ledger{grid-template-columns:repeat(3,1fr)}
  .m14-pipe{grid-template-columns:repeat(4,1fr)}
}
@media(prefers-reduced-motion:reduce){
  .m14-aur,.m14 h1 em,.m14-spin,.ad-chart i{animation:none}
  .m14 h1 em{color:var(--gold2);-webkit-text-fill-color:currentColor}
}
</style>

<div class="m14-hero">
  <div class="m14-aur"></div>
  <div class="wrap">
    <div class="kick">14 · Lab Perangkat</div>
    <h1>Enam kanvas.<br><em>Satu panel admin.</em></h1>
    <p class="lead">Satu basis kode, enam kelas layar. Panel admin yang sama dirender ulang per perangkat: sidebar penuh di layar lebar, navigasi bawah di ponsel. Tata letak, target sentuh, dan beban render disesuaikan — dari 360 piksel sampai 2560 piksel.</p>
    <div class="m14-chips">
      <span class="m14-chip"><b>6</b> kelas perangkat</span>
      <span class="m14-chip"><b>44 px</b> target sentuh</span>
      <span class="m14-chip"><b>3</b> jalur teknis</span>
      <span class="m14-chip"><b>0</b> tata letak terpotong</span>
    </div>
  </div>
  <div class="m14-stage" id="m14stage">
    <div class="m14-ring" id="m14ring">
      <div class="m14-spin">
        <div class="m14-item" style="--i:0" data-compact="1"><span>Android</span><div class="scr"></div><em>360–430 px</em></div>
        <div class="m14-item" style="--i:1" data-compact="1"><span>iPhone</span><div class="scr"></div><em>375–430 px</em></div>
        <div class="m14-item" style="--i:2"><span>iPad</span><div class="scr r-tab"></div><em>768–1024 px</em></div>
        <div class="m14-item" style="--i:3"><span>Tablet</span><div class="scr r-tab"></div><em>600–840 px</em></div>
        <div class="m14-item" style="--i:4"><span>Laptop</span><div class="scr r-lap"></div><em>1280–1600 px</em></div>
        <div class="m14-item" style="--i:5"><span>PC</span><div class="scr r-pc"></div><em>1600–2560 px</em></div>
      </div>
    </div>
  </div>
  <div class="m14-floor"></div>
</div>

<section class="m14-sec"><div class="wrap">
  <div class="kick rv">Breakpoint</div>
  <h2 class="rv">Enam kanvas, enam aturan</h2><div class="hr rv"></div>
  <div class="m14-ledger rv">
    <div class="m14-card"><b>360</b><span>ponsel sempit</span><p>Satu kolom, sidebar dilipat ke nav bawah, dua kartu KPI, target sentuh 44 px.</p></div>
    <div class="m14-card"><b>390</b><span>ponsel standar</span><p>Chart tetap terbaca, tabel dua baris, tombol aksi menempel bawah.</p></div>
    <div class="m14-card"><b>600</b><span>ponsel besar</span><p>Tiga kartu KPI, tabel empat baris, jarak antar kartu naik.</p></div>
    <div class="m14-card"><b>820</b><span>tablet</span><p>Sidebar tetap terlihat, chart dan tabel berdampingan dua kolom.</p></div>
    <div class="m14-card"><b>1280</b><span>laptop</span><p>Tiga kolom, sidebar penuh, tabel dengan kolom status terpisah.</p></div>
    <div class="m14-card"><b>1600</b><span>PC</span><p>Empat kolom, panel samping ganda, chart selebar separuh layar.</p></div>
  </div>
</div></section>

<section class="m14-sec"><div class="wrap">
  <div class="kick rv">Jalur teknis</div>
  <h2 class="rv">Dipilih per kebutuhan, bukan selera</h2><div class="hr rv"></div>
  <div class="rv">
    <div class="m14-route"><div class="hd"><h3>Kotlin</h3><b>native</b></div>
      <p>Native Android. Akses penuh kamera, Bluetooth, dan sensor berat. Dipakai bila performa dan integrasi perangkat menentukan.</p>
      <div class="bar"><i data-w="88"></i></div></div>
    <div class="m14-route"><div class="hd"><h3>Swift</h3><b>native</b></div>
      <p>Native iOS. Mengikuti panduan antarmuka Apple dan wajib lewat review App Store.</p>
      <div class="bar"><i data-w="80"></i></div></div>
    <div class="m14-route"><div class="hd"><h3>Flutter</h3><b>cross-platform</b></div>
      <p>Satu basis kode, dua build, biaya lebih rendah. Dipakai bila kedua platform wajib dan anggaran terbatas.</p>
      <div class="bar"><i data-w="92"></i></div></div>
  </div>
</div></section>

<section class="m14-sec"><div class="wrap">
  <h2 class="rv">Kebutuhan dan jalurnya</h2><div class="hr rv"></div>
  <table class="tbl rv">
    <tr><th>Kebutuhan</th><th>Jalur yang disarankan</th></tr>
    <tr><td>Akses kamera, Bluetooth, sensor berat</td><td>native</td></tr>
    <tr><td>Anggaran terbatas, rilis cepat</td><td>cross-platform</td></tr>
    <tr><td>Kedua platform wajib</td><td>cross-platform lebih dulu, native bila perlu</td></tr>
    <tr><td>Tablet dan iPad</td><td>dua kolom, target sentuh 44 px</td></tr>
    <tr><td>Laptop dan PC</td><td>tiga sampai empat kolom, papan ketik penuh</td></tr>
    <tr><td>Panel admin di semua layar</td><td>satu komponen, empat varian tata letak</td></tr>
  </table>
</div></section>

<section class="m14-sec"><div class="wrap">
  <h2 class="rv">Jalur kerja</h2><div class="hr rv"></div>
  <div class="m14-pipe rv">
    <div><b>Kanvas</b>Peta breakpoint dan target sentuh per kelas perangkat.</div>
    <div><b>Bangun</b>Satu basis kode, tata letak menyesuaikan lebar layar.</div>
    <div><b>Uji</b>Layar sempit, sedang, lebar; dua peramban; dua orientasi.</div>
    <div><b>Rilis</b>Build bertanda tangan, dua store, pendampingan review.</div>
  </div>
</div></section>

<section class="m14-sec"><div class="wrap"><div class="cta rv">
  <h2>Butuh aplikasi dengan panel admin?</h2>
  <p>Sebutkan perangkat sasaran dan fitur wajib. Balasan berisi jalur teknis, estimasi, dan durasi.</p>
  <div class="row"><a href="__WA__?text=Halo__soal__aplikasi" class="btn solid" target="_blank" rel="noopener">Kirim Brief</a><a href="/harga" class="btn ghost">Lihat Tarif</a></div>
</div></div></section>

<script nonce="__NONCE__">
(function(){
  function chart(){ var o=''; [34,56,40,72,48,84,60,94].forEach(function(v){ o+='<i style="--h:'+v+'%"></i>'; }); return o; }
  function tbl(){ var o=''; [0,1,0,1].forEach(function(k){ o+='<div class="ad-tr"><u></u><em'+(k?' class="w"':'')+'></em></div>'; }); return o; }
  function build(compact){
    return '<div class="ad'+(compact?' compact':'')+'">'
      + '<div class="ad-bar"><i class="ad-dot"></i><i class="ad-dot"></i><i class="ad-dot"></i>'
      + '<span class="ad-title">admin · alfiliator</span></div>'
      + '<div class="ad-body">'
      + (compact ? '' : '<div class="ad-side"><b class="ad-logo">A</b><i></i><i></i><i></i><i></i></div>')
      + '<div class="ad-main">'
      + '<div class="ad-kpi"><div><b>128</b><span>proyek</span></div>'
      + '<div><b>96%</b><span>kembali</span></div><div><b>2j</b><span>respon</span></div></div>'
      + '<div class="ad-chart">' + chart() + '</div>'
      + '<div class="ad-tbl">' + tbl() + '</div>'
      + '</div></div>'
      + '<div class="ad-nav"><i></i><i></i><i></i><i></i></div></div>';
  }
  document.querySelectorAll('.m14 .scr').forEach(function(s){
    var it = s.closest('.m14-item');
    s.innerHTML = build(it && it.dataset.compact === '1');
  });

  var st=document.getElementById('m14stage'), ring=document.getElementById('m14ring');
  if(!st || !ring) return;
  if(matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  var drag=false, x0=0, r0=0;
  st.addEventListener('pointerdown', function(e){
    drag=true; x0=e.clientX;
    r0=parseFloat(getComputedStyle(ring).getPropertyValue('--ry')) || 0;
    if(st.setPointerCapture) st.setPointerCapture(e.pointerId);
  });
  st.addEventListener('pointermove', function(e){
    var r=st.getBoundingClientRect();
    if(drag){ ring.style.setProperty('--ry',(r0+(e.clientX-x0)*.45)+'deg'); return; }
    st.style.setProperty('--tx',(((e.clientY-r.top)/r.height-.5)*-8).toFixed(2)+'deg');
    ring.style.setProperty('--ry',(((e.clientX-r.left)/r.width-.5)*18).toFixed(2)+'deg');
  });
  ['pointerup','pointercancel'].forEach(function(t){ st.addEventListener(t, function(){ drag=false; }); });
  st.addEventListener('pointerleave', function(){
    drag=false;
    st.style.setProperty('--tx','0deg');
    ring.style.setProperty('--ry','0deg');
  });
})();
</script>

"""

B["/integrasi"] = """
<div class="wrap pghead"><div class="kick">15 · Integrasi</div>
<h1>Layanan yang biasa <em>disambungkan</em>.</h1>
<p class="lead">Integrasi menambah waktu dan biaya uji. Semuanya butuh kredensial dari pihak Anda.</p></div>
<section><div class="wrap"><div class="grid">
  <div class="cell rv"><div class="ic"><i class="fas fa-credit-card"></i></div><h3>Payment Gateway</h3><p>Midtrans, Xendit, Tripay. Butuh akun merchant terverifikasi.</p></div>
  <div class="cell rv"><div class="ic"><i class="fab fa-whatsapp"></i></div><h3>WhatsApp API</h3><p>Pesan transaksional dan verifikasi nomor.</p></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-location-dot"></i></div><h3>Peta</h3><p>Alamat, rute, dan penentuan ongkir.</p></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-truck"></i></div><h3>Kurir</h3><p>Cek ongkir dan pembuatan resi otomatis.</p></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-envelope"></i></div><h3>Email Transaksional</h3><p>Notifikasi, reset sandi, dan bukti pesanan.</p></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-calculator"></i></div><h3>Sistem Akuntansi</h3><p>Sinkron jurnal dan stok.</p></div>
</div>
<p class="rv" style="margin-top:20px;font-size:12px;color:var(--dim);border-left:1px solid var(--gold);padding-left:16px">Semua kredensial disimpan sebagai variabel lingkungan, tidak pernah ditulis langsung di kode.</p>
</div></section>
"""

B["/hosting"] = """
<div class="wrap pghead"><div class="kick">16 · Infrastruktur</div>
<h1>Server dan <em>topologi penyebaran</em>.</h1>
<p class="lead">Situs ini sendiri berjalan tanpa basis data dan tanpa dependensi, sehingga permukaan serangnya kecil.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Lapisan</th><th>Pilihan</th><th>Catatan</th></tr>
  <tr><td>Web server</td><td>Nginx / Caddy</td><td>reverse proxy, TLS otomatis pada Caddy</td></tr>
  <tr><td>TLS</td><td>Let's Encrypt</td><td>perpanjangan otomatis</td></tr>
  <tr><td>Proses</td><td>systemd</td><td>mulai ulang otomatis bila mati</td></tr>
  <tr><td>Basis data</td><td>PostgreSQL / MySQL</td><td>hanya bila proyek butuh</td></tr>
  <tr><td>Berkas</td><td>object storage</td><td>dipisah dari server aplikasi</td></tr>
  <tr><td>Cache</td><td>Redis</td><td>sesi dan antrean</td></tr>
</table>
<p class="rv" style="margin-top:20px;font-size:12px;color:var(--dim)">VPS dipilih dengan RAM minimal dua kali kebutuhan puncak. Pemantauan uptime aktif sejak hari pertama.</p>
</div></section>
"""

B["/maintenance"] = """
<div class="wrap pghead"><div class="kick">17 · Perawatan</div>
<h1>Rawat bulanan, <em>cakupan jelas</em>.</h1>
<p class="lead">Perangkat lunak yang dibiarkan tanpa perawatan akan menua. Paket ini menjaga tetap aman dan mutakhir.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Kegiatan</th><th>Frekuensi</th></tr>
  <tr><td>Cadangan penuh</td><td>harian</td></tr>
  <tr><td>Uji pemulihan cadangan</td><td>bulanan</td></tr>
  <tr><td>Pembaruan keamanan</td><td>mingguan</td></tr>
  <tr><td>Pemeriksaan log anomali</td><td>mingguan</td></tr>
  <tr><td>Pembaruan dependensi</td><td>bulanan</td></tr>
  <tr><td>Jam kerja perubahan kecil</td><td>2 jam/bulan</td></tr>
</table>
<div class="cta rv" style="margin-top:26px"><h2>Rp 400.000 / bulan</h2>
<p>Bisa dihentikan kapan saja dengan pemberitahuan 14 hari. Cadangan diserahkan sebelum penghentian.</p>
<div class="row"><a href="__WA__?text=Halo__saya__mau__maintenance" class="btn solid" target="_blank" rel="noopener">Ambil Perawatan</a></div></div>
</div></section>
"""

B["/garansi"] = """
<div class="wrap pghead"><div class="kick">18 · Garansi</div>
<h1>Ditanggung dan <em>tidak ditanggung</em>.</h1>
<p class="lead">Ditulis tegas supaya tidak jadi perdebatan saat kejadian.</p></div>
<section><div class="wrap"><div class="grid">
  <div class="cell rv"><div class="ic"><i class="fas fa-check"></i></div><h3>Ditanggung</h3><p>Bug dari kode yang saya tulis, error tampilan, kegagalan fungsi sesuai brief.</p></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-xmark"></i></div><h3>Tidak ditanggung</h3><p>Fitur baru, perubahan brief, kerusakan akibat kelalaian pihak ketiga, salah konfigurasi oleh klien.</p></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-clock"></i></div><h3>Waktu tanggap</h3><p>Laporan bug kritis dibalas dalam 24 jam, non-kritis 3 hari kerja.</p></div>
</div>
<p class="rv" style="margin-top:20px;font-size:12px;color:var(--dim)">Garansi batal bila kode diubah pihak lain tanpa pemberitahuan.</p>
</div></section>
"""

B["/legal"] = """
<div class="wrap pghead"><div class="kick">19 · Legal</div>
<h1>Dokumen kerja <em>yang dipakai</em>.</h1>
<p class="lead">Semua ditandatangani sebelum pengerjaan. Tidak ada yang mengikat secara lisan saja.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Dokumen</th><th>Isi</th></tr>
  <tr><td>Surat pesanan</td><td>Lingkup, harga, tanggal, batas revisi</td></tr>
  <tr><td>NDA</td><td>Kerahasiaan dua arah, berlaku 2 tahun</td></tr>
  <tr><td>Pengalihan hak</td><td>Kepemilikan kode setelah pelunasan</td></tr>
  <tr><td>Berita acara</td><td>Serah terima dan pengujian bersama</td></tr>
</table>
<p class="rv" style="margin-top:20px;font-size:12px;color:var(--dim)">Sengketa diselesaikan secara musyawarah lebih dulu. Bila buntu, memakai jalur yang disepakati di surat pesanan.</p>
</div></section>
"""

B["/privasi"] = """
<div class="wrap pghead"><div class="kick">20 · Privasi</div>
<h1>Data yang <em>dikumpulkan situs ini</em>.</h1>
<p class="lead">Sesedikit mungkin. Situs ini tidak memakai pelacak iklan dan tidak memasang kuki analitik.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Data</th><th>Perlakuan</th></tr>
  <tr><td>Alamat IP</td><td>Dibaca untuk pembatasan permintaan, disimpan di memori</td></tr>
  <tr><td>Pilihan tema</td><td>Disimpan di perangkat, tidak dikirim ke mana pun</td></tr>
  <tr><td>Pesan WhatsApp</td><td>Diproses oleh WhatsApp, bukan oleh server ini</td></tr>
  <tr><td>Kuki</td><td>Tidak ada kuki pelacak</td></tr>
</table>
<p class="rv" style="margin-top:20px;font-size:12px;color:var(--dim)">Log akses server hilang saat proses dimulai ulang. Tidak ada basis data pengguna.</p>
</div></section>
"""

B["/syarat"] = """
<div class="wrap pghead"><div class="kick">21 · Syarat</div>
<h1>Ketentuan <em>pemakaian layanan</em>.</h1>
<p class="lead">Berlaku bagi siapa pun yang memakai situs dan jasa di dalamnya.</p></div>
<section><div class="wrap"><div class="grid">
  <div class="cell rv"><h3>Boleh</h3><p>Membaca, membagikan tautan, dan mengutip dengan atribusi.</p></div>
  <div class="cell rv"><h3>Perlu izin</h3><p>Menyalin utuh tampilan atau kode untuk dijual kembali.</p></div>
  <div class="cell rv"><h3>Tidak dijanjikan</h3><p>Ketersediaan tanpa henti, kecocokan untuk tujuan tertentu di luar brief.</p></div>
</div>
<p class="rv" style="margin-top:20px;font-size:12px;color:var(--dim)">Ketentuan dapat berubah; versi berlaku adalah yang tertera di halaman ini.</p>
</div></section>
"""

B["/catatan"] = """
<div class="wrap pghead"><div class="kick">22 · Catatan</div>
<h1>Tulisan pendek <em>soal praktik kerja</em>.</h1>
<p class="lead">Bukan blog pemasaran. Isinya hal teknis yang sering salah dikerjakan.</p></div>
<section><div class="wrap">
  <details class="rv"><summary>Kenapa estimasi sengaja dilonggarkan</summary><div class="bd"><div><p>Estimasi ketat menjual lebih mudah, tetapi merusak kepercayaan saat meleset. Longgar sedikit dan selesai lebih cepat terasa jauh lebih baik daripada sebaliknya.</p></div></div></details>
  <details class="rv"><summary>Kenapa source code diserahkan</summary><div class="bd"><div><p>Klien yang tersandera akan menyebar kabar buruk. Menyerahkan kode justru memicu rujukan.</p></div></div></details>
  <details class="rv"><summary>Kenapa tidak memakai page builder berat</summary><div class="bd"><div><p>Plugin bertumpuk memperlambat situs dan menambah celah. Situs ini sendiri berjalan tanpa satu pun dependensi Python.</p></div></div></details>
  <details class="rv"><summary>Kenapa revisi dibatasi</summary><div class="bd"><div><p>Revisi tanpa batas membuat proyek tidak pernah selesai. Batas jelas justru mempercepat peluncuran.</p></div></div></details>
</div></section>
"""

B["/glosarium"] = """
<div class="wrap pghead"><div class="kick">23 · Glosarium</div>
<h1>Istilah yang <em>sering membingungkan</em>.</h1>
<p class="lead">Supaya brief tidak salah tafsir.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Istilah</th><th>Arti</th></tr>
  <tr><td>Brief</td><td>Dokumen kebutuhan proyek</td></tr>
  <tr><td>Mockup</td><td>Rancangan tampilan sebelum dikode</td></tr>
  <tr><td>Staging</td><td>Salinan situs untuk uji, bukan untuk publik</td></tr>
  <tr><td>Deploy</td><td>Memasang versi baru ke server</td></tr>
  <tr><td>Rate limit</td><td>Batas jumlah permintaan per waktu</td></tr>
  <tr><td>CSP</td><td>Kebijakan yang membatasi sumber skrip dan gaya</td></tr>
  <tr><td>HSTS</td><td>Paksa koneksi memakai HTTPS</td></tr>
  <tr><td>IDOR</td><td>Akses data milik orang lain lewat penomoran</td></tr>
  <tr><td>SLA</td><td>Janji tingkat layanan</td></tr>
  <tr><td>Cross-platform</td><td>Satu kode untuk dua sistem</td></tr>
</table></div></section>
"""

B["/checklist"] = """
<div class="wrap pghead"><div class="kick">24 · Checklist</div>
<h1>Diperiksa <em>sebelum peluncuran</em>.</h1>
<p class="lead">Tidak ada proyek naik tanpa melewati daftar ini.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Pemeriksaan</th><th>Ambang</th></tr>
  <tr><td>Skor performa seluler</td><td>di atas 85</td></tr>
  <tr><td>Ukuran halaman awal</td><td>di bawah 1 MB</td></tr>
  <tr><td>Gambar terkompresi</td><td>wajib</td></tr>
  <tr><td>Alt teks gambar</td><td>wajib</td></tr>
  <tr><td>Kontras teks</td><td>rasio minimal 4,5</td></tr>
  <tr><td>Header keamanan</td><td>lengkap</td></tr>
  <tr><td>Formulir tervalidasi</td><td>sisi klien dan server</td></tr>
  <tr><td>Cadangan awal</td><td>sudah dibuat</td></tr>
  <tr><td>Pemantauan uptime</td><td>aktif</td></tr>
  <tr><td>robots.txt dan sitemap</td><td>tersedia</td></tr>
</table></div></section>
"""

B["/roadmap"] = """
<div class="wrap pghead"><div class="kick">25 · Roadmap Celah</div>
<h1>Penambalan celah, <em>dijadwalkan per minggu</em>.</h1>
<p class="lead">Standar internal yang diterapkan ke setiap proyek. Delapan minggu, urut dari paling berbahaya. Panah menandai celah yang sedang ditutup.</p></div>
<section><div class="wrap"><div class="weeks">
  <div class="wk flag"><span class="wn">MINGGU 1</span><span class="st done">SELESAI</span>
    <h4>Header dan TLS</h4><p>CSP, HSTS, X-Frame-Options, Permissions-Policy, paksa HTTPS.</p>
    <div class="track"><i data-w="100"></i></div><span class="arrow"><i class="fas fa-arrow-up-right-from-square"></i></span></div>
  <div class="wk"><span class="wn">MINGGU 2</span><span class="st done">SELESAI</span>
    <h4>Autentikasi</h4><p>Hash argon2, batas percobaan masuk, MFA opsional, kunci sesi.</p>
    <div class="track"><i data-w="100"></i></div></div>
  <div class="wk"><span class="wn">MINGGU 3</span><span class="st run">BERJALAN</span>
    <h4>Validasi masukan</h4><p>Query berparameter, sanitasi keluaran, validasi tipe di server.</p>
    <div class="track"><i data-w="68"></i></div><span class="arrow"><i class="fas fa-arrow-up-right-from-square"></i></span></div>
  <div class="wk"><span class="wn">MINGGU 4</span><span class="st plan">RENCANA</span>
    <h4>Otorisasi</h4><p>Pemeriksaan kepemilikan per objek untuk menutup IDOR.</p>
    <div class="track"><i data-w="0"></i></div></div>
  <div class="wk"><span class="wn">MINGGU 5</span><span class="st plan">RENCANA</span>
    <h4>Unggah berkas</h4><p>Validasi MIME, batas ukuran, simpan di luar webroot, ganti nama.</p>
    <div class="track"><i data-w="0"></i></div></div>
  <div class="wk"><span class="wn">MINGGU 6</span><span class="st plan">RENCANA</span>
    <h4>Pembatasan</h4><p>Rate limit per IP dan akun, proteksi bot pada formulir.</p>
    <div class="track"><i data-w="0"></i></div></div>
  <div class="wk"><span class="wn">MINGGU 7</span><span class="st plan">RENCANA</span>
    <h4>Cadangan</h4><p>Cadangan harian, uji pemulihan, rotasi kunci berkala.</p>
    <div class="track"><i data-w="0"></i></div></div>
  <div class="wk"><span class="wn">MINGGU 8</span><span class="st plan">RENCANA</span>
    <h4>Pemantauan</h4><p>Log anomali, peringatan otomatis, tinjauan dependensi.</p>
    <div class="track"><i data-w="0"></i></div></div>
</div>
<div class="cta rv" style="margin-top:28px"><h2>Minta jadwal untuk proyek Anda</h2>
<p>Roadmap disesuaikan dengan tumpukan teknologi dan risiko masing-masing proyek.</p>
<div class="row"><a href="__WA__?text=Halo__saya__mau__roadmap__celah" class="btn solid" target="_blank" rel="noopener">Minta Jadwal</a><a href="/keamanan" class="btn ghost">Cakupan Audit</a></div></div>
</div></section>
"""

B["/kapasitas"] = """
<div class="wrap pghead"><div class="kick">26 · Kapasitas</div>
<h1>Berapa proyek <em>berjalan bersamaan</em>.</h1>
<p class="lead">Dibatasi sengaja. Mengambil terlalu banyak membuat semuanya lambat.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Jenis</th><th>Bersamaan</th></tr>
  <tr><td>Proyek besar</td><td>1</td></tr>
  <tr><td>Proyek sedang</td><td>2</td></tr>
  <tr><td>Perbaikan kecil</td><td>3</td></tr>
  <tr><td>Audit keamanan</td><td>2</td></tr>
</table>
<p class="rv" style="margin-top:20px;font-size:12px;color:var(--dim)">Bila slot penuh, proyek baru masuk daftar tunggu dan tanggal mulai diberitahukan apa adanya.</p>
</div></section>
"""

B["/mitra"] = """
<div class="wrap pghead"><div class="kick">27 · Mitra</div>
<h1>Kolaborasi dan <em>rujukan silang</em>.</h1>
<p class="lead">Bila kebutuhan di luar kemampuan saya, diteruskan ke rekan yang tepat tanpa biaya perantara.</p></div>
<section><div class="wrap"><div class="grid">
  <div class="cell rv"><div class="ic"><i class="fas fa-pen-nib"></i></div><h3>Penulisan Naskah</h3><p>Naskah situs dan artikel rujukan.</p></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-camera"></i></div><h3>Fotografi Produk</h3><p>Foto katalog dan suasana tempat usaha.</p></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-bullhorn"></i></div><h3>Iklan Berbayar</h3><p>Pengelolaan kampanye setelah situs siap.</p></div>
</div>
<p class="rv" style="margin-top:20px;font-size:12px;color:var(--dim)">Nama mitra diberikan setelah brief dibaca, supaya rekomendasinya benar-benar cocok.</p>
</div></section>
"""

B["/kolaborasi"] = """
<div class="wrap pghead"><div class="kick">28 · Kolaborasi</div>
<h1>Peluang kerja sama <em>jangka panjang</em>.</h1>
<p class="lead">Terbuka untuk studio, agensi, dan freelancer yang butuh tenaga pengembang.</p></div>
<section><div class="wrap"><div class="grid">
  <div class="cell rv"><h3>Subkontrak</h3><p>Mengerjakan bagian teknis dari proyek Anda dengan NDA.</p></div>
  <div class="cell rv"><h3>Putih Label</h3><p>Hasil kerja tanpa nama, dipasarkan atas merek Anda.</p></div>
  <div class="cell rv"><h3>Bagi Hasil</h3><p>Untuk produk yang dikelola bersama.</p></div>
</div>
<div class="cta rv" style="margin-top:26px"><h2>Ajukan kerja sama</h2>
<p>Sertakan jenis proyek, volume, dan rentang waktu.</p>
<div class="row"><a href="__WA__?text=Halo__saya__mau__kolaborasi" class="btn solid" target="_blank" rel="noopener">Hubungi</a></div></div>
</div></section>
"""

B["/status"] = """
<div class="wrap pghead"><div class="kick">29 · Status</div>
<h1>Kondisi <em>node</em>.</h1>
<p class="lead">Situs ini dilayani dari satu proses tanpa basis data. Riwayat kejadian dicatat terbuka.</p></div>
<section><div class="wrap"><div class="grid">
  <div class="cell rv"><div class="ic"><i class="fas fa-circle-check"></i></div><h3>Operasional</h3><p>Seluruh 114 ruang dilayani normal.</p></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-gauge-high"></i></div><h3>Batas Permintaan</h3><p>90 permintaan per menit per alamat IP.</p></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-database"></i></div><h3>Basis Data</h3><p>Tidak dipakai. Tidak ada penyimpanan data pengguna.</p></div>
</div>
<table class="tbl rv" style="margin-top:26px"><tr><th>Waktu</th><th>Kejadian</th></tr>
  <tr><td>Hari ini</td><td>Peluncuran v5, 30 ruang aktif</td></tr>
  <tr><td>Sebelumnya</td><td>Pengerasan header dan pembatasan permintaan</td></tr>
  <tr><td>Awal</td><td>Rilis pertama, 1 halaman</td></tr>
</table></div></section>
"""

B["/dokumentasi"] = """
<div class="wrap pghead"><div class="kick">30 · Dokumentasi</div>
<h1>Struktur berkas <em>dan rute</em>.</h1>
<p class="lead">Dibuka supaya siapa pun bisa memeriksa sebelum memesan.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Berkas</th><th>Isi</th></tr>
  <tr><td>app.py</td><td>Server, rute, dan seluruh isi halaman</td></tr>
  <tr><td>start.sh</td><td>Menjalankan di latar belakang</td></tr>
  <tr><td>stop.sh</td><td>Menghentikan proses</td></tr>
  <tr><td>export.py</td><td>Mengekspor versi statis untuk Pages</td></tr>
</table>
<h2 class="rv" style="margin-top:30px">Rute</h2><div class="hr rv"></div>
<p class="rv" style="font-size:12.6px;color:var(--muted)">114 rute halaman, ditambah <span class="mono">/health</span>, <span class="mono">/robots.txt</span>, dan <span class="mono">/sitemap.xml</span>. Rute di luar daftar dijawab 404 tanpa membuka direktori.</p>
<div style="margin-top:24px"><a href="https://github.com/yuana448/alfiliator-landing" class="btn ghost" target="_blank" rel="noopener">Lihat Repositori</a></div>
</div></section>
"""



B["/kualitas"] = r"""
<div class="wrap pghead"><div class="kick">35 · Kualitas</div>
<h1>Standar yang dipakai <em>sebelum kode ditulis</em>.</h1>
<p class="lead">Kualitas bukan selera. Isinya ambang terukur yang disepakati di brief, lalu diperiksa sebelum peluncuran.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Aspek</th><th>Ambang</th><th>Alat</th></tr>
  <tr><td>Kontras teks</td><td>minimal 4,5:1</td><td>pemeriksa kontras</td></tr>
  <tr><td>Ukuran target sentuh</td><td>minimal 24×24 px</td><td>tinjau manual</td></tr>
  <tr><td>Skor performa seluler</td><td>di atas 85</td><td>Lighthouse</td></tr>
  <tr><td>Kesalahan konsol</td><td>nol</td><td>uji peramban</td></tr>
  <tr><td>Gambar tanpa alt</td><td>nol</td><td>lint HTML</td></tr>
  <tr><td>Ukuran halaman awal</td><td>di bawah 1 MB</td><td>ukur transfer</td></tr>
</table>
<div class="cta rv" style="margin-top:26px"><h2>Minta ambang untuk proyek Anda</h2>
<p>Ambang disesuaikan dengan jenis produk dan penggunanya, lalu dikunci di dokumen kerja.</p>
<div class="row"><a href="__WA__?text=Halo__mau__bahas__kualitas" class="btn solid" target="_blank" rel="noopener">Diskusikan</a></div></div>
</div></section>
"""

B["/pengujian"] = r"""
<div class="wrap pghead"><div class="kick">36 · Pengujian</div>
<h1>Diuji <em>sebelum diserahkan</em>.</h1>
<p class="lead">Tiga lapis: fungsi, beban, dan perangkat. Hasil uji diserahkan sebagai berkas, bukan lisan.</p></div>
<section><div class="wrap"><div class="steps">
  <div class="step rv"><h3>Uji fungsi</h3><p>Setiap alur di brief punya skenario lulus dan gagal. Bug dicatat, diperbaiki, lalu diuji ulang.</p></div>
  <div class="step rv"><h3>Uji beban</h3><p>Permintaan bersamaan dinaikkan bertahap sampai ambang gagal, lalu hasilnya dicatat.</p></div>
  <div class="step rv"><h3>Uji perangkat</h3><p>Layar sempit, sedang, dan lebar; dua peramban; mode gelap dan terang.</p></div>
</div>
<table class="tbl rv" style="margin-top:24px"><tr><th>Yang tidak diklaim</th><th>Alasan</th></tr>
  <tr><td>Bebas bug sepenuhnya</td><td>tidak ada perangkat lunak yang demikian</td></tr>
  <tr><td>Lulus semua peramban lama</td><td>dua versi terakhir saja yang dijamin</td></tr>
  <tr><td>Uji penetrasi penuh</td><td>itu cakupan audit terpisah</td></tr>
</table>
</div></section>
"""

B["/aksesibilitas"] = r"""
<div class="wrap pghead"><div class="kick">37 · Aksesibilitas</div>
<h1>Bisa dipakai <em>semua orang</em>.</h1>
<p class="lead">Mengikuti WCAG 2.2 level AA. Target sentuh minimal 24×24 piksel, kontras teks minimal 4,5:1, dan seluruh fungsi bisa dicapai lewat papan ketik.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Kriteria</th><th>Penerapan</th></tr>
  <tr><td>Ukuran target (2.5.8)</td><td>minimal 24×24 px atau jarak memadai</td></tr>
  <tr><td>Kontras (1.4.3)</td><td>minimal 4,5:1 untuk teks biasa</td></tr>
  <tr><td>Fokus terlihat (2.4.7)</td><td>garis fokus 2 px, bukan outline bawaan</td></tr>
  <tr><td>Lompat ke isi (2.4.1)</td><td>tautan skip di awal dokumen</td></tr>
  <tr><td>Gerak bisa dimatikan (2.3.3)</td><td>setelan animasi di panel</td></tr>
  <tr><td>Nama aksesibel (4.1.2)</td><td>label pada setiap tombol ikon</td></tr>
</table>
<p class="rv" style="margin-top:18px;font-size:12px;color:var(--dim);border-left:1px solid var(--gold);padding-left:16px">Situs ini punya mode kontras tinggi dan ukuran huruf tiga tingkat. Keduanya di panel setelan.</p>
</div></section>
"""

B["/performa"] = r"""
<div class="wrap pghead"><div class="kick">38 · Performa</div>
<h1>Anggaran muat, <em>ditulis di depan</em>.</h1>
<p class="lead">Kecepatan bukan tambahan di akhir. Angkanya masuk anggaran dan diuji sebelum rilis.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Metrik</th><th>Ambang</th></tr>
  <tr><td>LCP</td><td>di bawah 2,5 detik</td></tr>
  <tr><td>CLS</td><td>di bawah 0,1</td></tr>
  <tr><td>INP</td><td>di bawah 200 ms</td></tr>
  <tr><td>Ukuran awal</td><td>di bawah 1 MB</td></tr>
  <tr><td>Permintaan awal</td><td>di bawah 40</td></tr>
</table>
<h2 class="rv" style="margin-top:30px">Cara menekan</h2><div class="hr rv"></div>
<div class="grid">
  <div class="cell rv"><h3>Gambar</h3><p>WebP, ukuran sesuai tampil, muat bertahap.</p></div>
  <div class="cell rv"><h3>Skrip</h3><p>Tanpa pustaka berat, dimuat setelah isi utama.</p></div>
  <div class="cell rv"><h3>Font</h3><p>Dua keluarga, subset latin, preconnect.</p></div>
</div>
</div></section>
"""

B["/seo"] = r"""
<div class="wrap pghead"><div class="kick">39 · SEO</div>
<h1>Struktur yang <em>terbaca mesin</em>.</h1>
<p class="lead">Tanpa jasa backlink. Yang dikerjakan hanya hal teknis yang memang di bawah kendali pengembang.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Pekerjaan</th><th>Keterangan</th></tr>
  <tr><td>Canonical</td><td>satu URL resmi per halaman</td></tr>
  <tr><td>Judul dan deskripsi</td><td>unik, panjang wajar</td></tr>
  <tr><td>Data terstruktur</td><td>JSON-LD jenis usaha</td></tr>
  <tr><td>Sitemap dan robots</td><td>keduanya tersedia dan benar</td></tr>
  <tr><td>Heading</td><td>satu H1, urutan tanpa lompatan</td></tr>
  <tr><td>404</td><td>status benar, bukan pengalihan diam</td></tr>
</table>
<p class="rv" style="margin-top:18px;font-size:12px;color:var(--dim)">Peringkat tetap ditentukan konten dan tautan masuk. Klaim halaman satu tanpa itu tidak jujur.</p>
</div></section>
"""

B["/analitik"] = r"""
<div class="wrap pghead"><div class="kick">40 · Analitik</div>
<h1>Ukur tanpa <em>pelacak iklan</em>.</h1>
<p class="lead">Yang dicatat hanya kejadian yang berguna. Tidak ada kuki pihak ketiga, tidak ada profil pengunjung.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Kejadian</th><th>Guna</th></tr>
  <tr><td>Kunjungan halaman</td><td>tahu halaman yang dibaca</td></tr>
  <tr><td>Klik WhatsApp</td><td>tahu niat menghubungi</td></tr>
  <tr><td>Klik tarif</td><td>tahu minat harga</td></tr>
  <tr><td>Pengiriman brief</td><td>tahu ujung corong</td></tr>
</table>
<div class="grid rv" style="margin-top:24px">
  <div class="cell rv"><h3>Tanpa kuki</h3><p>Bisa dipasang tanpa spanduk persetujuan.</p></div>
  <div class="cell rv"><h3>Ringan</h3><p>Di bawah 2 KB, tanpa memblokir render.</p></div>
  <div class="cell rv"><h3>Milik Anda</h3><p>Data di akun Anda sendiri, bisa diekspor.</p></div>
</div>
</div></section>
"""

B["/konten"] = r"""
<div class="wrap pghead"><div class="kick">41 · Konten</div>
<h1>Naskah yang dibaca <em>manusia dan mesin</em>.</h1>
<p class="lead">Kalimat pendek, satu gagasan per paragraf, kata kerja jelas. Tanpa jargon pemasaran.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Aturan</th><th>Contoh salah</th><th>Perbaikan</th></tr>
  <tr><td>Satu gagasan per paragraf</td><td>paragraf empat kalimat campur</td><td>pecah jadi tiga</td></tr>
  <tr><td>Kalimat aktif</td><td>situs akan dikerjakan oleh kami</td><td>kami mengerjakan situs</td></tr>
  <tr><td>Angka konkret</td><td>pengerjaan cepat</td><td>selesai 7 hari kerja</td></tr>
  <tr><td>Tanpa klaim kosong</td><td>solusi terbaik nomor satu</td><td>muat 1,4 detik, terukur</td></tr>
</table>
<div class="cta rv" style="margin-top:26px"><h2>Butuh penulis naskah?</h2>
<p>Bila naskah disiapkan pihak lain, saya sesuaikan strukturnya agar tetap terbaca mesin.</p>
<div class="row"><a href="__WA__?text=Halo__soal__naskah" class="btn solid" target="_blank" rel="noopener">Tanya</a></div></div>
</div></section>
"""

B["/merek"] = r"""
<div class="wrap pghead"><div class="kick">42 · Merek</div>
<h1>Identitas yang <em>dipakai ulang</em>.</h1>
<p class="lead">Warna, huruf, dan jarak disimpan sebagai token. Perubahan satu tempat merambat konsisten, bukan diubah manual satu per satu.</p></div>
<section><div class="wrap"><div class="grid">
  <div class="cell rv"><h3>Token warna</h3><p>Variabel CSS, bukan kode warna tersebar.</p></div>
  <div class="cell rv"><h3>Skala huruf</h3><p>Tiga tingkat ukuran, tanpa nilai acak.</p></div>
  <div class="cell rv"><h3>Jarak</h3><p>Kelipatan tetap supaya rapi.</p></div>
</div>
<table class="tbl rv" style="margin-top:24px"><tr><th>Diserahkan</th><th>Bentuk</th></tr>
  <tr><td>Logo</td><td>SVG, versi terang dan gelap</td></tr>
  <tr><td>Palet</td><td>berkas token</td></tr>
  <tr><td>Aturan pakai</td><td>satu halaman ringkas</td></tr>
</table>
</div></section>
"""

B["/handover"] = r"""
<div class="wrap pghead"><div class="kick">43 · Serah Terima</div>
<h1>Diserahkan <em>utuh</em>, bukan setengah.</h1>
<p class="lead">Serah terima punya daftar periksa sendiri. Tidak ada kredensial yang tertahan setelah pelunasan.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Item</th><th>Keterangan</th></tr>
  <tr><td>Repositori</td><td>riwayat commit lengkap</td></tr>
  <tr><td>Kredensial</td><td>diserahkan lewat pengelola sandi</td></tr>
  <tr><td>Berkas desain</td><td>sumber, bukan hanya gambar</td></tr>
  <tr><td>Dokumentasi</td><td>cara pasang, cara cadangkan</td></tr>
  <tr><td>Hasil uji</td><td>berkas, termasuk yang gagal</td></tr>
  <tr><td>Berita acara</td><td>ditandatangani kedua pihak</td></tr>
</table>
<p class="rv" style="margin-top:18px;font-size:12px;color:var(--dim)">Garansi berjalan setelah berita acara ditandatangani, bukan setelah kode dikirim.</p>
</div></section>
"""

B["/pelatihan"] = r"""
<div class="wrap pghead"><div class="kick">44 · Pelatihan</div>
<h1>Tim Anda <em>bisa memakainya sendiri</em>.</h1>
<p class="lead">Satu sesi rekaman dan satu sesi tanya jawab. Materi tertulis, bukan hanya lisan.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Sesi</th><th>Isi</th><th>Durasi</th></tr>
  <tr><td>Dasar</td><td>masuk, peran, alur utama</td><td>60 menit</td></tr>
  <tr><td>Admin</td><td>kelola konten, pesanan, laporan</td><td>60 menit</td></tr>
  <tr><td>Tanya jawab</td><td>bebas, direkam</td><td>45 menit</td></tr>
</table>
<p class="rv" style="margin-top:18px;font-size:12px;color:var(--dim)">Tambahan di luar jadwal dihitung Rp 1.250.000 per sesi.</p>
</div></section>
"""

B["/eskalasi"] = r"""
<div class="wrap pghead"><div class="kick">45 · Eskalasi</div>
<h1>Kalau ada yang <em>rusak</em>.</h1>
<p class="lead">Jalur lapor dan waktu tanggap ditulis, bukan dijanjikan di percakapan.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Tingkat</th><th>Contoh</th><th>Tanggap</th></tr>
  <tr><td><span class="sev c">KRITIS</span></td><td>situs mati, pembayaran gagal</td><td>2 jam</td></tr>
  <tr><td><span class="sev h">TINGGI</span></td><td>fitur utama tidak jalan</td><td>12 jam</td></tr>
  <tr><td><span class="sev m">SEDANG</span></td><td>tampilan rusak, salah teks</td><td>2 hari kerja</td></tr>
  <tr><td><span class="sev l">RENDAH</span></td><td>permintaan perubahan kecil</td><td>5 hari kerja</td></tr>
</table>
<div class="cta rv" style="margin-top:26px"><h2>Laporkan insiden</h2>
<p>Sertakan URL, waktu kejadian, dan tangkapan layar bila ada.</p>
<div class="row"><a href="__WA__?text=INSIDEN" class="btn solid" target="_blank" rel="noopener">WhatsApp</a><a href="/kontak" class="btn ghost">Kanal Lain</a></div></div>
</div></section>
"""

B["/retainer"] = r"""
<div class="wrap pghead"><div class="kick">46 · Retainer</div>
<h1>Kerja sama <em>bulanan</em>.</h1>
<p class="lead">Untuk produk yang terus berjalan. Jam kerja disepakati di muka dan bisa dipakai untuk perbaikan maupun pengembangan kecil.</p></div>
<section><div class="wrap"><div class="plans">
  <div class="plan"><h3>Ringan</h3><div class="price">Rp 1.500.000<small>per bulan</small></div>
    <ul><li><i class="fas fa-check"></i>4 jam kerja</li><li><i class="fas fa-check"></i>Cadangan harian</li><li><i class="fas fa-check"></i>Tanggap 2 hari</li></ul></div>
  <div class="plan hot"><span class="tag">PALING DIPILIH</span><h3>Teratur</h3><div class="price">Rp 3.500.000<small>per bulan</small></div>
    <ul><li><i class="fas fa-check"></i>10 jam kerja</li><li><i class="fas fa-check"></i>Cadangan harian + uji pulih</li><li><i class="fas fa-check"></i>Tanggap 12 jam</li><li><i class="fas fa-check"></i>Laporan bulanan</li></ul></div>
  <div class="plan"><h3>Penuh</h3><div class="price">Rp 7.000.000<small>per bulan</small></div>
    <ul><li><i class="fas fa-check"></i>24 jam kerja</li><li><i class="fas fa-check"></i>Pemantauan aktif</li><li><i class="fas fa-check"></i>Tanggap 4 jam</li><li><i class="fas fa-check"></i>Prioritas antrean</li></ul></div>
</div>
<p class="rv" style="margin-top:18px;font-size:12px;color:var(--dim)">Jam yang tidak terpakai hangus di akhir bulan, kecuali disepakati lain. Bisa dihentikan dengan pemberitahuan 14 hari.</p>
</div></section>
"""

B["/anggaran"] = r"""
<div class="wrap pghead"><div class="kick">47 · Anggaran</div>
<h1>Susun angka <em>sebelum menghubungi</em>.</h1>
<p class="lead">Anggaran yang jelas mempersempit pilihan dan mempercepat penawaran. Ini cara menyusunnya.</p></div>
<section><div class="wrap"><div class="steps">
  <div class="step rv"><h3>Pisahkan wajib dan tambahan</h3><p>Fitur wajib menentukan paket. Sisanya masuk tahap dua.</p></div>
  <div class="step rv"><h3>Sisakan biaya pihak ketiga</h3><p>Domain, hosting, akun store, dan kunci API dibayar terpisah.</p></div>
  <div class="step rv"><h3>Sisakan perawatan</h3><p>Perkirakan 15 sampai 25 persen nilai proyek per tahun untuk rawat.</p></div>
</div>
<table class="tbl rv" style="margin-top:24px"><tr><th>Kisaran</th><th>Yang realistis didapat</th></tr>
  <tr><td>di bawah Rp 3 juta</td><td>satu halaman landing</td></tr>
  <tr><td>Rp 5–10 juta</td><td>situs profil atau toko ringkas</td></tr>
  <tr><td>Rp 15–30 juta</td><td>aplikasi mobile satu platform</td></tr>
  <tr><td>di atas Rp 30 juta</td><td>sistem custom atau lintas platform</td></tr>
</table>
</div></section>
"""

B["/risiko"] = r"""
<div class="wrap pghead"><div class="kick">48 · Risiko</div>
<h1>Yang bisa gagal, <em>dan cara menutupnya</em>.</h1>
<p class="lead">Daftar ini dibuka supaya tidak jadi kejutan. Setiap risiko punya penanganan yang disepakati di brief.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Risiko</th><th>Dampak</th><th>Penanganan</th></tr>
  <tr><td>Materi klien terlambat</td><td>tanggal mundur</td><td>tenggat materi per tahap</td></tr>
  <tr><td>Lingkup melebar</td><td>biaya naik</td><td>surat pesanan baru</td></tr>
  <tr><td>Akun store ditolak</td><td>rilis tertunda</td><td>pendampingan review</td></tr>
  <tr><td>Kunci API bocor</td><td>biaya membengkak</td><td>rotasi dan batas pemakaian</td></tr>
  <tr><td>Kode diubah pihak lain</td><td>garansi batal</td><td>pemberitahuan sebelum ubah</td></tr>
  <tr><td>Penyedia layanan berhenti</td><td>fitur mati</td><td>jalur pindah disiapkan</td></tr>
</table>
</div></section>
"""

B["/kepatuhan"] = r"""
<div class="wrap pghead"><div class="kick">49 · Kepatuhan</div>
<h1>Kewajiban saat <em>menyimpan data pribadi</em>.</h1>
<p class="lead">Bila proyek mengumpulkan data pengguna, UU 27/2022 berlaku. Ini yang harus disiapkan sebelum rilis.</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Kewajiban</th><th>Penerapan</th></tr>
  <tr><td>Dasar pemrosesan</td><td>persetujuan eksplisit, dicatat</td></tr>
  <tr><td>Hak subjek data</td><td>akses, koreksi, hapus, portabilitas</td></tr>
  <tr><td>Pemberitahuan kebocoran</td><td>tertulis, maksimal 3×24 jam</td></tr>
  <tr><td>Bukti pemrosesan</td><td>log dan catatan persetujuan</td></tr>
  <tr><td>Petugas pelindungan data</td><td>untuk pengendali tertentu</td></tr>
</table>
<p class="rv" style="margin-top:18px;font-size:12px;color:var(--dim);border-left:1px solid var(--gold);padding-left:16px">Rujukan: UU Nomor 27 Tahun 2022, Pasal 46. Bukan nasihat hukum; untuk kasus khusus tetap perlu penasihat.</p>
<div class="cta rv" style="margin-top:24px"><h2>Minta daftar periksa kepatuhan</h2>
<p>Disusun mengikuti jenis data yang benar-benar dikumpulkan proyek Anda.</p>
<div class="row"><a href="__WA__?text=Halo__soal__kepatuhan" class="btn solid" target="_blank" rel="noopener">Minta</a></div></div>
</div></section>
"""

B["/cari"] = """
<div class="wrap pghead"><div class="kick">31 \u00b7 Cari</div>
<h1>Temukan <em>ruang</em>.</h1>
<p class="lead">Ketik kata kunci: harga, garansi, iOS, keamanan, kontrak.</p>
<input id="q" type="search" placeholder="Kata kunci..." autocomplete="off"
 style="width:100%;max-width:460px;margin-top:18px;padding:13px 16px;background:var(--panel);
 border:1px solid var(--line);color:var(--ink);font-family:inherit;font-size:13.5px">
<div id="out" class="rooms" style="margin-top:24px"></div></div>
<section><div class="wrap"><p id="hint" style="font-size:12.4px;color:var(--dim)">Mulai mengetik untuk menyaring 114 ruang.</p></div></section>
<script nonce="__NONCE__">
(function(){
  var idx=[],out=document.getElementById('out'),q=document.getElementById('q'),hint=document.getElementById('hint');
  fetch('/index.json').then(function(r){return r.json()}).then(function(d){idx=d}).catch(function(){});
  function run(){
    var t=q.value.toLowerCase().trim();
    out.innerHTML='';
    if(!t){hint.textContent='Mulai mengetik untuk menyaring 114 ruang.';return}
    var hit=idx.filter(function(x){return (x.t+' '+x.d+' '+x.k).toLowerCase().indexOf(t)>-1}).slice(0,12);
    hint.textContent=hit.length+' ruang cocok';
    hit.forEach(function(x){
      var a=document.createElement('a');a.className='room';a.href=x.u;
      a.innerHTML='<span class="no">'+x.u+'</span><h3>'+x.t+'</h3><p>'+x.d+'</p>';
      out.appendChild(a);
    });
  }
  q.addEventListener('input',run);
})();
</script>
"""

B["/struktur"] = r"""
<div class="wrap pghead"><div class="kick">31 · Struktur</div>
<h1>Alur permintaan, <em>lapisan demi lapisan</em>.</h1>
<p class="lead">Setiap permintaan melewati tujuh gerbang sebelum HTML keluar. Tidak ada satu pun yang dilewati, termasuk untuk halaman statis.</p></div>
<section><div class="wrap">
<div class="flow"><div class="pk"></div><div class="pk"></div>
  <div class="nd"><b>01 · KLIEN</b><span>permintaan masuk</span></div>
  <div class="nd"><b>02 · TLS + HSTS</b><span>paksa kanal terenkripsi</span></div>
  <div class="nd"><b>03 · BATAS LAJU</b><span>90/menit · burst 18/10 dtk</span></div>
  <div class="nd"><b>04 · VALIDASI JALUR</b><span>regex · tolak traversal · maks 120</span></div>
  <div class="nd"><b>05 · ROUTER</b><span>daftar rute eksplisit · 404 tertutup</span></div>
  <div class="nd"><b>06 · RENDER</b><span>nonce baru tiap permintaan</span></div>
  <div class="nd"><b>07 · HEADER</b><span>CSP · COOP · CORP · nosniff</span></div>
</div>
<div class="tel">
  <div><b id="t1" class="live">200</b><span>status</span></div>
  <div><b id="t2">0</b><span>dependensi python</span></div>
  <div><b id="t3">90</b><span>batas / menit</span></div>
  <div><b id="t4">0</b><span>basis data</span></div>
  <div><b id="t5">18</b><span>antrean puncak</span></div>
  <div><b id="t6">7</b><span>gerbang aktif</span></div>
</div>
<p style="margin-top:18px;font-size:12px;color:var(--dim);border-left:1px solid var(--gold);padding-left:16px">Angka bergerak di atas hanya simulasi tampilan. Nilai sebenarnya ada di <a href="/status" style="color:var(--gold)">Status</a> dan <a href="/keamanan" style="color:var(--gold)">Keamanan</a>.</p>
</div></section>
<section><div class="wrap"><h2>Yang tidak dipakai</h2><div class="hr"></div>
<div class="grid">
  <div class="cell"><h3>Tanpa framework</h3><p>Tidak ada paket pihak ketiga yang bisa usang atau bocor.</p></div>
  <div class="cell"><h3>Tanpa basis data</h3><p>Tidak ada data pengguna yang bisa dicuri.</p></div>
  <div class="cell"><h3>Tanpa sesi</h3><p>Tidak ada kuki yang perlu dijaga.</p></div>
</div>
<div class="cta" style="margin-top:24px"><h2>Minta diagram untuk proyek Anda</h2>
<p>Struktur disusun per proyek, mengikuti risiko dan tumpukan yang dipakai.</p>
<div class="row"><a href="__WA__?text=Halo__mau__diagram__struktur" class="btn solid" target="_blank" rel="noopener">Minta Diagram</a></div></div>
</div></section>
<script nonce="__NONCE__">
(function(){
  var t=document.getElementById('t1'),s=0;
  setInterval(function(){
    s=(s+1)%9;
    t.textContent=['200','200','200','304','200','200','429','200','200'][s];
    t.className=s===6?'':'live';
  },1400);
})();
</script>
"""

B["/reaper"] = r"""
<div class="wrap pghead"><div class="kick">32 · REAPER</div>
<h1>REAPER, <em>dua mode</em>.</h1>
<p class="lead">Mode lokal menjawab tanpa jaringan dan tanpa token. Mode Venice memakai kunci API Anda sendiri untuk jawaban bebas.</p></div>
<section><div class="wrap"><div class="grid">
  <div class="cell"><h3>Lokal — gratis selamanya</h3><p>Basis jawaban ikut terunduh. Jalan tanpa sinyal, tanpa kunci, tanpa batas.</p></div>
  <div class="cell"><h3>Venice — pakai kunci sendiri</h3><p>Kunci disimpan di perangkat, tidak dikirim ke server situs ini. Butuh jaringan.</p></div>
  <div class="cell"><h3>Tanpa perantara</h3><p>Mode Venice memanggil api.venice.ai langsung.</p></div>
</div>
<div class="cta" style="margin-top:26px"><h2>Coba sekarang</h2>
<p>Tanya "berapa harga toko online" di mode lokal, atau isi kunci di mode Venice.</p>
<div class="row"><a href="#" id="rpop" class="btn solid">Buka REAPER</a><a href="/harga" class="btn ghost">Lihat Tarif</a></div></div>
</div></section>
<section><div class="wrap"><h2>Cara dapat kunci Venice</h2><div class="hr"></div>
<table class="tbl"><tr><th>Langkah</th><th>Keterangan</th></tr>
  <tr><td>1</td><td>Masuk akun Venice, buka halaman API</td></tr>
  <tr><td>2</td><td>Buat kunci. Biarkan daftar IP kosong bila dipasang di GitHub Pages</td></tr>
  <tr><td>3</td><td>Tempel di mode Venice. Tersimpan hanya di perangkat Anda</td></tr>
</table>
<p style="margin-top:16px;font-size:12px;color:var(--dim);border-left:1px solid var(--gold);padding-left:16px">Kunci yang dibatasi IP akan ditolak 403 dari GitHub Pages.</p>
</div></section>
<section><div class="wrap"><h2>Supaya tetap gratis</h2><div class="hr"></div>
<div class="grid">
  <div class="cell"><h3>Kredit harian DIEM</h3><p>Satu DIEM memberi kredit 1 dolar per hari, diperbarui 00:01 UTC, tidak kedaluwarsa.</p></div>
  <div class="cell"><h3>Rujukan</h3><p>Tautan rujukan memberi kredit 10 dolar untuk Anda dan pendaftar, setelah dia berlangganan Pro.</p></div>
  <div class="cell"><h3>Model murah</h3><p>DeepSeek V4.1 Flash sekitar 0,30 dolar per juta token masuk.</p></div>
</div>
<div style="margin-top:20px;display:flex;gap:10px;flex-wrap:wrap">
  <a href="https://venice.ai/token" class="btn ghost" target="_blank" rel="noopener">Dasbor Token</a>
  <a href="https://venice.ai/chat" class="btn ghost" target="_blank" rel="noopener">Ambil tautan rujukan</a>
</div>
<p style="margin-top:16px;font-size:12px;color:var(--dim)">Tautan rujukan ada di menu Setelan akun Venice. Belum ada komisi tunai, bentuknya kredit API.</p>
</div></section>
"""

B["/admin"] = r"""
<div class="wrap pghead"><div class="kick">33 · Admin</div>
<h1>Catatan kerja <em>dan kendali node</em>.</h1>
<p class="lead">Catatan disimpan di perangkat ini saja. Belum ada kata sandi, jangan simpan rahasia di sini.</p></div>
<section><div class="wrap">
<div class="grid">
  <div class="cell"><h3>Node</h3><p id="astat">memeriksa…</p></div>
  <div class="cell"><h3>Ruang</h3><p>114 rute aktif, 3 di antaranya baru.</p></div>
  <div class="cell"><h3>Catatan</h3><p id="acount">0 catatan tersimpan.</p></div>
</div>
<h2 style="margin-top:34px">Catatan baru</h2><div class="hr"></div>
<textarea id="ntext" placeholder="Contoh: klien A minta revisi warna, tenggat Kamis."></textarea>
<div style="display:flex;gap:9px;margin-top:12px;flex-wrap:wrap">
  <button id="nsave" class="btn solid">Simpan</button>
  <button id="nexp" class="btn ghost">Ekspor JSON</button>
  <button id="nclear" class="btn ghost">Hapus semua</button>
</div>
<h2 style="margin-top:34px">Daftar catatan</h2><div class="hr"></div>
<input id="nfilter" type="search" placeholder="Saring catatan..."><div id="nlist"></div>
</div></section>
<script nonce="__NONCE__">
(function(){
  var K='alf.notes', ta=document.getElementById('ntext'), list=document.getElementById('nlist'),
      cnt=document.getElementById('acount'), st=document.getElementById('astat'), FLT='';
  function get(){ try{ return JSON.parse(localStorage.getItem(K)||'[]'); }catch(e){ return []; } }
  function set(v){ localStorage.setItem(K, JSON.stringify(v)); render(); }
  function render(){
    var a=get(); list.innerHTML=''; cnt.textContent=a.length+' catatan tersimpan.';
    if(FLT) a=a.filter(function(n){return n.x.toLowerCase().indexOf(FLT)>-1});
    if(!a.length){ list.innerHTML='<p style="font-size:12px;color:var(--dim)">Belum ada catatan.</p>'; return; }
    a.slice().reverse().forEach(function(n){
      var d=document.createElement('div'); d.className='noteitem';
      var box=document.createElement('div');
      var t=document.createElement('time'); t.textContent=new Date(n.t).toLocaleString('id-ID');
      var q=document.createElement('div'); q.textContent=n.x;
      box.appendChild(t); box.appendChild(q);
      var del=document.createElement('button'); del.textContent='hapus';
      del.onclick=function(){ set(get().filter(function(o){return o.id!==n.id})); };
      d.appendChild(box); d.appendChild(del); list.appendChild(d);
    });
  }
  document.getElementById('nsave').onclick=function(){
    if(!ta.value.trim()) return;
    var v=get(); v.push({x:ta.value.trim(), t:Date.now(), id:String(Date.now())+Math.random()});
    set(v); ta.value='';
  };
  document.getElementById('nclear').onclick=function(){ if(confirm('Hapus semua catatan?')) set([]); };
  document.getElementById('nexp').onclick=function(){
    var b=new Blob([JSON.stringify(get(),null,2)],{type:'application/json'}), u=URL.createObjectURL(b);
    var a=document.createElement('a'); a.href=u; a.download='catatan-alfiliator.json'; a.click(); URL.revokeObjectURL(u);
  };
  document.getElementById('nfilter').addEventListener('input', function(e){ FLT=e.target.value.toLowerCase(); render(); });
  fetch('/health').then(function(r){return r.json()}).then(function(d){
    st.textContent='online · '+d.rooms+' ruang'; }).catch(function(){ st.textContent='health tidak terbaca'; });
  render();
})();
</script>

"""
def _page80(slug, num, title, desc, rows):
    if isinstance(rows, str):
        rows = [tuple(r.split("|", 1)) for r in rows.split("\n") if "|" in r]
    if rows:
        body = ('<table class="tbl rv">'
                + "".join("<tr><td>%s</td><td>%s</td></tr>" % (a, b) for a, b in rows)
                + "</table>")
    else:
        body = ""
    return ('<div class="wrap pghead"><div class="kick">%s &middot; %s</div>'
            '<h1>%s</h1><p class="lead">%s</p></div>'
            '<section><div class="wrap">%s'
            '<div class="cta rv" style="margin-top:26px"><h2>Bahas %s</h2>'
            '<p>Sertakan konteks singkat; balasan berisi estimasi, durasi, dan cakupan.</p>'
            '<div class="row"><a href="__WA__?text=Halo__soal__%s" class="btn solid" '
            'target="_blank" rel="noopener">Kirim Brief</a>'
            '<a href="/kontak" class="btn ghost">Kanal Lain</a></div></div>'
            '</div></section>') % (num, title, title, desc, body, title, slug.strip("/"))

for _s, _n, _t, _d, _rows in _EXT:
    if _s not in B:
        B[_s] = _page80(_s, _n, _t, _d, _rows)

PAGES = {u: (t, d, B[u]) for u, _n, t, d in ROOMS}
BUILT = {u: page(u, t, d, B[u]) for u, (t, d, _b) in PAGES.items()}

import re as _re
SEARCH_INDEX = [{"u": u, "t": t, "d": d,
  "k": " ".join(_re.findall(r"<h[23]>(.*?)</h[23]>", B[u]))} for u, _n, t, d in ROOMS]

ROBOTS = "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % BASE
SITEMAP = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           + "".join("<url><loc>%s%s</loc></url>" % (BASE, u) for u in PAGES)
           + "</urlset>")

class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "Atelier/5.1"
    sys_version = ""
    protocol_version = "HTTP/1.1"
    timeout = 15

    def _rl(self):
        if self.command == "HEAD":
            return True
        ip = self.client_address[0]
        ua = (self.headers.get("User-Agent") or "").lower()
        slow = any(b in ua for b in BAD_UA)
        now = time.time()
        q = _hits[ip]
        while q and now - q[0] > RATE_WINDOW: q.popleft()
        if len(q) >= (RATE_LIMIT // 3 if slow else RATE_LIMIT): return False
        b = _burst[ip]
        while b and now - b[0] > BURST_WINDOW: b.popleft()
        if len(b) >= BURST_LIMIT: return False
        q.append(now); b.append(now)
        if len(_hits) > 4096:
            for k in [k for k, v in _hits.items() if not v][:1024]:
                _hits.pop(k, None); _burst.pop(k, None)
        return True

    def _send(self, code, body, ctype="text/html; charset=utf-8", extra=None):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "geolocation=(), camera=(), microphone=()")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("X-Permitted-Cross-Domain-Policies", "none")
        self.send_header("X-Download-Options", "noopen")
        self.send_header("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")
        self.send_header("Content-Security-Policy",
            "default-src 'none'; worker-src 'self'; "
            "script-src 'nonce-%s'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://api.venice.ai https://api.pwnedpasswords.com https://api.github.com https://cloudflare-dns.com; manifest-src 'self'; "
            "form-action 'self'; base-uri 'none'; frame-ancestors 'none'; upgrade-insecure-requests"
            % getattr(self, "nonce", ""))
        if extra:
            for k, v in extra.items(): self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD": self.wfile.write(data)

    def _method_ok(self):
        if self.command not in ("GET", "HEAD"):
            self._send(405, "Metode tidak diizinkan",
                       extra={"Allow": "GET, HEAD"}); return False
        return True

    def do_GET(self):
        self.nonce = secrets.token_urlsafe(16)
        if not self._method_ok(): return
        raw = self.path.split("?", 1)[0]
        if len(raw) > MAX_PATH:
            self._send(414, "Jalur terlalu panjang"); return
        if ".." in raw or "//" in raw.strip("/"):
            self._send(400, "Jalur tidak sah"); return
        if not re.fullmatch(r"/[A-Za-z0-9\-/\.]*", raw):
            self._send(400, "Karakter jalur tidak sah"); return
        if not self._rl():
            self._send(429, "<h1 style='font-family:monospace;color:#d4af7a;background:#07070a;padding:44px'>429 // TERLALU BANYAK</h1>",
                       extra={"Retry-After": str(RATE_WINDOW)}); return
        path = raw.rstrip("/").lower() or "/"
        if path in BUILT:
            extra = {"X-Robots-Tag": "noindex"} if path == "/admin" else None
            self._send(200, BUILT[path].replace("__NONCE__", self.nonce), extra=extra)
        elif path == "/health": self._send(200, ('{"status":"online","rooms":%d}' % len(ROOMS)), "application/json")
        elif path == "/index.json":
            import json as _j
            self._send(200, _j.dumps(SEARCH_INDEX, ensure_ascii=False), "application/json")
        elif path == "/.well-known/security.txt":
            self._send(200, SEC_TXT, "text/plain; charset=utf-8")
        elif path == "/robots.txt": self._send(200, ROBOTS, "text/plain; charset=utf-8")
        elif path == "/sitemap.xml": self._send(200, SITEMAP, "application/xml; charset=utf-8")
        elif path == "/favicon.ico": self._send(204, "")
        else:
            self._send(404, page("/", "Tidak Ditemukan", "Halaman tidak ada.",
                "<div class='wrap pghead'><div class='kick'>404</div><h1>Ruang <em>tidak ada</em>.</h1>"
                "<p class='lead'>Tautan mungkin salah atau sudah dipindahkan.</p>"
                "<div style='margin-top:28px'><a href='/' class='btn solid'>Kembali ke Beranda</a></div></div>").replace("__NONCE__", self.nonce))

    do_HEAD = do_GET

    def log_message(self, fmt, *args):
        print("  %s -> %s" % (self.address_string(), fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True
    request_queue_size = 128

    def process_request(self, request, client_address):
        _sem.acquire()
        try:
            super().process_request(request, client_address)
        except Exception:
            _sem.release(); raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            _sem.release()


if __name__ == "__main__":
    print("=" * 52)
    print("  ATELIER NODE v6 AKTIF — 114 ruang, tema, roadmap")
    print("  http://localhost:%d" % PORT)
    print("=" * 52)
    try:
        with Server((HOST, PORT), Handler) as httpd: httpd.serve_forever()
    except KeyboardInterrupt: print("\n[!] Node dimatikan.")
