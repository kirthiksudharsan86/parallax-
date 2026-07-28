/* ── countdown.js ── Live countdown display (Chapter 3 §8) */
(function () {
  var PXCountdown = {};

  function pad(n) { return String(n).padStart(2, '0'); }

  PXCountdown.bind = function (container) {
    var targetAttr = container.getAttribute('data-countdown-target');
    if (!targetAttr) return;
    var target = new Date(targetAttr).getTime();
    if (isNaN(target)) return;

    var d = container.querySelector('[data-cd-days]');
    var h = container.querySelector('[data-cd-hours]');
    var m = container.querySelector('[data-cd-mins]');
    var s = container.querySelector('[data-cd-secs]');

    function tick() {
      var diff = target - Date.now();
      if (diff < 0) diff = 0;
      if (d) d.textContent = pad(Math.floor(diff / 86400000));
      if (h) h.textContent = pad(Math.floor((diff % 86400000) / 3600000));
      if (m) m.textContent = pad(Math.floor((diff % 3600000) / 60000));
      if (s) s.textContent = pad(Math.floor((diff % 60000) / 1000));
    }
    tick();
    setInterval(tick, 1000);
  };

  PXCountdown.init = function () {
    document.querySelectorAll('[data-countdown-target]').forEach(PXCountdown.bind);
  };

  window.PXCountdown = PXCountdown;
})();
