import hashlib
from binascii import unhexlify, hexlify
from as_sm2 import sm2_xcl

def get_address(pk):
    """
    get addr corresponding to pk, addr=repemd160(sha256(pk))
    """
    hashsha256 = hashlib.sha256(unhexlify(hexlify(pk.encode()).decode('utf-8'))).digest()
    hashripemd160 = hashlib.new('ripemd160')
    hashripemd160.update(hashsha256)
    hash160 = hashripemd160.digest()
    addr_string_hex = hexlify(hash160).decode('utf-8')

    return addr_string_hex

class transaction(object):
    """ make transaction """
    def __init__(self, inputs, outputs):
        self.tx = [inputs, outputs]

    def get_tx_id(self):
        """ get txid """
        tx_message = ''
        for i in self.tx[0].txinputs:
            tx_message += str(i[0])+str(i[1])+str(i[2])
        for i in self.tx[1].txoutputs:
            tx_message += str(i[0])+str(i[1])
        tx_str = bytes(tx_message, 'utf-8')
        hashsha256 = hashlib.sha256(unhexlify(hexlify(tx_str).decode('utf-8'))).digest()
        return bytes(hexlify(hashsha256).decode('utf-8'), 'utf-8')

    def get_txin(self):
        """ get tx input """
        return self.tx[0]

    def get_txout(self):
        """ get tx output """
        return self.tx[1]

class Txinputs(object):
    def __init__(self, txids, vouts, scriptSigs):
        assert len(txids) == len(vouts) and len(txids) == len(scriptSigs)
        self.txinputs = []
        for i in range(len(txids)):
            self.txinputs.append([txids[i], vouts[i], scriptSigs[i]])
    
    def get_txids(self):
        txids = []
        for i in self.txinputs:
            txids.append(i[0])
        return txids

    def get_vouts(self):
        vouts = []
        for i in self.txinputs:
            vouts.append(i[0])
        return vouts

    def get_scriptSigs(self):
        scriptSigs = []
        for i in self.txinputs:
            scriptSigs.append(i[0])
        return scriptSigs

class Txoutputs(object):
    def __init__(self, values, scriptPubKeys):
        assert len(values) == len(scriptPubKeys)
        self.txoutputs = []
        for i in range(len(values)):
            self.txoutputs.append([values[i], scriptPubKeys[i]])  

    def get_values(self):
        values = []
        for i in self.txoutputs:
            values.append(i[0])
        return values

    def get_scriptPubKeys(self):
        scriptPubKeys = []
        for i in self.txoutputs:
            scriptPubKeys.append(i[0])
        return scriptPubKeys          

class UTXO(object):
    def __init__(self, user_id, value, bc):
        assert user_id.user_name == "a" or user_id.user_name == "b"
        self.user_name = user_id.user_name
        self.user_id = user_id
        self.value = value
        self.inputs = Txinputs(txids=[self.user_name], vouts=[0], scriptSigs=[(("R", "S"),"pk")])
        self.outputs = Txoutputs(values=[self.value], scriptPubKeys=[self.user_id.p2pkh])
        self.tx = transaction(self.inputs, self.outputs)
        self.sm2_xcl = sm2_xcl(self.user_id.sk, self.user_id.pk)
        
        txid = self.tx.get_tx_id()
        bc.add_tx(self.tx, [self.sm2_xcl.Sign_sm2(txid)])

    
    def trans2Txinput(self):
        txid = self.tx.get_tx_id()
        scriptSig = (self.sm2_xcl.Sign_sm2(txid), self.user_id.pk)
        return Txinputs([txid], [0], [scriptSig])







