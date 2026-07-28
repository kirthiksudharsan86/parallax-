/* ── faq.js ── Accordion behavior: single-open-item rule (Chapter 3 §4)
   The open/close animation itself is pure CSS (grid-template-rows 0fr -> 1fr
   on .faq-body, see information.html). This keeps JS to just the toggle
   logic, so there is nothing here that can get stuck mid-animation or
   clip/hide the answer text. */
(function () {
  var PXFaq = {};

  PXFaq.init = function () {
    var items = document.querySelectorAll('.faq-item');
    if (!items.length) return;

    items.forEach(function (item) {
      // Let the browser's native <details> toggle happen on click (don't
      // fight it with preventDefault). Just react to the 'toggle' event to
      // enforce the single-open-item rule.
      item.addEventListener('toggle', function () {
        if (!item.open) return;
        items.forEach(function (other) {
          if (other !== item) other.removeAttribute('open');
        });
      });
    });
  };

  window.PXFaq = PXFaq;
})();
