"""
Embedding utilities for document and query processing
"""

from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from config.settings import Settings


def get_embeddings():
    """
    Get embeddings model based on configuration
    
    Returns:
        OpenAIEmbeddings or AzureOpenAIEmbeddings
    """
    # Check if Azure OpenAI config is valid
    has_valid_azure = (
        Settings.AZURE_OPENAI_API_KEY 
        and not Settings.AZURE_OPENAI_API_KEY.startswith("your_")
        and Settings.AZURE_OPENAI_ENDPOINT
        and not Settings.AZURE_OPENAI_ENDPOINT.startswith("your_")
    )
    
    if has_valid_azure:
        return AzureOpenAIEmbeddings(
            api_key=Settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=Settings.AZURE_OPENAI_ENDPOINT,
            api_version=Settings.AZURE_OPENAI_API_VERSION,
            model=Settings.EMBEDDING_MODEL,
        )
    else:
        return OpenAIEmbeddings(
            api_key=Settings.OPENAI_API_KEY,
            model=Settings.EMBEDDING_MODEL,
        )


def embed_query(query: str):
    """
    Embed a single query
    
    Args:
        query: Text query to embed
        
    Returns:
        Query embedding vector
    """
    embeddings = get_embeddings()
    return embeddings.embed_query(query)


def embed_documents(documents: list):
    """
    Embed multiple documents
    
    Args:
        documents: List of document texts
        
    Returns:
        List of document embeddings
    """
    embeddings = get_embeddings()
    return embeddings.embed_documents(documents)
