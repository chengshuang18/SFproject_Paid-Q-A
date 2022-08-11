/* * @Author: hjj * @Date: 2021-11-03 19:32:59 * @Last Modified by: wangyang * @Last Modified time: 2021-11-11 14:04:07 */

<template>
  <div class="mainbody">
    <div class="registration-form">
      <header>
        <h1>
          密码找回
        </h1>
        <p>
          完成所有步骤
        </p>
      </header>
      <form>
        <div class="input-section user-section" :class="{ 'fold-up': usernameUp }">
          <input v-model="username" type="text" placeholder="请输入用户名" autocomplete="off" />
          <div class="animated-button">
            <span :class="{ next: username != '' }">
              <i class="el-icon-user"></i>
            </span>
            <span class="next-button" @click="changeUsernameStatus">
              <i class="el-icon-top"></i>
            </span>
          </div>
        </div>
        <div class="input-section email-section" :class="{ folded: !usernameUp, 'fold-up': emailUp }">
          <input v-model="email" type="email" placeholder="请输入邮箱" autocomplete="off" />
          <div class="animated-button">
            <span :class="{ next: email != '' }">
              <i class="el-icon-document"></i>
            </span>
            <span class="next-button" @click="changeEmailStatus">
              <i class="el-icon-top"></i>
            </span>
          </div>
        </div>
        <div class="input-section verification-section" :class="{ folded: !emailUp, 'fold-up': verificationUp }">
          <input v-model="verification" type="text" placeholder="请输入6位验证码" autocomplete="off" />
          <div class="animated-button">
            <span :class="{ next: verification != '' }">
              <i class="el-icon-document"></i>
            </span>
            <span class="next-button" @click="changeVerificationStatus">
              <i class="el-icon-top"></i>
            </span>
          </div>
        </div>
        <div class="input-section password-section" :class="{ folded: !verificationUp, 'fold-up': passwordUp }">
          <input v-model="password" type="password" placeholder="请输入新密码" />
          <div class="animated-button">
            <span :class="{ next: password != '' }">
              <i class="el-icon-paperclip"></i>
            </span>
            <span class="next-button" @click="changePasswordStatus">
              <i class="el-icon-s-promotion"></i>
            </span>
          </div>
        </div>
        <div class="success" :class="{ end: passwordUp }">
          <p @click="closePage">
            密 码 修 改 成 功
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Forget",
  data() {
    return {
      username: "",
      email: "",
      verification: "",
      password: "",
      usernameUp: false,
      emailUp: false,
      verificationUp: false,
      passwordUp: false,
    };
  },
  methods: {
    changeUsernameStatus() {
      this.usernameUp = true;
    },
    changeEmailStatus() {
      const qs = require("qs");
      this.$http({
        url: this.$url + "api/sendverificationcode",
        method: "POST",
        data: qs.stringify({
          username: this.username,
          email: this.email,
        }),
      })
        .then(() => {
          this.emailUp = true;
        })
        .catch(() => {
          this.$message({
            showClose: true,
            message: "请输入正确的邮箱！",
            type: "error",
          });
        });
    },
    changeVerificationStatus() {
      this.verificationUp = true;
    },
    changePasswordStatus() {
      const qs = require("qs");
      this.$http({
        url: this.$url + "api/findpassword",
        method: "POST",
        data: qs.stringify({
          username: this.username,
          password: this.password,
          verificationcode: this.verification,
        }),
      })
        .then(() => {
          this.passwordUp = true;
        })
        .catch(() => {
          this.$message({
            showClose: true,
            message: "验证码错误！",
            type: "error",
          });
          this.$router.go(0);
        });
    },
    closePage() {
      this.$emit("child-msg", false);
    },
  },
};
</script>

<style lang="scss" scoped>
.mainbody {
  background: linear-gradient(#141e30, #243b55);
  position: absolute;
  width: 100%;
  height: 100%;
  font-family: "Roboto";
  z-index: 100;
}

.registration-form {
  width: 400px;
  position: absolute;
  left: 50%;
  transform: translate(-50%, 0%);
  top: 15%;

  background: transparent;

  header {
    position: relative;
    z-index: 4;
    background: white;
    padding: 20px 40px;
    border-radius: 15px 15px 0 0;

    h1 {
      font-weight: 900;
      letter-spacing: 1.5px;
      color: #333;
      font-size: 23px;
      text-transform: uppercase;
      margin: 0;
    }

    p {
      word-spacing: 0px;
      color: rgb(159, 172, 182);
      font-size: 17px;
      margin: 0;
      margin-top: 5px;
    }
  }

  form {
    position: relative;
  }

  .input-section {
    width: 100%;
    position: absolute;
    display: flex;
    left: 50%;
    transform: translate(-50%, 0);
    height: 75px;
    border-radius: 0 0 15px 15px;
    overflow: hidden;
    z-index: 2;
    box-shadow: 0px 0px 100px rgba(0, 0, 0, 0.2);
    transition: all 0.2s ease-in;

    &.folded {
      width: 95%;
      margin-top: 10px;
      left: 50%;
      transform: translate(-50%, 0);
      z-index: 1;

      input {
        background-color: rgb(233, 226, 192);
      }

      span {
        background-color: rgb(233, 226, 192);
      }
    }

    &.folded + .folded {
      width: 90%;
      margin-top: 20px;
      left: 50%;
      transform: translate(-50%, 0);
      z-index: 0;

      input {
        background-color: rgb(225, 188, 239);
      }

      span {
        background-color: rgb(225, 188, 239);
      }
    }

    &.fold-up {
      margin-top: -75px;
    }
  }

  form input {
    background: rgb(243, 243, 251);
    color: rgb(143, 143, 214);
    width: 80%;
    border: 0;
    padding: 20px 40px;
    margin: 0;

    &:focus {
      outline: none;
    }

    &::placeholder {
      color: rgb(143, 143, 214);
      font-weight: 100;
    }
  }
}

.animated-button {
  width: 20%;
  background-color: rgb(212, 212, 255);

  span {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    line-height: 75px;
    text-align: center;
    height: 75px;
    transition: all 0.2s ease-in;

    i {
      font-size: 25px;
      color: rgb(153, 153, 248);
    }
  }

  .next-button {
    background: transparent;
    color: rgb(153, 153, 248);
    font-weight: 100;
    width: 100%;
    border: 0;
  }
}

.next {
  margin-top: -75px;
}

.success {
  width: 100%;
  position: absolute;
  display: flex;
  align-items: center;
  left: 50%;
  transform: translate(-50%, 0);
  height: 75px;
  border-radius: 0 0 15px 15px;
  overflow: hidden;
  z-index: 2;
  box-shadow: 0px 0px 100px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease-in;
  background: limegreen;
  margin-top: -75px;

  p {
    color: white;
    font-weight: 900;
    letter-spacing: 2px;
    font-size: 18px;
    width: 100%;
    text-align: center;
  }
}

.end {
  margin-top: 0;
}
</style>
