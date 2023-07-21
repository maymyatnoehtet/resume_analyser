// Automatically close the flash message after 5 seconds
document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    var flashMessage = document.querySelector(".flash-msg");
    flashMessage.style.display = "none";
  }, 5000);
});
