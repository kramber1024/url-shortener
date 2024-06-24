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
    const terms = formData.get("checkbox")?.toString() ? "on" : undefined;

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

    if (!terms) {
        isFormValid = false;
        showError("checkbox", checkboxInput?.getAttribute("data-msg-required") ?? "");
    } else {
        hideError("checkbox");
    }

    if (!isFormValid) {
        return;
    }

    const body = JSON.stringify({ name, email, password, terms });

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
    // 201
});
