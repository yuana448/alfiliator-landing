#!/usr/bin/env python3
import os, sys, time, shutil, py_compile
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
APP = "app.py"
def must(s, a, n):
    if a not in s: sys.exit("[X] anchor hilang: " + n)
    return a
src = open(APP, encoding="utf-8").read()
if "import lab116" in src:
    sys.exit("[=] sudah tersambung.")
shutil.copy2(APP, APP + ".bak2-" + time.strftime("%Y%m%d-%H%M%S"))

CARI = must(src, 'ROOMS.append(("/cari", "115", "Cari", "Pencarian cepat antar ruang."))', "ROOMS /cari")
src = src.replace(CARI, CARI + '''
import lab116 as _l116, lab117 as _l117, lab118 as _l118, lab119 as _l119, lab120 as _l120
for _m in (_l116, _l117, _l118, _l119, _l120):
    ROOMS.append(_m.META)
''', 1)

BD = must(src, "\nB = {}\n", "B = {}")
src = src.replace(BD, BD + '''
for _m in (_l116, _l117, _l118, _l119, _l120):
    B[_m.META[0]] = _m.BODY
''', 1)

CSP = must(src, "connect-src 'self' https://api.venice.ai;", "connect-src")
src = src.replace(CSP,
  "connect-src 'self' https://api.venice.ai https://api.pwnedpasswords.com https://api.github.com;", 1)

open(APP, "w", encoding="utf-8").write(src)
py_compile.compile(APP, doraise=True)
print("[OK] tersambung dan kompilasi lolos")
