"""
-*- coding: utf-8 -*-
@Time : 2022/3/17 23:34
@Author : 风落心夜
@File : utils
@Project : body
"""
import hashlib
import re

USERNAME_PATTERN = re.compile(r'\w{6,20}')


def check_username(username):
    return USERNAME_PATTERN.fullmatch(username) is not None


def check_password(password):
    return len(password) >= 6


def gen_sha256_digest(content):
    if not isinstance(content, bytes):
        if isinstance(content, str):
            content = content.encode('utf-8')
        else:
            content = content.bytes(content)
    return hashlib.sha256(content).hexdigest()
