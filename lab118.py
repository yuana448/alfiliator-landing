META = ("/netguard", "118", "NetGuard", "Deteksi IP lokal, sisir subnet, dan catat host yang menjawab.")
BODY = r'''
<div class="wrap pghead"><div class="kick">118 · Lab Jaringan</div>
<h1>NetGuard, <em>sisir jaringan ini</em>.</h1>
<p class="lead">IP lokal lewat WebRTC, gateway diuji, lalu subnet disisir satu per satu. Yang menjawab dicatat.</p></div>
<section><div class="wrap">
<div class="lab-card">
  <div class="lab-in">
    <button id="ng" class="btn solid" type="button">Deteksi IP</button>
    <button id="np" class="btn ghost" type="button">Probe Gateway</button>
    <button id="ns2" class="btn ghost" type="button">Sisir Subnet</button>
  </div>
  <div class="lab-row"><b id="ni">&mdash;</b><span id="ns">Belum dipindai</span></div>
  <div id="nl" class="lab-list"></div>
</div>
<p class="lab-note">Sisir memakai fetch no-cors ke 254 alamat, 20 sekaligus, batas 1,2 detik per alamat. Host yang menolak CORS tetap terhitung menjawab bila koneksi tidak langsung gagal.</p>
</div></section>
<section><div class="wrap">
<h2 style="margin-top:34px">Host ditemukan</h2><div class="hr"></div>
<table class="lab-tbl" id="nt"><thead><tr><th>Alamat</th><th>Status</th><th>Aksi</th></tr></thead><tbody></tbody></table>
</div></section>
<script nonce="__NONCE__">
(function(){
  var i=document.getElementById('ni'), s=document.getElementById('ns'), l=document.getElementById('nl');
  var found=[], KEY='alf.netblock', subnet='';
  function add(t,w){ var d=document.createElement('div'); d.className='lab-item '+(w||'');
    d.innerHTML=t; l.appendChild(d); return d; }
  function blocked(){ try{ return JSON.parse(localStorage.getItem(KEY)||'[]'); }catch(e){ return []; } }
  function setB(v){ localStorage.setItem(KEY, JSON.stringify(v)); }
  function draw(){
    var tb=document.querySelector('#nt tbody'); tb.innerHTML='';
    if(!found.length){ tb.innerHTML='<tr><td colspan="3" style="color:var(--dim)">Belum ada host.</td></tr>'; return; }
    var b=blocked();
    found.forEach(function(ip){
      var off=b.indexOf(ip)>-1, tr=document.createElement('tr');
      tr.innerHTML='<td class="mono">'+ip+'</td><td><span class="lab-item '+(off?'bad':'ok')
        +'" style="padding:2px 8px">'+(off?'DIBLOKIR':'AKTIF')+'</span></td>';
      var td=document.createElement('td'), btn=document.createElement('button');
      btn.className='btn ghost'; btn.type='button'; btn.textContent=off?'Buka':'Blokir';
      btn.onclick=function(){ var c=blocked();
        if(c.indexOf(ip)>-1) c=c.filter(function(x){ return x!==ip; }); else c.push(ip);
        setB(c); draw(); };
      td.appendChild(btn); tr.appendChild(td); tb.appendChild(tr);
    });
  }
  function probe(ip, ms){
    var ctl=new AbortController(), to=setTimeout(function(){ ctl.abort(); }, ms||1200);
    return fetch('http://'+ip, {mode:'no-cors', signal:ctl.signal})
      .then(function(){ clearTimeout(to); return true; })
      .catch(function(){ clearTimeout(to); return false; });
  }
  document.getElementById('ng').onclick=function(){
    l.innerHTML=''; i.textContent='\u2026'; s.textContent='Meminta izin';
    if(!window.RTCPeerConnection){ s.textContent='WebRTC tidak didukung'; return; }
    var got=false, pc=new RTCPeerConnection({iceServers:[{urls:'stun:stun.l.google.com:19302'}]});
    pc.createDataChannel('x');
    pc.onicecandidate=function(ev){
      if(!ev.candidate){ pc.close(); return; }
      var m=/(\d{1,3}(?:\.\d{1,3}){3})/.exec(ev.candidate.candidate);
      if(!m||got) return; got=true;
      var ip=m[1], priv=/^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)/.test(ip);
      i.textContent=ip; subnet=ip.split('.').slice(0,3).join('.');
      s.textContent=priv?'Privat, subnet '+subnet+'.0/24':'Publik';
      add('<b>'+(priv?'LOKAL':'PUBLIK')+'</b> '+ip, priv?'ok':'warn');
    };
    pc.createOffer().then(function(o){ return pc.setLocalDescription(o); });
    setTimeout(function(){ if(!got) s.textContent='Tidak ada kandidat'; }, 6000);
  };
  document.getElementById('np').onclick=function(){
    l.innerHTML=''; s.textContent='Menguji gateway';
    ['1','254','2'].forEach(function(n){
      var ip=(subnet||'192.168.1')+'.'+n;
      probe(ip, 2000).then(function(ok){
        add('<b>'+(ok?'HIDUP':'DIAM')+'</b> '+ip, ok?'ok':'');
        if(ok && found.indexOf(ip)<0){ found.push(ip); draw(); }
      });
    });
  };
  document.getElementById('ns2').onclick=function(){
    if(!subnet){ s.textContent='Deteksi IP dulu'; return; }
    l.innerHTML=''; s.textContent='Menyisir '+subnet+'.0/24';
    found=[]; draw();
    var n=1, run=0, live=0, done=0;
    function next(){
      while(run<20 && n<255){
        var ip=subnet+'.'+(n++); run++;
        probe(ip).then(function(ok){
          run--; done++;
          if(ok){ live++; found.push(ip); add('<b>HIDUP</b> '+ip,'ok'); draw(); }
          if(done%25===0) s.textContent='Diperiksa '+done+'/254, hidup '+live;
          if(n<255) next(); else if(done>=254) s.textContent='Selesai: '+live+' host menjawab';
        });
      }
    }
    next();
  };
  draw();
})();
</script>
'''
