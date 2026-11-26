# lab119.py — PhishCatcher: pemangsa phish, simulator kampanye
META = ("/phishcatcher", "119", "PhishCatcher", "Simulasi halaman phish dan statistik kampanye.")

BODY = r'''
<style>
.pc-t{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.pc-t button{padding:7px 12px;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
  border:1px solid var(--line2);background:none;color:var(--muted);cursor:pointer}
.pc-t button[aria-pressed="true"]{border-color:var(--gold);color:var(--gold2);background:var(--panel2)}
.pc-prev{border:1px solid var(--line);background:#fff;color:#14161a;padding:0;overflow:hidden;min-height:210px}
.pc-bar{background:#f1f3f6;border-bottom:1px solid #dfe3e8;padding:7px 11px;display:flex;gap:7px;align-items:center}
.pc-dot{width:8px;height:8px;border-radius:50%;background:#d0d5dc}
.pc-url{flex:1;background:#fff;border:1px solid #dfe3e8;border-radius:99px;padding:3px 10px;
  font-family:'JetBrains Mono',monospace;font-size:10px;color:#5b636e;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pc-in{padding:22px 18px;text-align:center}
.pc-in h4{font-size:15px;margin:0 0 4px;color:#14161a;font-family:'Sora',sans-serif}
.pc-in p{font-size:11.5px;color:#5b636e;margin:0 0 14px}
.pc-in label{display:block;text-align:left;font-size:10px;color:#5b636e;margin-bottom:4px}
.pc-in input{width:100%;padding:9px;border:1px solid #d6dbe2;border-radius:5px;margin-bottom:9px;font-size:11.5px}
.pc-in .pc-go{width:100%;padding:10px;border:0;border-radius:5px;background:#1b5fd0;color:#fff;font-size:11.5px;font-weight:600}
.pc-stat{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line2);border:1px solid var(--line2);margin-top:16px}
.pc-stat div{background:var(--panel);padding:14px 12px}
.pc-stat b{display:block;font-family:'JetBrains Mono',monospace;font-size:17px;color:var(--gold2)}
.pc-stat span{font-size:8.5px;letter-spacing:.14em;color:var(--dim);text-transform:uppercase}
.pc-funnel{margin-top:16px;display:grid;gap:7px}
.pc-fb{height:22px;background:var(--panel2);border:1px solid var(--line2);position:relative;overflow:hidden}
.pc-fb i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--gold),var(--gold2));transition:width .6s var(--ease)}
.pc-fb span{position:absolute;left:9px;top:3px;font-family:'JetBrains Mono',monospace;font-size:9.5px;color:var(--ink)}
</style>
<div class="wrap pghead"><div class="kick">119 · Lab Phish</div>
<h1>PhishCatcher, <em>latih mata tim Anda</em>.</h1>
<p class="lead">Bangun halaman tiruan, hitung tingkat lolos, dan lihat corong kampanye. Semua template di sini contoh, bukan milik merek asli.</p></div>
<section><div class="wrap">
<div class="lab-card">
  <div class="pc-t" id="pt">
    <button data-k="bank" aria-pressed="true">Bank</button>
    <button data-k="toko">Marketplace</button>
    <button data-k="kurir">Kurir</button>
    <button data-k="sosial">Media Sosial</button>
  </div>
  <div class="pc-prev" id="pp"></div>
  <p class="lab-note" id="pnote"></p>
</div>
</div></section>
<section><div class="wrap">
<h2 style="margin-top:34px">Simulasi kampanye</h2><div class="hr"></div>
<div class="lab-card">
  <div class="lab-in">
    <label class="lab-input" style="display:flex;align-items:center;gap:8px;font-size:11.5px;color:var(--muted)">
      Penerima <input id="pn" type="range" min="10" max="500" step="10" value="120" style="flex:1">
      <b id="pnv" class="mono" style="color:var(--gold)">120</b>
    </label>
  </div>
  <div class="lab-in" style="margin-top:10px">
    <label class="lab-input" style="display:flex;align-items:center;gap:8px;font-size:11.5px;color:var(--muted)">
      Kualitas tiruan <input id="pq" type="range" min="1" max="5" step="1" value="3" style="flex:1">
      <b id="pqv" class="mono" style="color:var(--gold)">3</b>
    </label>
  </div>
  <div class="pc-stat">
    <div><b id="s1">0</b><span>Terkirim</span></div>
    <div><b id="s2">0</b><span>Klik</span></div>
    <div><b id="s3">0</b><span>Isi Form</span></div>
  </div>
  <div class="pc-funnel" id="pf"></div>
</div>
<p class="lab-note">Angka memakai laju contoh: klik 20&ndash;55 persen, isi form 8&ndash;30 persen dari yang klik. Naik seiring kualitas tiruan.</p>
</div></section>
<script nonce="__NONCE__">
(function(){
  var T={
    bank:{u:'https://bca-secure-login.verifikasi-akun.co.id',h:'Verifikasi Akun',s:'Sesi Anda akan berakhir dalam 24 jam',a:'Nomor Kartu',b:'PIN / OTP',n:'Tiruan bagus: domain berlapis, kata pemicu verifikasi.'},
    toko:{u:'https://tokopedia-promo.bonus-klaim.xyz',h:'Klaim Bonus Pembeli',s:'Saldo bonus Rp 250.000 menunggu',a:'Email atau Nomor HP',b:'Sandi Akun',n:'TLD murah plus dua kata pemicu, pola paling sering berhasil.'},
    kurir:{u:'http://jne-resi-track.klik-here.top',h:'Resi Gagal Diantar',s:'Paket ditahan, konfirmasi alamat',a:'Nomor Resi',b:'Alamat Lengkap',n:'HTTP tanpa S, isian resi membuat korban percaya.'},
    sosial:{u:'https://instagram-verified.biru-check.click',h:'Centang Biru Gratis',s:'Akun Anda memenuhi syarat',a:'Nama Pengguna',b:'Sandi',n:'Iming-iming centang biru, korban menyerahkan sandi.'}
  };
  var pv=document.getElementById('pp'), nt=document.getElementById('pnote'), cur='bank';
  function paint(k){
    cur=k; var d=T[k];
    pv.innerHTML='<div class="pc-bar"><i class="pc-dot"></i><i class="pc-dot"></i><i class="pc-dot"></i>'
      +'<span class="pc-url">'+d.u+'</span></div>'
      +'<div class="pc-in"><h4>'+d.h+'</h4><p>'+d.s+'</p>'
      +'<label>'+d.a+'</label><input placeholder="'+d.a+'">'
      +'<label>'+d.b+'</label><input placeholder="'+d.b+'">'
      +'<button class="pc-go" type="button">Lanjutkan</button></div>';
    nt.textContent=d.n;
  }
  document.querySelectorAll('#pt button').forEach(function(b){
    b.addEventListener('click', function(){
      document.querySelectorAll('#pt button').forEach(function(x){ x.setAttribute('aria-pressed', String(x===b)); });
      paint(b.dataset.k);
    });
  });
  paint('bank');

  var n=document.getElementById('pn'), q=document.getElementById('pq');
  function hit(){
    var tot=+n.value, lv=+q.value;
    document.getElementById('pnv').textContent=tot;
    document.getElementById('pqv').textContent=lv;
    var cr=0.20+lv*0.07, sr=0.08+lv*0.045;
    var cl=Math.round(tot*cr), sb=Math.round(cl*sr);
    document.getElementById('s1').textContent=tot;
    document.getElementById('s2').textContent=cl;
    document.getElementById('s3').textContent=sb;
    var rows=[['Terkirim',tot],['Klik',cl],['Isi form',sb]];
    var f=document.getElementById('pf'); f.innerHTML='';
    rows.forEach(function(r){
      var d=document.createElement('div'); d.className='pc-fb';
      var i=document.createElement('i'); i.style.width=(tot?r[1]/tot*100:0)+'%';
      var s=document.createElement('span'); s.textContent=r[0]+' &middot; '+r[1];
      s.innerHTML=r[0]+' &middot; '+r[1];
      d.appendChild(i); d.appendChild(s); f.appendChild(d);
    });
  }
  n.addEventListener('input', hit); q.addEventListener('input', hit); hit();
  var QZ=[
    ['https://bca-verifikasi.akun-aman.xyz','Verifikasi Akun BCA',1,'TLD .xyz plus dua kata pemicu.'],
    ['https://www.bca.co.id','BCA',0,'Domain resmi, dua lapis, .co.id.'],
    ['http://jne-resi.klik-here.top','Lacak Resi',1,'HTTP tanpa S dan .top.'],
    ['https://github.com/login','Sign in to GitHub',0,'Domain tunggal, HTTPS.'],
    ['https://tokopedia-promo.hadiah-klaim.click','Klaim Hadiah',1,'.click dan kata hadiah.'],
    ['https://mail.google.com','Gmail',0,'Subdomain resmi Google, HTTPS.']
  ];
  var qi=0, qsc=0;
  var qq=document.getElementById('qq'), qz=document.getElementById('qz'),
      qs=document.getElementById('qs'), qx=document.getElementById('qx');
  function show(){
    if(qi>=QZ.length){
      qq.innerHTML='<b>Selesai.</b> Skor '+qsc+' dari '+QZ.length+'.';
      qz.textContent=qsc; qs.textContent='Kuis berakhir';
      return;
    }
    qq.innerHTML='<b class="mono">'+QZ[qi][0]+'</b><br>'+QZ[qi][1];
    qs.textContent='Soal '+(qi+1)+' dari '+QZ.length;
  }
  function jawab(v){
    if(qi>=QZ.length) return;
    var it=QZ[qi], ok=(v===it[2]);
    if(ok) qsc++;
    qz.textContent=qsc;
    var d=document.createElement('div');
    d.className='lab-item '+(ok?'ok':'bad');
    d.innerHTML='<b>'+(ok?'BENAR':'SALAH')+'</b> '+(it[2]?'Ini phish. ':'Ini asli. ')+it[3];
    qx.appendChild(d);
    qi++; show();
  }
  document.getElementById('qf').onclick=function(){ jawab(1); };
  document.getElementById('qr').onclick=function(){ jawab(0); };
  show();

})();
<section><div class="wrap">
<h2 style="margin-top:34px">Kuis: phish atau asli</h2><div class="hr"></div>
<div class="lab-card">
  <div class="lab-row"><b id="qz">&mdash;</b><span id="qs">Soal 1 dari 6</span></div>
  <div id="qq" class="lab-item" style="margin-top:12px;font-size:13px"></div>
  <div class="lab-in" style="margin-top:12px">
    <button id="qf" class="btn solid" type="button">Phish</button>
    <button id="qr" class="btn ghost" type="button">Asli</button>
  </div>
  <div id="qx" class="lab-list"></div>
</div>
<p class="lab-note">Jawaban benar diberi alasan. Skor disimpan selama halaman terbuka.</p>
</div></section>
</script>
'''
