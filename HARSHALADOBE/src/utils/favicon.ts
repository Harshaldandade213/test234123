/**
 * Utility function to dynamically set the favicon
 * This can be used if the app needs to change favicons programmatically
 */

export function setFavicon(href: string): void {
  const link = document.querySelector('link[rel*="icon"]') || document.createElement('link');
  link.rel = 'icon';
  link.href = href;
  
  // Remove any existing favicon links to avoid duplicates
  const existingLinks = document.querySelectorAll('link[rel*="icon"]');
  existingLinks.forEach(existingLink => {
    if (existingLink !== link) {
      existingLink.remove();
    }
  });
  
  document.head.appendChild(link);
}

/**
 * Set the default Adobe+ favicon
 */
export function setAdobePlusFavicon(): void {
  setFavicon('/adobe-plus.svg');
}

/**
 * Set favicon based on theme preference
 */
export function setThemeAwareFavicon(): void {
  const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  setFavicon('/adobe-plus.svg'); // Both themes use the same SVG for now
}

/**
 * Initialize favicon with theme awareness
 */
export function initializeFavicon(): void {
  // Set initial favicon
  setAdobePlusFavicon();
  
  // Listen for theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', setThemeAwareFavicon);
}
