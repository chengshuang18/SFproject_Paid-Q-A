/*
 * @Author: hjj 
 * @Date: 2021-10-07 12:23:49 
 * @Last Modified by: hjj
 * @Last Modified time: 2021-11-16 10:35:07
 */

<template>
  <el-dialog :visible.sync="rechargeVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false">
    <el-tabs v-model="activeName">
      <el-tab-pane label="余额查看" name="first">
        <div>
          {{ userMsg.balance }}
        </div>
        <div class="tabs-footer">
          <el-button type="primary" @click="close()">确 定</el-button>
        </div>
      </el-tab-pane>
      <el-tab-pane label="账户充值" name="second">
        <div>
          <el-radio v-model="radio" label="1" border>6</el-radio>
          <el-radio v-model="radio" label="2" border>18</el-radio>
          <el-radio v-model="radio" label="3" border>68</el-radio>
          <el-radio v-model="radio" label="4" border>118</el-radio>
          <el-radio v-model="radio" label="5" border>648</el-radio>
        </div>
        <div class="tabs-footer">
          <el-button style="margin-left: 40px" @click="close()">取 消</el-button>
          <el-button type="primary" @click="commit()">确 定</el-button>
        </div>
      </el-tab-pane>
    </el-tabs>
  </el-dialog>
</template>

<script>
export default {
  props: {
    rechargeVisible: {
      type: Boolean,
      default: () => false,
    },
  },
  data() {
    return {
      activeName: "first",
      radio: "1",
      userMsg: {},
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    close() {
      this.$emit("update_rechargeVisible", false);
    },
    commit() {
      var num = 0;
      if(this.radio == "1")
        num = 6;
      if(this.radio == "2")
        num = 18;
      if(this.radio == "3")
        num = 68;
      if(this.radio == "4")
        num = 118;
      if(this.radio == "5")
        num = 648;
      const qs = require('qs');
      this.$http({
        url: this.$url + "api/walletmanagement",
        method: 'post',
        data: qs.stringify({
            "username": this.userMsg.username,
            "money": num,
        })
      }).then(res=>{
          this.$message({
              showClose: true,
              message: '充值成功',
              type: 'success',
              duration: 1000,
              onClose: ()=>{
                this.userMsg.balance += num;
                sessionStorage.removeItem('userMsg');
                sessionStorage.setItem('userMsg',JSON.stringify(this.userMsg));
                this.$emit("update_rechargeVisible", false);
              }
          });
      }).catch(error=>{
          if(error.response.status == 402){
              this.$message({
                  showClose: true,
                  message: '用户不存在',
                  type: 'error',
                  onClose: ()=>{
                      this.$emit("update_dialogVisible", false);
                  }
              });
          }
      })
      
      //this.$emit("update_rechargeVisible", false);
    },
    fetchData() {
      //从缓存中获取userMsg
      if(sessionStorage.getItem('userMsg')){
        let userMsg = sessionStorage.getItem('userMsg');
        this.userMsg = JSON.parse(userMsg);
      }
      else{
        this.userMsg = this.$userMsg;
      }

      //拉取个人最新信息
      this.$http({
        url: this.$url + "api/getusermsg",
        method: "get",
        params: {
          username: this.userMsg.username,
        },
      })
      .then((res) => {
        const userMsg = {
          photo: res.data.doc.photo,
          username: res.data.doc.username,
          email: res.data.doc.email,
          photo: "data:image/jpeg;base64," + res.data.doc.photo.slice(2).substr(0, res.data.doc.photo.length - 3),
          permission: res.data.doc.permission,
          balance: res.data.doc.balance,
        };
        this.userMsg = userMsg;
        sessionStorage.removeItem('userMsg');
        sessionStorage.setItem('userMsg', JSON.stringify(userMsg));
      })
    },
  },
};
</script>

<style scoped>
.tabs-footer {
  margin-top: 50px;
  display: flex;
  flex-direction: row-reverse;
}
</style>
