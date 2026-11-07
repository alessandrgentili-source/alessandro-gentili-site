/* Home EN only. Keep the static skip link when shared JS is unavailable.
   The shared script prepends its own working skip link; retain just that one. */
(() => {
  const fallback = document.querySelector('[data-home-skip]');
  if (fallback && document.querySelector('.skip-link:not([data-home-skip])')) {
    fallback.remove();
  }
})();
