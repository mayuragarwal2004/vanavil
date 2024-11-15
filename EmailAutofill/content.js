// Define the email to populate
const predefinedEmail = "milo@codingspots.com";

// Function to populate email fields
function autofillEmail() {
  const emailInputs = document.querySelectorAll('input[type="email"]');
  emailInputs.forEach((input) => {
    if (!input.value) {
      input.value = predefinedEmail;
      input.dispatchEvent(new Event("input", { bubbles: true }));
    }
  });
}

// Observe DOM changes for dynamic email popups
let observer;
function startAutofill() {
  autofillEmail();
  if (!observer) {
    observer = new MutationObserver(() => autofillEmail());
    observer.observe(document.body, { childList: true, subtree: true });
  }
}

function stopAutofill() {
  if (observer) {
    observer.disconnect();
    observer = null;
  }
}

// Check and start autofill when the page loads
chrome.storage.local.get("enabled", (data) => {
  if (data.enabled) {
    startAutofill();
  }
});

// Listen for messages to toggle functionality
chrome.runtime.onMessage.addListener((message) => {
  if (message.enabled) {
    startAutofill();
  } else {
    stopAutofill();
  }
});
