type errorType = "first_name" | "last_name" | "email" | "password" | "terms";

function createErrorLabel(type: errorType, message: string): HTMLLabelElement {
    const label: HTMLLabelElement = document.createElement("label");
    label.id = `${type}-error`;
    label.htmlFor = type;
    label.className = "error";
    label.textContent = message;
    return label;
}

/**
 * Displays an error message for a specific input type.
 * 
 * @param type The type of input field that contains errors.
 * @param message Error message to display.
 */
export function showError(type: errorType, message: string): void {
    let errorLabel: HTMLLabelElement | null = document.getElementById(`${type}-error`) as HTMLLabelElement;

    if (!errorLabel) {
        errorLabel = createErrorLabel(type, message);
        
        if (type === "terms") {
            const termsContainerDiv = document.querySelector(".form__terms-container") as HTMLDivElement;
            termsContainerDiv.insertAdjacentElement("afterend", errorLabel);
        } else {
            const inputElement = document.getElementById(type) as HTMLInputElement;
            inputElement.after(errorLabel);
        }
    }

    errorLabel.textContent = message;
}

/**
 * Hides an error message for a specific input type.
 * 
 * @param type The type of input field that contains errors.
 */
export function hideError(type: errorType): void {
    const errorLabel = document.getElementById(`${type}-error`) as HTMLLabelElement;
    if (errorLabel) {
        errorLabel.remove();
    }
}

/**
 * Starts the loading state by disabling the button and displaying a loader.
 */
export function startLoading(): void {
    const loaderDiv = document.createElement("div");
    loaderDiv.className = "loader";
    const button = document.querySelector("button") as HTMLButtonElement;
    button.disabled = true;
    button.dataset.message = button.textContent as string;
    button.textContent = "";
    button.appendChild(loaderDiv);
}

/**
 * Stops the loading state by hiding loader and enabling the button.
 */
export function stopLoading(): void {
    const button = document.querySelector("button") as HTMLButtonElement;
    button.disabled = false;
    button.textContent = button.dataset.message as string;
    button.removeAttribute("data-message");
}
