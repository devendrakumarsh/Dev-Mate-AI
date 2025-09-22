# 🤖 Dev-Mate-AI: Intelligent Code Documentation Assistant

A powerful Retrieval-Augmented Generation (RAG) application that helps developers understand API documentation and **automatically generates clean documentation** for code files using **free Hugging Face models**.

## 🚀 Features

- **📤 Document Upload**: Support for multiple file formats (TXT, MD, PDF, DOCX, PY, JS, JAVA, etc.)
- **⚡ Instant Documentation**: Automatically generates clean documentation for uploaded code files
- **🧠 Intelligent Chunking**: Smart text segmentation with overlap for better context
- **🔍 Vector Storage**: ChromaDB for efficient similarity search
- **🤖 RAG Pipeline**: Combines retrieval and generation for accurate responses
- **🌐 Web Interface**: User-friendly Streamlit interface
- **💬 Real-time Chat**: Interactive Q&A with your API documentation
- **📊 Source Attribution**: Shows which documents were used for each answer
- **🎯 Confidence Scoring**: Indicates reliability of responses
- **🆓 Free Models**: Uses Hugging Face models - no API keys required!

## 📋 Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)
- **No API keys required** - uses free Hugging Face models locally!

## 🛠️ Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd Dev-Mate-AI
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional: Set up environment variables for customization:**
   ```bash
   # Create .env file for custom settings (optional)
   # EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   # CODE_DOCUMENTATION_MODEL=Salesforce/codet5-small
   # ENABLE_INSTANT_DOCUMENTATION=true
   ```

## 🔧 Configuration

Create a `.env` file for custom settings (optional):

```env
# Application Configuration
APP_TITLE=Dev-Mate-AI Documentation Assistant
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TEMPERATURE=0.7
MAX_TOKENS=1500

# Hugging Face Models (Free)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHAT_MODEL=microsoft/DialoGPT-medium
CODE_DOCUMENTATION_MODEL=Salesforce/codet5-small

# Code Documentation Settings
ENABLE_INSTANT_DOCUMENTATION=true
MAX_CODE_LENGTH=10000

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
COLLECTION_NAME=api_docs
```

## 🚀 Usage

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**
   The application will automatically open at `http://localhost:8501`

3. **Upload Files:**
   - Go to the "📤 Upload API Documentation & Code Files" section
   - Upload your API documentation files OR code files
   - Choose your action:
     - **📚 Process for Q&A**: Add files to knowledge base for chat
     - **📋 Generate Documentation**: Instantly create clean documentation for code files

4. **Instant Documentation (NEW!):**
   - Upload Python, JavaScript, Java, or other code files
   - Click "📋 Generate Documentation"
   - Get instant, clean documentation with:
     - Overview and summary
     - Classes and methods
     - API endpoints detection
     - Test methods identification
     - Download as Markdown

5. **Ask Questions:**
   - Switch to the "💬 Chat" section
   - Ask questions about your uploaded documentation
   - Get intelligent, context-aware answers

## 📁 Project Structure

```
Dev-Mate-AI/
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── .env.example                       # Environment variables template
├── README.md                          # This file
├── src/                               # Source code
│   ├── config.py                     # Configuration management
│   ├── document_processor.py         # Document loading and chunking
│   ├── vector_store.py               # Vector storage and retrieval
│   ├── rag_pipeline.py               # RAG implementation
│   └── code_documentation_generator.py # NEW: Instant code documentation
├── utils/                             # Utility functions
│   └── helpers.py                    # Helper functions
└── data/                             # Data directory
    ├── sample_api_docs.md            # Sample API documentation
    ├── sample_api_test.py            # Sample test file
    └── sample_api_endpoints.py       # Sample API endpoints
```

## 🔍 How It Works

### 📚 Traditional Q&A Mode:
1. **Document Processing**: 
   - Uploaded documents are parsed and cleaned
   - Text is split into chunks with configurable size and overlap
   - Each chunk is assigned metadata (source, chunk ID, etc.)

2. **Vector Storage**:
   - Document chunks are converted to embeddings using **Sentence Transformers**
   - Embeddings are stored in ChromaDB for fast similarity search

3. **Query Processing**:
   - User queries are converted to embeddings
   - Similar document chunks are retrieved using vector similarity
   - Retrieved context is combined with the query

4. **Response Generation**:
   - **Hugging Face models** generate responses based on retrieved context
   - Responses include source attribution and confidence scores

### ⚡ Instant Documentation Mode (NEW!):
1. **Code Analysis**:
   - Uploaded code files are parsed using AST (Abstract Syntax Tree)
   - Extracts classes, functions, imports, and API endpoints
   - Identifies test methods and API endpoints automatically

2. **AI-Powered Documentation**:
   - Uses **CodeT5** model for intelligent code-to-text generation
   - Generates clean, structured documentation
   - Formats output as professional Markdown

3. **Instant Results**:
   - No waiting for processing - documentation generated immediately
   - Download as Markdown files
   - Perfect for API documentation and code reviews

## 📝 Supported File Types

### 📚 For Q&A Processing:
- **Text Files** (`.txt`): Plain text documents
- **Markdown** (`.md`): Markdown formatted documents
- **PDF** (`.pdf`): PDF documents (text extraction)
- **Word Documents** (`.docx`): Microsoft Word documents

### ⚡ For Instant Documentation:
- **Python** (`.py`): Python scripts, APIs, test files
- **JavaScript** (`.js`, `.ts`): JavaScript/TypeScript files
- **Java** (`.java`): Java classes and APIs
- **C/C++** (`.c`, `.cpp`): C/C++ source files
- **Go** (`.go`): Go source files
- **Rust** (`.rs`): Rust source files
- **PHP** (`.php`): PHP scripts and APIs

## 🎯 Example Questions

Try asking these types of questions about your API documentation:

- "How do I authenticate with this API?"
- "What are the available endpoints?"
- "How do I handle errors and status codes?"
- "What are the rate limits?"
- "How do I make a POST request?"
- "What request headers are required?"
- "How do I handle pagination?"
- "What response formats are supported?"

## ⚙️ Advanced Configuration

### Chunking Parameters

- `MAX_CHUNK_SIZE`: Maximum tokens per chunk (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks in tokens (default: 200)

### Model Parameters

- `TEMPERATURE`: Controls randomness in responses (0.0-1.0, default: 0.7)
- `MAX_TOKENS`: Maximum tokens in generated responses (default: 1500)

### Vector Database

- `CHROMA_PERSIST_DIRECTORY`: Directory for ChromaDB storage
- `COLLECTION_NAME`: Name of the document collection

## 🐛 Troubleshooting

### Common Issues

1. **"No documents in knowledge base"**
   - Upload some API documentation files first using "📚 Process for Q&A"

2. **Import errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - For code documentation: `pip install transformers torch`

3. **ChromaDB errors**
   - Delete the `chroma_db` directory and restart the application

4. **Code documentation not generating**
   - Ensure you're uploading supported code files (.py, .js, .java, etc.)
   - Check that the file contains valid code syntax

5. **Model loading issues**
   - First run may take time to download Hugging Face models
   - Ensure stable internet connection for initial model download

### Getting Help

- Check the application logs in the terminal
- Ensure all dependencies are properly installed
- Try with the sample files in the `data/` directory
- Models are downloaded automatically on first use

## 🔒 Security Notes

- **No API keys required** - all models run locally
- The application stores documents locally in ChromaDB
- **Complete privacy** - no data sent to external services
- All processing happens on your machine

## 📊 Performance Tips

- For large documents, consider adjusting chunk size and overlap
- **First run** may take time to download models (one-time only)
- Use specific, well-formed questions for better results
- Upload well-structured documentation for optimal performance
- For instant documentation, keep code files under 10,000 characters for best results

## 🤝 Contributing

This is a beginner-friendly project. Feel free to:

- Add support for more programming languages
- Improve the code analysis algorithms
- Enhance the documentation generation
- Add more configuration options
- Implement additional features

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Hugging Face** for providing free, open-source language models
- **Sentence Transformers** for excellent embedding models
- **ChromaDB** for vector storage capabilities
- **Streamlit** for the web interface framework
- **Salesforce CodeT5** for code-to-text generation
- The open-source community for various Python libraries used

---

**Happy documenting! 📚✨**