

// Initialize Tippy.js for elements with data-tippy-content
document.addEventListener('DOMContentLoaded', function () {
    tippy('[data-tippy-content]', {
        // You can add more options here, like animation, theme, etc.
        animation: 'fade',
        arrow: true,
        delay: [100, 100],
        theme: 'light-border',
    });
});