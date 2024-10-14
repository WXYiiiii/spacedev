# # 导入 datetime 模块
# import datetime
#
# # 获取当前日期
# current_date = datetime.datetime.now().date()
#
# # 打印当前日期
# print("当前日期是:", current_date)

# ------------------
# import random
# import string
#
# # 定义字符集，包括大写字母、小写字母和数字
# characters = string.ascii_letters + string.digits
#
# # 生成32位随机字符串
# random_string = ''.join(random.choice(characters) for _ in range(32))
#
# print(random_string)


# ------------------
from datetime import datetime

# 获取当前日期和时间
# now = datetime.now()

# 格式化日期和时间
formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print(formatted_time)





