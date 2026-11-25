# lab116.py — SecureScan: skor heuristik URL, murni sisi klien
META = ("/securescan", "116", "SecureScan", "Skor keamanan URL secara heuristik tanpa server.")

BODY = r'''
<div class="wrap pghead"><div class="kick">116 · Lab Keamanan</div>
<h1>SecureScan, <em>periksa URL sebelum diklik</em>.</h1>
<p class="lead">Heuristik sisi klien: skema, panjang, karakter menipu, TLD, dan kata pemicu. Tidak ada data yang dikirim ke mana pun.</p></div>
<section><div class="wrap">
<div class="lab-card">
  <div class="lab-in">
    <input id="su" class="lab-input" placeholder="https://contoh.co.id/login" autocomplete="off" spellcheck="false">
    <button id="sb" class="btn solid" type="button">Pindai</button>
  </div>
  <div class="gauge"><div class="gfill" id="sg"></div></div>
  <div class="lab-row"><b id="sv">&mdash;</b><span id="sl">Belum ada URL</span></div>
  <div id="sf" class="lab-list"></div>
</div>
<p class="lab-note">Batas: cek port, header, dan sertifikat butuh server. Skor tinggi bukan jaminan situs aman.</p>
</div></section>
<script nonce="__NONCE__">
(function(){
  var u=document.getElementById('su'), b=document.getElementById('sb'),
      g=document.getElementById('sg'), v=document.getElementById('sv'),
      l=document.getElementById('sl'), f=document.getElementById('sf');
  var BADT=['zip','xyz','top','click','rest','mom','lol','cfd','sbs','buzz','gq','tk','ml','ga','cf'];
  var KW=['login','verifikasi','verify','secure','akun','account','update','wallet','bonus','promo','klaim','hadiah'];
  function add(t,s,w){ var d=document.createElement('div'); d.className='lab-item '+w;
    d.innerHTML='<b>'+s+'</b> '+t; f.appendChild(d); }
  function scan(){
    f.innerHTML=''; var raw=u.value.trim(), sc=100;
    if(!raw){ l.textContent='Belum ada URL'; v.textContent='\u2014'; g.style.width='0'; return; }
    var full=/^[a-z]+:\/\//i.test(raw)?raw:'https://'+raw, o;
    try{ o=new URL(full); }catch(e){ l.textContent='URL tidak sah'; v.textContent='0'; g.style.width='0'; return; }
    var h=o.hostname.toLowerCase(), host=h.replace(/^www\./,''), tld=host.split('.').pop();
    if(o.protocol!=='https:'){ sc-=30; add('Bukan HTTPS, isi bisa disadap.','-30','bad'); }
    else add('Skema HTTPS.','+0','ok');
    if(host.split('.').length>3){ sc-=10; add('Subdomain bertumpuk, mudah dipalsukan.','-10','warn'); }
    if(/^\d+\.\d+\.\d+\.\d+$/.test(host)){ sc-=15; add('Alamat IP langsung, tanpa nama domain.','-15','warn'); }
    if(host.indexOf('xn--')>-1){ sc-=10; add('Punycode, huruf bisa mirip domain lain.','-10','warn'); }
    if(BADT.indexOf(tld)>-1){ sc-=12; add('TLD .'+tld+' sering dipakai penyalahgunaan.','-12','warn'); }
    if((host.match(/-/g)||[]).length>2){ sc-=8; add('Terlalu banyak tanda hubung.','-8','warn'); }
    if(host.length>30){ sc-=6; add('Nama domain panjang.','-6','warn'); }
    if(raw.indexOf('@')>-1){ sc-=12; add('Ada karakter @, bagian sebelum @ diabaikan peramban.','-12','bad'); }
    if(o.port && o.port!=='443' && o.port!=='80'){ sc-=6; add('Port tidak lazim: '+o.port,'-6','warn'); }
    var hit=KW.filter(function(k){ return host.indexOf(k)>-1||o.pathname.toLowerCase().indexOf(k)>-1; });
    if(hit.length){ sc-=hit.length*5; add('Kata pemicu: '+hit.join(', '),'-'+(hit.length*5),'warn'); }
    if(/^\d/.test(host)){ sc-=5; add('Domain diawali angka.','-5','warn'); }
    if(host.split('.').length===2) add('Struktur domain wajar.','+0','ok');
    if(sc>100) sc=100; if(sc<0) sc=0;
    g.style.width=sc+'%';
    g.className='gfill '+(sc>=75?'ok':sc>=45?'warn':'bad');
    v.textContent=sc;
    l.textContent=sc>=75?'Relatif aman, tetap periksa isi':sc>=45?'Perlu kehati-hatian':'Berisiko tinggi';
  }
  b.addEventListener('click', scan);
  u.addEventListener('keydown', function(e){ if(e.key==='Enter'){ e.preventDefault(); scan(); } });
})();
</script>
'''
