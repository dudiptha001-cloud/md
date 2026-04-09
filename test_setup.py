#!/usr/bin/env python
"""
Quick test script to verify the Customer Support Agent setup
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has valid API key"""
    print("\n[1] Checking .env file...")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("  ERROR: .env file not found")
        print("  Create it with: cp .env.example .env")
        return False
    
    with open(".env") as f:
        content = f.read()
        
    if "your_openai_api_key" in content or "your_azure" in content:
        print("  WARNING: .env has placeholder values")
        print("  Update with real API keys")
        return False
    
    print("  OK: .env file exists")
    return True


def check_imports():
    """Check if all imports work"""
    print("\n[2] Checking Python imports...")
    
    try:
        from config.settings import Settings
        print("  OK: Settings imported")
        
        from src.agent import SupportAgent
        print("  OK: SupportAgent imported")
        
        from src.document_loader import DocumentProcessor
        print("  OK: DocumentProcessor imported")
        
        return True
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return False


def check_vectorstore():
    """Check if vectorstore exists"""
    print("\n[3] Checking vectorstore...")
    
    vectorstore_path = Path("data/vectorstore/faiss_index")
    if vectorstore_path.exists():
        print("  OK: Vectorstore found")
        return True
    else:
        print("  WARNING: Vectorstore not found")
        print("  Run: python src/document_loader.py")
        return False


def test_agent():
    """Test agent initialization"""
    print("\n[4] Testing agent initialization...")
    
    try:
        from config.settings import Settings
        if not Settings.has_valid_api_key():
            print("  ERROR: No valid API key configured")
            return False
        
        from src.agent import SupportAgent
        agent = SupportAgent()
        print("  OK: Agent initialized successfully")
        return True
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("CUSTOMER SUPPORT AGENT - SETUP CHECK")
    print("=" * 60)
    
    checks = [
        ("Environment File", check_env_file),
        ("Python Imports", check_imports),
        ("Vector Store", check_vectorstore),
        ("Agent", test_agent),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n  EXCEPTION: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {name}: {status}")
    
    all_passed = all(r for _, r in results)
    
    if all_passed:
        print("\n[SUCCESS] Everything is ready!")
        print("\nRun the app with:")
        print("  streamlit run app.py")
        return 0
    else:
        print("\n[INCOMPLETE] Fix the issues above")
        print("\nFor detailed help, see:")
        print("  - SETUP_API_KEYS.md")
        print("  - README.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())
