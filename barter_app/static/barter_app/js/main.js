/**
 * Обработка сообщений
 */
document.addEventListener('DOMContentLoaded', function() {
    const closeButtons = document.querySelectorAll('.message__close');
    
    closeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const message = this.closest('.message');
            message.style.opacity = '0';
            setTimeout(function() {
                message.style.display = 'none';
            }, 300);
        });
    });
});

/**
 * Обработка навигации в мобильной версии
 */
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.header__menu-toggle');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            const menu = document.querySelector('.header__menu');
            menu.classList.toggle('header__menu--active');
            
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            menuToggle.setAttribute('aria-expanded', !isExpanded);
        });
    }
});
