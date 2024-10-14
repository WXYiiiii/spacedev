import os
import re

# 定义搜索目录
search_directory = './'  # 当前目录

# 定义正则表达式
pattern = re.compile(r'.*\.txt$')  # 匹配以 .txt 结尾的文件

# 遍历目录及子目录
for root, dirs, files in os.walk(search_directory):
    for file in files:
        if pattern.match(file):
            # 打印符合条件的文件路径
            file_path = os.path.join(root, file)
            print(file_path)