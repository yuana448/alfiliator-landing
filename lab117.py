# lab117.py — PassGuard: meter kekuatan, cek bocor k-anonim, brankas lokal
META = ("/passguard", "117", "PassGuard", "Uji kekuatan sandi, cek kebocoran, simpan di brankas terenkripsi.")

BODY = r'''
<div class="wrap pghead"><div class="kick">117 · Lab Sandi</div>
<h1>PassGuard, <em>sandi diuji sebelum dipakai</em>.</h1>
<p class="lead">Meter kekuatan, cek kebocoran lewat SHA-1 k-anonim, dan brankas AES-GCM. Sandi asli tidak pernah dikirim utuh.</p></div>
<section><div class="wrap">
<div class="lab-card">
  <div class="lab-in">
    <input id="pu" class="lab-input" type="text" placeholder="Ketik sandi uji" autocomplete="off" spellcheck="false">
    <button id="pt" class="btn ghost" type="button">Tampil</button>
  </div>
  <div class="gauge"><div class="gfill" id="pg"></div></div>
  <div class="lab-row"><b id="pv">&mdash;</b><span id="pl">Kekuatan belum diukur</span></div>
  <p class="lab-note" id="pe">Entropi 0 bit.</p>
  <div class="lab-in" style="margin-top:12px">
    <button id="pc" class="btn solid" type="button">Cek Kebocoran</button>
  </div>
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
    <button id="vwipe" class="btn ghost" type="button" style="margin-top:12px">Kosongkan brankas</button>
  </div>
</div>
<p class="lab-note">PBKDF2 150.000 putaran + AES-GCM 256. Sandi induk tidak disimpan, salah ketik berarti brankas tidak bisa dibuka. Data hanya di peramban ini.</p>
</div></section>
<script nonce="__NONCE__">
(function(){
  var u=document.getElementById('pu'), t=document.getElementById('pt'), g=document.getElementById('pg'),
      v=document.getElementById('pv'), l=document.getElementById('pl'), e=document.getElementById('pe'),
      c=document.getElementById('pc'), o=document.getElementById('po');
  var SETS=[[/a-z/,'a-z',26],[/A-Z/,'A-Z',26],[/0-9/,'0-9',10],[/[^A-Za-z0-9]/,'simbol',33]];
  function pool(s){ var p=0; SETS.forEach(function(x){ if(x[0].test(s)) p+=x[2]; }); return p; }
  function measure(){
    var s=u.value, n=0; if(!s){ g.style.width='0'; v.textContent='\u2014';
      l.textContent='Kekuatan belum diukur'; e.textContent='Entropi 0 bit.'; return 0; }
    var p=pool(s), bits=Math.round(s.length*Math.log2(p||1));
    var cls=0; SETS.forEach(function(x){ if(x[0].test(s)) cls++; });
    if(s.length>=8) n++; if(s.length>=12) n++; if(s.length>=16) n++;
    if(cls>=2) n++; if(cls>=3) n++; if(cls>=4) n++;
    if(/^\d+$/.test(s)) n--; if(/(.)\1{2,}/.test(s)) n--;
    n=Math.max(0,Math.min(6,n));
    var pct=[8,24,42,58,74,88,100][n];
    g.style.width=pct+'%'; g.className='gfill '+(n>=5?'ok':n>=3?'warn':'bad');
    v.textContent=bits; e.textContent='Entropi '+bits+' bit, '+s.length+' karakter, '+cls+' kelas.';
    l.textContent=bits<40?'Lemah':bits<60?'Sedang':bits<80?'Kuat':'Sangat kuat';
    return bits;
  }
  u.addEventListener('input', measure);
  t.addEventListener('click', function(){ u.type = u.type==='password'?'text':'password'; });
  c.addEventListener('click', function(){
    o.innerHTML='';
    var s=u.value; if(!s){ o.innerHTML='<div class="lab-item warn"><b>!</b> Isi sandi dulu.</div>'; return; }
    if(!window.crypto||!crypto.subtle){ o.innerHTML='<div class="lab-item warn"><b>!</b> Butuh HTTPS atau localhost.</div>'; return; }
    o.innerHTML='<div class="lab-item"><b>&hellip;</b> Menghitung SHA-1</div>';
    crypto.subtle.digest('SHA-1', new TextEncoder().encode(s)).then(function(buf){
      var hex=[].map.call(new Uint8Array(buf), function(x){ return ('0'+x.toString(16)).slice(-2); }).join('').toUpperCase();
      var pre=hex.slice(0,5), suf=hex.slice(5);
      return fetch('https://api.pwnedpasswords.com/range/'+pre).then(function(r){
        if(!r.ok) throw new Error('HTTP '+r.status);
        return r.text();
      }).then(function(txt){
        o.innerHTML='';
        var n=0;
        txt.split('\n').forEach(function(row){
          var p=row.trim().split(':');
          if(p[0]===suf) n=parseInt(p[1],10)||0;
        });
        if(n) o.innerHTML='<div class="lab-item bad"><b>BOCOR</b> Ditemukan '+n.toLocaleString('id-ID')+' kali di kebocoran publik. Ganti sandi ini.</div>';
        else o.innerHTML='<div class="lab-item ok"><b>BERSIH</b> Tidak ditemukan di basis kebocoran.</div>';
      });
    }).catch(function(err){
      o.innerHTML='<div class="lab-item warn"><b>GAGAL</b> '+err.message+'. Periksa jaringan.</div>';
    });
  });

  /* brankas */
  var K='alf.vault', mem=null, key=null;
  function b64(b){ return btoa(String.fromCharCode.apply(null, new Uint8Array(b))); }
  function unb64(s){ return new Uint8Array(atob(s).split('').map(function(c){ return c.charCodeAt(0); })); }
  function dk(m, salt){
    return crypto.subtle.importKey('raw', new TextEncoder().encode(m), 'PBKDF2', false, ['deriveKey'])
      .then(function(k){
        return crypto.subtle.deriveKey({name:'PBKDF2', salt:salt, iterations:150000, hash:'SHA-256'},
          k, {name:'AES-GCM', length:256}, false, ['encrypt','decrypt']);
      });
  }
  function draw(){
    var box=document.getElementById('vlist'); box.innerHTML='';
    if(!mem||!mem.length){ box.innerHTML='<div class="lab-item">Brankas kosong.</div>'; return; }
    mem.forEach(function(it, i){
      var d=document.createElement('div'); d.className='lab-item ok';
      d.innerHTML='<b>'+it.n.replace(/</g,'&lt;')+'</b> <span class="mono">'+it.p.replace(/</g,'&lt;')+'</span>';
      var x=document.createElement('button'); x.textContent='hapus'; x.className='lab-x';
      x.onclick=function(){ mem.splice(i,1); save(); };
      d.appendChild(x); box.appendChild(d);
    });
  }
  function save(){
    if(!key) return;
    var salt=crypto.getRandomValues(new Uint8Array(16)), iv=crypto.getRandomValues(new Uint8Array(12));
    crypto.subtle.encrypt({name:'AES-GCM', iv:iv}, key, new TextEncoder().encode(JSON.stringify(mem)))
      .then(function(ct){
        localStorage.setItem(K, JSON.stringify({s:b64(salt), i:b64(iv), c:b64(ct)}));
        draw();
      });
  }
  document.getElementById('vopen').onclick=function(){
    var m=document.getElementById('vm').value;
    if(!m){ return; }
    var raw=localStorage.getItem(K);
    var body=document.getElementById('vbody');
    if(!raw){
      var salt=crypto.getRandomValues(new Uint8Array(16));
      dk(m, salt).then(function(k){ key=k; mem=[]; body.hidden=false;
        localStorage.setItem(K, JSON.stringify({s:b64(salt), i:'', c:''})); draw(); });
      return;
    }
    var o=JSON.parse(raw);
    dk(m, unb64(o.s)).then(function(k){
      return crypto.subtle.decrypt({name:'AES-GCM', iv:unb64(o.i)}, k, unb64(o.c))
        .then(function(pt){ key=k; mem=JSON.parse(new TextDecoder().decode(pt)); body.hidden=false; draw(); });
    }).catch(function(){ alert('Sandi induk salah.'); });
  };
  document.getElementById('vadd').onclick=function(){
    var n=document.getElementById('vn').value.trim(), p=document.getElementById('vp').value;
    if(!n||!p) return;
    mem.push({n:n, p:p}); document.getElementById('vn').value=''; document.getElementById('vp').value=''; save();
  };
  document.getElementById('vwipe').onclick=function(){
    if(!confirm('Kosongkan seluruh brankas?')) return;
    mem=[]; localStorage.removeItem(K); key=null;
    document.getElementById('vbody').hidden=true;
  };
})();
</script>
'''
