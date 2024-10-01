# Kid-Friendly Webpage Converter - Chrome Extension

This project is a Chrome extension, located in the `kid_friendly_webpage_converter` folder, that rephrases the content of any webpage to make it simple and kid-friendly by utilizing the Perplexity API. The extension scrapes the text content from the webpage and sends it to the API for rephrasing, then updates the content to display in a more kid-friendly format.

## Features

- Scrapes text content (headings, paragraphs, list items, etc.) from any webpage.
- Sends the scraped content to the Perplexity API to rephrase it for younger audiences.
- Displays the rephrased content as HTML on the same page.
- Toggles between original and kid-friendly content with a button click.
- Handles API tokens securely by hiding them in a separate config file.

## Project Structure

```
kid_friendly_webpage_converter/
│
├── manifest.json             # Chrome extension configuration
├── background.js             # Chrome background script
├── content.js                # Script that interacts with webpage content
├── popup.html                # Popup UI for the extension
├── popup.js                  # JavaScript for the extension popup
├── config.js                 # Hidden file for API token (ignored by Git)
└── README.md                 # Project documentation
```

## Getting Started

### Prerequisites

- Google Chrome (for testing the extension).
- A Perplexity API token (you can sign up for an API key from [Perplexity](https://www.perplexity.ai)).

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/mayuragarwal2004/vanavil.git
   ```

2. **Navigate to the extension folder**:

   ```bash
   cd vanavil/kid_friendly_webpage_converter
   ```

3. **Add your API token**:

   Create a `config.js` file (make sure this file is included in `.gitignore`):

   ```js
   // config.js
   const config = {
     API_TOKEN: "your-perplexity-api-token-here",
   };

   export default config;
   ```

4. **Install the extension**:

   - Open Chrome and go to `chrome://extensions/`.
   - Enable **Developer mode**.
   - Click **Load unpacked** and select the `kid_friendly_webpage_converter` folder.
   - The extension will now be installed in your browser.

5. **Run the extension**:

   - Click the extension icon in your Chrome toolbar.
   - Toggle between original and kid-friendly content using the button in the popup.

## Usage

- **Kid-Friendly Mode**: After activating the extension on a webpage and clicking the button, the content will be scraped and rephrased using the Perplexity API. It will then be displayed in a simpler, kid-friendly format.
  
- **Reset Mode**: Click the button again to reset the page back to its original content.