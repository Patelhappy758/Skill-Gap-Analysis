"""
Skill Gap Analysis System - Main Streamlit Application
Focused on document parsing and skill matching analysis
"""

import streamlit as st
import time
from typing import Optional, Tuple, List, Set
import re

# Import custom modules
from parser_pipeline import DocumentParser, get_parser
from text_cleaner import TextCleaner

# Configure Streamlit page
st.set_page_config(
    page_title="Skill Gap Analysis System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI/UX
def load_custom_css():
    """Load custom CSS for enhanced styling"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Global Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --tertiary-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        --warning-gradient: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        --glass-bg: rgba(255, 255, 255, 0.08);
        --glass-border: rgba(255, 255, 255, 0.2);
        --shadow-light: 0 8px 32px rgba(31, 38, 135, 0.37);
        --shadow-heavy: 0 15px 35px rgba(0, 0, 0, 0.2);
        --border-radius: 24px;
        --border-radius-sm: 16px;
        --transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
    }
    
    /* Main styling */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        min-height: 100vh;
        padding: 1rem;
    }
    
    /* Global backdrop blur effect */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='7' cy='7' r='7'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
        z-index: -1;
        opacity: 0.3;
    }
    
    /* Glassmorphism card base */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-light);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    }
    
    /* Custom header styling */
    .custom-header {
        background: var(--glass-bg);
        backdrop-filter: blur(30px);
        padding: 3rem 2rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: var(--shadow-heavy);
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }
    
    .custom-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
        z-index: 0;
    }
    
    .custom-header > * {
        position: relative;
        z-index: 1;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Upload container styling */
    .upload-container {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        padding: 2.5rem;
        border-radius: var(--border-radius);
        margin: 1.5rem 0;
        color: white;
        text-align: center;
        transition: var(--transition);
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }
    
    .upload-container::after {
        content: '';
        position: absolute;
        inset: -2px;
        background: var(--secondary-gradient);
        border-radius: var(--border-radius);
        z-index: -1;
        opacity: 0;
        transition: var(--transition);
    }
    
    .upload-container:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px rgba(240, 147, 251, 0.4);
    }
    
    .upload-container:hover::after {
        opacity: 0.1;
    }
    
    /* Data review container */
    .review-container {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        padding: 2.5rem;
        border-radius: var(--border-radius);
        margin: 1.5rem 0;
        color: white;
        box-shadow: var(--shadow-light);
        border: 1px solid var(--glass-border);
        position: relative;
    }
    
    .review-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--tertiary-gradient);
        border-radius: var(--border-radius) var(--border-radius) 0 0;
    }
    
    /* Analysis container */
    .analysis-container {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        padding: 2.5rem;
        border-radius: var(--border-radius);
        margin: 1.5rem 0;
        color: white;
        box-shadow: var(--shadow-light);
        border: 1px solid var(--glass-border);
        position: relative;
        animation: slideInUp 0.8s ease-out;
    }
    
    .analysis-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--success-gradient);
        border-radius: var(--border-radius) var(--border-radius) 0 0;
    }
    
    /* Enhanced Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(0, 0, 0, 0.2);
        padding: 6px;
        border-radius: var(--border-radius-sm);
        backdrop-filter: blur(15px);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
        border: none;
        padding: 12px 24px;
        transition: var(--transition);
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        inset: 0;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        opacity: 0;
        transition: var(--transition);
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.15);
        color: white;
        box-shadow: 0 4px 20px rgba(255, 255, 255, 0.15);
        transform: scale(1.05);
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        opacity: 1;
    }
    
    /* Enhanced Button styling */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: var(--border-radius-sm);
        padding: 1rem 3rem;
        font-weight: 600;
        font-size: 16px;
        transition: var(--transition);
        box-shadow: var(--shadow-light);
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: var(--transition);
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.5);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Skill cards with enhanced styling */
    .skill-match {
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: var(--border-radius-sm);
        margin: 0.8rem 0;
        border-left: 4px solid #38ef7d;
        border: 1px solid rgba(56, 239, 125, 0.3);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .skill-match::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #38ef7d, #11998e);
        animation: pulse 2s infinite;
    }
    
    .skill-match:hover {
        transform: translateX(8px);
        box-shadow: 0 10px 30px rgba(56, 239, 125, 0.3);
    }
    
    .skill-missing {
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: var(--border-radius-sm);
        margin: 0.8rem 0;
        border-left: 4px solid #ff6b6b;
        border: 1px solid rgba(255, 107, 107, 0.3);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .skill-missing::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #ff6b6b, #ee5a52);
        animation: pulse 2s infinite;
    }
    
    .skill-missing:hover {
        transform: translateX(8px);
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
    }
    
    /* Text areas styling */
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid var(--glass-border);
        border-radius: var(--border-radius-sm);
        color: white;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        line-height: 1.6;
        backdrop-filter: blur(10px);
        transition: var(--transition);
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(102, 126, 234, 0.8);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        outline: none;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: var(--border-radius-sm);
        background: rgba(0, 0, 0, 0.2);
        transition: var(--transition);
    }
    
    .stFileUploader > div > div:hover {
        border-color: rgba(102, 126, 234, 0.8);
        background: rgba(102, 126, 234, 0.1);
        transform: scale(1.02);
    }
    
    /* Metrics styling */
    .stMetric > div {
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border-radius: var(--border-radius-sm);
        border: 1px solid var(--glass-border);
        padding: 1.5rem;
        text-align: center;
        transition: var(--transition);
    }
    
    .stMetric > div:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-light);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(0,0,0,0.4), rgba(0,0,0,0.6));
        backdrop-filter: blur(20px);
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: var(--success-gradient);
        border: none;
        border-radius: var(--border-radius-sm);
        color: white;
        backdrop-filter: blur(15px);
    }
    
    .stError {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        border: none;
        border-radius: var(--border-radius-sm);
        color: white;
        backdrop-filter: blur(15px);
    }
    
    .stWarning {
        background: var(--warning-gradient);
        border: none;
        border-radius: var(--border-radius-sm);
        color: #333;
        backdrop-filter: blur(15px);
    }
    
    .stInfo {
        background: var(--tertiary-gradient);
        border: none;
        border-radius: var(--border-radius-sm);
        color: white;
        backdrop-filter: blur(15px);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(60px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.8s cubic-bezier(0.23, 1, 0.320, 1);
    }
    
    .animate-float {
        animation: float 6s ease-in-out infinite;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        
        .custom-header,
        .upload-container,
        .review-container,
        .analysis-container {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .stButton > button {
            padding: 0.8rem 2rem;
            font-size: 14px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'parsed_data' not in st.session_state:
        st.session_state.parsed_data = {}
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False

def sidebar_navigation():
    """Create simple sidebar navigation"""
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h2 style='color: #667eea;'>📊 Skill Gap Analysis</h2>
            <p style='color: #888;'>Document Parsing & Analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🧹 Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("Cache cleared!")
        
        if st.button("🔄 Reset Session", use_container_width=True):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

def document_upload_section():
    """Document upload section"""
    st.markdown("""
    <div class='custom-header animate-fade-in'>
        <h1>📊 Skill Gap Analysis System</h1>
        <p style='font-size: 1.2em; margin: 0; opacity: 0.9;'>
            Upload Resume and Job Description for Skill Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 📤 Upload Documents")
    
    # Create two columns for resume and job description
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class='upload-container'>
            <h3>📄 Upload Resume</h3>
            <p>Upload your resume for skill analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        resume_file = st.file_uploader(
            "Choose resume file",
            type=['pdf', 'docx', 'txt'],
            key="resume_uploader",
            help="Upload your resume in PDF, DOCX, or TXT format (Max: 200MB)"
        )
        
        if resume_file:
            st.success(f"✅ Resume uploaded: {resume_file.name}")
    
    with col2:
        st.markdown("""
        <div class='upload-container'>
            <h3>💼 Upload Job Description</h3>
            <p>Upload the target job description</p>
        </div>
        """, unsafe_allow_html=True)
        
        job_file = st.file_uploader(
            "Choose job description file",
            type=['pdf', 'docx', 'txt'],
            key="job_uploader",
            help="Upload job description in PDF, DOCX, or TXT format (Max: 200MB)"
        )
        
        if job_file:
            st.success(f"✅ Job description uploaded: {job_file.name}")
    
    # Manual text input section
    st.markdown("## ✏️ Or Enter Text Manually")
    
    col3, col4 = st.columns(2, gap="large")
    
    with col3:
        st.markdown("### 📝 Resume Text")
        resume_text = st.text_area(
            "Paste resume content here:",
            height=200,
            placeholder="Paste your resume text here...",
            key="resume_text"
        )
    
    with col4:
        st.markdown("### 📋 Job Description Text")
        job_text = st.text_area(
            "Paste job description here:",
            height=200,
            placeholder="Paste the job description here...",
            key="job_text"
        )
    
    return resume_file, job_file, resume_text, job_text

def process_documents(parser, resume_file, job_file, resume_text, job_text):
    """Process uploaded documents and text"""
    
    if not any([resume_file, job_file, resume_text, job_text]):
        st.warning("⚠️ Please upload files or enter text manually before processing.")
        return None
    
    # Processing indicator
    with st.spinner("🔄 Processing documents..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = {
            'resume': {'raw': '', 'cleaned': ''},
            'job': {'raw': '', 'cleaned': ''}
        }
        
        # Process resume
        status_text.text("📄 Processing resume...")
        progress_bar.progress(25)
        
        if resume_file:
            file_path = parser.save_uploaded_file(resume_file)
            if file_path:
                raw, cleaned, _ = parser.extract_text_auto(file_path)
                results['resume'] = {'raw': raw, 'cleaned': cleaned}
        elif resume_text:
            raw, cleaned, _ = parser.process_text_input(resume_text, "resume")
            results['resume'] = {'raw': raw, 'cleaned': cleaned}
        
        progress_bar.progress(50)
        
        # Process job description
        status_text.text("💼 Processing job description...")
        progress_bar.progress(75)
        
        if job_file:
            file_path = parser.save_uploaded_file(job_file)
            if file_path:
                raw, cleaned, _ = parser.extract_text_auto(file_path)
                results['job'] = {'raw': raw, 'cleaned': cleaned}
        elif job_text:
            raw, cleaned, _ = parser.process_text_input(job_text, "job_description")
            results['job'] = {'raw': raw, 'cleaned': cleaned}
        
        progress_bar.progress(100)
        status_text.text("✅ Processing complete!")
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
    
    return results

def extract_skills_simple(text: str) -> Set[str]:
    """Simple skill extraction using keyword matching"""
    # Common technical skills and keywords
    skill_patterns = [
        # Programming languages
        r'\bpython\b', r'\bjava\b', r'\bc#\b', r'\bc\+\+\b', r'\bjavascript\b', r'\bhtml\b', r'\bcss\b',
        r'\bsql\b', r'\br\b', r'\bscala\b', r'\bruby\b', r'\bphp\b', r'\bgo\b', r'\brust\b',
        
        # Frameworks and libraries
        r'\breact\b', r'\bangular\b', r'\bvue\b', r'\bdjango\b', r'\bflask\b', r'\bspring\b',
        r'\bnode\.?js\b', r'\bexpress\b', r'\btensorflow\b', r'\bpytorch\b', r'\bnumpy\b', r'\bpandas\b',
        
        # Tools and platforms
        r'\bgit\b', r'\bdocker\b', r'\bkubernetes\b', r'\baws\b', r'\bazure\b', r'\bgcp\b',
        r'\blinux\b', r'\bwindows\b', r'\bmysql\b', r'\bpostgresql\b', r'\bmongodb\b',
        
        # Skills and concepts
        r'\bmachine\s+learning\b', r'\bdata\s+science\b', r'\bartificial\s+intelligence\b',
        r'\bweb\s+development\b', r'\bfull\s+stack\b', r'\bapi\b', r'\bretful?\b', r'\bmicroservices\b',
        r'\bagile\b', r'\bscrum\b', r'\bdevops\b', r'\bci/cd\b', r'\btesting\b', r'\bdebugging\b'
    ]
    
    skills = set()
    text_lower = text.lower()
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        skills.update(match.strip() for match in matches)
    
    # Clean up and filter skills
    cleaned_skills = set()
    for skill in skills:
        if len(skill) > 1 and skill not in ['a', 'an', 'the', 'is', 'are', 'was', 'were']:
            cleaned_skills.add(skill.title())
    
    return cleaned_skills

def skill_analysis_section(results):
    """Skill analysis and comparison section"""
    if not results or not (results['resume']['cleaned'] and results['job']['cleaned']):
        return
    
    st.markdown("""
    <div class='analysis-container animate-fade-in'>
        <h2>🔍 Skill Analysis & Matching</h2>
        <p style='font-size: 1.1em; opacity: 0.9;'>
            Compare skills from resume and job description
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Extract skills
    resume_skills = extract_skills_simple(results['resume']['cleaned'])
    job_skills = extract_skills_simple(results['job']['cleaned'])
    
    # Calculate matches
    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills
    extra_skills = resume_skills - job_skills
    
    # Display statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Resume Skills", len(resume_skills))
    
    with col2:
        st.metric("Job Requirements", len(job_skills))
    
    with col3:
        st.metric("Matched Skills", len(matched_skills))
    
    with col4:
        match_percentage = (len(matched_skills) / len(job_skills) * 100) if job_skills else 0
        st.metric("Match Rate", f"{match_percentage:.1f}%")
    
    # Skill comparison tabs
    skill_tabs = st.tabs(["🎯 Matched Skills", "❌ Missing Skills", "➕ Additional Skills"])
    
    with skill_tabs[0]:
        st.subheader("Skills You Have That Match Job Requirements")
        if matched_skills:
            for skill in sorted(matched_skills):
                st.markdown(f"""
                <div class='skill-match'>
                    ✅ <strong>{skill}</strong>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No matching skills found. Consider reviewing your resume or the job requirements.")
    
    with skill_tabs[1]:
        st.subheader("Skills Required But Missing from Resume")
        if missing_skills:
            for skill in sorted(missing_skills):
                st.markdown(f"""
                <div class='skill-missing'>
                    ❌ <strong>{skill}</strong> - Consider learning this skill
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Great! You have all the required skills mentioned in the job description.")
    
    with skill_tabs[2]:
        st.subheader("Additional Skills You Have")
        if extra_skills:
            for skill in sorted(extra_skills):
                st.markdown(f"💡 **{skill}** - This could be a bonus skill!")
        else:
            st.info("No additional skills identified beyond job requirements.")

def data_review_section(results):
    """Data review section for raw and cleaned content"""
    if not results:
        return
    
    st.markdown("""
    <div class='review-container animate-fade-in'>
        <h2>📋 Document Content Review</h2>
        <p style='font-size: 1.1em; opacity: 0.9;'>
            Review the raw and cleaned document content
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Document tabs
    doc_tabs = st.tabs(["📄 Resume Content", "💼 Job Description Content"])
    
    with doc_tabs[0]:
        if results['resume']['raw']:
            review_single_document("Resume", results['resume']['raw'], results['resume']['cleaned'])
        else:
            st.info("No resume data available for review.")
    
    with doc_tabs[1]:
        if results['job']['raw']:
            review_single_document("Job Description", results['job']['raw'], results['job']['cleaned'])
        else:
            st.info("No job description data available for review.")

def review_single_document(doc_name, raw_text, cleaned_text):
    """Review a single document with raw and cleaned versions"""
    
    # Content tabs
    content_tabs = st.tabs(["📝 Raw Text", "✨ Cleaned Text"])
    
    with content_tabs[0]:
        st.markdown(f"#### Raw {doc_name} Content")
        st.text_area(
            f"Original {doc_name.lower()} text:",
            value=raw_text,
            height=400,
            key=f"raw_{doc_name.lower().replace(' ', '_')}",
            help="This is the original extracted text before any cleaning"
        )
        
        # Download option
        st.download_button(
            f"💾 Download Raw {doc_name}",
            data=raw_text,
            file_name=f"raw_{doc_name.lower().replace(' ', '_')}.txt",
            mime="text/plain"
        )
    
    with content_tabs[1]:
        st.markdown(f"#### Cleaned {doc_name} Content")
        st.text_area(
            f"Processed {doc_name.lower()} text:",
            value=cleaned_text,
            height=400,
            key=f"cleaned_{doc_name.lower().replace(' ', '_')}",
            help="This is the cleaned and processed text ready for analysis"
        )
        
        # Download option
        st.download_button(
            f"💾 Download Cleaned {doc_name}",
            data=cleaned_text,
            file_name=f"cleaned_{doc_name.lower().replace(' ', '_')}.txt",
            mime="text/plain"
        )

def main():
    """Main application function"""
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Initialize parser
    parser = get_parser()
    
    # Sidebar navigation
    sidebar_navigation()
    
    # Document upload and parsing section
    resume_file, job_file, resume_text, job_text = document_upload_section()
    
    # Processing section
    st.markdown("## 🚀 Process Documents")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🔄 Parse Documents & Analyze Skills", use_container_width=True, type="primary"):
            results = process_documents(parser, resume_file, job_file, resume_text, job_text)
            
            if results:
                st.session_state.parsed_data = results
                st.session_state.processing_complete = True
                st.success("✅ Documents processed successfully!")
                st.balloons()
    
    # Show results if processing is complete
    if st.session_state.processing_complete and st.session_state.parsed_data:
        # Skill analysis section
        skill_analysis_section(st.session_state.parsed_data)
        
        # Data review section
        data_review_section(st.session_state.parsed_data)

if __name__ == "__main__":
    main()