/* ── cursor.js ── Custom liquid cursor + fading trail (Chapter 2 §9) */
(function () {
  var PXCursor = {};

  PXCursor.init = function () {
    var isCoarse = window.matchMedia('(hover: none), (pointer: coarse)').matches;
    var isNarrow = window.innerWidth < 1024;
    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (isCoarse || isNarrow || reduced) return;

    var cursor = document.getElementById('custom-cursor');
    var canvas = document.getElementById('cursor-trail-canvas');
    if (!cursor || !canvas || !canvas.getContext) return;

    var ctx = canvas.getContext('2d');
    var TRAIL_LEN = 14;
    var trail = [];
    var mouseX = -100, mouseY = -100;
    var activated = false;

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    function activateOnce() {
      if (activated) return;
      activated = true;
      document.documentElement.classList.add('has-custom-cursor');
      cursor.classList.add('active');
    }

    window.addEventListener('mousemove', function (e) {
      activateOnce();
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursor.style.transform = 'translate(' + mouseX + 'px,' + mouseY + 'px)';

      trail.push({ x: mouseX, y: mouseY });
      if (trail.length > TRAIL_LEN) trail.shift();

      var target = e.target;
      var isInteractive = target.closest && target.closest('a, button, .magnetic, .track-card, .sponsor-card, input, select, textarea, summary, [role="button"]');
      cursor.classList.toggle('pointer', !!isInteractive);
    }, { passive: true });

    window.addEventListener('mouseleave', function () {
      cursor.classList.remove('active');
    });
    window.addEventListener('mouseenter', function () {
      if (activated) cursor.classList.add('active');
    });

    var rafId = null;
    function drawTrail() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (var i = 0; i < trail.length; i++) {
        var pt = trail[i];
        var t = i / trail.length;
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, t * 4 + 0.5, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(0,217,255,' + (t * 0.35) + ')';
        ctx.fill();
      }
      rafId = requestAnimationFrame(drawTrail);
    }
    rafId = requestAnimationFrame(drawTrail);

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        if (rafId) cancelAnimationFrame(rafId);
        rafId = null;
        trail.length = 0;
      } else if (!rafId) {
        rafId = requestAnimationFrame(drawTrail);
      }
    });
  };

  window.PXCursor = PXCursor;
})();
