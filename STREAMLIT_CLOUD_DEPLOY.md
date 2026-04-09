# Deploy to Streamlit Cloud - Step-by-Step Guide

Streamlit Cloud is the **easiest way** to deploy your Customer Support Agent. It's free, reliable, and takes just 10 minutes.

---

## Prerequisites

- GitHub account (free at https://github.com)
- Your project pushed to GitHub
- OpenAI API key (from SETUP_API_KEYS.md)

---

## Step 1: Push Your Project to GitHub

### 1.1 Create a GitHub Repository

1. Go to https://github.com/new
2. **Repository name:** `customer-support-agent` (or your choice)
3. **Description:** "AI-powered customer support with RAG pipeline"
4. **Public** (required for free Streamlit Cloud)
5. Click "Create repository"

### 1.2 Push Your Code to GitHub

Open PowerShell in your project folder and run:

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Customer Support Agent"

# Add remote (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/customer-support-agent.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example:**
```powershell
git remote add origin https://github.com/dudip/customer-support-agent.git
git push -u origin main
```

✅ Your code is now on GitHub!

---

## Step 2: Prepare for Streamlit Cloud

### 2.1 Update .gitignore

Add this to prevent uploading sensitive files:

```bash
# File: .gitignore
.env
.venv/
__pycache__/
*.pyc
.DS_Store
*.egg-info/
.streamlit/secrets.toml
```

### 2.2 Verify requirements.txt

Make sure your `requirements.txt` has all dependencies:

```bash
# Regenerate requirements.txt
pip freeze > requirements.txt
```

Expected contents:
```
langchain>=0.2.0
openai>=1.0.0
faiss-cpu==1.13.1
streamlit>=1.35.0
python-dotenv>=1.0.0
pydantic>=2.0.0
pypdf>=3.0.0
tiktoken>=0.5.0
```

Push this to GitHub:
```powershell
git add requirements.txt
git commit -m "Update requirements.txt"
git push
```

---

## Step 3: Deploy to Streamlit Cloud

### 3.1 Sign Up for Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "Sign in with GitHub" 
3. Authorize Streamlit (no charges, they just read your repos)
4. Wait for email confirmation

### 3.2 Create New App

1. Click "New app" (top right)
2. Fill in the form:

| Field | Value |
|-------|-------|
| **Repository** | your-username/customer-support-agent |
| **Branch** | main |
| **File path** | app.py |

3. Click "Deploy!"

✅ Your app is now deploying! (takes 2-3 minutes)

### 3.3 Get Your App URL

Your app is live at:
```
https://[something]-customer-support-agent.streamlit.app
```

Example: `https://dudip-customer-support-agent.streamlit.app`

---

## Step 4: Add API Keys (Secrets)

### 4.1 Access Secrets Settings

1. Go to your deployed app URL
2. Click **hamburger menu** (☰) top right
3. Select **"Settings"**
4. Click **"Secrets"** tab

### 4.2 Add Your Secrets

In the secrets editor, paste:

```toml
OPENAI_API_KEY = "sk-proj-YOUR-KEY-HERE"
USE_AZURE = false
DEMO_MODE = false
```

**Replace** `sk-proj-YOUR-KEY-HERE` with your actual OpenAI key from [SETUP_API_KEYS.md](SETUP_API_KEYS.md)

**To find your OpenAI key:**
1. Go to https://platform.openai.com/account/api-keys
2. Copy your key
3. Paste into secrets above

### 4.3 Save Secrets

Click "Save" and the app will restart automatically ✅

---

## Step 5: Test Your Deployed App

### 5.1 Wait for Restart

After saving secrets, wait 30 seconds for the app to reload.

### 5.2 First Test

In the chat interface:
1. Type: **"What is your refund policy?"**
2. Should see an answer with sources

### 5.3 Upload Documents

1. Expand **"📚 Upload Documents"** in sidebar
2. Click file upload
3. Select `data/documents/faq.md`
4. Wait for processing

### 5.4 Test with New Docs

Ask a question from the uploaded file to verify it's working.

---

## Troubleshooting

### Issue: "Import Error" or "Module Not Found"

**Cause:** Missing dependency in requirements.txt

**Fix:**
1. Locally run: `pip freeze > requirements.txt`
2. Commit and push:
   ```powershell
   git add requirements.txt
   git commit -m "Fix requirements"
   git push
   ```
3. Restart app (Settings → Reboot)

### Issue: "API Error" or "Invalid API Key"

**Cause:** Wrong OpenAI key or DEMO_MODE still True

**Fix:**
1. Go to Settings → Secrets
2. Verify `OPENAI_API_KEY` is correct
3. Verify `DEMO_MODE = false`
4. Save and wait 30 seconds

### Issue: App loads but shows "No documents"

**Cause:** Knowledge base not uploaded

**Fix:**
1. Click "Upload Documents" in sidebar
2. Upload files from `data/documents/` folder
3. Wait for indexing (1-2 minutes)

### Issue: "Rate limit exceeded" errors

**Cause:** Too many API calls or OpenAI quota reached

**Fix:**
1. Add payment method to OpenAI account
2. Check usage at https://platform.openai.com/usage
3. Set higher token limits if needed

### Issue: App appears to hang or is very slow

**Cause:** Streamlit Cloud free tier limited resources

**Fix:**
- Keep knowledge base < 500MB
- Use GPT-3.5-turbo instead of GPT-4 (faster, cheaper)
- Reduce chunk size in `src/document_loader.py`

---

## Sharing Your App

### 📤 Share URL
Your app is public at: `https://your-username-customer-support-agent.streamlit.app`

### 📊 Get Analytics
1. Go to https://share.streamlit.io/
2. Click your app
3. View "Analytics" tab to see usage stats

### 🔗 Embed in Website
Add this to any website to embed your chat:
```html
<iframe src="https://your-username-customer-support-agent.streamlit.app" 
        width="100%" 
        height="600">
</iframe>
```

---

## Managing Your Deployment

### Update Code on GitHub

When you make changes locally:

```powershell
# Make changes to files
# Then commit and push:

git add .
git commit -m "Update: describe your changes"
git push
```

Streamlit Cloud will **automatically deploy** within 2 minutes! ✅

### Restart App

If needed, restart from Settings → "Reboot app"

### View Logs

1. Go to https://share.streamlit.io/
2. Click your app
3. View "Logs" to debug issues

### Delete App

1. Go to https://share.streamlit.io/
2. Click app → Settings
3. Scroll to "Delete app"

---

## Pricing & Limits

### Free Tier (Perfect for You)
- ✅ 1 app
- ✅ Up to 500 hours/month
- ✅ 1GB memory
- ✅ Public access
- ✅ Free SSL certificate
- ❌ No private deployments
- ❌ Limited to 3 GB app size total

### Pro Tier ($9/month per seat)
- ✅ Unlimited apps
- ✅ Custom domain support
- ✅ Priority support
- ✅ 3GB memory per app
- ✅ Better performance

### When to Upgrade
- If you need > 1 app
- If you need custom domain (your-company.com)
- If you want private apps
- If app is slow (need more memory)

---

## Performance Tips

### 1. Cache Everything
```python
# Already in app.py, but keep it!
@st.cache_resource
def get_agent():
    return SupportAgent()
```

### 2. Use GPT-3.5 Instead of GPT-4
In your code:
```python
# Faster & cheaper (but less capable)
"gpt-3.5-turbo"  # Instead of "gpt-4"
```

### 3. Optimize Knowledge Base
- Keep only relevant documents
- Remove duplicates
- Archive old content

### 4. Enable Streaming
```python
# Stream responses for better UX
response_container.write(response)
# instead of showing all at once
```

---

## Next Steps After Deployment

1. ✅ **Share the URL** with team/customers
2. ✅ **Add more documents** via sidebar upload
3. ✅ **Monitor usage** in Analytics
4. ✅ **Collect feedback** from users
5. ✅ **Iterate** based on performance

---

## Security Best Practices

### ✅ DO:
- Keep DEMO_MODE = false (uses real API)
- Store API keys in Secrets (never in code)
- Use HTTPS only (Streamlit Cloud does this automatically)
- Regularly rotate API keys

### ❌ DON'T:
- Commit .env file to GitHub
- Share your API key
- Set DEMO_MODE = true in production
- Use free OpenAI tier (has strict limits)

---

## Support & Resources

### Streamlit Cloud Documentation
- https://docs.streamlit.io/streamlit-cloud/get-started

### Streamlit Community
- https://discuss.streamlit.io/

### Common Issues
- Check "Logs" tab in your Streamlit Cloud app dashboard
- Look for error messages in deployment logs

### Still Having Issues?

1. Check [Troubleshooting](#troubleshooting) section above
2. Review [README_COMPLETE.md](README_COMPLETE.md)
3. Check [SETUP_API_KEYS.md](SETUP_API_KEYS.md) for API setup

---

## Your Deployment Checklist

- [ ] GitHub account created
- [ ] Project pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed to Streamlit Cloud
- [ ] API key added to Secrets
- [ ] Tested with sample question
- [ ] Documents uploaded
- [ ] URL shared with team/customers
- [ ] Monitoring enabled for usage tracking

**Congratulations! 🎉 Your Customer Support Agent is live!**

Visit your app at: `https://your-username-customer-support-agent.streamlit.app`

---

## Example Workflow

```
Day 1:
  Morning: Push code to GitHub
  Afternoon: Deploy to Streamlit Cloud
  Evening: Share with team

Day 2:
  Team uploads support docs
  Agent starts answering queries
  Track usage in Analytics

Day 3+:
  Collect feedback
  Iterate on knowledge base
  Optimize prompts based on queries
  Scale to more users
```

---

**Everything is now live and ready to go! 🚀**
