###############################################################
## Project: Generalized Channels for SM2 Adaptor Signatures  ##
## Developer: Chuanlong Xie                                  ##
## Time: 2022-4-12                                           ##
## Company: Xidian University                                ##
###############################################################
import json
import random

from identity import Id
from utils import UTXO
from channel import Channel
from blockchain import Blockchain


if __name__ == "__main__":

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