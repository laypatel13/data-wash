// Set progress bar widths from aria-valuenow
document.querySelectorAll(".progress-bar").forEach(bar => {
  const val = bar.getAttribute("aria-valuenow");
  bar.style.width = val + "%";
});

// Set progress bar widths
document.querySelectorAll(".progress-bar").forEach(bar => {
  const val = bar.getAttribute("aria-valuenow");
  bar.style.width = val + "%";
});

// Page loading spinner with fade in
document.querySelectorAll("a, button[type='submit']").forEach(el => {
  el.addEventListener("click", function () {
    setTimeout(() => {
      const spinner = document.getElementById("dw-spinner");
      if (spinner) {
        spinner.style.opacity = "0";
        spinner.style.display = "flex";
        spinner.style.transition = "opacity 0.3s ease";
        setTimeout(() => spinner.style.opacity = "1", 10);
      }
    }, 150);
  });
});