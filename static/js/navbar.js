/* ── navbar.js ── Navigation scroll states + mobile drawer (Chapter 2 §10, Chapter 3 §1) */
(function () {
  var PXNavbar = {};

  PXNavbar.init = function () {
    var nav = document.getElementById('nav');
    if (nav) {
      var update = function () {
        var y = window.scrollY || window.pageYOffset;
        nav.classList.toggle('scrolled', y > 4);
        nav.classList.toggle('shadowed', y > 48);
      };
      update();
      window.addEventListener('scroll', update, { passive: true });
    }

    var hamburger = document.getElementById('nav-hamburger');
    var drawer = document.getElementById('nav-drawer');
    var overlay = document.getElementById('nav-drawer-overlay');
    var closeBtn = document.getElementById('nav-drawer-close');

    if (!hamburger || !drawer || !overlay) return;

    function openDrawer() {
      drawer.classList.add('open');
      overlay.classList.add('open');
      hamburger.classList.add('open');
      hamburger.setAttribute('aria-expanded', 'true');
      document.body.classList.add('drawer-lock');
    }

    function closeDrawer() {
      drawer.classList.remove('open');
      overlay.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('drawer-lock');
    }

    hamburger.addEventListener('click', function () {
      if (drawer.classList.contains('open')) closeDrawer(); else openDrawer();
    });
    overlay.addEventListener('click', closeDrawer);
    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);

    drawer.querySelectorAll('.nav-drawer-link, .nav-drawer-actions a').forEach(function (link) {
      link.addEventListener('click', closeDrawer);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer();
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 860 && drawer.classList.contains('open')) closeDrawer();
    }, { passive: true });
  };

window.PXNavbar = PXNavbar;

document.addEventListener("DOMContentLoaded", function () {
    PXNavbar.init();
});

})();