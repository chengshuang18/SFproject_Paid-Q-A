/* * @Author: wangyang * @Date: 2021-10-30 16:55:46 * @Last Modified by: wangyang * @Last Modified time: 2021-10-30 20:58:26 */

<template>
  <el-dialog
    title="更改密码"
    :visible.sync="updatePwdVisible"
    width="30%"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <el-form>
      <el-form-item label="原密码">
        <el-input placeholder="请输入原密码" v-model="raw_pwd" show-password></el-input>
      </el-form-item>
      <el-form-item label="新密码">
        <el-input placeholder="请输入新密码" v-model="new_pwd" show-password></el-input>
      </el-form-item>
      <el-form-item label="确认新密码">
        <el-input placeholder="请确认新密码" v-model="new_pwd2" show-password></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="cancel()">取 消</el-button>
      <el-button type="primary" @click="close()">更 新</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  data() {
    return {
      raw_pwd: "",
      new_pwd: "",
      new_pwd2: "",
      userMsg: {},
    };
  },
  props: {
    updatePwdVisible: {
      type: Boolean,
      default: () => false,
    },
  },
  created() {
    this.fetchData();
  },
  methods: {
    cancel() {
      this.$emit("update_updatePwdVisible", false);
    },
    close() {
      if (this.new_pwd != this.new_pwd2) {
        this.$message.error("两次输入的新密码不一致，请重试！");
      } else {
        const qs = require("qs");
        this.$http({
          url: this.$url + "api/login",
          method: "post",
          data: qs.stringify({
            username: this.userMsg.username,
            password: this.raw_pwd,
          }),
        })
          .catch((error) => {
            if (error.response.status == 401) {
              this.$message({
                showClose: true,
                message: "原密码错误，请重试！",
                type: "error",
              });
            }
          })
          .then((res) => {
            if (res.status == 200) {
              this.$message({
                showClose: true,
                message: "修改密码成功！",
                type: "success",
              });
            }
            this.$emit("update_updatePwdVisible", false);
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
