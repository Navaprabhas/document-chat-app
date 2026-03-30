"""
Test script to verify Document Chat Application setup
"""
import sys
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    tests = {
        'streamlit': 'Streamlit',
        'langchain': 'LangChain',
        'chromadb': 'ChromaDB',
        'PyPDF2': 'PyPDF2',
        'openai': 'OpenAI',
        'dotenv': 'python-dotenv'
    }
    
    failed = []
    
    for module, name in tests.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError as e:
            print(f"  ❌ {name}: {str(e)}")
            failed.append(name)
    
    return len(failed) == 0, failed

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from config import Config
        print(f"  ✓ Config loaded")
        print(f"  - LLM Provider: {Config.LLM_PROVIDER}")
        print(f"  - Embedding Model: {Config.EMBEDDING_MODEL}")
        print(f"  - Chunk Size: {Config.CHUNK_SIZE}")
        return True
    except Exception as e:
        print(f"  ❌ Config error: {str(e)}")
        return False

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directories...")
    
    dirs = ['temp', 'chroma_db']
    all_exist = True
    
    for directory in dirs:
        path = Path(directory)
        if path.exists():
            print(f"  ✓ {directory}/")
        else:
            print(f"  ❌ {directory}/ (missing)")
            all_exist = False
    
    return all_exist

def test_env_file():
    """Test if .env file exists and has required keys"""
    print("\nTesting environment file...")
    
    env_path = Path('.env')
    if not env_path.exists():
        print("  ❌ .env file not found")
        return False
    
    print("  ✓ .env file exists")
    
    # Check for required keys
    with open(env_path) as f:
        content = f.read()
        
    required_keys = ['OPENAI_API_KEY', 'LLM_PROVIDER']
    missing = []
    
    for key in required_keys:
        if key in content:
            # Check if it has a value
            for line in content.split('\n'):
                if line.startswith(key):
                    if '=' in line and line.split('=')[1].strip():
                        print(f"  ✓ {key} configured")
                    else:
                        print(f"  ⚠️  {key} exists but may be empty")
                    break
        else:
            print(f"  ❌ {key} missing")
            missing.append(key)
    
    return len(missing) == 0

def test_document_processor():
    """Test document processor initialization"""
    print("\nTesting document processor...")
    
    try:
        from document_processor import DocumentProcessor
        processor = DocumentProcessor()
        print("  ✓ DocumentProcessor initialized")
        return True
    except Exception as e:
        print(f"  ❌ DocumentProcessor error: {str(e)}")
        return False

def test_embeddings_manager():
    """Test embeddings manager initialization"""
    print("\nTesting embeddings manager...")
    
    try:
        from embeddings_manager import EmbeddingsManager
        print("  ⚠️  Attempting to initialize (may require API key)...")
        manager = EmbeddingsManager()
        print("  ✓ EmbeddingsManager initialized")
        return True
    except Exception as e:
        print(f"  ❌ EmbeddingsManager error: {str(e)}")
        print("  Note: This may fail if API keys are not configured")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Document Chat Application - Setup Test")
    print("=" * 60)
    print()
    
    results = {}
    
    # Run tests
    results['imports'], failed_imports = test_imports()
    results['config'] = test_config()
    results['directories'] = test_directories()
    results['env'] = test_env_file()
    results['processor'] = test_document_processor()
    results['embeddings'] = test_embeddings_manager()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {test}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! Ready to run:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        
        if not results['imports']:
            print("\nTo fix import errors:")
            print("   pip install -r requirements.txt")
        
        if not results['env']:
            print("\nTo fix environment errors:")
            print("   cp .env.example .env")
            print("   # Then edit .env with your API keys")
        
        if not results['directories']:
            print("\nTo fix directory errors:")
            print("   python setup.py")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
