var cacheName = 'api-mmo-v1';
var contentToCache = [
  '/',
  '/login',
  '/estimation',
  '/list_houses',
  '/faq',
  '/static/js/bootstrap.bundle.min.js',
  '/static/css/bootstrap.min.css',
  '/static/css/styles.css',
  '/static/img/icons/favicon.ico',
  '/static/img/bootstrap-icons.svg',
  '/static/img/icons/ai-logo.png',
  '/static/img/icons/ai-logo-16.png',
  '/static/img/icons/ai-logo-32.png',
  '/static/img/icons/ai-logo-128.png',
  '/static/img/icons/ai-logo-180.png',
  '/static/img/icons/ai-logo-512.png',
  '/static/img/icons/icon-192x192.png',
  '/static/img/icons/icon-256x256.png',
  '/static/img/icons/icon-384x384.png',
  '/static/img/icons/icon-512x512.png'
];

self.addEventListener('install', (e) => {
    console.log('[Service Worker] Installation');
    e.waitUntil(
        caches.open(cacheName).then((cache) => {
              console.log('[Service Worker] Mise en cache globale: app shell et contenu');
          return cache.addAll(contentToCache);
        })
    );
});

self.addEventListener('fetch', (e) => {
    console.log('[Service Worker] Ressource récupérée '+e.request.url);
    e.respondWith(
        caches.match(e.request).then((r) => {
              console.log('[Service Worker] Récupération de la ressource: '+e.request.url);
          return r || fetch(e.request).then((response) => {
                    return caches.open(cacheName).then((cache) => {
              console.log('[Service Worker] Mise en cache de la nouvelle ressource: '+e.request.url);
              cache.put(e.request, response.clone());
              return response;
            });
          });
        })
      );
});