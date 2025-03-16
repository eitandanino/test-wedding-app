// Language switcher
document.getElementById('language-switcher').addEventListener('click', function() {
    const html = document.querySelector('html');
    if (html.getAttribute('dir') === 'rtl') {
        html.setAttribute('dir', 'ltr');
        this.textContent = 'Switch to Hebrew';
    } else {
        html.setAttribute('dir', 'rtl');
        this.textContent = 'Switch to English';
    }
});