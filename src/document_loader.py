"""
Document loading and processing utilities
"""

import os
import pickle
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from config.settings import Settings
from src.embeddings import get_embeddings


class DocumentProcessor:
    """Handle document loading and processing"""

    def __init__(self):
        self.chunk_size = Settings.CHUNK_SIZE
        self.chunk_overlap = Settings.CHUNK_OVERLAP
        self.documents_dir = Settings.DOCUMENTS_DIR
        self.vectorstore_path = os.path.join(Settings.VECTORSTORE_DIR, "faiss_index")
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )

    def load_documents(self) -> List:
        """
        Load documents from the documents directory
        
        Returns:
            List of loaded documents
        """
        documents = []
        
        if not os.path.exists(self.documents_dir):
            print(f"Creating documents directory: {self.documents_dir}")
            os.makedirs(self.documents_dir, exist_ok=True)
            return documents

        for file_path in Path(self.documents_dir).glob("**/*"):
            if file_path.is_file():
                if file_path.suffix.lower() == ".pdf":
                    print(f"Loading PDF: {file_path.name}")
                    loader = PyPDFLoader(str(file_path))
                    documents.extend(loader.load())
                elif file_path.suffix.lower() in [".txt", ".md"]:
                    print(f"Loading text: {file_path.name}")
                    loader = TextLoader(str(file_path))
                    documents.extend(loader.load())
        
        print(f"Loaded {len(documents)} documents from {self.documents_dir}")
        return documents

    def split_documents(self, documents: List) -> List:
        """
        Split documents into chunks
        
        Args:
            documents: List of documents
            
        Returns:
            List of split documents (chunks)
        """
        if not documents:
            print("No documents to split")
            return []
        
        chunks = self.text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks (size={self.chunk_size}, overlap={self.chunk_overlap})")
        return chunks

    def create_vectorstore(self, force_recreate: bool = False) -> FAISS:
        """
        Create or load vector store
        
        Args:
            force_recreate: Force recreation of vector store
            
        Returns:
            FAISS vector store
        """
        # Check if vectorstore already exists
        if not force_recreate and os.path.exists(self.vectorstore_path):
            print(f"Loading existing vectorstore from {self.vectorstore_path}")
            embeddings = get_embeddings()
            vectorstore = FAISS.load_local(self.vectorstore_path, embeddings)
            return vectorstore

        # Create new vectorstore
        print("Creating new vectorstore...")
        documents = self.load_documents()
        
        if not documents:
            print("WARNING: No documents found. Creating empty vectorstore.")
            # Create empty vectorstore with sample data
            documents = self._create_sample_docs()
        
        chunks = self.split_documents(documents)
        
        if not chunks:
            raise ValueError("No document chunks created. Please add documents.")
        
        embeddings = get_embeddings()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        
        # Save vectorstore
        os.makedirs(Settings.VECTORSTORE_DIR, exist_ok=True)
        vectorstore.save_local(self.vectorstore_path)
        print(f"Vectorstore saved to {self.vectorstore_path}")
        
        return vectorstore

    @staticmethod
    def _create_sample_docs():
        """Create sample support documents"""
        return [
            {
                "page_content": "Password Reset: To reset your password, go to the login page and click 'Forgot Password'. "
                               "Enter your email address and follow the instructions sent to your inbox. "
                               "The reset link is valid for 24 hours.",
                "metadata": {"source": "sample"}
            },
            {
                "page_content": "Account Settings: You can update your profile information, email, and preferences in the Account Settings page. "
                               "Click on your profile icon in the top right corner and select Settings.",
                "metadata": {"source": "sample"}
            },
            {
                "page_content": "Billing and Subscription: Your current subscription plan can be managed in Billing section. "
                               "You can upgrade, downgrade, or cancel your subscription anytime. "
                               "Changes take effect at the end of the current billing cycle.",
                "metadata": {"source": "sample"}
            },
        ]


def build_vectorstore(force_recreate: bool = False):
    """
    Build or rebuild the vector store
    
    Args:
        force_recreate: Force recreation even if it exists
    """
    processor = DocumentProcessor()
    vectorstore = processor.create_vectorstore(force_recreate=force_recreate)
    print(f"Vectorstore ready with {vectorstore.index.ntotal} embeddings")


if __name__ == "__main__":
    build_vectorstore()
