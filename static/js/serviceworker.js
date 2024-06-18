
// const CACHE_NAME = 'my-site-cache-v1';
// const urlsToCache = [
//   '/',
//   '/static/assets/css/theme.css',
//   '/static/assets/css/demo.css',
//   '/static/assets/js/main.js',
//   '/static/assets/js/theme.js',
//   '/static/assets/js/config.js'
// ];

// // Install the service worker
// self.addEventListener('install', event => {
//   event.waitUntil(
//     caches.open(CACHE_NAME)
//       .then(cache => {
//         return cache.addAll(urlsToCache);
//       })
//   );
// });

// // Cache and return requests
// self.addEventListener('fetch', event => {
//   event.respondWith(
//     caches.match(event.request)
//       .then(response => {
//         return response || fetch(event.request);
//       })
//   );
// });

// // Update a service worker
// self.addEventListener('activate', event => {
//   const cacheWhitelist = [CACHE_NAME];
//   event.waitUntil(
//     caches.keys().then(cacheNames => {
//       return Promise.all(
//         cacheNames.map(cacheName => {
//           if (cacheWhitelist.indexOf(cacheName) === -1) {
//             return caches.delete(cacheName);
//           }
//         })
//       );
//     })
//   );
// });

// // Push notifications
// self.addEventListener('push', event => {
//   const data = event.data.json();
//   const title = data.title || 'New Notification';
//   const options = {
//     body: data.body || 'You have a new message.',
//     icon: data.icon || '/static/images/notification-icon.png',
//     data: data.url || '/'
//   };

//   event.waitUntil(
//     self.registration.showNotification(title, options)
//   );
// });

// // Handle notification click event
// self.addEventListener('notificationclick', event => {
//   event.notification.close();
//   event.waitUntil(
//     clients.openWindow(event.notification.data)
//   );
// });
