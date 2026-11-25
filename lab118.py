# lab118.py — NetGuard: deteksi IP lokal, probe gateway, tabel perangkat
META = ("/netguard", "118", "NetGuard", "Deteksi jaringan lokal, probe gateway, dan tabel perangkat.")

BODY = r'''
<div class="wrap pghead"><div class="kick">118 · Lab Jaringan</div>
<h1>NetGuard, <em>lihat siapa di jaringan ini</em>.</h1>
<p class="lead">Deteksi alamat lokal lewat WebRTC, probe gateway umum, dan catat perangkat yang boleh lewat. Semua di peramban.</p></div>
<section><div class="wrap">
<div class="lab-card">
  <div class="lab-in">
    <button id="ng" class="btn solid" type="button">Deteksi Jaringan</button>
    <button id="np" class="btn ghost" type="button">Probe Gateway</button>
  </div>
  <div class="lab-row"><b id="ni">&mdash;</b><span id="ns">Belum dipindai</span></div>
  <div id="nl" class="lab-list"></div>
</div>
<p class="lab-note">Batas: ARP asli butuh aplikasi atau server. Nama perangkat di tabel adalah contoh, status blokir disimpan lokal.</p>
</div></section>
<section><div class="wrap">
<h2 style="margin-top:34px">Perangkat</h2><div class="hr"></div>
<table class="lab-tbl" id="nt"><thead><tr><th>Perangkat</th><th>Alamat</th><th>Status</th><th>Aksi</th></tr></thead><tbody></tbody></table>
</div></section>
<script nonce="__NONCE__">
(function(){
  var i=document.getElementById('ni'), s=document.getElementById('ns'), l=document.getElementById('nl');
  function add(t,w){ var d=document.createElement('div'); d.className='lab-item '+(w||''); d.innerHTML=t; l.appendChild(d); }
  document.getElementById('ng').onclick=function(){
    l.innerHTML=''; i.textContent='\u2026'; s.textContent='Meminta izin jaringan';
    if(!window.RTCPeerConnection){ i.textContent='\u2014'; s.textContent='WebRTC tidak didukung'; return; }
    var got=false, pc=new RTCPeerConnection({iceServers:[{urls:'stun:stun.l.google.com:19302'}]});
    pc.createDataChannel('x');
    pc.onicecandidate=function(ev){
      if(!ev.candidate){ pc.close(); if(!got){ i.textContent='\u2014'; s.textContent='Tidak ada kandidat'; add('<b>!</b> Jaringan tertutup atau STUN diblokir.','warn'); } return; }
      var m=/(\d{1,3}(?:\.\d{1,3}){3})/.exec(ev.candidate.candidate);
      if(!m||got) return;
      got=true; i.textContent=m[1];
      var ip=m[1];
      var priv=/^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)/.test(ip);
      s.textContent=priv?'Alamat privat, jaringan lokal':'Alamat publik';
      add('<b>'+(priv?'LOKAL':'PUBLIK')+'</b> '+ip, priv?'ok':'warn');
      if(priv){
        var g=ip.split('.').slice(0,3).join('.');
        add('<b>INFO</b> Gateway kemungkinan '+g+'.1','');
      }
      pc.close();
    };
    pc.createOffer().then(function(o){ return pc.setLocalDescription(o); });
    setTimeout(function(){ if(!got){ i.textContent='\u2014'; s.textContent='Waktu habis'; } }, 6000);
  };
  document.getElementById('np').onclick=function(){
    l.innerHTML=''; s.textContent='Menguji gateway umum';
    ['192.168.1.1','192.168.0.1','192.168.88.1','10.0.0.1'].forEach(function(h){
      var t0=Date.now();
      var ctl=new AbortController();
      var to=setTimeout(function(){ ctl.abort(); }, 2500);
      fetch('http://'+h, {mode:'no-cors', signal:ctl.signal}).then(function(){
        clearTimeout(to);
        add('<b>HIDUP</b> '+h+' &middot; '+(Date.now()-t0)+' ms','ok');
      }).catch(function(){
        clearTimeout(to);
        add('<b>DIAM</b> '+h,'');
      });
    });
  };

  var DEV=[['Router','192.168.1.1',1],['Ponsel Andi','192.168.1.7',1],
    ['Laptop Kerja','192.168.1.12',1],['TV Ruang Tamu','192.168.1.21',1],
    ['Kamera Depan','192.168.1.33',1],['Tablet Tamu','192.168.1.44',1]];
  var KEY='alf.netblock';
  function blocked(){ try{ return JSON.parse(localStorage.getItem(KEY)||'[]'); }catch(e){ return []; } }
  function setB(v){ localStorage.setItem(KEY, JSON.stringify(v)); }
  function draw(){
    var tb=document.querySelector('#nt tbody'); tb.innerHTML=''; var b=blocked();
    DEV.forEach(function(d, idx){
      var off=b.indexOf(d[1])>-1;
      var tr=document.createElement('tr');
      tr.innerHTML='<td>'+d[0]+'</td><td class="mono">'+d[1]+'</td>'
        +'<td><span class="lab-item '+(off?'bad':'ok')+'" style="padding:2px 8px">'+(off?'DIBLOKIR':'AKTIF')+'</span></td>';
      var td=document.createElement('td');
      var btn=document.createElement('button'); btn.className='btn ghost'; btn.type='button';
      btn.textContent=off?'Buka':'Blokir';
      btn.onclick=function(){
        var cur=blocked();
        if(cur.indexOf(d[1])>-1) cur=cur.filter(function(x){ return x!==d[1]; });
        else cur.push(d[1]);
        setB(cur); draw();
      };
      td.appendChild(btn); tr.appendChild(td); tb.appendChild(tr);
    });
  }
  draw();
})();
</script>
'''
