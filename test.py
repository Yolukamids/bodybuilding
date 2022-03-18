"""
-*- coding: utf-8 -*-
@Time : 2022/3/18 18:44
@Author : 风落心夜
@File : test
@Project : body
"""
import jwt
# 加密
encode_jwt = jwt.encode({'uid':'123'},'密钥123',algorithm='HS256')
print(encode_jwt)
# 解密
encode_jwt = str(encode_jwt,encoding='utf-8')  #  转码强转 必须进行转码
decode_jwt = jwt.decode(encode_jwt,'密钥123',algorithms=['HS256'])
print(decode_jwt)  # 字典形式
