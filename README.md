# Trendyol Chrome Extension README

This repository contains the files for a Chrome extension. The extension adds a custom "Import" button to web pages on the 'https://www.trendyol.com/' domain when it is installed or updated.

## Directory Structure

- **images**: This directory contains icon images of different sizes (16x16, 48x48, and 128x128 pixels) used for the extension's icon.

- **packages**: This directory includes the jQuery library ('jquery-3.6.0.min.js') that the extension may use for DOM manipulation.

- **background.js**: This JavaScript file is a background script for the extension. It contains code that runs in the background and manages extension functionality.

- **content.js**: This JavaScript file is a content script injected into web pages. It is responsible for adding the "Import" button to the target web page.

- **index.html**: This HTML file represents the popup that appears when you click on the extension's icon in the Chrome toolbar. It may contain additional UI elements or settings.

- **manifest.json**: The manifest file is a crucial part of a Chrome extension. It defines metadata about the extension, including permissions, icons, background scripts, content scripts, and more.

- **popup.js**: This JavaScript file is used for controlling the behavior of the extension's popup (defined in `index.html`).

- **README.md**: The file you're currently reading. It provides information about the extension and directory structure.

- **styles.css**: This CSS file can be used to style the extension's popup or any other UI components.

## Extension Description

This Chrome extension enhances the browsing experience on 'https://www.trendyol.com/' by adding an "Import" button to relevant pages. The button allows users to perform a specific action on the website.

## Installation

To install the extension:

1. Open Google Chrome.

2. Navigate to `chrome://extensions/`.

3. Enable "Developer mode" in the top right corner of the Extensions page.

4. Click on the "Load unpacked" button.

5. Select the directory containing these extension files.

6. The extension should now be installed and active in your Chrome browser.

## Usage

Once the extension is installed and active, it will add the "Import" button to web pages on 'https://www.trendyol.com/' whenever the extension is installed or updated.

