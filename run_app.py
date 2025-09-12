"""
Application runner script for Milestone 1
Launches the Streamlit dashboard
"""

import subprocess
import sys
import os


def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'PyPDF2', 
        'python-docx',
        'pandas',
        'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True


def run_streamlit_app():
    """Run the Streamlit application."""
    print("\n🚀 Starting Milestone 1: Data Ingestion and Parsing Module")
    print("=" * 60)
    print("📊 Gap Analysis System - Document Upload & Processing")
    print("🌐 The app will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("=" * 60)
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "false",
            "--server.address", "localhost",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")


def main():
    """Main function."""
    print("🎯 Milestone 1: Data Ingestion and Parsing Module")
    print("=" * 60)
    
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        return
    
    # Check if sample files exist
    sample_files = [
        'source/sample_resume.txt',
        'source/sample_resume_pdf.pdf', 
        'source/sample_resume_doc.docx'
    ]
    
    print(f"\n📁 Checking sample files...")
    for file_path in sample_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"⚠️  {file_path} (optional)")
    
    run_streamlit_app()


if __name__ == "__main__":
    main()