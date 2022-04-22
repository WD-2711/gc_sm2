# -*- coding:gbk -*-
import sys
from utils import get_address


class Id:
    """
    用于生成与身份相关的密钥和地址 sk,pk,addr,p2pkh
    """
    def __init__(self, user, sk, pk):
        self.user_name = user
        self.sk = sk
        self.pk = pk
        self.addr = get_address(pk)
        self.p2pkh = ['OP_DUP', 'OP_HASH160', self.addr, 'OP_EQUALVERIFY', 'OP_CHECKSIG_'+user]