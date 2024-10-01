chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: toggleKidFriendlyMode,
  });
});

function toggleKidFriendlyMode() {
  console.log("Toggling kid-friendly mode");
  
  if (document.body.getAttribute('data-kid-friendly') === 'true') {
    resetOriginalContent();
  } else {
    makeWebsiteKidFriendly();
  }
}
