/* 
 * @Author: hjj 
 * @Date: 2021-10-16 15:55:08 
 * @Last Modified by: hjj
 * @Last Modified time: 2021-11-10 16:36:38
 */

<template>
  <el-dialog :visible.sync="askVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false" width="800px">
    <el-form :model="form">
      <el-form-item label="提问标题" :label-width="formLabelWidth">
        <el-input v-model="form.title" autocomplete="off" type="textarea"></el-input>
      </el-form-item>
      <el-form-item label="提问内容" :label-width="formLabelWidth">
        <el-input v-model="form.content" autocomplete="off" type="textarea"></el-input>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close()">取 消</el-button>
      <el-button type="primary" @click="commit()">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  props: {
    askVisible: {
      type: Boolean,
      default: () => false,
    },
    answer: "",
    price: 0,
  },
  data() {
    return {
      form: {
        title: "",
        content: "",
      },
      formLabelWidth: "120px",
      userMsg: {},
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    close() {
      this.$emit("update_askVisible", false);
    },
    commit() {
      if (this.form.title == "") {
        this.$message({
          showClose: true,
          message: "标题不能为空",
          type: "warning",
        });
      } else if (this.form.content == "") {
        this.$message({
          showClose: true,
          message: "内容不能为空",
          type: "warning",
        });
      } else if (this.userMsg.balance < this.price) {
        this.$message({
          showClose: true,
          message: "您的余额不足，请充值后重试！",
          type: "warning",
        });
      } else {
        let _this = this;
        const qs = require("qs");
        this.$http({
          url: this.$url + "api/ask",
          method: "post",
          data: qs.stringify({
            title: this.form.title,
            questioner: this.userMsg.username,
            answerer: this.answer,
            content: this.form.content,
          }),
        })
          .then(() => {
            this.$http({
              url: this.$url + "api/walletmanagement",
              method: "post",
              data: qs.stringify({
                money: -_this.price,
                username: _this.userMsg.username,
              })
            }).then(() => {
              this.$message({
                showClose: true,
                message: "提问成功",
                type: "success",
                duration: 1000,
                onClose: () => {
                  _this.userMsg.balance -= _this.price;
                  sessionStorage.removeItem('userMsg');
                  sessionStorage.setItem('userMsg',JSON.stringify(_this.userMsg));
                  this.$emit("update_askVisible", false);
                },
              });
            })
          })
          .catch((error) => {
            this.$message({
              showClose: true,
              message: "提问失败",
              type: "error",
              onClose: () => {
                this.$emit("update_askVisible", false);
              },
            });
          });
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
    },
  },
};
</script>

<style scoped>
.el_dialog {
  width: 700px;
  height: 700px;
}
</style>
