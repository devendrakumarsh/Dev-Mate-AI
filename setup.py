"""
Setup script for the LLM RAG Application
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    # Core packages that should install without issues
    core_packages = [
        "streamlit",
        "openai",
        "python-dotenv",
        "requests",
        "markdown"
    ]
    
    # Install core packages first
    for package in core_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
    
    # Try to install other packages
    other_packages = [
        "PyPDF2",
        "python-docx",
        "chromadb",
        "sentence-transformers",
        "tiktoken",
        "numpy",
        "pandas"
    ]
    
    for package in other_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Warning: Failed to install {package}: {e}")
            print(f"   You can try installing {package} manually later")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("""# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Application Configuration
APP_TITLE=API Documentation RAG Assistant
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TEMPERATURE=0.7
MAX_TOKENS=1500

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
COLLECTION_NAME=api_docs
""")
        print("✅ Created .env file. Please add your OpenAI API key!")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up LLM RAG Application...")
    print("=" * 50)
    
    # Install requirements
    install_requirements()
    
    print("\n" + "=" * 50)
    
    # Create .env file
    create_env_file()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Add your OpenAI API key to the .env file")
    print("2. Run: streamlit run app.py")
    print("3. Upload some API documentation and start asking questions!")

if __name__ == "__main__":
    main()