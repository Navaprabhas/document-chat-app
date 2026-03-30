# 🏗️ Architecture Documentation

Complete technical architecture of the Document Chat Application.

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│                     (Streamlit - app.py)                     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Sidebar    │  │  Chat Area   │  │   Settings   │     │
│  │              │  │              │  │              │     │
│  │ • Upload     │  │ • Messages   │  │ • Chunk Size │     │
│  │ • Doc List   │  │ • Citations  │  │ • Top-K      │     │
│  │ • Export     │  │ • Input      │  │ • Overlap    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────┬────────────────────────────────┬──────────────┘
             │                                │
             ▼                                ▼
┌────────────────────────┐        ┌──────────────────────────┐
│  Document Processor    │        │     Chat Engine          │
│  (document_processor)  │        │    (chat_engine.py)      │
│                        │        │                          │
│  • PDF Reading         │        │  • Query Processing      │
│  • Text Extraction     │        │  • Context Retrieval     │
│  • Chunking            │        │  • LLM Integration       │
│  • Metadata Tracking   │        │  • Response Generation   │
└────────────┬───────────┘        └──────────┬───────────────┘
             │                                │
             │                                │
             ▼                                ▼
┌─────────────────────────────────────────────────────────────┐
│              Embeddings Manager                              │
│            (embeddings_manager.py)                           │
│                                                              │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │  Embedding Model │         │   Vector Store   │         │
│  │                  │         │                  │         │
│  │  • OpenAI        │◄───────►│  • ChromaDB      │         │
│  │  • Ollama        │         │  • Persistence   │         │
│  └──────────────────┘         │  • Search        │         │
│                                └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
             │                                │
             ▼                                ▼
┌────────────────────────┐        ┌──────────────────────────┐
│   External Services    │        │    Local Storage         │
│                        │        │                          │
│  • OpenAI API          │        │  • chroma_db/            │
│  • Ollama Server       │        │  • temp/                 │
│                        │        │  • logs/                 │
└────────────────────────┘        └──────────────────────────┘
```

## 🔄 Data Flow

### Document Upload Flow

```
1. User uploads PDF
   │
   ├─► app.py receives file
   │
   ├─► Save to temp/ directory
   │
   ├─► DocumentProcessor.process_pdf()
   │   │
   │   ├─► Extract text page by page (PyPDF2)
   │   │
   │   ├─► Clean text
   │   │
   │   └─► Split into chunks (RecursiveCharacterTextSplitter)
   │       │
   │       └─► Return chunks + metadata
   │
   ├─► EmbeddingsManager.add_documents()
   │   │
   │   ├─► Generate embeddings (OpenAI/Ollama)
   │   │
   │   └─► Store in ChromaDB
   │       │
   │       ├─► Document text
   │       ├─► Embeddings
   │       └─► Metadata (source, page, chunk_index)
   │
   └─► Update UI with success message
```

### Query Flow

```
1. User asks question
   │
   ├─► app.py receives query
   │
   ├─► ChatEngine.chat()
   │   │
   │   ├─► EmbeddingsManager.search()
   │   │   │
   │   │   ├─► Generate query embedding
   │   │   │
   │   │   ├─► Search ChromaDB (cosine similarity)
   │   │   │
   │   │   └─► Return top-k relevant chunks
   │   │
   │   ├─► Format context from chunks
   │   │
   │   ├─► Build prompt with:
   │   │   ├─► System message
   │   │   ├─► Context
   │   │   ├─► Chat history
   │   │   └─► User question
   │   │
   │   ├─► Call LLM (OpenAI/Ollama)
   │   │
   │   └─► Extract citations
   │
   └─► Display response + citations in UI
```

## 🧩 Component Details

### 1. app.py (Frontend)

**Responsibilities:**
- User interface rendering
- File upload handling
- Session state management
- Chat display
- Settings management

**Key Functions:**
- `initialize_session_state()` - Setup session variables
- `sidebar()` - Render sidebar UI
- `process_documents()` - Handle document upload
- `display_chat_message()` - Render messages
- `main()` - Application entry point

**Session State:**
```python
{
    'messages': [],              # Chat history
    'documents': [],             # Uploaded docs info
    'vector_store_ready': False, # Processing status
    'chat_engine': None,         # ChatEngine instance
    'embeddings_manager': None   # EmbeddingsManager instance
}
```

### 2. document_processor.py (Document Processing)

**Responsibilities:**
- PDF text extraction
- Text cleaning
- Intelligent chunking
- Metadata tracking

**Key Classes:**
- `DocumentProcessor` - Main processor class

**Key Methods:**
- `process_pdf()` - Process entire PDF
- `_extract_text_from_pdf()` - Extract text by page
- `_clean_text()` - Clean extracted text
- `get_document_stats()` - Get document statistics

**Chunking Strategy:**
```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Characters per chunk
    chunk_overlap=200,      # Overlap between chunks
    separators=[            # Split priority
        "\n\n",            # Paragraphs first
        "\n",              # Then lines
        ". ",              # Then sentences
        " ",               # Then words
        ""                 # Then characters
    ]
)
```

### 3. embeddings_manager.py (Vector Store)

**Responsibilities:**
- Embedding generation
- Vector store management
- Similarity search
- Persistence

**Key Classes:**
- `EmbeddingsManager` - Main manager class

**Key Methods:**
- `_initialize_embeddings()` - Setup embedding model
- `_initialize_vector_store()` - Setup ChromaDB
- `add_documents()` - Add chunks to store
- `search()` - Semantic search
- `get_collection_stats()` - Get statistics
- `clear_collection()` - Clear all data

**Vector Store Schema:**
```python
{
    'id': 'document_name_chunk_index',
    'embedding': [0.1, 0.2, ...],  # 1536-dim for OpenAI
    'document': 'chunk text',
    'metadata': {
        'source': 'document.pdf',
        'page': 5,
        'chunk_index': 2,
        'text': 'preview...'
    }
}
```

### 4. chat_engine.py (RAG Engine)

**Responsibilities:**
- Query processing
- Context retrieval
- Prompt engineering
- LLM interaction
- Citation extraction

**Key Classes:**
- `ChatEngine` - Main RAG engine

**Key Methods:**
- `_initialize_llm()` - Setup language model
- `_create_prompt_template()` - Create prompt
- `chat()` - Generate response
- `_format_context()` - Format retrieved docs
- `_format_chat_history()` - Format history
- `_extract_citations()` - Extract sources

**Prompt Structure:**
```
System Message:
  - Role definition
  - Instructions
  - Context from documents

Chat History:
  - Previous messages
  - Limited to last N messages

User Question:
  - Current query
```

### 5. config.py (Configuration)

**Responsibilities:**
- Environment variable loading
- Configuration validation
- Default values
- Settings management

**Configuration Categories:**
- API Keys
- LLM Settings
- Embedding Settings
- Vector Store Settings
- Document Processing
- RAG Parameters

## 🔐 Security Architecture

### API Key Management
```
.env file (not in git)
    ↓
os.getenv() in config.py
    ↓
Used in components
    ↓
Never logged or displayed
```

### Data Flow Security
- User uploads → Temp storage → Processed → Deleted
- API keys → Environment variables only
- No sensitive data in logs
- Vector store → Local persistence

## 📊 Performance Considerations

### Bottlenecks
1. **PDF Processing**: I/O bound
2. **Embedding Generation**: API/GPU bound
3. **Vector Search**: Memory/CPU bound
4. **LLM Generation**: API/GPU bound

### Optimizations
- Batch embedding generation
- Efficient chunking strategy
- Vector store indexing (HNSW)
- Caching (Streamlit @cache)
- Async operations (future)

### Scaling Strategies
```
Single User:
  Streamlit → Local ChromaDB → OpenAI API

Multiple Users:
  Streamlit → Shared ChromaDB → OpenAI API
  (Add authentication)

Production:
  Load Balancer
      ↓
  Multiple Streamlit Instances
      ↓
  Managed Vector DB (Pinecone/Weaviate)
      ↓
  OpenAI API / Self-hosted LLM
```

## 🗄️ Data Storage

### Temporary Storage
```
temp/
  └── uploaded_file.pdf  (deleted after processing)
```

### Vector Store
```
chroma_db/
  ├── chroma.sqlite3     (metadata)
  └── [uuid]/            (embeddings)
```

### Logs
```
logs/
  └── app.log            (application logs)
```

### Session State
- In-memory (Streamlit session)
- Lost on page refresh
- Can be persisted (future enhancement)

## 🔌 Integration Points

### External APIs
- **OpenAI API**: Embeddings + LLM
- **Ollama API**: Local embeddings + LLM

### File System
- Read: PDF uploads
- Write: Temp files, logs, vector DB

### Browser
- WebSocket: Streamlit communication
- HTTP: File uploads
- LocalStorage: Streamlit state (minimal)

## 🧪 Testing Architecture

### Unit Tests (Future)
- `test_document_processor.py`
- `test_embeddings_manager.py`
- `test_chat_engine.py`
- `test_config.py`

### Integration Tests (Future)
- End-to-end document processing
- Query-response flow
- Error handling

### Current Testing
- `test_setup.py` - Setup validation
- Manual testing checklist

## 🔄 State Management

### Application State
```python
# Streamlit Session State
st.session_state = {
    'messages': [],           # Chat messages
    'documents': [],          # Document metadata
    'vector_store_ready': False,
    'chat_engine': ChatEngine,
    'embeddings_manager': EmbeddingsManager
}
```

### Configuration State
```python
# config.py - Global configuration
Config.CHUNK_SIZE = 1000
Config.TOP_K = 5
# etc.
```

### Vector Store State
```python
# ChromaDB - Persistent
collection.count()  # Number of chunks
collection.get()    # Retrieve chunks
```

## 📈 Monitoring Points

### Application Metrics
- Document processing time
- Query response time
- Error rate
- API call count

### System Metrics
- Memory usage
- Disk usage
- CPU usage
- Network I/O

### Business Metrics
- Documents processed
- Queries answered
- User sessions
- API costs

## 🔮 Future Architecture

### Planned Enhancements
```
Current:
  Streamlit → ChromaDB → OpenAI

Future:
  React Frontend
      ↓
  FastAPI Backend
      ↓
  ┌─────────┬─────────┬─────────┐
  │ Redis   │ Postgres│ Vector  │
  │ Cache   │ Metadata│ DB      │
  └─────────┴─────────┴─────────┘
      ↓
  LLM Service (OpenAI/Self-hosted)
```

### Microservices (Future)
- Document Processing Service
- Embedding Service
- Query Service
- User Management Service

---

**For implementation details, see source code files.**
