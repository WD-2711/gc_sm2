import sys
sys.path.append('C:\\Users\\WD\\Desktop\\bishe\\code')
from gmssl import sm2, sm3, func


# ecc parameters
default_ecc_table = {
    'n': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',
    'p': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',
    'g': '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7'\
         'bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0',
    'a': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',
    'b': '28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',
}

class NIZK_sm2(sm2.CryptSM2):
    """ Non-Interactive Zero-Knowledge NIZK(VIZK) algorithm """
    def __init__(self, private_key, public_key, ecc_table=default_ecc_table):
        # essential paras
        self.ecc_table = sm2.default_ecc_table
        self.para_len = len(ecc_table['n'])
        self.ecc_a3 = (int(ecc_table['a'], 16) + 3) % int(ecc_table['p'], 16)
        # sk, pk
        self.private_key = private_key
        self.public_key = public_key
    
    def prove(self, Q, Y, y):
        """ prove algorithm """
        c = sm3.sm3_hash(
            list(
                bytes.fromhex(
                    self.public_key[0:self.para_len] + Q[0:self.para_len] + Y[0:self.para_len]
                    )
                )
            )
        r = (int(y, 16) + int(c, 16) * int(self.private_key, 16)) % int(self.ecc_table['n'], 16)

        return (Y, r)
    
    def verify(self, Q, Y, r):
        """ verify algorithm """
        c = sm3.sm3_hash(
            list(
                bytes.fromhex(
                    self.public_key[0:self.para_len] + Q[0:self.para_len] + Y[0:self.para_len]
                    )
                )
            )
        
        tmp1 = self._kg(r, self.ecc_table['g']) 
        tmp2 = self._kg(int(c,16), self.public_key)
        tmp2 = self._convert_jacb_to_nor(self._add_point(Y, tmp2))
        if tmp1 == tmp2:
            return True
        else:
            return False

class AS_sm2(sm2.CryptSM2):
    """ Adaptor Signature of SM2 """
    def __init__(self, private_key, public_key, yy, ecc_table=default_ecc_table):
        # essential paras
        self.ecc_table = sm2.default_ecc_table
        self.para_len = len(ecc_table['n'])
        self.ecc_a3 = (int(ecc_table['a'], 16) + 3) % int(ecc_table['p'], 16)
        # sk, pk
        self.private_key = private_key
        self.public_key = public_key
        # difficult state Y and difficult proof y
        self.y = yy[0]
        self.Y = yy[1]
        # NIZK
        self.NIZK = NIZK_sm2(private_key, public_key)

    def change_y(self, yy):
        """ change y and Y """
        self.y = yy[0]
        self.Y = yy[1]        
    
    def pSign_sm2(self, data, sk=None, Y=None):
        """ pSign """
        sk = self.private_key
        Y = self.Y
        y = self.y
        
        # Step1: calculate k, K
        k = func.random_hex(self.para_len)
        K = self._kg(int(k, 16), self.ecc_table['g'])

        # Step2: calculate Q, r, s_1
        # Q
        tmp1 = int(sk, 16) + 1
        Q = self._kg(tmp1, Y)
        # r
        hash_data = int(bytes.fromhex(self.get_e(data.hex())).hex(),16)
        f_KQ = int(self._convert_jacb_to_nor(self._add_point(K, Q))[0:self.para_len], 16)
        r = ((hash_data + f_KQ) % int(self.ecc_table['n'], 16))
        # s_1
        tmp2 = pow(tmp1, int(self.ecc_table['n'], 16) - 2, int(self.ecc_table['n'], 16))
        s_1 = (tmp2*(int(k,16) + r) - r) % int(self.ecc_table['n'], 16)

        # Step3: generate NIZK.prove
        pai = self.NIZK.prove(Q, Y, y)

        return (r, s_1, Q, pai)
    
    def pVrfy_sm2(self, data, pSign_result, pk=None, Y=None):
        """ pVrfy """
        pk = self.public_key
        Y = self.Y
        (r_rev, s_1_rev, Q_rev, pai_rev) = pSign_result

        # Step1: calculate K_rev
        K_rev = self._add_point(
            self._kg(s_1_rev, self.ecc_table['g']),
            self._kg((r_rev+s_1_rev)% int(self.ecc_table['n'], 16), pk)
        )
        K_rev = self._convert_jacb_to_nor(K_rev)

        # Step2: calculate tmp and verify tmp ?= r_rev
        hash_data = int(bytes.fromhex(self.get_e(data.hex())).hex(),16)
        f_KQ = int(self._convert_jacb_to_nor(self._add_point(K_rev, Q_rev))[0:self.para_len], 16)
        tmp = ((hash_data + f_KQ) % int(self.ecc_table['n'], 16))
        assert tmp == r_rev

        # Step3: NIZK.verify
        assert self.NIZK.verify(Q_rev, pai_rev[0], pai_rev[1]) == True

        return True

    def Adapt_sm2(self, pSign_result, y=None):
        """ Adapt """
        y = self.y
        (r_rev, s_1_rev, Q_rev, pai_rev) = pSign_result

        # calculate s
        s = (s_1_rev + int(y,16)) % int(self.ecc_table['n'], 16)

        return (r_rev, s)

    def Ext_sm2(self, Sign_result, pSign_result, Y=None):
        """ Ext """
        Y = self.Y
        (r_rev_1, s_1_rev, Q_rev, pai_rev) = pSign_result
        (r_rev_2, s_rev) = Sign_result

        # calculate tmp1
        re = (s_rev - s_1_rev) % int(self.ecc_table['n'], 16)
        tmp1 = self._kg(re, self.ecc_table['g'])

        assert tmp1 == Y
        return re

class sm2_xcl(sm2.CryptSM2):
    """ Normal Signature of SM2 """
    def __init__(self, private_key, public_key, ecc_table=default_ecc_table):
        # essential paras
        self.ecc_table = sm2.default_ecc_table
        self.para_len = len(ecc_table['n'])
        self.ecc_a3 = (int(ecc_table['a'], 16) + 3) % int(ecc_table['p'], 16)
        # sk, pk
        self.private_key = private_key
        self.public_key = public_key

    def Sign_sm2(self, data):
        """ Sign """
        # Step1: random choose k and calculate K=k*G
        k = func.random_hex(self.para_len)
        K = self._kg(int(k, 16), self.ecc_table['g'])

        # Step2: calculate r, s
        # r
        hash_data = int(bytes.fromhex(self.get_e(data.hex())).hex(),16)
        f_K = int(K[0:self.para_len], 16)
        r = ((hash_data + f_K) % int(self.ecc_table['n'], 16))
        # s
        tmp1 = int(self.private_key, 16) + 1
        tmp2 = pow(tmp1, int(self.ecc_table['n'], 16) - 2, int(self.ecc_table['n'], 16))
        s = (tmp2*(int(k,16) + r) - r) % int(self.ecc_table['n'], 16)

        return (r, s)
    
    def Vrfy_sm2(self, data, Sign_result):
        """ Vrfy """
        (r_rev, s_rev) = Sign_result

        # calculate tmp1
        hash_data = int(bytes.fromhex(self.get_e(data.hex())).hex(),16)
        tmp1 = int(self._convert_jacb_to_nor(
            self._add_point(
                self._kg(s_rev, self.ecc_table['g']), 
                self._kg((r_rev + s_rev) % int(self.ecc_table['n'], 16), self.public_key))
            )[0:self.para_len], 16) + hash_data
        tmp1 %= int(self.ecc_table['n'], 16)
        
        assert tmp1 == r_rev
        return True



if __name__ == "__main__":
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D7'
    public_key = '2c2c0f20b0eaf58357f12825bff9590cf4216bb7fa0f1204270adaab1af4511553093b41da161237541803f41838fa4a16e909812cedeb884f69690a7659a82d'
    # public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    
    yy = ('e803812cffc123a5d512dd6cd42e4655dc48c482f53f54dc2845512bcc23837a', 'e0df2b1f260176be74ba3d1e795a33fbac3b95bc7fcd644a9dabda30a3f71f79033893d99f393c9c76a4b7bf51d83d3b7f08fd4b5d8118741d9a19225b854ec3')
    a = AS_sm2(private_key, public_key, yy)

    data = b'16'

    pSign = a.pSign_sm2(data)
    a.pVrfy_sm2(data, pSign)
    Sign = a.Adapt_sm2(pSign)
    bb = a.Ext_sm2(Sign, pSign)
    print(int(yy[0],16))
    print(bb)
    # private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D7'
    # public_key = a._kg(int(private_key, 16), default_ecc_table['g'])
    # print(public_key)
    # a = sm2_xcl(private_key, public_key)
    # sign = a.Sign_sm2(data)
    # print(a.Vrfy_sm2(data,sign))


