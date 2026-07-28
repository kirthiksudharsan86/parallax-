/* ── backtotop.js ── Scroll-to-top behavior (Chapter 3 §6) */
(function () {
  var PXBackToTop = {};

  PXBackToTop.init = function () {
    var btn = document.getElementById('back-to-top');
    if (!btn) return;

    function update() {
      btn.classList.toggle('show', (window.scrollY || window.pageYOffset) > 480);
    }
    window.addEventListener('scroll', update, { passive: true });
    update();

    btn.addEventListener('click', function () {
      var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
    });
  };

  window.PXBackToTop = PXBackToTop;
})();
