/* ── interactions.js ── Magnetic buttons & 3D card tilt (Chapter 2 §7-8) */
(function () {
  var PXInteractions = {};

  var MAGNETIC_SELECTOR = '.magnetic, .nav-register-btn, .nav-login-btn, .btn-cta';
  var TILT_SELECTOR = '.track-card, .sponsor-card, .expect-card, .person-card, ' +
    '.prize-track-card, .prize-pool-card, .info-card';
  var STRENGTH = 18;
  var MAX_TILT = 8;

  function isTouch() {
    return window.matchMedia('(hover: none), (pointer: coarse)').matches;
  }
  function reduced() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function bindMagnetic(root) {
    if (isTouch() || reduced()) return;
    root.querySelectorAll(MAGNETIC_SELECTOR + ':not([data-magnetic-bound])').forEach(function (el) {
      el.setAttribute('data-magnetic-bound', '1');
      el.addEventListener('mousemove', function (e) {
        el.style.transition = 'transform .1s ease-out';
        var rect = el.getBoundingClientRect();
        var relX = e.clientX - rect.left - rect.width / 2;
        var relY = e.clientY - rect.top - rect.height / 2;
        var moveX = (relX / (rect.width / 2)) * STRENGTH;
        var moveY = (relY / (rect.height / 2)) * STRENGTH;
        el.style.transform = 'translate(' + moveX + 'px,' + moveY + 'px)';
      });
      el.addEventListener('mouseleave', function () {
        el.style.transition = 'transform .35s var(--ease)';
        el.style.transform = 'translate(0,0)';
      });
    });
  }

  function bindTilt(root) {
    if (isTouch() || reduced()) return;
    root.querySelectorAll(TILT_SELECTOR + ':not([data-tilt-bound])').forEach(function (el) {
      el.setAttribute('data-tilt-bound', '1');
      el.addEventListener('mousemove', function (e) {
        el.style.transition = 'transform .1s ease-out, box-shadow .4s var(--ease)';
        var rect = el.getBoundingClientRect();
        var px = (e.clientX - rect.left) / rect.width;
        var py = (e.clientY - rect.top) / rect.height;
        var rotY = (px - 0.5) * MAX_TILT * 2;
        var rotX = (0.5 - py) * MAX_TILT * 2;
        el.style.transform = 'perspective(900px) rotateX(' + rotX + 'deg) rotateY(' + rotY + 'deg) translateY(-4px)';
      });
      el.addEventListener('mouseleave', function () {
        el.style.transition = 'transform .35s var(--ease), box-shadow .4s var(--ease)';
        el.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) translateY(0)';
      });
    });
  }

  PXInteractions.rebind = function (root) {
    root = root || document;
    bindMagnetic(root);
    bindTilt(root);
  };

  PXInteractions.init = function () {
    PXInteractions.rebind(document);
    // Expose the documented global rebind hook for dynamically inserted content
    window.__PARALLAX_REBIND_TILT__ = function (root) {
      PXInteractions.rebind(root || document);
      if (window.PXScroll) window.PXScroll.observeReveal(root || document);
    };
  };

  window.PXInteractions = PXInteractions;
})();
