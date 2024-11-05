import pytesseract
from PIL import Image

# 指定Tesseract-OCR的路径（Windows系统需要）   // 安装链接 https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_python_code(image_path):
    # 打开图片
    image = Image.open(image_path)

    # 使用pytesseract进行OCR识别
    text = pytesseract.image_to_string(image, lang='eng')

    # 返回识别到的文本
    return text


if __name__ == "__main__":
    # 替换为你的图片路径
    image_path = './data/241016-识别图片中的文字.png'

    code = extract_python_code(image_path)

    print("识别到的Python代码：")
    print(code)
