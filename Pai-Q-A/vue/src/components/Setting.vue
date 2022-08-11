/* 
 * @Author: wangyang 
 * @Date: 2021-10-30 12:22:02 
 * @Last Modified by: wangyang
 * @Last Modified time: 2021-11-04 12:20:01
 */

<template>
  <el-container>
    <el-header>
      用户个人信息
    </el-header>
    <el-row>
      <h3>公开头像</h3>
      <div class="avatar-image">
        <el-avatar style="width: 150px; height: 150px" :src="userphoto"></el-avatar>
        <el-upload
          class="upload avatar-image"
          action=""
          accept="image/jpeg,image/png"
          :before-upload="beforeUpload"
          :show-file-list="false"
          :http-request="httpRequest"
        >
          <el-button size="small" type="primary">上传新头像</el-button>
          <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过100kb</div>
        </el-upload>
      </div>
    </el-row>
    <el-divider></el-divider>
    <el-row>
      <h3>用户名: {{ $userMsg.username }}</h3>
      <small>用户名是不可修改的唯一标识</small>
    </el-row>
    <el-divider></el-divider>
    <el-row>
      <h3>邮箱: {{ useremail }}</h3>
      <small>您可以更新自己的邮箱，邮箱通常用于找回密码：</small>
      <el-button type="success" size="small" @click="update_email">更新邮箱</el-button>
    </el-row>
    <el-divider></el-divider>
    <el-row>
      <h3>密码: **********</h3>
      <small>密码是单向哈希保存的，因此您不可见！您可以选择更改密码：</small>
      <el-button type="warning" size="small" @click="update_password">更改密码</el-button>
    </el-row>
    <UdPwd :updatePwdVisible="updatePwdVisible" @update_updatePwdVisible="update_updatePwdVisible"></UdPwd>
    <el-divider></el-divider>
  </el-container>
</template>

<script>
import UdPwd from "@/components/UpdatePassword.vue";

export default {
  name: "Setting",
  data() {
    return {
      useremail: this.$userMsg.email,
      userphoto: "",
      updatePwdVisible: false,
    };
  },
  methods: {
    // 上传文件之前检查文件格式
    beforeUpload(file) {
      const isJPGorPNG = file.type === "image/jpeg" || "image/png";
      const isLt1M = file.size / 1024 / 1024 < 1;
      if (!isJPGorPNG) {
        this.$message.error("上传的头像文件只能是 jpg 或者 png 图片格式！");
      }
      if (!isLt1M) {
        this.$message.error("上传的头像文件大小不能超过 100 KB！");
      }
      return isJPGorPNG && isLt1M;
    },
    // 不使用默认的 action 上传
    httpRequest(data) {
      let _this = this;
      let reader = new FileReader();
      let file = data.file;
      reader.readAsDataURL(file);
      reader.onloadend = function(e) {
        _this.userphoto = this.result;
        //_this.updataImg();
      };
    },
    // 更新邮箱的弹窗
    update_email() {
      var _this = this;
      this.$prompt("请输入新的邮箱", "更新邮箱", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
        inputErrorMessage: "邮箱格式不正确",
      }).then(({ value }) => {
        _this.useremail = value;
        this.$message({
          type: "success",
          message: "更新成功，新邮箱为: " + value,
        });
      }).catch(() => {});
    },
    // 更新密码的弹窗
    update_password() {
      this.updatePwdVisible = true;
    },
    update_updatePwdVisible(val) {
      this.updatePwdVisible = val;
    },
  },
  components: {
    UdPwd,
  },
};
</script>

<style scoped>
.el-container {
  text-align: center;
  line-height: 20px;
  display: flex;
  margin-left: 40px;
  margin-right: 40px;
}
.el-header {
  font-size: 30px;
  font-weight: bold;
  display: flex;
  padding-top: 8px;
  padding-bottom: 8px;
  align-items: center;
  border-bottom: 1px solid #dbdbdb;
}
.el-row {
  text-align: left;
}
.avatar-image {
  display: inline-block;
}
.info-container {
  font-weight: bold;
}
.form-group {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>
