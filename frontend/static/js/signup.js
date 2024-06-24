/**
 * @param {"name" | "email" | "password" | "checkbox"} type 
 * @param {string} message 
 * @returns {HTMLLabelElement}
 */
function createErrorLabel(type, message) {
    const label = document.createElement("label");
    label.id = `${type}-error`;
    label.htmlFor = type;
    label.className = "error";
    label.textContent = message;
    return label;
}

/**
 * @param {"name" | "email" | "password" | "checkbox"} type 
 * @param {string} message
 * @returns {void}
 */
function showError(type, message) {
    let errorLabel = document.getElementById(`${type}-error`);

    if (!errorLabel) {
        errorLabel = createErrorLabel(type, message);
        if (type === "checkbox") {
            document.querySelector(".form__terms-container")?.insertAdjacentElement("afterend", errorLabel);
        }
        else {
            document.getElementById(type)?.insertAdjacentElement("afterend", errorLabel);
        }
    }

    errorLabel.textContent = message;
}

/**
 * @param {"name" | "email" | "password" | "checkbox"} type
 * @returns {void}
 */
function hideError(type) {
    document.getElementById(`${type}-error`)?.remove();
}

const form = document.querySelector("form");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const checkboxInput = document.getElementById("checkbox");
form?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    let isFormValid = true;

    const name = formData.get("name")?.toString().trim();
    const email = formData.get("email")?.toString().trim();
    const password = formData.get("password")?.toString();
    const checkbox = formData.get("checkbox")?.toString() ? true : false;

    if (!name) {
        isFormValid = false;
        showError("name", nameInput?.getAttribute("data-msg-required") ?? "");
    } else if (name.length < 3) {
        isFormValid = false;
        showError("name", nameInput?.getAttribute("data-msg-minlength") ?? "");
    } else if (name.length > 32) {
        isFormValid = false;
        showError("name", nameInput?.getAttribute("data-msg-maxlength") ?? "");
    } else {
        hideError("name");
    }

    if (!email) {
        isFormValid = false;
        showError("email", emailInput?.getAttribute("data-msg-required") ?? "");
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 64 || email.length < 5) {
        isFormValid = false;
        showError("email", emailInput?.getAttribute("data-msg-invalid") ?? "");
    } else {
        hideError("email");
    }

    if (!password) {
        isFormValid = false;
        showError("password", passwordInput?.getAttribute("data-msg-required") ?? "");
    } else if (password.length < 8) {
        isFormValid = false;
        showError("password", passwordInput?.getAttribute("data-msg-minlength") ?? "");
    } else if (password.length > 256) {
        isFormValid = false;
        showError("password", passwordInput?.getAttribute("data-msg-maxlength") ?? "");
    } else {
        hideError("password");
    }

    if (!checkbox) {
        isFormValid = false;
        showError("checkbox", checkboxInput?.getAttribute("data-msg-required") ?? "");
    } else {
        hideError("checkbox");
    }

    if (!isFormValid) {
        return;
    }

    
});
