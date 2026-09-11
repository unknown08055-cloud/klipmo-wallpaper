// ---------------------------------------------------------------------
// Blur-up image loading: images start slightly blurred/faded via the
// .blur-up CSS class, and get .is-loaded added the instant they finish
// loading (or immediately if they were already cached).
// ---------------------------------------------------------------------
(function () {
  var imgs = document.querySelectorAll('img.blur-up');
  imgs.forEach(function (img) {
    if (img.complete && img.naturalWidth > 0) {
      img.classList.add('is-loaded');
    } else {
      img.addEventListener('load', function () { img.classList.add('is-loaded'); }, { once: true });
      img.addEventListener('error', function () { img.classList.add('is-loaded'); }, { once: true });
    }
  });
})();

// ---------------------------------------------------------------------
// Scroll reveal: fade/slide elements in as they enter the viewport.
// Falls back to showing everything immediately if IntersectionObserver
// isn't available, and does nothing extra for prefers-reduced-motion
// (CSS already neutralises .reveal in that case).
// ---------------------------------------------------------------------
(function () {
  var targets = document.querySelectorAll('.reveal');
  if (!targets.length) return;

  if (!('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('is-visible'); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });

  targets.forEach(function (el) { observer.observe(el); });

  // Safety net: if IntersectionObserver misbehaves in some edge-case browser,
  // never leave content permanently invisible -- force it visible shortly
  // after load regardless.
  setTimeout(function () {
    targets.forEach(function (el) { el.classList.add('is-visible'); });
  }, 2500);
})();

// ---------------------------------------------------------------------
// Hover-to-preview: live wallpaper cards in any grid play a muted video
// loop on hover/focus instead of their static poster image.
// ---------------------------------------------------------------------
(function () {
  var liveCards = document.querySelectorAll('.wall-card[data-type="live"]');
  liveCards.forEach(function (card) {
    var video = card.querySelector('.card-hover-video');
    if (!video) return;

    var loaded = false;
    function start() {
      if (!loaded) {
        var src = video.getAttribute('data-src');
        if (src) video.src = src;
        loaded = true;
      }
      video.play().catch(function () { /* autoplay may be blocked; poster stays visible */ });
    }
    function stop() {
      video.pause();
      video.currentTime = 0;
    }

    card.addEventListener('mouseenter', start);
    card.addEventListener('mouseleave', stop);
    card.addEventListener('focus', start);
    card.addEventListener('blur', stop);
  });
})();

// ---------------------------------------------------------------------
// Wallpaper detail page: Phone / Laptop preview toggle. Swaps which pane
// is shown, lazy-loads + plays the relevant video if this is a live
// wallpaper, and highlights the matching download button.
// ---------------------------------------------------------------------
(function () {
  var toggle = document.querySelector('.wp-preview-toggle');
  if (!toggle) return;

  var buttons = toggle.querySelectorAll('[data-preview-btn]');
  var panes = document.querySelectorAll('.wp-pane');
  var downloadLinks = document.querySelectorAll('[data-download]');

  function activate(device) {
    buttons.forEach(function (btn) {
      var isMatch = btn.getAttribute('data-preview-btn') === device;
      btn.classList.toggle('is-active', isMatch);
      btn.setAttribute('aria-selected', isMatch ? 'true' : 'false');
    });

    panes.forEach(function (pane) {
      var isMatch = pane.getAttribute('data-pane') === device;
      pane.classList.toggle('is-active', isMatch);
      var video = pane.querySelector('video[data-src]');
      if (video) {
        if (isMatch) {
          if (!video.src) video.src = video.getAttribute('data-src');
          video.play().catch(function () {});
        } else {
          video.pause();
        }
      }
    });

    downloadLinks.forEach(function (link) {
      var isMatch = link.getAttribute('data-download') === device;
      link.classList.toggle('btn-primary', isMatch);
      link.classList.toggle('btn-outline', !isMatch);
    });
  }

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      activate(btn.getAttribute('data-preview-btn'));
    });
  });

  // Start the initially-active (phone) video playing, same as the old
  // autoplay behaviour, without duplicating the activate() side effects.
  var initialVideo = document.querySelector('.wp-pane.is-active video[data-src]');
  if (initialVideo) {
    initialVideo.src = initialVideo.getAttribute('data-src');
    initialVideo.play().catch(function () {});
  }
})();

// ---------------------------------------------------------------------
// Browse-all page: search / category / type filtering, with a small
// "pop" animation on the cards that remain visible after each change.
// ---------------------------------------------------------------------
(function () {
  var grid = document.querySelector('[data-filter-grid]');
  if (!grid) return;

  var searchInput = document.querySelector('[data-filter-search]');
  var categorySelect = document.querySelector('[data-filter-category]');
  var typeSelect = document.querySelector('[data-filter-type]');
  var cards = Array.prototype.slice.call(grid.querySelectorAll('[data-card]'));
  var emptyState = document.querySelector('[data-empty-state]');
  var firstRun = true;

  function apply() {
    var q = (searchInput && searchInput.value || '').trim().toLowerCase();
    var cat = (categorySelect && categorySelect.value) || 'all';
    var type = (typeSelect && typeSelect.value) || 'all';
    var visible = 0;

    cards.forEach(function (card) {
      var haystack = (card.getAttribute('data-search') || '').toLowerCase();
      var cardCat = card.getAttribute('data-category');
      var cardType = card.getAttribute('data-type');

      var matches =
        (q === '' || haystack.indexOf(q) !== -1) &&
        (cat === 'all' || cardCat === cat) &&
        (type === 'all' || cardType === type);

      card.style.display = matches ? '' : 'none';
      if (matches) {
        visible++;
        if (!firstRun) {
          card.classList.remove('just-filtered');
          void card.offsetWidth; // restart the animation
          card.classList.add('just-filtered');
        }
      }
    });

    if (emptyState) emptyState.hidden = visible !== 0;
    firstRun = false;
  }

  [searchInput, categorySelect, typeSelect].forEach(function (el) {
    if (el) el.addEventListener('input', apply);
  });

  apply();
})();
