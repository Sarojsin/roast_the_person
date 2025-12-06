# Deploying to Render with Blueprint

This guide explains how to deploy the "Roast My Profile" application to Render using the "Blueprint" (Infrastructure as Code) feature.

## Prerequisites

- A [Render](https://render.com) account.
- This repository pushed to GitHub or GitLab.

## Deployment Steps

1.  **Create a New Blueprint Instance**
    - Go to your Render Dashboard.
    - Click **New +** -> **Blueprint**.
    - Connect your repository.

2.  **Configuration**
    Render will automatically detect the `render.yaml` file and show you the services it will create:
    - `roast-backend` (Web Service)
    - `roast-frontend` (Static Site)

3.  **Environment Variables**
    You will be prompted to provide values for the following variables (marked as `sync: false` in the blueprint):

    - **GEMINI_API_KEY**: Your Google Gemini API Key.
    - **CORS_ORIGINS**: The URL of your frontend.
        > **Tip**: Since the frontend URL isn't generated until *after* the blueprint is created, you can initially set this to `*` (asterisk) or `http://localhost:3000` to let the deployment proceed. Once deployed, copy the assigned frontend URL (e.g., `https://roast-frontend.onrender.com`) and update this variable in the Backend Service settings.

4.  **Deploy**
    - Click **Apply** or **Create Blueprint**.
    - Render will deploy the backend and frontend in parallel (or sequentially if dependencies dictate).
    - The `VITE_API_URL` for the frontend will be automatically populated with the backend's URL.

## Post-Deployment Check

1.  **Update CORS (Safe Practice)**
    - If you used `*` for `CORS_ORIGINS` during setup, go to the **roast-backend** service settings -> Environment.
    - Update `CORS_ORIGINS` to match your actual frontend URL (e.g., `https://roast-frontend-xyz.onrender.com`).

2.  **Verify**
    - Open your Frontend URL.
    - Upload an image to test the application.
