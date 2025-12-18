# Deployment Guide for Document Verification API

## Prerequisites
- Vercel CLI installed ✓
- Git repository initialized ✓
- Google Cloud Vision API credentials

## Deployment Steps

### 1. Deploy to Vercel
```bash
# In the project directory, run:
vercel --prod

# Follow the prompts:
# - Set up and deploy? → Yes (Y)
# - Which scope? → Select your account
# - Link to existing project? → No (N)
# - What's your project's name? → (Press enter or provide a name)
# - In which directory is your code located? → ./ (Press enter)
```

### 2. Set Up Google Cloud Vision API Credentials

**IMPORTANT:** You need to configure Google Cloud credentials as an environment variable in Vercel.

#### Option A: Using Vercel Dashboard (Recommended)
1. Go to your project on Vercel Dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add a new environment variable:
   - **Name:** `GOOGLE_APPLICATION_CREDENTIALS`
   - **Value:** The full path to your credentials JSON file OR the JSON content itself
   - **Environments:** Production, Preview, Development

#### Option B: Using Vercel CLI
```bash
# If you have a credentials.json file locally:
vercel env add GOOGLE_APPLICATION_CREDENTIALS production < credentials.json
```

### 3. Redeploy After Adding Credentials
```bash
vercel --prod
```

## Project Structure
```
.
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel configuration
├── BackEnd/                 # Backend modules
│   ├── aadharVerification.py
│   ├── panVerification.py
│   ├── aadharResize.py
│   ├── panResize.py
│   └── reduceSize.py
└── Frontend/                # Frontend templates and static files
    ├── Templates/
    │   ├── index.html
    │   ├── aadhar.html
    │   └── pan.html
    └── static/
        ├── css/
        ├── js/
        └── images/
```

## API Endpoints

### Frontend Pages
- `GET /` - Home page with document selection
- `GET /aadhar` - Aadhar card verification page
- `GET /pan` - PAN card verification page

### API Endpoints
- `POST /aadharVerification` - Verify Aadhar card (image or number)
- `POST /panVerification` - Verify PAN card (image or number)
- `POST /aadharResizeMAR` - Resize Aadhar maintaining aspect ratio
- `POST /aadharResizeHard` - Hard resize Aadhar card
- `POST /panResizeMAR` - Resize PAN maintaining aspect ratio
- `POST /panResizeHard` - Hard resize PAN card
- `POST /reduceSize` - Reduce image file size
- `GET /health` - Health check endpoint

## Testing Checklist

### 1. Basic Functionality
- [ ] Home page loads correctly
- [ ] Navigation to Aadhar page works
- [ ] Navigation to PAN page works
- [ ] Static files (CSS, JS, images) load properly

### 2. Aadhar Card Verification
- [ ] Upload Aadhar card image
- [ ] Verify Aadhar number extraction
- [ ] Validate Aadhar number format (12 digits)
- [ ] Test with invalid image
- [ ] Test manual number entry

### 3. PAN Card Verification
- [ ] Upload PAN card image
- [ ] Verify PAN number extraction
- [ ] Validate PAN format (AAAAA9999A)
- [ ] Test with invalid image
- [ ] Test manual number entry

### 4. Image Resizing
- [ ] Aadhar resize with aspect ratio
- [ ] Aadhar hard resize
- [ ] PAN resize with aspect ratio
- [ ] PAN hard resize
- [ ] Verify resized image quality

### 5. File Size Reduction
- [ ] Upload image for size reduction
- [ ] Verify reduced file is smaller
- [ ] Check image quality is maintained

## Known Limitations

1. **Google Cloud Vision API Required**: The OCR functionality requires valid Google Cloud Vision API credentials
2. **File Size Limits**: Maximum upload size is 16MB
3. **Supported Formats**: Only PNG, JPG, JPEG images are supported
4. **Serverless Constraints**: Uses /tmp directory for temporary files (automatically cleaned)

## Troubleshooting

### Issue: "Module not found" errors
**Solution:** Ensure all dependencies in requirements.txt are installed. Redeploy with `vercel --prod`

### Issue: Google Cloud Vision API errors
**Solution:** 
1. Verify credentials are set in Vercel environment variables
2. Ensure the Google Cloud Vision API is enabled in your GCP project
3. Check that the service account has proper permissions

### Issue: Image upload fails
**Solution:**
1. Check file size (must be < 16MB)
2. Verify file format (PNG, JPG, JPEG only)
3. Check browser console for errors

### Issue: Static files not loading
**Solution:**
1. Verify Frontend/static directory structure
2. Check browser network tab for 404 errors
3. Ensure vercel.json routing is correct

## Post-Deployment Verification

After deployment, test the following URL patterns:
- `https://your-app.vercel.app/` - Home page
- `https://your-app.vercel.app/health` - Health check
- `https://your-app.vercel.app/aadhar` - Aadhar page
- `https://your-app.vercel.app/pan` - PAN page

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| GOOGLE_APPLICATION_CREDENTIALS | Path or content of GCP credentials JSON | Yes |

## Support

For issues related to:
- **Vercel deployment**: Check Vercel logs in dashboard
- **Google Cloud Vision**: Check GCP console and API quotas
- **Application errors**: Check Vercel function logs

## Next Steps After Deployment

1. ✅ Verify deployment URL is accessible
2. ✅ Test all frontend pages load
3. ✅ Configure Google Cloud credentials
4. ✅ Test document verification with sample images
5. ✅ Test resize functionality
6. ✅ Monitor Vercel function logs for errors
7. ✅ Set up custom domain (optional)
