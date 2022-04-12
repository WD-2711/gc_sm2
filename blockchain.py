from utils import transaction


class Blockchain(object):
    """ make Blockchain """
    def __init__(self):
        self.tx_list = []
        self.tx_sign_list = []
        self.tx_number = 0
    
    def add_tx(self, tx, tx_sign):
        """ add transaction and it's sig to blockchain """
        assert type(tx) is transaction
        self.tx_list.append(tx)
        self.tx_sign_list.append(tx_sign)
        self.tx_number += 1
        return True
    
    def search_tx_by_id(self, txid):
        """ search transactions by txid"""
        ff = False
        for i in range(self.tx_number):
            tmp_id = self.tx_list[i].get_tx_id()
            if txid == tmp_id:
                ff = True
                break
        assert ff == True
        return self.tx_list[i]
