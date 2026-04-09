"""
Customer Support Agent - Getting Started Notebook

This notebook demonstrates how to use the Customer Support Agent.
"""

import sys
from src.agent import SupportAgent
from src.document_loader import DocumentProcessor
from src.utils import format_response, get_document_stats


def test_basic_queries():
    """Test agent with basic queries"""
    print("="*60)
    print("INITIALIZING AGENT")
    print("="*60)
    
    # Initialize agent (this will create vectorstore if needed)
    agent = SupportAgent()
    
    print("\n" + "="*60)
    print("TESTING QUERIES")
    print("="*60)
    
    test_queries = [
        "How do I reset my password?",
        "What subscription plans do you offer?",
        "How can I export my data?",
        "Is two-factor authentication available?",
        "What are your payment methods?",
    ]
    
    for query in test_queries:
        print(f"\nQ: {query}")
        response = agent.query(query)
        print(format_response(response))


def test_vectorstore():
    """Test vector store creation and loading"""
    print("="*60)
    print("VECTORSTORE TEST")
    print("="*60)
    
    processor = DocumentProcessor()
    
    # Get document stats
    stats = get_document_stats()
    print(f"\nDocuments found: {stats['total_documents']}")
    print(f"Vectorstore exists: {stats['vectorstore_exists']}")
    print(f"Vectorstore size: {stats['vectorstore_size']} bytes")
    
    # Load documents
    documents = processor.load_documents()
    print(f"\nLoaded {len(documents)} documents")
    
    # Split documents
    chunks = processor.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    
    # Create vectorstore
    vectorstore = processor.create_vectorstore()
    print(f"Vectorstore has {vectorstore.index.ntotal} embeddings")


def test_conversation_history():
    """Test conversation history"""
    print("="*60)
    print("CONVERSATION HISTORY TEST")
    print("="*60)
    
    agent = SupportAgent()
    
    # Make a few queries
    queries = ["How do I reset my password?", "What plans do you offer?"]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = agent.query(query)
        print(f"Answer: {response['answer'][:100]}...")
    
    # Show history
    history = agent.get_history()
    print(f"\n\nConversation History ({len(history)} items):")
    for i, item in enumerate(history, 1):
        print(f"{i}. Q: {item['question']}")
        print(f"   A: {item['answer'][:80]}...")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("CUSTOMER SUPPORT AGENT - TESTING")
    print("="*60 + "\n")
    
    # Test 1: Vectorstore
    test_vectorstore()
    
    # Test 2: Basic queries
    test_basic_queries()
    
    # Test 3: Conversation history
    test_conversation_history()
    
    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Add your support documents to data/documents/")
    print("2. Run: python src/document_loader.py")
    print("3. Run: streamlit run app.py")
