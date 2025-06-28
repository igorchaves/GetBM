document.addEventListener("DOMContentLoaded", function () {
  const openButtons = document.querySelectorAll("[data-modal-target]");
  const closeButtons = document.querySelectorAll(".modal .close, .modal .btn-secondary");

  openButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const modalId = btn.getAttribute("data-modal-target");
      const modal = document.getElementById(modalId);
      if (modal) {
        modal.style.display = "block";
      } else {
        console.warn(`Modal com ID "${modalId}" não encontrado.`);
      }
    });
  });

  closeButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const modal = btn.closest(".modal");
      if (modal) {
        modal.style.display = "none";
      }
    });
  });

  window.addEventListener("click", (event) => {
    if (event.target.classList.contains("modal")) {
      event.target.style.display = "none";
    }
  });
});
