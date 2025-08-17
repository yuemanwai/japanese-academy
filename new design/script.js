console.log("Welcome to JP Academy! The site is ready.");

document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggler
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme');

    const applyTheme = (theme) => {
        if (theme === 'light') {
            document.body.classList.add('light-theme');
            themeToggle.checked = true;
        } else {
            document.body.classList.remove('light-theme');
            themeToggle.checked = false;
        }
    };

    if (currentTheme) {
        applyTheme(currentTheme);
    } else {
        // Optional: Check user's OS preference
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        if (prefersDark) {
            applyTheme('dark');
        } else {
            applyTheme('light');
        }
    }

    themeToggle.addEventListener('change', () => {
        let theme = 'light';
        if (!themeToggle.checked) {
            theme = 'dark';
        }
        localStorage.setItem('theme', theme);
        applyTheme(theme);
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('header a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            } else if (targetId === '#') {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add a simple animation to cards on scroll
    const cards = document.querySelectorAll('.animated-card');

    const observer = new IntersectionObserver(entries => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add a staggered delay
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 100);
                 observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    cards.forEach(card => {
        observer.observe(card);
    });
});