import os

def read_txt(file_path):
    """
    Returns:
        str: Extracted text content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print("Successfully read file")
            return content

    except FileNotFoundError:
        print("❌ File not found")
        return ""

    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read()
                print("✅ File read with latin-1 encoding")
                return content
        except Exception as e:
            print(f"❌ Error reading file with latin-1: {e}")
            return ""

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return ""

if __name__ == "__main__":
    txt_content = read_txt("sample_description.txt")
    print("\nTXT Content Preview:")
    print(txt_content[:200] + "..." if len(txt_content) > 200 else txt_content)
