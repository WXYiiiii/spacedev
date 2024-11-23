from pysmx.SM2 import Encrypt, Decrypt, generate_keypair, Sign, Verify
import chardet

class SM2Cryptography:
    def __init__(self):
        # 生成公钥和私钥
        self.pk, self.sk = generate_keypair()
        print(f'生成的公钥: {self.pk}')
        print(f'生成的私钥: {self.sk}')

    def save_keys(self, public_key_file='pk.key', private_key_file='sk.key'):
        """将公钥和私钥保存到文件"""
        with open(public_key_file, 'wb') as binfile:
            binfile.write(self.pk)
        with open(private_key_file, 'wb') as binfile:
            binfile.write(self.sk)
        print(f'公钥已保存到 {public_key_file}')
        print(f'私钥已保存到 {private_key_file}')

    def encrypt_message(self, plaintext):
        """加密消息"""
        len_para = 64  # 参数长度
        ciphertext = Encrypt(plaintext.encode(), self.pk, len_para, Hexstr=0)
        return ciphertext

    def decrypt_message(self, ciphertext):
        """解密消息"""
        len_para = 64  # 参数长度
        decrypted_message = Decrypt(ciphertext, self.sk, len_para)
        return decrypted_message.decode()

# 使用示例
if __name__ == "__main__":
    sm2 = SM2Cryptography()  # 创建 SM2 加密对象
    sm2.save_keys()  # 保存生成的公钥和私钥

    plaintext = "你好"
    ciphertext = sm2.encrypt_message(plaintext)  # 加密
    print(f'加密后的数据: {ciphertext}')

    decrypted_message = sm2.decrypt_message(ciphertext)  # 解密
    print(f'解密后的明文: {decrypted_message}')