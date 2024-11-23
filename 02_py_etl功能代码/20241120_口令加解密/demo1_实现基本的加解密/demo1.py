from pysmx.SM2 import Encrypt, Decrypt, generate_keypair, Sign, Verify
import chardet

# 生成公钥和私钥
pk, sk = generate_keypair()

# 检测公钥的编码（可选）
# ret = chardet.detect(pk)
# print(f'ret: {ret}')

# 打印公钥
print(f'公钥: {pk}')

# 将公钥写入文件
filepath = 'pk.key'
with open(filepath, 'wb') as binfile:
    binfile.write(pk)

# 将私钥写入文件
filepath = 'sk.key'
with open(filepath, 'wb') as binfile:
    binfile.write(sk)

# 打印私钥
print(f'私钥: {sk}')

# 签名示例
len_para = 64  # 参数长度
message = "你好"  # 待签名的消息
sig = Sign(message, sk, '12345678abcdef', len_para)  # 使用私钥签名

# 验签示例
print(Verify(sig, message, pk, len_para))  # 验证签名

# 加密示例
plaintext = '你好'.encode()  # 明文消息编码为字节
print(f'明文: {plaintext}')

# 从文件读取公钥
filepath = 'pk.key'
with open(filepath, 'rb') as binfile:
    pk = binfile.read()

len_para = 64  # 参数长度
c = Encrypt(plaintext, pk, len_para, Hexstr=0)  # 加密，Hexstr=0 表示输入不是16进制字符串
print(f'加密后的数据: {c}')

# 解密示例
m = Decrypt(c, sk, len_para)  # 使用私钥解密
print(f'解密后的明文: {m.decode()}')  # 解码为字符串并打印