// Set progress bar widths from aria-valuenow
document.querySelectorAll(".progress-bar").forEach(bar => {
  const val = bar.getAttribute("aria-valuenow");
  bar.style.width = val + "%";
});