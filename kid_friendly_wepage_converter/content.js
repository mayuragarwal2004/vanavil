// Import the API token
import config from "./config.js";

let originalContent = ""; // Store original content

// Function to scrape text content from the page
function getTextContent() {
  let bodyText = "";
  const elements = document.body.querySelectorAll(
    "p, h1, h2, h3, h4, h5, h6, li, span"
  );

  elements.forEach((el) => {
    bodyText += el.innerText + " ";
  });

  return bodyText.trim();
}

// Function to call the Perplexity API to rephrase the website content for kids
async function rephraseForKids(content) {
  const apiToken = config.API_TOKEN;

  const options = {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "llama-3.1-sonar-small-128k-online",
      messages: [
        {
          role: "system",
          content: "Rephrase this for kids, making it simple and kid-friendly.",
        },
        { role: "user", content },
      ],
      max_tokens: 2000,
      temperature: 0.2,
      top_p: 0.9,
      return_citations: true,
      search_domain_filter: ["perplexity.ai"],
      return_images: false,
      return_related_questions: false,
      search_recency_filter: "month",
      top_k: 0,
      stream: false,
      presence_penalty: 0,
      frequency_penalty: 1,
    }),
  };

  try {
    const response = await fetch(
      "https://api.perplexity.ai/chat/completions",
      options
    );
    const data = await response.json();
    console.log({ data });

    return data.choices[0].message.content; // Get the rephrased text
  } catch (error) {
    console.error("Error with the API request:", error);
    return null;
  }
}

// Function to make the website kid-friendly
async function makeWebsiteKidFriendly() {
  const scrapedText = getTextContent(); // Get original website content

  const kidFriendlyText = await rephraseForKids(scrapedText); // Rephrase content for kids

  if (kidFriendlyText) {
    // Store the original content
    originalContent = document.body.innerHTML;

    // Replace the content of the page
    const elements = document.body.querySelectorAll(
      "p, h1, h2, h3, h4, h5, h6, li, span"
    );

    let textIndex = 0;
    const sentences = kidFriendlyText.split(". "); // Split rephrased text into sentences

    elements.forEach((el) => {
      const newText = sentences[textIndex++] || el.innerText;
      // Convert Markdown to HTML using marked.js
      el.innerHTML = marked.parse(newText);
    });

    // Set an attribute to indicate kid-friendly mode is active
    document.body.setAttribute('data-kid-friendly', 'true');
  } else {
    console.log("Failed to get kid-friendly content.");
  }
}

// Function to reset the original website content
function resetOriginalContent() {
  if (originalContent) {
    document.body.innerHTML = originalContent; // Restore original content
    document.body.setAttribute('data-kid-friendly', 'false'); // Reset kid-friendly mode
  }
}


async function toggleKidFriendlyMode() {
  const scrapedText = getTextContent(); // Get original website content

  const kidFriendlyText = await rephraseForKids(scrapedText); // Rephrase content for kids

  if (kidFriendlyText) {
    // Replace the content of the page
    const elements = document.body.querySelectorAll(
      "p, h1, h2, h3, h4, h5, h6, li, span"
    );

    let textIndex = 0;
    const sentences = kidFriendlyText.split(". "); // Split rephrased text into sentences

    elements.forEach((el) => {
      const newText = sentences[textIndex++] || el.innerText;
      el.innerText = newText; // Replace each element's text
    });
  } else {
    console.log("Failed to get kid-friendly content.");
  }
}

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "toggleKidFriendlyMode") {
    toggleKidFriendlyMode();
    sendResponse({ status: "Content updated to kid-friendly mode" });
  }
});
