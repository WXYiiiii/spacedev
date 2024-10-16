# 输入字符串
input_string = "a=yyyy"







# 将字符串拆分为键值对
pairs = input_string.split(',')

# 创建字典
result_dict = {}

# 遍历每个键值对并填充字典
for pair in pairs:
    key, value = pair.split('=')
    result_dict[key] = value

# 输出结果
print(result_dict)
try:
    result1 = result_dict[
        'b'
    ]
except KeyError:
    result1 = None
print(result1)