'use strict';

// No network requests, cookies, analytics, or persistent browser storage.
document.documentElement.classList.add('js');
const menuButton = document.querySelector('[data-menu-toggle]');
const navigation = document.querySelector('#site-navigation');
function closeMenu() {
  if (!menuButton || !navigation) return;
  menuButton.setAttribute('aria-expanded', 'false');
  navigation.classList.remove('is-open');
}
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  navigation?.classList.toggle('is-open', open);
});
navigation?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});
document.addEventListener('click', event => {
  if (!navigation?.contains(event.target) && !menuButton?.contains(event.target)) closeMenu();
});

document.querySelectorAll('[data-filter-region]').forEach(region => {
  const buttons = [...region.querySelectorAll('[data-filter]')];
  const items = [...region.querySelectorAll('[data-category]')];
  const input = region.querySelector('input[type="search"]');
  const count = region.querySelector('[data-result-count]');
  const empty = region.querySelector('[data-empty]');
  let selected = 'all';
  function update() {
    const term = (input?.value || '').trim().toLocaleLowerCase();
    let visible = 0;
    for (const item of items) {
      const matches = (selected === 'all' || item.dataset.category === selected)
        && item.textContent.toLocaleLowerCase().includes(term);
      item.hidden = !matches;
      if (matches) visible += 1;
    }
    const noun = region.dataset.resultNoun || 'results';
    if (count) count.textContent = `${visible} ${visible === 1 ? noun.replace(/s$/, '') : noun} shown`;
    if (empty) empty.hidden = visible !== 0;
  }
  for (const button of buttons) button.addEventListener('click', () => {
    selected = button.dataset.filter;
    for (const other of buttons) other.setAttribute('aria-pressed', String(other === button));
    update();
  });
  input?.addEventListener('input', update);
  region.querySelector('[data-clear-filters]')?.addEventListener('click', () => {
    selected = 'all';
    if (input) input.value = '';
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === 'all')));
    update();
    input?.focus();
  });
  update();
});

const themeButton = document.querySelector('[data-theme-toggle]');
themeButton?.addEventListener('click', () => {
  const isDark = document.documentElement.dataset.theme !== 'dark';
  document.documentElement.dataset.theme = isDark ? 'dark' : 'light';
  themeButton.setAttribute('aria-pressed', String(isDark));
  themeButton.setAttribute('aria-label', isDark ? 'Switch to light theme' : 'Switch to dark theme');
});

document.querySelectorAll('[data-copy-email]').forEach(button => button.addEventListener('click', async () => {
  const status = document.querySelector('[data-copy-status]');
  try {
    if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
    await navigator.clipboard.writeText('aliawais4413@gmail.com');
    if (status) status.textContent = 'Email address copied.';
  } catch {
    if (status) status.textContent = 'Copy this email address: aliawais4413@gmail.com';
  }
}));

const pageSections = [...document.querySelectorAll('main > section[id]')];
if ('IntersectionObserver' in window && pageSections.length) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      navigation?.querySelectorAll('a[href*="#"]').forEach(link => {
        const destination = new URL(link.href, window.location.href);
        if (destination.pathname === window.location.pathname && destination.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
  }, {rootMargin: '-15% 0px -60% 0px'});
  pageSections.forEach(section => observer.observe(section));
}
