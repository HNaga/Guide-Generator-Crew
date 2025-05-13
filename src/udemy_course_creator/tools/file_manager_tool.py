import os

def save_file(path, filename, content):
    """Saves content to a file using UTF-8 encoding"""
    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, filename)
    
    with open(full_path, 'w', encoding='utf-8', errors='utf-8-sig') as f:
        f.write(content)

    return full_path

def organize_assets(curriculum_data):
    print("Organizing assets...")
    # Implement logic to move files into correct folders