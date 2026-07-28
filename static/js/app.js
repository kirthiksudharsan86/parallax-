/* ── app.js ── Global initialization / dependency order (Chapter 2 §2, Chapter 6 §17) */
(function () {
  function initAmbientGlow() {
    var glow = document.getElementById('cursor-glow');
    if (!glow) return;
    if (window.matchMedia && window.matchMedia('(hover: none), (pointer: coarse)').matches) return;
    window.addEventListener('mousemove', function (e) {
      glow.style.left = e.clientX + 'px';
      glow.style.top = e.clientY + 'px';
    }, { passive: true });
  }

  function initCore() {
    initAmbientGlow();
    if (window.PXNavbar) window.PXNavbar.init();
    if (window.PXScroll) window.PXScroll.init();
    if (window.PXParticles) window.PXParticles.init();
    if (window.PXCursor) window.PXCursor.init();
    if (window.PXInteractions) window.PXInteractions.init();
    if (window.PXFaq) window.PXFaq.init();
    if (window.PXToast) window.PXToast.init();
    if (window.PXCountdown) window.PXCountdown.init();
    if (window.PXBackToTop) window.PXBackToTop.init();
  }

  function boot() {
    // 1. Loader runs first and gates the rest of the interaction system.
    if (window.PXLoader) {
      window.PXLoader.init(initCore);
    } else {
      initCore();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  // Re-run initialization cheaply when the page is restored from the
  // back-forward cache, so animations/particles/cursor don't appear frozen
  // after switching tabs or navigating back.
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) {
      var loader = document.getElementById('loader');
      if (loader) loader.classList.add('hidden');
      if (window.PXParticles) window.PXParticles.init();
      if (window.PXScroll) {
        window.PXScroll.observeReveal(document);
        window.PXScroll.forceRevealVisible(document);
      }
    }
  });
})();
