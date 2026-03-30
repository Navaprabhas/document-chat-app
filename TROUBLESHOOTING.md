# 🔧 Troubleshooting Guide

Complete guide to fixing common issues with the Document Chat Application.

## 🚨 Installation Issues

### Python Not Found

**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
1. Install Python 3.10+ from https://python.org
2. During installation, check "Add Python to PATH"
3. Restart terminal/command prompt
4. Verify: `python --version`

### pip Install Fails

**Error**: `ERROR: Could not install packages due to an OSError`

**Solutions**:
```bash
# Try with --user flag
pip install --user -r requirements.txt

# Or upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt

# On Windows, run as administrator
# On macOS/Linux, try:
sudo pip install -r requirements.txt
```

### Virtual Environment Issues

**Error**: `venv\Scripts\activate.bat is not recognized`

**Solution**:
```bash
# Delete and recreate venv
rm -rf venv  # or rmdir /s venv on Windows
python -m venv venv

# Activate again
# Windows:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate
```

## 🔑 API Key Issues

### OpenAI API Key Not Found

**Error**: `openai.error.AuthenticationError: No API key provided`

**Solutions**:

1. **Check .env file exists**:
```bash
# Should be in project root
ls .env  # or dir .env on Windows
```

2. **Verify .env format**:
```env
# Correct format (no spaces around =)
OPENAI_API_KEY=sk-your-key-here

# Wrong formats:
OPENAI_API_KEY = sk-your-key-here  # ❌ spaces
OPENAI_API_KEY="sk-your-key-here"  # ❌ quotes
```

3. **Check key is valid**:
- Go to https://platform.openai.com/api-keys
- Verify key is active
- Check billing is set up

4. **Restart application** after editing .env

### Invalid API Key

**Error**: `openai.error.AuthenticationError: Incorrect API key`

**Solutions**:
1. Copy key again from OpenAI dashboard
2. Ensure no extra spaces or characters
3. Key should start with `sk-`
4. Check key hasn't been revoked

## 📄 PDF Processing Issues

### Can't Read PDF

**Error**: `Error processing PDF: [various errors]`

**Solutions**:

1. **Password-protected PDF**:
   - Remove password protection first
   - Use Adobe Acrobat or online tools

2. **Corrupted PDF**:
   - Try opening in PDF reader
   - Re-download or get new copy
   - Convert to PDF again if possible

3. **Scanned PDF (images only)**:
   - Current version doesn't support OCR
   - Use OCR tool first (Adobe, online services)
   - Convert to searchable PDF

4. **Large PDF**:
   - Split into smaller files
   - Increase timeout in config
   - Process one at a time

### PDF Uploads But No Text

**Issue**: Processing completes but can't answer questions

**Solutions**:
1. PDF might be image-based (needs OCR)
2. Check if text is selectable in PDF reader
3. Try different PDF
4. Check logs for extraction errors

## 🗄️ ChromaDB Issues

### ChromaDB Connection Error

**Error**: `chromadb.errors.ChromaError`

**Solutions**:

1. **Delete and recreate database**:
```bash
# Stop application
# Delete database folder
rm -rf chroma_db  # or rmdir /s chroma_db on Windows
# Restart application
```

2. **Check disk space**:
```bash
# Ensure you have at least 500MB free
df -h  # macOS/Linux
# or check in File Explorer on Windows
```

3. **Permissions issue**:
```bash
# macOS/Linux
chmod -R 755 chroma_db

# Windows: Right-click folder > Properties > Security
```

### Vector Store Full

**Issue**: Slow performance or errors after many documents

**Solution**:
1. Click "Clear All Documents" in sidebar
2. Or delete `chroma_db/` folder
3. Restart application
4. Re-upload only needed documents

## 🤖 LLM Issues

### Slow Responses

**Issue**: Takes >30 seconds to get answers

**Solutions**:

1. **Reduce retrieval count**:
   - Set "Number of Results" to 3-5
   - Smaller chunks (800-1000)

2. **Use faster model**:
```env
# In .env
OPENAI_MODEL=gpt-3.5-turbo  # Faster than GPT-4
```

3. **Check internet connection**:
   - Test speed at speedtest.net
   - Try different network

4. **OpenAI API issues**:
   - Check status.openai.com
   - Wait and retry

### Poor Quality Answers

**Issue**: Answers are wrong or irrelevant

**Solutions**:

1. **Increase context**:
   - Set "Number of Results" to 7-10
   - Larger chunks (1500-2000)
   - More overlap (300-400)

2. **Better questions**:
   - Be more specific
   - Reference page numbers
   - Ask one thing at a time

3. **Use better model**:
```env
OPENAI_MODEL=gpt-4-turbo-preview
```

4. **Check document quality**:
   - Ensure text is extractable
   - Not image-based PDF
   - Good quality scan

### Rate Limit Errors

**Error**: `openai.error.RateLimitError`

**Solutions**:
1. Wait 60 seconds and retry
2. Upgrade OpenAI plan
3. Use Ollama (local, no limits)
4. Implement rate limiting in code

## 🖥️ Streamlit Issues

### Port Already in Use

**Error**: `OSError: [Errno 98] Address already in use`

**Solutions**:

1. **Kill existing process**:
```bash
# Find process on port 8501
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8501 | xargs kill -9
```

2. **Use different port**:
```bash
streamlit run app.py --server.port 8502
```

### Browser Doesn't Open

**Issue**: Application starts but browser doesn't open

**Solutions**:
1. Manually open: http://localhost:8501
2. Check firewall settings
3. Try different browser
4. Check if port is blocked

### UI Not Loading

**Issue**: Blank page or loading forever

**Solutions**:
1. Hard refresh: Ctrl+Shift+R (Cmd+Shift+R on Mac)
2. Clear browser cache
3. Try incognito/private mode
4. Check browser console for errors (F12)
5. Try different browser

## 💾 Memory Issues

### Out of Memory

**Error**: `MemoryError` or system freezes

**Solutions**:

1. **Process fewer documents**:
   - Upload 1-2 at a time
   - Clear old documents

2. **Reduce chunk size**:
   - Set to 800-1000
   - Less overlap (100-150)

3. **Close other applications**

4. **Increase system RAM** (if possible)

5. **Use smaller model**:
```env
OPENAI_MODEL=gpt-3.5-turbo
```

## 🔒 Permission Issues

### Can't Write Files

**Error**: `PermissionError: [Errno 13] Permission denied`

**Solutions**:

1. **Run as administrator** (Windows)
2. **Check folder permissions**:
```bash
# macOS/Linux
chmod -R 755 .
```

3. **Move to different location**:
   - Not in Program Files
   - Not in system directories
   - Use Documents or Desktop

## 🌐 Network Issues

### Can't Connect to OpenAI

**Error**: `Connection error` or `Timeout`

**Solutions**:

1. **Check internet connection**
2. **Check OpenAI status**: status.openai.com
3. **Try different network**
4. **Check firewall/proxy settings**
5. **Use VPN** if OpenAI is blocked

### Ollama Connection Failed

**Error**: `Connection refused` to localhost:11434

**Solutions**:

1. **Start Ollama**:
```bash
# Check if running
curl http://localhost:11434

# Start Ollama
ollama serve
```

2. **Check port**:
```env
# In .env
OLLAMA_BASE_URL=http://localhost:11434
```

3. **Pull models**:
```bash
ollama pull llama2
ollama pull nomic-embed-text
```

## 🐛 General Debugging

### Check Logs

```bash
# Look for error messages
cat logs/app.log  # macOS/Linux
type logs\app.log  # Windows
```

### Run Diagnostics

```bash
# Comprehensive system check
python test_setup.py

# Check specific component
python -c "from document_processor import DocumentProcessor; print('OK')"
```

### Enable Debug Mode

```python
# In config.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components

```python
# Test embeddings
python -c "from embeddings_manager import EmbeddingsManager; em = EmbeddingsManager(); print('OK')"

# Test document processor
python -c "from document_processor import DocumentProcessor; dp = DocumentProcessor(); print('OK')"
```

## 📞 Getting More Help

### Before Asking for Help

1. ✅ Run `python test_setup.py`
2. ✅ Check this troubleshooting guide
3. ✅ Read error message carefully
4. ✅ Check logs in `logs/` folder
5. ✅ Try the suggested solutions

### When Asking for Help

Include:
- Operating system and version
- Python version (`python --version`)
- Error message (full text)
- What you were trying to do
- What you've already tried
- Relevant logs

### Useful Commands

```bash
# System info
python --version
pip list
python test_setup.py

# Check configuration
python -c "from config import Config; print(Config.get_info())"

# Test imports
python -c "import streamlit, langchain, chromadb; print('All imports OK')"
```

## 🔄 Reset Everything

If all else fails, complete reset:

```bash
# 1. Stop application (Ctrl+C)

# 2. Delete everything except source files
rm -rf venv chroma_db temp logs .env

# 3. Reinstall
# Windows:
install.bat

# macOS/Linux:
./install.sh

# 4. Reconfigure .env

# 5. Test
python test_setup.py

# 6. Run
# Windows:
run.bat

# macOS/Linux:
./run.sh
```

## ✅ Prevention Tips

1. **Keep backups** of working .env
2. **Document your settings** that work well
3. **Update regularly** but test first
4. **Monitor logs** for warnings
5. **Start small** when testing changes

---

**Still stuck?** Check the main README.md or create an issue with full details.
