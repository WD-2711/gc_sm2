<template>
  <div>
    <base-header
      class="header pb-8 pt-5 pt-lg-8 d-flex align-items-center"
      style="
        min-height: 600px;
        background-image: url(img/theme/profile-cover.jpg);
        background-size: cover;
        background-position: center top;
      "
    >
      <!-- Mask -->
      <span class="mask bg-gradient-success opacity-8"></span>
      <!-- Header container -->
      <div class="container-fluid d-flex align-items-center">
        <div class="row">
          <div class="col-lg-7 col-md-10">
            <h1 class="display-2 text-white">你好 谢传龙!</h1>
            <p class="text-white mt-0 mb-5">
              这是构建支付通道的主页面，你可以在这里模拟A、B双方的支付通道构建工作
            </p>
          </div>
        </div>
      </div>
    </base-header>

    <div class="container-fluid mt--7">
      <div class="row">

        <!-- 最左边一栏，初始输入信息 -->
        <div class="col-xl-4 order-xl-1" v-show="infoSubmit==='0'">
          <card shadow type="secondary">
            <form>
              <h6 class="heading-small text-muted mb-4">使用者A的信息</h6>
              <div class="pl-lg-4">
                <div class="row">
                  <div class="col-lg-11">
                    <base-input
                      alternative=""
                      label="A的私钥"
                      placeholder="2efb120XXX0fc49ba"
                      input-classes="form-control-alternative"
                      v-model="model.a_sk"
                    />
                  </div>

                </div>
                <div class="row">
                  <div class="col-lg-11">
                    <base-input
                      alternative=""
                      label="A存入双方账户的金额"
                      placeholder="250"
                      input-classes="form-control-alternative"
                      v-model.number="model.a_input"
                    />
                  </div>

                </div>
              </div>
              <hr class="my-4" />
              <h6 class="heading-small text-muted mb-4">使用者B的信息</h6>
              <div class="pl-lg-4">
                <div class="row">
                  <div class="col-lg-11">
                    <base-input
                      alternative=""
                      label="B的私钥"
                      placeholder="8dfa1b0XXX3fc46dc"
                      input-classes="form-control-alternative"
                      v-model="model.b_sk"
                    />
                  </div>

                </div>
                <div class="row">
                  <div class="col-lg-11">
                    <base-input
                      alternative=""
                      label="B存入双方账户的金额"
                      placeholder="300"
                      input-classes="form-control-alternative"
                      v-model.number="model.b_input"
                    />
                  </div>

                </div>
              </div>
              <hr class="my-4" />
              <h6 class="heading-small text-muted mb-4">构建支付通道的费用</h6>
              <div class="pl-lg-4">
                <div class="row">
                  <div class="col-lg-11">
                    <base-input
                      alternative=""
                      label="费用"
                      placeholder="100"
                      input-classes="form-control-alternative"
                      v-model.number="model.fee"
                    />
                  </div>

                </div>
              </div>
            </form>
            <div class="text-center">
              <button class="btn btn-info" @click="postInitData">创建通道</button>
            </div>
          </card>
        </div>
        <!-- 最左边一栏，初始输入信息(end) -->

        <!-- 最左边一栏，提交完初始信息 -->
        <div class="col-xl-4 order-xl-1" v-show="infoSubmit==='1'">
          <card shadow type="secondary">
            <form>
              <h6 class="heading-small text-muted mb-4">A的信息</h6>
              <div class="pl-lg-4">
                <div class="row">
                  <div class="col-lg-11">
                    私钥：
                    <base-input type="text" :value="model2.a_sk" readonly="true" />
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-11">
                    公钥：
                    <base-input type="text" :value="model2.a_pk" readonly="true" />
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-11">
                    地址：
                    <base-input type="text" :value="model2.a_addr" readonly="true" />
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-11">
                    P2PKH：
                    <base-input type="text" :value="model2.a_p2pkh" readonly="true" />
                  </div>
                </div>
              </div>
              <hr class="my-4" />
              <h6 class="heading-small text-muted mb-4">B的信息</h6>
              <div class="pl-lg-4">
                <div class="row">
                  <div class="col-lg-11">
                    私钥：
                    <base-input type="text" :value="model2.b_sk" readonly="true" />
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-11">
                    公钥：
                    <base-input type="text" :value="model2.b_pk" readonly="true" />
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-11">
                    地址：
                    <base-input type="text" :value="model2.b_addr" readonly="true" />
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-11">
                    P2PKH：
                    <base-input type="text" :value="model2.b_p2pkh" readonly="true" />
                  </div>
                </div>
              </div>
              <hr class="my-4" />
              <h6 class="heading-small text-muted mb-4">更新支付通道状态</h6>
              <div class="pl-lg-4">
                <div class="row">
                  <div class="col-lg-11">
                    <base-input
                      alternative=""
                      label="更新状态"
                      placeholder="300,250"
                      input-classes="form-control-alternative"
                      v-model="model2.newState"
                    />
                  </div>

                </div>
              </div>
              <div class="text-center">
                <button type="primary" class="btn btn-info" @click="postNewStateData">更新通道</button>
              </div>
              <hr class="my-4" />
              <h6 class="heading-small text-muted mb-4">惩罚某用户 or 关闭通道</h6>
              <div class="pl-lg-4">
                <div class="row">
                  <div class="col-lg-11">
                    <base-input
                      alternative=""
                      label="所要惩罚的用户"
                      placeholder="a"
                      input-classes="form-control-alternative"
                      v-model="model2.punishUserName"
                    />
                  </div>

                </div>
              </div>
              <div class="text-center">
                <button type="primary" class="btn btn-info" @click="postPunishData">惩罚用户</button>
                <button type="primary" class="btn btn-info" @click="postCloseData">关闭通道</button>
              </div>
            </form>
          </card>
        </div>
        <!-- 最左边一栏，提交完信息(end) -->
        <!-- 中间一栏，支付通道信息-->
        <div class="col-xl-4 order-xl-2 mb-5 mb-xl-0">
          <div class="card card-profile shadow">
            <div class="card-body pt-0 pt-md-4">
              <div class="text-center">
                <!--中间一栏，支付通道名称与更新时间-->
                <h2>通用支付通道</h2>
                <div class="h5 font-weight-300">
                  更新时间：
                  <i class="ni location_pin mr-2">{{updateTime(model3.fund_tx.inputTable)}}</i>
                </div>
                <!--中间一栏，支付通道名称与更新时间(end)-->
                <!--交易-->
                <div class="card" v-show="infoSubmit==='1'" >
                  <div class="card-header border-0">
                    <div class="row align-items-center">
                      <div class="col">
                        <h3 class="mb-0">当前funding交易</h3>
                      </div>
                    </div>
                  </div>
                  <Tx type="dark" 
                      v-bind:inputTable="model3.fund_tx.inputTable"
                      v-bind:outputTable="model3.fund_tx.outputTable"
                  />
                </div>
                <hr class="my-4"/>
                <!--交易(end)-->
                <!--交易-->
                <div class="card" v-show="infoSubmit==='1'">
                  <div class="card-header border-0">
                    <div class="row align-items-center">
                      <div class="col">
                        <h3 class="mb-0">当前commit交易</h3>
                      </div>
                    </div>
                  </div>
                  <Tx type="dark" 
                      v-bind:inputTable="model3.comm_tx.inputTable"
                      v-bind:outputTable="model3.comm_tx.outputTable"
                  />
                </div>
                <hr class="my-4" />
                <!--交易(end)-->
                <!--交易-->
                <div class="card" v-show="infoSubmit==='1'">
                  <div class="card-header border-0">
                    <div class="row align-items-center">
                      <div class="col">
                        <h3 class="mb-0">当前split交易</h3>
                      </div>
                    </div>
                  </div>
                  <Tx type="dark" 
                      v-bind:inputTable="model3.splt_tx.inputTable"
                      v-bind:outputTable="model3.splt_tx.outputTable"
                  />
                </div>
                <hr class="my-4" />
                <!--交易(end)-->
                <!--通道状态-->
                <div class="card" v-show="infoSubmit==='1'">
                  <div class="card-header border-0">
                    <div class="row align-items-center">
                      <div class="col">
                        <h3 class="mb-0">当前通道状态</h3>
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-xl-6 col-lg-6">
                      <stats-card
                        title="A账户余额"
                        :sub-title="model3.state.a"
                        class="mb-4 mb-xl-0"
                      >
                      </stats-card>
                    </div>
                    <div class="col-xl-6 col-lg-6">
                      <stats-card
                        title="B账户余额"
                        :sub-title="model3.state.b"
                        class="mb-4 mb-xl-0"
                      >
                      </stats-card>
                    </div>
                  </div>
                </div>
                <!--通道状态(end)-->

              </div>
            </div>
          </div>
        </div>
        <!-- 中间一栏，支付通道信息(end)-->
        <!-- 右边一栏，区块链信息-->
        <div class="col-xl-4 order-xl-3 mb-5 mb-xl-0">
          <div class="card card-profile shadow">
            <div class="card-body pt-0 pt-md-4">
              <div class="text-center" id="blockchainTxInsert">
                <!--右边一栏，区块链名称-->
                <h2>区块链</h2>
                <!--交易-->
                <div v-for="(item,index) in model4.txs" :key="index">
                  <div class="card">
                    <div class="card-header border-0">
                      <div class="row align-items-center">
                        <div class="col">
                          <h4 class="mb-0">交易{{index+1}}</h4>
                        </div>
                      </div>
                    </div>
                    <Tx v-bind:inputTable="item.inputTable"
                        v-bind:outputTable="item.outputTable"
                    />
                  </div>
                  <hr class="my-4" />
                </div>
                <!--交易(end)-->

              </div>
            </div>
          </div>
        </div>
        <!-- 右边一栏，区块链信息(end)-->
      </div>
    
    </div>
  </div>
</template>
<script>
import Tx from './Tx.vue'
import dayjs from '../../public/dayjs.min.js'
export default {
  name: "Basic",
  components:{Tx},
  data() {
    return {
      infoSubmit:"0",
      tx_number:0,
      model: {
        a_sk: "",
        a_input: "",
        b_sk: "",
        b_input: "",
        fee: "",
      },
      model2:{
        a_sk:"",
        a_pk:"",
        a_addr:"",
        a_p2pkh:"",
        b_sk:"",
        b_pk:"",
        b_addr:"",
        b_p2pkh:"",   
        newState:"",
        punishUserName:""   
      },
      model3:{
        fund_tx:{
          inputTable: [],
          outputTable: []
        },
        comm_tx:{
          inputTable: [],
          outputTable: []
        },
        splt_tx:{
          inputTable: [],
          outputTable: []
        },
        state:{
          a:"",
          b:""
        }
      },
      model4:{
        txs:[]
      }
    };
  },
  methods:{
    prepareTxDataByGcmsg(data, n){
      var msglist = data[0][1][n]
      var msgdata = []
      for (var i = 0; i < msglist.length; i++) {
          if(i != 1){
            var item = msglist[i]
          }
          else{
            var item = msglist[i][0]
          }
          var inputdata = item[0][0][1]
          var outputdata = item[0][1][1]
          msgdata.push([inputdata, outputdata])
      }
      var statedata = data[1][1][n]
      return [msgdata, statedata]
    },
    setTxData(tx, data){
      var input = data[0]
      var output = data[1]
      for(var i = 0; i < input.length; i++){
        tx.inputTable.push({
            txId: input[i][0],
            txOut: input[i][1],
            scriptKey: input[i][2]         
        })
      }
      for(var i = 0; i < output.length; i++){
        tx.outputTable.push({
          val: output[i][0],
          scriptPubKey: output[i][1],     
        })
      }
    },
    loadBcData(data){
      this.model4.txs = []
      for(var i = 0; i < data.length; i++){
        
        var txData = data[i][1][0][1]
        var input = txData[0][1]
        var output = txData[1][1]
        let inputTable = []
        let outputTable = []
        
        for(var j = 0; j < input.length; j++){
          inputTable.push({
              txId: input[j][0],
              txOut: input[j][1],
              scriptKey: input[j][2]         
          })
        }
        for(var k = 0; k < output.length; k++){
          outputTable.push({
            val: output[k][0],
            scriptPubKey: output[k][1],     
          })
        }
        this.model4.txs.push({"inputTable":inputTable, "outputTable":outputTable})
      }
    },
    postInitData(){
      //Step1:准备post的数据
      let postData = {
          sk_a:this.model.a_sk,
          pk_a:'',
          sk_b:this.model.b_sk,
          pk_b:'',
          money_a:this.model.a_input,
          money_b:this.model.b_input,
          fee:this.model.fee
      }
      //Step2:上传数据并获得response
      this.axios.post('/api/channelInit', postData)
      .then((res) => {

        //Step3:使用initRes处理最左边一栏数据(用户ID)
        this.model2.a_sk = res.data.id_a[0]
        this.model2.a_pk = res.data.id_a[1]
        this.model2.a_addr = res.data.id_a[2]
        this.model2.a_p2pkh = res.data.id_a[3]
        this.model2.b_sk = res.data.id_b[0]
        this.model2.b_pk = res.data.id_b[1]
        this.model2.b_addr = res.data.id_b[2]
        this.model2.b_p2pkh = res.data.id_b[3]

        //Step4:中间一栏数据(支付通道数据)
        var gcdata = this.prepareTxDataByGcmsg(res.data.gcMsg, this.tx_number)
        this.tx_number += 1
        this.setTxData(this.model3.fund_tx, gcdata[0][0])
        this.setTxData(this.model3.comm_tx, gcdata[0][1])
        this.setTxData(this.model3.splt_tx, gcdata[0][2])
        this.model3.state.a = gcdata[1][0]+''
        this.model3.state.b = gcdata[1][1]+''

        //Step5:右边一栏数据(区块链数据，动态加载)
        this.loadBcData(res.data.bcMsg)
      })
      .catch((err) => {return err})    
      this.infoSubmit = "1"
      
    },
    clearPreGc(){
      this.model3.fund_tx.inputTable = []
      this.model3.fund_tx.outputTable = []
      this.model3.comm_tx.inputTable = []
      this.model3.comm_tx.outputTable = []
      this.model3.splt_tx.inputTable = []
      this.model3.splt_tx.outputTable = []
      this.model3.state.a = ""
      this.model3.state.b = ""
    },
    postNewStateData(){
      //Step1:准备post的数据
      let postData = {
          state_a:this.model2.newState.split(",")[0] - 0,
          state_b:this.model2.newState.split(",")[1] - 0
      }
      if(postData.state_a+postData.state_b+this.model.fee !== this.model.a_input+this.model.b_input){
        alert("输入的新状态有误")
      }
      //Step2:清楚之前的gc数据
      this.clearPreGc()

      //Step3:上传数据并获得response
      this.axios.post('/api/channelUpdate', postData)
      .then((res) => {
          //Step4:中间一栏数据(支付通道数据)
          var gcdata = this.prepareTxDataByGcmsg(res.data, this.tx_number)
          this.tx_number += 1
          this.setTxData(this.model3.fund_tx, gcdata[0][0])
          this.setTxData(this.model3.comm_tx, gcdata[0][1])
          this.setTxData(this.model3.splt_tx, gcdata[0][2])
          this.model3.state.a = gcdata[1][0]+''
          this.model3.state.b = gcdata[1][1]+''
          return res
      })
      .catch((err) => {return err})      
    },
    postPunishData(){
      //Step1:准备post的数据
      let postData = {
          userName:this.model2.punishUserName
      }
      //Step3:上传数据并获得response
      this.axios.post('/api/channelPunish', postData)
      .then((res) => {
          //Step4:右边一栏数据(区块链数据，动态加载)
          this.loadBcData(res.data.bcMsg)
          return res
      })
      .catch((err) => {return err}) 
      //Step5:关闭支付通道
      this.infoSubmit = "0"
      alert("支付通道已关闭，惩罚用户"+this.model2.punishUserName)
    },
    postCloseData(){
      let postData = {}
      this.axios.post('/api/channelClose', postData)
      .then((res) => {
          //Step1:右边一栏数据(区块链数据，动态加载)
          this.loadBcData(res.data.bcMsg)
          return res
      })
      .catch((err) => {return err})
      //Step2:关闭支付通道
      this.infoSubmit = "0"
      alert("支付通道已关闭")
    },

  },
  computed:{
    updateTime(){
      return function(data){
        return dayjs().format('YYYY-MM-DD HH:mm:ss')
      }
    }
  }
};
</script>

