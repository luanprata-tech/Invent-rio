const CACHE_NAME = 'inventi-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/inventario',
  '/ips',
  '/static/css/style.css',
  '/static/js/tailwind-config.js',
  '/static/js/login.js',
  '/static/img/icon-192x192.png',
  '/static/img/icon-512x512.png'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS_TO_CACHE))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(clients.claim());
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    fetch(event.request)
      .then(response => {
        const responseClone = response.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseClone);
        });
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
