#!/usr/bin/env python3
"""
Quick Demo Script for Milestone 1: Data Ingestion and Parsing Module
Shows document processing capabilities with sample files
"""

import os
import sys
sys.path.append('utils')

from file_processors import document_processor, text_cleaner


def demo_document_processing():
    """Demonstrate document processing with sample files."""
    print("🎯 MILESTONE 1 DEMO: Data Ingestion and Parsing Module")
    print("=" * 70)
    print("📊 Resume-Job Description Gap Analysis System")
    print("🔧 Document Upload, Parsing & Text Extraction")
    print("=" * 70)
    
    # Sample files to process
    sample_files = [
        {
            'path': 'source/sample_resume.txt',
            'type': '.txt',
            'description': 'Text Resume'
        },
        {
            'path': 'source/sample_resume_pdf.pdf', 
            'type': '.pdf',
            'description': 'PDF Resume'
        },
        {
            'path': 'source/sample_resume_doc.docx',
            'type': '.docx', 
            'description': 'Word Document Resume'
        }
    ]
    
    results = []
    
    for file_info in sample_files:
        print(f"\n📄 Processing {file_info['description']}")
        print("-" * 50)
        
        if not os.path.exists(file_info['path']):
            print(f"⚠️  File not found: {file_info['path']}")
            continue
        
        # Extract text
        extraction_result = document_processor.extract_text(file_path=file_info['path'])
        
        if extraction_result['success']:
            # Clean text
            cleaning_result = text_cleaner.clean_and_normalize(extraction_result['text'])
            
            # Extract sections
            sections = text_cleaner.extract_sections(cleaning_result['cleaned_text'])
            sections_found = [k for k, v in sections.items() if v.strip()]
            
            # Store results
            result = {
                'file': file_info['description'],
                'success': True,
                'chars_original': len(extraction_result['text']),
                'chars_cleaned': len(cleaning_result['cleaned_text']),
                'words': cleaning_result['cleaning_stats']['words_count'],
                'sections': sections_found,
                'metadata': extraction_result['metadata']
            }
            results.append(result)
            
            print(f"✅ Successfully processed {file_info['description']}")
            print(f"   📊 Original: {result['chars_original']:,} characters")
            print(f"   🧹 Cleaned:  {result['chars_cleaned']:,} characters")
            print(f"   📝 Words:    {result['words']:,}")
            print(f"   📋 Sections: {', '.join(sections_found) if sections_found else 'None identified'}")
            
            # Show preview
            preview = cleaning_result['cleaned_text'][:150] + "..." if len(cleaning_result['cleaned_text']) > 150 else cleaning_result['cleaned_text']
            print(f"   👁️  Preview:  {preview}")
            
        else:
            print(f"❌ Failed to process {file_info['description']}: {extraction_result['error']}")
            results.append({
                'file': file_info['description'],
                'success': False,
                'error': extraction_result['error']
            })
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 PROCESSING SUMMARY")
    print("=" * 70)
    
    successful = [r for r in results if r.get('success', False)]
    failed = [r for r in results if not r.get('success', False)]
    
    print(f"✅ Successfully processed: {len(successful)} files")
    print(f"❌ Failed to process: {len(failed)} files")
    
    if successful:
        total_chars_original = sum(r['chars_original'] for r in successful)
        total_chars_cleaned = sum(r['chars_cleaned'] for r in successful)
        total_words = sum(r['words'] for r in successful)
        
        print(f"\n📈 TOTAL STATISTICS:")
        print(f"   📊 Original text: {total_chars_original:,} characters")
        print(f"   🧹 Cleaned text:  {total_chars_cleaned:,} characters")
        print(f"   📝 Total words:   {total_words:,}")
        print(f"   🔄 Cleaning efficiency: {((total_chars_original - total_chars_cleaned) / total_chars_original * 100):.1f}% reduction")
        
        # File type breakdown
        print(f"\n📁 FILE TYPE BREAKDOWN:")
        for result in successful:
            file_type = result['metadata'].get('file_type', 'Unknown')
            print(f"   {file_type}: {result['words']:,} words, {result['chars_cleaned']:,} chars")
    
    print("\n" + "=" * 70)
    print("🎯 MILESTONE 1 COMPLETED SUCCESSFULLY!")
    print("📋 Ready for Milestone 2: Skill Extraction using NLP")
    print("=" * 70)


def demo_text_cleaning():
    """Demonstrate text cleaning capabilities."""
    print("\n🧪 TEXT CLEANING DEMONSTRATION")
    print("=" * 50)
    
    test_cases = [
        "John    Doe\nEmail:  john@email.com\n\n\nSkills: Python,   Java,    SQL",
        "PROFESSIONAL   SUMMARY\n\nExperienced developer with 5+ years...",
        "Education:\n• Bachelor's Degree\n• Master's Degree\n\nCertifications:\n• AWS Certified"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n📝 Example {i}:")
        print(f"Original: {repr(text[:50])}...")
        
        result = text_cleaner.clean_and_normalize(text)
        print(f"Cleaned:  {repr(result['cleaned_text'][:50])}...")
        print(f"Stats:    {result['cleaning_stats']['words_count']} words, {result['cleaning_stats']['special_chars_removed']} special chars removed")


if __name__ == "__main__":
    demo_document_processing()
    demo_text_cleaning()