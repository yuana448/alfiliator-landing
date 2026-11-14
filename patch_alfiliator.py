#!/usr/bin/env python3
"""Penambal ALFILIATOR v4 — pola longgar + diagnosa otomatis."""
import re, sys, os, json, zlib, struct, shutil, pathlib, datetime

HERE = pathlib.Path(__file__).resolve().parent
CAND = [pathlib.Path.home() / "alfiliator-landing", HERE, pathlib.Path.home() / "alfiliator-landing",
        pathlib.Path.home() / "storage/shared/alfiliator-landing",
        pathlib.Path("/sdcard/alfiliator-landing")]
ROOT = next((c for c in CAND if (c / "app.py").exists()), HERE)
os.chdir(ROOT)
APP, EXP, STATIC = ROOT / "app.py", ROOT / "export.py", ROOT / "static"
SITE = "https://yuana448.github.io/alfiliator-landing"
STAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
BK = ROOT / ("_backup_" + STAMP)
DRY = "--dry-run" in sys.argv
REPORT = []

def log(state, msg, note=""):
    REPORT.append((state, msg, note))

def src():
    return APP.read_text(encoding="utf-8")

def put(new):
    if not DRY: APP.write_text(new, encoding="utf-8")

def sub(pat, fn, label, count=1, flags=re.M):
    s = src()
    new, n = re.subn(pat, fn, s, count=count, flags=flags)
    if n: put(new); log("ok", label, "%d titik" % n)
    else: log("fail", label, "pola tidak cocok")

if "--revert" in sys.argv:
    c = sorted(ROOT.glob("_backup_*"))
    if not c: sys.exit("Tidak ada cadangan.")
    for f in c[-1].iterdir(): shutil.copy(f, ROOT / f.name)
    print("Dipulihkan dari", c[-1].name); sys.exit(0)

if not APP.exists(): sys.exit("app.py tidak ditemukan.")
print("Repo:", ROOT)
if APP.stat().st_size < 5000 or "BUILT" not in APP.read_text(encoding="utf-8"):
    sys.exit("app.py di %s bukan file asli (%d byte)." % (ROOT, APP.stat().st_size))

BK.mkdir(exist_ok=True)
for f in (APP, EXP):
    if f.exists(): shutil.copy(f, BK / f.name)
print("Cadangan:", BK.name)

# 1. BASE
if not re.search(r"^import os\b", src(), re.M):
    s = src()
    s = s.replace("\n", "\nimport os\n", 1) if s.startswith("#") else "import os\n" + s
    put(s); log("ok", "import os disisipkan")
sub(r"^BASE\s*=.*$",
    lambda m: 'BASE = (os.environ.get("BASE") or "http://localhost:%d" % PORT).rstrip("/")',
    "BASE mengikuti env")

# 2. statistik
def _stat(m):
    attrs = m.group(0)
    num = m.group(1)
    pre = re.search(r'data-p="([^"]*)"', attrs)
    suf = re.search(r'data-s="([^"]*)"', attrs)
    return re.sub(r">\s*0\s*</b>",
                  ">" + (pre.group(1) if pre else "") + num + (suf.group(1) if suf else "") + "</b>",
                  attrs)
sub(r'<b\b[^>]*data-c="(\d+)"[^>]*>\s*0\s*</b>', _stat, "statistik punya teks cadangan")

# 3. counter
sub(r"(t0\s*=\s*null;)", lambda m: m.group(1) + "b.textContent=pre+suf;", "counter tidak berkedip")

# 4. WhatsApp
sub(r"Halo_{2,}ALFILIATOR", lambda m: "Halo%20ALFILIATOR", "teks prefill WhatsApp")

# 5. jumlah ruang
sub(r"(?<![\d])30(\s+)(Ruang|ruang)", lambda m: "31" + m.group(1) + m.group(2), "label jumlah ruang")
sub(r"([\"']rooms[\"']\s*:\s*)30\b", lambda m: m.group(1) + "31", "health melaporkan 31")

# 6. og:image
def _og(m):
    s = src()
    s = re.sub(r'(property=["\']og:image["\'][^>]*content=["\'])[^"\']*', r'\g<1>/og.png', s, count=1)
    s = re.sub(r'(content=["\'])[^"\']*(["\'][^>]*property=["\']og:image)', r'\g<1>/og.png\g<2>', s, count=1)
    put(s); return m.group(0)
sub(r'og:image', _og, "og:image ke PNG")

REGIONAL = r"""
<style nonce="__NONCE__">
.reg{position:fixed;left:14px;bottom:14px;z-index:9999;font:500 13px/1.4 system-ui,sans-serif}
.reg-b{border:1px solid #8884;background:#111;color:#fff;border-radius:999px;padding:9px 14px;cursor:pointer;box-shadow:0 4px 18px #0004}
.reg-p{background:#111;color:#fff;border:1px solid #8884;border-radius:14px;padding:14px;margin-bottom:8px;width:242px;box-shadow:0 8px 30px #0006}
.reg-p[hidden]{display:none}
.reg-p label{display:block;font-size:11px;letter-spacing:.08em;text-transform:uppercase;opacity:.6;margin:10px 0 4px}
.reg-p label:first-child{margin-top:0}
.reg-p select,.reg-p input{width:100%;background:#1c1c1c;color:#fff;border:1px solid #8884;border-radius:8px;padding:7px 8px;font:inherit}
.reg-note{font-size:11px;opacity:.55;margin-top:9px;line-height:1.45}
.reg-x{margin-top:10px;width:100%;background:none;border:1px solid #8884;color:#fff;border-radius:8px;padding:7px;cursor:pointer;font:inherit}
@media print{.reg{display:none}}
</style>
<script nonce="__NONCE__">
(function(){
var KEY='alf_reg',rate=16300,lang='id',cur='IDR';
try{var st=JSON.parse(localStorage.getItem(KEY)||'{}');rate=+st.rate||rate;lang=st.lang||lang;cur=st.cur||cur}catch(e){}
var LANGS=[['id','Indonesia'],['en','English'],['ms','Melayu'],['zh','中文'],['ja','日本語'],['ar','العربية']];
var CURS=[['IDR','Rupiah'],['USD','Dolar AS'],['EUR','Euro'],['SGD','Dolar SG']];
var UNIT={rb:1e3,jt:1e6,miliar:1e9};
var T={
en:{'Beranda':'Home','Layanan':'Services','Harga':'Pricing','Portofolio':'Portfolio','Proses':'Process','Keamanan':'Security','Ketentuan':'Terms','Tanya':'FAQ','Kontak':'Contact','Mulai':'Start','Matriks':'Comparison','Teknologi Web':'Web Tech','Teknologi Mobile':'Mobile Tech','Integrasi':'Integrations','Infrastruktur':'Infrastructure','Perawatan':'Maintenance','Garansi':'Warranty','Legal':'Legal','Privasi':'Privacy','Syarat':'Terms of Use','Catatan':'Notes','Glosarium':'Glossary','Roadmap Celah':'Gap Roadmap','Kapasitas':'Capacity','Mitra':'Partners','Kolaborasi':'Collaboration','Status':'Status','Dokumentasi':'Docs','Cari':'Search','Proyek Selesai':'Projects Delivered','Klien Kembali':'Returning Clients','Respon':'Response','Kirim Brief':'Send Brief','Lihat Tarif':'See Rates','Konsultasi':'Consult','Formulir':'Form','Perangkat lunak yang dibuat ':'Software built ','benda mahal':'expensive things'},
ms:{'Beranda':'Utama','Layanan':'Perkhidmatan','Harga':'Harga','Portofolio':'Portfolio','Proses':'Proses','Keamanan':'Keselamatan','Ketentuan':'Terma','Tanya':'Soalan','Kontak':'Hubungi','Mulai':'Mula','Matriks':'Perbandingan','Teknologi Web':'Teknologi Web','Teknologi Mobile':'Teknologi Mudah Alih','Integrasi':'Integrasi','Infrastruktur':'Infrastruktur','Perawatan':'Penyelenggaraan','Garansi':'Jaminan','Legal':'Perundangan','Privasi':'Privasi','Syarat':'Syarat Guna','Catatan':'Nota','Glosarium':'Glosari','Roadmap Celah':'Peta Jurang','Kapasitas':'Kapasiti','Mitra':'Rakan','Kolaborasi':'Kerjasama','Status':'Status','Dokumentasi':'Dokumentasi','Cari':'Cari','Proyek Selesai':'Projek Siap','Klien Kembali':'Klien Berulang','Respon':'Respons','Kirim Brief':'Hantar Brief','Lihat Tarif':'Lihat Kadar','Konsultasi':'Rundingan','Formulir':'Borang','Perangkat lunak yang dibuat ':'Perisian yang dibina ','benda mahal':'barang mahal'},
zh:{'Beranda':'首页','Layanan':'服务','Harga':'价格','Portofolio':'作品','Proses':'流程','Keamanan':'安全','Ketentuan':'条款','Tanya':'常见问题','Kontak':'联系','Mulai':'开始','Matriks':'对比','Teknologi Web':'Web 技术','Teknologi Mobile':'移动技术','Integrasi':'集成','Infrastruktur':'基础设施','Perawatan':'维护','Garansi':'保修','Legal':'法律','Privasi':'隐私','Syarat':'使用条款','Catatan':'笔记','Glosarium':'术语表','Roadmap Celah':'差距路线图','Kapasitas':'产能','Mitra':'合作伙伴','Kolaborasi':'合作','Status':'状态','Dokumentasi':'文档','Cari':'搜索','Proyek Selesai':'完成项目','Klien Kembali':'回头客','Respon':'响应','Kirim Brief':'发送简报','Lihat Tarif':'查看费率','Konsultasi':'咨询','Formulir':'表单','Perangkat lunak yang dibuat ':'像昂贵物件一样打造的软件','benda mahal':'昂贵物件'},
ja:{'Beranda':'ホーム','Layanan':'サービス','Harga':'料金','Portofolio':'実績','Proses':'進め方','Keamanan':'セキュリティ','Ketentuan':'規約','Tanya':'よくある質問','Kontak':'お問い合わせ','Mulai':'はじめる','Matriks':'比較','Teknologi Web':'Web技術','Teknologi Mobile':'モバイル技術','Integrasi':'連携','Infrastruktur':'インフラ','Perawatan':'保守','Garansi':'保証','Legal':'法務','Privasi':'プライバシー','Syarat':'利用規約','Catatan':'記録','Glosarium':'用語集','Roadmap Celah':'改善ロードマップ','Kapasitas':'対応枠','Mitra':'パートナー','Kolaborasi':'協業','Status':'稼働状況','Dokumentasi':'ドキュメント','Cari':'検索','Proyek Selesai':'完了案件','Klien Kembali':'リピート顧客','Respon':'返信','Kirim Brief':'ブリーフを送る','Lihat Tarif':'料金を見る','Konsultasi':'相談','Formulir':'フォーム','Perangkat lunak yang dibuat ':'高級品のように作られたソフトウェア','benda mahal':'高級品'},
ar:{'Beranda':'الرئيسية','Layanan':'الخدمات','Harga':'الأسعار','Portofolio':'الأعمال','Proses':'سير العمل','Keamanan':'الأمان','Ketentuan':'الشروط','Tanya':'الأسئلة','Kontak':'اتصل','Mulai':'ابدأ','Matriks':'المقارنة','Teknologi Web':'تقنيات الويب','Teknologi Mobile':'تقنيات الجوال','Integrasi':'التكامل','Infrastruktur':'البنية التحتية','Perawatan':'الصيانة','Garansi':'الضمان','Legal':'القانوني','Privasi':'الخصوصية','Syarat':'شروط الاستخدام','Catatan':'ملاحظات','Glosarium':'المصطلحات','Roadmap Celah':'خطة الثغرات','Kapasitas':'الطاقة','Mitra':'الشركاء','Kolaborasi':'التعاون','Status':'الحالة','Dokumentasi':'الوثائق','Cari':'بحث','Proyek Selesai':'مشاريع منجزة','Klien Kembali':'عملاء عائدون','Respon':'الاستجابة','Kirim Brief':'أرسل موجزاً','Lihat Tarif':'انظر الأسعار','Konsultasi':'استشارة','Formulir':'نموذج','Perangkat lunak yang dibuat ':'برمجيات تُصنع كأنها قطعة فاخرة','benda mahal':'قطعة فاخرة'}
};
var box=document.createElement('div');box.className='reg';
var btn=document.createElement('button');btn.type='button';btn.className='reg-b';btn.textContent='ID · Rp';btn.setAttribute('aria-expanded','false');
var pan=document.createElement('div');pan.className='reg-p';pan.hidden=true;
function row(label,el){var l=document.createElement('label');l.textContent=label;pan.appendChild(l);pan.appendChild(el)}
var selL=document.createElement('select'),selC=document.createElement('select'),inp=document.createElement('input');
LANGS.forEach(function(p){var o=document.createElement('option');o.value=p[0];o.textContent=p[1];selL.appendChild(o)});
CURS.forEach(function(p){var o=document.createElement('option');o.value=p[0];o.textContent=p[1];selC.appendChild(o)});
inp.type='number';inp.min='1';inp.step='1';
row('Bahasa',selL);row('Mata uang',selC);row('Kurs 1 USD (IDR)',inp);
var note=document.createElement('div');note.className='reg-note';note.textContent='Konversi memakai kurs manual di atas. Angka asli tetap rupiah.';pan.appendChild(note);
var rst=document.createElement('button');rst.type='button';rst.className='reg-x';rst.textContent='Kembalikan ke IDR';pan.appendChild(rst);
box.appendChild(pan);box.appendChild(btn);document.body.appendChild(box);
var texts=[],prices=[];
function walk(n){
  if(n.nodeType===3){var v=n.nodeValue;if(v&&v.trim()){n.__o=v;texts.push(n);if(/Rp\.?\s?[\d.,]+\s?(miliar|jt|rb)?/i.test(v)){n.__p=v;prices.push(n)}}return}
  if(n.nodeType!==1)return;var t=n.tagName;if(t==='SCRIPT'||t==='STYLE'||t==='NOSCRIPT')return;
  if(n.classList&&n.classList.contains('reg'))return;
  for(var i=0;i<n.childNodes.length;i++)walk(n.childNodes[i]);
}
walk(document.body);
function fmt(idr){
  var v=cur==='IDR'?idr:(cur==='USD'?idr/rate:(cur==='EUR'?idr/rate/1.08:idr/rate*1.35));
  if(cur==='IDR')return 'Rp '+Math.round(v).toLocaleString('id-ID');
  var sym=cur==='USD'?'$':(cur==='EUR'?'€':'S$');
  return sym+Math.round(v).toLocaleString('en-US');
}
function apply(){
  var map=T[lang]||{};
  texts.forEach(function(n){var k=n.__o.trim(),tr=map[k];n.nodeValue=tr?n.__o.replace(k,tr):n.__o});
  prices.forEach(function(n){n.nodeValue=n.__p.replace(/Rp\.?\s?([\d.,]+)\s?(miliar|jt|rb)?/gi,function(_,d,u){
    var num=parseFloat(d.replace(/\./g,'').replace(',','.'))*(UNIT[(u||'').toLowerCase()]||1);
    return fmt(num);
  })});
  document.documentElement.lang=lang;document.documentElement.dir=(lang==='ar'?'rtl':'ltr');
  btn.textContent=lang.toUpperCase()+' · '+(cur==='IDR'?'Rp':cur);
  try{localStorage.setItem(KEY,JSON.stringify({lang:lang,cur:cur,rate:rate}))}catch(e){}
}
selL.value=lang;selC.value=cur;inp.value=rate;
selL.onchange=function(){lang=selL.value;apply()};
selC.onchange=function(){cur=selC.value;apply()};
inp.onchange=function(){rate=+inp.value||16300;apply()};
rst.onclick=function(){cur='IDR';selC.value='IDR';apply()};
btn.onclick=function(){pan.hidden=!pan.hidden;btn.setAttribute('aria-expanded',String(!pan.hidden))};
apply();
})();
</script>
"""

def widget():
    s = src()
    if "reg-p{position:fixed" in s or "reg{position:fixed" in s:
        log("skip", "widget", "sudah ada"); return
    for a in ("</body>", "</html>"):
        if a in s:
            put(s.replace(a, REGIONAL + a, 1)); log("ok", "widget sebelum " + a); return
    m = re.search(r"<body[^>]*>", s)
    if m:
        put(s[:m.end()] + REGIONAL + s[m.end():]); log("ok", "widget setelah <body>"); return
    log("fail", "widget", "tidak ada anchor body/html")
widget()

if not DRY:
    STATIC.mkdir(exist_ok=True)
    W, H = 1200, 630
    rows = []
    for y in range(H):
        row = bytearray(b"\x00")
        for x in range(W):
            t = (x / W + y / H) / 2
            row += bytes((int(12 + t * 36), int(12 + t * 26), int(16 + t * 58)))
        rows.append(bytes(row))
    def _chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xffffffff)
    png = (b"\x89PNG\r\n\x1a\n"
           + _chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
           + _chunk(b"IDAT", zlib.compress(b"".join(rows), 9))
           + _chunk(b"IEND", b""))
    (STATIC / "og.png").write_bytes(png)
    log("ok", "static/og.png dibuat")

NEW_EXPORT = '''import os, re, json, shutil, pathlib, datetime

SITE = "https://yuana448.github.io/alfiliator-landing"
os.environ["BASE"] = SITE

from app import PAGES, BUILT, SEARCH_INDEX

out = pathlib.Path("docs")
shutil.rmtree(out, ignore_errors=True)
out.mkdir(parents=True, exist_ok=True)
(out / ".nojekyll").write_text("")

for f in pathlib.Path("static").iterdir():
    shutil.copy(f, out / f.name)

stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
sw = out / "sw.js"
if sw.exists():
    sw.write_text(re.sub(r"(cache\\w*\\s*=\\s*['\\"])[^'\\"]*",
                         lambda m: m.group(1) + "alf-" + stamp,
                         sw.read_text(encoding="utf-8"), flags=re.I), encoding="utf-8")

ld = {"@context": "https://schema.org", "@type": "ProfessionalService",
      "name": "ALFILIATOR", "url": SITE + "/", "image": SITE + "/og.png",
      "description": "Atelier digital: web, Android, iOS, sistem internal, bot automation, dan audit keamanan.",
      "areaServed": "ID", "priceRange": "Rp 1.500.000+",
      "availableLanguage": ["id", "en", "ms", "zh", "ja", "ar"]}
LD = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\\n</head>"

for path in PAGES:
    slug = path.strip("/")
    prefix = "../" * (1 if slug else 0)
    h = BUILT[path]
    h = re.sub(r'href="/([a-z0-9\\-]*)("|/)',
               lambda m: 'href="' + prefix + (m.group(1) + "/" if m.group(1) else "./") + '"', h)
    for f in ("favicon.svg", "icon.svg", "manifest.webmanifest", "index.json"):
        h = h.replace('href="/' + f + '"', 'href="' + prefix + f + '"')
    canon = SITE + "/" + (slug + "/" if slug else "")
    h = re.sub(r'<link rel="canonical" href="[^"]*"',
               '<link rel="canonical" href="' + canon + '"', h)
    h = re.sub(r'<meta property="og:image" content="[^"]*"',
               '<meta property="og:image" content="' + SITE + '/og.png">', h)
    if 'property="og:url"' not in h:
        h = h.replace("</head>", '<meta property="og:url" content="' + canon + '">\\n</head>', 1)
    if "application/ld+json" not in h:
        h = h.replace("</head>", LD, 1)
    h = h.replace('nonce="__NONCE__"', "")
    t = out / slug if slug else out
    t.mkdir(parents=True, exist_ok=True)
    (t / "index.html").write_text(h, encoding="utf-8")

today = datetime.date.today().isoformat()
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in PAGES:
    sm.append("<url><loc>%s%s</loc><lastmod>%s</lastmod></url>" % (SITE, u, today))
sm.append("</urlset>")

(out / "index.json").write_text(json.dumps(SEARCH_INDEX, ensure_ascii=False), encoding="utf-8")
(out / "robots.txt").write_text(
    "User-agent: *\\nAllow: /\\nDisallow: /health/\\nDisallow: /index.json\\n"
    "Sitemap: " + SITE + "/sitemap.xml\\n", encoding="utf-8")
(out / "sitemap.xml").write_text("\\n".join(sm), encoding="utf-8")
(out / ".well-known").mkdir(exist_ok=True)
(out / ".well-known" / "security.txt").write_text(
    "Contact: mailto:support@alfiliator.id\\nExpires: 2027-12-31T23:59:00.000Z\\n"
    "Preferred-Languages: id, en\\nCanonical: " + SITE + "/.well-known/security.txt\\n",
    encoding="utf-8")
(out / "health").mkdir(exist_ok=True)
(out / "health" / "index.html").write_text(
    json.dumps({"status": "ok", "rooms": len(PAGES), "mode": "static"}), encoding="utf-8")

mf = out / "manifest.webmanifest"
if mf.exists():
    try:
        d = json.loads(mf.read_text(encoding="utf-8"))
        d["lang"], d["dir"] = "id", "ltr"
        mf.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

n = BUILT["/"].replace('href="/', 'href="/alfiliator-landing/')
n = re.sub(r'<link rel="canonical"[^>]*>', "", n)
n = n.replace('nonce="__NONCE__"', "")
n = re.sub(r"<title>[^<]*</title>",
           "<title>Halaman tidak ditemukan — ALFILIATOR</title>", n, count=1)
n = n.replace("<head>", '<head>\\n<meta name="robots" content="noindex">', 1)
banner = ('<div style="margin:0;padding:16px 22px;background:#b3261e;color:#fff;'
          'font:600 15px/1.5 system-ui,sans-serif">404 — Halaman tidak ditemukan. '
          '<a href="/alfiliator-landing/" style="color:#fff">Kembali ke beranda</a></div>')
n = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + banner, n, count=1)
(out / "404.html").write_text(n, encoding="utf-8")

print("ekspor selesai:", len(PAGES), "halaman")
'''
if not DRY: EXP.write_text(NEW_EXPORT, encoding="utf-8")
log("ok", "export.py ditulis ulang")

gi = ROOT / ".gitignore"
cur = gi.read_text(encoding="utf-8") if gi.exists() else ""
add = [x for x in ("__pycache__/", "*.pyc", ".server.pid", "server.log", "_backup_*/") if x not in cur]
if add and not DRY:
    gi.write_text(cur.rstrip() + "\n" + "\n".join(add) + "\n", encoding="utf-8")
if add: log("ok", ".gitignore diperluas")

print("\n=== LAPORAN ===")
for state, msg, note in REPORT:
    print({"ok": "[ OK ]", "skip": "[SKIP]", "fail": "[GAGAL]"}[state], msg, ("— " + note) if note else "")
bad = [r for r in REPORT if r[0] == "fail"]

if bad:
    print("\n=== DIAGNOSA app.py ===")
    s = src()
    print("ukuran:", len(s), "byte | baris:", s.count(chr(10)))
    for label, pat in (("BASE", r"^BASE.{0,80}"), ("data-c", r"data-c.{0,60}"),
                       ("t0=null", r"t0\s*=\s*null.{0,40}"), ("Halo", r"Halo.{0,40}"),
                       ("ruang", r"\d+\s*[Rr]uang"), ("rooms", r"[\"']rooms[\"'].{0,20}"),
                       ("og", r"og:image.{0,60}"), ("body", r"</body>|</html>")):
        m = re.search(pat, s, re.M)
        print(("- " + label + ": ").ljust(12), repr(m.group(0)[:80]) if m else "TIDAK ADA")
    print("\nKirim keluaran bagian DIAGNOSA ini.")

print("\n%d berhasil, %d gagal." % (len(REPORT) - len(bad), len(bad)))
if bad: print("Pulihkan: python3 patch_alfiliator.py --revert")
sys.exit(1 if bad else 0)
