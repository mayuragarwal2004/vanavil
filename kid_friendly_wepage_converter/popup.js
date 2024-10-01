// popup.js

document.getElementById("toggleButton").addEventListener("click", () => {
  console.log("Button clicked");

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    console.log("Sending message to content script in tab:", tabs[0].id);

    chrome.tabs.sendMessage(tabs[0].id, { action: "toggleKidFriendlyMode" }, (response) => {
      console.log("Response from content script:", response);
    });
  });
});
