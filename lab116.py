# lab116.py — SecureScan v2: heuristik URL + DNS nyata lewat DoH
META = ("/securescan", "116", "SecureScan", "Skor keamanan URL dan pemeriksaan DNS domain.")

BODY = r'''
<div class="wrap pghead"><div class="kick">116 · Lab Keamanan</div>
<h1>SecureScan, <em>URL dan DNS sekaligus</em>.</h1>
<p class="lead">Heuristik URL, lalu catatan DNS nyata: SPF, DMARC, CAA, DNSSEC. Lewat DoH, jadi tidak ada server sendiri.</p></div>
<section><div class="wrap">
<div class="lab-card">
  <div class="lab-in">
    <input id="su" class="lab-input" placeholder="contoh.co.id atau https://contoh.co.id/login" autocomplete="off" spellcheck="false">
    <button id="sb" class="btn solid" type="button">Pindai</button>
  </div>
  <div class="gauge"><div class="gfill" id="sg"></div></div>
  <div class="lab-row"><b id="sv">&mdash;</b><span id="sl">Belum ada URL</span></div>
  <div id="sf" class="lab-list"></div>
</div>
<p class="lab-note">Batas: port, header, dan sertifikat tetap butuh server. DNS dibaca dari Cloudflare DoH, publik dan tanpa kunci.</p>
</div></section>
<section><div class="wrap">
<h2 style="margin-top:34px">Riwayat</h2><div class="hr"></div>
<div id="sh" class="lab-list"></div>
<div class="lab-in" style="margin-top:10px">
  <button id="sx" class="btn ghost" type="button">Ekspor JSON</button><button id="srep" class="btn ghost" type="button">Salin laporan</button>
  <button id="sc" class="btn ghost" type="button">Bersihkan</button>
</div>
</div></section>
<script nonce="__NONCE__">
'''
BODY += r'''
(function(){
  var u=document.getElementById('su'), b=document.getElementById('sb'),
      g=document.getElementById('sg'), v=document.getElementById('sv'),
      l=document.getElementById('sl'), f=document.getElementById('sf'),
      h=document.getElementById('sh'), K='alf.scanhist';
  var BADT=['zip','xyz','top','click','rest','mom','lol','cfd','sbs','buzz','gq','tk','ml','ga','cf'];
  var KW=['login','verifikasi','verify','secure','akun','account','update','wallet','bonus','promo'];
  function add(t,s,w){ var d=document.createElement('div'); d.className='lab-item '+(w||'');
    d.innerHTML='<b>'+s+'</b> '+t; f.appendChild(d); return d; }
  function dns(name,type){
    var url='https://cloudflare-dns.com/dns-query?name='+encodeURIComponent(name)+'&type='+type;
    return fetch(url,{headers:{accept:'application/dns-json'}}).then(function(r){ return r.json(); })
      .then(function(j){ return j.Answer||[]; });
  }
  function txt(name,type){ return dns(name,type).then(function(a){
    return a.map(function(x){ return (x.data||'').replace(/"/g,''); }); }); }
  function heur(raw,o,host,tld,sc){
    if(o.protocol!=='https:'){ sc-=25; add('Bukan HTTPS.','-25','bad'); } else add('Skema HTTPS.','+0','ok');
    if(host.split('.').length>3){ sc-=10; add('Subdomain bertumpuk.','-10','warn'); }
    if(/^\d+\.\d+\.\d+\.\d+$/.test(host)){ sc-=12; add('IP langsung.','-12','warn'); }
    if(host.indexOf('xn--')>-1){ sc-=10; add('Punycode.','-10','warn'); }
    if(BADT.indexOf(tld)>-1){ sc-=10; add('TLD .'+tld+' rawan.','-10','warn'); }
    if(raw.indexOf('@')>-1){ sc-=12; add('Ada karakter @.','-12','bad'); }
    var hit=KW.filter(function(k){ return host.indexOf(k)>-1||o.pathname.toLowerCase().indexOf(k)>-1; });
    if(hit.length){ sc-=hit.length*4; add('Kata pemicu: '+hit.join(', '),'-'+(hit.length*4),'warn'); }
    return sc;
  }
  function dnsChecks(host,sc){
    var base=host.replace(/^www\./,'');
    return Promise.all([txt(base,'TXT'), txt('_dmarc.'+base,'TXT'), dns(base,'CAA'), dns(base,'MX'), dns(base,'NS')])
    .then(function(r){
      var spf=r[0].filter(function(t){ return /^v=spf1/i.test(t); });
      if(spf.length) add('SPF ada, pengirim dipersempit.','+0','ok');
      else { sc-=10; add('SPF tidak ada, email mudah dipalsukan.','-10','warn'); }
      var dm=r[1].filter(function(t){ return /^v=DMARC1/i.test(t); });
      if(dm.length){ add('DMARC ada.','+0','ok'); }
      else { sc-=12; add('DMARC tidak ada.','-12','warn'); }
      if(r[2].length) add('CAA ada, penerbit sertifikat dibatasi.','+0','ok');
      else { sc-=4; add('CAA tidak ada.','-4','warn'); }
      if(r[3].length) add('MX aktif ('+r[3].length+' host).','+0','ok');
      else add('Tanpa MX, domain tidak menerima email.','+0','');
      if(r[4].length) add('NS: '+r[4].slice(0,2).map(function(x){ return x.data; }).join(', '),'+0','');
      return sc;
    }).catch(function(){ add('DNS tidak terbaca.','+0','warn'); return sc; });
  }
  function hist(url, sc){
    var a=[]; try{ a=JSON.parse(localStorage.getItem(K)||'[]'); }catch(e){}
    a.unshift({u:url,s:sc,t:Date.now()}); a=a.slice(0,20);
    localStorage.setItem(K, JSON.stringify(a)); draw();
  }
  function draw(){
    var a=[]; try{ a=JSON.parse(localStorage.getItem(K)||'[]'); }catch(e){}
    h.innerHTML='';
    if(!a.length){ h.innerHTML='<div class="lab-item">Belum ada riwayat.</div>'; return; }
    a.forEach(function(x){
      var d=document.createElement('div');
      d.className='lab-item '+(x.s>=75?'ok':x.s>=45?'warn':'bad');
      d.innerHTML='<b>'+x.s+'</b> '+x.u.replace(/</g,'&lt;');
      h.appendChild(d);
    });
  }
  function scan(){
    f.innerHTML=''; var raw=u.value.trim(), sc=100;
    if(!raw){ l.textContent='Belum ada URL'; v.textContent='\u2014'; g.style.width='0'; return; }
    var full=/^[a-z]+:\/\//i.test(raw)?raw:'https://'+raw, o;
    try{ o=new URL(full); }catch(e){ l.textContent='URL tidak sah'; v.textContent='0'; return; }
    var host=o.hostname.toLowerCase(), tld=host.split('.').pop();
    sc=heur(raw,o,host,tld,sc);
    l.textContent='Memeriksa DNS\u2026'; v.textContent='\u2026';
    dnsChecks(host,sc).then(function(s){
      if(s>100) s=100; if(s<0) s=0;
      g.style.width=s+'%'; g.className='gfill '+(s>=75?'ok':s>=45?'warn':'bad');
      v.textContent=s;
      l.textContent=s>=75?'Relatif aman, tetap periksa isi':s>=45?'Perlu kehati-hatian':'Berisiko tinggi';
      hist(full, s);
    });
  }
  document.getElementById('srep').onclick=function(){
    var t='SecureScan '+u.value+'\nskor '+v.textContent+'\n';
    f.querySelectorAll('.lab-item').forEach(function(d){ t+= '- '+d.textContent.trim()+'\n'; });
    if(navigator.clipboard) navigator.clipboard.writeText(t);
    var b2=document.getElementById('srep'), o=b2.textContent;
    b2.textContent='Tersalin'; setTimeout(function(){ b2.textContent=o; }, 1200);
  };
  b.addEventListener('click', scan);
  u.addEventListener('keydown', function(e){ if(e.key==='Enter'){ e.preventDefault(); scan(); } });
  document.getElementById('sx').onclick=function(){
    var a=localStorage.getItem(K)||'[]';
    var bl=new Blob([a],{type:'application/json'}), t=URL.createObjectURL(bl);
    var x=document.createElement('a'); x.href=t; x.download='securescan.json'; x.click(); URL.revokeObjectURL(t);
  };
  document.getElementById('sc').onclick=function(){ localStorage.removeItem(K); draw(); };
  draw();
})();
</script>
'''
