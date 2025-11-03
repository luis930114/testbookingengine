document.addEventListener("DOMContentLoaded", function() {
                document.querySelectorAll(".progress-bar").forEach(function(bar) {
                    const width = bar.style.width;
                    bar.style.width = "0";
                    setTimeout(() => { bar.style.width = width; }, 300);
                });
            });