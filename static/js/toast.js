/* ── toast.js ── Toast notification system (Chapter 3 §5) */
(function () {
  var PXToast = {};
  var LIFETIME = 6000;
  var EXIT_DURATION = 300;

  var ICONS = {
    success: 'fa-solid fa-circle-check',
    error: 'fa-solid fa-circle-exclamation',
    warning: 'fa-solid fa-triangle-exclamation',
    info: 'fa-solid fa-circle-info'
  };

  function ensureStack() {
    var stack = document.getElementById('toast-stack');
    if (!stack) {
      stack = document.createElement('div');
      stack.id = 'toast-stack';
      document.body.appendChild(stack);
    }
    return stack;
  }

  PXToast.show = function (message, type) {
    type = type || 'info';
    var stack = ensureStack();

    var toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.innerHTML =
      '<span class="toast-icon"><i class="' + (ICONS[type] || ICONS.info) + '"></i></span>' +
      '<span class="toast-msg"></span>' +
      '<button type="button" class="toast-close" aria-label="Dismiss notification"><i class="fa-solid fa-xmark"></i></button>';
    toast.querySelector('.toast-msg').textContent = message;

    stack.appendChild(toast);
    requestAnimationFrame(function () { toast.classList.add('toast-show'); });

    var remaining = LIFETIME;
    var timerStart = Date.now();
    var timer = null;

    function dismiss() {
      toast.classList.add('toast-hide');
      toast.classList.remove('toast-show');
      setTimeout(function () {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, EXIT_DURATION);
    }

    function startTimer() {
      timerStart = Date.now();
      timer = setTimeout(dismiss, remaining);
    }
    function pauseTimer() {
      if (timer) {
        clearTimeout(timer);
        remaining -= (Date.now() - timerStart);
      }
    }

    startTimer();
    toast.addEventListener('mouseenter', pauseTimer);
    toast.addEventListener('mouseleave', startTimer);
    toast.querySelector('.toast-close').addEventListener('click', function () {
      pauseTimer();
      dismiss();
    });

    return toast;
  };

  // Convert server-rendered Django messages into toasts on load.
  PXToast.hydrateFromDjangoMessages = function () {
    var block = document.querySelector('.site-messages');
    if (!block) return;
    var rows = block.querySelectorAll(':scope > div');
    rows.forEach(function (row) {
      var text = row.textContent.trim();
      if (!text) return;
      var type = 'info';
      var cls = (row.className || '') + ' ' + (block.className || '');
      if (/success/i.test(cls)) type = 'success';
      else if (/error|danger/i.test(cls)) type = 'error';
      else if (/warning/i.test(cls)) type = 'warning';
      PXToast.show(text, type);
    });
  };

  PXToast.init = function () {
    PXToast.hydrateFromDjangoMessages();
  };

  window.PXToast = PXToast;
  window.showToast = PXToast.show;
})();
