function toggleMenu() {
    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main");
    const toggleBtn = document.getElementById("menuToggle");

    sidebar.classList.toggle("expanded");

    if (sidebar.classList.contains("expanded")) {
        main.style.marginLeft = "200px";
        main.style.width = "calc(100% - 200px)";
        toggleBtn.textContent = "✖";
    } else {
        main.style.marginLeft = "60px";
        main.style.width = "calc(100% - 60px)";
        toggleBtn.textContent = "☰";

        // Fecha todos os submenus ao recolher o menu
        document.querySelectorAll(".submenu").forEach(sub => sub.classList.remove("open"));
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");

    // Seleciona todos os links com submenu
    const submenuTriggers = sidebar.querySelectorAll(".has-submenu");

    submenuTriggers.forEach(trigger => {
        trigger.addEventListener("click", function (e) {
            e.preventDefault();

            // Verifica se o menu está expandido antes de abrir submenu
            if (!sidebar.classList.contains("expanded")) return;

            const submenu = this.nextElementSibling;
            if (submenu && submenu.classList.contains("submenu")) {
                submenu.classList.toggle("open");
            }
        });
    });
});


