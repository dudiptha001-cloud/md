# Development Guide

## Project Architecture

### Core Components

```
┌─────────────────┐
│   Streamlit UI  │ (app.py)
└────────┬────────┘
         │
    ┌────▼─────┐
    │ SupportAgent (RAG Chain)
    ├───────────┤
    │ - LLM     │──► OpenAI/Azure
    │ - Retriever
    │ - Memory
    └────┬──────┘
         │
    ┌────▼─────────────┐
    │ FAISS VectorStore│
    └────┬─────────────┘
         │
    ┌────▼──────────────┐
    │ Document Embeddings
    │ (OpenAI Embeddings)
    └─────────────────┘
```

### Data Flow

1. **Document Processing**
   - Load documents from `data/documents/`
   - Split into chunks (default: 1000 tokens)
   - Generate embeddings using OpenAI API
   - Store in FAISS vector database

2. **Query Processing**
   - User submits question via Streamlit UI
   - Generate question embedding
   - Similarity search in FAISS (retrieve top-k)
   - Format context from retrieved documents
   - Send to LLM with context + prompt
   - Return answer + source attribution

3. **Response Generation**
   - LLM generates answer grounded in document context
   - Confidence calculated from number of sources
   - Sources formatted with excerpts
   - Stored in conversation history

## Key Files

### `src/agent.py`
Main RAG agent implementation:
- `SupportAgent` class
- Query handling with RetrievalQA
- Conversation history management
- Confidence scoring

### `src/document_loader.py`
Document processing pipeline:
- `DocumentProcessor` class
- PDF and text file loading
- Document chunking
- Vector store creation/loading

### `config/settings.py`
Configuration management:
- Environment variable loading
- Model and embedding settings
- Path configuration
- Validation

### `app.py`
Streamlit web interface:
- Chat UI
- Document upload
- Settings panel
- Conversation management

## Development Workflow

### Local Testing
```bash
# Start development server
streamlit run app.py

# Or test agent directly
python -c "
from src.agent import SupportAgent
agent = SupportAgent()
print(agent.query('test question')['answer'])
"
```

### Document Testing
```bash
# Test document loading and processing
python src/document_loader.py

# Test agent with documents
python notebooks/getting_started.py
```

### Debugging

Enable debug mode in `.env`:
```
DEBUG=True
```

Then view debug output:
```python
from config.settings import Settings
if Settings.DEBUG:
    print("Debug info...")
```

## Customization

### Modify the Prompt
Edit `src/agent.py`, function `_build_qa_chain()`:
```python
template = """Your custom prompt here
...
{context}
...
{question}
"""
```

### Change LLM Model
Edit `config/settings.py`:
```python
MODEL_NAME = "gpt-3.5-turbo"  # or other models
```

### Adjust Chunk Size
For more accurate retrieval, reduce chunk size:
```python
CHUNK_SIZE = 500  # Smaller = more precise
CHUNK_OVERLAP = 100
```

### Change Embedding Model
Edit `config/settings.py`:
```python
EMBEDDING_MODEL = "text-embedding-3-large"  # More powerful
```

## Performance Optimization

### Speed
- Reduce `TOP_K` (retrieval count)
- Use smaller chunk size
- Cache embeddings
- Use cheaper embedding model

### Accuracy
- Increase `TOP_K`
- Reduce chunk size for precision
- Fine-tune prompt template
- Add domain-specific examples

### Cost
- Use GPT-3.5-turbo instead of GPT-4
- Reduce document chunk overlap
- Cache vectorstore locally
- Batch queries

## Testing

### Unit Tests
Create `tests/test_agent.py`:
```python
from src.agent import SupportAgent

def test_query():
    agent = SupportAgent()
    response = agent.query("test")
    assert "answer" in response
    assert "sources" in response
```

### Integration Tests
Test full pipeline:
```bash
python notebooks/getting_started.py
```

## Deployment

### Local Deployment
```bash
streamlit run app.py
```

### Cloud Deployment

**Heroku:**
```bash
heroku login
heroku create
git push heroku main
```

**Azure:**
```bash
az web app up --name <app-name>
```

**AWS:**
Use Elastic Beanstalk or Lambda

## Monitoring

Track performance:
- Response time
- Query count
- Accuracy metrics
- User satisfaction

Log queries:
```python
# In agent.py
self.conversation_history.append({
    "timestamp": datetime.now(),
    "query": question,
    "response_time": elapsed,
    "model_used": self.llm.model_name,
})
```

## Troubleshooting Development

### Import Errors
```bash
# Reinstall in development mode
pip install -e .
```

### Cache Issues
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### Vectorstore Issues
```bash
# Rebuild vectorstore
python -c "
from src.document_loader import DocumentProcessor
proc = DocumentProcessor()
proc.create_vectorstore(force_recreate=True)
"
```

## Best Practices

1. **Document Management**
   - Use clear, structured documents
   - Include metadata in files
   - Keep documents up-to-date
   - Version control documents

2. **Prompt Engineering**
   - Be specific in instructions
   - Include examples
   - Define output format
   - Test variations

3. **Monitoring**
   - Track failed queries
   - Monitor response times
   - Collect user feedback
   - Measure accuracy

4. **Security**
   - Never commit API keys
   - Use environment variables
   - Validate user input
   - Log sensitive operations

## Contributing

When adding features:
1. Create feature branch
2. Write tests
3. Update documentation
4. Submit pull request

## Resources

- [LangChain Docs](https://python.langchain.com)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Streamlit Docs](https://docs.streamlit.io)
