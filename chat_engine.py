"""
RAG-based chat engine for document Q&A
"""
import logging
from typing import List, Dict, Tuple
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from config import Config

logger = logging.getLogger(__name__)

class ChatEngine:
    """Handles RAG-based chat with documents"""
    
    def __init__(self, embeddings_manager):
        """
        Initialize chat engine
        
        Args:
            embeddings_manager: EmbeddingsManager instance
        """
        self.embeddings_manager = embeddings_manager
        self.llm = self._initialize_llm()
        self.prompt_template = self._create_prompt_template()
        logger.info("Chat engine initialized")
    
    def _initialize_llm(self):
        """Initialize language model based on configuration"""
        try:
            if Config.LLM_PROVIDER == "openai":
                logger.info(f"Using OpenAI model: {Config.OPENAI_MODEL}")
                return ChatOpenAI(
                    openai_api_key=Config.OPENAI_API_KEY,
                    model=Config.OPENAI_MODEL,
                    temperature=Config.TEMPERATURE,
                    max_tokens=Config.MAX_TOKENS
                )
            elif Config.LLM_PROVIDER == "google":
                logger.info(f"Using Google model: {Config.GOOGLE_MODEL}")
                from langchain_google_genai import ChatGoogleGenerativeAI
                return ChatGoogleGenerativeAI(
                    model=Config.GOOGLE_MODEL,
                    google_api_key=Config.GOOGLE_API_KEY,
                    temperature=Config.TEMPERATURE,
                    max_output_tokens=Config.MAX_TOKENS
                )
            elif Config.LLM_PROVIDER == "ollama":
                logger.info(f"Using Ollama model: {Config.OLLAMA_MODEL}")
                return ChatOllama(
                    model=Config.OLLAMA_MODEL,
                    base_url=Config.OLLAMA_BASE_URL,
                    temperature=Config.TEMPERATURE
                )
            else:
                raise ValueError(f"Unknown LLM provider: {Config.LLM_PROVIDER}")
                
        except Exception as e:
            logger.error(f"Error initializing LLM: {str(e)}")
            raise
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """Create prompt template for RAG"""
        system_message = """You are a helpful AI assistant that answers questions based on the provided document context.

Instructions:
1. Answer questions using ONLY the information from the provided context
2. If the context doesn't contain enough information, say so clearly
3. Cite specific documents and page numbers when possible
4. Be concise but comprehensive
5. If asked to compare or synthesize information from multiple sources, do so clearly

Context from documents:
{context}

Remember: Base your answers strictly on the provided context."""

        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])
    
    def chat(self, query: str, chat_history: List[Dict]) -> Tuple[str, List[Dict]]:
        """
        Generate response using RAG
        
        Args:
            query: User question
            chat_history: Previous conversation messages
            
        Returns:
            Tuple of (response, citations)
        """
        try:
            logger.info(f"Processing query: {query}")
            
            # Retrieve relevant documents
            relevant_docs = self.embeddings_manager.search(query, Config.TOP_K)
            
            if not relevant_docs:
                return "I couldn't find any relevant information in the documents to answer your question.", []
            
            # Format context
            context = self._format_context(relevant_docs)
            
            # Format chat history
            formatted_history = self._format_chat_history(chat_history)
            
            # Generate response
            messages = self.prompt_template.format_messages(
                context=context,
                chat_history=formatted_history,
                question=query
            )
            
            response = self.llm.invoke(messages)
            
            # Extract citations
            citations = self._extract_citations(relevant_docs)
            
            logger.info("Response generated successfully")
            return response.content, citations
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
    def _format_context(self, relevant_docs: List[Dict]) -> str:
        """
        Format retrieved documents as context
        
        Args:
            relevant_docs: List of relevant document chunks
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, doc in enumerate(relevant_docs, 1):
            metadata = doc['metadata']
            text = doc['text']
            
            context_parts.append(
                f"[Document {i}]\n"
                f"Source: {metadata['source']}\n"
                f"Page: {metadata['page']}\n"
                f"Content: {text}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def _format_chat_history(self, chat_history: List[Dict]) -> List:
        """
        Format chat history for prompt
        
        Args:
            chat_history: List of message dictionaries
            
        Returns:
            List of LangChain message objects
        """
        formatted = []
        
        # Only include recent history to avoid context overflow
        recent_history = chat_history[-Config.MAX_HISTORY_MESSAGES:]
        
        for msg in recent_history:
            if msg['role'] == 'user':
                formatted.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                formatted.append(AIMessage(content=msg['content']))
        
        return formatted
    
    def _extract_citations(self, relevant_docs: List[Dict]) -> List[Dict]:
        """
        Extract citation information from relevant documents
        
        Args:
            relevant_docs: List of relevant document chunks
            
        Returns:
            List of citation dictionaries
        """
        citations = []
        
        for doc in relevant_docs:
            metadata = doc['metadata']
            citations.append({
                'source': metadata['source'],
                'page': metadata['page'],
                'text': doc['text'],
                'score': doc['score']
            })
        
        return citations
    
    def summarize_document(self, document_name: str) -> str:
        """
        Generate a summary of a specific document
        
        Args:
            document_name: Name of the document to summarize
            
        Returns:
            Summary text
        """
        try:
            # This would require filtering by document name in the vector store
            # For now, return a placeholder
            return f"Summary generation for {document_name} is not yet implemented."
            
        except Exception as e:
            logger.error(f"Error summarizing document: {str(e)}")
            raise
