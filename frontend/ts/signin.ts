import { showError, hideError, startLoading, stopLoading } from "./auth";
import { Error } from "./schemes";

const form = document.querySelector("form") as HTMLFormElement;
const emailInput = document.getElementById("email") as HTMLInputElement;
const passwordInput = document.getElementById("password") as HTMLInputElement;
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData: FormData = new FormData(form);
    let isFormValid = true;

    const email = (formData.get("email") as string).trim();
    const password = formData.get("password") as string;

    // Validate email
    if (!email) {
        isFormValid = false;
        showError("email", emailInput.getAttribute("data-msg-required") as string);
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 64 || email.length < 5) {
        isFormValid = false;
        showError("email", emailInput.getAttribute("data-msg-invalid") as string);
    } else {
        hideError("email");
    }

    // Validate password
    if (!password || password.length < 8 || password.length > 256) {
        isFormValid = false;
        showError("password", passwordInput.getAttribute("data-msg-required") as string);
    } else {
        hideError("password");
    }

    if (!isFormValid) {
        return;
    }

    startLoading();
    let body = JSON.stringify(Object.fromEntries(formData.entries()));
    let response: Response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body,
    });
    const result = await response.json();
    const errors: Error[] = result.errors;

    switch (response.status) {
        case 422: {
            errors.forEach((error) => {
                if (error.type === "email") {
                    showError("email", emailInput.getAttribute("data-msg-invalid") as string);
                }
            });
            break;
        }
        case 401: {
            showError("password", passwordInput.getAttribute("data-msg-incorrect") as string);
            showError("email", emailInput.getAttribute("data-msg-incorrect") as string);
            break;
        }
        case 200: {
            // go to app
            break;
        }
    }
    stopLoading();
});
