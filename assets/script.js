document.querySelectorAll('[data-filter]').forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach((b) => b.setAttribute('aria-pressed', 'false'));
    button.setAttribute('aria-pressed', 'true');
    document.querySelectorAll('[data-archive-item]').forEach((article) => {
      article.hidden = filter !== 'all' && article.dataset.category !== filter;
    });
  });
});

const form = document.getElementById('newsletter-form');
if (form) {
  const emailInput = document.getElementById('email');
  const feedback = document.getElementById('newsletter-feedback');
  form.addEventListener('submit', (event) => {
    const value = emailInput.value.trim();
    const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    if (!valid) {
      event.preventDefault();
      feedback.textContent = 'Inserisci un indirizzo email valido prima di inviare il modulo.';
      feedback.dataset.state = 'error';
      emailInput.setAttribute('aria-invalid', 'true');
      emailInput.focus();
      return;
    }
    feedback.textContent = 'Formato email valido. Puoi procedere con l’iscrizione.';
    feedback.dataset.state = 'ok';
    emailInput.removeAttribute('aria-invalid');
  });
}
