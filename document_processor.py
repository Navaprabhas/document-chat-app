"""
Document processing module for PDF parsing and text chunking
"""
import logging
from pathlib import Path
from typing import List, Dict, Tuple
import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import Config

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles PDF document processing and text chunking"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def process_pdf(self, file_path: str) -> Tuple[List[str], Dict]:
        """
        Process a PDF file and return chunks with metadata
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Tuple of (chunks, metadata)
        """
        try:
            logger.info(f"Processing PDF: {file_path}")
            
            # Extract text from PDF
            text_by_page = self._extract_text_from_pdf(file_path)
            
            # Create chunks with page tracking
            chunks = []
            metadata = {
                'source': Path(file_path).name,
                'total_pages': len(text_by_page),
                'chunks': []
            }
            
            for page_num, page_text in enumerate(text_by_page, start=1):
                if not page_text.strip():
                    continue
                
                # Split page text into chunks
                page_chunks = self.text_splitter.split_text(page_text)
                
                for chunk_idx, chunk in enumerate(page_chunks):
                    chunks.append(chunk)
                    metadata['chunks'].append({
                        'page': page_num,
                        'chunk_index': chunk_idx,
                        'source': Path(file_path).name
                    })
            
            logger.info(f"Created {len(chunks)} chunks from {len(text_by_page)} pages")
            return chunks, metadata
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            raise
    
    def _extract_text_from_pdf(self, file_path: str) -> List[str]:
        """
        Extract text from PDF file page by page
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of text strings, one per page
        """
        text_by_page = []
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    # Clean up text
                    text = self._clean_text(text)
                    text_by_page.append(text)
                    
            return text_by_page
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text
        
        Args:
            text: Raw text from PDF
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove special characters that might cause issues
        text = text.replace('\x00', '')
        
        return text
    
    def get_document_stats(self, file_path: str) -> Dict:
        """
        Get statistics about a PDF document
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary with document statistics
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                total_pages = len(pdf_reader.pages)
                total_chars = 0
                
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    total_chars += len(text)
                
                return {
                    'total_pages': total_pages,
                    'total_characters': total_chars,
                    'avg_chars_per_page': total_chars // total_pages if total_pages > 0 else 0
                }
                
        except Exception as e:
            logger.error(f"Error getting document stats: {str(e)}")
            return {}
