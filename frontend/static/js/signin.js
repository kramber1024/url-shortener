/**
 * Creates an error label element.
 * 
 * @param {"email" | "password"} type The type of the input element.
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
 * @param {"email" | "password"} type The type of input field that contains errors.
 * @param {string} message Error message to display.
 * @returns {void}
 */
function showError(type, message) {
    let errorLabel = document.getElementById(`${type}-error`);

    if (!errorLabel) {
        errorLabel = createErrorLabel(type, message);
        document.getElementById(type)?.insertAdjacentElement("afterend", errorLabel);
    }

    errorLabel.textContent = message;
}

/**
 * Hides an error message for a specific input type.
 * 
 * @param {"email" | "password"} type The type of input field that contains errors.
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
    button.textContent = "Sign In";
}

const form = document.querySelector("form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
form?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    let isFormValid = true;

    const email = formData.get("email")?.toString().trim();
    const password = formData.get("password")?.toString();

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
        showError("password", passwordInput?.getAttribute("data-msg-required") ?? "");
    } else if (password.length > 256) {
        isFormValid = false;
        showError("password", passwordInput?.getAttribute("data-msg-required") ?? "");
    } else {
        hideError("password");
    }

    if (!isFormValid) {
        return;
    }   
    console.log("go")
    startLoading();
    const body = JSON.stringify({ email, password });
    let response = await fetch("/api/v1/auth/login", {
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
    }
    // 200 logic here
    stopLoading();
});
