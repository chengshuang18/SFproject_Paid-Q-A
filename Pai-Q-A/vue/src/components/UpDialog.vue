/*
 * @Author: hjj 
 * @Date: 2021-10-05 10:19:10 
 * @Last Modified by: hjj
 * @Last Modified time: 2021-11-11 20:26:52
 */

<template>
  <el-dialog title="详情" :visible.sync="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false">
    <el-form :model="showForm" v-show="userMsg.permission == 2">
      <el-form-item label="个人简介" :label-width="formLabelWidth">
        <el-input v-model="showForm.resume" autocomplete="off" type="textarea" :placeholder="showForm.resume"></el-input>
      </el-form-item>
      <el-form-item label="回答领域" :label-width="formLabelWidth">
        <el-select v-model="showForm.field" :placeholder="showForm.field">
          <el-option label="数学" value="数学"></el-option>
          <el-option label="英语" value="英语"></el-option>
          <el-option label="社会人文" value="社会人文"></el-option>
          <el-option label="物理" value="物理"></el-option>
          <el-option label="化学" value="化学"></el-option>
          <el-option label="体育" value="体育"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="回答定价" :label-width="formLabelWidth">
        <el-input v-model="showForm.price" autocomplete="off" :placeholder="'定价区间为: ' + sysparam_lowest_prices + ' ~ ' + sysparam_top_prices"></el-input>
      </el-form-item>
    </el-form>
    <el-form :model="form" v-show="userMsg.permission == 1">
      <el-form-item label="个人简介" :label-width="formLabelWidth">
        <el-input v-model="form.resume" autocomplete="off" type="textarea" placeholder="输入字数不能超过100"></el-input>
      </el-form-item>
      <el-form-item label="回答领域" :label-width="formLabelWidth">
        <el-select v-model="form.field" placeholder="请选择回答领域">
          <el-option label="数学" value="数学"></el-option>
          <el-option label="英语" value="英语"></el-option>
          <el-option label="社会人文" value="社会人文"></el-option>
          <el-option label="物理" value="物理"></el-option>
          <el-option label="化学" value="化学"></el-option>
          <el-option label="体育" value="体育"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="回答定价" :label-width="formLabelWidth">
        <el-input v-model="form.price" autocomplete="off" :placeholder="'定价区间为: ' + sysparam_lowest_prices + ' ~ ' + sysparam_top_prices"></el-input>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close()">取 消</el-button>
      <el-button v-if="userMsg.permission == 1" type="primary" @click="commit()">确 定</el-button>
      <el-button v-else type="primary" @click="commit()">更 新</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  props: {
    dialogVisible: {
      type: Boolean,
      default: () => false,
    },
  },
  data() {
    return {
      form: {
        resume: "",
        field: "",
        price: "",
      },
      showForm: {
        resume: "",
        field: "",
        price: "",
      },
      formLabelWidth: "120px",
      userMsg: {},
      sysparam_lowest_prices: 0,
      sysparam_top_prices: 0,
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    close() {
      this.$emit("update_dialogVisible", false);
    },
    commit() {
      if(this.userMsg.permission == 1){
        if (this.form.resume == "") {
          this.$message({
            showClose: true,
            message: "简介不能为空",
            type: "warning",
          });
        } else if (this.form.field == "") {
          this.$message({
            showClose: true,
            message: "请选择回答领域",
            type: "warning",
          });
        } else if (this.form.price == "") {
          this.$message({
            showClose: true,
            message: "请设置回答定价",
            type: "warning",
          });
        } else if (this.form.price < this.sysparam_lowest_prices){
          this.$message({
            showClose: true,
            message: "定价过低",
            type: "warning",
          });
        } else if (this.form.price > this.sysparam_top_prices){
          this.$message({
            showClose: true,
            message: "定价过高",
            type: "warning",
          });
        }
        else {
          const qs = require('qs');
          let field = 0;
          if(this.form.field == "英语")
              field = 1;
          if(this.form.field == "社会人文")
              field = 2;
          if(this.form.field == "物理")
              field = 3;
          if(this.form.field == "化学")
              field = 4;
          if(this.form.field == "体育")
              field = 5;
          this.$http({
              url: this.$url + "api/upgrade",
              method: 'post',
              data: qs.stringify({
                  "username": this.userMsg.username,
                  "resume": this.form.resume,
                  "field": field,
                  "price": parseFloat(this.form.price),
              })
          }).then(res=>{
              var tmp = this.userMsg;
              tmp.permission = 2;
              sessionStorage.removeItem('userMsg');
              sessionStorage.setItem('userMsg',JSON.stringify(tmp));
              this.$message({
                  showClose: true,
                  message: '升级成功',
                  type: 'success',
                  duration: 1000,
                  onClose: ()=>{
                      this.$emit("update_dialogVisible", false);
                      this.$router.go(0);
                  }
              });
          }).catch(error=>{
            console.log("error: ",error)
            this.$message({
                showClose: true,
                message: '升级失败',
                type: 'error',
                onClose: ()=>{
                    this.$emit("update_dialogVisible", false);
                }
            });
          })
        }
      }
      else{
        if (this.showForm.resume == "") {
          this.$message({
            showClose: true,
            message: "简介不能为空",
            type: "warning",
          });
        } else if (this.showForm.field == "") {
          this.$message({
            showClose: true,
            message: "请选择回答领域",
            type: "warning",
          });
        } else if (this.showForm.price == "") {
          this.$message({
            showClose: true,
            message: "请设置回答定价",
            type: "warning",
          });
        } else if (this.showForm.price < this.sysparam_lowest_prices){
          this.$message({
            showClose: true,
            message: "定价过低",
            type: "warning",
          });
        } else if (this.showForm.price > this.sysparam_top_prices){
          this.$message({
            showClose: true,
            message: "定价过高",
            type: "warning",
          });
        }
        else {
          const qs = require('qs');
          let field = 0;
          if(this.showForm.field == "英语")
              field = 1;
          if(this.showForm.field == "社会人文")
              field = 2;
          if(this.showForm.field == "物理")
              field = 3;
          if(this.showForm.field == "化学")
              field = 4;
          if(this.showForm.field == "体育")
              field = 5;
          this.$http({
              url: this.$url + "api/upgrade",
              method: 'post',
              data: qs.stringify({
                  "username": this.userMsg.username,
                  "resume": this.showForm.resume,
                  "field": field,
                  "price": this.showForm.price,
              })
          }).then(res=>{
              this.$message({
                  showClose: true,
                  message: '更新成功',
                  type: 'success',
                  duration: 1000,
                  onClose: ()=>{
                      this.$emit("update_dialogVisible", false);
                      this.$router.go(0);
                  }
              });
          }).catch(error=>{
            console.log("error: ",error)
            console.log("showForm.price: ",parseFloat(this.showForm.price));
            this.$message({
                showClose: true,
                message: '更新失败',
                type: 'error',
                onClose: ()=>{
                    this.$emit("update_dialogVisible", false);
                }
            });
          })
        }
      }
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

      //获取全局参数
      if(sessionStorage.getItem('sysparam_lowest_prices')){
        let sysparam_lowest_prices = sessionStorage.getItem('sysparam_lowest_prices');
        let sysparam_top_prices = sessionStorage.getItem('sysparam_top_prices');
        this.sysparam_lowest_prices = parseInt(sysparam_lowest_prices);
        this.sysparam_top_prices = parseInt(sysparam_top_prices);
      }
      else{
        this.sysparam_lowest_prices = this.$Usersysparam.sysparam_lowest_prices;
        this.sysparam_top_prices = this.$Usersysparam.sysparam_top_prices;
      }

      if(this.userMsg.permission == 2){
        this.$http({
          url: this.$url + "api/sendansinfo",
          method: "get",
        })
        .then((res) => {
          for(var i = 0;i < res.data.res.length;i++){
            if(res.data.res[i].username == this.userMsg.username){
              this.showForm.resume = res.data.res[i].resume;
              this.showForm.price = res.data.res[i].price;
              switch (res.data.res[i].field) {
                case 0:
                  this.showForm.field = "数学";
                  break;
                case 1:
                  this.showForm.field = "英语";
                  break;
                case 2:
                  this.showForm.field = "社会人文";
                  break;
                case 3:
                  this.showForm.field = "物理";
                  break;
                case 4:
                  this.showForm.field = "化学";
                  break;
                default:
                  this.showForm.field = "体育";
                  break;
              }
            }
          }
        })
        .catch((error) => {
            console.log(error);
        });
      }
    }
  },
};
</script>

<style scoped></style>
