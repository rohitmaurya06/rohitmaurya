
document.addEventListener("DOMContentLoaded", () => {
  const navbar = document.getElementById("mainNav");
  const navMenu = document.getElementById("navMenu");
  const navLinks = document.querySelectorAll(".nav-link");

  // Dynamic copyright year
  document.getElementById("year").textContent =
    new Date().getFullYear();

  // Navbar shadow while scrolling
  function handleScroll() {
    navbar.classList.toggle("scrolled", window.scrollY > 30);
  }

  // Highlight the current section in navigation
  const sections = document.querySelectorAll("main section[id]");

  function updateActiveLink() {
    let activeId = "home";

    sections.forEach(section => {
      const sectionTop = section.offsetTop - 160;

      if (window.scrollY >= sectionTop) {
        activeId = section.id;
      }
    });

    navLinks.forEach(link => {
      link.classList.toggle(
        "active",
        link.getAttribute("href") === `#${activeId}`
      );
    });
  }

  // Close mobile menu after selecting a link
  navLinks.forEach(link => {
    link.addEventListener("click", () => {
      if (navMenu.classList.contains("show")) {
        bootstrap.Collapse
          .getOrCreateInstance(navMenu)
          .hide();
      }
    });
  });

  // Smooth scrolling for internal links
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", event => {
      const targetId = link.getAttribute("href");

      if (targetId === "#") {
        event.preventDefault();
        return;
      }

      const target = document.querySelector(targetId);

      if (target) {
        event.preventDefault();

        target.scrollIntoView({
          behavior: window.matchMedia(
            "(prefers-reduced-motion: reduce)"
          ).matches ? "auto" : "smooth",
          block: "start"
        });
      }
    });
  });

  window.addEventListener("scroll", () => {
    handleScroll();
    updateActiveLink();
  }, { passive: true });

  handleScroll();
  updateActiveLink();
});
 
  