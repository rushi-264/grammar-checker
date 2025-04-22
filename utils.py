import PyPDF2
import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "".join([page.extract_text() for page in reader.pages if page.extract_text()])

def check_grammar(text):
    matches = tool.check(text)
    return matches

def correct_text(text, matches):
    return language_tool_python.utils.correct(text, matches)

def highlight_text(text, matches):
    highlighted = ""
    last_index = 0
    for match in sorted(matches, key=lambda m: m.offset):
        start = match.offset
        end = match.offset + match.errorLength
        highlighted += text[last_index:start]
        highlighted += f"<span style='background-color: #ffcccb;' title='{match.message}'>{text[start:end]}</span>"
        last_index = end
    highlighted += text[last_index:]
    return highlighted
