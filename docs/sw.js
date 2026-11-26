const C='alf-v1';
self.addEventListener('install',e=>{self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(self.clients.claim())});
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  e.respondWith(caches.open(C).then(c=>c.match(e.request).then(r=>r||fetch(e.request).then(res=>{c.put(e.request,res.clone());return res}).catch(()=>r))));
});
    }).catch(() => caches.match(r).then(hit => hit || caches.match('./'))));
    return;
  }
  e.respondWith(caches.match(r).then(hit => hit || fetch(r).then(res => {
    if (res.ok && new URL(r.url).origin === location.origin) {
      const cp = res.clone();
      caches.open(CACHE).then(c => c.put(r, cp));
    }
    return res;
  }).catch(() => hit)));
});
