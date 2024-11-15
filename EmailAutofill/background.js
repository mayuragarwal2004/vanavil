let enabled = false;

// Initialize the state from storage when the extension loads
chrome.runtime.onStartup.addListener(() => {
  chrome.storage.local.get("enabled", (data) => {
    enabled = data.enabled || false;
    updateActionIcon();
  });
});

// Update the icon and tooltip
function updateActionIcon() {
  chrome.action.setIcon({
    path: enabled ? "icon-on.png" : "icon-off.png"
  });
  chrome.action.setTitle({
    title: enabled ? "Disable Email Autofill" : "Enable Email Autofill"
  });
}

// Listen for toolbar button clicks to toggle the state
chrome.action.onClicked.addListener((tab) => {
  enabled = !enabled;

  // Save the state
  chrome.storage.local.set({ enabled });

  // Update the icon and tooltip
  updateActionIcon();

  // Notify the content script of the current state
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]) {
      chrome.tabs.sendMessage(tabs[0].id, { enabled });
    }
  });
});

// Notify all tabs of the current state when the extension starts
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get("enabled", (data) => {
    enabled = data.enabled || false;
    chrome.tabs.query({}, (tabs) => {
      tabs.forEach((tab) => {
        chrome.tabs.sendMessage(tab.id, { enabled });
      });
    });
  });
});
