import re, shutil, time, os, sys

SRC = "app.py"
if not os.path.exists(SRC) or os.path.getsize(SRC) < 20000:
    print("GAGAL: app.py tidak ada atau terlalu kecil (%d byte)" % (os.path.getsize(SRC) if os.path.exists(SRC) else 0))
    sys.exit(1)

stamp = time.strftime("%Y%m%d-%H%M%S")
shutil.copy2(SRC, "app.py.bak-" + stamp)
print("[i] cadangan: app.py.bak-" + stamp)

s = open(SRC, encoding="utf-8").read()
rep = []

def must(cond, msg):
    if not cond:
        print("GAGAL:", msg)
        sys.exit(1)

# ---------------------------------------------------------------- 1. CSS gerak
A_CSS = '\nHEADBOOT = r"""'
must(A_CSS in s, "anchor CSS tidak ketemu")

CSS2 = r'''
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

if "LAPIS GERAK v2" not in s:
    s = s.replace(A_CSS, "\nEXTRA_CSS += r'''" + CSS2 + "'''" + A_CSS, 1)
    rep.append("CSS gerak")

# ---------------------------------------------------------------- 2. JS gerak
A_JS = '\n})();\n"""'
must(A_JS in s, "anchor JS tidak ketemu")

JS2 = r'''
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
'''

if "lapis gerak v2" not in s:
    s = s.replace(A_JS, "\n" + JS2 + A_JS, 1)
    rep.append("JS gerak")

# ---------------------------------------------------------------- 3. papan 14
P14 = r'''
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
'''

pat = re.compile(r'B\["/mobile"\] = """.*?"\n\nB\["/integrasi"\]', re.S)
must(pat.search(s), "blok B[/mobile] tidak ketemu")
s = pat.sub(lambda m: 'B["/mobile"] = """\n' + P14 + '\n"""\n\nB["/integrasi"]', s, count=1)
rep.append("papan 14")

# ---------------------------------------------------------------- 4. t5/t6 dobel
DUP = '''  <div><b id="t5">18</b><span>antrean puncak</span></div>
  <div><b id="t6">7</b><span>gerbang aktif</span></div>
  <div><b id="t5">18</b><span>antrean puncak</span></div>
  <div><b id="t6">7</b><span>gerbang aktif</span></div>'''
if DUP in s:
    s = s.replace(DUP, '''  <div><b id="t5">18</b><span>antrean puncak</span></div>
  <div><b id="t6">7</b><span>gerbang aktif</span></div>''', 1)
    rep.append("t5/t6 dobel")

# ---------------------------------------------------------------- 5. label ruang
n = 0
for a, b in (("34 Ruang", "114 Ruang"), ("34 RUANG", "114 RUANG"),
             ("34 ruang", "114 ruang"), ("34 rute", "114 rute")):
    if a in s:
        n += s.count(a); s = s.replace(a, b)
if n:
    rep.append("label %d tempat" % n)

s = s.replace('\'{"status":"online","rooms":31}\'', '(\'{"status":"online","rooms":%d}\' % len(ROOMS))', 1)

open(SRC, "w", encoding="utf-8").write(s)
print("[ok] patch terpasang:", ", ".join(rep) if rep else "tidak ada perubahan")
print("[i] baris:", s.count("\n"))
