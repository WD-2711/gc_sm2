<template>
    <!--输入-->
    <div class="table-responsive">
      <base-table 
        :thead-classes="type === 'dark' ? 'thead-dark' : 'thead-light'" 
        :class="type === 'dark' ? 'table-dark' : ''"
        :data="inputTable">
        <template v-slot:columns>
          <th>所花费交易的ID</th>
          <th>所花费交易的输出序号</th>
          <th>ScriptKey</th>
        </template>

        <template v-slot:default="row">
          <th scope="row" @click="showCompleteMsg(row.item.txId.toString())">
            {{ row.item.txId.toString().length > 4 ? row.item.txId.toString().substring(0,4)+"..." : row.item.txId.toString()}}
          </th>
          <td>
            {{ row.item.txOut }}
          </td>
          <td @click="showCompleteMsg(row.item.scriptKey.toString())">
            {{ row.item.scriptKey.toString().length > 8 ? row.item.scriptKey.toString().substring(0,8)+"..." : row.item.scriptKey.toString()}}
          </td>

        </template>
      </base-table>
    </div>
    <!--输出-->
    <div class="table-responsive">
      <base-table 
        :thead-classes="type === 'dark' ? 'thead-dark' : 'thead-light'" 
        :class="type === 'dark' ? 'table-dark' : ''"
        :data="outputTable">
        <template v-slot:columns>
          <th>值</th>
          <th>ScriptPubKey</th>
        </template>

        <template v-slot:default="row">
          <th scope="row">
            {{ row.item.val }}
          </th>
          <td @click="showCompleteMsg(row.item.scriptPubKey.toString())">
            {{ row.item.scriptPubKey.toString().length > 8 ? row.item.scriptPubKey.toString().substring(0,8)+"..." : row.item.scriptPubKey.toString()}}
          </td>

        </template>
      </base-table>
    </div>
</template>

<script>

export default {
    name:"Tx",
    props:{
      type: String,
      inputTable: Array,
      outputTable: Array
    },
    data() {
      return {};
    },
    methods:{
      showCompleteMsg(data){
        alert(data)
      }
    }

}
</script>
