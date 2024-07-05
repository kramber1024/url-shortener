export interface Error {
    message: string;
    type: string;
}

export interface ErrorResponse {
    errors: Error[];
    message: string;
    status: number;
}

export interface SuccessResponse {
    message: string;
    status: number;
}

export interface User {
    id: string;
    first_name: string;
    last_name: string | null;
    email: string;
}
