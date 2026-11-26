# lab117.py — PassGuard v2: generator, meter, cek bocor, brankas, riwayat
META = ("/passguard", "117", "PassGuard", "Buat dan uji sandi, cek kebocoran, simpan terenkripsi.")

BODY = r'''
<div class="wrap pghead"><div class="kick">117 · Lab Sandi</div>
<h1>PassGuard, <em>dibuat lalu diuji</em>.</h1>
<p class="lead">Pembuat sandi acak kriptografis, meter kekuatan, cek kebocoran k-anonim, brankas AES-GCM.</p></div>
<section><div class="wrap">
<div class="lab-card">
  <div class="lab-in">
    <input id="gen" class="lab-input mono" readonly value="">
    <button id="gr" class="btn solid" type="button">Buat</button>
    <button id="gc" class="btn ghost" type="button">Salin</button>
  </div>
  <div class="lab-in" style="margin-top:12px">
    <label class="lab-input" style="display:flex;gap:8px;align-items:center;font-size:11.5px;color:var(--muted)">
      Panjang <input id="gl" type="range" min="8" max="48" value="20" style="flex:1">
      <b id="glv" class="mono" style="color:var(--gold)">20</b>
    </label>
  </div>
  <div class="lab-in" style="margin-top:8px">
    <label class="lab-item" style="border:1px solid var(--line2)"><input id="g1" type="checkbox" checked> huruf besar</label>
    <label class="lab-item" style="border:1px solid var(--line2)"><input id="g2" type="checkbox" checked> angka</label>
    <label class="lab-item" style="border:1px solid var(--line2)"><input id="g3" type="checkbox" checked> simbol</label>
    <label class="lab-item" style="border:1px solid var(--line2)"><input id="g4" type="checkbox"> frasa kata</label>
  </div>
  <div id="gq" style="margin-top:14px"></div>
</div>
<p class="lab-note">Acak memakai crypto.getRandomValues. Kode QR hanya dikirim ke api.qrserver.com bila Anda menekannya.</p>
</div></section>
<section><div class="wrap">
<h2 style="margin-top:34px">Uji sandi sendiri</h2><div class="hr"></div>
<div class="lab-card">
  <div class="lab-in">
    <input id="pu" class="lab-input" type="text" placeholder="Ketik sandi uji" autocomplete="off" spellcheck="false">
    <button id="pc" class="btn solid" type="button">Cek Kebocoran</button>
  </div>
  <div class="gauge"><div class="gfill" id="pg"></div></div>
  <div class="lab-row"><b id="pv">&mdash;</b><span id="pl">Kekuatan belum diukur</span></div>
  <p class="lab-note" id="pe">Entropi 0 bit.</p>
  <div id="po" class="lab-list"></div>
</div>
</div></section>
<section><div class="wrap">
<h2 style="margin-top:34px">Brankas lokal</h2><div class="hr"></div>
<div class="lab-card">
  <div class="lab-in">
    <input id="vm" class="lab-input" type="password" placeholder="Sandi induk brankas" autocomplete="off">
    <button id="vopen" class="btn solid" type="button">Buka</button>
  </div>
  <div id="vbody" hidden>
    <div class="lab-in" style="margin-top:12px">
      <input id="vn" class="lab-input" placeholder="Nama layanan" autocomplete="off">
      <input id="vp" class="lab-input" type="password" placeholder="Sandi disimpan">
      <button id="vadd" class="btn ghost" type="button">Tambah</button>
    </div>
    <div id="vlist" class="lab-list"></div>
  </div>
</div>
<p class="lab-note">PBKDF2 150.000 putaran + AES-GCM 256. Sandi induk tidak disimpan.</p>
</div></section>
<section><div class="wrap">
<h2 style="margin-top:34px">Riwayat buatan</h2><div class="hr"></div>
<div id="hrl" class="lab-list"></div>
</div></section>
<script nonce="__NONCE__">
    try{ a=JSON.parse(localStorage.getItem(K)||'[]'); }catch(e){}
    a.unshift(s); a=a.slice(0,10);
    localStorage.setItem(K, JSON.stringify(a)); draw();
  }
  function draw(){
    var h=document.getElementById('hrl'); if(!h) return;
    var a=[]; try{ a=JSON.parse(localStorage.getItem(K)||'[]'); }catch(e){}
    h.innerHTML='';
    if(!a.length){ h.innerHTML='<div class="lab-item">Belum ada.</div>'; return; }
    a.forEach(function(x){
      var d=document.createElement('div'); d.className='lab-item ok';
      d.innerHTML='<b class="mono">'+x.replace(/</g,'&lt;')+'</b>';
      h.appendChild(d);
    });
  }
  var u=document.getElementById('pu'), g=document.getElementById('pg'),
      v=document.getElementById('pv'), l=document.getElementById('pl'), e=document.getElementById('pe');
  var SETS=[[/a-z/,26],[/A-Z/,26],[/0-9/,10],[/[^A-Za-z0-9]/,33]];
  function measure(){
    var s=u.value; if(!s){ g.style.width='0'; v.textContent='\u2014';
      l.textContent='Kekuatan belum diukur'; e.textContent='Entropi 0 bit.'; return; }
    var p=0, cls=0;
    SETS.forEach(function(x){ if(x[0].test(s)){ p+=x[1]; cls++; } });
    var bits=Math.round(s.length*Math.log2(p||1)), n=0;
    if(s.length>=8) n++; if(s.length>=12) n++; if(s.length>=16) n++;
    if(cls>=2) n++; if(cls>=3) n++; if(cls>=4) n++;
    if(/^\d+$/.test(s)) n--; if(/(.)\1{2,}/.test(s)) n--;
    n=Math.max(0,Math.min(6,n));
    g.style.width=[8,24,42,58,74,88,100][n]+'%';
    g.className='gfill '+(n>=5?'ok':n>=3?'warn':'bad');
    v.textContent=bits;
    e.textContent='Entropi '+bits+' bit, '+s.length+' karakter, '+cls+' kelas.';
    l.textContent=bits<40?'Lemah':bits<60?'Sedang':bits<80?'Kuat':'Sangat kuat';
  }
  u.addEventListener('input', measure);
  var o=document.getElementById('po');
  document.getElementById('pc').onclick=function(){
    o.innerHTML=''; var s=u.value;
    if(!s){ o.innerHTML='<div class="lab-item warn"><b>!</b> Isi sandi dulu.</div>'; return; }
    if(!window.crypto||!crypto.subtle){ o.innerHTML='<div class="lab-item warn"><b>!</b> Butuh HTTPS.</div>'; return; }
    o.innerHTML='<div class="lab-item"><b>&hellip;</b> Menghitung SHA-1</div>';
    crypto.subtle.digest('SHA-1', new TextEncoder().encode(s)).then(function(buf){
      var hex=[].map.call(new Uint8Array(buf), function(x){ return ('0'+x.toString(16)).slice(-2); }).join('').toUpperCase();
      var pre=hex.slice(0,5), suf=hex.slice(5);
      return fetch('https://api.pwnedpasswords.com/range/'+pre).then(function(r){
        if(!r.ok) throw new Error('HTTP '+r.status);
        return r.text();
      }).then(function(t){
        o.innerHTML=''; var hit=0;
        t.split('\n').forEach(function(row){
          var p=row.trim().split(':');
          if(p[0]===suf) hit=parseInt(p[1],10)||0;
        });
        o.innerHTML=hit
          ? '<div class="lab-item bad"><b>BOCOR</b> '+hit.toLocaleString('id-ID')+' kali ditemukan.</div>'
          : '<div class="lab-item ok"><b>BERSIH</b> Tidak ditemukan.</div>';
      });
    }).catch(function(err){ o.innerHTML='<div class="lab-item warn"><b>GAGAL</b> '+err.message+'</div>'; });
  };
  var mem=null, key=null, VK='alf.vault';
  function b64(b){ return btoa(String.fromCharCode.apply(null, new Uint8Array(b))); }
  function ub(s){ return new Uint8Array(atob(s).split('').map(function(c){ return c.charCodeAt(0); })); }
  function dk(m, salt){
    return crypto.subtle.importKey('raw', new TextEncoder().encode(m), 'PBKDF2', false, ['deriveKey'])
      .then(function(k){ return crypto.subtle.deriveKey({name:'PBKDF2', salt:salt, iterations:150000, hash:'SHA-256'},
        k, {name:'AES-GCM', length:256}, false, ['encrypt','decrypt']); });
  }
  function vdraw(){
    var box=document.getElementById('vlist'); box.innerHTML='';
    if(!mem||!mem.length){ box.innerHTML='<div class="lab-item">Brankas kosong.</div>'; return; }
    mem.forEach(function(it, i){
      var d=document.createElement('div'); d.className='lab-item ok';
      d.innerHTML='<b>'+it.n.replace(/</g,'&lt;')+'</b> <span class="mono">'+it.p.replace(/</g,'&lt;')+'</span>';
      var x=document.createElement('button'); x.className='lab-x'; x.textContent='hapus';
      x.onclick=function(){ mem.splice(i,1); vsave(); };
      d.appendChild(x); box.appendChild(d);
    });
  }
  function vsave(){
    if(!key) return;
    var salt=crypto.getRandomValues(new Uint8Array(16)), iv=crypto.getRandomValues(new Uint8Array(12));
    crypto.subtle.encrypt({name:'AES-GCM', iv:iv}, key, new TextEncoder().encode(JSON.stringify(mem)))
      .then(function(ct){ localStorage.setItem(VK, JSON.stringify({s:b64(salt), i:b64(iv), c:b64(ct)})); vdraw(); });
  }
  document.getElementById('vopen').onclick=function(){
    var m=document.getElementById('vm').value; if(!m) return;
    var body=document.getElementById('vbody'), raw=localStorage.getItem(VK);
    if(!raw){
      var salt=crypto.getRandomValues(new Uint8Array(16));
      dk(m, salt).then(function(k){ key=k; mem=[]; body.hidden=false;
        localStorage.setItem(VK, JSON.stringify({s:b64(salt), i:'', c:''})); vdraw(); });
      return;
    }
    var ob=JSON.parse(raw);
    dk(m, ub(ob.s)).then(function(k){
      return crypto.subtle.decrypt({name:'AES-GCM', iv:ub(ob.i)}, k, ub(ob.c))
        .then(function(pt){ key=k; mem=JSON.parse(new TextDecoder().decode(pt)); body.hidden=false; vdraw(); });
    }).catch(function(){ alert('Sandi induk salah.'); });
  };
  document.getElementById('vadd').onclick=function(){
    var n=document.getElementById('vn').value.trim(), p=document.getElementById('vp').value;
    if(!n||!p) return; mem.push({n:n, p:p});
    document.getElementById('vn').value=''; document.getElementById('vp').value=''; vsave();
  };
  document.getElementById('gr').onclick=make;
  document.getElementById('gc').onclick=function(){
    if(!out.value) return;
    if(navigator.clipboard) navigator.clipboard.writeText(out.value);
  };
  len.addEventListener('input', function(){ lv.textContent=len.value; });
  draw(); make();
})();
</script>
'''
