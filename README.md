# Gap Analysis System - Milestone 1

## Data Ingestion and Parsing Module (Weeks 1-2)

This milestone implements the foundational document processing capabilities for the Resume-Job Description Gap Analysis System.

### 🎯 Project Overview

The system uses Natural Language Processing (NLP) to extract skills from resumes and job descriptions, compares them, and identifies gaps. This application provides intelligent recommendations for upskilling by highlighting missing or underrepresented skills, improving job readiness.

### 📋 Milestone 1 Features

#### ✅ Implemented Features

1. **Document Upload System**
   - Support for PDF, DOCX, and TXT formats
   - Drag-and-drop file upload interface
   - File validation and error handling

2. **Text Extraction Pipeline**
   - PDF text extraction using PyPDF2
   - DOCX text extraction using python-docx
   - TXT file processing with encoding detection
   - Robust error handling for various file formats

3. **Text Cleaning & Normalization**
   - Whitespace normalization
   - Special character removal
   - Punctuation standardization
   - Text preprocessing for NLP readiness

4. **Document Analysis Dashboard**
   - Real-time document preview
   - Text statistics and metrics
   - Section identification (Contact, Summary, Experience, Education, Skills)
   - Processing efficiency visualization

5. **Interactive Web Interface**
   - Streamlit-based dashboard
   - Document upload and parsing
   - Clean, normalized output display
   - Processing statistics and analytics

### 🏗️ Project Structure

```
/workspace/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── run_app.py            # Application launcher
├── test_system.py        # Testing utilities
├── utils/
│   ├── __init__.py
│   └── file_processors.py # Document processing utilities
└── source/               # Sample files
    ├── sample_resume.txt
    ├── sample_resume_pdf.pdf
    └── sample_resume_doc.docx
```

### 🚀 Getting Started

#### Prerequisites

- Python 3.7+
- pip package manager

#### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python run_app.py
   ```
   
   Or directly with Streamlit:
   ```bash
   streamlit run app.py
   ```

3. **Access the Dashboard**
   - Open your browser to `http://localhost:8501`
   - Upload documents (PDF, DOCX, or TXT)
   - View processed results and analytics

#### Testing

Run the test suite to verify functionality:
```bash
python test_system.py
```

### 📊 Dashboard Features

#### Document Upload & Parsing
- **Upload Interface**: Drag-and-drop file upload supporting PDF, DOCX, TXT
- **Real-time Processing**: Immediate text extraction and cleaning
- **Error Handling**: Comprehensive error reporting for file issues

#### Document Preview
- **Text Preview**: Clean, formatted text display
- **Metadata Display**: File information, character/word counts, processing stats
- **Section Analysis**: Automatic identification of resume/job description sections

#### Analytics & Visualization
- **Text Length Comparison**: Before/after cleaning visualization
- **Section Distribution**: Pie chart showing content distribution
- **Processing Efficiency**: Bar charts showing cleaning statistics

### 🔧 Technical Implementation

#### Core Components

1. **DocumentProcessor Class**
   - Handles multi-format document parsing
   - Supports both file paths and uploaded file content
   - Provides detailed extraction metadata

2. **TextCleaner Class**
   - Normalizes whitespace and punctuation
   - Removes unwanted characters
   - Extracts document sections automatically

3. **Streamlit Dashboard**
   - Interactive file upload interface
   - Real-time document processing
   - Comprehensive analytics display

#### Supported File Formats

- **PDF**: Using PyPDF2 for text extraction
- **DOCX**: Using python-docx for paragraph extraction
- **TXT**: Native text processing with encoding detection

### 📈 Output Screenshots

The dashboard provides:

1. **Upload Interface**
   - Clean file upload area
   - Format indicators (PDF, DOCX, TXT)
   - Processing status feedback

2. **Document Preview**
   - Extracted text display
   - Character and word count metrics
   - File metadata information

3. **Analysis Charts**
   - Text length comparison graphs
   - Section distribution pie charts
   - Processing efficiency metrics

### 🔄 Next Steps (Future Milestones)

- **Milestone 2**: Skill Extraction using NLP and NER models
- **Milestone 3**: Skill Gap Analysis and Similarity Matching
- **Milestone 4**: Visualization and Reporting Dashboard

### 🛠️ Dependencies

```
streamlit==1.28.1    # Web dashboard framework
PyPDF2==3.0.1        # PDF text extraction
python-docx==0.8.11  # DOCX document processing
pandas==2.0.3        # Data manipulation
numpy==1.24.3        # Numerical computing
plotly==5.17.0       # Interactive visualizations
```

### 📝 Usage Examples

1. **Upload a Resume**
   - Select "Resume" document type
   - Upload PDF/DOCX/TXT file
   - View extracted text and analysis

2. **Upload a Job Description**
   - Select "Job Description" document type
   - Upload document file
   - Compare processing results

3. **Analyze Multiple Documents**
   - Upload several documents
   - Compare processing statistics
   - Review section extraction results

### 🎯 Success Criteria

- ✅ Support for PDF, DOCX, and TXT file uploads
- ✅ Clean text extraction with normalization
- ✅ Interactive dashboard with real-time processing
- ✅ Document preview and analysis features
- ✅ Processing statistics and visualizations
- ✅ Error handling and user feedback

---

**Milestone 1 Status**: ✅ **COMPLETED**

This milestone provides the foundation for the complete Gap Analysis System, enabling robust document ingestion and text preprocessing for subsequent NLP analysis phases.