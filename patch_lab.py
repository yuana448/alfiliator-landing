#!/usr/bin/env python3
import os, sys, time, shutil, py_compile
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
APP = "app.py"
def must(s, a, n):
    if a not in s: sys.exit("[X] anchor hilang: " + n)
    return a
src = open(APP, encoding="utf-8").read()
if "import lab116" in src:
    sys.exit("[=] sudah tersambung, tidak ada yang diubah.")
stamp = time.strftime("%Y%m%d-%H%M%S")
shutil.copy2(APP, APP + ".bak-" + stamp)
print("[+] cadangan: app.py.bak-" + stamp)
CSS = r'''
.lab-card{border:1px solid var(--line);background:var(--panel);padding:20px}
.lab-in{display:flex;gap:8px;flex-wrap:wrap}
.lab-input{flex:1;min-width:170px;padding:12px 14px;background:var(--panel2);
  border:1px solid var(--line2);color:var(--ink);font:inherit;font-size:13px}
.gauge{height:6px;background:var(--line2);margin:16px 0 10px;overflow:hidden}
.gfill{height:100%;width:0;background:var(--gold);transition:width .5s,background .3s}
.gfill.ok{background:#3fdb9a}.gfill.warn{background:#f0c04a}.gfill.bad{background:#f0685f}
.lab-row{display:flex;align-items:baseline;gap:12px;font-family:'JetBrains Mono',monospace}
.lab-row b{font-size:26px;color:var(--gold2)}
.lab-row span{font-size:11px;color:var(--dim);letter-spacing:.1em}
.lab-list{margin-top:14px;display:grid;gap:6px}
.lab-item{font-size:12.2px;padding:8px 11px;border-left:2px solid var(--line2);
  background:var(--panel2);color:var(--muted);display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.lab-item b{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.1em}
.lab-item.ok{border-color:#3fdb9a}.lab-item.warn{border-color:#f0c04a}.lab-item.bad{border-color:#f0685f}
.lab-item a{color:var(--gold2);text-decoration:underline}
.lab-x{margin-left:auto;background:none;border:1px solid var(--line2);color:var(--dim);
  cursor:pointer;font-size:9.5px;padding:2px 7px}
.lab-note{font-size:11.5px;color:var(--dim);margin-top:16px;border-left:1px solid var(--gold);padding-left:14px}
.lab-tbl{width:100%;border-collapse:collapse;font-size:12.4px;border:1px solid var(--line2)}
.lab-tbl th,.lab-tbl td{padding:11px 13px;text-align:left;border-bottom:1px solid var(--line2)}
.lab-tbl th{font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);
  background:var(--panel2);font-weight:600}
.lab-tbl tr:last-child td{border-bottom:0}
@media(max-width:639px){.lab-tbl{display:block;overflow-x:auto}.lab-tbl th,.lab-tbl td{white-space:nowrap}}
'''
CARI = must(src, 'ROOMS.append(("/cari", "115", "Cari", "Pencarian cepat antar ruang."))', "ROOMS /cari")
WIRE = '''
import lab116 as _l116, lab117 as _l117, lab118 as _l118, lab119 as _l119, lab120 as _l120
for _m in (_l116, _l117, _l118, _l119, _l120):
    ROOMS.append(_m.META)
    B[_m.META[0]] = _m.BODY
'''
src = src.replace(CARI, CARI + WIRE, 1)

CSP = must(src, "connect-src 'self' https://api.venice.ai;", "connect-src")
src = src.replace(CSP,
    "connect-src 'self' https://api.venice.ai https://api.pwnedpasswords.com https://api.github.com;", 1)

HB = must(src, 'HEADBOOT = r"""', "HEADBOOT")
src = src.replace(HB, "EXTRA_CSS += r'''" + CSS + "'''\n\n" + HB, 1)

for a, b in (("114 Ruang", "120 Ruang"), ("114 RUANG", "120 RUANG"),
             ("114 ruang", "120 ruang"), ("114 rute", "120 rute")):
    src = src.replace(a, b)
print("[+] lima rute tersambung, CSP diperluas, CSS masuk")
open(APP, "w", encoding="utf-8").write(src)
py_compile.compile(APP, doraise=True)
print("[OK] app.py tertulis dan kompilasi lolos")
print("[i] jalankan: bash -c 'pkill -f app.py; python3 app.py &' lalu buka /health")
