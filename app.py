"""
Main Streamlit application for Document Chat
"""
import streamlit as st
import logging
from pathlib import Path
import json
from datetime import datetime

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

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: #000000 !important;
    }
    .user-message {
        background-color: #e3f2fd;
        color: #000000 !important;
    }
    .assistant-message {
        background-color: #f5f5f5;
        color: #000000 !important;
    }
    .chat-message p {
        color: #000000 !important;
        margin: 0;
    }
    .chat-message strong {
        color: #1f77b4 !important;
    }
    .citation {
        font-size: 0.85rem;
        color: #666;
        font-style: italic;
        margin-top: 0.5rem;
    }
    .stButton>button {
        width: 100%;
    }
    /* Fix Streamlit chat message styling */
    .stChatMessage {
        background-color: transparent !important;
    }
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
    }
    /* Fix expander styling for View Sources */
    .streamlit-expanderHeader {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
    }
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e0e0e0 !important;
    }
    /* Fix all text in expander */
    .streamlit-expanderContent p,
    .streamlit-expanderContent div,
    .streamlit-expanderContent span,
    .streamlit-expanderContent strong,
    .streamlit-expanderContent em {
        color: #000000 !important;
    }
    /* Fix markdown in expander */
    .streamlit-expanderContent [data-testid="stMarkdownContainer"] {
        color: #000000 !important;
    }
    .streamlit-expanderContent [data-testid="stMarkdownContainer"] * {
        color: #000000 !important;
    }
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
                with st.expander(f"📄 {doc['name']}"):
                    st.write(f"**Pages:** {doc['pages']}")
                    st.write(f"**Chunks:** {doc['chunks']}")
                    st.write(f"**Uploaded:** {doc['timestamp']}")
        
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
            help="Size of text chunks for processing"
        )
        
        chunk_overlap = st.slider(
            "Chunk Overlap",
            min_value=0,
            max_value=500,
            value=Config.CHUNK_OVERLAP,
            step=50,
            help="Overlap between consecutive chunks"
        )
        
        top_k = st.slider(
            "Number of Results",
            min_value=1,
            max_value=10,
            value=Config.TOP_K,
            help="Number of relevant chunks to retrieve"
        )
        
        # Update config
        Config.CHUNK_SIZE = chunk_size
        Config.CHUNK_OVERLAP = chunk_overlap
        Config.TOP_K = top_k

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
            total_files = len(uploaded_files)
            
            for idx, uploaded_file in enumerate(uploaded_files):
                logger.info(f"Processing {uploaded_file.name}")
                
                # Save uploaded file temporarily
                temp_path = Path("temp") / uploaded_file.name
                temp_path.parent.mkdir(exist_ok=True)
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process document
                chunks, metadata = processor.process_pdf(str(temp_path))
                
                # Add to vector store
                st.session_state.embeddings_manager.add_documents(
                    chunks,
                    metadata
                )
                
                # Store document info
                st.session_state.documents.append({
                    'name': uploaded_file.name,
                    'pages': metadata.get('total_pages', 0),
                    'chunks': len(chunks),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        <strong style="color: #1f77b4;">{icon} {role.capitalize()}</strong><br>
        <p style="color: #000000; margin-top: 0.5rem;">{content}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display citations if available
    if role == "assistant" and 'citations' in message:
        with st.expander("📎 View Sources", expanded=False):
            for i, citation in enumerate(message['citations'], 1):
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border-left: 3px solid #1f77b4;">
                    <p style="color: #000000; margin: 0;"><strong style="color: #1f77b4;">Source {i}</strong></p>
                    <p style="color: #000000; margin: 0.5rem 0 0 0;"><strong>Document:</strong> <span style="color: #000000;">{citation['source']}</span></p>
                    <p style="color: #000000; margin: 0.25rem 0 0 0;"><strong>Page:</strong> <span style="color: #000000;">{citation['page']}</span></p>
                    <p style="color: #000000; margin: 0.25rem 0 0 0;"><strong>Relevance Score:</strong> <span style="color: #000000;">{citation['score']:.2f}</span></p>
                    <p style="color: #000000; margin: 0.5rem 0 0 0;"><em style="color: #666;">Excerpt:</em> <span style="color: #333;">{citation['text'][:200]}...</span></p>
                </div>
                """, unsafe_allow_html=True)

def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">📚 Document Chat Assistant</div>', unsafe_allow_html=True)
    st.markdown("Upload PDF documents and chat with them using AI-powered search and generation.")
    
    # Sidebar
    sidebar()
    
    # Main chat interface
    if not st.session_state.vector_store_ready:
        st.info("👈 Upload and process documents from the sidebar to start chatting!")
        
        # Show example queries
        st.markdown("### 💡 Example Questions You Can Ask:")
        st.markdown("""
        - What are the main topics covered in these documents?
        - Summarize the key findings from page 5
        - Compare the approaches mentioned in different documents
        - What does the document say about [specific topic]?
        """)
    else:
        # Display chat messages
        for message in st.session_state.messages:
            display_chat_message(message)
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            # Add user message
            st.session_state.messages.append({
                'role': 'user',
                'content': prompt
            })
            
            # Display user message
            display_chat_message(st.session_state.messages[-1])
            
            # Generate response
            with st.spinner("Thinking..."):
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
