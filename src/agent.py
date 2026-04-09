"""
Core agent logic for customer support using RAG
"""

import os
from typing import Dict, List, Any

from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config.settings import Settings
from src.embeddings import get_embeddings
from src.document_loader import DocumentProcessor


class SupportAgent:
    """Customer support agent using Retrieval-Augmented Generation (RAG)"""

    def __init__(self, use_azure: bool = None):
        """
        Initialize the support agent
        
        Args:
            use_azure: Use Azure OpenAI if True, OpenAI if False, auto-detect if None
        """
        Settings.validate()
        
        # Auto-detect if not specified
        if use_azure is None:
            use_azure = bool(Settings.AZURE_OPENAI_API_KEY)
        
        self.use_azure = use_azure
        self.demo_mode = Settings.DEMO_MODE
        
        # In demo mode, skip vectorstore and LLM initialization
        if self.demo_mode:
            self.llm = None
            self.qa_chain = None
            self.vectorstore = None
        else:
            self.vectorstore = self._load_vectorstore()
            self.llm = self._get_llm()
            self.qa_chain = self._build_qa_chain()
        
        self.conversation_history = []

    def _get_llm(self):
        """Initialize LLM"""
        # Check if Azure OpenAI config is valid
        has_valid_azure = (
            Settings.AZURE_OPENAI_API_KEY 
            and not Settings.AZURE_OPENAI_API_KEY.startswith("your_")
            and Settings.AZURE_OPENAI_ENDPOINT
            and not Settings.AZURE_OPENAI_ENDPOINT.startswith("your_")
        )
        
        if has_valid_azure:
            return AzureChatOpenAI(
                api_key=Settings.AZURE_OPENAI_API_KEY,
                azure_endpoint=Settings.AZURE_OPENAI_ENDPOINT,
                api_version=Settings.AZURE_OPENAI_API_VERSION,
                model=Settings.MODEL_NAME,
                temperature=Settings.TEMPERATURE,
            )
        else:
            return ChatOpenAI(
                api_key=Settings.OPENAI_API_KEY,
                model=Settings.MODEL_NAME,
                temperature=Settings.TEMPERATURE,
            )

    def _load_vectorstore(self) -> FAISS:
        """Load or create vector store"""
        processor = DocumentProcessor()
        return processor.create_vectorstore()

    def _build_qa_chain(self):
        """Build the RAG chain using modern LangChain API"""
        
        # Custom prompt template
        template = """You are a helpful customer support assistant. 
Use the following pieces of context to answer the question at the end. 
If you don't know the answer based on the provided context, say "I don't have that information in my knowledge base."

Context:
{context}

Question: {question}

Helpful Answer:"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

        # Create retriever
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": Settings.TOP_K}
        )

        # Build RAG chain using modern API
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Store original docs for sources
        self.retrieved_docs = []
        
        def retrieve_and_store(query):
            docs = retriever.invoke(query)
            self.retrieved_docs = docs
            return format_docs(docs)

        chain = (
            {
                "context": lambda x: retrieve_and_store(x.get("query", "")),
                "question": lambda x: x.get("query", "")
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain, retriever

    def query(self, question: str) -> Dict[str, Any]:
        """
        Process a customer query
        
        Args:
            question: Customer's question
            
        Returns:
            Dictionary with answer and source documents
        """
        if self.demo_mode:
            return self._demo_query(question)
        
        # Invoke chain
        chain, retriever = self.qa_chain
        answer = chain.invoke({"query": question})
        
        # Get source documents
        source_docs = retriever.invoke(question)
        
        # Format sources
        sources = []
        for doc in source_docs:
            sources.append({
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", 0)
            })
        
        # Store in history
        self.conversation_history.append({
            "question": question,
            "answer": answer,
            "sources": sources
        })
        
        # Keep only last N items
        if len(self.conversation_history) > Settings.MAX_HISTORY:
            self.conversation_history = self.conversation_history[-Settings.MAX_HISTORY:]
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": self._calculate_confidence(source_docs)
        }

    def _calculate_confidence(self, source_docs: List) -> float:
        """
        Calculate confidence based on number of sources
        
        Args:
            source_docs: Retrieved source documents
            
        Returns:
            Confidence score between 0 and 1
        """
        # Simple heuristic: more sources = higher confidence
        return min(len(source_docs) / Settings.TOP_K, 1.0)

    def _demo_query(self, question: str) -> Dict[str, Any]:
        """
        Demo mode query with hardcoded responses
        
        Args:
            question: Customer's question
            
        Returns:
            Dictionary with demo answer and sources
        """
        # Demo responses based on keywords
        demo_responses = {
            "password": (
                "To reset your password:\n"
                "1. Go to the login page\n"
                "2. Click 'Forgot Password'\n"
                "3. Enter your email address\n"
                "4. Check your email for a reset link (valid for 24 hours)\n"
                "5. Follow the link to set a new password",
                "Password Reset Guide"
            ),
            "email": (
                "To change your email address:\n"
                "1. Log in to your account\n"
                "2. Go to Account Settings\n"
                "3. Click 'Change Email'\n"
                "4. Enter your new email\n"
                "5. Verify through the confirmation link sent to your new email",
                "Email Change Guide"
            ),
            "subscription": (
                "We offer three subscription plans:\n"
                "- Free: Basic features (limited support)\n"
                "- Pro: Advanced features ($9.99/month)\n"
                "- Enterprise: Custom features (contact sales)\n\n"
                "To change plans, go to Billing Settings and select 'Change Plan'.",
                "Subscription Plans"
            ),
            "billing": (
                "We accept the following payment methods:\n"
                "- Credit cards (Visa, Mastercard, Amex)\n"
                "- Debit cards\n"
                "- PayPal\n"
                "- Wire transfer (Enterprise only)\n\n"
                "You can view invoices in Billing Settings under 'Invoices'.",
                "Billing & Payment"
            ),
            "2fa": (
                "To enable Two-Factor Authentication:\n"
                "1. Go to Account Settings\n"
                "2. Click 'Security'\n"
                "3. Enable 'Two-Factor Authentication'\n"
                "4. Choose SMS or authenticator app\n"
                "5. Follow the setup instructions",
                "Security & 2FA"
            ),
            "export": (
                "To export your data:\n"
                "1. Go to Account Settings\n"
                "2. Click 'Data & Privacy'\n"
                "3. Select 'Export My Data'\n"
                "4. Choose format (CSV or JSON)\n"
                "5. Download your data from the email link",
                "Data Export"
            ),
        }
        
        # Find best matching response
        question_lower = question.lower()
        answer_text = "I'm running in demo mode. Here's sample information:\n\n"
        source_title = "Demo Response"
        
        for keyword, (response, title) in demo_responses.items():
            if keyword in question_lower:
                answer_text = response
                source_title = title
                break
        else:
            # Default response
            answer_text = (
                "Thank you for your question! I'm currently in demo mode without API keys configured.\n\n"
                "Try asking about:\n"
                "- Password reset\n"
                "- Email change\n"
                "- Subscription plans\n"
                "- Billing information\n"
                "- Two-factor authentication\n"
                "- Data export\n\n"
                "To use real AI responses, configure your API key in the .env file and set DEMO_MODE=False"
            )
        
        sources = [{
            "content": answer_text[:150] + "...",
            "source": source_title,
            "page": 0
        }]
        
        # Store in history
        self.conversation_history.append({
            "question": question,
            "answer": answer_text,
            "sources": sources
        })
        
        # Keep only last N items
        if len(self.conversation_history) > Settings.MAX_HISTORY:
            self.conversation_history = self.conversation_history[-Settings.MAX_HISTORY:]
        
        return {
            "answer": answer_text,
            "sources": sources,
            "confidence": 0.8  # Demo confidence
        }

    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history.copy()

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def rebuild_vectorstore(self):
        """Rebuild the vector store from documents"""
        if self.demo_mode or not self.qa_chain:
            # In demo mode, don't actually rebuild
            return
        
        processor = DocumentProcessor()
        self.vectorstore = processor.create_vectorstore(force_recreate=True)
        # Rebuild QA chain with new vectorstore
        self.qa_chain = self._build_qa_chain()


# Example usage
if __name__ == "__main__":
    # Initialize agent
    agent = SupportAgent()
    
    # Query examples
    test_queries = [
        "How do I reset my password?",
        "How can I change my email?",
        "What's my current subscription plan?",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Q: {query}")
        print(f"{'='*60}")
        
        result = agent.query(query)
        print(f"A: {result['answer']}")
        print(f"\nConfidence: {result['confidence']:.2%}")
        print(f"Sources: {len(result['sources'])} documents")
        for i, source in enumerate(result['sources'], 1):
            print(f"  {i}. {source['source']} - {source['content']}")
