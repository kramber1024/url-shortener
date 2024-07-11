import { showError, hideError, startLoading, stopLoading } from "./auth";
import { Error } from "./schemes";

const form = document.querySelector("form") as HTMLFormElement;
const firstNameInput = document.getElementById("first_name") as HTMLInputElement;
const lastNameInput = document.getElementById("last_name") as HTMLInputElement;
const emailInput = document.getElementById("email") as HTMLInputElement;
const passwordInput = document.getElementById("password") as HTMLInputElement;
const checkboxInput = document.getElementById("terms") as HTMLInputElement;
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData: FormData = new FormData(form);
    let isFormValid = true;

    const firstName = (formData.get("first_name") as string).trim();
    const lastName = (formData.get("last_name") as string).trim();
    const email = (formData.get("email") as string).trim();
    const password = formData.get("password") as string;
    const terms = formData.get("terms") as string ? "on" : "off";

    // Validate first name
    if (!firstName) {
        isFormValid = false;
        showError("first_name", firstNameInput.getAttribute("data-msg-required") as string);
    } else if (firstName.length < 3) {
        isFormValid = false;
        showError("first_name", firstNameInput.getAttribute("data-msg-minlength") as string);
    } else if (firstName.length > 32) {
        isFormValid = false;
        showError("first_name", firstNameInput.getAttribute("data-msg-maxlength") as string);
    } else {
        hideError("first_name");
    }

    // Validate last name
    if (!lastName) {
        formData.delete("last_name");
    }
    if (lastName.length < 3 && lastName.length > 0) {
        isFormValid = false;
        showError("last_name", lastNameInput.getAttribute("data-msg-minlength") as string);
    } else if (lastName.length > 32) {
        isFormValid = false;
        showError("last_name", lastNameInput.getAttribute("data-msg-maxlength")  as string);
    } else {
        hideError("last_name");
    }

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
    if (!password) {
        isFormValid = false;
        showError("password", passwordInput.getAttribute("data-msg-required") as string);
    } else if (password.length < 8) {
        isFormValid = false;
        showError("password", passwordInput.getAttribute("data-msg-minlength") as string);
    } else if (password.length > 256) {
        isFormValid = false;
        showError("password", passwordInput.getAttribute("data-msg-maxlength") as string);
    } else {
        hideError("password");
    }

    // Validate terms
    if (terms !== "on") {
        isFormValid = false;
        showError("terms", checkboxInput.getAttribute("data-msg-required") as string);
    } else {
        hideError("terms");
    }

    if (!isFormValid) {
        return;
    }

    startLoading();
    let body = JSON.stringify(Object.fromEntries(formData.entries()));
    let response: Response = await fetch("/api/auth/register", {
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
        case 409: {
            showError("email", emailInput.getAttribute("data-msg-conflict") as string);
            break;
        }
        case 201: {
            body = JSON.stringify({ email, password });
            response = await fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body,
            });
            
            if (response.status === 200) {
                // go to app
            } else {
                window.location.href = "/login";
            }
            break;
        }
    }
    stopLoading();
});
