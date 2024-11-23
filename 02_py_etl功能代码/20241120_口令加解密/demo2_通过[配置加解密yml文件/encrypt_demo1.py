import yaml
from pysmx.SM2 import Encrypt, Decrypt, generate_keypair

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

    def load_config(self, config_file='A.yml'):
        """加载配置文件A"""
        with open(config_file, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def load_encryption_config(self, enc_config_file='B.yml'):
        """加载加密配置文件B"""
        with open(enc_config_file, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def encrypt_config(self, config):
        """根据B中的配置返回加密后的A"""
        enc_config = config.copy()  # 保留原始配置
        encryption_keys = self.load_encryption_config()

        for key in encryption_keys.get('encript', {}).get('A', []):
            if key in config:
                enc_config[key] = self.encrypt_message(config[key])  # 加密指定的键

        return enc_config

    def decrypt_config(self, enc_config):
        """解密配置并返回原始信息"""
        dec_config = enc_config.copy()  # 保留加密后的配置

        for key in enc_config.keys():
            if isinstance(enc_config[key], bytes):  # 检查是否是密文
                dec_config[key] = self.decrypt_message(enc_config[key])  # 解密

        return dec_config

# 使用示例
if __name__ == "__main__":
    sm2 = SM2Cryptography()  # 创建 SM2 加密对象
    sm2.save_keys()  # 保存生成的公钥和私钥

    # 加载配置A
    config_a = sm2.load_config('A.yml')
    print("原始配置:", config_a)

    # 加密配置A中的敏感信息
    encrypted_config = sm2.encrypt_config(config_a)
    print("加密后的配置:", encrypted_config)

    # 将加密后的配置写入新的YAML文件（可选）
    with open('encrypted_A.yml', 'w', encoding='utf-8') as file:
        yaml.dump(encrypted_config, file)

    # 解密配置
    decrypted_config = sm2.decrypt_config(encrypted_config)
    print("解密后的配置:", decrypted_config)