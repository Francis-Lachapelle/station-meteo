document.addEventListener('DOMContentLoaded', () => {
    // Functions to open and close a modal
    function openModal($el) {
        $el.classList.add('is-active');
    }

    function closeModal($el) {
        $el.classList.remove('is-active');
    }

    function closeAllModals() {
        (document.querySelectorAll('.modal') || []).forEach(($modal) => {
            closeModal($modal);
        });
    }

    // Add a click event on buttons to open a specific modal
    (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
        const modal = $trigger.dataset.target;
        const $target = document.getElementById(modal);
        $trigger.addEventListener('click', () => {
            openModal($target);
        });
    });

    // Add a click event on various child elements to close the parent modal
    (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
        const $target = $close.closest('.modal');

        $close.addEventListener('click', () => {
            closeModal($target);
        });
    });

    // Add a keyboard event to close all modals
    document.addEventListener('keydown', (event) => {
        if (event.key === "Escape") {
            closeAllModals();
        }
    });

    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Add a click event on each of them
    $navbarBurgers.forEach(el => {
        el.addEventListener('click', () => {

            // Get the target from the "data-target" attribute
            const target = el.dataset.target;
            const $target = document.getElementById(target);

            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');

        });
    });

    const savedTheme = localStorage.getItem("theme");
    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)").matches;


    if (savedTheme === "dark" || (!savedTheme && prefersDarkScheme)) {
        toggleThemeIcons('theme-dark')
    } else {
        toggleThemeIcons('theme-light')
    }

    function toggleThemeIcons(theme) {

        const icons = document.getElementsByClassName('icon')
        for (const icon of icons) {
            const darkIconPath = icon.getAttribute("data-dark-icon");
            const lightIconPath = icon.getAttribute("data-light-icon");
            icon.src = theme === 'theme-light' ? darkIconPath : lightIconPath
        }
    }

    function toggleTheme() {
        const $html = document.getElementsByTagName('html')[0]
        const theme = $html.className === 'theme-dark' ? 'theme-light' : 'theme-dark'
        $html.className = theme
        toggleThemeIcons(theme)
    }

    document.getElementById('toggleTheme').addEventListener('click', toggleTheme)

    const sensorModal = document.getElementById('sensor-modal');
    const sensorModalTitle = document.getElementById('sensor-modal-title');
    const sensorModalData = document.getElementById('sensor-modal-data');

    document.querySelectorAll('.option-button').forEach(button => {
        button.addEventListener('click', async (event) => {
            const sensorId = event.target.getAttribute('data-id');
            const itemData = await (await fetch('/update-section')).text()

            if (itemData) {
                // Update modal content with the selected data
                sensorModalTitle.textContent = `${sensorId}`;
                sensorModalData.innerHTML = `
                    ${itemData}
                `;

                // Show the modal
                sensorModal.classList.add('is-active');
            }
        });
    });
});

async function updateContent() {
    try {
        // Make an asynchronous request to the server
        const response = await fetch('/update-section');

        // Check if the response is okay (status code 200)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Convert the response to text
        const data = await response.text();

        // Update the dynamic section with the new content
        document.getElementById('dynamic-section').innerHTML = data;

    } catch (error) {
        console.error('Error fetching the content:', error);
    }
}
