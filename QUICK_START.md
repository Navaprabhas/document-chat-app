# 🚀 Quick Start Guide

Get your Document Chat Application running in 5 minutes!

## Step 1: Install Dependencies (2 minutes)

```bash
# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Configure API Keys (1 minute)

```bash
# Copy environment template
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-key-here
```

**Don't have an OpenAI key?** Use Ollama (free, local):
1. Install Ollama: https://ollama.ai
2. Run: `ollama pull llama2` and `ollama pull nomic-embed-text`
3. In `.env`, set: `LLM_PROVIDER=ollama` and `EMBEDDING_MODEL=ollama`

## Step 3: Run Setup (30 seconds)

```bash
python setup.py
```

This creates necessary directories and validates your configuration.

## Step 4: Launch Application (30 seconds)

```bash
streamlit run app.py
```

Your browser will open to `http://localhost:8501`

## Step 5: Upload and Chat (1 minute)

1. Click **"Browse files"** in the sidebar
2. Select a PDF document
3. Click **"Process Documents"**
4. Wait for processing (shows progress bar)
5. Type a question in the chat input
6. Press Enter and get your answer with citations!

## 🎯 Example Workflow

```
1. Upload: "company_report.pdf"
2. Ask: "What were the key findings?"
3. View: AI response with page citations
4. Ask: "Can you elaborate on the financial results?"
5. Export: Download chat history
```

## ⚡ Quick Tips

- **Multiple Documents**: Upload several PDFs at once for cross-document search
- **Better Answers**: Adjust "Number of Results" slider (5-7 works well)
- **Faster Processing**: Use smaller chunk sizes (800-1000)
- **More Context**: Increase chunk overlap (200-300)

## 🐛 Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key error"
- Check `.env` file exists in project root
- Verify `OPENAI_API_KEY` is set correctly
- No spaces around the `=` sign

### "ChromaDB error"
```bash
# Delete and recreate
rm -rf chroma_db
python setup.py
```

### "PDF won't process"
- Ensure PDF is not password-protected
- Try a different PDF
- Check file isn't corrupted

## 🎨 Customization

Want to customize? Edit these files:

- **UI/Layout**: `app.py` (Streamlit components)
- **Chunk Settings**: `config.py` (CHUNK_SIZE, CHUNK_OVERLAP)
- **Prompt Template**: `chat_engine.py` (system message)
- **Styling**: `app.py` (CSS in markdown section)

## 📚 Next Steps

Once running, try these features:

1. **Multi-document search**: Upload 3-5 related PDFs
2. **Citation tracking**: Click "View Sources" on responses
3. **Export history**: Save conversations as JSON
4. **Adjust settings**: Fine-tune chunk size and retrieval count
5. **Compare documents**: Ask questions that span multiple files

## 🚀 Production Deployment

Ready to deploy? See `README.md` for:
- Streamlit Cloud deployment
- Docker containerization
- Security best practices
- Performance optimization

## 💡 Pro Tips

1. **Start Simple**: Test with 1-2 small PDFs first
2. **Iterate Settings**: Adjust chunk size based on document type
3. **Use GPT-4**: For best quality (GPT-3.5 for speed)
4. **Monitor Costs**: Track OpenAI API usage in dashboard
5. **Save Configs**: Document your optimal settings per use case

## 🎓 Learning Resources

- **RAG Concepts**: https://python.langchain.com/docs/use_cases/question_answering/
- **Embeddings**: https://platform.openai.com/docs/guides/embeddings
- **ChromaDB**: https://docs.trychroma.com/
- **Streamlit**: https://docs.streamlit.io/

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] `.env` configured with API key
- [ ] Setup script runs without errors
- [ ] Application launches in browser
- [ ] Can upload and process a PDF
- [ ] Can ask questions and get responses
- [ ] Citations show correct page numbers
- [ ] Can export chat history

**All checked?** You're ready to go! 🎉

---

Need help? Check `README.md` for detailed documentation.
