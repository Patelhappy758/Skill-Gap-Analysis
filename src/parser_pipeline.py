"""
Enhanced Document Parser Pipeline Module
Handles extraction and processing of text from various document formats
"""

import os
import io
import time
from typing import Tuple, Dict, Optional, List
from pathlib import Path
import streamlit as st
import pandas as pd

# Import file readers
from file_reader import read_txt
from file_reader_pdf import read_pdf
from file_reader_doc import read_docx
from text_cleaner import TextCleaner


class DocumentParser:
    """Enhanced document parser with comprehensive error handling and analytics"""
    
    def __init__(self):
        self.supported_extensions = {".txt", ".pdf", ".docx"}
        self.max_file_size = 200 * 1024 * 1024  # 200MB
        self.upload_dir = "uploads"
        self.parsing_history = []
        
        # Ensure upload directory exists
        os.makedirs(self.upload_dir, exist_ok=True)

    def validate_file(self, uploaded_file) -> Dict[str, any]:
        """
        Validate uploaded file
        Args:
            uploaded_file: Streamlit uploaded file object
        Returns:
            dict: Validation result with status and messages
        """
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'file_info': {}
        }

        if not uploaded_file:
            result['is_valid'] = False
            result['errors'].append('No file provided')
            return result

        # Get file extension
        file_extension = Path(uploaded_file.name).suffix.lower()
        
        # File info
        result['file_info'] = {
            'name': uploaded_file.name,
            'size': uploaded_file.size,
            'type': uploaded_file.type,
            'extension': file_extension
        }

        # Check file size
        if uploaded_file.size > self.max_file_size:
            result['is_valid'] = False
            result['errors'].append(
                f"File size ({self._format_file_size(uploaded_file.size)}) "
                f"exceeds maximum allowed size ({self._format_file_size(self.max_file_size)})"
            )

        # Check file extension
        if file_extension not in self.supported_extensions:
            result['is_valid'] = False
            result['errors'].append(
                f"Unsupported file type: {file_extension}. "
                f"Supported types: {', '.join(self.supported_extensions)}"
            )

        # Additional validations
        if len(uploaded_file.name) > 255:
            result['warnings'].append('File name is very long and may cause issues')

        if uploaded_file.size == 0:
            result['is_valid'] = False
            result['errors'].append('File is empty')

        return result

    def save_uploaded_file(self, uploaded_file) -> Optional[str]:
        """
        Save uploaded file to disk
        Args:
            uploaded_file: Streamlit uploaded file object
        Returns:
            str: Path to saved file, or None if failed
        """
        if not uploaded_file:
            return None
        
        try:
            # Create unique filename to avoid conflicts
            timestamp = int(time.time())
            filename = f"{timestamp}_{uploaded_file.name}"
            dest_path = os.path.join(self.upload_dir, filename)
            
            with open(dest_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            return dest_path
        except Exception as e:
            st.error(f"Error saving file: {str(e)}")
            return None

    def extract_text_auto(self, file_path: str) -> Tuple[str, str, Dict]:
        """
        Automatically extract and clean text from file
        Args:
            file_path (str): Path to the file
        Returns:
            tuple: (raw_text, cleaned_text, extraction_info)
        """
        start_time = time.time()
        extraction_info = {
            'file_path': file_path,
            'file_size': 0,
            'extraction_time': 0,
            'success': False,
            'error': None,
            'file_type': None
        }

        try:
            # Get file info
            if os.path.exists(file_path):
                extraction_info['file_size'] = os.path.getsize(file_path)
            
            # Extract text based on file extension
            file_extension = Path(file_path).suffix.lower()
            extraction_info['file_type'] = file_extension
            
            raw_text = ""
            
            if file_extension == ".txt":
                raw_text = read_txt(file_path)
            elif file_extension == ".pdf":
                raw_text = read_pdf(file_path)
            elif file_extension == ".docx":
                raw_text = read_docx(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")

            # Clean the text
            cleaned_text = TextCleaner.advanced_clean(raw_text)
            
            # Calculate extraction time
            extraction_info['extraction_time'] = time.time() - start_time
            extraction_info['success'] = True
            
            # Add to parsing history
            self.parsing_history.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'file_name': os.path.basename(file_path),
                'file_type': file_extension,
                'file_size': extraction_info['file_size'],
                'extraction_time': extraction_info['extraction_time'],
                'raw_length': len(raw_text),
                'cleaned_length': len(cleaned_text),
                'success': True
            })

            return raw_text, cleaned_text, extraction_info

        except Exception as e:
            extraction_info['error'] = str(e)
            extraction_info['extraction_time'] = time.time() - start_time
            
            # Add failed attempt to history
            self.parsing_history.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'file_name': os.path.basename(file_path) if file_path else 'Unknown',
                'file_type': file_extension if 'file_extension' in locals() else 'Unknown',
                'file_size': extraction_info['file_size'],
                'extraction_time': extraction_info['extraction_time'],
                'raw_length': 0,
                'cleaned_length': 0,
                'success': False,
                'error': str(e)
            })
            
            return "", "", extraction_info

    def process_text_input(self, text: str, text_type: str = "manual") -> Tuple[str, str, Dict]:
        """
        Process manually entered text
        Args:
            text (str): Input text
            text_type (str): Type identifier for the text
        Returns:
            tuple: (raw_text, cleaned_text, processing_info)
        """
        start_time = time.time()
        
        processing_info = {
            'input_type': 'manual_text',
            'text_type': text_type,
            'processing_time': 0,
            'success': True,
            'error': None
        }

        try:
            raw_text = text
            cleaned_text = TextCleaner.advanced_clean(text)
            
            processing_info['processing_time'] = time.time() - start_time
            
            # Add to parsing history
            self.parsing_history.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'file_name': f'Manual_{text_type}',
                'file_type': 'text_input',
                'file_size': len(text),
                'extraction_time': processing_info['processing_time'],
                'raw_length': len(raw_text),
                'cleaned_length': len(cleaned_text),
                'success': True
            })

            return raw_text, cleaned_text, processing_info

        except Exception as e:
            processing_info['error'] = str(e)
            processing_info['success'] = False
            processing_info['processing_time'] = time.time() - start_time
            
            return text, text, processing_info

    def get_parsing_analytics(self) -> Dict:
        """
        Get analytics from parsing history
        Returns:
            dict: Analytics data
        """
        if not self.parsing_history:
            return {}
        
        df = pd.DataFrame(self.parsing_history)
        
        analytics = {
            'total_files_processed': len(df),
            'successful_extractions': len(df[df['success'] == True]),
            'failed_extractions': len(df[df['success'] == False]),
            'success_rate': round(len(df[df['success'] == True]) / len(df) * 100, 1),
            'average_extraction_time': round(df['extraction_time'].mean(), 2),
            'total_characters_processed': int(df[df['success'] == True]['raw_length'].sum()),
            'file_types_processed': df['file_type'].value_counts().to_dict(),
            'average_file_size': round(df['file_size'].mean(), 2)
        }
        
        return analytics

    def display_parsing_history(self):
        """
        Display parsing history in Streamlit
        """
        if not self.parsing_history:
            st.info("No parsing history available yet.")
            return
        
        st.subheader("📊 Parsing History & Analytics")
        
        # Analytics overview
        analytics = self.get_parsing_analytics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Files Processed", analytics['total_files_processed'])
        
        with col2:
            st.metric("Success Rate", f"{analytics['success_rate']}%")
        
        with col3:
            st.metric("Avg. Processing Time", f"{analytics['average_extraction_time']}s")
        
        with col4:
            st.metric("Characters Processed", 
                     self._format_number(analytics['total_characters_processed']))
        
        # Detailed history table
        if st.checkbox("Show detailed history"):
            df = pd.DataFrame(self.parsing_history)
            df['file_size'] = df['file_size'].apply(self._format_file_size)
            df['extraction_time'] = df['extraction_time'].apply(lambda x: f"{x:.2f}s")
            
            st.dataframe(
                df[['timestamp', 'file_name', 'file_type', 'file_size', 
                   'extraction_time', 'raw_length', 'cleaned_length', 'success']],
                use_container_width=True
            )

    def cleanup_old_files(self, max_age_hours: int = 24):
        """
        Clean up old uploaded files
        Args:
            max_age_hours (int): Maximum age in hours before deletion
        """
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            deleted_count = 0
            for filename in os.listdir(self.upload_dir):
                file_path = os.path.join(self.upload_dir, filename)
                file_age = current_time - os.path.getctime(file_path)
                
                if file_age > max_age_seconds:
                    os.remove(file_path)
                    deleted_count += 1
            
            if deleted_count > 0:
                st.info(f"Cleaned up {deleted_count} old files")
                
        except Exception as e:
            st.error(f"Error during cleanup: {str(e)}")

    @staticmethod
    def _format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    @staticmethod
    def _format_number(num: int) -> str:
        """Format large numbers with K/M/B suffixes"""
        if num < 1000:
            return str(num)
        elif num < 1000000:
            return f"{num/1000:.1f}K"
        elif num < 1000000000:
            return f"{num/1000000:.1f}M"
        else:
            return f"{num/1000000000:.1f}B"


# Global parser instance for the session
@st.cache_resource
def get_parser():
    """Get or create parser instance"""
    return DocumentParser()


if __name__ == "__main__":
    # Demo usage
    parser = DocumentParser()
    
    # Test with a sample file
    demo_file = "sample_resume.txt"
    if os.path.exists(demo_file):
        raw, cleaned, info = parser.extract_text_auto(demo_file)
        print("Raw preview:", raw[:200])
        print("\nCleaned preview:", cleaned[:200])
        print("\nExtraction info:", info)
        
        analytics = parser.get_parsing_analytics()
        print("\nAnalytics:", analytics)