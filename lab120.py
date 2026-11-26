# lab120.py — OSINT-Track: jejak nama pengguna publik
META = ("/osint-track", "120", "OSINT-Track", "Lacak jejak nama pengguna publik di banyak platform.")

BODY = r'''
<div class="wrap pghead"><div class="kick">120 · Lab Jejak</div>
<h1>OSINT-Track, <em>jejak publik satu nama</em>.</h1>
<p class="lead">Satu nama pengguna, banyak platform. GitHub diperiksa langsung lewat API, sisanya dibuka untuk Anda nilai. Hanya data publik.</p></div>
<section><div class="wrap">
<div class="lab-card">
  <div class="lab-in">
    <input id="ou" class="lab-input" placeholder="nama_pengguna" autocomplete="off" spellcheck="false">
    <button id="ob" class="btn solid" type="button">Lacak</button>
  </div>
  <div class="lab-row"><b id="ov">&mdash;</b><span id="os">Belum dilacak</span></div>
  <div id="ol" class="lab-list"></div>
</div>
<p class="lab-note">Batas: hanya GitHub yang benar-benar diperiksa (200/404). Platform lain menghasilkan tautan dugaan, belum tentu ada. Tidak ada kunci API yang dipakai.</p>
</div></section>
<section><div class="wrap">
<h2 style="margin-top:34px">Cara membaca hasil</h2><div class="hr"></div>
<table class="lab-tbl"><thead><tr><th>Tanda</th><th>Arti</th></tr></thead><tbody>
<tr><td><span class="lab-item ok" style="padding:2px 8px">ADA</span></td><td>Diperiksa langsung dan profil ditemukan</td></tr>
<tr><td><span class="lab-item bad" style="padding:2px 8px">KOSONG</span></td><td>Diperiksa langsung dan profil tidak ada</td></tr>
<tr><td><span class="lab-item" style="padding:2px 8px">DUGAAN</span></td><td>Tautan dibuat dari pola, perlu dibuka manual</td></tr>
</tbody></table>
</div></section>
<script nonce="__NONCE__">
(function(){
  var u=document.getElementById('ou'), b=document.getElementById('ob'),
      v=document.getElementById('ov'), s=document.getElementById('os'), l=document.getElementById('ol');
  var PLAT=[
    ['GitHub','https://github.com/','api'],
    ['GitLab','https://gitlab.com/','gitlab'],
    ['Reddit','https://reddit.com/user/','reddit'],
    ['Dev.to','https://dev.to/','devto'],
    ['Hacker News','https://news.ycombinator.com/user?id=','hn'],
    ['npm','https://www.npmjs.com/~','npm'],
    ['PyPI','https://pypi.org/user/','pypi'],
    ['Instagram','https://instagram.com/',''],
    ['Twitter / X','https://x.com/',''],
    ['TikTok','https://tiktok.com/@',''],
    ['Medium','https://medium.com/@',''],
    ['Telegram','https://t.me/','']
  ];
  function row(name, url, cls, txt){
    var d=document.createElement('div'); d.className='lab-item '+(cls||'');
    d.innerHTML='<b>'+(txt||'DUGAAN')+'</b> <a href="'+url+'" target="_blank" rel="noopener">'+name+'</a>';
    l.appendChild(d);
    return d;
  }
  function run(){
    l.innerHTML=''; var n=u.value.trim().replace(/^@/,'').replace(/[^A-Za-z0-9._-]/g,'');
    if(!n){ s.textContent='Nama kosong'; v.textContent='\u2014'; return; }
    u.value=n; v.textContent='\u2026'; s.textContent='Memeriksa '+n;
    var found=0, guess=0, done=0, total=0;
    function tally(){ done++; v.textContent=found;
      s.textContent=found+' ada &middot; '+guess+' tautan dugaan';
      if(done===total) s.textContent='Selesai: '+found+' profil publik'; }
    PLAT.forEach(function(p){
      var url=p[1]+(p[2]==='hn'?'?id=':'')+n, k=p[2];
      if(!k){ guess++; row(p[0], url, '', 'DUGAAN'); return; }
      total++;
      var job;
      if(k==='api') job=fetch('https://api.github.com/users/'+n).then(function(r){ return r.status===200; });
      else if(k==='gitlab') job=fetch('https://gitlab.com/api/v4/users?username='+n).then(function(r){ return r.json(); }).then(function(a){ return a.length>0; });
      else if(k==='reddit') job=fetch('https://www.reddit.com/user/'+n+'/about.json').then(function(r){ return r.status===200; });
      else if(k==='devto') job=fetch('https://dev.to/api/users/by_username?url='+n).then(function(r){ return r.status===200; });
      else if(k==='hn') job=fetch('https://hn.algolia.com/api/v1/search?tags=author_'+n+'&hitsPerPage=1').then(function(r){ return r.json(); }).then(function(d){ return d.hits.length>0; });
      else if(k==='npm') job=fetch('https://registry.npmjs.org/-/v1/search?text=maintainer:'+n+'&size=1').then(function(r){ return r.json(); }).then(function(d){ return d.total>0; });
      else job=fetch('https://pypi.org/pypi/'+n+'/json').then(function(r){ return r.status===200; });
      job.then(function(ok){
        if(ok){ found++; row(p[0], url, 'ok', 'ADA'); } else row(p[0], url, 'bad', 'KOSONG');
        tally();
      }).catch(function(){ row(p[0], url, '', 'GAGAL'); tally(); });
    });
  }
  b.addEventListener('click', run);
  u.addEventListener('keydown', function(e){ if(e.key==='Enter'){ e.preventDefault(); run(); } });
})();
</script>
'''
