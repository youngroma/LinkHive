# ReferralHive Backend API Documentation

## Overview

This backend API is designed to offer essential user management functionalities, including user registration, login, and a comprehensive referral system. It is developed using Django Rest Framework (DRF) with JWT (JSON Web Token) authentication for secure user sessions. The platform offers several key features, such as password recovery, a reward-based referral system, and rate limiting, creating an engaging and interactive user experience

## Features

- **User Registration & Authentication**: Users can register with email, username, and password. JWT is used for secure authentication and token management.
- **Referral System**: Existing users can refer new users with a unique referral link. Rewards can be issued for successful referrals.
- **Password Reset**: Users can reset passwords using email-based tokens.
- **Rate Limiting**: Protection against abuse by limiting the number of requests to registration and login endpoints.
- **Security**: Passwords are securely hashed, and the system is protected against common vulnerabilities.
- **Jenkins Integration**: The project uses Jenkins for CI/CD, automating the build, test, and deployment processes to ensure smooth and reliable development cycles.

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
      "confirm_password": "newpassword123"
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

## CI/CD with Jenkins

This project uses Jenkins for Continuous Integration and Continuous Deployment (CI/CD). The Jenkins pipeline automates the process of building, testing, and deploying the application, ensuring efficient and error-free development cycles.

Pipeline Stages:
- Create .env File
- Build Docker Image
- Run Tests
- Push Docker Image to Registry
- Post Actions
  - Cleaning up unused Docker images
  - Deleting the .env file

### Credentials and Secrets Management
The pipeline uses Jenkins' Credentials Manager to securely manage and use sensitive data such as the SECRET_KEY, DB_USER, and DB_PASSWORD. These credentials are stored in Jenkins and are accessed using the withCredentials block to ensure that no sensitive information is exposed in the pipeline.

### Docker Registry
The image is pushed to Docker Hub using the docker.withRegistry block. This enables the team to have access to the latest Docker image version for deployment and testing in different environments.
