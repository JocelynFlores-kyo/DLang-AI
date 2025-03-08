# 文档解析
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from docx import Document
from typing import List

def load_document(file_path: str) -> List[dict]:
    """统一文档加载入口"""
    if file_path.endswith(".docx") or file_path.endswith('.doc'):
        return _parse_docx(file_path)
    elif file_path.endswith(".pdf"):
        return _parse_pdf(file_path)
    else:
        raise ValueError("Unsupported file type")

def _parse_docx(file_path: str):
    """解析Word文档"""
    doc = Document(file_path)
    return [{"text": para.text, "metadata": {"source": file_path}} for para in doc.paragraphs]

def _parse_pdf(file_path: str):
    """解析PDF（自动处理文本/图片PDF）"""
    try:
        # 尝试文本PDF解析
        with pdfplumber.open(file_path) as pdf:
            pages = []
            for page in pdf.pages:
                text = page.extract_text()
                pages.append({
                    "text": text,
                    "metadata": {
                        "source": file_path,
                        "page": page.page_number,
                        "bbox": [0, 0, 1, 1]  # 示例坐标
                    }
                })
            return pages
    except:
        # 降级到OCR解析
        images = convert_from_path(file_path)
        return [{
            "text": pytesseract.image_to_string(img),
            "metadata": {
                "source": file_path,
                "page": i+1,
                "bbox": [0, 0, 1, 1]  # 示例坐标
            }
        } for i, img in enumerate(images)]