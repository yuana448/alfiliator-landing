import os, re, json, shutil, pathlib, datetime

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
    sw.write_text(re.sub(r"(cache\w*\s*=\s*['\"])[^'\"]*",
                         lambda m: m.group(1) + "alf-" + stamp,
                         sw.read_text(encoding="utf-8"), flags=re.I), encoding="utf-8")

ld = {"@context": "https://schema.org", "@type": "ProfessionalService",
      "name": "ALFILIATOR", "url": SITE + "/", "image": SITE + "/og.png",
      "description": "Atelier digital: web, Android, iOS, sistem internal, bot automation, dan audit keamanan.",
      "areaServed": "ID", "priceRange": "Rp 1.500.000+",
      "availableLanguage": ["id", "en", "ms", "zh", "ja", "ar"]}
LD = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n</head>"

for path in PAGES:
    slug = path.strip("/")
    prefix = "../" * (1 if slug else 0)
    h = BUILT[path]
    h = re.sub(r'href="/([a-z0-9\-]*)("|/)',
               lambda m: 'href="' + prefix + (m.group(1) + "/" if m.group(1) else "./") + '"', h)
    for f in ("favicon.svg", "icon.svg", "manifest.webmanifest", "index.json"):
        h = h.replace('href="/' + f + '"', 'href="' + prefix + f + '"')
    canon = SITE + "/" + (slug + "/" if slug else "")
    h = re.sub(r'<link rel="canonical" href="[^"]*"',
               '<link rel="canonical" href="' + canon + '"', h)
    h = re.sub(r'<meta property="og:image" content="[^"]*"',
               '<meta property="og:image" content="' + SITE + '/og.png">', h)
    if 'property="og:url"' not in h:
        h = h.replace("</head>", '<meta property="og:url" content="' + canon + '">\n</head>', 1)
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
    "User-agent: *\nAllow: /\nDisallow: /health/\nDisallow: /index.json\n"
    "Sitemap: " + SITE + "/sitemap.xml\n", encoding="utf-8")
(out / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
(out / ".well-known").mkdir(exist_ok=True)
(out / ".well-known" / "security.txt").write_text(
    "Contact: mailto:support@alfiliator.id\nExpires: 2027-12-31T23:59:00.000Z\n"
    "Preferred-Languages: id, en\nCanonical: " + SITE + "/.well-known/security.txt\n",
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
n = n.replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1)
banner = ('<div style="margin:0;padding:16px 22px;background:#b3261e;color:#fff;'
          'font:600 15px/1.5 system-ui,sans-serif">404 — Halaman tidak ditemukan. '
          '<a href="/alfiliator-landing/" style="color:#fff">Kembali ke beranda</a></div>')
n = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + banner, n, count=1)
(out / "404.html").write_text(n, encoding="utf-8")

print("ekspor selesai:", len(PAGES), "halaman")
