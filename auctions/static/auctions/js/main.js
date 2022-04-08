// Mobile nav/toggle
const menuToggle = document.querySelector(".mobile-menu-button");
const menuBar = document.querySelector("#nav-menu");
const endDate = document.querySelector("#listing-end-date").innerHTML;
const auctionEnd = document.querySelector("#auction-end");

menuToggle.addEventListener("click", () => {
  if (!menuToggle.classList.contains("hide-hamburger")) {
    menuToggle.classList.add("hide-hamburger");
    menuBar.classList.remove("menu-closed");
    menuBar.classList.add("menu-open");
  } else {
    menuToggle.classList.remove("hide-hamburger");
    menuBar.classList.remove("menu-open");
    menuBar.classList.add("menu-closed");
  }
});

function listingCountdown() {
  let today = new Date();
  let timedelta = Date.parse(endDate) - today;

  let day = Math.floor(timedelta / 86400000);
  let hour = Math.floor(timedelta / 3600000);
  let minute = Math.floor(timedelta / 60000);
  let second = Math.floor(timedelta / 1000);

  if (timedelta <= 0) {
    document.querySelector("#auction-end-outer").outerHTML = "<p class='alert'>Auction Ended</p>";
    document.querySelector("#bid-submit").classList.add('sr-only')
  } else if (day < 1 && hour < 1) {
    auctionEnd.innerHTML = `${minute} min ${second} s`;
  } else if (day < 1) {
    auctionEnd.innerHTML = `${hour} hr ${minute} min`;
  } else {
    auctionEnd.innerHTML = `${day} day ${hour} hr`;
  }
}
setInterval(listingCountdown, 1000);
