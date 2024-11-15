const toggleButton = document.getElementById("toggleButton");

// Fetch the current state and update the button
chrome.storage.local.get("enabled", (data) => {
    const enabled = data.enabled || false;
    updateButtonState(enabled);
});

// Add a click listener to toggle the state
toggleButton.addEventListener("click", () => {
    chrome.storage.local.get("enabled", (data) => {
        const enabled = data.enabled || false;
        const newState = !enabled;

        // Save the new state
        chrome.storage.local.set({ enabled: newState });

        // Notify all tabs about the new state
        chrome.tabs.query({}, (tabs) => {
            tabs.forEach((tab) => {
                chrome.tabs.sendMessage(tab.id, { enabled: newState });
            });
        });

        // Update the button state
        updateButtonState(newState);
    });
});

// Function to update the button's appearance and text
function updateButtonState(enabled) {
    if (enabled) {
        toggleButton.textContent = "Turn Off";
        toggleButton.classList.remove("off");
        toggleButton.classList.add("on");
    } else {
        toggleButton.textContent = "Turn On";
        toggleButton.classList.remove("on");
        toggleButton.classList.add("off");
    }
}
