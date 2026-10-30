// Theme switcher shared script
(function(){
    const themeBtns = document.querySelectorAll('.theme-toggle button');
    const darkToggle = document.getElementById('darkToggle');
    const themes = ['cool', 'warm', 'neutral'];

    function applyTheme(theme){
        if (!themes.includes(theme)) theme = 'cool';
        themes.forEach(t => document.documentElement.classList.remove('cv-theme-' + t));
        document.documentElement.classList.add('cv-theme-' + theme);

        // Card-level widgets for upload pages
        const uploadCard = document.querySelector('.upload-card');
        if (uploadCard) {
            themes.forEach(t => uploadCard.classList.remove('theme-' + t));
            uploadCard.classList.add('theme-' + theme);
        }

        if (themeBtns) {
            themeBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.theme === theme));
        }

        localStorage.setItem('cv_theme', theme);
    }

    function applyDarkMode(enabled){
        if (enabled) {
            document.documentElement.classList.add('dark-mode');
        } else {
            document.documentElement.classList.remove('dark-mode');
        }

        if (darkToggle) darkToggle.checked = enabled;
        localStorage.setItem('cv_dark', enabled ? '1' : '0');
    }

    if (themeBtns && themeBtns.length) {
        themeBtns.forEach(btn => btn.addEventListener('click', () => applyTheme(btn.dataset.theme)));
        const savedTheme = localStorage.getItem('cv_theme') || 'cool';
        applyTheme(savedTheme);
    } else {
        // still apply stored theme even if no buttons (for consistency across pages)
        const savedTheme = localStorage.getItem('cv_theme') || 'cool';
        themes.forEach(t => document.documentElement.classList.remove('cv-theme-' + t));
        document.documentElement.classList.add('cv-theme-' + savedTheme);
    }

    if (darkToggle) {
        darkToggle.addEventListener('change', () => applyDarkMode(darkToggle.checked));
    }
    const savedDark = localStorage.getItem('cv_dark') === '1';
    applyDarkMode(savedDark);
})();
