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

      // TODO refactor into an iterable

    day = timedelta / 86400000,
    hour =  (day - Math.floor(day)) * 24,
    minute = (hour - Math.floor(hour)) * 60,
    second = (minute - Math.floor(minute)) * 60,

      second = Math.floor(second)
      hour = Math.floor(hour)
      minute = Math.floor(minute)
      day = Math.floor(day)

  if (timedelta <= 0) {
    document.querySelector("#auction-end-outer").outerHTML = "<p class='alert'>Auction Ended</p>";
    document.querySelector("#bid-submit").classList.add('sr-only')
  } else if (day < 1 && hour < 1) {
    auctionEnd.innerHTML = `${minute} mins ${second} s`;
  } else if (day < 1) {
    auctionEnd.innerHTML = `${hour} hrs ${minute} mins`;
  } else {
    auctionEnd.innerHTML = `${day} days ${hour} hrs`;
  }
}
setInterval(listingCountdown, 1000);
