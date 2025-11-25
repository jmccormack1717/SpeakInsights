# CORS Fix Instructions

## Problem
The frontend at `https://speakinsights-prototype.onrender.com` cannot communicate with the backend at `https://speakinsights-backend.onrender.com` due to CORS policy blocking.

## Solution Applied

1. **Updated CORS defaults** in `backend/app/config.py` to include the production frontend URL
2. **Added CORS logging** on startup to verify configuration
3. **Updated env.example** with the correct CORS origins

## Required Action on Render

### Backend Environment Variables

Make sure your Render backend service has the `CORS_ORIGINS` environment variable set:

```
CORS_ORIGINS=https://speakinsights-prototype.onrender.com,http://localhost:5173,http://localhost:3000
```

**OR** if you want to allow all origins (less secure, but easier for development):

```
CORS_ORIGINS=*
```

### Steps to Update on Render:

1. Go to your Render dashboard
2. Select your backend service (`speakinsights-backend`)
3. Go to "Environment" tab
4. Add or update the `CORS_ORIGINS` variable:
   - Key: `CORS_ORIGINS`
   - Value: `https://speakinsights-prototype.onrender.com,http://localhost:5173,http://localhost:3000`
5. Save and redeploy

## Additional Fixes

- Better error handling in query endpoint
- Automatic dataset import on startup if CSV is available
- Improved logging for debugging

## Testing

After redeploying:
1. Check backend logs for: `CORS allowed origins: [...]`
2. Try a query from the frontend
3. Check browser console - CORS errors should be gone
4. If 500 error persists, check backend logs for the actual error

