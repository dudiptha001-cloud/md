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
    azure_key = Settings.get_azure_api_key()
    azure_endpoint = Settings.get_azure_endpoint()
    
    has_valid_azure = (
        azure_key 
        and not azure_key.startswith("your_")
        and azure_endpoint
        and not azure_endpoint.startswith("your_")
    )
    
    if has_valid_azure:
        return AzureOpenAIEmbeddings(
            api_key=azure_key,
            azure_endpoint=azure_endpoint,
            api_version=Settings.AZURE_OPENAI_API_VERSION,
            model=Settings.EMBEDDING_MODEL,
        )
    else:
        openai_key = Settings.get_openai_api_key()
        return OpenAIEmbeddings(
            api_key=openai_key,
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
