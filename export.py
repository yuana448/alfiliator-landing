import re, pathlib, shutil, json
from app import PAGES, BUILT, SEARCH_INDEX

out = pathlib.Path("docs")
shutil.rmtree(out, ignore_errors=True)
out.mkdir(parents=True, exist_ok=True)
(out / ".nojekyll").write_text("")

for f in pathlib.Path("static").iterdir():
    shutil.copy(f, out / f.name)

for path, _v in PAGES.items():
    slug = path.strip("/")
    prefix = "../" * (1 if slug else 0)
    h = re.sub(r'href="/([a-z]*)("|/)', lambda m: 'href="' + prefix + (m.group(1) + "/" if m.group(1) else "./") + '"', BUILT[path])
    h = h.replace('href="/favicon.svg"', 'href="' + prefix + 'favicon.svg"')
    h = h.replace('href="/icon.svg"', 'href="' + prefix + 'icon.svg"')
    h = h.replace('href="/manifest.webmanifest"', 'href="' + prefix + 'manifest.webmanifest"')
    h = h.replace('href="/index.json"', 'href="' + prefix + 'index.json"')
    h = h.replace('<link rel="canonical" href="' + prefix, '<link rel="canonical" href="https://yuana448.github.io/alfiliator-landing/' + prefix)
    t = out / slug if slug else out
    t.mkdir(parents=True, exist_ok=True)
    (t / "index.html").write_text(h, encoding="utf-8")

(out / "index.json").write_text(json.dumps(SEARCH_INDEX, ensure_ascii=False), encoding="utf-8")

n = BUILT["/"].replace('href="/', 'href="/alfiliator-landing/')
(out / "404.html").write_text(n, encoding="utf-8")
print("ekspor selesai:", len(PAGES), "halaman")
