const mobileNavQuery = window.matchMedia('(max-width: 760px)');
const dropdownNavItems = document.querySelectorAll('.primary-nav-item--dropdown');

const closePrimaryNavDropdowns = (exceptItem) => {
  dropdownNavItems.forEach((item) => {
    if (item === exceptItem) {
      return;
    }
    item.classList.remove('is-open');
    item.querySelector('.primary-nav-link')?.setAttribute('aria-expanded', 'false');
  });
};

dropdownNavItems.forEach((item) => {
  const trigger = item.querySelector('.primary-nav-link');
  if (!trigger) {
    return;
  }

  trigger.setAttribute('aria-expanded', 'false');
  trigger.addEventListener('click', (event) => {
    if (!mobileNavQuery.matches) {
      return;
    }

    event.preventDefault();
    const isOpen = item.classList.toggle('is-open');
    trigger.setAttribute('aria-expanded', String(isOpen));
    closePrimaryNavDropdowns(item);
  });
});

document.addEventListener('click', (event) => {
  if (!mobileNavQuery.matches || event.target.closest('.primary-nav')) {
    return;
  }

  closePrimaryNavDropdowns();
});

document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') {
    return;
  }

  closePrimaryNavDropdowns();
});

mobileNavQuery.addEventListener('change', () => {
  closePrimaryNavDropdowns();
});
document.querySelectorAll('[data-filter]').forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach((b) => b.setAttribute('aria-pressed', 'false'));
    button.setAttribute('aria-pressed', 'true');
    document.querySelectorAll('[data-archive-item]').forEach((item) => {
      item.hidden = filter !== 'all' && item.dataset.category !== filter;
    });
  });
});

document.querySelectorAll('[data-newsletter-form]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const name = form.querySelector('[name="name"]')?.value.trim() || '';
    const email = form.querySelector('[name="email"]')?.value.trim() || '';
    const feedback = form.querySelector('.feedback');
    const validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!name || !validEmail) {
      if (feedback) {
        feedback.textContent = 'Inserisci nome e indirizzo email valido.';
        feedback.dataset.state = 'error';
      }
      return;
    }
    const subject = encodeURIComponent('Iscrizione alla Lettera periodica');
    const body = encodeURIComponent(`Ciao Alessandro,\n\nvorrei iscrivermi alla Lettera periodica.\n\nNome: ${name}\nEmail: ${email}\n`);
    window.location.href = `mailto:lettera@alessandro-gentili.it?subject=${subject}&body=${body}`;
    if (feedback) {
      feedback.textContent = 'Si aprirà il tuo client email per confermare l’iscrizione.';
      feedback.dataset.state = 'ok';
    }
  });
});
