// Import translations if in a module environment
let translationsObj;
try {
  translationsObj = translations;
} catch (e) {
  // If translations is not defined globally, try to import it
  if (typeof require !== "undefined") {
    try {
      translationsObj = require("./translations").translations;
    } catch (err) {
      console.error("Could not load translations:", err);
      translationsObj = {};
    }
  } else {
    console.error("Translations not available");
    translationsObj = {};
  }
}

// Function to update page content based on language
function updatePageContent(language) {
  if (!translationsObj || !translationsObj[language]) return;

  const trans = translationsObj[language];

  // Update navbar items
  document.querySelectorAll("[data-trans]").forEach((element) => {
    const key = element.getAttribute("data-trans");
    if (trans[key]) {
      element.textContent = trans[key];
    }
  });

  // Set the direction based on the language
  const html = document.querySelector("html");
  if (language === "he") {
    html.setAttribute("dir", "rtl");
    html.setAttribute("lang", "he");
  } else {
    html.setAttribute("dir", "ltr");
    html.setAttribute("lang", "en");
  }

  // Store the selected language in session storage
  sessionStorage.setItem("selectedLanguage", language);
}

// Language switcher
document.addEventListener("DOMContentLoaded", function () {
  const languageSwitcher = document.getElementById("language-switcher");
  if (!languageSwitcher) return;

  // Retrieve the selected language from session storage
  const storedLanguage = sessionStorage.getItem("selectedLanguage") || "en";

  // Update the page content and language switcher text
  updatePageContent(storedLanguage);
  const languageText = languageSwitcher.querySelector(".language-text");
  if (languageText) {
    languageText.textContent =
      storedLanguage === "he" ? "Switch to English" : "Switch to Hebrew";
  }

  languageSwitcher.addEventListener("click", function (e) {
    e.preventDefault();
    const html = document.querySelector("html");
    const languageText = this.querySelector(".language-text");

    if (html.getAttribute("dir") === "rtl") {
      html.setAttribute("dir", "ltr");
      html.setAttribute("lang", "en");
      if (languageText) languageText.textContent = "Switch to Hebrew";
      updatePageContent("en");
    } else {
      html.setAttribute("dir", "rtl");
      html.setAttribute("lang", "he");
      if (languageText) languageText.textContent = "Switch to English";
      updatePageContent("he");
    }
  });
});
