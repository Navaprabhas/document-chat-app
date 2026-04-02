"""
Embeddings and vector store management
"""
import logging
import os
from typing import List, Dict, Optional
import pickle
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from config import Config

logger = logging.getLogger(__name__)

class EmbeddingsManager:
    """Manages embeddings and vector store operations"""
    
    def __init__(self):
        """Initialize embeddings model and vector store"""
        self.embeddings = self._initialize_embeddings()
        self.vector_store = self._initialize_vector_store()
        self.metadata_store = []  # Store metadata separately
        logger.info("Embeddings manager initialized")
    
    def _initialize_embeddings(self):
        """Initialize embeddings model based on configuration"""
        try:
            if Config.EMBEDDING_MODEL == "openai":
                logger.info("Using OpenAI embeddings")
                api_key = os.getenv("OPENAI_API_KEY", "")
                return OpenAIEmbeddings(
                    openai_api_key=api_key,
                    model=Config.OPENAI_EMBEDDING_MODEL
                )
            elif Config.EMBEDDING_MODEL == "google":
                logger.info(f"Using Google embeddings: {Config.GOOGLE_EMBEDDING_MODEL}")
                from langchain_google_genai import GoogleGenerativeAIEmbeddings
                # Get API key directly from environment (updated by user input)
                api_key = os.getenv("GOOGLE_API_KEY", "")
                if not api_key:
                    raise ValueError("Google API key not found. Please enter your API key.")
                return GoogleGenerativeAIEmbeddings(
                    model=Config.GOOGLE_EMBEDDING_MODEL,
                    google_api_key=api_key,
                    task_type="retrieval_document"
                )
            elif Config.EMBEDDING_MODEL == "ollama":
                logger.info("Using Ollama embeddings")
                return OllamaEmbeddings(
                    model=Config.OLLAMA_EMBEDDING_MODEL,
                    base_url=Config.OLLAMA_BASE_URL
                )
            else:
                raise ValueError(f"Unknown embedding model: {Config.EMBEDDING_MODEL}")
                
        except Exception as e:
            logger.error(f"Error initializing embeddings: {str(e)}")
            raise
    
    def _initialize_vector_store(self):
        """Initialize FAISS vector store"""
        try:
            store_path = Path(Config.VECTOR_STORE_PATH)
            
            # Try to load existing store
            if store_path.exists():
                logger.info(f"Loading existing vector store from {store_path}")
                vector_store = FAISS.load_local(
                    str(store_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                
                # Load metadata
                metadata_path = store_path / "metadata.pkl"
                if metadata_path.exists():
                    with open(metadata_path, 'rb') as f:
                        self.metadata_store = pickle.load(f)
                
                return vector_store
            else:
                logger.info("Creating new vector store")
                return None
                
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            return None
    
    def add_documents(self, chunks: List[str], metadata: Dict):
        """
        Add document chunks to vector store
        
        Args:
            chunks: List of text chunks
            metadata: Document metadata including chunk information
        """
        try:
            logger.info(f"Adding {len(chunks)} chunks to vector store")
            
            # Create Document objects for FAISS
            documents = []
            for i, chunk in enumerate(chunks):
                doc_metadata = {
                    'source': metadata['chunks'][i]['source'],
                    'page': metadata['chunks'][i]['page'],
                    'chunk_index': metadata['chunks'][i]['chunk_index']
                }
                documents.append(Document(page_content=chunk, metadata=doc_metadata))
                self.metadata_store.append(doc_metadata)
            
            # Create or update vector store
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
            else:
                # Add to existing store
                new_store = FAISS.from_documents(documents, self.embeddings)
                self.vector_store.merge_from(new_store)
            
            # Save vector store
            self._save_vector_store()
            
            logger.info(f"Successfully added {len(chunks)} chunks")
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def _save_vector_store(self):
        """Save vector store to disk"""
        try:
            store_path = Path(Config.VECTOR_STORE_PATH)
            store_path.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            self.vector_store.save_local(str(store_path))
            
            # Save metadata
            metadata_path = store_path / "metadata.pkl"
            with open(metadata_path, 'wb') as f:
                pickle.dump(self.metadata_store, f)
            
            logger.info(f"Vector store saved to {store_path}")
            
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant documents with metadata
        """
        try:
            if top_k is None:
                top_k = Config.TOP_K
            
            if self.vector_store is None:
                logger.warning("Vector store is empty")
                return []
            
            # Search in FAISS
            results = self.vector_store.similarity_search_with_score(query, k=top_k)
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    'text': doc.page_content,
                    'metadata': doc.metadata,
                    'score': 1 / (1 + score)  # Convert distance to similarity
                })
            
            logger.info(f"Found {len(formatted_results)} relevant documents")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            raise
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the vector store collection"""
        try:
            if self.vector_store is None:
                return {'total_chunks': 0}
            
            return {
                'total_chunks': len(self.metadata_store),
                'collection_name': 'faiss_store'
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {}
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        try:
            self.vector_store = None
            self.metadata_store = []
            
            # Remove saved files
            store_path = Path(Config.VECTOR_STORE_PATH)
            if store_path.exists():
                import shutil
                shutil.rmtree(store_path)
            
            logger.info("Collection cleared")
        except Exception as e:
            logger.error(f"Error clearing collection: {str(e)}")
            raise
