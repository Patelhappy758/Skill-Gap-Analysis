# file_reader_pdf.py - Enhanced PDF File Reader
"""
Enhanced PDF File Reader with multiple extraction methods and error handling
"""

import PyPDF2
import pdfplumber
import streamlit as st
from typing import Optional, Dict, Any
import os


def read_pdf_pypdf2(file_path: str) -> str:
    """
    Read PDF using PyPDF2 library
    Args:
        file_path (str): Path to the PDF file
    Returns:
        str: Extracted text
    """
    try:
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text() or ""
                    text += f"\n--- Page {page_num + 1} ---\n" + page_text
                except Exception as e:
                    st.warning(f"⚠️ Could not extract text from page {page_num + 1}: {str(e)}")
                    continue
        
        return text.strip()
    except Exception as e:
        st.error(f"❌ PyPDF2 extraction failed: {str(e)}")
        return ""


def read_pdf_pdfplumber(file_path: str) -> str:
    """
    Read PDF using pdfplumber library (more accurate for complex layouts)
    Args:
        file_path (str): Path to the PDF file
    Returns:
        str: Extracted text
    """
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                try:
                    page_text = page.extract_text() or ""
                    if page_text.strip():
                        text += f"\n--- Page {page_num + 1} ---\n" + page_text
                except Exception as e:
                    st.warning(f"⚠️ Could not extract text from page {page_num + 1}: {str(e)}")
                    continue
        
        return text.strip()
    except Exception as e:
        st.error(f"❌ pdfplumber extraction failed: {str(e)}")
        return ""


def read_pdf(file_path: str, method: str = "auto") -> str:
    """
    Read PDF file with multiple extraction methods
    Args:
        file_path (str): Path to the PDF file
        method (str): Extraction method ('auto', 'pypdf2', 'pdfplumber')
    Returns:
        str: Extracted text content from PDF
    """
    try:
        # Validate file
        if not file_path or not os.path.exists(file_path):
            st.error(f"❌ PDF file not found: {file_path}")
            return ""
        
        # Get file info
        file_size = os.path.getsize(file_path)
        st.info(f"📄 Processing PDF file: {os.path.basename(file_path)} ({file_size / (1024*1024):.1f} MB)")
        
        text = ""
        
        if method == "auto" or method == "pdfplumber":
            # Try pdfplumber first (generally more accurate)
            try:
                text = read_pdf_pdfplumber(file_path)
                if text.strip():
                    st.success("✅ Successfully extracted text using pdfplumber")
                    method_used = "pdfplumber"
                else:
                    raise Exception("No text extracted")
            except:
                if method == "pdfplumber":
                    st.error("❌ pdfplumber extraction failed")
                    return ""
                # Fall back to PyPDF2
                st.info("🔄 Falling back to PyPDF2...")
                text = read_pdf_pypdf2(file_path)
                method_used = "pypdf2"
        
        elif method == "pypdf2":
            text = read_pdf_pypdf2(file_path)
            method_used = "pypdf2"
        
        else:
            st.error(f"❌ Unknown extraction method: {method}")
            return ""
        
        # Validate extracted text
        if not text.strip():
            st.warning("⚠️ No text could be extracted from the PDF")
            return ""
        
        st.success(f"✅ Successfully read PDF file using {method_used} ({len(text)} characters)")
        return text

    except FileNotFoundError:
        st.error("❌ PDF file not found")
        return ""
    
    except PermissionError:
        st.error("❌ Permission denied to read PDF file")
        return ""
    
    except Exception as e:
        st.error(f"❌ Error reading PDF file: {str(e)}")
        return ""


def get_pdf_metadata(file_path: str) -> Dict[str, Any]:
    """
    Get metadata information about the PDF file
    Args:
        file_path (str): Path to the PDF file
    Returns:
        dict: PDF metadata
    """
    try:
        metadata = {}
        
        # File system metadata
        stat = os.stat(file_path)
        metadata.update({
            'file_name': os.path.basename(file_path),
            'file_size': stat.st_size,
            'created_time': stat.st_ctime,
            'modified_time': stat.st_mtime
        })
        
        # PDF-specific metadata
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                metadata.update({
                    'num_pages': len(reader.pages),
                    'pdf_info': reader.metadata or {}
                })
        except:
            pass
        
        return metadata
    except Exception as e:
        return {'error': str(e)}
