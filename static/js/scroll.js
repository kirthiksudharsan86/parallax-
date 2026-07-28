/* ── scroll.js ── Scroll reveal engine + progress indicator (Chapter 2 §4-5) */
(function () {
  var PXScroll = {};

  var SELECTORS = '.reveal, .section-header, .why-card, .track-card, .sponsor-card, ' +
    '.expect-card, .person-card, .lead-box, .prize-track-card, .prize-pool-card, ' +
    '.oc-panel, .info-card, .placeholder-card';

  var STAGGER_MS = 85;
  var STAGGER_CYCLE = 6;

  function reduceMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  PXScroll.observeReveal = function (root) {
    root = root || document;
    var nodes = root.querySelectorAll(SELECTORS + ':not(.reveal-bound)');
    if (!nodes.length) return;

    if (reduceMotion() || !('IntersectionObserver' in window)) {
      nodes.forEach(function (el) {
        el.classList.add('reveal-bound', 'in', 'visible');
      });
      return;
    }

    var counter = 0;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var delay = (counter % STAGGER_CYCLE) * STAGGER_MS;
        counter++;
        el.style.transitionDelay = delay + 'ms';
        el.classList.add('in', 'visible');
        io.unobserve(el);
      });
    }, { threshold: 0.15 });

    nodes.forEach(function (el) {
      el.classList.add('reveal', 'reveal-bound');
      io.observe(el);
    });
  };

  PXScroll.initProgress = function () {
    var bar = document.getElementById('progress-bar');
    if (!bar) return;
    var ticking = false;
    function update() {
      var scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      var pct = scrollHeight > 0 ? (window.scrollY / scrollHeight) * 100 : 0;
      bar.style.width = Math.min(100, Math.max(0, pct)) + '%';
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) {
        window.requestAnimationFrame(update);
        ticking = true;
      }
    }, { passive: true });
    update();
  };

  // Safety net: if an element was already bound but never crossed the
  // IntersectionObserver threshold (e.g. bfcache restore froze it mid-way),
  // reveal it immediately if it's currently on-screen instead of leaving it stuck at opacity:0.
  PXScroll.forceRevealVisible = function (root) {
    root = root || document;
    var nodes = root.querySelectorAll(SELECTORS + '.reveal-bound:not(.in)');
    nodes.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        el.classList.add('in', 'visible');
      }
    });
  };

  PXScroll.init = function () {
    PXScroll.initProgress();
    PXScroll.observeReveal(document);
  };

  window.PXScroll = PXScroll;
})();
