import yaml
import logging
from pysmx.SM2 import Encrypt, Decrypt, generate_keypair

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SM2Cryptography:
    def __init__(self):
        """生成公钥和私钥"""
        self.pk, self.sk = generate_keypair()
        logging.info(f'生成的公钥: {self.pk}')
        logging.info(f'生成的私钥: {self.sk}')

    def save_keys(self, public_key_file='pk.key', private_key_file='sk.key'):
        """将公钥和私钥保存到文件"""
        self._save_to_file(public_key_file, self.pk)
        self._save_to_file(private_key_file, self.sk)

    def _save_to_file(self, filename, data):
        """通用保存函数"""
        with open(filename, 'wb') as binfile:
            binfile.write(data)
        logging.info(f'数据已保存到 {filename}')

    def encrypt_message(self, plaintext):
        """加密消息"""
        len_para = 64  # 参数长度
        ciphertext = Encrypt(plaintext.encode(), self.pk, len_para, Hexstr=0)
        logging.info(f'加密消息: {plaintext} -> {ciphertext}')
        return ciphertext

    def decrypt_message(self, ciphertext):
        """解密消息"""
        len_para = 64  # 参数长度
        decrypted_message = Decrypt(ciphertext, self.sk, len_para)
        logging.info(f'解密消息: {ciphertext} -> {decrypted_message.decode()}')
        return decrypted_message.decode()

    def load_config(self, config_file='A.yml'):
        """加载配置文件A"""
        return self._load_yaml(config_file)

    def load_encryption_config(self, enc_config_file='B.yml'):
        """加载加密配置文件B"""
        return self._load_yaml(enc_config_file)

    def _load_yaml(self, filename):
        """通用加载YAML文件函数"""
        with open(filename, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            logging.info(f'加载配置文件: {filename}')
            return config

    def encrypt_config(self, config):
        """根据B中的配置返回加密后的A"""
        enc_config = config.copy()  # 保留原始配置
        encryption_keys = self.load_encryption_config()

        for key in encryption_keys.get('encript', {}).get('A', []):
            if key in config:
                enc_config[key] = self.encrypt_message(config[key])  # 加密指定的键

        logging.info('加密配置完成')
        return enc_config

    def decrypt_config(self, enc_config):
        """解密配置并返回原始信息"""
        dec_config = enc_config.copy()  # 保留加密后的配置

        for key in enc_config.keys():
            if isinstance(enc_config[key], bytes):  # 检查是否是密文
                dec_config[key] = self.decrypt_message(enc_config[key])  # 解密

        logging.info('解密配置完成')
        return dec_config

# 使用示例
if __name__ == "__main__":
    sm2 = SM2Cryptography()  # 创建 SM2 加密对象
    sm2.save_keys()  # 保存生成的公钥和私钥

    # 加载配置A
    config_a = sm2.load_config('A.yml')
    logging.info(f"原始配置: {config_a}")

    # 加密配置A中的敏感信息
    encrypted_config = sm2.encrypt_config(config_a)
    logging.info(f"加密后的配置: {encrypted_config}")

    # 将加密后的配置写入新的YAML文件（可选）
    with open('encrypted_A.yml', 'w', encoding='utf-8') as file:
        yaml.dump(encrypted_config, file)

    # 解密配置
    decrypted_config = sm2.decrypt_config(encrypted_config)
    logging.info(f"解密后的配置: {decrypted_config}")