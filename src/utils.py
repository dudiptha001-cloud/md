"""
Utility functions for the customer support agent
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any


def save_conversation(conversation: List[Dict], filename: str = None) -> str:
    """
    Save conversation history to a JSON file
    
    Args:
        conversation: Conversation history
        filename: Optional filename (default: timestamp-based)
        
    Returns:
        Path to saved file
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
    
    filepath = os.path.join("data", "conversations", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w") as f:
        json.dump(conversation, f, indent=2)
    
    return filepath


def load_conversation(filepath: str) -> List[Dict]:
    """
    Load conversation from a JSON file
    
    Args:
        filepath: Path to conversation file
        
    Returns:
        Conversation history
    """
    with open(filepath, "r") as f:
        return json.load(f)


def format_response(response: Dict[str, Any]) -> str:
    """
    Format response for display
    
    Args:
        response: Response from agent
        
    Returns:
        Formatted string
    """
    output = f"\n{'='*60}\n"
    output += f"Answer:\n{response['answer']}\n\n"
    output += f"Confidence: {response['confidence']:.1%}\n\n"
    
    if response['sources']:
        output += f"Sources ({len(response['sources'])}):\n"
        for i, source in enumerate(response['sources'], 1):
            output += f"  {i}. {source['source']}\n"
            output += f"     {source['content']}\n"
    
    output += f"{'='*60}\n"
    return output


def get_document_stats() -> Dict[str, Any]:
    """
    Get statistics about loaded documents
    
    Returns:
        Document statistics
    """
    stats = {
        "total_documents": 0,
        "total_chunks": 0,
        "vectorstore_exists": False,
        "vectorstore_size": 0,
    }
    
    # Check documents
    documents_dir = "data/documents"
    if os.path.exists(documents_dir):
        stats["total_documents"] = len(os.listdir(documents_dir))
    
    # Check vectorstore
    vectorstore_path = "data/vectorstore/faiss_index"
    if os.path.exists(vectorstore_path):
        stats["vectorstore_exists"] = True
        # Estimate size in bytes
        stats["vectorstore_size"] = sum(
            os.path.getsize(os.path.join(vectorstore_path, f))
            for f in os.listdir(vectorstore_path)
            if os.path.isfile(os.path.join(vectorstore_path, f))
        )
    
    return stats
