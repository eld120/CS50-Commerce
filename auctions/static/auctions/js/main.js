
// Mobile nav/toggle
const menuToggle = document.querySelector(".mobile-menu-button");
const menuBar = document.querySelector("#nav-menu");

menuToggle.addEventListener("click", () => {
  if (!menuToggle.classList.contains("hide-hamburger")) {
    menuToggle.classList.add("hide-hamburger");
    menuBar.classList.remove("menu-closed");
    menuBar.classList.add("menu-open");
  }
  else {
    menuToggle.classList.remove( "hide-hamburger");
    menuBar.classList.remove("menu-open");
    menuBar.classList.add("menu-closed");
  }
});
