import yaml
import logging
from pysmx.SM2 import Decrypt, generate_keypair

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SM2Cryptography:
    def __init__(self, private_key_file='sk.key'):
        """加载私钥"""
        self.sk = self.load_private_key(private_key_file)
        logging.info(f'加载的私钥: {self.sk}')

    def load_private_key(self, filename):
        """从文件加载私钥"""
        with open(filename, 'rb') as binfile:
            return binfile.read()

    def decrypt_message(self, ciphertext):
        """解密消息"""
        len_para = 64  # 参数长度
        decrypted_message = Decrypt(ciphertext, self.sk, len_para)
        logging.info(f'解密消息: {ciphertext} -> {decrypted_message.decode()}')
        return decrypted_message.decode()

    def load_yaml(self, filename):
        """通用加载YAML文件函数"""
        with open(filename, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        logging.info(f'加载配置文件: {filename}')
        return config

    def decrypt_config(self, enc_config):
        """解密配置并返回原始信息"""
        dec_config = enc_config.copy()  # 保留加密后的配置

        for key in enc_config.keys():
            if isinstance(enc_config[key], bytes):  # 检查是否是密文
                dec_config[key] = self.decrypt_message(enc_config[key])  # 解密
            elif isinstance(enc_config[key], dict):  # 如果是字典，递归解密
                dec_config[key] = self.decrypt_config(enc_config[key])

        logging.info('解密配置完成')
        return dec_config

    def load_and_decrypt_encrypted_file(self, encrypted_filename):
        """加载加密后的YAML文件并返回解密后的结果"""
        encrypted_config = self.load_yaml(encrypted_filename)

        # 解密当前配置中的敏感信息
        decrypted_config = self.decrypt_config(encrypted_config)

        logging.info(f"解密后的配置 ({encrypted_filename}): {decrypted_config}")

        return decrypted_config

# 使用示例
if __name__ == "__main__":
    sm2 = SM2Cryptography()  # 创建 SM2 解密对象

    # 示例：读取并解密加密后的 A.yml 文件
    decrypted_result = sm2.load_and_decrypt_encrypted_file('A.yml')

    # 输出解密后的结果
    print(decrypted_result)