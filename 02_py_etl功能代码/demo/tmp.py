import os
import zipfile

def extract_zip_to_directory(zip_file_path):
    # 获取ZIP文件名（不带扩展名）
    zip_file_name = os.path.splitext(os.path.basename(zip_file_path))[0]

    # 创建与ZIP文件同名的目录
    extract_dir = os.path.join(os.path.dirname(zip_file_path), zip_file_name)
    os.makedirs(extract_dir, exist_ok=True)

    # 解压ZIP文件到指定目录
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        print(f"Extracted to: {extract_dir}")

        # 读取ZIP文件中的所有文件名
        for file_name in zip_ref.namelist():
            print(f"File in ZIP: {file_name}")

# 使用示例
if __name__ == "__main__":
    zip_file_path = 'example.zip'  # 替换为你的ZIP文件路径
    extract_zip_to_directory(zip_file_path)