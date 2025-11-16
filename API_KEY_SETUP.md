# API Key Setup Guide

There are two ways to set up your Anthropic API key for Novel Writer:

## Option 1: Using the GUI (Recommended)

1. Launch Novel Writer (double-click the launcher)
2. The API Key Setup dialog will appear automatically on first launch
3. Click "Get API Key from Anthropic" to open your browser
4. Copy your API key from https://console.anthropic.com/settings/keys
5. Paste it into the dialog and click "Save and Continue"

**Done!** Your key is saved securely.

---

## Option 2: Manual Setup (Advanced)

If you prefer to set up the API key manually or if the GUI method isn't working:

### Step 1: Create the config directory

**On Mac/Linux:**
```bash
mkdir -p ~/.novel_writer
```

**On Windows:**
```cmd
mkdir %USERPROFILE%\.novel_writer
```

### Step 2: Create the .env file

**On Mac/Linux:**
```bash
nano ~/.novel_writer/.env
```

**On Windows:**
```cmd
notepad %USERPROFILE%\.novel_writer\.env
```

### Step 3: Add your API key

Paste this line into the file, replacing `YOUR_API_KEY_HERE` with your actual key:

```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Your API key should:**
- Start with `sk-ant-`
- Be around 100+ characters long
- Have no spaces or quotes around it

### Step 4: Save and restart

1. Save the file
2. Close and restart Novel Writer
3. The app should now detect your API key

---

## Troubleshooting

### "No API Key" warning still appears

1. Check that the .env file is in the correct location:
   - Mac/Linux: `~/.novel_writer/.env`
   - Windows: `C:\Users\YourName\.novel_writer\.env`

2. Check the file contents:
   ```bash
   # Mac/Linux:
   cat ~/.novel_writer/.env

   # Windows:
   type %USERPROFILE%\.novel_writer\.env
   ```

3. Make sure your API key:
   - Starts with `sk-ant-`
   - Has no extra spaces or quotes
   - Is all on one line

4. Check the terminal/console output when launching for debug messages

### Get a new API key

Visit: https://console.anthropic.com/settings/keys

---

## Security Notes

- Your API key is stored in `~/.novel_writer/.env` with restricted permissions
- Never share your API key publicly
- Never commit the .env file to version control
- If your key is compromised, delete it from Anthropic's console and generate a new one

---

## Need Help?

If you're still having trouble:
1. Check the terminal/console output for error messages
2. Try using the GUI method (Option 1) instead
3. Verify your API key works by testing it at https://console.anthropic.com/
4. Create a new API key if the current one isn't working
