# Quick Deployment Reference

## 🚀 Deploy to Vercel (3 Steps)

### Step 1: Deploy
```bash
vercel --prod
```

Answer the prompts:
- Set up and deploy? → **Y**
- Which scope? → Select your account
- Link to existing project? → **N**
- Project name? → Press Enter (or provide custom name)
- Code directory? → **./** (Press Enter)

### Step 2: Add Google Cloud Credentials

**Option A: Via Vercel Dashboard** (Recommended)
1. Go to https://vercel.com/dashboard
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Click **Add New**
5. Name: `GOOGLE_APPLICATION_CREDENTIALS`
6. Value: Paste your entire credentials.json content
7. Select: Production, Preview, Development
8. Click **Save**

**Option B: Via CLI**
```bash
# If you have credentials.json locally
cat credentials.json | vercel env add GOOGLE_APPLICATION_CREDENTIALS production
```

### Step 3: Redeploy
```bash
vercel --prod
```

## ✅ Verify Deployment

### Quick Test (Replace YOUR_URL)
```bash
# Test health check
curl https://YOUR_URL.vercel.app/health

# Test home page
curl https://YOUR_URL.vercel.app/

# Run automated tests
python test_api.py https://YOUR_URL.vercel.app
```

### Browser Test
1. Open: `https://YOUR_URL.vercel.app/`
2. Click "Aadhar Card Verification"
3. Try uploading an image or entering a number
4. Check browser console for errors (F12)

## 📝 Important Notes

### Google Cloud Setup (If not done)
1. Go to https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable **Cloud Vision API**
4. Create **Service Account**
5. Download **JSON key file**
6. Use this JSON in Vercel environment variables

### File Locations
- Main app: `app.py`
- Config: `vercel.json`
- Dependencies: `requirements.txt`
- Backend: `BackEnd/` directory
- Frontend: `Frontend/` directory

### Supported Operations
✅ Aadhar card verification (image + number)
✅ PAN card verification (image + number)
✅ Image resizing (maintain aspect ratio)
✅ Image resizing (hard resize)
✅ File size reduction

### File Requirements
- Max size: 16MB
- Formats: PNG, JPG, JPEG
- Clear, readable text for OCR

## 🐛 Troubleshooting

### Deployment fails
```bash
# Check Vercel logs
vercel logs

# Verify files
git status
git log -1
```

### API not working
1. Check Vercel function logs in dashboard
2. Verify environment variables are set
3. Test health endpoint: `/health`

### OCR not working
1. Verify Google Cloud credentials are set
2. Check Vision API is enabled in GCP
3. Verify service account has permissions
4. Check GCP quotas and billing

### Static files 404
1. Check `Frontend/static/` directory exists
2. Verify `vercel.json` routing
3. Clear browser cache

## 📊 Test Endpoints

### GET Endpoints
```bash
# Home page
https://YOUR_URL.vercel.app/

# Aadhar page
https://YOUR_URL.vercel.app/aadhar

# PAN page
https://YOUR_URL.vercel.app/pan

# Health check
https://YOUR_URL.vercel.app/health
```

### POST Endpoints (Use Postman/curl)
```bash
# Aadhar verification (number)
curl -X POST https://YOUR_URL.vercel.app/aadharVerification \
  -F "number=234567891234"

# PAN verification (number)
curl -X POST https://YOUR_URL.vercel.app/panVerification \
  -F "number=ABCDE1234F"

# Image upload example
curl -X POST https://YOUR_URL.vercel.app/aadharVerification \
  -F "file=@/path/to/aadhar.jpg"
```

## 🎯 Success Criteria

✅ Deployment completes without errors
✅ `/health` returns `{"status": "healthy"}`
✅ Home page loads with document options
✅ Aadhar and PAN pages load
✅ Static files (CSS, JS) load correctly
✅ Number validation works
✅ Image upload works (with GCP credentials)

## 📞 Need Help?

1. **Deployment Guide**: See `DEPLOYMENT_GUIDE.md`
2. **File Review**: See `FILE_REVIEW_CHECKLIST.md`
3. **Vercel Docs**: https://vercel.com/docs
4. **Google Cloud Vision**: https://cloud.google.com/vision/docs

## 🔄 Update Deployment

```bash
# Make changes to code
git add .
git commit -m "Your changes"

# Redeploy
vercel --prod
```

---

**Ready to deploy?** Run `vercel --prod` in your terminal! 🚀
