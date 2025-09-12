"""
Milestone 1: Data Ingestion and Parsing Module
Resume and Job Description Gap Analysis System

This Streamlit application handles document upload, parsing, and text extraction
for resumes and job descriptions in PDF, DOCX, and TXT formats.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from file_processors import document_processor, text_cleaner


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'processed_documents' not in st.session_state:
        st.session_state.processed_documents = []
    if 'current_document' not in st.session_state:
        st.session_state.current_document = None


def display_header():
    """Display the application header and navigation."""
    st.set_page_config(
        page_title="Gap Analysis System - Milestone 1",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #4A90E2; margin-bottom: 10px;'>📊 GAP ANALYSIS</h1>
            <h2 style='color: #666; font-size: 24px; margin-top: 0;'>Milestone 1: Data Ingestion and Parsing Module</h2>
            <p style='color: #888; font-size: 16px;'>Resume and job description upload system • File parsing and text extraction • Clean, normalized input data</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("⚙️ Settings", use_container_width=True):
            st.info("Settings functionality will be available in future milestones.")
    with col3:
        st.markdown("**Document Type:**")
    with col4:
        doc_type = st.selectbox("", ["Resume", "Job Description"], label_visibility="collapsed")
    
    return doc_type


def display_upload_section():
    """Display the document upload interface."""
    st.markdown("### 📁 Upload Documents")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Drag and drop files here or click to browse",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("**PDF**")
        st.markdown("📄 Portable Document Format")
    with col2:
        st.markdown("**DOCX**") 
        st.markdown("📝 Microsoft Word Document")
    with col3:
        st.markdown("**TXT**")
        st.markdown("📋 Plain Text File")
    
    return uploaded_file


def process_uploaded_file(uploaded_file, doc_type):
    """Process the uploaded file and extract text."""
    if uploaded_file is None:
        return None
    
    # Show processing status
    with st.spinner(f'Processing {uploaded_file.name}...'):
        # Get file extension
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Extract text using document processor
        extraction_result = document_processor.extract_text(
            file_content=uploaded_file.getvalue(),
            file_type=file_extension
        )
        
        if not extraction_result['success']:
            st.error(f"Error processing file: {extraction_result['error']}")
            return None
        
        # Clean and normalize text
        cleaning_result = text_cleaner.clean_and_normalize(extraction_result['text'])
        
        # Extract sections
        sections = text_cleaner.extract_sections(cleaning_result['cleaned_text'])
        
        # Prepare document data
        document_data = {
            'filename': uploaded_file.name,
            'file_type': file_extension,
            'doc_type': doc_type,
            'upload_time': datetime.now(),
            'raw_text': extraction_result['text'],
            'cleaned_text': cleaning_result['cleaned_text'],
            'metadata': extraction_result['metadata'],
            'cleaning_stats': cleaning_result['cleaning_stats'],
            'sections': sections,
            'file_size': len(uploaded_file.getvalue())
        }
        
        return document_data


def display_document_preview(document_data):
    """Display document preview and analysis."""
    if not document_data:
        st.info("👆 Please upload a document to see the preview")
        return
    
    st.markdown("### 👁️ Document Preview")
    
    # Document info tabs
    tab1, tab2, tab3 = st.tabs(["📄 Preview", "📊 Analysis", "🔧 Processing Stats"])
    
    with tab1:
        # Document metadata
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("File Name", document_data['filename'])
        with col2:
            st.metric("File Type", document_data['file_type'].upper())
        with col3:
            st.metric("Document Type", document_data['doc_type'])
        with col4:
            st.metric("File Size", f"{document_data['file_size']} bytes")
        
        # Text preview
        st.markdown("#### 📝 Extracted Text Preview")
        preview_text = document_data['cleaned_text'][:1000]
        if len(document_data['cleaned_text']) > 1000:
            preview_text += "..."
        
        st.text_area(
            "Document Content",
            value=preview_text,
            height=300,
            disabled=True,
            label_visibility="collapsed"
        )
        
        # Character and word counts
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Characters", len(document_data['cleaned_text']))
        with col2:
            st.metric("Words", document_data['cleaning_stats']['words_count'])
        with col3:
            if 'page_count' in document_data['metadata']:
                st.metric("Pages", document_data['metadata']['page_count'])
            elif 'paragraph_count' in document_data['metadata']:
                st.metric("Paragraphs", document_data['metadata']['paragraph_count'])
    
    with tab2:
        st.markdown("#### 📊 Document Analysis")
        
        # Text length analysis
        fig_length = go.Figure()
        fig_length.add_trace(go.Bar(
            x=['Original Text', 'Cleaned Text'],
            y=[len(document_data['raw_text']), len(document_data['cleaned_text'])],
            marker_color=['#ff7f0e', '#2ca02c']
        ))
        fig_length.update_layout(
            title="Text Length Comparison",
            yaxis_title="Character Count",
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig_length, use_container_width=True)
        
        # Section analysis
        sections_with_content = {k: v for k, v in document_data['sections'].items() if v.strip()}
        if sections_with_content:
            st.markdown("#### 📋 Identified Sections")
            section_lengths = {k: len(v) for k, v in sections_with_content.items()}
            
            fig_sections = px.pie(
                values=list(section_lengths.values()),
                names=list(section_lengths.keys()),
                title="Content Distribution by Section"
            )
            st.plotly_chart(fig_sections, use_container_width=True)
            
            # Display sections
            for section, content in sections_with_content.items():
                if content.strip():
                    with st.expander(f"{section.title()} Section"):
                        st.text_area(
                            f"{section}_content",
                            value=content[:500] + ("..." if len(content) > 500 else ""),
                            height=150,
                            disabled=True,
                            label_visibility="collapsed"
                        )
    
    with tab3:
        st.markdown("#### 🔧 Processing Statistics")
        
        # Processing metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Original Length", f"{len(document_data['raw_text']):,} chars")
            st.metric("Cleaned Length", f"{len(document_data['cleaned_text']):,} chars")
            st.metric("Words Count", f"{document_data['cleaning_stats']['words_count']:,}")
        
        with col2:
            st.metric("Whitespace Reduced", f"{document_data['cleaning_stats']['whitespace_reduction']:,} chars")
            st.metric("Special Chars Removed", f"{document_data['cleaning_stats']['special_chars_removed']:,}")
            st.metric("Lines Count", f"{document_data['cleaning_stats']['lines_count']:,}")
        
        # Processing efficiency chart
        efficiency_data = {
            'Metric': ['Whitespace Reduction', 'Special Chars Removed', 'Content Preserved'],
            'Value': [
                document_data['cleaning_stats']['whitespace_reduction'],
                document_data['cleaning_stats']['special_chars_removed'],
                len(document_data['cleaned_text'])
            ]
        }
        
        fig_efficiency = px.bar(
            efficiency_data,
            x='Metric',
            y='Value',
            title="Text Processing Efficiency",
            color='Metric'
        )
        st.plotly_chart(fig_efficiency, use_container_width=True)


def display_processed_documents():
    """Display list of processed documents."""
    if not st.session_state.processed_documents:
        st.info("No documents processed yet. Upload a document to get started!")
        return
    
    st.markdown("### 📚 Processed Documents")
    
    # Create dataframe for display
    doc_list = []
    for i, doc in enumerate(st.session_state.processed_documents):
        doc_list.append({
            'Index': i + 1,
            'Filename': doc['filename'],
            'Type': doc['file_type'].upper(),
            'Document Type': doc['doc_type'],
            'Upload Time': doc['upload_time'].strftime('%Y-%m-%d %H:%M:%S'),
            'Characters': len(doc['cleaned_text']),
            'Words': doc['cleaning_stats']['words_count']
        })
    
    df = pd.DataFrame(doc_list)
    st.dataframe(df, use_container_width=True)
    
    # Document selection for detailed view
    selected_doc = st.selectbox(
        "Select document for detailed view:",
        options=range(len(st.session_state.processed_documents)),
        format_func=lambda x: st.session_state.processed_documents[x]['filename']
    )
    
    if st.button("View Selected Document", use_container_width=True):
        st.session_state.current_document = st.session_state.processed_documents[selected_doc]
        st.rerun()


def main():
    """Main application function."""
    initialize_session_state()
    doc_type = display_header()
    
    # Main layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Upload section
        uploaded_file = display_upload_section()
        
        # Process file if uploaded
        if uploaded_file:
            document_data = process_uploaded_file(uploaded_file, doc_type)
            
            if document_data:
                st.session_state.current_document = document_data
                
                # Add to processed documents if not already there
                if not any(doc['filename'] == document_data['filename'] and 
                          doc['upload_time'] == document_data['upload_time'] 
                          for doc in st.session_state.processed_documents):
                    st.session_state.processed_documents.append(document_data)
                
                st.success(f"✅ Successfully processed {uploaded_file.name}")
        
        # Display processed documents list
        st.markdown("---")
        display_processed_documents()
    
    with col2:
        # Document preview section
        display_document_preview(st.session_state.current_document)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>Milestone 1: Data Ingestion and Parsing Module (Weeks 1-2)</strong></p>
        <p>Module: Data Ingestion and Parsing • Resume and job description upload system • File parsing and text extraction • Clean, normalized input data</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()