from as_sm2 import AS_sm2, sm2_xcl
from utils import Txinputs, Txoutputs, transaction

import sys
sys.path.append('C:\\Users\\WD\\Desktop\\bishe\\code')
from gmssl import sm2, func


class Channel(sm2.CryptSM2):
    """ Generalized Channel """
    def __init__(self, id_a, id_b, input_a, input_b, fee):
        self.input_a = input_a
        self.input_b = input_b
        self.id_a = id_a
        self.id_b = id_b
        self.fee = fee

        # parameters
        self.ecc_table = sm2.default_ecc_table
        self.para_len = len(self.ecc_table['n'])
        self.ecc_a3 = (int(self.ecc_table['a'], 16) + 3) % int(self.ecc_table['p'], 16)
        self.yy_a = self._gen_pair()
        self.rr_a = self._gen_pair()
        self.yy_b = self._gen_pair()
        self.rr_b = self._gen_pair()

        self.S_a = sm2_xcl(self.id_a.sk, self.id_a.pk)
        self.S_b = sm2_xcl(self.id_b.sk, self.id_b.pk)
        self.AS_a = AS_sm2(self.id_a.sk, self.id_a.pk, self.yy_b)
        self.AS_b = AS_sm2(self.id_b.sk, self.id_b.pk, self.yy_a)
        
        # channel parameters
        self.id = "18180300053"
        self.messages = []
        self.state = []
        self.seita = []
    
    def _gen_tx_fund(self, bc):
        """ generate fundation transaction """

        # Step1: tx_fund's inputs
        txids = [self.input_a.txinputs[0][0], self.input_b.txinputs[0][0]]
        vouts = [self.input_a.txinputs[0][1], self.input_b.txinputs[0][1]]
        scriptSigs = [self.input_a.txinputs[0][2], self.input_b.txinputs[0][2]]
        fund_input = Txinputs(txids, vouts, scriptSigs)
        
        # Step2: tx_fund's outputs
        value = bc.search_tx_by_id(txids[0]).get_txout().get_values()[0] + \
                bc.search_tx_by_id(txids[1]).get_txout().get_values()[0] - \
                self.fee
        scriptPubKey = ['OP_CHECKSIG_b', 'OP_CHECKSIG_a'] # scriptSig:[sigA, sigB]
        fund_output = Txoutputs([value], [scriptPubKey])

        # Step3: make fund_tx
        fund_tx = transaction(fund_input, fund_output)
        return fund_tx        
        
    def _gen_tx_comm(self, tx_f):
        """ generate commitment transaction """

        # Step1: tx_comm's inputs
        tx_f_id = tx_f.get_tx_id()
        scriptSig = (
                        self.S_a.Sign_sm2(tx_f_id), \
                        self.S_b.Sign_sm2(tx_f_id)
                    )
        comm_input = Txinputs([tx_f_id], [0], [scriptSig])

        # Step2: tx_comm's outputs
        value = tx_f.get_txout().get_values()[0]
        # scriptSig:[sigA, sigB] or [sig_RB, sig_YB, sigA] or [sig_RA, sig_YA, sigB]
        scriptPubKey = ['OP_CHECKSIG_b',
                        'OP_IF', 
                            'OP_CHECKSIG_ya',
                            'OP_IF',
                                'OP_CHECKSIG_ra',
                            'OP_ELIF',
                                'OP_CHECKSIG_a',
                            'END_IF'
                        'OP_ELIF',
                            'OP_CHECKSIG_a',
                            'OP_IF',
                                'OP_CHECKSIG_yb',
                                'OP_IF',
                                    'OP_CHECKSIG_rb'
                                'END_IF'
                            'END_IF'
                        'END_IF'
                    ]
        comm_output = Txoutputs([value], [scriptPubKey])

        # Step3: make comm_tx
        comm_tx = transaction(comm_input, comm_output)
        return comm_tx       

    def _gen_tx_splt(self, tx_m, vals):
        """ generate split transaction """
        (val_a, val_b) = vals

        # Step1: tx_splt's inputs
        tx_m_id = tx_m.get_tx_id()
        scriptSig = (
                        self.S_a.Sign_sm2(tx_m_id), \
                        self.S_b.Sign_sm2(tx_m_id)
                    )
        splt_input = Txinputs([tx_m_id], [0], [scriptSig])
        
        # Step2: tx_splt's outputs
        value = tx_m.get_txout().get_values()[0]
        assert val_a + val_b == value and val_a*val_b > 0
        splt_output = Txoutputs([val_a, val_b], [['OP_CHECKSIG_a'],['OP_CHECKSIG_b']])

        # Step3: make splt_tx
        splt_tx = transaction(splt_input, splt_output)
        return splt_tx               

    def _gen_tx_push(self, tx, id, args):
        """ generate punishment transaction """
        (y) = args
        assert id.user_name == "a" or id.user_name == "b"

        # Step1: tx_push's inputs
        tx_id = tx.get_tx_id()
        S_r = sm2_xcl(self.rr_b[0], self.rr_b[1])
        S_y = sm2_xcl(hex(y)[2:], self._kg(y, self.ecc_table['g']))
        scriptSig = (
                        S_r.Sign_sm2(tx_id), \
                        S_y.Sign_sm2(tx_id), \
                        self.S_a.Sign_sm2(tx_id) if id.user_name == "a" else self.S_b.Sign_sm2(tx_id)
                    )
        push_input = Txinputs([tx_id], [0], [scriptSig])
        
        # Step2: tx_push's outputs
        scriptPubKey = ['OP_CHECKSIG_'+id.user_name]
        push_output = Txoutputs(tx.get_txout().get_values(), [scriptPubKey])

        # Step3: make push_tx
        push_tx = transaction(push_input, push_output)
        return push_tx, scriptSig         

    def _gen_pair(self):
        """ generate pair just like (sk, pk) """
        p1 = func.random_hex(self.para_len)
        p2 = self._kg(int(p1, 16), self.ecc_table['g'])
        return (p1, p2)

    def _find_tx_comp_by_id(self, id):
        """ find complete transaction in self.message by txid"""
        for i in self.messages:
            txs_comp = [i[0], i[1][0], i[2]]
            for tx_comp in txs_comp:
                tx = tx_comp[0]
                if tx.get_tx_id() == id:
                    return tx_comp
        return False

    def _force_close(self):
        """ let channel close forcely """
        self.messages = []
        self.seita = []
        self.state = []
        return True

    def create(self, bc):
        """ channel create """
        # Step1: A generate fund_tx
        tx_f = self._gen_tx_fund(bc)
        
        # Step2: A generate comm_tx
        tx_m = self._gen_tx_comm(tx_f)

        # Step3: A generate splt_tx
        val_a = bc.search_tx_by_id(tx_f.get_txin().get_txids()[0]).get_txout().get_values()[0] - 0.5*self.fee
        val_b = bc.search_tx_by_id(tx_f.get_txin().get_txids()[1]).get_txout().get_values()[0] - 0.5*self.fee
        tx_s = self._gen_tx_splt(tx_m, (val_a, val_b))
        self.state.append((val_a, val_b))

        # Step4: A make s_c_a, s_s_a
        tx_f_id = tx_f.get_tx_id()
        tx_m_id = tx_m.get_tx_id()
        tx_s_id = tx_s.get_tx_id()
        s_c_a = self.AS_a.pSign_sm2(tx_m_id)
        s_s_a = self.S_a.Sign_sm2(tx_s_id)

        # Step5: B make s_c_b, s_s_b
        s_c_b = self.AS_b.pSign_sm2(tx_m_id)
        s_s_b = self.S_b.Sign_sm2(tx_s_id)
        
        # Step6: A make s_c_b, s_s_b
        assert self.AS_b.pVrfy_sm2(tx_m_id, s_c_b) == True and \
               self.S_b.Vrfy_sm2(tx_s_id, s_s_b)
        s_f_a = self.S_a.Sign_sm2(tx_f_id)

        # Step7: B verified s_c_a, s_s_a
        assert self.AS_a.pVrfy_sm2(tx_m_id, s_c_a) == True and \
               self.S_a.Vrfy_sm2(tx_s_id, s_s_a)
        s_f_b = self.S_b.Sign_sm2(tx_f_id)    
        
        # Step8: A,B verified s_f_b,s_f_a, and add tx_fund to blockchain
        assert self.S_b.Vrfy_sm2(tx_f_id, s_f_b) == True and \
               self.S_a.Vrfy_sm2(tx_f_id, s_f_a) == True
        bc.add_tx(tx_f, [s_f_a, s_f_b])
        tx_f_complete = (tx_f, [s_f_a, s_f_b])

        # Step9: A make tx_m_complete, tx_s_complete
        tx_m_complete = (tx_m, [self.S_a.Sign_sm2(tx_m_id), self.AS_b.Adapt_sm2(s_c_b)])
        tx_s_complete = (tx_s, [s_s_a, s_s_b])
        self.messages.append([
            tx_f_complete, 
            (tx_m_complete, self.rr_a[0], self.rr_b[1], self.yy_b[1], s_c_a),
            tx_s_complete
            ])
        
        # Step10: Initialize self.seita
        self.seita.append([
            tx_m,
            self.rr_a, self.yy_a,
            self.rr_b, self.yy_b,
            s_c_a, s_c_b
            ])
        return self

    def update(self, new_state):
        """ channel update """
        assert len(self.messages) > 0
        # Step1: A,B make new yy_a,rr_a,yy_b,rr_b
        self.yy_a = self._gen_pair()
        self.rr_a = self._gen_pair()
        self.yy_b = self._gen_pair()
        self.rr_b = self._gen_pair()
        self.AS_a.change_y(self.yy_b)
        self.AS_b.change_y(self.yy_a)

        # Step2: B get tx_fund from self.messages, and generate new tx_m,tx_s
        tx_f = self.messages[-1][0][0]
        tx_m = self._gen_tx_comm(tx_f)
        tx_s = self._gen_tx_splt(tx_m, new_state)
        self.state.append(new_state)

        tx_m_id = tx_m.get_tx_id()
        tx_s_id = tx_s.get_tx_id()

        # Step3: B generate s_s_b, and A verify it
        s_s_b = self.S_b.Sign_sm2(tx_s_id)
        assert self.S_b.Vrfy_sm2(tx_s_id, s_s_b) == True
        
        # Step4: A generate s_c_a,s_s_a
        s_c_a = self.AS_a.pSign_sm2(tx_m_id)
        s_s_a = self.S_a.Sign_sm2(tx_s_id)  

        # Step5: B verify s_c_a,s_s_a
        assert self.AS_a.pVrfy_sm2(tx_m_id, s_c_a) == True and \
               self.S_a.Vrfy_sm2(tx_s_id, s_s_a)
        s_c_b = self.AS_b.pSign_sm2(tx_m_id)  

        # Step6: A verify s_c_b and generate tx_m_complete,tx_s_complete
        assert self.AS_b.pVrfy_sm2(tx_m_id, s_c_b) == True
        tx_m_complete = (tx_m, [self.S_a.Sign_sm2(tx_m_id), self.AS_b.Adapt_sm2(s_c_b)])
        tx_s_complete = (tx_s, [s_s_a, s_s_b])
        self.messages.append([
            self.messages[-1][0], 
            (tx_m_complete, self.rr_a[0], self.rr_b[1], self.yy_b[1], s_c_a),
            tx_s_complete
            ])
        
        # Step7: update self.seita
        self.seita.append([
            tx_m,
            self.rr_a, self.yy_a,
            self.rr_b, self.yy_b,
            s_c_a, s_c_b
            ])

    def punish(self, punished_user, blockchain):
        """
        Notes: punish don't check in code. Actually, we can punish user only when user do wrong things.
        punish someone, get all money to user who is cheated.
        """
        assert len(self.messages) > 0
        now_seita = self.seita[-1]
        tx_m = now_seita[0]
        user = punished_user.user_name # evil user
        assert user == "a" or user == "b"
        
        tx_m_id = tx_m.get_tx_id()
        tx_m_comp = self._find_tx_comp_by_id(tx_m_id)

        # Step1: verify sig
        assert tx_m_comp != False and \
                (
                    self.S_a.Vrfy_sm2(tx_m_id, tx_m_comp[1][0]) == True or \
                    self.S_b.Vrfy_sm2(tx_m_id, tx_m_comp[1][0]) == True
                )
        
        # Step2: get evil's y, generate push_tx
        if user == "b":
            y = self.AS_b.Ext_sm2(tx_m_comp[1][1], now_seita[6])
            tx_p, (s_r, s_y, s) = self._gen_tx_push(tx_m, self.id_a, (y))
        else:
            y = self.AS_a.Ext_sm2(self.AS_a.Adapt_sm2(now_seita[5]), now_seita[5])
            tx_p, (s_r, s_y, s) = self._gen_tx_push(tx_m, self.id_b, (y))
        
        # Step3: add tx to blockchain
        blockchain.add_tx(tx_p, [s_y, s_r, s])
        self._force_close()

    def close(self, bc):
        """ channel close """
        assert len(self.messages) > 0

        # Step1: A get tx_fund from self.messages, and generate tx_splt again
        tx_f = self.messages[-1][0][0]
        _vals = self.messages[-1][2][0].get_txout().get_values()
        assert type(_vals) is list
        tx_s = self._gen_tx_splt(tx_f, tuple(_vals))  
          
        # Step2: A,B generate s_s_a,s_s_b
        s_s_a = self.S_a.Sign_sm2(tx_s.get_tx_id()) 
        s_s_b = self.S_b.Sign_sm2(tx_s.get_tx_id())   

        # Step3: A verify s_s_b
        assert self.S_b.Vrfy_sm2(tx_s.get_tx_id(), s_s_b) == True

        # Step5: A generate tx_s_complete and put it to blockchain
        bc.add_tx(tx_s, [s_s_a, s_s_b])
        self.messages = []
        self.seita = []
        self.state = []
        return True


