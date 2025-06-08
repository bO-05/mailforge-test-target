import docx
import re

def convert_docx_to_markdown(docx_path, md_path):
    # Open the .docx file
    doc = docx.Document(docx_path)

    # Initialize the Markdown content
    md_content = []

    # Iterate through each paragraph in the document
    for para in doc.paragraphs:
        # Convert paragraph text to Markdown
        md_para = convert_paragraph_to_markdown(para)
        md_content.append(md_para)

    # Write the Markdown content to a .md file
    with open(md_path, 'w', encoding='utf-8') as md_file:
        md_file.write('\n'.join(md_content))

def convert_paragraph_to_markdown(paragraph):
    # Initialize the Markdown paragraph
    md_para = paragraph.text

    # Convert headings
    if paragraph.style.name.startswith('Heading'):
        level = int(paragraph.style.name.split()[-1])
        md_para = f"{'#' * level} {md_para}"

    # Convert bold text
    for run in paragraph.runs:
        if run.bold:
            md_para = md_para.replace(run.text, f"**{run.text}**")

    # Convert italic text
    for run in paragraph.runs:
        if run.italic:
            md_para = md_para.replace(run.text, f"*{run.text}*")

    # Convert bullet points
    if paragraph.style.name == 'List Paragraph':
        md_para = f"- {md_para}"

    return md_para

# Example usage
if __name__ == "__main__":
    docx_path = 'example.docx'
    md_path = 'example.md'
    convert_docx_to_markdown(docx_path, md_path)