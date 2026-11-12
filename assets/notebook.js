const toggleCode = document.querySelector('#toggle-code');
toggleCode.addEventListener('click', () => {
 const hide = toggleCode.getAttribute('aria-pressed') !== 'true';
 document.querySelectorAll('.nb-code').forEach(cell => { cell.open = !hide; });
 toggleCode.setAttribute('aria-pressed', String(hide));
 toggleCode.textContent = hide ? 'Show code' : 'Hide code';
});
