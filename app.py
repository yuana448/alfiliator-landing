#!/usr/bin/env python3
# ==========================================================
#  ALFILIATOR // ATELIER NODE v5 — 30 ruang, tema, roadmap
#  python app.py   |   PORT=8888
# ==========================================================
import os, time, html, http.server, socketserver
from collections import defaultdict, deque

PORT = int(os.environ.get("PORT", "8888"))
HOST = os.environ.get("HOST", "0.0.0.0")
WA   = "https://wa.me/6281292442362"
BASE = "http://localhost:%d" % PORT
RATE_LIMIT, RATE_WINDOW = 90, 60
_hits = defaultdict(deque)

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
        var end=+b.dataset.c,pre=b.dataset.p||'',suf=b.dataset.s||'',t0=null;
        (function st(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1300);
          b.textContent=pre+Math.floor(end*(1-Math.pow(1-p,3)))+suf;
          if(p<1)requestAnimationFrame(st);else b.textContent=pre+end+suf})(performance.now());}
      e.target.querySelectorAll&&e.target.querySelectorAll('.bar i,.track i').forEach(function(x){x.style.width=x.dataset.w+'%'});
      io.unobserve(e.target);
    });
  },{threshold:.15,rootMargin:'0px 0px -40px'});
  document.querySelectorAll('.rv,.wk').forEach(function(el){io.observe(el)});

  var ds=document.querySelectorAll('details');
  ds.forEach(function(d){d.addEventListener('toggle',function(){if(d.open)ds.forEach(function(o){if(o!==d)o.close()})})});
})();
"""

HEADBOOT = r"""
(function(){var R=document.documentElement,L=localStorage;
 R.setAttribute('data-theme',L.getItem('alf.theme')||'emas');
 R.setAttribute('data-fs',L.getItem('alf.fs')||'m');
 R.setAttribute('data-motion',L.getItem('alf.motion')||'on');
 R.setAttribute('data-grain',L.getItem('alf.grain')||'on');})();
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
]

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
<div id="drawer"><div class="dhead">30 Ruang</div>__DR__</div>

<aside id="panel" aria-label="Setelan tampilan">
  <button class="iconbtn close" id="pclose" aria-label="Tutup"><i class="fas fa-xmark"></i></button>
  <div class="kick">Setelan</div>
  <h3>Warna aksen</h3>
  <div class="sw">
    <button data-t="emas" style="background:#d4af7a" aria-label="Emas"></button>
    <button data-t="sian" style="background:#38d6e8" aria-label="Sian"></button>
    <button data-t="violet" style="background:#a48bff" aria-label="Violet"></button>
    <button data-t="zamrud" style="background:#3fdb9a" aria-label="Zamrud"></button>
    <button data-t="rose" style="background:#f0799c" aria-label="Rose"></button>
    <button data-t="mono" style="background:#cfcfcf" aria-label="Mono"></button>
  </div>
  <h3>Ukuran huruf</h3>
  <div class="seg">
    <button data-fs="s" aria-pressed="false">Kecil</button>
    <button data-fs="m" aria-pressed="true">Normal</button>
    <button data-fs="l" aria-pressed="false">Besar</button>
  </div>
  <h3>Animasi</h3>
  <div class="seg">
    <button data-mt="on" aria-pressed="true">Aktif</button>
    <button data-mt="off" aria-pressed="false">Mati</button>
  </div>
  <h3>Tekstur</h3>
  <div class="seg">
    <button data-gr="on" aria-pressed="true">Aktif</button>
    <button data-gr="off" aria-pressed="false">Mati</button>
  </div>
  <h3>Kembalikan</h3>
  <div class="seg"><button id="preset">Setel ulang semua</button></div>
  <p class="note">Pilihan disimpan di perangkat ini saja. Tidak dikirim ke server.</p>
</aside>""".replace("__NL__", nl).replace("__DR__", dr).replace("__WA__", WA)

def shell(active, title, desc, body):
    return """<!DOCTYPE html>
<html lang="id" data-theme="emas" data-fs="m" data-motion="on" data-grain="on"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#07070a">
<title>__T__ — ALFILIATOR</title>
<meta name="description" content="__D__">
<meta property="og:title" content="__T__ — ALFILIATOR">
<meta property="og:description" content="__D__">
<meta property="og:type" content="website">
<script>__HB__</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Sora:wght@300;400;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>__CSS__</style>
</head><body>
<div id="prog"></div><div id="cur"></div><div id="scan"></div>
<div class="bgfx"><div class="orb o1" data-px=".10"></div><div class="orb o2" data-px="-.13"></div><div class="orb o3" data-px=".07"></div><div class="mesh"></div></div>
<div class="grain"></div>
__NAV__
<main>__BODY__</main>
<footer><div class="wrap fg">
  <div>&copy; 2026 ALFILIATOR — Atelier Digital</div>
  <div class="mono">NODE v5 · 30 RUANG</div>
</div></footer>
<a class="fab" href="__WA__?text=Halo__ALFILIATOR" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
<button id="top" aria-label="Atas"><i class="fas fa-arrow-up"></i></button>
<script>__JS__</script>
</body></html>""".replace("__T__", html.escape(title)).replace("__D__", html.escape(desc)) \
   .replace("__HB__", HEADBOOT).replace("__CSS__", CSS).replace("__NAV__", nav(active)) \
   .replace("__BODY__", body).replace("__WA__", WA).replace("__JS__", JS)

def page(active, title, desc, body):
    return shell(active, title, desc, body)

# ============================================================ halaman
B = {}
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
    <div class="stat"><b data-c="128" data-s="+">0</b><span>Proyek Selesai</span></div>
    <div class="stat"><b data-c="96" data-s="%">0</b><span>Klien Kembali</span></div>
    <div class="stat"><b data-c="99" data-s=".9%">0</b><span>Uptime</span></div>
    <div class="stat"><b data-c="2" data-p="&lt;" data-s=" jam">0</b><span>Respon</span></div>
  </div>
</div>
<section><div class="wrap">
  <div class="kick rv">Tiga Puluh Ruang</div>
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
  <div class="cell rv"><div class="ic"><i class="fas fa-window-maximize"></i></div><h3>Landing Page</h3><p>Halaman promosi fokus untuk iklan berbayar dan closing cepat.</p><span class="from">mulai Rp 850.000</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-building"></i></div><h3>Company Profile</h3><p>Profil bisnis profesional, katalog layanan, formulir lead.</p><span class="from">mulai Rp 2.400.000</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-cart-shopping"></i></div><h3>Toko Online</h3><p>Katalog, keranjang, checkout, integrasi payment gateway.</p><span class="from">mulai Rp 4.500.000</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-diagram-project"></i></div><h3>Sistem Custom</h3><p>Dashboard, multi-peran, laporan, dan API internal.</p><span class="from">mulai Rp 9.500.000</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-mobile-screen-button"></i></div><h3>Aplikasi Mobile</h3><p>Android dan iOS, native maupun cross-platform.</p><span class="from">mulai Rp 6.500.000</span></div>
  <div class="cell rv"><div class="ic"><i class="fab fa-telegram"></i></div><h3>Bot &amp; Automation</h3><p>WhatsApp/Telegram, auto-reply, notifikasi, sinkronisasi.</p><span class="from">mulai Rp 1.750.000</span></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-shield-halved"></i></div><h3>Security Audit</h3><p>Pemindaian celah, pengerasan server, laporan prioritas.</p><span class="from">mulai Rp 2.500.000</span></div>
</div></div></section>
<section><div class="wrap"><div class="cta rv"><h2>Butuh kombinasi?</h2>
<p>Banyak proyek menggabungkan web dan bot sekaligus. Sebutkan semuanya, saya susun satu penawaran utuh.</p>
<div class="row"><a href="__WA__?text=Halo__2C__saya__butuh__kombinasi" class="btn solid" target="_blank" rel="noopener">Diskusikan</a><a href="/harga" class="btn ghost">Lihat Tarif</a></div></div></div></section>
"""

B["/harga"] = """
<div class="wrap pghead"><div class="kick">03 · Tarif</div>
<h1>Harga terbuka, <em>durasi jujur</em>.</h1>
<p class="lead">Estimasi sudah memuat desain, revisi terjadwal, dan pengujian. Pembayaran 50 persen di awal, 50 persen saat serah terima.</p></div>
<section><div class="wrap">
  <div class="plans rv">
    <div class="plan"><h3>Starter</h3><div class="price">Rp 850.000<small>sekali bayar</small></div><div class="eta"><i class="far fa-clock"></i> 4–6 hari</div>
      <ul><li><i class="fas fa-check"></i>1 halaman</li><li><i class="fas fa-check"></i>Responsif</li><li><i class="fas fa-check"></i>Form kontak</li><li><i class="fas fa-check"></i>SEO dasar</li><li><i class="fas fa-check"></i>1x revisi</li><li class="off"><i class="fas fa-minus"></i>CMS</li></ul>
      <a href="__WA__?text=Paket__Starter" class="btn ghost" target="_blank" rel="noopener">Ambil</a></div>
    <div class="plan hot"><span class="tag">DIMINATI</span><h3>Bisnis</h3><div class="price">Rp 3.500.000<small>sekali bayar</small></div><div class="eta"><i class="far fa-clock"></i> 12–18 hari</div>
      <ul><li><i class="fas fa-check"></i>8 halaman</li><li><i class="fas fa-check"></i>Desain custom</li><li><i class="fas fa-check"></i>CMS</li><li><i class="fas fa-check"></i>Hosting + SSL</li><li><i class="fas fa-check"></i>Analytics</li><li><i class="fas fa-check"></i>2x revisi</li></ul>
      <a href="__WA__?text=Paket__Bisnis" class="btn solid" target="_blank" rel="noopener">Ambil</a></div>
    <div class="plan"><h3>Enterprise</h3><div class="price">Rp 9.500.000<small>mulai dari</small></div><div class="eta"><i class="far fa-clock"></i> 30–45 hari</div>
      <ul><li><i class="fas fa-check"></i>Sistem custom</li><li><i class="fas fa-check"></i>Multi-peran</li><li><i class="fas fa-check"></i>API internal</li><li><i class="fas fa-check"></i>Dashboard</li><li><i class="fas fa-check"></i>Deploy VPS</li><li><i class="fas fa-check"></i>Garansi 60 hari</li></ul>
      <a href="__WA__?text=Paket__Enterprise" class="btn ghost" target="_blank" rel="noopener">Ambil</a></div>
  </div>
  <h3 class="rv" style="letter-spacing:.2em;font-size:11px;color:var(--gold);text-transform:uppercase;margin:34px 0 14px">Mobile — Android dan iOS dibedakan</h3>
  <div class="plans rv">
    <div class="plan"><h3>Android</h3><div class="price">Rp 6.500.000<small>mulai dari</small></div><div class="eta"><i class="far fa-clock"></i> 21–28 hari</div>
      <ul><li><i class="fas fa-check"></i>Kotlin / Flutter</li><li><i class="fas fa-check"></i>UI custom</li><li><i class="fas fa-check"></i>Integrasi API</li><li><i class="fas fa-check"></i>Build + signing</li><li><i class="fas fa-check"></i>Pendampingan Play Store</li></ul>
      <a href="__WA__?text=Aplikasi__Android" class="btn ghost" target="_blank" rel="noopener">Ambil</a></div>
    <div class="plan"><h3>iPhone / iOS</h3><div class="price">Rp 12.000.000<small>mulai dari</small></div><div class="eta"><i class="far fa-clock"></i> 30–40 hari</div>
      <ul><li><i class="fas fa-check"></i>Swift / Flutter</li><li><i class="fas fa-check"></i>UI sesuai HIG</li><li><i class="fas fa-check"></i>Integrasi API</li><li><i class="fas fa-check"></i>TestFlight</li><li><i class="fas fa-check"></i>Pendampingan App Store</li></ul>
      <a href="__WA__?text=Aplikasi__iOS" class="btn ghost" target="_blank" rel="noopener">Ambil</a></div>
    <div class="plan"><h3>Cross-Platform</h3><div class="price">Rp 18.000.000<small>mulai dari</small></div><div class="eta"><i class="far fa-clock"></i> 40–55 hari</div>
      <ul><li><i class="fas fa-check"></i>Satu basis Flutter</li><li><i class="fas fa-check"></i>Dua build</li><li><i class="fas fa-check"></i>Desain adaptif</li><li><i class="fas fa-check"></i>Dua store</li><li><i class="fas fa-check"></i>Garansi 45 hari</li></ul>
      <a href="__WA__?text=Cross-platform" class="btn solid" target="_blank" rel="noopener">Ambil</a></div>
  </div>
  <table class="tbl rv" style="margin-top:26px"><tr><th>Tambahan</th><th>Tarif</th></tr>
    <tr><td>Bot WhatsApp / Telegram</td><td>Rp 1.750.000</td></tr>
    <tr><td>Audit keamanan + pengerasan</td><td>Rp 2.500.000</td></tr>
    <tr><td>Payment gateway</td><td>Rp 1.250.000</td></tr>
    <tr><td>Desain UI/UX Figma</td><td>Rp 1.500.000</td></tr>
    <tr><td>SEO lanjutan</td><td>Rp 1.000.000</td></tr>
    <tr><td>Maintenance bulanan</td><td>Rp 400.000</td></tr>
  </table>
  <p class="rv" style="margin-top:18px;font-size:12px;color:var(--dim);border-left:1px solid var(--gold);padding-left:16px">Di luar paket: Play Console 25 dolar sekali, Apple Developer 99 dolar per tahun, domain dan hosting untuk paket Starter. Fitur berat dihitung terpisah.</p>
</div></section>
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
<p class="lead">Supaya tidak ada yang tersembunyi di balik kata "menyesuaikan".</p></div>
<section><div class="wrap"><table class="tbl rv">
  <tr><th>Isi</th><th>Starter</th><th>Bisnis</th><th>Enterprise</th></tr>
  <tr><td>Jumlah halaman</td><td>1</td><td>8</td><td>tanpa batas wajar</td></tr>
  <tr><td>Desain custom</td><td>template</td><td>ya</td><td>ya</td></tr>
  <tr><td>CMS</td><td>tidak</td><td>ya</td><td>ya</td></tr>
  <tr><td>Login pengguna</td><td>tidak</td><td>opsional</td><td>ya</td></tr>
  <tr><td>Multi-peran</td><td>tidak</td><td>tidak</td><td>ya</td></tr>
  <tr><td>API internal</td><td>tidak</td><td>tidak</td><td>ya</td></tr>
  <tr><td>Hosting + SSL</td><td>setup saja</td><td>1 tahun</td><td>1 tahun</td></tr>
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
<div class="wrap pghead"><div class="kick">14 · Teknologi Mobile</div>
<h1>Android dan iOS, <em>dua jalur berbeda</em>.</h1>
<p class="lead">Native dipakai bila butuh performa dan akses perangkat. Cross-platform dipakai bila anggaran dan waktu lebih ketat.</p></div>
<section><div class="wrap"><div class="grid">
  <div class="cell rv"><div class="ic"><i class="fab fa-android"></i></div><h3>Kotlin</h3><p>Native Android, akses penuh ke API sistem.</p></div>
  <div class="cell rv"><div class="ic"><i class="fab fa-apple"></i></div><h3>Swift</h3><p>Native iOS, sesuai panduan antarmuka Apple.</p></div>
  <div class="cell rv"><div class="ic"><i class="fas fa-layer-group"></i></div><h3>Flutter</h3><p>Satu basis kode, dua build, biaya lebih rendah.</p></div>
</div>
<table class="tbl rv" style="margin-top:26px"><tr><th>Kebutuhan</th><th>Jalur yang disarankan</th></tr>
  <tr><td>Akses kamera, Bluetooth, sensor berat</td><td>native</td></tr>
  <tr><td>Anggaran terbatas, rilis cepat</td><td>cross-platform</td></tr>
  <tr><td>Kedua platform wajib</td><td>cross-platform lebih dulu, native bila perlu</td></tr>
</table></div></section>
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
  <div class="cell rv"><div class="ic"><i class="fas fa-circle-check"></i></div><h3>Operasional</h3><p>Seluruh 30 ruang dilayani normal.</p></div>
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
<p class="rv" style="font-size:12.6px;color:var(--muted)">30 rute halaman, ditambah <span class="mono">/health</span>, <span class="mono">/robots.txt</span>, dan <span class="mono">/sitemap.xml</span>. Rute di luar daftar dijawab 404 tanpa membuka direktori.</p>
<div style="margin-top:24px"><a href="https://github.com/yuana448/alfiliator-landing" class="btn ghost" target="_blank" rel="noopener">Lihat Repositori</a></div>
</div></section>
"""

PAGES = {u: (t, d, B[u]) for u, _n, t, d in ROOMS}
BUILT = {u: page(u, t, d, B[u]) for u, (t, d, _b) in PAGES.items()}

ROBOTS = "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % BASE
SITEMAP = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           + "".join("<url><loc>%s%s</loc></url>" % (BASE, u) for u in PAGES)
           + "</urlset>")

class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "AlfiliatorAtelier/5.0"
    sys_version = ""

    def _rl(self):
        ip = self.client_address[0]; now = time.time(); q = _hits[ip]
        while q and now - q[0] > RATE_WINDOW: q.popleft()
        if len(q) >= RATE_LIMIT: return False
        q.append(now); return True

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
        self.send_header("Content-Security-Policy",
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https:; script-src 'self' 'unsafe-inline'; "
            "form-action 'self'; base-uri 'self'; frame-ancestors 'self'")
        if extra:
            for k, v in extra.items(): self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD": self.wfile.write(data)

    def do_GET(self):
        if not self._rl():
            self._send(429, "<h1 style='font-family:monospace;color:#d4af7a;background:#07070a;padding:44px'>429 // TERLALU BANYAK</h1>",
                       extra={"Retry-After": str(RATE_WINDOW)}); return
        path = self.path.split("?")[0].rstrip("/") or "/"
        if path in BUILT: self._send(200, BUILT[path])
        elif path == "/health": self._send(200, '{"status":"online","rooms":30}', "application/json")
        elif path == "/robots.txt": self._send(200, ROBOTS, "text/plain; charset=utf-8")
        elif path == "/sitemap.xml": self._send(200, SITEMAP, "application/xml; charset=utf-8")
        elif path == "/favicon.ico": self._send(204, "")
        else:
            self._send(404, page("/", "Tidak Ditemukan", "Halaman tidak ada.",
                "<div class='wrap pghead'><div class='kick'>404</div><h1>Ruang <em>tidak ada</em>.</h1>"
                "<p class='lead'>Tautan mungkin salah atau sudah dipindahkan.</p>"
                "<div style='margin-top:28px'><a href='/' class='btn solid'>Kembali ke Beranda</a></div></div>"))

    do_HEAD = do_GET

    def log_message(self, fmt, *args):
        print("  %s -> %s" % (self.address_string(), fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    print("=" * 52)
    print("  ATELIER NODE v5 AKTIF — 30 ruang, tema, roadmap")
    print("  http://localhost:%d" % PORT)
    print("=" * 52)
    try:
        with Server((HOST, PORT), Handler) as httpd: httpd.serve_forever()
    except KeyboardInterrupt: print("\n[!] Node dimatikan.")
