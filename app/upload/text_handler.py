def extract_text_from_txt(file: str) -> str:
    with open(file, "r", encoding="utf-8") as f:
        return f.read()