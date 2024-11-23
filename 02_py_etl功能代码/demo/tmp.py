import re

# 示例字符串
data = ("""value1;
        value2;   
        value3;  
        value4;
        value5;
        value6;
        """)

# 使用正则表达式分割字符串，处理 ; 和 \n 之间的空格
result = re.split(r'\s*;\s*\n', data)

# 打印结果
print(result)