def sanitize_filename(name: str) -> str:
    """Replace invalid characters and spaces with safe ones"""
    invalid_chars = r'<>:"/\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    return name.strip().replace(' ', '_')