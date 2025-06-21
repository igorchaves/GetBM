document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("modalUserStory");
  const openBtn = document.querySelector(".add-btn");
  const closeBtn = modal?.querySelector(".close");
  const cancelBtn = document.getElementById("cancelarModal");

  if (!modal || !openBtn || !closeBtn || !cancelBtn) {
    console.warn("Algum elemento do modal não foi encontrado.");
    return;
  }

  openBtn.addEventListener("click", () => {
    console.log("Botão clicado - abrindo modal");
    modal.style.display = "block";
  });

  closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  cancelBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("click", (event) => {
    });
});

