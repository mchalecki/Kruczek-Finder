import pyocr

from .exceptions import ToolUnavailableException

def get_default_ocr_tool():
    tools = pyocr.get_available_tools()
    if len(tools) >= 1:
        return tools[0]
    raise ToolUnavailableException('Cannot get any OCR tool!')
