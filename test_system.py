"""
Test script for Milestone 1 functionality
Tests document processing pipeline with sample files
"""

import os
import sys
sys.path.append('utils')

from file_processors import document_processor, text_cleaner


def test_document_processing():
    """Test document processing with sample files."""
    print("🧪 Testing Milestone 1: Document Processing Pipeline")
    print("=" * 60)
    
    # Test files
    test_files = [
        ('source/sample_resume.txt', '.txt'),
        ('source/sample_resume_pdf.pdf', '.pdf'),
        ('source/sample_resume_doc.docx', '.docx')
    ]
    
    for file_path, file_type in test_files:
        print(f"\n📄 Testing {file_type.upper()} file: {file_path}")
        print("-" * 40)
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
        
        # Test text extraction
        result = document_processor.extract_text(file_path=file_path)
        
        if result['success']:
            print(f"✅ Text extraction successful")
            print(f"   - Extracted {len(result['text'])} characters")
            print(f"   - Metadata: {result['metadata']}")
            
            # Test text cleaning
            cleaned = text_cleaner.clean_and_normalize(result['text'])
            print(f"✅ Text cleaning successful")
            print(f"   - Original: {cleaned['original_length']} chars")
            print(f"   - Cleaned: {cleaned['cleaned_length']} chars")
            print(f"   - Words: {cleaned['cleaning_stats']['words_count']}")
            
            # Test section extraction
            sections = text_cleaner.extract_sections(cleaned['cleaned_text'])
            sections_with_content = {k: v for k, v in sections.items() if v.strip()}
            print(f"✅ Section extraction successful")
            print(f"   - Found sections: {list(sections_with_content.keys())}")
            
            # Show preview
            preview = result['text'][:200] + "..." if len(result['text']) > 200 else result['text']
            print(f"\n📝 Text Preview:")
            print(f"   {preview}")
            
        else:
            print(f"❌ Text extraction failed: {result['error']}")
    
    print("\n" + "=" * 60)
    print("✅ Document processing pipeline test completed!")


def test_text_cleaning_edge_cases():
    """Test text cleaning with various edge cases."""
    print("\n🧪 Testing Text Cleaning Edge Cases")
    print("=" * 60)
    
    test_cases = [
        ("", "Empty string"),
        ("   Multiple    spaces   everywhere   ", "Multiple spaces"),
        ("Text with special chars @#$%^&*()", "Special characters"),
        ("Line1\n\n\nLine2\n\nLine3", "Multiple newlines"),
        ("Text...with...dots...", "Multiple dots"),
        ("Text , with , spacing , issues", "Punctuation spacing")
    ]
    
    for text, description in test_cases:
        print(f"\n📝 Testing: {description}")
        print(f"   Original: '{text}'")
        
        result = text_cleaner.clean_and_normalize(text)
        print(f"   Cleaned:  '{result['cleaned_text']}'")
        print(f"   Stats: {result['cleaning_stats']}")


if __name__ == "__main__":
    test_document_processing()
    test_text_cleaning_edge_cases()