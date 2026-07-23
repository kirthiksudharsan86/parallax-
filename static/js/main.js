// ── PARALLAX main.js ── HackForge + Parallax fusion

// Scroll progress bar
const progressBar = document.getElementById('progress-bar');
if (progressBar) {
  window.addEventListener('scroll', () => {
    const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
    progressBar.style.width = scrolled + '%';
  }, { passive: true });
}

// Cursor glow effect
const cursorGlow = document.getElementById('cursor-glow');
if (cursorGlow) {
  document.addEventListener('mousemove', (e) => {
    cursorGlow.style.left = e.clientX + 'px';
    cursorGlow.style.top = e.clientY + 'px';
  }, { passive: true });
}

// Nav scroll state
const nav = document.getElementById('nav');
if (nav) {
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 40);
  }, { passive: true });
}

// Scroll reveal via IntersectionObserver
(function () {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
})();

// Parallax scroll on hero geometry (home only)
const geoWrap = document.getElementById('geoWrap');
if (geoWrap) {
  window.addEventListener('scroll', () => {
    geoWrap.style.transform = 'translateY(' + (window.scrollY * 0.16) + 'px)';
  }, { passive: true });
}

// Reference hero countdown: counts down to the event date while retaining safe fallback values.
(() => {
  const ids = ['count-days','count-hours','count-mins','count-secs'];
  if (!ids.every(id => document.getElementById(id))) return;
  const target = new Date('2026-08-18T00:00:00+05:30').getTime();
  const tick = () => {
    const diff = Math.max(0, target - Date.now());
    const vals = [Math.floor(diff/86400000), Math.floor(diff/3600000)%24, Math.floor(diff/60000)%60, Math.floor(diff/1000)%60];
    ids.forEach((id,i) => document.getElementById(id).textContent = String(vals[i]).padStart(2,'0'));
  };
  tick(); setInterval(tick,1000);
})();
