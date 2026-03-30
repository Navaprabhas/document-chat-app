# 🚀 Get Started in 3 Minutes

The fastest way to get your Document Chat Application running!

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key (or Ollama installed for free local option)
- 500MB free disk space

## ⚡ Quick Install

### Windows

1. **Double-click** `install.bat`
2. Wait for installation to complete
3. Edit `.env` file and add your OpenAI API key
4. **Double-click** `run.bat`
5. Browser opens automatically at http://localhost:8501

### macOS/Linux

```bash
# Make scripts executable
chmod +x install.sh run.sh

# Run installation
./install.sh

# Edit .env and add your API key
nano .env

# Run application
./run.sh
```

## 🔑 Get Your API Key

### Option 1: OpenAI (Recommended)
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Paste in `.env` file: `OPENAI_API_KEY=sk-your-key-here`

### Option 2: Ollama (Free, Local)
1. Install Ollama: https://ollama.ai
2. Run: `ollama pull llama2`
3. Run: `ollama pull nomic-embed-text`
4. In `.env`, set:
   ```
   LLM_PROVIDER=ollama
   EMBEDDING_MODEL=ollama
   ```

## 📚 First Steps

### 1. Upload a Document
- Click **"Browse files"** in sidebar
- Select a PDF (try a small one first, 5-10 pages)
- Click **"Process Documents"**
- Wait ~10 seconds

### 2. Ask a Question
- Type in chat: "What is this document about?"
- Press Enter
- Get answer with citations!

### 3. Explore Features
- Click **"View Sources"** to see where answers came from
- Upload more documents for cross-document search
- Adjust settings in sidebar
- Export chat history

## 🎯 Example Questions to Try

```
"Summarize the main points of this document"
"What does page 5 say about [topic]?"
"Compare the approaches in these documents"
"List all the key recommendations"
"What are the conclusions?"
```

## ⚙️ Quick Settings Guide

### For Better Accuracy
- Increase "Number of Results" to 7-10
- Use larger "Chunk Size" (1500-2000)
- More "Chunk Overlap" (300-400)

### For Faster Responses
- Decrease "Number of Results" to 3-5
- Use smaller "Chunk Size" (800-1000)
- Less "Chunk Overlap" (100-200)

## 🐛 Quick Fixes

### "Module not found" error
```bash
# Windows
venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

### "API key not found" error
1. Check `.env` file exists in project folder
2. Open `.env` and verify `OPENAI_API_KEY=sk-...`
3. No spaces around the `=` sign
4. Restart the application

### "Can't process PDF" error
- Ensure PDF is not password-protected
- Try a different PDF
- Check PDF is not corrupted

### Application won't start
```bash
# Run diagnostics
python test_setup.py

# Check what's wrong and follow suggestions
```

## 📖 Learn More

- **Full Documentation**: See `README.md`
- **Deployment Guide**: See `DEPLOYMENT.md`
- **Project Overview**: See `PROJECT_SUMMARY.md`
- **Quick Reference**: See `QUICK_START.md`

## 💡 Pro Tips

1. **Start Small**: Test with 1-2 small PDFs first
2. **Good Questions**: Be specific in your questions
3. **Check Sources**: Always verify citations
4. **Experiment**: Try different settings for your use case
5. **Save Chats**: Export important conversations

## 🎓 Video Tutorial (Conceptual)

1. **Install** (1 min): Run install script, add API key
2. **Upload** (30 sec): Browse and select PDF
3. **Process** (30 sec): Click process, wait for completion
4. **Chat** (1 min): Ask questions, view responses
5. **Explore** (30 sec): Try settings, export history

## 🔥 Common Use Cases

### Research Papers
```
"What methodology did the authors use?"
"Summarize the key findings"
"What are the limitations mentioned?"
```

### Business Reports
```
"What were the Q4 results?"
"List all recommendations"
"Compare this year vs last year"
```

### Legal Documents
```
"What are the key terms in section 5?"
"Summarize the obligations"
"What are the termination clauses?"
```

### Technical Manuals
```
"How do I configure [feature]?"
"What are the system requirements?"
"Explain the troubleshooting steps"
```

## 🎉 You're Ready!

That's it! You now have a powerful AI-powered document chat system.

**Next Steps:**
1. Upload your first document
2. Ask a question
3. Explore the features
4. Share with your team

**Need Help?**
- Run `python test_setup.py` for diagnostics
- Check `README.md` for detailed docs
- Review error messages carefully

---

**Happy Chatting! 🚀**
