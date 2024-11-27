import os

def convert_crlf_to_lf(directory):
    # 遍历指定目录中的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.sh'):
                file_path = os.path.join(root, file)
                # 读取文件内容并转换换行符
                with open(file_path, 'rb') as f:
                    content = f.read()
                # 替换 CRLF 为 LF
                content = content.replace(b'\r\n', b'\n')
                # 写回文件
                with open(file_path, 'wb') as f:
                    f.write(content)
                print(f'Converted: {file_path}')

if __name__ == "__main__":
    # 指定要处理的目录（可以修改为你需要的目录）
    directory_to_process = './'
    convert_crlf_to_lf(directory_to_process)
    print("Conversion complete.")