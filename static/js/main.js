(function () {
    const toggle = document.querySelector("[data-crm-menu-toggle]");
    const close = document.querySelector("[data-crm-menu-close]");
    const menu = document.querySelector("[data-crm-mobile-menu]");
    const backdrop = document.querySelector("[data-crm-mobile-backdrop]");

    if (!toggle || !menu || !backdrop) {
        return;
    }

    function openMenu() {
        menu.classList.add("is-open");
        menu.setAttribute("aria-hidden", "false");
        toggle.setAttribute("aria-expanded", "true");
        backdrop.hidden = false;
        document.body.classList.add("crm-menu-open");
    }

    function closeMenu() {
        menu.classList.remove("is-open");
        menu.setAttribute("aria-hidden", "true");
        toggle.setAttribute("aria-expanded", "false");
        backdrop.hidden = true;
        document.body.classList.remove("crm-menu-open");
    }

    toggle.addEventListener("click", openMenu);

    if (close) {
        close.addEventListener("click", closeMenu);
    }

    backdrop.addEventListener("click", closeMenu);

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeMenu();
        }
    });

    menu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", closeMenu);
    });
})();