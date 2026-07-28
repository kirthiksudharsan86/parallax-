/* ── loader.js ── Cinematic loading sequence (Chapter 2 §3) */
(function () {
  var PXLoader = {};

  PXLoader.init = function (done) {
    var loader = document.getElementById('loader');
    var textEl = document.getElementById('loader-text');

    if (!loader) { if (done) done(); return; }

    var messages = [
      'Initializing Innovation...',
      'Loading AI Core...',
      'Connecting Teams...',
      'Synchronizing Universe...',
      'Ready.'
    ];

    var MESSAGE_INTERVAL = 280;
    var MIN_DISPLAY_TIME = 1300;
    var startTime = Date.now();
    var i = 0;

    if (textEl) textEl.textContent = messages[0];

    var msgTimer = setInterval(function () {
      i++;
      if (i >= messages.length) {
        clearInterval(msgTimer);
        return;
      }
      if (textEl) textEl.textContent = messages[i];
    }, MESSAGE_INTERVAL);

    function finish() {
      var elapsed = Date.now() - startTime;
      var remaining = Math.max(0, MIN_DISPLAY_TIME - elapsed);
      setTimeout(function () {
        loader.classList.add('hidden');
        setTimeout(function () {
          if (loader.parentNode) loader.setAttribute('aria-hidden', 'true');
          if (done) done();
        }, 520);
      }, remaining);
    }

    if (document.readyState === 'complete') {
      finish();
    } else {
      window.addEventListener('load', finish, { once: true });
      // safety net in case 'load' never fires quickly (slow subresources)
      setTimeout(finish, 4000);
    }
  };

  window.PXLoader = PXLoader;
})();
