console.log("Welcome to JP Academy! The modern theme is ready.");

document.addEventListener("DOMContentLoaded", () => {
  // Theme Toggler
  const themeToggle = document.getElementById("theme-toggle");
  const currentTheme = localStorage.getItem("theme");

  const applyTheme = (theme) => {
    if (theme === "light") {
      document.body.classList.add("light-theme");
      if (themeToggle) themeToggle.checked = true;
    } else {
      document.body.classList.remove("light-theme");
      if (themeToggle) themeToggle.checked = false;
    }
  };

  if (currentTheme) {
    applyTheme(currentTheme);
  } else {
    // Check user's OS preference
    const prefersDark =
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches;
    if (prefersDark) {
      applyTheme("dark");
    } else {
      applyTheme("light");
    }
  }

  if (themeToggle) {
    themeToggle.addEventListener("change", () => {
      let theme = "light";
      if (!themeToggle.checked) {
        theme = "dark";
      }
      localStorage.setItem("theme", theme);
      applyTheme(theme);
    });
  }

  // Smooth scrolling for navigation links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();

      const targetId = this.getAttribute("href");
      const targetElement = document.querySelector(targetId);

      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: "smooth",
        });
      } else if (targetId === "#") {
        window.scrollTo({
          top: 0,
          behavior: "smooth",
        });
      }
    });
  });

  // Add animation to cards on scroll
  const cards = document.querySelectorAll(".animated-card, .glass-panel");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          // Add a staggered delay
          setTimeout(() => {
            entry.target.classList.add("visible");
          }, index * 100);
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
    }
  );

  cards.forEach((card) => {
    observer.observe(card);
  });

  // Update active navigation link based on current page
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll(".navbar-nav .nav-link");

  navLinks.forEach((link) => {
    const href = link.getAttribute("href");
    if (href && currentPath.includes(href.replace("/", ""))) {
      link.classList.add("active");
    }
  });
});

// Function to show loading state
function showLoading(element) {
  if (element) {
    element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    element.disabled = true;
  }
}

// Function to hide loading state
function hideLoading(element, originalText) {
  if (element) {
    element.innerHTML = originalText;
    element.disabled = false;
  }
}
