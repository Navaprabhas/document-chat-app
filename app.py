"""
Main Streamlit application for Document Chat
"""
import streamlit as st
import logging
from pathlib import Path
import json
from datetime import datetime
import os

from document_processor import DocumentProcessor
from embeddings_manager import EmbeddingsManager
from chat_engine import ChatEngine
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Document Chat Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern, Beautiful Design
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem 0;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Document card styling */
    .doc-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        transition: transform 0.2s;
    }
    
    .doc-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Suggested questions */
    .suggested-question {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 25px;
        margin: 0.5rem;
        cursor: pointer;
        display: inline-block;
        transition: all 0.3s;
        border: none;
        font-size: 0.95rem;
    }
    
    .suggested-question:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        animation: fadeIn 0.3s;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        margin-left: 20%;
    }
    
    .user-message p, .user-message strong {
        color: white !important;
    }
    
    .assistant-message {
        background: white;
        color: #1e293b !important;
        margin-right: 20%;
        border: 1px solid #e2e8f0;
    }
    
    .assistant-message p, .assistant-message strong {
        color: #1e293b !important;
    }
    
    /* Icons */
    .message-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    /* Citations */
    .citation-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.25rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        border-left: 4px solid #667eea;
        transition: all 0.2s;
    }
    
    .citation-card:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #e0e7ff 0%, #cffafe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin: 0.5rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 10px;
        font-weight: 600;
        color: #1e293b !important;
    }
    
    .streamlit-expanderContent {
        background: white;
        border-radius: 0 0 10px 10px;
        border: 1px solid #e2e8f0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* File uploader */
    .uploadedFile {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        border-radius: 10px;
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        border-radius: 10px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    if 'vector_store_ready' not in st.session_state:
        st.session_state.vector_store_ready = False
    if 'chat_engine' not in st.session_state:
        st.session_state.chat_engine = None
    if 'embeddings_manager' not in st.session_state:
        st.session_state.embeddings_manager = None
    if 'api_key_configured' not in st.session_state:
        st.session_state.api_key_configured = False
    if 'user_api_key' not in st.session_state:
        st.session_state.user_api_key = None
    if 'document_summaries' not in st.session_state:
        st.session_state.document_summaries = {}
    if 'suggested_questions' not in st.session_state:
        st.session_state.suggested_questions = []

def sidebar():
    """Render sidebar with document upload and management"""
    with st.sidebar:
        st.markdown("### 📁 Document Management")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload PDF documents",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more PDF documents to chat with"
        )
        
        if uploaded_files:
            if st.button("Process Documents", type="primary"):
                process_documents(uploaded_files)
        
        # Display processed documents
        if st.session_state.documents:
            st.markdown("---")
            st.markdown("### 📚 Loaded Documents")
            for doc in st.session_state.documents:
                with st.expander(f"📄 {doc['name']}", expanded=False):
                    # Document stats
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Pages", doc['pages'])
                    with col2:
                        st.metric("Chunks", doc['chunks'])
                    
                    # Summary
                    if 'summary' in doc and doc['summary']:
                        st.markdown("**📝 Summary:**")
                        st.info(doc['summary'])
                    
                    st.caption(f"Uploaded: {doc['timestamp']}")
        
        # Clear all button
        if st.session_state.documents:
            st.markdown("---")
            if st.button("🗑️ Clear All Documents", type="secondary"):
                clear_all_documents()
        
        # Export chat history
        if st.session_state.messages:
            st.markdown("---")
            if st.button("💾 Export Chat History"):
                export_chat_history()
        
        # Settings
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        chunk_size = st.slider(
            "Chunk Size",
            min_value=500,
            max_value=2000,
            value=Config.CHUNK_SIZE,
            step=100,
            help="📏 **Chunk Size**: Controls how much text is processed at once.\n\n"
                 "• **Smaller (500-800)**: More precise answers, better for specific questions\n"
                 "• **Medium (1000-1200)**: Balanced approach (recommended)\n"
                 "• **Larger (1500-2000)**: More context, better for broad questions\n\n"
                 "💡 Start with 1000 and adjust based on your documents."
        )
        
        chunk_overlap = st.slider(
            "Chunk Overlap",
            min_value=0,
            max_value=500,
            value=Config.CHUNK_OVERLAP,
            step=50,
            help="🔗 **Chunk Overlap**: How much text is shared between consecutive chunks.\n\n"
                 "• **No Overlap (0)**: Faster processing, may miss context\n"
                 "• **Low (50-100)**: Good for simple documents\n"
                 "• **Medium (150-250)**: Balanced (recommended)\n"
                 "• **High (300-500)**: Better context preservation\n\n"
                 "💡 Use 200 for most documents."
        )
        
        top_k = st.slider(
            "Number of Results",
            min_value=1,
            max_value=10,
            value=Config.TOP_K,
            help="🎯 **Number of Results**: How many relevant text chunks to retrieve.\n\n"
                 "• **Few (1-3)**: Faster, more focused answers\n"
                 "• **Medium (4-6)**: Balanced approach (recommended)\n"
                 "• **Many (7-10)**: More comprehensive, may include less relevant info\n\n"
                 "💡 Use 5 for best balance of speed and accuracy."
        )
        
        # Update config
        Config.CHUNK_SIZE = chunk_size
        Config.CHUNK_OVERLAP = chunk_overlap
        Config.TOP_K = top_k

def generate_document_summary(doc_name, chunks):
    """Generate a quick summary of the document using AI"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Use first few chunks for summary
        sample_text = " ".join(chunks[:3])[:2000]
        
        llm = ChatGoogleGenerativeAI(
            model=Config.GOOGLE_MODEL,
            google_api_key=os.getenv("GOOGLE_API_KEY", ""),
            temperature=0.3
        )
        
        prompt = f"""Provide a brief 2-3 sentence summary of this document:

{sample_text}

Summary:"""
        
        response = llm.invoke(prompt)
        return response.content
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return "Summary generation failed."

def generate_suggested_questions():
    """Generate suggested questions based on uploaded documents"""
    try:
        if not st.session_state.documents:
            return []
        
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Get document names
        doc_names = [doc['name'] for doc in st.session_state.documents]
        
        llm = ChatGoogleGenerativeAI(
            model=Config.GOOGLE_MODEL,
            google_api_key=os.getenv("GOOGLE_API_KEY", ""),
            temperature=0.7
        )
        
        prompt = f"""Based on these document names: {', '.join(doc_names)}

Generate 5 smart, specific questions that users might want to ask about these documents.
Make them diverse and useful.

Format: Return only the questions, one per line, without numbering."""
        
        response = llm.invoke(prompt)
        questions = [q.strip() for q in response.content.split('\n') if q.strip() and not q.strip().startswith('#')]
        return questions[:5]
        
    except Exception as e:
        logger.error(f"Error generating questions: {str(e)}")
        return [
            "What are the main topics covered in these documents?",
            "Can you summarize the key findings?",
            "What are the most important points?",
            "Are there any conclusions or recommendations?",
            "What information is most relevant to my needs?"
        ]

def validate_google_api_key(api_key):
    """Validate Google Gemini API key by making a test call"""
    try:
        import google.generativeai as genai
        
        # Configure with the API key
        genai.configure(api_key=api_key)
        
        # Try to list models to verify the key works
        models = genai.list_models()
        
        # Check if we can access at least one model
        for model in models:
            if 'gemini' in model.name.lower():
                return True, "API key is valid!"
        
        return False, "API key is valid but no Gemini models found"
        
    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
            return False, "Invalid API key. Please check and try again."
        elif "quota" in error_msg.lower():
            return False, "API key is valid but quota exceeded."
        else:
            return False, f"Error validating API key: {error_msg}"

def check_api_key_section():
    """Display API key input section with validation"""
    import os
    
    # Check if API key is in environment (for local development)
    env_api_key = os.getenv('GOOGLE_API_KEY')
    
    # If no API key in session and no env key, show input
    if not st.session_state.api_key_configured and not env_api_key:
        st.warning("⚠️ Please enter your Google Gemini API key to use this application.")
        
        with st.expander("🔑 Enter Your Google Gemini API Key", expanded=True):
            st.markdown("""
            ### How to get your API key:
            1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
            2. Sign in with your Google account
            3. Click "Create API Key"
            4. Copy your API key and paste it below
            
            ### 🔒 Privacy & Security:
            - Your API key is **only stored in your browser session**
            - It is **never saved on our servers**
            - Each user has their own separate session
            - Your API key is **not visible to other users**
            - The key is cleared when you close your browser
            """)
            
            api_key_input = st.text_input(
                "Google Gemini API Key",
                type="password",
                placeholder="AIza...",
                help="Your API key will be validated and used only for this session. It's never shared or stored permanently.",
                key="api_key_input"
            )
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("✅ Validate & Set API Key", type="primary"):
                    if api_key_input and len(api_key_input) > 20:
                        with st.spinner("Validating API key..."):
                            is_valid, message = validate_google_api_key(api_key_input)
                            
                            if is_valid:
                                st.session_state.user_api_key = api_key_input
                                st.session_state.api_key_configured = True
                                # Set it in environment for this session only
                                os.environ['GOOGLE_API_KEY'] = api_key_input
                                st.success(f"✅ {message}")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
                    else:
                        st.error("❌ Please enter a valid API key (should start with 'AIza')")
        
        return False
    else:
        # API key is configured (either from user input or environment)
        if not st.session_state.api_key_configured and env_api_key:
            st.session_state.api_key_configured = True
            st.session_state.user_api_key = env_api_key
        
        # Show configured status in sidebar
        with st.sidebar:
            st.success("✅ API Key Configured")
            if st.button("🔄 Change API Key"):
                st.session_state.api_key_configured = False
                st.session_state.user_api_key = None
                # Clear from environment
                if 'GOOGLE_API_KEY' in os.environ:
                    del os.environ['GOOGLE_API_KEY']
                st.rerun()
        
        return True

def process_documents(uploaded_files):
    """Process uploaded PDF documents"""
    try:
        with st.spinner("Processing documents..."):
            # Initialize processor
            processor = DocumentProcessor()
            
            # Initialize embeddings manager if not exists
            if st.session_state.embeddings_manager is None:
                st.session_state.embeddings_manager = EmbeddingsManager()
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            total_files = len(uploaded_files)
            
            for idx, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}...")
                logger.info(f"Processing {uploaded_file.name}")
                
                # Save uploaded file temporarily
                temp_path = Path("temp") / uploaded_file.name
                temp_path.parent.mkdir(exist_ok=True)
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process document
                chunks, metadata = processor.process_pdf(str(temp_path))
                
                # Generate summary
                status_text.text(f"Generating summary for {uploaded_file.name}...")
                summary = generate_document_summary(uploaded_file.name, chunks)
                
                # Add to vector store
                st.session_state.embeddings_manager.add_documents(
                    chunks,
                    metadata
                )
                
                # Store document info with summary
                st.session_state.documents.append({
                    'name': uploaded_file.name,
                    'pages': metadata.get('total_pages', 0),
                    'chunks': len(chunks),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'summary': summary
                })
                
                # Update progress
                progress_bar.progress((idx + 1) / total_files)
                
                # Clean up temp file
                temp_path.unlink()
            
            # Initialize chat engine
            st.session_state.chat_engine = ChatEngine(
                st.session_state.embeddings_manager
            )
            st.session_state.vector_store_ready = True
            
            # Generate suggested questions
            status_text.text("Generating suggested questions...")
            st.session_state.suggested_questions = generate_suggested_questions()
            
            status_text.empty()
            st.success(f"✅ Successfully processed {total_files} document(s)!")
            logger.info(f"Processed {total_files} documents successfully")
            
    except Exception as e:
        logger.error(f"Error processing documents: {str(e)}")
        st.error(f"Error processing documents: {str(e)}")

def clear_all_documents():
    """Clear all documents and reset state"""
    st.session_state.documents = []
    st.session_state.messages = []
    st.session_state.vector_store_ready = False
    st.session_state.chat_engine = None
    st.session_state.embeddings_manager = None
    st.success("All documents cleared!")
    st.rerun()

def export_chat_history():
    """Export chat history as JSON"""
    try:
        chat_data = {
            'exported_at': datetime.now().isoformat(),
            'documents': st.session_state.documents,
            'messages': st.session_state.messages
        }
        
        json_str = json.dumps(chat_data, indent=2)
        
        st.download_button(
            label="Download Chat History",
            data=json_str,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
    except Exception as e:
        logger.error(f"Error exporting chat history: {str(e)}")
        st.error(f"Error exporting chat history: {str(e)}")

def display_chat_message(message):
    """Display a chat message with citations"""
    role = message['role']
    content = message['content']
    
    css_class = "user-message" if role == "user" else "assistant-message"
    icon = "👤" if role == "user" else "🤖"
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <span class="message-icon">{icon}</span>
        <strong>{role.capitalize()}</strong><br>
        <p style="margin-top: 0.75rem;">{content}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display citations if available
    if role == "assistant" and 'citations' in message:
        with st.expander("📎 View Sources", expanded=False):
            for i, citation in enumerate(message['citations'], 1):
                st.markdown(f"""
                <div class="citation-card">
                    <p style="margin: 0;"><strong style="color: #667eea;">📌 Source {i}</strong></p>
                    <p style="margin: 0.5rem 0 0 0;"><strong>Document:</strong> {citation['source']}</p>
                    <p style="margin: 0.25rem 0 0 0;"><strong>Page:</strong> {citation['page']}</p>
                    <p style="margin: 0.25rem 0 0 0;"><strong>Relevance:</strong> {citation['score']:.0%}</p>
                    <p style="margin: 0.75rem 0 0 0; color: #64748b;"><em>"{citation['text'][:200]}..."</em></p>
                </div>
                """, unsafe_allow_html=True)

def main():
    """Main application"""
    initialize_session_state()
    
    # Header with modern design
    st.markdown('<div class="main-header">📚 Document Chat Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Upload documents and chat with them using AI-powered intelligence</div>', unsafe_allow_html=True)
    
    # Check API key first
    if not check_api_key_section():
        st.markdown('<div class="info-box">👆 Please configure your API key above to continue.</div>', unsafe_allow_html=True)
        st.stop()
    
    # Sidebar
    sidebar()
    
    # Main chat interface
    if not st.session_state.vector_store_ready:
        # Welcome screen with better design
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### 👋 Welcome!")
        st.markdown("Upload PDF documents from the sidebar to start chatting with them using AI.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show example queries in a nice grid
        st.markdown("### 💡 Example Questions You Can Ask:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="doc-card">
                <strong>📊 Analysis</strong><br>
                • What are the main topics?<br>
                • Summarize key findings<br>
                • What are the conclusions?
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="doc-card">
                <strong>🔍 Search</strong><br>
                • Find information about [topic]<br>
                • Compare different sections<br>
                • What does page X say about Y?
            </div>
            """, unsafe_allow_html=True)
    else:
        # Show document statistics
        if st.session_state.documents:
            col1, col2, col3 = st.columns(3)
            
            total_pages = sum(doc['pages'] for doc in st.session_state.documents)
            total_chunks = sum(doc['chunks'] for doc in st.session_state.documents)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{len(st.session_state.documents)}</div>
                    <div class="stat-label">Documents</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{total_pages}</div>
                    <div class="stat-label">Total Pages</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{total_chunks}</div>
                    <div class="stat-label">Text Chunks</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Show suggested questions if available and no messages yet
        if st.session_state.suggested_questions and not st.session_state.messages:
            st.markdown("### 💡 Suggested Questions")
            st.markdown("Click on any question to ask it:")
            
            # Display suggested questions as clickable buttons
            for question in st.session_state.suggested_questions:
                if st.button(question, key=f"suggested_{question}", use_container_width=True):
                    # Add user message
                    st.session_state.messages.append({
                        'role': 'user',
                        'content': question
                    })
                    st.rerun()
        
        # Display chat messages
        for message in st.session_state.messages:
            display_chat_message(message)
        
        # Chat input
        if prompt := st.chat_input("💬 Ask a question about your documents..."):
            # Add user message
            st.session_state.messages.append({
                'role': 'user',
                'content': prompt
            })
            
            # Display user message
            display_chat_message(st.session_state.messages[-1])
            
            # Generate response
            with st.spinner("🤔 Thinking..."):
                try:
                    response, citations = st.session_state.chat_engine.chat(
                        prompt,
                        st.session_state.messages[:-1]
                    )
                    
                    # Add assistant message
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': response,
                        'citations': citations
                    })
                    
                    # Display assistant message
                    display_chat_message(st.session_state.messages[-1])
                    
                except Exception as e:
                    logger.error(f"Error generating response: {str(e)}")
                    st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main()
