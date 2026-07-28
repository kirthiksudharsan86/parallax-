/* ── particles.js ── Interactive neural-network background (Chapter 2 §6) */
(function () {
  var PXParticles = {};

  PXParticles.init = function () {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var canvas = document.getElementById('particles-canvas');
    if (!canvas || !canvas.getContext) return;
    var ctx = canvas.getContext('2d');

    var width, height, dpr;
    var particles = [];
    var mouse = { x: -9999, y: -9999 };
    var isTouch = window.matchMedia('(hover: none), (pointer: coarse)').matches;

    function deviceConfig() {
      var w = window.innerWidth;
      if (isTouch) return { count: 45, linkDist: 90 };
      if (w <= 1024) return { count: 60, linkDist: 110 };
      return { count: 110, linkDist: 130 };
    }

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = width + 'px';
      canvas.style.height = height + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function makeParticles() {
      var cfg = deviceConfig();
      particles = [];
      for (var i = 0; i < cfg.count; i++) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.28,
          vy: (Math.random() - 0.5) * 0.28,
          r: Math.random() * 1.6 + 0.6
        });
      }
      particles.linkDist = cfg.linkDist;
    }

    function step() {
      ctx.clearRect(0, 0, width, height);
      var linkDist = particles.linkDist;

      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        if (!isTouch) {
          var dxm = p.x - mouse.x, dym = p.y - mouse.y;
          var distM = Math.sqrt(dxm * dxm + dym * dym);
          if (distM < 140) {
            var force = (140 - distM) / 140 * 0.04;
            p.vx += (dxm / (distM || 1)) * force;
            p.vy += (dym / (distM || 1)) * force;
          }
        }

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(0,217,255,0.65)';
        ctx.fill();
      }

      for (var a = 0; a < particles.length; a++) {
        for (var b = a + 1; b < particles.length; b++) {
          var dx = particles[a].x - particles[b].x;
          var dy = particles[a].y - particles[b].y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < linkDist) {
            ctx.beginPath();
            ctx.moveTo(particles[a].x, particles[a].y);
            ctx.lineTo(particles[b].x, particles[b].y);
            ctx.strokeStyle = 'rgba(0,82,204,' + (1 - dist / linkDist) * 0.42 + ')';
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }
      }
    }

    var rafId = null;
    function runFrame() {
      step();
      rafId = requestAnimationFrame(runFrame);
    }

    resize();
    makeParticles();
    rafId = requestAnimationFrame(runFrame);

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        if (rafId) cancelAnimationFrame(rafId);
        rafId = null;
      } else if (!rafId) {
        resize();
        rafId = requestAnimationFrame(runFrame);
      }
    });

    window.addEventListener('resize', function () {
      resize();
      makeParticles();
    }, { passive: true });

    if (!isTouch) {
      window.addEventListener('mousemove', function (e) {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
      }, { passive: true });
    }
  };

  window.PXParticles = PXParticles;
})();
