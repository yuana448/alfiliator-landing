#!/usr/bin/env python3
# ==========================================================
#  ALFILIATOR // SERVICE LANDING NODE v3
#  Single file, no deps. PORT=8888 python bio_link.py
# ==========================================================
import os
import http.server
import socketserver

PORT = int(os.environ.get("PORT", "8888"))
HOST = os.environ.get("HOST", "0.0.0.0")
WA = "https://wa.me/6281292442362"

PAGE = r"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#05070d">
<title>ALFILIATOR — Jasa Pembuatan Aplikasi Web, Android, iOS &amp; Sistem Custom</title>
<meta name="description" content="Jasa pembuatan aplikasi web, aplikasi Android & iOS, sistem custom, bot automation, dan audit keamanan. Estimasi waktu akurat, source code diserahkan, garansi bug.">
<meta property="og:title" content="ALFILIATOR — Jasa Pembuatan Aplikasi">
<meta property="og:description" content="Web, Android, iOS, sistem custom, bot automation. Harga transparan, timeline realistis.">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfessionalService","name":"ALFILIATOR",
"description":"Jasa pembuatan aplikasi web, Android, iOS, sistem custom, bot automation, audit keamanan.",
"areaServed":"ID","priceRange":"Rp850.000 - Rp45.000.000",
"sameAs":["https://github.com/yuana448","https://x.com/Leon63921453481"]}
</script>
<style>
:root{
  --bg:#05070d; --panel:#0a0f19; --line:rgba(120,170,220,.13);
  --ink:#eaf2fb; --muted:#8298b0;
  --cy:#22e3ff; --vi:#8b6bff; --gr:#38f5a8; --am:#ffb648; --rd:#ff5d7a;
  --ease:cubic-bezier(.16,1,.3,1);
}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html{scroll-behavior:smooth;scroll-padding-top:80px}
body{font-family:'Sora',sans-serif;background:var(--bg);color:var(--ink);
  line-height:1.65;overflow-x:hidden;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
.wrap{width:min(1180px,100% - 40px);margin-inline:auto}
.mono{font-family:'JetBrains Mono',monospace}

/* ---------- PROGRESS + CURSOR ---------- */
#prog{position:fixed;top:0;left:0;height:2.5px;width:0;z-index:90;
  background:linear-gradient(90deg,var(--cy),var(--vi),var(--gr));
  box-shadow:0 0 12px var(--cy)}
#cur{position:fixed;top:0;left:0;width:340px;height:340px;border-radius:50%;z-index:1;
  pointer-events:none;opacity:0;transition:opacity .4s;
  background:radial-gradient(circle,rgba(34,227,255,.10),transparent 62%);
  transform:translate(-50%,-50%)}
@media(pointer:fine){#cur{opacity:1}}

/* ---------- LATAR ---------- */
.bgfx{position:fixed;inset:0;z-index:-3;pointer-events:none;overflow:hidden}
.bgfx .orb{position:absolute;border-radius:50%;filter:blur(90px);opacity:.5;will-change:transform}
.bgfx .o1{width:52vmax;height:52vmax;left:-14%;top:-18%;background:radial-gradient(circle,#0a5cff,transparent 68%)}
.bgfx .o2{width:44vmax;height:44vmax;right:-16%;top:26%;background:radial-gradient(circle,#8b6bff,transparent 68%)}
.bgfx .o3{width:40vmax;height:40vmax;left:26%;bottom:-22%;background:radial-gradient(circle,#00ffc2,transparent 70%)}
.bgfx .mesh{position:absolute;inset:0;opacity:.28;
  background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);
  background-size:72px 72px;
  mask-image:radial-gradient(ellipse at 50% 0%,#000 10%,transparent 78%);
  -webkit-mask-image:radial-gradient(ellipse at 50% 0%,#000 10%,transparent 78%)}
.grain{position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.045;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)'/%3E%3C/svg%3E")}

/* ---------- NAV ---------- */
header{position:sticky;top:0;z-index:60;backdrop-filter:blur(16px);
  background:rgba(5,7,13,.55);border-bottom:1px solid transparent;transition:.3s}
header.stuck{background:rgba(5,7,13,.92);border-bottom-color:var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;height:68px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:.16em;font-size:13px}
.brand i{width:30px;height:30px;display:grid;place-items:center;border-radius:8px;
  background:linear-gradient(135deg,var(--cy),var(--vi));color:#04121a;font-size:13px;
  animation:bp 3.4s ease-in-out infinite}
@keyframes bp{50%{transform:scale(1.09) rotate(-6deg)}}
.nav-links{display:none;gap:26px;font-size:13px;color:var(--muted)}
.nav-links a{position:relative;padding-block:4px}
.nav-links a::after{content:"";position:absolute;left:0;bottom:0;height:1px;width:0;
  background:var(--cy);transition:width .3s var(--ease)}
.nav-links a:hover{color:var(--cy)}
.nav-links a:hover::after{width:100%}
.nav-cta{display:none}
.btn{position:relative;display:inline-flex;align-items:center;justify-content:center;gap:9px;
  padding:12px 22px;border-radius:10px;font-weight:600;font-size:13.5px;overflow:hidden;
  border:1px solid transparent;cursor:pointer;transition:.28s var(--ease);white-space:nowrap;
  will-change:transform}
.btn::before{content:"";position:absolute;top:0;bottom:0;width:60%;left:-80%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.42),transparent);
  transform:skewX(-18deg)}
.btn:hover::before{animation:sh .75s var(--ease)}
@keyframes sh{to{left:130%}}
.btn-p{background:linear-gradient(135deg,var(--cy),var(--vi));color:#04121a;
  box-shadow:0 10px 34px -14px var(--cy)}
.btn-p:hover{box-shadow:0 16px 40px -12px var(--cy)}
.btn-g{border-color:var(--line);color:var(--ink);background:rgba(255,255,255,.03)}
.btn-g:hover{border-color:var(--cy);color:var(--cy)}

/* ---------- HERO ---------- */
.hero{padding:64px 0 72px;position:relative}
.pill{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:999px;
  border:1px solid rgba(56,245,168,.3);background:rgba(56,245,168,.07);
  font-size:10.5px;letter-spacing:.18em;color:var(--gr);margin-bottom:22px;
  animation:pin .8s var(--ease) both}
@keyframes pin{from{opacity:0;transform:translateY(-10px)}}
.pill .dot{width:6px;height:6px;border-radius:50%;background:var(--gr);box-shadow:0 0 10px var(--gr);animation:bl 1.6s steps(2) infinite}
@keyframes bl{50%{opacity:.2}}
h1{font-size:clamp(30px,6.4vw,58px);font-weight:800;line-height:1.06;letter-spacing:-.025em;margin-bottom:18px}
h1 .w{display:inline-block;opacity:0;transform:translateY(22px) rotateX(-40deg);
  animation:wr .7s var(--ease) forwards}
@keyframes wr{to{opacity:1;transform:none}}
h1 .grad{background:linear-gradient(100deg,var(--cy),var(--vi) 55%,var(--gr));
  background-size:200% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;
  animation:gsh 6s linear infinite}
@keyframes gsh{to{background-position:200% 0}}
.hero p.lead{font-size:clamp(14px,2.4vw,16.5px);color:var(--muted);max-width:620px;margin-bottom:30px;
  opacity:0;animation:fu .8s var(--ease) .55s forwards}
@keyframes fu{to{opacity:1}}
.hero-actions{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:44px;
  opacity:0;animation:fu .8s var(--ease) .7s forwards}
.trust{display:flex;flex-wrap:wrap;gap:22px;font-size:11.5px;color:var(--muted)}
.trust span{display:inline-flex;align-items:center;gap:7px}
.trust i{color:var(--gr);font-size:11px}

.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line);
  border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-top:46px}
.stat{background:#070c15;padding:22px 18px;transition:background .3s}
.stat:hover{background:#0b1220}
.stat b{display:block;font-size:clamp(21px,4.6vw,30px);font-weight:800;color:var(--cy);letter-spacing:-.02em}
.stat span{font-size:10px;letter-spacing:.16em;color:var(--muted);text-transform:uppercase}

/* ---------- MARQUEE ---------- */
.mq{border-block:1px solid var(--line);background:rgba(255,255,255,.015);overflow:hidden;padding:14px 0;
  mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.mq-track{display:flex;gap:44px;width:max-content;animation:mq 26s linear infinite}
.mq:hover .mq-track{animation-play-state:paused}
.mq-track span{font-family:'JetBrains Mono',monospace;font-size:11.5px;letter-spacing:.22em;color:#5d7a96;white-space:nowrap}
@keyframes mq{to{transform:translateX(-50%)}}

/* ---------- SECTION ---------- */
section{padding:84px 0}
.head{max-width:660px;margin-bottom:48px}
.eyebrow{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.24em;
  color:var(--cy);margin-bottom:14px;display:flex;align-items:center;gap:10px}
.eyebrow::before{content:"";width:26px;height:1px;background:var(--cy)}
h2{font-size:clamp(23px,4.4vw,36px);font-weight:800;line-height:1.16;letter-spacing:-.02em;margin-bottom:14px}
.head p{color:var(--muted);font-size:14.5px}

/* ---------- SPOTLIGHT CARD BASE ---------- */
.spot{position:relative;overflow:hidden}
.spot::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:0;transition:opacity .35s;
  background:radial-gradient(340px circle at var(--mx,50%) var(--my,0%),rgba(34,227,255,.16),transparent 68%)}
.spot:hover::before{opacity:1}

/* ---------- LAYANAN ---------- */
.grid-s{display:grid;gap:14px;grid-template-columns:1fr}
.svc{padding:26px 22px;border:1px solid var(--line);border-radius:14px;
  background:linear-gradient(160deg,rgba(14,22,36,.8),rgba(6,10,17,.9));transition:.3s var(--ease)}
.svc::after{content:"";position:absolute;inset:0;opacity:0;transition:.3s;pointer-events:none;
  background:radial-gradient(420px circle at 20% 0%,color-mix(in srgb,var(--a) 14%,transparent),transparent 70%)}
.svc:hover{border-color:color-mix(in srgb,var(--a) 50%,transparent);transform:translateY(-4px)}
.svc:hover::after{opacity:1}
.svc .ic{width:42px;height:42px;display:grid;place-items:center;border-radius:11px;
  border:1px solid color-mix(in srgb,var(--a) 35%,transparent);
  background:color-mix(in srgb,var(--a) 10%,transparent);color:var(--a);font-size:16px;margin-bottom:16px;
  transition:.35s var(--ease)}
.svc:hover .ic{transform:translateY(-3px) rotate(-8deg);
  box-shadow:0 0 22px color-mix(in srgb,var(--a) 55%,transparent)}
.svc h3{font-size:15.5px;font-weight:600;margin-bottom:8px}
.svc p{font-size:13px;color:var(--muted)}
.svc .from{display:inline-block;margin-top:14px;font-family:'JetBrains Mono',monospace;
  font-size:11.5px;color:var(--a);letter-spacing:.06em}

/* ---------- HARGA ---------- */
.plans{display:grid;gap:16px;grid-template-columns:1fr}
.plan{display:flex;flex-direction:column;padding:28px 24px;
  border:1px solid var(--line);border-radius:16px;background:#080d16;transition:.3s var(--ease)}
.plan:hover{transform:translateY(-4px);border-color:rgba(34,227,255,.4)}
.plan.hot{border-color:rgba(34,227,255,.5);background:linear-gradient(175deg,rgba(34,227,255,.09),#080d16 42%);
  box-shadow:0 24px 70px -34px var(--cy)}
.plan .tag{position:absolute;top:-1px;right:18px;padding:4px 11px;border-radius:0 0 8px 8px;
  background:linear-gradient(135deg,var(--cy),var(--vi));color:#04121a;font-size:9.5px;font-weight:800;letter-spacing:.14em}
.plan h3{font-size:14px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
.price{font-size:clamp(24px,5vw,31px);font-weight:800;letter-spacing:-.03em;color:var(--ink)}
.price small{display:block;font-size:10.5px;font-weight:400;color:var(--muted);letter-spacing:.1em;margin-top:5px}
.plan ul{list-style:none;margin:20px 0 22px;display:grid;gap:10px;font-size:12.8px;color:#a9bccf}
.plan li{display:flex;gap:9px;align-items:flex-start}
.plan li i{color:var(--gr);font-size:11px;margin-top:5px}
.plan li.off{color:#5c6f83}
.plan li.off i{color:#3c4c5c}
.plan .btn{width:100%;margin-top:auto}
.eta{display:inline-flex;align-items:center;gap:7px;font-family:'JetBrains Mono',monospace;
  font-size:10.5px;color:var(--am);letter-spacing:.09em;margin-bottom:18px;
  border:1px solid rgba(255,182,72,.28);background:rgba(255,182,72,.07);
  padding:4px 9px;border-radius:6px}

/* ---------- MOBILE SECTION ---------- */
.mob{display:grid;gap:14px;grid-template-columns:1fr}
.mcard{position:relative;padding:26px 22px;border:1px solid var(--line);border-radius:14px;
  background:linear-gradient(165deg,rgba(14,22,36,.85),rgba(6,10,17,.95));transition:.3s var(--ease)}
.mcard:hover{transform:translateY(-4px)}
.mcard.and:hover{border-color:rgba(56,245,168,.45)}
.mcard.ios:hover{border-color:rgba(255,255,255,.4)}
.mcard.cross:hover{border-color:rgba(139,107,255,.5)}
.mcard .os{display:flex;align-items:center;gap:10px;font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted);margin-bottom:16px}
.mcard .os i{font-size:20px}
.mcard.and .os i{color:#3ddc84}
.mcard.ios .os i{color:#e8f4ff}
.mcard.cross .os i{color:var(--vi)}
.mcard .big{font-size:clamp(21px,4.4vw,26px);font-weight:800;letter-spacing:-.02em}
.mcard .big small{display:block;font-size:10px;font-weight:400;color:var(--muted);letter-spacing:.1em;margin-top:4px}
.mcard .eta{margin:14px 0 0}
.mcard ul{list-style:none;margin:16px 0 20px;display:grid;gap:9px;font-size:12.6px;color:#a9bccf}
.mcard li{display:flex;gap:8px}
.mcard li i{font-size:10px;margin-top:6px;color:var(--gr)}
.mcard .btn{width:100%}
.mnote{margin-top:16px;border:1px dashed rgba(255,182,72,.35);border-radius:12px;
  background:rgba(255,182,72,.05);padding:18px 20px;font-size:12.6px;color:#c9b493}
.mnote b{color:var(--am);display:block;margin-bottom:8px;font-size:12px;letter-spacing:.1em}
.mnote ul{list-style:none;display:grid;gap:7px;margin-top:6px}
.mnote li{display:flex;gap:8px}
.mnote li::before{content:"—";color:var(--am)}

/* ---------- FAKTOR ---------- */
.factors{display:grid;gap:10px;grid-template-columns:1fr;margin-top:20px}
.factor{display:flex;gap:12px;padding:16px 18px;border:1px solid var(--line);border-radius:11px;background:#070c15}
.factor i{color:var(--cy);font-size:13px;margin-top:3px}
.factor b{display:block;font-size:13px;margin-bottom:3px}
.factor span{font-size:12.4px;color:var(--muted)}

/* ---------- ADDON ---------- */
.addons{border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-top:20px}
.addon{display:flex;align-items:center;justify-content:space-between;gap:16px;
  padding:15px 20px;border-bottom:1px solid var(--line);font-size:13px;background:#070c14;transition:.2s}
.addon:last-child{border-bottom:0}
.addon:hover{background:#0b1220}
.addon .n{display:flex;align-items:center;gap:11px}
.addon i{color:var(--am);font-size:12px;width:16px;text-align:center}
.addon b{font-family:'JetBrains Mono',monospace;color:var(--am);font-size:12.5px;white-space:nowrap}

/* ---------- PROSES ---------- */
.steps{display:grid;gap:12px;grid-template-columns:1fr;counter-reset:s}
.step{position:relative;padding:24px 22px 24px 60px;border:1px solid var(--line);
  border-radius:12px;background:#070c15;transition:.3s}
.step:hover{border-color:rgba(34,227,255,.35)}
.step::before{counter-increment:s;content:"0" counter(s);position:absolute;left:20px;top:24px;
  font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;color:var(--cy)}
.step h4{font-size:14.5px;margin-bottom:6px}
.step p{font-size:12.8px;color:var(--muted)}

/* ---------- SKILL ---------- */
.skills{display:grid;gap:22px;grid-template-columns:1fr}
.skill .top{display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:8px}
.skill .top b{font-family:'JetBrains Mono',monospace;color:var(--cy);font-weight:400}
.bar{height:5px;border-radius:99px;background:rgba(255,255,255,.06);overflow:hidden}
.bar i{display:block;height:100%;width:0;border-radius:99px;
  background:linear-gradient(90deg,var(--cy),var(--vi));transition:width 1.3s var(--ease)}

/* ---------- TESTI ---------- */
.quotes{display:grid;gap:14px;grid-template-columns:1fr}
.quote{padding:24px 22px;border:1px solid var(--line);border-radius:14px;background:#080d16;transition:.3s}
.quote:hover{transform:translateY(-3px);border-color:rgba(255,182,72,.35)}
.quote .stars{color:var(--am);font-size:11px;margin-bottom:12px;letter-spacing:2px}
.quote p{font-size:13.4px;color:#b7c9d9;margin-bottom:16px}
.who{display:flex;align-items:center;gap:11px}
.who .av{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;
  background:linear-gradient(135deg,var(--cy),var(--vi));color:#04121a;font-weight:800;font-size:13px}
.who b{display:block;font-size:12.5px}
.who span{font-size:11px;color:var(--muted)}

/* ---------- FAQ ---------- */
details{border:1px solid var(--line);border-radius:12px;background:#070c15;margin-bottom:10px;overflow:hidden;transition:border-color .25s}
details[open]{border-color:rgba(34,227,255,.35)}
summary{padding:17px 20px;cursor:pointer;font-size:13.8px;font-weight:600;list-style:none;
  display:flex;justify-content:space-between;gap:16px;align-items:center}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-family:'JetBrains Mono',monospace;color:var(--cy);font-size:17px;
  transition:transform .3s var(--ease)}
details[open] summary::after{transform:rotate(45deg)}
.body{display:grid;grid-template-rows:0fr;transition:grid-template-rows .35s var(--ease)}
details[open] .body{grid-template-rows:1fr}
.body>div{overflow:hidden}
.body p{padding:0 20px 18px;font-size:13px;color:var(--muted)}

/* ---------- CTA ---------- */
.cta{position:relative;border:1px solid rgba(34,227,255,.28);border-radius:18px;overflow:hidden;
  padding:clamp(34px,6vw,58px) clamp(22px,5vw,50px);text-align:center;
  background:linear-gradient(160deg,rgba(34,227,255,.11),rgba(139,107,255,.09) 55%,#060a12)}
.cta::after{content:"";position:absolute;inset:-40%;pointer-events:none;
  background:conic-gradient(from 0deg,transparent,rgba(34,227,255,.13),transparent 40%);
  animation:spin 9s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.cta>*{position:relative;z-index:1}
.cta h2{margin-bottom:14px}
.cta p{color:#a9bccf;max-width:520px;margin:0 auto 28px;font-size:14px}
.cta .row{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}

/* ---------- KONTAK ---------- */
.contact-grid{display:grid;gap:10px;grid-template-columns:repeat(2,1fr)}
.clink{--a:var(--cy);display:flex;align-items:center;gap:12px;padding:15px 16px;
  border:1px solid var(--line);border-radius:11px;background:#070c15;font-size:12.8px;transition:.25s var(--ease)}
.clink:hover{border-color:color-mix(in srgb,var(--a) 55%,transparent);transform:translateX(3px)}
.clink i{color:var(--a);font-size:14px;width:18px;text-align:center}

footer{border-top:1px solid var(--line);padding:34px 0 44px;margin-top:40px}
.fgrid{display:flex;flex-wrap:wrap;gap:18px;justify-content:space-between;align-items:center;
  font-size:11.5px;color:var(--muted)}

.wa{position:fixed;right:16px;bottom:calc(16px + env(safe-area-inset-bottom));z-index:70;
  width:52px;height:52px;border-radius:50%;display:grid;place-items:center;
  background:#25d366;color:#04120a;font-size:22px;box-shadow:0 12px 32px -10px #25d366;
  transition:.25s var(--ease);animation:wp 2.6s ease-in-out infinite}
@keyframes wp{50%{box-shadow:0 12px 32px -6px #25d366,0 0 0 10px rgba(37,211,102,.10)}}
.wa:hover{transform:scale(1.09)}
#top{position:fixed;left:16px;bottom:calc(16px + env(safe-area-inset-bottom));z-index:70;
  width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font-size:13px;
  border:1px solid var(--line);background:rgba(8,13,22,.9);color:var(--muted);
  opacity:0;pointer-events:none;transition:.3s var(--ease)}
#top.on{opacity:1;pointer-events:auto}
#top:hover{color:var(--cy);border-color:var(--cy);transform:translateY(-3px)}

/* ---------- REVEAL ---------- */
.rv{opacity:0;transform:translateY(22px);transition:opacity .7s var(--ease),transform .7s var(--ease)}
.rv.on{opacity:1;transform:none}

@media(min-width:640px){
  .stats{grid-template-columns:repeat(4,1fr)}
  .grid-s,.quotes,.mob{grid-template-columns:repeat(2,1fr)}
  .skills,.factors{grid-template-columns:repeat(2,1fr)}
  .contact-grid{grid-template-columns:repeat(3,1fr)}
  .steps{grid-template-columns:repeat(2,1fr)}
}
@media(min-width:900px){
  .nav-links,.nav-cta{display:flex}
  .grid-s{grid-template-columns:repeat(3,1fr)}
  .plans{grid-template-columns:repeat(3,1fr)}
  .mob{grid-template-columns:repeat(3,1fr)}
  .quotes{grid-template-columns:repeat(3,1fr)}
  .steps{grid-template-columns:repeat(4,1fr)}
  .hero{padding:88px 0 90px}
  section{padding:104px 0}
}
@media(prefers-reduced-motion:reduce){
  *{animation-duration:.01ms!important;transition-duration:.01ms!important}
  .rv{opacity:1;transform:none}
  h1 .w{opacity:1;transform:none}
  .hero p.lead,.hero-actions{opacity:1}
}
</style>
</head>
<body>

<div id="prog"></div>
<div id="cur"></div>

<div class="bgfx"><div class="orb o1" data-px=".10"></div><div class="orb o2" data-px="-.14"></div><div class="orb o3" data-px=".07"></div><div class="mesh"></div></div>
<div class="grain"></div>

<header id="hdr">
  <div class="wrap nav">
    <a href="#" class="brand"><i class="fas fa-bolt"></i>ALFILIATOR</a>
    <nav class="nav-links">
      <a href="#layanan">Layanan</a>
      <a href="#harga">Harga</a>
      <a href="#mobile">Mobile App</a>
      <a href="#proses">Proses</a>
      <a href="#faq">FAQ</a>
    </nav>
    <a href="__WA__?text=Halo%20ALFILIATOR%2C%20saya%20mau%20konsultasi%20proyek" class="btn btn-p nav-cta mag" target="_blank" rel="noopener">
      <i class="fab fa-whatsapp"></i> Konsultasi Gratis
    </a>
  </div>
</header>

<main>
<div class="wrap hero">
  <div class="pill"><span class="dot"></span> 2 SLOT PROYEK TERSISA BULAN INI</div>
  <h1 id="h1">Aplikasi web, Android &amp; iOS yang <span class="grad">langsung bisa dipakai</span>.</h1>
  <p class="lead">Saya membangun landing page, toko online, sistem internal, aplikasi mobile, bot automation, dan hardening keamanan. Timeline dihitung realistis sejak awal, source code 100% jadi milik Anda, plus garansi bug 30 hari.</p>
  <div class="hero-actions">
    <a href="__WA__?text=Halo%2C%20saya%20mau%20minta%20penawaran" class="btn btn-p mag" target="_blank" rel="noopener">
      <i class="fas fa-paper-plane"></i> Minta Penawaran
    </a>
    <a href="#harga" class="btn btn-g mag"><i class="fas fa-tags"></i> Lihat Paket Harga</a>
  </div>
  <div class="trust">
    <span><i class="fas fa-check"></i> Garansi bug 30 hari</span>
    <span><i class="fas fa-check"></i> Source code diserahkan</span>
    <span><i class="fas fa-check"></i> NDA tersedia</span>
    <span><i class="fas fa-check"></i> Timeline tertulis</span>
  </div>
  <div class="stats">
    <div class="stat"><b data-count="128" data-suffix="+">0</b><span>Proyek Selesai</span></div>
    <div class="stat"><b data-count="96" data-suffix="%">0</b><span>Klien Repeat</span></div>
    <div class="stat"><b data-count="99" data-suffix=".9%">0</b><span>Uptime Server</span></div>
    <div class="stat"><b data-count="2" data-prefix="&lt;" data-suffix=" jam">0</b><span>Respon Chat</span></div>
  </div>
</div>

<div class="mq"><div class="mq-track">
  <span>PYTHON</span><span>LARAVEL</span><span>REACT</span><span>NODE.JS</span><span>FLUTTER</span><span>KOTLIN</span><span>SWIFT</span><span>MYSQL</span><span>POSTGRESQL</span><span>DOCKER</span><span>LINUX VPS</span><span>PLAY STORE</span><span>APP STORE</span><span>PENTEST</span>
  <span>PYTHON</span><span>LARAVEL</span><span>REACT</span><span>NODE.JS</span><span>FLUTTER</span><span>KOTLIN</span><span>SWIFT</span><span>MYSQL</span><span>POSTGRESQL</span><span>DOCKER</span><span>LINUX VPS</span><span>PLAY STORE</span><span>APP STORE</span><span>PENTEST</span>
</div></div>

<section id="layanan"><div class="wrap">
  <div class="head rv">
    <div class="eyebrow">LAYANAN</div>
    <h2>Tujuh jenis pekerjaan yang saya tangani</h2>
    <p>Semua paket web sudah termasuk setup hosting, SSL, dan optimasi kecepatan dasar. Harga di bawah adalah titik mulai — spesifikasi akhir menyesuaikan kompleksitas.</p>
  </div>
  <div class="grid-s">
    <div class="svc spot rv" style="--a:#22e3ff">
      <div class="ic"><i class="fas fa-window-maximize"></i></div>
      <h3>Landing Page Konversi</h3>
      <p>Halaman promosi fokus, dirancang untuk iklan berbayar dan closing cepat.</p>
      <span class="from">mulai Rp 850.000</span>
    </div>
    <div class="svc spot rv" style="--a:#8b6bff">
      <div class="ic"><i class="fas fa-building"></i></div>
      <h3>Company Profile</h3>
      <p>Profil bisnis profesional, katalog layanan, dan form lead masuk.</p>
      <span class="from">mulai Rp 2.400.000</span>
    </div>
    <div class="svc spot rv" style="--a:#38f5a8">
      <div class="ic"><i class="fas fa-cart-shopping"></i></div>
      <h3>Toko Online</h3>
      <p>Katalog produk, keranjang, checkout, dan integrasi payment gateway.</p>
      <span class="from">mulai Rp 4.500.000</span>
    </div>
    <div class="svc spot rv" style="--a:#ffb648">
      <div class="ic"><i class="fas fa-diagram-project"></i></div>
      <h3>Sistem / Web App Custom</h3>
      <p>Dashboard, multi-role, laporan, dan API internal sesuai alur kerja Anda.</p>
      <span class="from">mulai Rp 9.500.000</span>
    </div>
    <div class="svc spot rv" style="--a:#22e3ff">
      <div class="ic"><i class="fas fa-mobile-screen-button"></i></div>
      <h3>Aplikasi Android &amp; iOS</h3>
      <p>Aplikasi native maupun cross-platform, siap rilis ke Play Store / App Store.</p>
      <span class="from">mulai Rp 6.500.000</span>
    </div>
    <div class="svc spot rv" style="--a:#8b6bff">
      <div class="ic"><i class="fab fa-telegram"></i></div>
      <h3>Bot &amp; Automation</h3>
      <p>Bot WhatsApp/Telegram, auto-reply, notifikasi, sinkronisasi data.</p>
      <span class="from">mulai Rp 1.750.000</span>
    </div>
    <div class="svc spot rv" style="--a:#ff5d7a">
      <div class="ic"><i class="fas fa-shield-halved"></i></div>
      <h3>Security Audit</h3>
      <p>Pemindaian celah, hardening server, dan laporan rekomendasi.</p>
      <span class="from">mulai Rp 2.500.000</span>
    </div>
  </div>
</div></section>

<section id="harga"><div class="wrap">
  <div class="head rv">
    <div class="eyebrow">PAKET HARGA — WEB</div>
    <h2>Harga transparan, durasi jujur</h2>
    <p>Estimasi waktu di bawah sudah memperhitungkan desain, revisi terjadwal, dan pengujian. 50% di awal sebagai tanda jadi, 50% saat serah terima.</p>
  </div>
  <div class="plans">
    <div class="plan spot rv">
      <h3>Starter</h3>
      <div class="price">Rp 850.000<small>sekali bayar</small></div>
      <div class="eta"><i class="far fa-clock"></i> 4–6 hari kerja</div>
      <ul>
        <li><i class="fas fa-check"></i> 1 halaman landing</li>
        <li><i class="fas fa-check"></i> Mobile &amp; desktop responsif</li>
        <li><i class="fas fa-check"></i> Form kontak / WhatsApp</li>
        <li><i class="fas fa-check"></i> SEO on-page dasar</li>
        <li><i class="fas fa-check"></i> 1x revisi</li>
        <li class="off"><i class="fas fa-minus"></i> CMS &amp; dashboard</li>
      </ul>
      <a href="__WA__?text=Halo%2C%20saya%20mau%20paket%20Starter" class="btn btn-g mag" target="_blank" rel="noopener">Ambil Paket</a>
    </div>
    <div class="plan hot spot rv">
      <span class="tag">PALING DIMINATI</span>
      <h3>Bisnis</h3>
      <div class="price">Rp 3.500.000<small>sekali bayar</small></div>
      <div class="eta"><i class="far fa-clock"></i> 12–18 hari kerja</div>
      <ul>
        <li><i class="fas fa-check"></i> Hingga 8 halaman</li>
        <li><i class="fas fa-check"></i> Desain custom sesuai brand</li>
        <li><i class="fas fa-check"></i> CMS artikel &amp; katalog</li>
        <li><i class="fas fa-check"></i> Setup hosting + SSL</li>
        <li><i class="fas fa-check"></i> SEO + Google Analytics</li>
        <li><i class="fas fa-check"></i> 2x revisi + garansi 30 hari</li>
      </ul>
      <a href="__WA__?text=Halo%2C%20saya%20mau%20paket%20Bisnis" class="btn btn-p mag" target="_blank" rel="noopener">Ambil Paket</a>
    </div>
    <div class="plan spot rv">
      <h3>Enterprise</h3>
      <div class="price">Rp 9.500.000<small>mulai dari</small></div>
      <div class="eta"><i class="far fa-clock"></i> 30–45 hari kerja</div>
      <ul>
        <li><i class="fas fa-check"></i> Sistem / web app custom</li>
        <li><i class="fas fa-check"></i> Multi-role &amp; hak akses</li>
        <li><i class="fas fa-check"></i> Database + API internal</li>
        <li><i class="fas fa-check"></i> Dashboard &amp; laporan</li>
        <li><i class="fas fa-check"></i> Deployment VPS</li>
        <li><i class="fas fa-check"></i> Garansi 60 hari + dokumentasi</li>
      </ul>
      <a href="__WA__?text=Halo%2C%20saya%20mau%20paket%20Enterprise" class="btn btn-g mag" target="_blank" rel="noopener">Ambil Paket</a>
    </div>
  </div>
</div></section>

<section id="mobile"><div class="wrap">
  <div class="head rv">
    <div class="eyebrow">APLIKASI MOBILE</div>
    <h2>Android dan iPhone dibedakan, bukan disamakan</h2>
    <p>Harga iOS lebih tinggi bukan tanpa alasan: butuh akun Apple Developer berbayar tahunan, build wajib lewat Xcode, dan review App Store jauh lebih ketat daripada Play Store. Saya cantumkan apa adanya supaya Anda bisa memilih dengan sadar.</p>
  </div>
  <div class="mob">
    <div class="mcard and spot rv">
      <div class="os"><i class="fab fa-android"></i> Android</div>
      <div class="big">Rp 6.500.000<small>mulai dari / aplikasi sederhana</small></div>
      <div class="eta"><i class="far fa-clock"></i> 21–28 hari kerja</div>
      <ul>
        <li><i class="fas fa-check"></i> Kotlin / Flutter</li>
        <li><i class="fas fa-check"></i> Desain UI custom</li>
        <li><i class="fas fa-check"></i> Integrasi API &amp; database</li>
        <li><i class="fas fa-check"></i> Build APK / AAB + signing</li>
        <li><i class="fas fa-check"></i> Pendampingan rilis Play Store</li>
        <li><i class="fas fa-check"></i> Garansi bug 30 hari</li>
      </ul>
      <a href="__WA__?text=Halo%2C%20saya%20mau%20aplikasi%20Android" class="btn btn-g mag" target="_blank" rel="noopener">Ambil Paket</a>
    </div>
    <div class="mcard ios spot rv">
      <div class="os"><i class="fab fa-apple"></i> iPhone / iOS</div>
      <div class="big">Rp 12.000.000<small>mulai dari / aplikasi sederhana</small></div>
      <div class="eta"><i class="far fa-clock"></i> 30–40 hari kerja</div>
      <ul>
        <li><i class="fas fa-check"></i> Swift / Flutter</li>
        <li><i class="fas fa-check"></i> Desain UI sesuai HIG Apple</li>
        <li><i class="fas fa-check"></i> Integrasi API &amp; database</li>
        <li><i class="fas fa-check"></i> Build via Xcode + TestFlight</li>
        <li><i class="fas fa-check"></i> Pendampingan review App Store</li>
        <li><i class="fas fa-check"></i> Garansi bug 30 hari</li>
      </ul>
      <a href="__WA__?text=Halo%2C%20saya%20mau%20aplikasi%20iOS" class="btn btn-g mag" target="_blank" rel="noopener">Ambil Paket</a>
    </div>
    <div class="mcard cross spot rv">
      <div class="os"><i class="fas fa-layer-group"></i> Cross-Platform</div>
      <div class="big">Rp 18.000.000<small>mulai dari / Android + iOS</small></div>
      <div class="eta"><i class="far fa-clock"></i> 40–55 hari kerja</div>
      <ul>
        <li><i class="fas fa-check"></i> Satu basis kode Flutter</li>
        <li><i class="fas fa-check"></i> Dua build: Android + iOS</li>
        <li><i class="fas fa-check"></i> Desain adaptif per platform</li>
        <li><i class="fas fa-check"></i> Integrasi API &amp; database</li>
        <li><i class="fas fa-check"></i> Pendampingan rilis dua store</li>
        <li><i class="fas fa-check"></i> Garansi bug 45 hari</li>
      </ul>
      <a href="__WA__?text=Halo%2C%20saya%20mau%20aplikasi%20cross-platform" class="btn btn-p mag" target="_blank" rel="noopener">Ambil Paket</a>
    </div>
  </div>

  <div class="mnote rv">
    <b>BIAYA DI LUAR PAKET — DIBACA DULU</b>
    <ul>
      <li>Akun Google Play Console: $25 sekali bayar (dibuat atas nama Anda)</li>
      <li>Akun Apple Developer Program: $99 per tahun, wajib diperpanjang</li>
      <li>Perangkat uji iOS disarankan tersedia dari pihak Anda</li>
      <li>Fitur kompleks (peta, realtime, chat, pembayaran, offline sync) dihitung terpisah</li>
      <li>Estimasi bertambah bila materi konten, aset desain, atau akses API belum siap</li>
    </ul>
  </div>

  <div class="factors">
    <div class="factor rv"><i class="fas fa-code-branch"></i><div><b>Jumlah fitur</b><span>Setiap fitur menambah hari kerja dan biaya uji.</span></div></div>
    <div class="factor rv"><i class="fas fa-plug"></i><div><b>Integrasi pihak ketiga</b><span>Payment, peta, WhatsApp API, atau ERP memperpanjang waktu.</span></div></div>
    <div class="factor rv"><i class="fas fa-palette"></i><div><b>Kesiapan aset</b><span>Logo, konten, dan foto yang belum siap menahan progres.</span></div></div>
    <div class="factor rv"><i class="fas fa-repeat"></i><div><b>Revisi</b><span>Revisi di luar cakupan awal dihitung per jam dan menambah durasi.</span></div></div>
  </div>

  <div class="addons rv">
    <div class="addon"><span class="n"><i class="fas fa-plus"></i>Bot WhatsApp / Telegram automation</span><b>Rp 1.750.000</b></div>
    <div class="addon"><span class="n"><i class="fas fa-plus"></i>Audit keamanan + hardening server</span><b>Rp 2.500.000</b></div>
    <div class="addon"><span class="n"><i class="fas fa-plus"></i>Integrasi payment gateway</span><b>Rp 1.250.000</b></div>
    <div class="addon"><span class="n"><i class="fas fa-plus"></i>Desain UI/UX di Figma</span><b>Rp 1.500.000</b></div>
    <div class="addon"><span class="n"><i class="fas fa-plus"></i>Optimasi SEO on-page lanjutan</span><b>Rp 1.000.000</b></div>
    <div class="addon"><span class="n"><i class="fas fa-plus"></i>Maintenance &amp; backup bulanan</span><b>Rp 400.000 / bln</b></div>
  </div>
</div></section>

<section id="proses"><div class="wrap">
  <div class="head rv">
    <div class="eyebrow">ALUR KERJA</div>
    <h2>Empat tahap, semuanya terlihat</h2>
    <p>Anda tahu posisi proyek di setiap tahap. Tidak ada kerja hitam-hitaman.</p>
  </div>
  <div class="steps">
    <div class="step rv"><h4>Diskusi &amp; Brief</h4><p>Tujuan bisnis, referensi, target pengguna, dan batasan teknis dipetakan.</p></div>
    <div class="step rv"><h4>Desain &amp; Persetujuan</h4><p>Mockup dikirim untuk direview. Pengerjaan kode dimulai setelah Anda setuju.</p></div>
    <div class="step rv"><h4>Development</h4><p>Pengerjaan bertahap dengan preview link yang bisa Anda pantau.</p></div>
    <div class="step rv"><h4>Launch &amp; Garansi</h4><p>Deploy, serah terima source code, pelatihan singkat, lalu masuk masa garansi.</p></div>
  </div>
</div></section>

<section id="skill"><div class="wrap">
  <div class="head rv">
    <div class="eyebrow">SKILL</div>
    <h2>Yang saya kuasai di balik layar</h2>
    <p>Bukan sekadar tampilan — arsitektur, keamanan, dan server juga bagian dari pekerjaan.</p>
  </div>
  <div class="skills">
    <div class="skill rv"><div class="top"><span>Python &amp; Automation</span><b>95%</b></div><div class="bar"><i data-w="95"></i></div></div>
    <div class="skill rv"><div class="top"><span>PHP / Laravel</span><b>88%</b></div><div class="bar"><i data-w="88"></i></div></div>
    <div class="skill rv"><div class="top"><span>JavaScript / Node.js</span><b>90%</b></div><div class="bar"><i data-w="90"></i></div></div>
    <div class="skill rv"><div class="top"><span>Flutter / Dart</span><b>85%</b></div><div class="bar"><i data-w="85"></i></div></div>
    <div class="skill rv"><div class="top"><span>Kotlin (Android)</span><b>82%</b></div><div class="bar"><i data-w="82"></i></div></div>
    <div class="skill rv"><div class="top"><span>Swift (iOS)</span><b>78%</b></div><div class="bar"><i data-w="78"></i></div></div>
    <div class="skill rv"><div class="top"><span>MySQL / PostgreSQL</span><b>87%</b></div><div class="bar"><i data-w="87"></i></div></div>
    <div class="skill rv"><div class="top"><span>Linux / VPS Hardening</span><b>93%</b></div><div class="bar"><i data-w="93"></i></div></div>
    <div class="skill rv"><div class="top"><span>Cyber Security</span><b>89%</b></div><div class="bar"><i data-w="89"></i></div></div>
    <div class="skill rv"><div class="top"><span>UI/UX Design</span><b>86%</b></div><div class="bar"><i data-w="86"></i></div></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="head rv">
    <div class="eyebrow">TESTIMONI</div>
    <h2>Kata klien sebelumnya</h2>
  </div>
  <div class="quotes">
    <div class="quote rv">
      <div class="stars">★★★★★</div>
      <p>"Landing page selesai sesuai estimasi yang dijanjikan dan konversi iklan kami naik. Komunikasinya jelas, revisi cepat."</p>
      <div class="who"><div class="av">R</div><div><b>Rizky A.</b><span>Owner Toko Online</span></div></div>
    </div>
    <div class="quote rv">
      <div class="stars">★★★★★</div>
      <p>"Sistem inventori kami sebelumnya manual di Excel. Sekarang rapi dan bisa multi-user. Timeline-nya juga masuk akal."</p>
      <div class="who"><div class="av">D</div><div><b>Dewi P.</b><span>Manajer Operasional</span></div></div>
    </div>
    <div class="quote rv">
      <div class="stars">★★★★★</div>
      <p>"Bot WhatsApp-nya menghemat 2 jam kerja admin per hari. Dokumentasi dan serah terimanya lengkap."</p>
      <div class="who"><div class="av">F</div><div><b>Fajar S.</b><span>Klinik Kecantikan</span></div></div>
    </div>
  </div>
</div></section>

<section id="faq"><div class="wrap">
  <div class="head rv">
    <div class="eyebrow">FAQ</div>
    <h2>Pertanyaan yang sering masuk</h2>
  </div>
  <details class="rv"><summary>Berapa DP yang harus dibayar?</summary><div class="body"><div><p>50% di awal sebagai tanda jadi, sisanya 50% setelah proyek selesai dan Anda setujui sebelum deploy final.</p></div></div></details>
  <details class="rv"><summary>Kenapa aplikasi iOS lebih mahal?</summary><div class="body"><div><p>Karena butuh akun Apple Developer Program $99/tahun, build wajib lewat Xcode, dan review App Store jauh lebih ketat serta memakan waktu lebih lama. Biaya itu menutup jam kerja dan risiko penolakan, bukan markup sembarangan.</p></div></div></details>
  <details class="rv"><summary>Apakah estimasi waktu bisa lebih cepat?</summary><div class="body"><div><p>Bisa, dengan biaya prioritas. Estimasi normal di halaman ini sengaja dibuat longgar supaya tidak ada janji kosong. Kalau proyek mendesak, sebutkan tanggal target di awal dan saya beri hitungan terpisah.</p></div></div></details>
  <details class="rv"><summary>Apakah source code jadi milik saya?</summary><div class="body"><div><p>Ya. Seluruh kode dan aset diserahkan setelah pelunasan. Tidak ada penguncian atau sewa lisensi.</p></div></div></details>
  <details class="rv"><summary>Bisa revisi berapa kali?</summary><div class="body"><div><p>Starter 1x, Bisnis 2x, paket aplikasi menyesuaikan kontrak. Revisi di luar cakupan awal dihitung per jam.</p></div></div></details>
  <details class="rv"><summary>Garansinya mencakup apa?</summary><div class="body"><div><p>Perbaikan bug dan error dari sisi pengerjaan saya. Perubahan fitur baru di luar brief masuk kategori pengembangan lanjutan.</p></div></div></details>
  <details class="rv"><summary>Bisa NDA?</summary><div class="body"><div><p>Bisa. Kirim draf NDA Anda sebelum brief dimulai, atau saya siapkan versi sederhana untuk ditandatangani kedua pihak.</p></div></div></details>
  <details class="rv"><summary>Apakah termasuk hosting dan akun store?</summary><div class="body"><div><p>Paket web Bisnis dan Enterprise sudah termasuk setup hosting dan SSL tahun pertama. Untuk aplikasi mobile, akun Play Console dan Apple Developer dibuat atas nama Anda, biayanya ditanggung klien.</p></div></div></details>
</div></section>

<section><div class="wrap">
  <div class="cta rv">
    <div class="eyebrow" style="justify-content:center">MULAI SEKARANG</div>
    <h2>Ceritakan proyek Anda hari ini</h2>
    <p>Konsultasi awal gratis. Kirim kebutuhan singkat, saya balas dengan estimasi biaya, durasi, dan cakupan kerja yang jelas.</p>
    <div class="row">
      <a href="__WA__?text=Halo%20ALFILIATOR%2C%20saya%20mau%20konsultasi%20proyek" class="btn btn-p mag" target="_blank" rel="noopener"><i class="fab fa-whatsapp"></i> Chat WhatsApp</a>
      <a href="https://t.me/WiteXCTbot" class="btn btn-g mag" target="_blank" rel="noopener"><i class="fab fa-telegram-plane"></i> Telegram Bot</a>
    </div>
  </div>
</div></section>

<section id="kontak" style="padding-top:0"><div class="wrap">
  <div class="head rv">
    <div class="eyebrow">KANAL LAIN</div>
    <h2>Hubungi lewat mana pun</h2>
  </div>
  <div class="contact-grid">
    <a class="clink rv" style="--a:#25d366" href="__WA__" target="_blank" rel="noopener"><i class="fab fa-whatsapp"></i> WhatsApp Business</a>
    <a class="clink rv" style="--a:#2aabee" href="https://t.me/WiteXCTbot" target="_blank" rel="noopener"><i class="fab fa-telegram-plane"></i> Telegram Bot</a>
    <a class="clink rv" style="--a:#2aabee" href="https://t.me/wof1NBI7ObBlNzE9" target="_blank" rel="noopener"><i class="fab fa-telegram"></i> Channel</a>
    <a class="clink rv" style="--a:#ff4d4d" href="https://fastwork.id/user/alfiliaor_web?source=web_chat_navbar-earnings" target="_blank" rel="noopener"><i class="fas fa-briefcase"></i> Fastwork</a>
    <a class="clink rv" style="--a:#b3b3b3" href="https://github.com/yuana448?tab=projects" target="_blank" rel="noopener"><i class="fab fa-github"></i> GitHub</a>
    <a class="clink rv" style="--a:#1877f2" href="https://web.facebook.com/zerinova112/" target="_blank" rel="noopener"><i class="fab fa-facebook-f"></i> Facebook</a>
    <a class="clink rv" style="--a:#ff2fb9" href="https://www.instagram.com/javanova666/" target="_blank" rel="noopener"><i class="fab fa-instagram"></i> Instagram</a>
    <a class="clink rv" style="--a:#e8f4ff" href="https://x.com/Leon63921453481" target="_blank" rel="noopener"><i class="fab fa-x-twitter"></i> Twitter / X</a>
  </div>
</div></section>
</main>

<footer><div class="wrap fgrid">
  <div>&copy; 2026 ALFILIATOR — Digital Solutions &amp; Cyber Security</div>
  <div class="mono">BUILD v3.0 · NODE ONLINE</div>
</div></footer>

<a class="wa" href="__WA__?text=Halo%20ALFILIATOR" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
<button id="top" aria-label="Kembali ke atas"><i class="fas fa-arrow-up"></i></button>

<script>
(function(){
  const reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;

  /* progress bar + nav state + back to top */
  const prog = document.getElementById('prog'), hdr = document.getElementById('hdr'), top = document.getElementById('top');
  let raf = 0;
  addEventListener('scroll', ()=>{
    if(raf) return;
    raf = requestAnimationFrame(()=>{
      const h = document.documentElement.scrollHeight - innerHeight;
      prog.style.width = (h > 0 ? (scrollY/h)*100 : 0) + '%';
      hdr.classList.toggle('stuck', scrollY > 12);
      top.classList.toggle('on', scrollY > 620);
      if(!reduce) document.querySelectorAll('.orb').forEach(o=>{
        o.style.transform = 'translateY(' + scrollY * parseFloat(o.dataset.px||0) + 'px)';
      });
      raf = 0;
    });
  }, {passive:true});
  top.addEventListener('click', ()=> scrollTo({top:0, behavior:'smooth'}));

  /* headline stagger */
  const h1 = document.getElementById('h1');
  const walk = (node)=>{
    node.childNodes.forEach(c=>{
      if(c.nodeType === 3){
        const frag = document.createDocumentFragment();
        c.textContent.split(/(\s+)/).forEach(t=>{
          if(!t.trim()){ frag.appendChild(document.createTextNode(t)); return; }
          const s = document.createElement('span');
          s.className = 'w'; s.textContent = t;
          s.style.animationDelay = (frag.childNodes.length * 45) + 'ms';
          frag.appendChild(s);
        });
        node.replaceChild(frag, c);
      } else if(c.nodeType === 1 && !c.classList.contains('grad')) walk(c);
    });
  };
  if(!reduce) walk(h1);

  /* cursor glow */
  if(matchMedia('(pointer:fine)').matches && !reduce){
    const cur = document.getElementById('cur');
    let cx = innerWidth/2, cy = innerHeight/2, tx = cx, ty = cy;
    addEventListener('pointermove', e=>{ tx = e.clientX; ty = e.clientY; }, {passive:true});
    (function follow(){
      cx += (tx-cx)*0.13; cy += (ty-cy)*0.13;
      cur.style.left = cx+'px'; cur.style.top = cy+'px';
      requestAnimationFrame(follow);
    })();
  }

  /* spotlight kartu */
  document.querySelectorAll('.spot').forEach(el=>{
    el.addEventListener('pointermove', e=>{
      const r = el.getBoundingClientRect();
      el.style.setProperty('--mx', (e.clientX-r.left)+'px');
      el.style.setProperty('--my', (e.clientY-r.top)+'px');
    }, {passive:true});
  });

  /* tombol magnetik */
  if(matchMedia('(pointer:fine)').matches && !reduce){
    document.querySelectorAll('.mag').forEach(b=>{
      b.addEventListener('pointermove', e=>{
        const r = b.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width/2)/r.width;
        const y = (e.clientY - r.top - r.height/2)/r.height;
        b.style.transform = 'translate(' + x*6 + 'px,' + y*4 + 'px)';
      });
      b.addEventListener('pointerleave', ()=> b.style.transform = '');
    });
  }

  /* reveal + counter + skill bar */
  const io = new IntersectionObserver(es=>{
    es.forEach(e=>{
      if(!e.isIntersecting) return;
      e.target.classList.add('on');
      const b = e.target.querySelector?.('b[data-count]');
      if(b && !b.dataset.done){
        b.dataset.done = 1;
        const end = +b.dataset.count, pre = b.dataset.prefix||'', suf = b.dataset.suffix||'';
        let t0 = null;
        const step = ts=>{
          if(!t0) t0 = ts;
          const p = Math.min(1,(ts-t0)/1200);
          const n = Math.floor(end * (1-Math.pow(1-p,3)));
          b.textContent = pre + n + suf;
          if(p<1) requestAnimationFrame(step); else b.textContent = pre + end + suf;
        };
        requestAnimationFrame(step);
      }
      e.target.querySelectorAll?.('.bar i').forEach(bar=>{ bar.style.width = bar.dataset.w + '%'; });
      io.unobserve(e.target);
    });
  }, {threshold:.18, rootMargin:'0px 0px -40px'});
  document.querySelectorAll('.rv').forEach(el=> io.observe(el));

  /* accordion tunggal */
  const ds = document.querySelectorAll('details');
  ds.forEach(d=> d.addEventListener('toggle', ()=>{
    if(d.open) ds.forEach(o=>{ if(o!==d) o.open = false; });
  }));
})();
</script>
</body>
</html>
"""

PAGE = PAGE.replace("__WA__", WA)


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "Alfiliator/3.0"

    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE)
        elif self.path == "/health":
            self._send(200, '{"status":"online"}', "application/json")
        elif self.path == "/favicon.ico":
            self._send(204, "")
        else:
            self._send(404, "<h1 style='font-family:monospace;color:#22e3ff;"
                            "background:#05070d;padding:44px'>404 // NOT FOUND</h1>")

    do_HEAD = do_GET

    def log_message(self, fmt, *args):
        print("  %s -> %s" % (self.address_string(), fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    print("=" * 48)
    print("  ALFILIATOR // SERVICE NODE v3 AKTIF")
    print("  http://localhost:%d" % PORT)
    print("  Stop: ./stop.sh")
    print("=" * 48)
    try:
        with Server((HOST, PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Node dimatikan.")
