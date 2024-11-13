import uuid

# 生成 UUID1
uuid1 = uuid.uuid1()
print("UUID1:", uuid1)
print("UUID1:", type(uuid1))
print("UUID1:", len(str(uuid1)))

# 生成 UUID3
uuid3 = uuid.uuid3(uuid.NAMESPACE_DNS, 'example.com')
print("UUID3:", uuid3)


# 生成 UUID4
uuid4 = uuid.uuid4()
print("UUID4:", uuid4)

# 生成 UUID5
uuid5 = uuid.uuid5(uuid.NAMESPACE_DNS, 'example.com')
print("UUID5:", uuid5)


