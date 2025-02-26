# LinkHive Backend API

## Overview

This backend API provides user registration, login, and referral system functionalities for a platform similar to Linktr.ee or Bento.me. It is built using Django Rest Framework (DRF), leveraging JWT for authentication, and includes various features like password reset, referral system, and rate limiting.

## Features

- **User Registration & Authentication**: Users can register with email, username, and password. JWT is used for secure authentication and token management.
- **Referral System**: Existing users can refer new users with a unique referral link. Rewards can be issued for successful referrals.
- **Password Reset**: Users can reset passwords using email-based tokens.
- **Rate Limiting**: Protection against abuse by limiting the number of requests to registration and login endpoints.
- **Security**: Passwords are securely hashed, and the system is protected against common vulnerabilities.

## API Endpoints

### 1. **User Registration**
- **Endpoint**: `POST /api/register/`
- **Request Body**:
    ```json
    {
      "email": "user@example.com",
      "username": "user123",
      "password": "strongpassword",
      "referral_code": "referral_code123"  // Optional
    }
    ```
- **Response**:
    - **201 Created**: User successfully registered.
    - **400 Bad Request**: Email already in use or invalid referral code.
    - **429 Too Many Requests**: Rate limit exceeded.

### 2. **User Login**
- **Endpoint**: `POST /api/login/`
- **Request Body**:
    ```json
    {
      "email": "user@example.com",
      "password": "strongpassword"
    }
    ```
- **Response**:
    - **200 OK**: Login successful, returns JWT token.
    - **401 Unauthorized**: Invalid credentials.
    - **429 Too Many Requests**: Rate limit exceeded.

### 3. **Forgot Password**
- **Endpoint**: `POST /api/forgot-password/`
- **Request Body**:
    ```json
    {
      "email": "user@example.com"
    }
    ```
- **Response**:
    - **200 OK**: Password reset link sent to email.
    - **404 Not Found**: User with the provided email does not exist.

### 4. **Referral Stats**
- **Endpoint**: `GET /api/referral-stats/`
- **Response**:
    - **200 OK**: Returns the number of successful sign-ups made through the user's referral link.

### 5. **Referral Link**
- **Endpoint**: `GET /api/referral-link/`
- **Response**:
    - **200 OK**: Returns the user's unique referral link.

### 6. **Reset Password**
- **Endpoint**: `POST /api/reset-password/{token}/`
- **Request Body**:
    ```json
    {
      "username": "user123",
      "new_password": "newpassword123"
    }
    ```
- **Response**:
    - **200 OK**: Password successfully reset.
    - **400 Bad Request**: Invalid or expired token.
    - **404 Not Found**: User not found.


## Rate Limiting

Rate limiting is applied to prevent abuse:
- **Registration**: A maximum of 5 requests per minute per IP address.
- **Login**: A maximum of 5 requests per minute per IP address.

## Security

- **JWT Tokens**: Securely stored in HttpOnly cookies.
- **Password Hashing**: Uses Django’s secure password hashing algorithm (Argon2).
- **Protection Against SQL Injection, XSS, CSRF**: The application is designed to protect against these common vulnerabilities.
- **Rate Limiting**: To prevent brute-force attacks on the login and registration endpoints.

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Start the Django development server:
      ```bash
   python manage.py runserver
   ```


## Testing
### Unit and integration tests are implemented for:

- Registration and login endpoints.
- Referral system logic (including referral code validation).
- Password reset functionality.
- Ensure that edge cases such as invalid referral codes, self-referrals, and tracking of successful referrals are handled.

