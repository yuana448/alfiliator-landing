import re, shutil, time, os, sys

SRC = "app.py"
if not os.path.exists(SRC) or os.path.getsize(SRC) < 20000:
    print("GAGAL: app.py tidak ada atau terlalu kecil")
    sys.exit(1)
stamp = time.strftime("%Y%m%d-%H%M%S")
shutil.copy2(SRC, "app.py.bak-" + stamp)
print("[i] cadangan: app.py.bak-" + stamp)

s = open(SRC, encoding="utf-8").read()
rep = []

def must(c, m):
    if not c:
        print("GAGAL:", m); sys.exit(1)

# ------------------------------------------------------------------ 1. CSS
A = '\nHEADBOOT = r"""'
must(A in s, "anchor CSS tidak ketemu")

CSS3 = r'''
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

if "PUSAT SETELAN" not in s:
    s = s.replace(A, "\nEXTRA_CSS += r'''" + CSS3 + "'''" + A, 1)
    rep.append("CSS setelan")

# ------------------------------------------------------------------ 2. HEADBOOT
HB = "R.setAttribute('data-grid',L.getItem('alf.grid')||'off');})();"
must(HB in s, "anchor HEADBOOT tidak ketemu")
NEWHB = (
"R.setAttribute('data-font',L.getItem('alf.font')||'sora');"
"R.setAttribute('data-head',L.getItem('alf.head')||'normal');"
"R.setAttribute('data-lh',L.getItem('alf.lh')||'n');"
"R.setAttribute('data-ls',L.getItem('alf.ls')||'n');"
"R.setAttribute('data-bw',L.getItem('alf.bw')||'1');"
"R.setAttribute('data-tbl',L.getItem('alf.tbl')||'garis');"
"R.setAttribute('data-btn',L.getItem('alf.btn')||'kotak');"
"R.setAttribute('data-nav',L.getItem('alf.nav')||'menempel');"
"R.setAttribute('data-pat',L.getItem('alf.pat')||'mati');"
"R.setAttribute('data-sh',L.getItem('alf.sh')||'lembut');"
"R.setAttribute('data-blur',L.getItem('alf.blur')||'nyala');"
"R.setAttribute('data-cur',L.getItem('alf.cur')||'cincin');"
"R.setAttribute('data-par',L.getItem('alf.par')||'lembut');"
"R.setAttribute('data-acc',L.getItem('alf.acc')||'bawaan');"
"R.setAttribute('data-sel',L.getItem('alf.sel')||'bawaan');"
"R.setAttribute('data-link',L.getItem('alf.link')||'biasa');"
"R.setAttribute('data-focus',L.getItem('alf.focus')||'mati');"
"var _cc=L.getItem('alf.custom');if(_cc){R.style.setProperty('--gold',_cc);"
"R.style.setProperty('--gold2',_cc);"
"R.style.setProperty('--glow','color-mix(in srgb,'+_cc+' 40%, transparent)');"
"R.style.setProperty('--line','color-mix(in srgb,'+_cc+' 18%, transparent)');}})();"
)
if "alf.font" not in s:
    s = s.replace(HB, NEWHB, 1)
    rep.append("HEADBOOT")

# ------------------------------------------------------------------ 3. panel
SW = "".join('<button data-t="%s" style="background:%s" aria-label="%s"></button>' % (k, c, k)
             for k, c in [("emas","#d4af7a"),("sian","#38d6e8"),("violet","#a48bff"),
                          ("zamrud","#3fdb9a"),("rose","#f0799c"),("mono","#cfcfcf"),
                          ("indigo","#7d8cff"),("toska","#3fd6c4"),("kuning","#f0c04a"),
                          ("merah","#f0685f"),("langit","#5cb8f5"),("limau","#a8e05a"),
                          ("magenta","#ef6ad4"),("baja","#9fb0c4"),("kertas","#f6f3ec"),
                          ("kapur","#eaf1f5"),("senja","#ff8a4c"),("anggur","#b4527a")])

def seg(attr, opts):
    return '<div class="seg">' + "".join(
        '<button data-%s="%s"%s>%s</button>' % (attr, v, ' aria-pressed="true"' if d else "", t)
        for v, t, d in opts) + '</div>'

PANEL = '''<aside id="panel" aria-label="Setelan tampilan">
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
      <div class="prow"><h3>Paket desain</h3>''' + seg("pk", [("atelier","Atelier",1),("editorial","Editorial",0),("terminal","Terminal",0),("lembut","Lembut",0),("tegas","Tegas",0)]) + '''</div>
      <div class="prow"><h3>Warna aksen</h3><div class="sw">''' + SW + '''</div></div>
      <div class="prow"><h3>Warna sendiri</h3><input type="color" id="pcust" value="#d4af7a" aria-label="Warna sendiri"></div>
      <div class="prow"><h3>Intensitas aksen</h3>''' + seg("acc", [("bawaan","Bawaan",1),("nyala","Nyala",0),("pudar","Pudar",0)]) + '''</div>
      <div class="prow"><h3>Warna seleksi</h3>''' + seg("sel", [("bawaan","Bawaan",1),("emas","Emas",0),("invers","Invers",0)]) + '''</div>
      <div class="prow"><h3>Kontras</h3>''' + seg("cn", [("n","Normal",1),("t","Tinggi",0)]) + '''</div>
      <div class="prow"><h3>Transparansi panel</h3>''' + seg("tr", [("s","Solid",1),("t","Tipis",0)]) + '''</div>
    </section>
    <section class="pgrp" data-g="huruf">
      <div class="prow"><h3>Pasangan huruf</h3>''' + seg("font", [("sora","Sora",1),("playfair","Serif",0),("mono","Mono",0),("sistem","Sistem",0)]) + '''</div>
      <div class="prow"><h3>Gaya judul</h3>''' + seg("head", [("normal","Normal",1),("serif","Serif",0),("mono","Mono",0),("kapital","Kapital",0),("renggang","Renggang",0)]) + '''</div>
      <div class="prow"><h3>Ukuran huruf</h3>''' + seg("fs", [("s","Kecil",0),("m","Normal",1),("l","Besar",0)]) + '''</div>
      <div class="prow"><h3>Tinggi baris</h3>''' + seg("lh", [("rapat","Rapat",0),("n","Normal",1),("renggang","Renggang",0)]) + '''</div>
      <div class="prow"><h3>Jarak huruf</h3>''' + seg("ls", [("n","Normal",1),("renggang","Renggang",0),("sangat","Sangat",0)]) + '''</div>
    </section>
    <section class="pgrp" data-g="tata">
      <div class="prow"><h3>Lebar konten</h3>''' + seg("wd", [("s","Sempit",0),("n","Normal",1),("l","Lebar",0),("p","Penuh",0)]) + '''</div>
      <div class="prow"><h3>Kerapatan</h3>''' + seg("dn", [("l","Renggang",0),("n","Normal",1),("r","Rapat",0)]) + '''</div>
      <div class="prow"><h3>Sudut</h3>''' + seg("rd", [("k","Kotak",1),("n","Normal",0),("b","Bulat",0),("p","Pil",0)]) + '''</div>
      <div class="prow"><h3>Tebal garis</h3>''' + seg("bw", [("0","Tanpa",0),("1","Normal",1),("2","Tebal",0)]) + '''</div>
      <div class="prow"><h3>Gaya tabel</h3>''' + seg("tbl", [("garis","Garis",1),("belang","Belang",0),("minimal","Minimal",0)]) + '''</div>
      <div class="prow"><h3>Bentuk tombol</h3>''' + seg("btn", [("kotak","Kotak",1),("bulat","Bulat",0),("pil","Pil",0)]) + '''</div>
      <div class="prow"><h3>Navigasi</h3>''' + seg("nav", [("menempel","Menempel",1),("sembunyi","Sembunyi",0),("diam","Diam",0)]) + '''</div>
      <div class="prow"><h3>Garis bantu</h3>''' + seg("gd", [("off","Mati",1),("on","Aktif",0)]) + '''</div>
    </section>
    <section class="pgrp" data-g="efek">
      <div class="prow"><h3>Animasi</h3>''' + seg("mt", [("on","Aktif",1),("off","Mati",0)]) + '''</div>
      <div class="prow"><h3>Kekuatan parallax</h3>''' + seg("par", [("mati","Mati",0),("lembut","Lembut",1),("kuat","Kuat",0)]) + '''</div>
      <div class="prow"><h3>Pola latar</h3>''' + seg("pat", [("mati","Mati",1),("mesh","Mesh",0),("titik","Titik",0),("garis","Garis",0)]) + '''</div>
      <div class="prow"><h3>Tekstur butir</h3>''' + seg("gr", [("on","Aktif",1),("off","Mati",0)]) + '''</div>
      <div class="prow"><h3>Bayangan</h3>''' + seg("sh", [("off","Mati",0),("lembut","Lembut",1),("tegas","Tegas",0)]) + '''</div>
      <div class="prow"><h3>Buram kaca</h3>''' + seg("blur", [("nyala","Aktif",1),("off","Mati",0)]) + '''</div>
      <div class="prow"><h3>Kursor</h3>''' + seg("cur", [("cincin","Cincin",1),("titik","Titik",0),("mati","Mati",0)]) + '''</div>
      <div class="prow"><h3>Mode fokus</h3>''' + seg("focus", [("mati","Mati",1),("on","Aktif",0)]) + '''</div>
      <div class="prow"><h3>Gaya tautan</h3>''' + seg("link", [("biasa","Biasa",1),("garis","Garis bawah",0)]) + '''</div>
    </section>
    <section class="pgrp" data-g="suara">
      <div class="prow"><h3>Bunyi antarmuka</h3>''' + seg("sd", [("on","Aktif",1),("off","Mati",0)]) + '''</div>
      <div class="prow"><h3>Volume</h3><input id="pvol" class="range" type="range" min="0" max="100" step="5" value="45" aria-label="Volume bunyi"></div>
      <div class="prow"><h3>Nada</h3>''' + seg("pk2", [("lembut","Lembut",1),("tajam","Tajam",0),("rendah","Rendah",0)]) + '''</div>
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
</aside>'''

pat = re.compile(r'<aside id="panel".*?</aside>', re.S)
must(pat.search(s), "blok panel tidak ketemu")
s = pat.sub(lambda m: PANEL, s, count=1)
rep.append("panel baru")

# ------------------------------------------------------------------ 4. bunyi
T = "g.gain.exponentialRampToValueAtTime(vol || 0.045, t + 0.012);"
if T in s:
    s = s.replace(T, "var VV=(+localStorage.getItem('alf.vol')||45)/100;\n"
        "      g.gain.exponentialRampToValueAtTime(Math.max(0.0002,(vol||0.045)*VV), t + 0.012);", 1)
    rep.append("volume")

OLD = """  function sHover(){ tone(1180, 0.06, 'triangle', 0.022); }
  function sClick(){ tone(520, 0.09, 'sine', 0.05); setTimeout(function(){ tone(780, 0.1, 'sine', 0.04); }, 70); }
  function sGood(){ tone(660, 0.12, 'sine', 0.05); setTimeout(function(){ tone(990, 0.16, 'sine', 0.045); }, 90); }"""
NEW = """  function PKT(){ return localStorage.getItem('alf.pack')||'lembut'; }
  function sHover(){ var p=PKT(); tone(p==='tajam'?1720:p==='rendah'?720:1180, 0.06, 'triangle', 0.022); }
  function sClick(){ var p=PKT(), f=p==='tajam'?820:p==='rendah'?340:520;
    tone(f, 0.09, 'sine', 0.05); setTimeout(function(){ tone(f*1.5, 0.1, 'sine', 0.04); }, 70); }
  function sGood(){ var p=PKT(), f=p==='tajam'?980:p==='rendah'?420:660;
    tone(f, 0.12, 'sine', 0.05); setTimeout(function(){ tone(f*1.5, 0.16, 'sine', 0.045); }, 90); }"""
if OLD in s:
    s = s.replace(OLD, NEW, 1)
    rep.append("nada bunyi")

# ------------------------------------------------------------------ 5. JS panel
A2 = '\n})();\n"""'
must(A2 in s, "anchor JS tidak ketemu")

JS3 = r'''
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
'''

if "pusat setelan" not in s:
    s = s.replace(A2, "\n" + JS3 + A2, 1)
    rep.append("JS setelan")

open(SRC, "w", encoding="utf-8").write(s)
print("[ok] terpasang:", ", ".join(rep))
