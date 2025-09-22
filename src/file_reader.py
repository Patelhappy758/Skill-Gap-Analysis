# file_reader.py - Enhanced TXT File Reader
"""
Enhanced TXT File Reader with comprehensive error handling and encoding detection
"""

import os
import chardet
import streamlit as st
from pathlib import Path
from typing import Optional, Dict, Any


def detect_encoding(file_path: str) -> str:
    """
    Detect file encoding using chardet
    Args:
        file_path (str): Path to the file
    Returns:
        str: Detected encoding or 'utf-8' as fallback
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # Read first 10KB for detection
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'
    except:
        return 'utf-8'


def read_txt(file_path: str) -> str:
    """
    Read text file with encoding detection and error handling
    Args:
        file_path (str): Path to the TXT file
    Returns:
        str: Extracted text content from TXT file
    """
    try:
        # Validate file path
        if not file_path or not os.path.exists(file_path):
            st.error(f"❌ TXT file not found: {file_path}")
            return ""
        
        # Get file info
        file_size = os.path.getsize(file_path)
        st.info(f"📄 Processing TXT file: {os.path.basename(file_path)} ({file_size / 1024:.1f} KB)")
        
        # Detect encoding
        encoding = detect_encoding(file_path)
        st.success(f"🔍 Detected encoding: {encoding}")
        
        # Read file with detected encoding
        try:
            with open(file_path, "r", encoding=encoding) as f:
                text = f.read()
        except UnicodeDecodeError:
            # Fallback to utf-8 with error handling
            st.warning("⚠️ Encoding issue detected, using UTF-8 with error handling")
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        
        # Validate content
        if not text.strip():
            st.warning("⚠️ TXT file appears to be empty")
            return ""
        
        st.success(f"✅ Successfully read TXT file ({len(text)} characters)")
        return text

    except FileNotFoundError:
        st.error("❌ TXT file not found")
        return ""
    
    except PermissionError:
        st.error("❌ Permission denied to read TXT file")
        return ""
    
    except Exception as e:
        st.error(f"❌ Error reading TXT file: {str(e)}")
        return ""


def get_txt_metadata(file_path: str) -> Dict[str, Any]:
    """
    Get metadata information about the TXT file
    Args:
        file_path (str): Path to the TXT file
    Returns:
        dict: File metadata
    """
    try:
        stat = os.stat(file_path)
        return {
            'file_name': os.path.basename(file_path),
            'file_size': stat.st_size,
            'created_time': stat.st_ctime,
            'modified_time': stat.st_mtime,
            'encoding': detect_encoding(file_path)
        }
    except Exception as e:
        return {'error': str(e)}