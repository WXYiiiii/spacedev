# import logging
# from ruamel.yaml import YAML
# from pysmx.SM2 import Encrypt, generate_keypair
# import binascii  # 用于十六进制编码
#
# # 配置日志
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
# class SM2Cryptography:
#     def __init__(self):
#         self.cfg_crypt_path = './B.yml'
#         self.pk, self.sk = generate_keypair()
#         logging.info(f'生成的公钥: {self.pk}')
#         logging.info(f'生成的私钥: {self.sk}')
#         self.yaml = YAML()
#
#     def save_keys(self, public_key_file='pk.key', private_key_file='sk.key'):
#         self._save_to_file(public_key_file, self.pk)
#         self._save_to_file(private_key_file, self.sk)
#
#     def _save_to_file(self, filename, data):
#         with open(filename, 'wb') as binfile:
#             binfile.write(data)
#         logging.info(f'数据已保存到 {filename}')
#
#     def encrypt_message(self, plaintext):
#         len_para = 64
#         ciphertext = Encrypt(plaintext.encode(), self.pk, len_para, Hexstr=0)
#         logging.info(f'加密消息: {plaintext} -> {ciphertext}')
#         return binascii.hexlify(ciphertext).decode()  # 使用十六进制编码返回字符串
#
#     def load_yaml(self, filename):
#         with open(filename, 'r', encoding='utf-8') as file:
#             config = self.yaml.load(file)
#         logging.info(f'加载配置文件: {filename}')
#         return config
#
#     def load_encryption_config(self):
#         return self.load_yaml(self.cfg_crypt_path)
#
#     def replace_encrypted_fields(self, data, keys_to_encrypt):
#         """在指定的字段上进行加密替换"""
#         for key in keys_to_encrypt:
#             keys = key.split('.')
#             temp_data = data
#             for k in keys[:-1]:
#                 temp_data = temp_data.get(k)
#                 if temp_data is None:
#                     break
#             last_key = keys[-1]
#             if temp_data and last_key in temp_data:
#                 original_value = temp_data[last_key]
#                 encrypted_value = self.encrypt_message(original_value)
#                 temp_data[last_key] = encrypted_value
#                 logging.info(f'替换字段: {key} -> {encrypted_value}')
#
#     def process_files(self):
#         encryption_keys = self.load_encryption_config()
#         for file_info in encryption_keys.get('encript', []):
#             filename = file_info['filename']
#             keys_to_encrypt = file_info['keys']
#
#             # 加载 YAML 文件
#             data = self.load_yaml(filename)
#             logging.info(f"原始配置 ({filename}): {data}")
#
#             # 替换并加密指定字段
#             self.replace_encrypted_fields(data, keys_to_encrypt)
#
#             # 写回文件，保留原有格式和注释
#             with open(filename, 'w', encoding='utf-8') as file:
#                 self.yaml.dump(data, file)
#
# if __name__ == "__main__":
#     sm2 = SM2Cryptography()
#     sm2.save_keys()
#     sm2.process_files()