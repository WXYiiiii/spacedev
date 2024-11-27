import oyaml as yaml
import logging
from pysmx.SM2 import Encrypt, Decrypt, generate_keypair

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SM2Cryptography:
    def __init__(self):
        # 口令加密配置文件
        self.cfg_crypt_path = './B.yml'

        # 生成公钥和私钥
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

    def load_yaml(self, filename):
        """通用加载YAML文件函数"""
        with open(filename, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        logging.info(f'加载配置文件: {filename}')
        return config

    def load_encryption_config(self):
        """加载加密配置文件B"""
        return self.load_yaml(self.cfg_crypt_path)

    def encrypt_config(self, config, keys_to_encrypt):
        """根据指定的键返回加密后的配置"""
        enc_config = config.copy()  # 保留原始配置

        for key in keys_to_encrypt:
            keys = key.split('.')  # 将点分隔符的键转换为字典路径
            temp_config = enc_config

            for k in keys[:-1]:  # 遍历到倒数第二个键
                temp_config = temp_config.get(k, {})

            last_key = keys[-1]  # 获取最后一个键
            if last_key in temp_config:  # 检查最后一个键是否存在
                temp_config[last_key] = self.encrypt_message(temp_config[last_key])  # 加密指定的键

        logging.info('加密配置完成')
        return enc_config

    def process_files(self):
        """处理所有指定的配置文件进行加密"""
        encryption_keys = self.load_encryption_config()

        for file_info in encryption_keys.get('encript', []):
            filename = file_info['filename']
            keys_to_encrypt = file_info['keys']

            # 加载当前配置文件
            config = self.load_yaml(filename)
            logging.info(f"原始配置 ({filename}): {config}")

            # 加密当前配置中的敏感信息
            encrypted_config = self.encrypt_config(config, keys_to_encrypt)
            logging.info(f"加密后的配置 ({filename}): {encrypted_config}")

            # 将加密后的配置写入新的YAML文件（可选）
            with open(f'encrypted_{filename}', 'w', encoding='utf-8') as file:
                yaml.dump(encrypted_config, file)

# 使用示例
if __name__ == "__main__":
    sm2 = SM2Cryptography()  # 创建 SM2 加密对象

    sm2.save_keys()  # 保存生成的公钥和私钥
    # 处理所有指定的配置文件进行加密
    sm2.process_files()