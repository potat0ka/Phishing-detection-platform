# Local Setup Guide - AI Phishing Detection Platform

## Quick Setup (3 Steps)

### 1. Install Dependencies
```bash
python install_minimal.py
```

### 2. Run Application with Auto-Setup
```bash
python run_local.py
```

### 3. Login with Test Account
- **Email**: test@example.com
- **Password**: password123
- **Username**: testuser

## What's Working Now

✅ **Authentication System**: Login required for `/check` and `/analyze-media` pages
✅ **MongoDB Fallback**: Works offline with local file authentication
✅ **Core Features**: All phishing detection features available after login
✅ **User-Friendly**: Automatic test user creation for development

## Pages Access Levels

### Public (No Login Required)
- Homepage (`/`)
- Safety Tips (`/tips`)

### Protected (Login Required)
- Phishing Detection (`/check`)
- Media Analysis (`/analyze-media`)
- User Dashboard
- Admin Features

## Development Features

- **Automatic Test User**: Creates default test account if MongoDB unavailable
- **File-based Fallback**: Authentication works even when database is offline
- **Session Management**: Proper Flask-Login integration
- **Role Support**: User/Admin/Superadmin roles ready

## How Authentication Works

1. **MongoDB First**: Tries to authenticate with MongoDB Atlas
2. **File Fallback**: Uses local JSON file if MongoDB fails
3. **Default User**: Creates test user automatically if no data found
4. **Session Persistence**: Remembers login across browser sessions

## Customization

To create additional test users, run:
```bash
python create_test_user.py
```

Or modify `data/test_users.json` directly.

## Production Notes

- Change default test credentials before deployment
- Enable MongoDB connection for production
- Update secret keys in environment variables
- Set DEBUG=False for production

The platform now properly protects the analysis features while providing a smooth development experience!