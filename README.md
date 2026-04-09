# Customer Support Agent - End-to-End Pipeline

A comprehensive customer support agent built with LangChain, OpenAI/Azure OpenAI, and FAISS vector databases.

## Features

- **RAG Pipeline**: Retrieval-Augmented Generation for accurate, document-grounded responses
- **Multi-Provider Support**: Works with both OpenAI and Azure OpenAI
- **Vector Database**: FAISS for efficient similarity search
- **Web Interface**: Streamlit-based UI for easy interaction
- **Document Processing**: Automatic chunking and embedding of support documents
- **Conversation Memory**: Context-aware responses with chat history

## Tech Stack

- **LangChain**: LLM orchestration and RAG
- **OpenAI/Azure OpenAI**: Language models
- **FAISS**: Vector similarity search
- **Streamlit**: Web interface
- **Python 3.8+**: Core language

## Project Structure

```
├── data/                    # Document storage
│   ├── documents/          # Support documents
│   └── vectorstore/        # FAISS vector database
├── src/                    # Source code
│   ├── agent.py           # Core agent logic
│   ├── embeddings.py      # Embedding utilities
│   ├── document_loader.py # Document processing
│   └── utils.py           # Helper functions
├── config/                 # Configuration files
│   └── settings.py        # Application settings
├── notebooks/             # Jupyter notebooks
├── app.py                 # Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- API key from OpenAI or Azure OpenAI

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 4. Prepare Documents
Place your support documents (PDF, TXT) in `data/documents/`

### 5. Build Vector Store
```bash
python src/document_loader.py
```

### 6. Run the Agent
```bash
streamlit run app.py
```

## Usage

### In Streamlit UI
1. Open the application in your browser
2. Type your customer support question
3. The agent retrieves relevant documents and generates a response
4. View sources and conversation history

### Programmatic Usage
```python
from src.agent import SupportAgent

agent = SupportAgent()
response = agent.query("How do I reset my password?")
print(response["answer"])
print(response["sources"])
```

## Configuration

Edit `config/settings.py` to customize:
- Model parameters
- Chunk size and overlap
- Number of retrieved documents
- Temperature and other LLM settings

## API Keys

### OpenAI
1. Get key from https://platform.openai.com/api-keys
2. Set `OPENAI_API_KEY` in `.env`

### Azure OpenAI
1. Deploy in Azure and get credentials
2. Set `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` in `.env`

## Performance Tips

- Use smaller chunk sizes for more precise retrieval
- Increase `top_k` for more context but slower responses
- Cache embeddings to avoid reprocessing
- Use async calls for multiple queries

## Troubleshooting

**Q: "No valid API key" error**
- Verify `.env` file is configured correctly
- Check API key is not expired

**Q: Vector store not found**
- Run `python src/document_loader.py` to generate embeddings

**Q: Slow responses**
- Reduce chunk size or number of documents retrieved
- Use faster embedding models

## Next Steps

- Integrate with customer database
- Add conversation logging
- Deploy to cloud (Azure, AWS)
- Fine-tune models on domain data
- Add feedback mechanisms

## License

MIT

## Support

For issues or questions, refer to the documentation or create an issue in the repository.
