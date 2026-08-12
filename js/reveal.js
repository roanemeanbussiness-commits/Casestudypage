/* Scroll reveal.
   Elements lift into place as they enter the viewport, staggered a little
   within each group so a row of metrics arrives in sequence rather than all
   at once. The hiding styles are scoped to .js, so with JavaScript off the
   page renders as plain static content with nothing missing. */
(function () {
  var root = document.documentElement;

  // Anyone who has asked for less motion gets the page with none of this.
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  root.classList.add('js');

  // Groups whose children should arrive one after another, and the lone
  // elements that just fade up on their own.
  var GROUPS = '.rollup, .scale-strip, .case-grid, .systems, .metrics, .steps';
  var SINGLES = '.hero > .eyebrow, .hero > h1, .hero > .sub, .case-head,' +
                '.sys-title, .case-note, .how > h2, .cta';

  var items = [];

  document.querySelectorAll(GROUPS).forEach(function (group) {
    Array.prototype.forEach.call(group.children, function (child, i) {
      child.classList.add('reveal');
      // Cap the stagger so a five-item list never feels slow to finish.
      child.style.transitionDelay = Math.min(i, 5) * 70 + 'ms';
      items.push(child);
    });
  });

  document.querySelectorAll(SINGLES).forEach(function (el) {
    el.classList.add('reveal');
    items.push(el);
  });

  var show = function (el) { el.classList.add('in'); };

  if (!('IntersectionObserver' in window)) {
    items.forEach(show);
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      show(entry.target);
      observer.unobserve(entry.target);
    });
  }, {
    // Fire a little before the element reaches the bottom edge, so it is
    // already settled by the time it is properly in view.
    rootMargin: '0px 0px -12% 0px',
    threshold: 0.05
  });

  items.forEach(function (el) { observer.observe(el); });

  // Anything already on screen at load reveals immediately, in order,
  // rather than waiting for a scroll that may never come.
  requestAnimationFrame(function () {
    items.forEach(function (el) {
      if (el.getBoundingClientRect().top < window.innerHeight) show(el);
    });
  });
})();
