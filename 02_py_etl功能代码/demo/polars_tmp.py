import polars as pl

# 创建一个 DataFrame
df = pl.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["New York", "Los Angeles", "Chicago"]
})

# 显示 DataFrame
print(df)

# 选择特定列
ages = df.select("age")
print(ages)

# 过滤数据
filtered_df = df.filter(pl.col("age") > 28)
print(filtered_df)

# 聚合数据
average_age = df.select(pl.mean("age"))
print(average_age)