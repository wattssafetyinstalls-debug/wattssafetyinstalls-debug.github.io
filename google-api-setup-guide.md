# Google API Setup Guide for ATP Bid Generator

## ✅ Google Drive API - Already Enabled!

Great! I can see you've successfully enabled the Google Drive API. Now let's get the credentials you need.

## 🔧 Next Steps: Get Your Credentials

### 1. Go to Google Cloud Console
- Navigate to: https://console.cloud.google.com/
- Make sure you're on the right project (or create a new one)

### 2. Enable Gmail API (if not already enabled)
- In the search bar, type "Gmail API"
- Click on it and click "Enable"
- This is needed for scanning emails

### 3. Create Credentials
- In the left menu, go to **"APIs & Services" → "Credentials"**
- Click **"+ Create Credentials" → "OAuth 2.0 Client ID"**
- Select **"Web application"**
- **Application name**: ATP Bid Generator
- **Authorized JavaScript origins**: `http://localhost:3000`
- **Authorized redirect URIs**: `http://localhost:3000`
- Click **"Create"**

### 4. Get Your Credentials
- You'll see a **Client ID** (looks like: `123456789-abc.apps.googleusercontent.com`)
- Click **"Download JSON"** to get your API key
- The JSON file contains both your Client ID and API Key

### 5. Update the Code
- Open: `c:\Users\User\my-website\tools\bidgen\google-integration.html`
- Replace these lines:
```javascript
const CLIENT_ID = 'YOUR_CLIENT_ID_HERE';
const API_KEY = 'YOUR_API_KEY_HERE';
```
- With your actual credentials:
```javascript
const CLIENT_ID = '123456789-abc.apps.googleusercontent.com';
const API_KEY = 'AIzaSyABC123XYZ456789';
```

## 🔍 Quick Setup Checklist

- [x] Google Drive API enabled ✅
- [ ] Gmail API enabled
- [ ] OAuth 2.0 Client ID created
- [ ] API Key obtained
- [ ] Code updated with credentials
- [ ] Test connection

## 🚀 Test Your Setup

1. Open the Google Integration page
2. Click "Connect Google Account"
3. Sign in with your Google account
4. Grant permissions for Drive and Gmail
5. Try scanning Drive for ATP files

## 📊 What You'll Get

Once set up, you can scan:
- **Google Drive**: PDF quotes, contracts, estimates
- **Gmail**: Bid-related emails and attachments
- **Automatic Detection**: ATP, Watts, bid, quote files
- **Import**: All data into your bid generator

## 🔒 Security Notes

- **Read-only access only** - no modifications
- **Local token storage** - secure
- **OAuth 2.0** - industry standard
- **No data sharing** - all processing local

## 🆘 Need Help?

If you run into any issues:
1. Check that both APIs are enabled
2. Verify the redirect URI is exactly `http://localhost:3000`
3. Make sure you're using the right Google account
4. Try refreshing the page and reconnecting

## 📞 Support

The Google Cloud Console has excellent documentation if you need help with any step!

---

**Ready to enhance your ATP bid generator with Google Drive and Gmail integration!** 🎯
