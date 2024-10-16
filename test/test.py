
def dict_to_tuple(d):
    """
    将字典转换为元组，元组中的值是字典的value，不考虑字典的key
    
    参数:
    d (dict): 输入的字典
    
    返回:
    tuple: 包含字典value的元组
    """
    return tuple(d.values())

# 使用示例
if __name__ == "__main__":
    sample_dict = {"a": 1, "b": 2, "c": 3}
    result = dict_to_tuple(sample_dict)
    print(f"原始字典: {sample_dict}")
    print(f"转换后的元组: {result}")
