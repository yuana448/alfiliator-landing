import re, pathlib, shutil
from app import PAGES, BUILT

out = pathlib.Path("docs")
shutil.rmtree(out / "layanan", ignore_errors=True)

for path, _v in PAGES.items():
    slug = path.strip("/")
    prefix = "../" * (1 if slug else 0)
    html = BUILT[path]

    def fix(m):
        t = m.group(1)
        return 'href="' + prefix + (t + "/" if t else "./") + '"'

    html = re.sub(r'href="/([a-z]*)"', fix, html)
    target = out / slug if slug else out
    target.mkdir(parents=True, exist_ok=True)
    (target / "index.html").write_text(html, encoding="utf-8")
    print("tulis", target / "index.html")

(out / ".nojekyll").write_text("")
print("selesai")
