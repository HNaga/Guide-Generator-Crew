def sanitize_filename(name: str) -> str:
    """Replace invalid filename characters with empty string"""
    invalid_chars = r'<>:"/\|?*'
    for char in invalid_chars:
        name = name.replace(char, "")
    return name.strip().replace(" ", "_")