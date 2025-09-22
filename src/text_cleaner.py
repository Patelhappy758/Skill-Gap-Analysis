"""
Enhanced Text Cleaning Module
Provides comprehensive text cleaning and normalization functions
"""

import re
from typing import List, Callable, Dict, Tuple
import streamlit as st


class TextCleaner:
    """Enhanced text cleaning utility class"""
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace characters in text
        Args:
            text (str): Input text
        Returns:
            str: Text with normalized whitespace
        """
        if not text:
            return ""
        
        # Convert different line endings to \n
        text = re.sub(r"\r\n|\r", "\n", text)
        
        # Replace non-breaking spaces with regular spaces
        text = re.sub(r"\u00a0", " ", text)
        
        # Replace multiple tabs with single space
        text = re.sub(r"\t+", " ", text)
        
        # Replace multiple spaces with single space
        text = re.sub(r"\s+", " ", text)
        
        return text.strip()

    @staticmethod
    def remove_emails(text: str) -> str:
        """
        Remove email addresses from text
        Args:
            text (str): Input text
        Returns:
            str: Text with emails removed
        """
        email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        return re.sub(email_pattern, " ", text)

    @staticmethod
    def remove_urls(text: str) -> str:
        """
        Remove URLs from text
        Args:
            text (str): Input text
        Returns:
            str: Text with URLs removed
        """
        url_pattern = r"https?://\S+|www\.\S+"
        return re.sub(url_pattern, " ", text)

    @staticmethod
    def remove_phone_numbers(text: str) -> str:
        """
        Remove phone numbers from text
        Args:
            text (str): Input text
        Returns:
            str: Text with phone numbers removed
        """
        phone_patterns = [
            r"\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}",
            r"\+?[0-9]{1,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}"
        ]
        for pattern in phone_patterns:
            text = re.sub(pattern, " ", text)
        return text

    @staticmethod
    def dehyphenate_line_breaks(text: str) -> str:
        """
        Fix hyphenated line breaks
        Args:
            text (str): Input text
        Returns:
            str: Text with dehyphenated line breaks
        """
        if not text:
            return ""
        return re.sub(r"-\n\s*", "", text)

    @staticmethod
    def normalize_punctuation(text: str) -> str:
        """
        Remove excessive punctuation
        Args:
            text (str): Input text
        Returns:
            str: Text with normalized punctuation
        """
        # Replace multiple periods with single period
        text = re.sub(r"\.{2,}", ".", text)
        
        # Replace multiple exclamation marks
        text = re.sub(r"!{2,}", "!", text)
        
        # Replace multiple question marks
        text = re.sub(r"\?{2,}", "?", text)
        
        return text

    @staticmethod
    def remove_social_handles(text: str) -> str:
        """
        Remove social media handles and hashtags
        Args:
            text (str): Input text
        Returns:
            str: Text with social handles removed
        """
        # Remove @mentions and #hashtags
        text = re.sub(r"@\w+", " ", text)
        text = re.sub(r"#\w+", " ", text)
        
        # Remove LinkedIn, GitHub, Twitter profile patterns
        text = re.sub(r"linkedin\.com/in/\S+", " ", text, flags=re.IGNORECASE)
        text = re.sub(r"github\.com/\S+", " ", text, flags=re.IGNORECASE)
        text = re.sub(r"twitter\.com/\S+", " ", text, flags=re.IGNORECASE)
        
        return text

    @staticmethod
    def remove_special_characters(text: str, keep_basic: bool = True) -> str:
        """
        Remove special characters from text
        Args:
            text (str): Input text
            keep_basic (bool): Keep basic punctuation (.,!?-:;)
        Returns:
            str: Text with special characters removed
        """
        if keep_basic:
            # Keep alphanumeric, basic punctuation, and whitespace
            text = re.sub(r"[^a-zA-Z0-9\s.,!?;:\-()]", " ", text)
        else:
            # Keep only alphanumeric and whitespace
            text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        
        return text

    @classmethod
    def basic_clean(cls, text: str) -> str:
        """
        Basic cleaning pipeline
        Args:
            text (str): Input text
        Returns:
            str: Cleaned text
        """
        transformations: List[Callable[[str], str]] = [
            cls.dehyphenate_line_breaks,
            cls.remove_urls,
            cls.remove_emails,
            cls.normalize_whitespace,
        ]

        cleaned_text = text or ""
        
        for transform in transformations:
            cleaned_text = transform(cleaned_text)
        
        return cleaned_text

    @classmethod
    def advanced_clean(cls, text: str) -> str:
        """
        Advanced cleaning pipeline with additional transformations
        Args:
            text (str): Input text
        Returns:
            str: Thoroughly cleaned text
        """
        transformations: List[Callable[[str], str]] = [
            cls.dehyphenate_line_breaks,
            cls.remove_urls,
            cls.remove_emails,
            cls.remove_phone_numbers,
            cls.remove_social_handles,
            cls.normalize_punctuation,
            lambda x: cls.remove_special_characters(x, keep_basic=True),
            cls.normalize_whitespace,
        ]

        cleaned_text = text or ""
        
        for transform in transformations:
            cleaned_text = transform(cleaned_text)
        
        return cleaned_text

    @classmethod
    def get_cleaning_stats(cls, original_text: str, cleaned_text: str) -> Dict[str, any]:
        """
        Get cleaning statistics
        Args:
            original_text (str): Original text
            cleaned_text (str): Cleaned text
        Returns:
            dict: Statistics about the cleaning process
        """
        original_length = len(original_text)
        cleaned_length = len(cleaned_text)
        
        if original_length == 0:
            reduction_percentage = 0
        else:
            reduction_percentage = round((original_length - cleaned_length) / original_length * 100, 1)

        return {
            'original_length': original_length,
            'cleaned_length': cleaned_length,
            'characters_removed': original_length - cleaned_length,
            'reduction_percentage': f"{reduction_percentage}%",
            'original_lines': len(original_text.split('\n')),
            'cleaned_lines': len(cleaned_text.split('\n')),
            'original_words': len(original_text.split()),
            'cleaned_words': len(cleaned_text.split())
        }

    @classmethod
    def preview_transformations(cls, text: str) -> Dict[str, str]:
        """
        Preview cleaning transformations step by step
        Args:
            text (str): Input text
        Returns:
            dict: Preview of each transformation step
        """
        steps = {}
        current_text = text or ""

        steps['original'] = current_text
        steps['dehyphenated'] = cls.dehyphenate_line_breaks(current_text)
        steps['urls_removed'] = cls.remove_urls(steps['dehyphenated'])
        steps['emails_removed'] = cls.remove_emails(steps['urls_removed'])
        steps['phones_removed'] = cls.remove_phone_numbers(steps['emails_removed'])
        steps['social_removed'] = cls.remove_social_handles(steps['phones_removed'])
        steps['punctuation_normalized'] = cls.normalize_punctuation(steps['social_removed'])
        steps['special_chars_removed'] = cls.remove_special_characters(steps['punctuation_normalized'])
        steps['whitespace_normalized'] = cls.normalize_whitespace(steps['special_chars_removed'])

        return steps

    @classmethod
    def create_cleaning_demo(cls):
        """
        Create an interactive Streamlit demo for text cleaning
        """
        st.subheader("🧹 Text Cleaning Demo")
        
        # Sample text for demo
        sample_text = """John Doe
Email: john.doe@example.com
Phone: +1-234-567-8901
LinkedIn: https://linkedin.com/in/johndoe
GitHub: github.com/johndoe

Professional    Summary:
Machine-
learning expert with 5+ years experience!!!

Skills: Python, SQL, @DataScience #MachineLearning"""

        # Text input
        input_text = st.text_area(
            "Enter text to clean:",
            value=sample_text,
            height=200,
            help="Paste any text here to see the cleaning transformations"
        )

        if input_text:
            # Cleaning options
            col1, col2 = st.columns(2)
            
            with col1:
                cleaning_type = st.radio(
                    "Choose cleaning type:",
                    ["Basic Clean", "Advanced Clean", "Step-by-Step Preview"]
                )
            
            with col2:
                show_stats = st.checkbox("Show cleaning statistics", value=True)

            if cleaning_type == "Step-by-Step Preview":
                st.subheader("📋 Transformation Steps")
                
                steps = cls.preview_transformations(input_text)
                
                for step_name, step_text in steps.items():
                    with st.expander(f"Step: {step_name.replace('_', ' ').title()}", expanded=False):
                        st.code(step_text[:500] + "..." if len(step_text) > 500 else step_text)
            
            else:
                # Apply cleaning
                if cleaning_type == "Basic Clean":
                    cleaned_text = cls.basic_clean(input_text)
                else:
                    cleaned_text = cls.advanced_clean(input_text)
                
                # Display results
                st.subheader("✨ Cleaned Result")
                st.text_area("Cleaned text:", value=cleaned_text, height=200)
                
                if show_stats:
                    stats = cls.get_cleaning_stats(input_text, cleaned_text)
                    
                    st.subheader("📊 Cleaning Statistics")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Characters", stats['cleaned_length'], 
                                delta=f"-{stats['characters_removed']}")
                    
                    with col2:
                        st.metric("Words", stats['cleaned_words'], 
                                delta=f"{stats['cleaned_words'] - stats['original_words']}")
                    
                    with col3:
                        st.metric("Lines", stats['cleaned_lines'], 
                                delta=f"{stats['cleaned_lines'] - stats['original_lines']}")
                    
                    with col4:
                        st.metric("Reduction", stats['reduction_percentage'])


if __name__ == "__main__":
    # Demo usage
    sample = (
        "Email: john.doe@example.com\nLinkedIn: https://linkedin.com/in/john\n"
        "Machine-\nlearning, data\tScience\n\n  Skills: Python, SQL"
    )
    
    cleaner = TextCleaner()
    basic_result = cleaner.basic_clean(sample)
    advanced_result = cleaner.advanced_clean(sample)
    
    print("Original:", repr(sample))
    print("\nBasic Clean:", repr(basic_result))
    print("\nAdvanced Clean:", repr(advanced_result))
    
    stats = cleaner.get_cleaning_stats(sample, advanced_result)
    print("\nCleaning Stats:", stats)