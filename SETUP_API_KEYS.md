# API Key Configuration Guide

## Get Your API Key

### Option 1: OpenAI API (Recommended for getting started)

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Update `.env` file:
   ```
   OPENAI_API_KEY=sk-your-copied-key-here
   ```

### Option 2: Azure OpenAI

1. Create an Azure account at https://azure.microsoft.com
2. Create an Azure OpenAI resource
3. Go to "Keys and Endpoint"
4. Copy the key and endpoint
5. Update `.env` file:
   ```
   AZURE_OPENAI_API_KEY=your-azure-key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   ```

## Quick Test

After updating `.env`, run:
```bash
streamlit run app.py
```

## Troubleshooting

**Error: "Connection error"**
- Check your API key is not the placeholder text
- Verify the API key is valid and active
- Make sure there are no extra spaces in the `.env` file

**Error: "API key is invalid"**
- Your API key might be deactivated
- Try generating a new key from the platform

**Error: "Rate limited"**
- You've made too many API calls
- Wait a few minutes and try again
- Consider upgrading your plan

## Get Free Credits

- **OpenAI**: New accounts get $5 in free credits
- **Azure**: $200 free credits for 30 days

## File Location

Your `.env` file is at:
```
c:\Users\dudip\Customer Support Agent — End-to-End Pipeline\.env
```

Edit it with any text editor (VS Code, Notepad, etc.)
