document.addEventListener('click', function (e) {
    const isDropdownButton = e.target.closest('.dropdown-toggle');
    const dropdowns = document.querySelectorAll('.dropdown-menu');

    // Fecha todos os menus
    dropdowns.forEach(menu => {
        menu.style.display = 'none';
    });

    // Se clicou no botão de dropdown, abre o menu correspondente
    if (isDropdownButton) {
        const menu = isDropdownButton.nextElementSibling;
        if (menu) {
            menu.style.display = 'block';
        }
    }
});
