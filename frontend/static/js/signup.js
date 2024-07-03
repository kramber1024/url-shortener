/**
 * Creates an error label element.
 * 
 * @param {"first_name" | "last_name" | "email" | "password" | "terms"} type The type of the input element.
 * @param {string} message The error message to display.
 * @returns {HTMLLabelElement} The created error label element.
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
 * Displays an error message for a specific input type.
 * 
 * @param {"first_name" | "last_name" | "email" | "password" | "terms"} type The type of input field that contains errors.
 * @param {string} message Error message to display.
 * @returns {void}
 */
function showError(type, message) {
    let errorLabel = document.getElementById(`${type}-error`);

    if (!errorLabel) {
        errorLabel = createErrorLabel(type, message);
        if (type === "terms") {
            document.querySelector(".form__terms-container")?.insertAdjacentElement("afterend", errorLabel);
        }
        else {
            document.getElementById(type)?.insertAdjacentElement("afterend", errorLabel);
        }
    }

    errorLabel.textContent = message;
}

/**
 * Hides an error message for a specific input type.
 * 
 * @param {"first_name" | "last_name" | "email" | "password" | "terms"} type The type of input field that contains errors.
 * @returns {void}
 */
function hideError(type) {
    document.getElementById(`${type}-error`)?.remove();
}

/**
 * Starts the loading state by disabling the button and displaying a loader.
 * 
 * @returns {void}
 */
function startLoading() {
    const loaderDiv = document.createElement("div");
    loaderDiv.className = "loader";
    const button = document.querySelector("button") ?? HTMLButtonElement.prototype;
    button.disabled = true
    button.textContent = "";
    button.appendChild(loaderDiv);
}

/**
 * Stops the loading state by hiding loader and enabling the button.
 * 
 * @returns {void}
 */
function stopLoading() {
    const button = document.querySelector("button") ?? HTMLButtonElement.prototype;
    button.disabled = false;
    button.textContent = "Create Account";
}

const form = document.querySelector("form");
const firstNameInput = document.getElementById("first_name");
const lastNameInput = document.getElementById("last_name");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const checkboxInput = document.getElementById("terms");
form?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    let isFormValid = true;

    const first_name = formData.get("first_name")?.toString().trim();
    const last_name = formData.get("last_name")?.toString().trim() ?? "";
    const email = formData.get("email")?.toString().trim();
    const password = formData.get("password")?.toString();
    const terms = formData.get("terms")?.toString() ? "on" : undefined;

    // Check first name
    if (!first_name) {
        isFormValid = false;
        showError("first_name", firstNameInput?.getAttribute("data-msg-required") ?? "");
    } else if (first_name.length < 3) {
        isFormValid = false;
        showError("first_name", firstNameInput?.getAttribute("data-msg-minlength") ?? "");
    } else if (first_name.length > 32) {
        isFormValid = false;
        showError("first_name", firstNameInput?.getAttribute("data-msg-maxlength") ?? "");
    } else {
        hideError("first_name");
    }

    // Check last name
    if (!last_name) {
        formData.delete("last_name");
    }
    if (last_name.length < 3 && last_name.length > 0) {
        isFormValid = false;
        showError("last_name", lastNameInput?.getAttribute("data-msg-minlength") ?? "");
    } else if (last_name.length > 32) {
        isFormValid = false;
        showError("last_name", lastNameInput?.getAttribute("data-msg-maxlength") ?? "");
    } else {
        hideError("last_name");
    }

    // Check email
    if (!email) {
        isFormValid = false;
        showError("email", emailInput?.getAttribute("data-msg-required") ?? "");
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 64 || email.length < 5) {
        isFormValid = false;
        showError("email", emailInput?.getAttribute("data-msg-invalid") ?? "");
    } else {
        hideError("email");
    }

    // Check password
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

    // Check terms
    if (!terms) {
        isFormValid = false;
        showError("terms", checkboxInput?.getAttribute("data-msg-required") ?? "");
    } else {
        hideError("terms");
    }

    if (!isFormValid) {
        return;
    }

    startLoading();
    const body = JSON.stringify(Object.fromEntries(formData.entries())); 
    let response = await fetch("/api/v1/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body,
    });
    const result = await response.json();
    /**
     * @typedef {Object} Error
     * @property {string} type
     * @property {string} message
     */
    /** @type {Error[]} */
    const errors = result.errors;

    if (response.status === 422) {
        errors.forEach(error => {
            if (error.type === "email") {
                showError("email", emailInput?.getAttribute("data-msg-invalid") ?? "");
            }
        });
    } else if (response.status === 409) {
        showError("email", emailInput?.getAttribute("data-msg-conflict") ?? "");
    }
    // 201 logic here
    stopLoading();
});
