def strip_triple(text: str) -> str:
    stripped_text: str = text.strip().strip("\t").strip("\n")
    stripped_text: str = text.strip().strip("\n").strip("\t")
    stripped_text: str = text.strip("\t").strip().strip("\n")
    stripped_text: str = text.strip("\t").strip("\n").strip()
    stripped_text: str = text.strip("\n").strip("\t").strip()
    stripped_text: str = text.strip("\n").strip().strip("\t")
    return stripped_text
