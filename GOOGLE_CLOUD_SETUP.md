# Google Cloud Vision API Setup Guide

## What You Need

Your application uses **Google Cloud Vision API** for OCR (Optical Character Recognition) to:
- Extract text from Aadhar card images
- Extract text from PAN card images
- Validate document authenticity after resizing
- Reduce file size while maintaining text readability

## Step-by-Step Setup

### Step 1: Create Google Cloud Project

1. Go to: https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Enter project name: `document-verification-api` (or any name)
4. Click "Create"
5. Wait for project creation (takes ~30 seconds)

### Step 2: Enable Cloud Vision API

1. In the Google Cloud Console, go to: https://console.cloud.google.com/apis/library
2. Search for "Cloud Vision API"
3. Click on "Cloud Vision API"
4. Click "Enable"
5. Wait for API to be enabled

### Step 3: Create Service Account

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click "Create Service Account"
3. Enter details:
   - **Service account name**: `vercel-document-api`
   - **Service account ID**: (auto-generated)
   - **Description**: "Service account for Vercel deployment"
4. Click "Create and Continue"
5. **Grant permissions**:
   - Select role: "Cloud Vision AI Service Agent" or "Owner"
   - Click "Continue"
6. Click "Done"

### Step 4: Create and Download JSON Key

1. In the Service Accounts list, find your newly created account
2. Click on the service account email
3. Go to "Keys" tab
4. Click "Add Key" → "Create new key"
5. Select "JSON" format
6. Click "Create"
7. **A JSON file will download automatically** - SAVE THIS FILE!

The JSON file looks like this:
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  ...
}
```

### Step 5: Add Credentials to Vercel

#### Option A: Using Vercel Dashboard (Recommended)

1. Go to your Vercel project dashboard
2. Click on your project
3. Go to **Settings** → **Environment Variables**
4. Click "Add New"
5. Enter:
   - **Name**: `GOOGLE_APPLICATION_CREDENTIALS`
   - **Value**: Paste the ENTIRE contents of the JSON file you downloaded
   - **Environments**: Check all (Production, Preview, Development)
6. Click "Save"

#### Option B: Using Vercel CLI

```bash
# Navigate to your project directory
cd /Users/kishoreprashanth/Developer/API/API-Document-Resize-Validation-Verification-main

# Add the environment variable (replace path with your JSON file location)
vercel env add GOOGLE_APPLICATION_CREDENTIALS production < /path/to/your-credentials.json
```

### Step 6: Redeploy Your Application

After adding the environment variable:
1. In Vercel dashboard, go to "Deployments"
2. Click "Redeploy" on the latest deployment
   OR
3. Push a new commit to trigger automatic deployment

## Verification

After deployment, test your application:

1. **Test Health Endpoint**:
   ```
   https://your-app.vercel.app/health
   ```
   Should return: `{"status": "healthy"}`

2. **Test Number Validation** (doesn't need Google Cloud):
   - Go to: `https://your-app.vercel.app/aadhar`
   - Enter Aadhar number: `234567891234`
   - Click Submit
   - Should validate the format

3. **Test Image Upload** (needs Google Cloud):
   - Upload an Aadhar or PAN card image
   - The OCR should extract the number

## Troubleshooting

### Error: "Could not load credentials"
**Solution**: Make sure you copied the ENTIRE JSON file content, including the curly braces `{}`

### Error: "API not enabled"
**Solution**: Go back to Step 2 and ensure Cloud Vision API is enabled

### Error: "Permission denied"
**Solution**: 
1. Go to IAM & Admin → Service Accounts
2. Click on your service account
3. Add role: "Cloud Vision AI Service Agent"

### Error: "Quota exceeded"
**Solution**: 
1. Go to: https://console.cloud.google.com/apis/api/vision.googleapis.com/quotas
2. Check your usage
3. Free tier: 1,000 requests/month
4. Enable billing for more quota

## Cost Information

**Free Tier (No credit card required)**:
- 1,000 Vision API requests per month
- Perfect for testing and small projects

**Paid Tier**:
- $1.50 per 1,000 requests (after free tier)
- Only charged if you exceed free tier

## Security Notes

⚠️ **IMPORTANT**:
- Never commit the JSON credentials file to Git
- The `.gitignore` file already excludes `credentials.json`
- Only store credentials in Vercel environment variables
- Rotate keys periodically for security

## What Happens Without Credentials?

If you don't set up Google Cloud credentials:
- ✅ Number validation will still work (format checking)
- ❌ Image upload and OCR will fail
- ❌ Resize validation will fail
- ❌ File size reduction will fail

## Summary Checklist

- [ ] Created Google Cloud Project
- [ ] Enabled Cloud Vision API
- [ ] Created Service Account
- [ ] Downloaded JSON credentials file
- [ ] Added credentials to Vercel environment variables
- [ ] Redeployed application
- [ ] Tested functionality

---

**Need Help?** 
- Google Cloud Console: https://console.cloud.google.com/
- Cloud Vision API Docs: https://cloud.google.com/vision/docs
- Vercel Environment Variables: https://vercel.com/docs/environment-variables
