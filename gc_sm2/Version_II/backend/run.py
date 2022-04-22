
# Run.py aims to connect to Vue using flask
# It's just like tunnel between gc_sm2 and Vue

import json

from main import gc_sm2
from flask import Flask, request
app = Flask(__name__)
myGod = None

@app.route('/api/channelInit', methods=['POST'])
def channelInit():
    # get post data
    data = request.get_data().decode()
    data = json.loads(data)
    keys = [[data['sk_a'], data['pk_a']], [data['sk_b'], data['pk_b']]]
    money = [data['money_a'], data['money_b']]
    fee = data['fee']

    # make gc_sm2
    global myGod
    myGod = gc_sm2(keys, money, fee)
    return json.dumps(myGod._getInitMessage())

@app.route('/api/channelUpdate', methods=['POST'])
def channelUpdate():
    # get post data
    data = request.get_data().decode()
    data = json.loads(data)
    money = [data['state_a'], data['state_b']]
    
    # channel update
    myGod.updateChannel(money)
    return json.dumps(myGod._getInfoFromChannel(myGod.channel))

@app.route('/api/channelPunish', methods=['POST'])
def channelPunish():
    # get post data
    data = request.get_data().decode()
    data = json.loads(data)
    
    # channel punish
    myGod.punishUser(data['userName'])
    return json.dumps(myGod._getPunishAndCloseMessage())

@app.route('/api/channelClose', methods=['POST'])
def channelClose():
    # channel close
    myGod.closeChannel()
    return json.dumps(myGod._getPunishAndCloseMessage())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
