import zipfile
import os
import time  # 导入 time 模块
import inspect

print(inspect.getsource(zipfile.ZipFile.extractall))


# 列出包中的所有内容
# print(dir(zipfile))
# print(dir(os))
# print(dir(time))


# print(zipfile.__all__)



# 查看包的文件路径
# print(zipfile.__file__)



# print(zipfile.__doc__)