"""
Streamlit web interface for Customer Support Agent
"""

import streamlit as st
from datetime import datetime
import os
from src.agent import SupportAgent
from src.document_loader import DocumentProcessor
from src.utils import format_response, get_document_stats
from config.settings import Settings


# Page configuration
st.set_page_config(
    page_title="Customer Support Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stChat {
        max-width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state"""
    if "agent" not in st.session_state:
        st.session_state.agent = None
        st.session_state.agent_error = None
        st.session_state.agent_init_attempted = False
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "show_sources" not in st.session_state:
        st.session_state.show_sources = True
    
    # In demo mode, try to initialize agent immediately (it won't call API)
    if Settings.get_demo_mode() and st.session_state.agent is None and not st.session_state.agent_init_attempted:
        try:
            st.session_state.agent = SupportAgent()
            st.session_state.agent_init_attempted = True
        except Exception as e:
            # In demo mode, this shouldn't fail, but just in case
            st.session_state.agent_error = None
            st.session_state.agent_init_attempted = True


def get_agent():
    """Lazy initialize and return the agent"""
    # If in demo mode, don't try to load real agent
    if Settings.get_demo_mode():
        if st.session_state.agent is None:
            st.session_state.agent = SupportAgent()
        return st.session_state.agent
    
    if st.session_state.agent is not None:
        return st.session_state.agent
    
    if st.session_state.agent_init_attempted:
        return None
    
    st.session_state.agent_init_attempted = True
    
    try:
        # Try to initialize agent
        st.session_state.agent = SupportAgent()
        return st.session_state.agent
    except Exception as e:
        st.session_state.agent_error = str(e)
        return None


def main():
    """Main Streamlit application"""
    
    # Initialize
    initialize_session_state()
    
    # Check API configuration
    api_key_configured = Settings.has_valid_api_key()
    demo_mode = Settings.get_demo_mode()
    
    # Header
    st.title("Customer Support Agent")
    st.markdown("_Powered by LangChain, OpenAI, and FAISS_")
    
    # Show demo mode banner
    if demo_mode and not api_key_configured:
        st.info(
            "**Demo Mode Enabled**\n\n"
            "You're viewing demo responses. To use real AI:\n"
            "1. Get API key from https://platform.openai.com/api-keys\n"
            "2. Update `.env` with: `OPENAI_API_KEY=sk-...`\n"
            "3. Set: `DEMO_MODE=False`\n"
            "4. Restart the app"
        )
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # API Status
        st.success("API Key Configured")
        
        # Stats
        st.subheader("System Status")
        stats = get_document_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Documents", stats["total_documents"])
        with col2:
            st.metric("Vectorstore", "Ready" if stats["vectorstore_exists"] else "Empty")
        
        # Settings
        st.subheader("Settings")
        show_sources = st.checkbox("Show Sources", value=True)
        st.session_state.show_sources = show_sources
        
        if demo_mode:
            st.info("Running in Demo Mode - AI responses disabled")
        
        # Agent controls
        agent = get_agent()
        if agent:
            # Clear history button
            if st.button("Clear History"):
                st.session_state.conversation_history = []
                agent.clear_history()
                st.success("Conversation history cleared!")
            
            # Rebuild vectorstore button (only if not in demo mode)
            if not demo_mode:
                if st.button("Rebuild Vectorstore"):
                    with st.spinner("Rebuilding vectorstore..."):
                        agent.rebuild_vectorstore()
                    st.success("Vectorstore rebuilt!")
        elif st.session_state.agent_error and not demo_mode:
            st.error(f"**Agent Error:**\n{st.session_state.agent_error}")
            st.info(
                "Tip: Set `DEMO_MODE=True` in .env to test without API keys"
            )
        
        # Upload documents
        st.subheader("Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload support documents (PDF, TXT)",
            type=["pdf", "txt"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            try:
                docs_dir = "data/documents"
                os.makedirs(docs_dir, exist_ok=True)
                for uploaded_file in uploaded_files:
                    # Save file
                    file_path = f"{docs_dir}/{uploaded_file.name}"
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.read())
                    st.success(f"Saved {uploaded_file.name}")
                
                # Rebuild vectorstore with new documents
                if st.button("Build Vector Store with New Documents"):
                    agent = get_agent()
                    if agent:
                        with st.spinner("Processing documents and building vectorstore..."):
                            agent.rebuild_vectorstore()
                        st.success("Vector store ready!")
                    else:
                        st.error("Agent not initialized. Check API keys.")
            except Exception as e:
                st.error(f"Error uploading files: {str(e)}")
    
    # Main chat interface
    st.header("Chat")
    
    # Check if agent is ready
    agent = get_agent()
    if not agent:
        if st.session_state.agent_error:
            st.error(
                f"**Failed to initialize agent:**\n\n{st.session_state.agent_error}\n\n"
                "**Solutions:**\n"
                "1. Ensure `.env` file exists with API keys\n"
                "2. Verify OPENAI_API_KEY or AZURE_OPENAI_API_KEY is set\n"
                "3. Check that your API key is valid\n"
                "4. Restart the app after updating `.env`"
            )
        else:
            st.info("Loading agent... Please wait.")
        return
    
    # Display conversation history
    if st.session_state.conversation_history:
        for i, item in enumerate(st.session_state.conversation_history):
            # Question
            with st.chat_message("user"):
                st.write(item["question"])
            
            # Answer
            with st.chat_message("assistant"):
                st.write(item["answer"])
                
                # Confidence
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(f"Confidence: {item.get('confidence', 0):.1%}")
                
                # Sources
                if st.session_state.show_sources and item.get("sources"):
                    with st.expander(f"Sources ({len(item['sources'])})"):
                        for j, source in enumerate(item["sources"], 1):
                            st.markdown(f"**Source {j}:** {source['source']}")
                            st.caption(source['content'])
    
    # Input area
    st.divider()
    
    # User input
    user_query = st.text_input(
        "Ask your question:",
        placeholder="e.g., How do I reset my password?",
        key="user_input"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("Send", use_container_width=True, type="primary"):
            if user_query:
                with st.spinner("Thinking..."):
                    try:
                        response = agent.query(user_query)
                        
                        # Add to history
                        st.session_state.conversation_history.append({
                            "question": user_query,
                            "answer": response["answer"],
                            "sources": response["sources"],
                            "confidence": response["confidence"],
                            "timestamp": datetime.now().isoformat()
                        })
                        
                        # Rerun to display the response
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error processing query: {str(e)}")
            else:
                st.warning("Please enter a question!")
    
    with col2:
        if st.button("Save", use_container_width=True):
            if st.session_state.conversation_history:
                from src.utils import save_conversation
                filepath = save_conversation(st.session_state.conversation_history)
                st.success(f"Saved to {filepath}")
            else:
                st.info("No conversation to save")
    
    with col3:
        if st.button("Export", use_container_width=True):
            if st.session_state.conversation_history:
                import json
                export_data = json.dumps(st.session_state.conversation_history, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=export_data,
                    file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.info("No conversation to export")


if __name__ == "__main__":
    main()
