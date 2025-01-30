def read_markdown_file(file: str) -> str:
    """Read a markdown file and return its content.

    Args:
        file (str): The path to the markdown file.

    Returns:
        str: The content of the markdown file.
    """
    with open(file=file, mode="r") as markdown_file:
        return markdown_file.read()
