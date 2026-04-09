# Quick Start Guide

## Installation (5 minutes)

### 1. Clone or navigate to project
```bash
cd "Customer Support Agent — End-to-End Pipeline"
```

### 2. Create virtual environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API keys
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=sk-...
# or
# AZURE_OPENAI_API_KEY=...
# AZURE_OPENAI_ENDPOINT=...
```

## Running the Agent

### Option A: Streamlit Web UI (Recommended)
```bash
streamlit run app.py
```
Opens at http://localhost:8501

### Option B: Command Line Testing
```bash
python notebooks/getting_started.py
```

### Option C: Python Script
```python
from src.agent import SupportAgent

agent = SupportAgent()
response = agent.query("How do I reset my password?")
print(response["answer"])
```

## File Structure

```
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # Full documentation
├── QUICKSTART.md             # This file
│
├── config/
│   ├── settings.py           # Application settings
│   └── __init__.py
│
├── src/
│   ├── agent.py              # Core RAG agent
│   ├── document_loader.py    # Document processing
│   ├── embeddings.py         # Embedding utilities
│   ├── utils.py              # Helper functions
│   └── __init__.py
│
├── data/
│   ├── documents/            # Place your support documents here
│   │   └── support_knowledge_base.txt  # Sample document
│   └── vectorstore/          # FAISS vector store (auto-generated)
│
└── notebooks/
    └── getting_started.py    # Testing notebook
```

## Configuration

### Environment Variables
See `.env.example` for all available options:

- `OPENAI_API_KEY` - OpenAI API key
- `AZURE_OPENAI_API_KEY` - Azure OpenAI API key  
- `AZURE_OPENAI_ENDPOINT` - Azure OpenAI endpoint
- `MODEL_NAME` - LLM model (default: gpt-4)
- `TEMPERATURE` - Response creativity (0-1, default: 0.1)
- `CHUNK_SIZE` - Document chunk size (default: 1000)
- `TOP_K` - Number of retrieved documents (default: 5)

### Python Settings
Edit `config/settings.py` to customize chunk sizes, model parameters, etc.

## Adding Your Documents

### Step 1: Prepare Documents
Place support documents in `data/documents/`:
- PDF files (.pdf)
- Text files (.txt)
- Markdown files (.md)

### Step 2: Build Vector Store
```bash
python src/document_loader.py
```

### Step 3: Use in Agent
The agent automatically uses the updated vector store.

## Troubleshooting

#### "API Key Error"
- Verify `.env` file exists and has correct keys
- Check API key is not expired
- Try both OpenAI and Azure options

#### "No documents found"
- Add files to `data/documents/`
- Run `python src/document_loader.py`
- Check file formatting (PDF/TXT)

#### "Slow responses"
- Reduce `TOP_K` in settings
- Use smaller `CHUNK_SIZE`
- Consider using smaller model

#### "FAISS not found"
- Run: `pip install faiss-cpu`
- Or CPU version: `pip install faiss-cpu==1.7.4`

## Next Steps

1. **Add Documents**: Place your support knowledge base in `data/documents/`
2. **Build Vector Store**: Run document processor to create embeddings
3. **Test Queries**: Use Streamlit UI or command line to test
4. **Customize Prompts**: Edit prompt template in `src/agent.py`
5. **Deploy**: Run on cloud platform (Heroku, Azure, AWS, etc.)

## Features Used

✅ Retrieval-Augmented Generation (RAG)
✅ Vector embeddings with FAISS
✅ LangChain chains and retrievers
✅ Multi-provider LLM support
✅ Conversation history tracking
✅ Source document attribution
✅ Confidence scoring
✅ Web UI with Streamlit

## Support

For issues:
1. Check troubleshooting section above
2. Review full README.md
3. Check LangChain docs at https://python.langchain.com
4. Check OpenAI docs at https://platform.openai.com/docs
