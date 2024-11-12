import pandas as pd
import matplotlib.pyplot as plt

# 创建初始 DataFrame
data = {
    '类型': ['个人', '企业', '个人', '企业'],
    '证件': ['1234567890', 'ABC123456', '9876543210', 'DEF987654'],
    'col_3': ['A', 'B', 'C', 'D'],
    'col_4': [1, 2, 3, 4]
}
df = pd.DataFrame(data)

# 加密过程（模拟）
df['证件'] = df.apply(lambda row: f'encrypted_{row.name + 1}' if row['类型'] == '个人' else row['证件'], axis=1)

# 可视化
plt.figure(figsize=(10,5))
plt.title('DataFrame变化过程')
plt.plot(df['类型'], label='类型', marker='o')
plt.plot(df['证件'], label='证件', marker='x')
plt.legend()
plt.show()