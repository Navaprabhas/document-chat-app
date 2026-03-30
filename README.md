# 📚 Document Chat Application

A production-ready RAG (Retrieval Augmented Generation) application that allows users to upload PDF documents and chat with them using AI-powered search and generation.

## ✨ Features

- **Multi-document Upload**: Upload and process multiple PDF documents simultaneously
- **Intelligent Text Chunking**: Smart text splitting with configurable overlap for better context
- **Semantic Search**: Vector-based similarity search through documents using embeddings
- **Citation Tracking**: See which document and page each answer comes from
- **Conversation Memory**: Maintains chat history for contextual conversations
- **Export Chat History**: Download conversation history as JSON
- **Document Preview**: View loaded documents with statistics
- **Flexible LLM Support**: Works with OpenAI GPT or local models via Ollama
- **Vector Database**: ChromaDB for efficient embedding storage and retrieval
- **Clean UI**: Modern Streamlit interface with responsive design

## 🏗️ Architecture

```
document-chat-app/
├── app.py                    # Main Streamlit application
├── document_processor.py     # PDF processing and chunking
├── embeddings_manager.py     # Vector store operations
├── chat_engine.py           # RAG implementation
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the project directory
cd document-chat-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Add your OpenAI API key or configure Ollama
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## ⚙️ Configuration Options

### Using OpenAI (Recommended for Production)

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
EMBEDDING_MODEL=openai
```

### Using Ollama (Local/Free)

First, install and run Ollama:
```bash
# Install Ollama from https://ollama.ai
# Pull required models
ollama pull llama2
ollama pull nomic-embed-text
```

Then configure:
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama2
EMBEDDING_MODEL=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

## 📖 Usage Guide

### 1. Upload Documents
- Click "Browse files" in the sidebar
- Select one or more PDF documents
- Click "Process Documents"
- Wait for processing to complete

### 2. Ask Questions
- Type your question in the chat input
- Press Enter or click Send
- View the AI-generated response with citations

### 3. View Sources
- Click "View Sources" under any response
- See which documents and pages were used
- Check relevance scores for each source

### 4. Export Chat
- Click "Export Chat History" in the sidebar
- Download JSON file with full conversation

### 5. Adjust Settings
- Use sliders in sidebar to adjust:
  - Chunk Size (500-2000 characters)
  - Chunk Overlap (0-500 characters)
  - Number of Results (1-10 documents)

## 🎯 Example Questions

- "What are the main topics covered in these documents?"
- "Summarize the key findings from page 5"
- "Compare the approaches mentioned in different documents"
- "What does the document say about [specific topic]?"
- "List all the recommendations from the documents"

## 🔧 Advanced Configuration

### Chunk Size and Overlap

- **Chunk Size**: Larger chunks (1500-2000) provide more context but may be less precise
- **Chunk Overlap**: More overlap (200-300) helps maintain context across chunks
- **Top K**: More results (7-10) provide broader context but may include less relevant info

### Temperature Settings

- **Low (0.0-0.3)**: More focused and deterministic responses
- **Medium (0.4-0.7)**: Balanced creativity and accuracy
- **High (0.8-1.0)**: More creative but potentially less accurate

## 🐛 Troubleshooting

### "No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"
- Check your `.env` file has `OPENAI_API_KEY` set
- Ensure `.env` is in the same directory as `app.py`

### "ChromaDB connection error"
- Delete the `chroma_db` folder and restart
- Check disk space and permissions

### "PDF processing failed"
- Ensure PDF is not password-protected
- Try a different PDF reader library if issues persist

## 📊 Performance Tips

1. **Batch Processing**: Upload multiple documents at once for efficiency
2. **Chunk Size**: Start with 1000 and adjust based on your documents
3. **Top K**: Use 3-5 for faster responses, 7-10 for comprehensive answers
4. **Model Selection**: GPT-4 for best quality, GPT-3.5 for speed

## 🔒 Security Notes

- Never commit `.env` file with real API keys
- Use environment variables for production deployment
- Implement rate limiting for public deployments
- Sanitize user inputs in production

## 🚢 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Add secrets in dashboard (API keys)
4. Deploy

### Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

### Local Server

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 📝 Logging

Logs are written to console with timestamps. To save logs:

```bash
streamlit run app.py > app.log 2>&1
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Support for more document types (DOCX, TXT, etc.)
- Advanced filtering and search options
- Multi-language support
- Document comparison features
- Batch question answering

## 📄 License

MIT License - feel free to use in your projects!

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [LangChain](https://langchain.com/) - LLM orchestration
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [OpenAI](https://openai.com/) - Language models
- [Ollama](https://ollama.ai/) - Local model support

## 📧 Support

For issues and questions:
- Check the troubleshooting section
- Review configuration settings
- Check logs for error messages
