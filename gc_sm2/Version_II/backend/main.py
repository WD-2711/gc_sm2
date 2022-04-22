###############################################################
## Project: Generalized Channels for SM2 Adaptor Signatures  ##
## Developer: Chuanlong Xie                                  ##
## Time: 2022-4-12                                           ##
## Company: Xidian University                                ##
###############################################################
import sys
sys.path.append('C:\\Users\\WD\\Desktop\\bishe\\code')
from gmssl import sm2
from as_sm2 import default_ecc_table

from identity import Id
from utils import UTXO
from channel import Channel
from blockchain import Blockchain

"""
gc_sm2 model
"""
class gc_sm2(sm2.CryptSM2):
    def __init__(self, keys, initialMoney, fee):

        # some ugly paras
        self.ecc_table = default_ecc_table
        self.para_len = len(self.ecc_table['n'])
        self.ecc_a3 = (int(self.ecc_table['a'], 16) + 3) % int(self.ecc_table['p'], 16)

        # Initialize
        self.bc = Blockchain()
        self.bcTxNumber = 0
        keys = self._keyProcess(keys)
        # get (sk,pk) of A and B
        [[private_key_a, public_key_a], [private_key_b, public_key_b]] = keys
        self.id_a = Id("a", private_key_a, public_key_a)
        self.id_b = Id("b", private_key_b, public_key_b)

        # initial UTXO of A and B
        self.input_a = UTXO(self.id_a, initialMoney[0], self.bc).trans2Txinput()
        self.input_b = UTXO(self.id_b, initialMoney[1], self.bc).trans2Txinput()

        # make channel
        self.channel = Channel(self.id_a, self.id_b, self.input_a, self.input_b, fee).create(self.bc)

    def _keyProcess(self, keys):
        if keys[0][1] != "" and keys[1][1] != "":
            return keys
        else:
            pk1 = self._kg(int(keys[0][0], 16), self.ecc_table['g'])
            pk2 = self._kg(int(keys[1][0], 16), self.ecc_table['g'])
            return [[keys[0][0], pk1], [keys[1][0], pk2]]

    def _getInitMessage(self):
        message = {}
        message['id_a']=[self.id_a.sk, self.id_a.pk, self.id_a.addr, self.id_a.p2pkh]
        message['id_b']=[self.id_b.sk, self.id_b.pk, self.id_b.addr, self.id_b.p2pkh]
        message['bcMsg']=self._getInfoFromBlockchain(self.bc)
        message['gcMsg']=self._getInfoFromChannel(self.channel)
        return message

    def _getPunishAndCloseMessage(self):
        message = {}
        message['bcMsg']=self._getInfoFromBlockchain(self.bc)
        message['gcMsg']=self._getInfoFromChannel(self.channel)
        return message
        
    def _getInfoFromBlockchain(self, bc):
        bcMessage = []
        for index in range(bc.tx_number):
            bcItem = []
            tx = bc.tx_list[index]
            bcItem.append(['txMsg',self._getInfoFromTx(tx)])
            bcItem.append(['signMsg',bc.tx_sign_list[index]])
            bcMessage.append(['tx'+str(index+1), bcItem])
        return bcMessage

    def _getInfoFromTx(self, tx):
        txMessage = []
        input = [[item[0].decode() if type(item[0]) != str else item[0], item[1], item[2]] for item in tx.get_txin().txinputs]
        txMessage.append(['input', input])
        txMessage.append(['output', tx.get_txout().txoutputs])
        return txMessage

    def _getInfoFromChannel(self, c):
        msglist = []
        for item in c.messages:
            msgItem = [
                (self._getInfoFromTx(item[0][0]), item[0][1]), \
                ((self._getInfoFromTx(item[1][0][0]), item[1][0][1]), item[1][1], item[1][2], item[1][3], item[1][4]), \
                (self._getInfoFromTx(item[2][0]), item[2][1])
            ]
            msglist.append(msgItem)
        return [
            ['msgList',msglist],
            ['stateList',c.state],
        ]
    
    def updateChannel(self, newState):
        self.channel.update((newState[0], newState[1]))

    def punishUser(self, user):
        id = self.id_a if user == 'a' else self.id_b
        self.channel.punish(punished_user=id, blockchain=self.bc)

    def closeChannel(self):
        self.channel.close(self.bc)

"""
test main function
"""
if __name__ == '__main__':
    keys = [["3d088ea6ba313224f9c57d029fd2a8f5b23b284444a21e6dee6e84555e056adb", "6cbf77b9e195af841b73869a00f27dfaed38abf31081c55fe41a26186291d014f953217c81ede02a1f557164b30c3cc3d2676c8f48b9b8a58f4f2bac6e82fae5"],
    ["17032f80abb8fe1d9fce9947b55642704d39efc2fc48150238853361accf539d", "c88b476170582bb2f0d49ead24634b24223613fd36e479e184e4980ebcad495c344ab1d971f7adabe0d1a5e4738634404cc28912cbe746317a14cab385be8fc2"]]
    money = [100, 200]
    fee = 10
    gc = gc_sm2(keys, money, fee)
    # print(gc._getInfoFromBlockchain(gc.bc))
    gc.updateChannel([150, 140])
    # gc.punishUser(gc.id_a)
    # gc.closeChannel()
    

"""
previous code
"""
"""
def gc_sm2():
    # Initialize
    bc = Blockchain()

    # Step1: get (sk,pk) of A and B
    with open("./data/key.json", "r") as f:
        keys = json.load(f)
    [[private_key_a, public_key_a], [private_key_b, public_key_b]] = random.sample(keys,2)
    id_a = Id("a", private_key_a, public_key_a)
    id_b = Id("b", private_key_b, public_key_b)
    
    # Step2: initial UTXO of A and B
    input_a = UTXO(id_a, 100, bc).trans2Txinput()
    input_b = UTXO(id_b, 200, bc).trans2Txinput()

    # Step3: make channel
    fee = 5
    channel = Channel(id_a, id_b, input_a, input_b, fee).create(bc)

    channel.update((100, 195))
    channel.update((120, 175))
    channel.punish(punished_user=id_b, blockchain=bc)
    # channel.close(bc)


    print(bc.tx_number)
    for i in range(bc.tx_number):
        print("----------------------------------------------------")
        tx = bc.tx_list[i]
        print("sign", bc.tx_sign_list[i])
        tx_in = tx.get_txin()
        print("input ", tx_in.txinputs)
        tx_out = tx.get_txout()
        print("output ", tx_out.txoutputs)
        print("----------------------------------------------------")
"""


