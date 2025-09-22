"""
Main Streamlit application for the LLM RAG API Documentation Assistant
"""
import streamlit as st
import os
import sys
from typing import List, Dict

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import Config
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.rag_pipeline import RAGPipeline
from src.professional_doc_generator import ProfessionalDocumentationGenerator

# Page configuration
st.set_page_config(
    page_title="API Documentation RAG Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'knowledge_base_stats' not in st.session_state:
    st.session_state.knowledge_base_stats = None
if 'professional_doc_generator' not in st.session_state:
    st.session_state.professional_doc_generator = None
if 'generated_documentation' not in st.session_state:
    st.session_state.generated_documentation = []

def initialize_app():
    """Initialize the RAG pipeline"""
    try:
        config = Config()
        config.validate_config()
        st.session_state.rag_pipeline = RAGPipeline()
        return True
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        st.info("Please create a .env file with your OpenAI API key. See .env.example for reference.")
        return False
    except Exception as e:
        st.error(f"Initialization Error: {str(e)}")
        return False

def upload_documents():
    """Handle document upload and processing"""
    st.header("📤 Upload API Documentation & Code Files")
    
    # Initialize professional documentation generator
    if st.session_state.professional_doc_generator is None:
        st.session_state.professional_doc_generator = ProfessionalDocumentationGenerator()
    
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        type=['txt', 'md', 'pdf', 'docx', 'py', 'js', 'java', 'cpp', 'c', 'go', 'rs', 'php', 'ts'],
        accept_multiple_files=True,
        help="Upload your API documentation files or code files. Supported formats: TXT (including code in text files), MD, PDF, DOCX, PY, JS, JAVA, CPP, C, GO, RS, PHP, TS"
    )
    
    if uploaded_files:
        col1, col2 = st.columns(2)
        
        with col1:
            process_docs = st.button("📚 Process for Q&A", type="primary")
        with col2:
            generate_pro_docs = st.button("📋 Generate Documentation", type="primary")
        
        if process_docs:
            with st.spinner("Processing documents for Q&A..."):
                processor = DocumentProcessor()
                vector_store = VectorStore()
                
                total_chunks = 0
                processed_files = []
                
                for uploaded_file in uploaded_files:
                    try:
                        # Process document
                        chunks = processor.process_uploaded_file(uploaded_file)
                        
                        # Add to vector store
                        success = vector_store.add_documents(chunks)
                        
                        if success:
                            total_chunks += len(chunks)
                            processed_files.append({
                                'name': uploaded_file.name,
                                'chunks': len(chunks),
                                'size': uploaded_file.size
                            })
                        else:
                            st.error(f"Failed to process {uploaded_file.name}")
                    
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
                if processed_files:
                    st.success(f"Successfully processed {len(processed_files)} files with {total_chunks} chunks!")
                    
                    # Show processing summary
                    st.subheader("Processing Summary")
                    for file_info in processed_files:
                        st.write(f"✅ **{file_info['name']}** - {file_info['chunks']} chunks ({file_info['size']} bytes)")
                    
                    # Update knowledge base stats
                    update_knowledge_base_stats()
        
        if generate_pro_docs:
            with st.spinner("Generating documentation..."):
                st.session_state.generated_documentation = []
                
                for uploaded_file in uploaded_files:
                    try:
                        # Check if it's a code file
                        if st.session_state.professional_doc_generator.is_code_file(uploaded_file.name):
                            # Read file content
                            file_content = uploaded_file.read().decode('utf-8')
                            
                            # Generate professional documentation
                            markdown_doc = st.session_state.professional_doc_generator.generate_professional_documentation(
                                file_content, uploaded_file.name
                            )
                            
                            st.session_state.generated_documentation.append({
                                'filename': uploaded_file.name,
                                'documentation': None,
                                'markdown': markdown_doc,
                                'type': 'professional'
                            })
                        else:
                            st.warning(f"⚠️ {uploaded_file.name} is not recognized as a code file. Supported: .py, .js, .java, .cpp, .c, .go, .rs, .php, .ts, or .txt files containing code (with keywords like 'test', 'api', 'service', etc. in filename)")
                    
                    except Exception as e:
                        st.error(f"Error generating documentation for {uploaded_file.name}: {str(e)}")
                
                if st.session_state.generated_documentation:
                    st.success(f"✨ Generated documentation for {len(st.session_state.generated_documentation)} code file(s)!")
                    st.info("📋 Check the 'Generated Documentation' section below to view the results.")
    
    # Display generated documentation
    if st.session_state.generated_documentation:
        st.divider()
        st.header("📋 Generated Documentation")
        
        for doc_info in st.session_state.generated_documentation:
            with st.expander(f"📄 {doc_info['filename']}", expanded=True):
                st.markdown(doc_info['markdown'])
                
                # Download button for documentation
                st.download_button(
                    label=f"💾 Download Documentation",
                    data=doc_info['markdown'],
                    file_name=f"{doc_info['filename']}_documentation.md",
                    mime="text/markdown"
                )
        
        # Clear documentation button
        if st.button("🗑️ Clear Generated Documentation"):
            st.session_state.generated_documentation = []
            st.rerun()

def update_knowledge_base_stats():
    """Update knowledge base statistics"""
    if st.session_state.rag_pipeline:
        st.session_state.knowledge_base_stats = st.session_state.rag_pipeline.get_knowledge_base_stats()

def show_knowledge_base_info():
    """Display knowledge base information"""
    st.header("📊 Knowledge Base Status")
    
    if st.session_state.knowledge_base_stats is None:
        update_knowledge_base_stats()
    
    stats = st.session_state.knowledge_base_stats
    
    if stats:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Documents", stats.get('total_documents', 0))
        
        with col2:
            st.metric("Unique Sources", stats.get('unique_sources', 0))
        
        with col3:
            st.metric("Status", stats.get('status', 'Unknown').title())
        
        if stats.get('source_files'):
            st.subheader("📁 Uploaded Files")
            for source in stats['source_files']:
                st.write(f"• {source}")
        
        # Clear knowledge base button
        if st.button("🗑️ Clear Knowledge Base", type="secondary"):
            if st.session_state.rag_pipeline:
                vector_store = VectorStore()
                if vector_store.delete_collection():
                    st.success("Knowledge base cleared successfully!")
                    update_knowledge_base_stats()
                    st.rerun()
                else:
                    st.error("Failed to clear knowledge base")

def chat_interface():
    """Main chat interface"""
    st.header("💬 Ask Questions About Your API Documentation")
    
    # Check if knowledge base has documents
    if st.session_state.knowledge_base_stats and st.session_state.knowledge_base_stats.get('total_documents', 0) == 0:
        st.warning("⚠️ No documents in knowledge base. Please upload some API documentation first.")
        return
    
    # Suggested questions
    with st.expander("💡 Suggested Questions"):
        suggested = st.session_state.rag_pipeline.get_suggested_questions()
        for i, question in enumerate(suggested):
            if st.button(question, key=f"suggested_{i}"):
                st.session_state.current_query = question
    
    # Chat input
    query = st.text_input(
        "Ask a question about your API documentation:",
        value=st.session_state.get('current_query', ''),
        placeholder="e.g., How do I authenticate with this API?",
        key="query_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        ask_button = st.button("Ask", type="primary")
    with col2:
        clear_chat = st.button("Clear Chat History")
    
    if clear_chat:
        st.session_state.chat_history = []
        st.rerun()
    
    if ask_button and query:
        with st.spinner("Searching knowledge base and generating response..."):
            # Process query
            result = st.session_state.rag_pipeline.process_query(query)
            
            # Add to chat history
            st.session_state.chat_history.append({
                'query': query,
                'response': result['response'],
                'sources': result['sources'],
                'confidence': result['confidence']
            })
        
        # Clear the input
        st.session_state.current_query = ""
        st.rerun()
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("💭 Chat History")
        
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.container():
                st.markdown(f"**🙋 Question:** {chat['query']}")
                st.markdown(f"**🤖 Answer:** {chat['response']}")
                
                # Show confidence and sources
                col1, col2 = st.columns(2)
                with col1:
                    confidence_color = "green" if chat['confidence'] > 0.7 else "orange" if chat['confidence'] > 0.4 else "red"
                    st.markdown(f"**Confidence:** :{confidence_color}[{chat['confidence']:.1%}]")
                
                with col2:
                    if chat['sources']:
                        st.markdown("**Sources:**")
                        for source in chat['sources']:
                            st.markdown(f"• {source['name']} (relevance: {source['relevance_score']:.1%})")
                
                st.divider()

def main():
    """Main application"""
    st.title("📚 API Documentation RAG Assistant")
    st.markdown("Upload your API documentation and ask questions to get intelligent, context-aware answers!")
    
    # Initialize app
    if not initialize_app():
        return
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ Controls")
        
        page = st.selectbox(
            "Choose a section:",
            ["💬 Chat", "📤 Upload Documents", "📊 Knowledge Base"]
        )
        
        st.divider()
        
        # Configuration info
        st.subheader("⚙️ Configuration")
        config = Config()
        st.write(f"**Model:** {config.CHAT_MODEL}")
        st.write(f"**Temperature:** {config.TEMPERATURE}")
        st.write(f"**Max Tokens:** {config.MAX_TOKENS}")
        
        st.divider()
        
        # Help section
        with st.expander("❓ Help"):
            st.markdown("""
            **How to use:**
            1. Upload your API documentation files
            2. Wait for processing to complete
            3. Ask questions about your API
            4. Get intelligent, context-aware answers
            
            **Supported file types:**
            - Text files (.txt)
            - Markdown files (.md)
            - PDF files (.pdf)
            - Word documents (.docx)
            """)
    
    # Main content based on selected page
    if page == "💬 Chat":
        chat_interface()
    elif page == "📤 Upload Documents":
        upload_documents()
    elif page == "📊 Knowledge Base":
        show_knowledge_base_info()

if __name__ == "__main__":
    main()