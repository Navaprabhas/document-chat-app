"""
Setup script for Document Chat Application
"""
import os
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = ['temp', 'chroma_db', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def check_env_file():
    """Check if .env file exists"""
    if not Path('.env').exists():
        print("\n⚠️  .env file not found!")
        print("Creating .env from template...")
        
        if Path('.env.example').exists():
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ Created .env file")
            print("\n⚠️  Please edit .env and add your API keys!")
            return False
        else:
            print("❌ .env.example not found!")
            return False
    else:
        print("✓ .env file exists")
        return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'langchain',
        'chromadb',
        'PyPDF2',
        'openai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} not installed")
    
    if missing_packages:
        print("\n⚠️  Missing packages detected!")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def validate_config():
    """Validate configuration"""
    try:
        from config import Config
        Config.validate()
        print("✓ Configuration valid")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False

def main():
    """Run setup"""
    print("=" * 60)
    print("Document Chat Application - Setup")
    print("=" * 60)
    print()
    
    print("1. Creating directories...")
    create_directories()
    print()
    
    print("2. Checking environment file...")
    env_ok = check_env_file()
    print()
    
    print("3. Checking dependencies...")
    deps_ok = check_dependencies()
    print()
    
    if env_ok and deps_ok:
        print("4. Validating configuration...")
        config_ok = validate_config()
        print()
    else:
        config_ok = False
    
    print("=" * 60)
    if env_ok and deps_ok and config_ok:
        print("✅ Setup complete! You can now run:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Setup incomplete. Please fix the issues above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
