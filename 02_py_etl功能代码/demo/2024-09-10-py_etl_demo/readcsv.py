# 原始字符串
original_string = "rpt_xxx_yyy_m"

# 分割字符串
# parts = original_string.split('_')

# 获取中间部分
result = '_'.join(original_string.split('_')[1:-1])

print(result)  # 输出: xxx_yyy