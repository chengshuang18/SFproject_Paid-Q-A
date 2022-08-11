/* * @Author: hjj * @Date: 2021-08-19 18:39:59 * @Last Modified by: wangyang * @Last Modified time: 2021-11-07 21:21:07 */

<template>
  <div class="mainbody">
    <div v-bind:class="{ container: true, 'right-panel-active': isOK }">
      <!-- Sign Up -->
      <div class="container__form container--signup">
        <form action="#" class="form" id="form1">
          <h2 class="form__title">Sign Up</h2>
          <div class="user-box">
            <input type="text" name="" required value="" v-model="upUsername" />
            <label>Username</label>
          </div>
          <div class="user-box">
            <input type="text" name="" required value="" v-model="upEmail" />
            <label>Email</label>
          </div>
          <div class="user-box">
            <input type="password" name="" required value="" v-model="upPassword" />
            <label>Password</label>
          </div>
          <a @click="addUser">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            Sign Up
          </a>
        </form>
      </div>

      <!-- Sign In -->
      <div class="container__form container--signin">
        <form action="#" class="form" id="form2">
          <h2 class="form__title">Sign In</h2>
          <div class="user-box">
            <input type="text" name="" required value="" v-model="inUsername" />
            <label>Username</label>
          </div>
          <div class="user-box">
            <input type="password" name="" required value="" v-model="inPassword" />
            <label>Password</label>
          </div>
          <span @click="dialogFormVisible = true" class="link">Forget password</span>
          <div class="btngroup">
            <a @click="toURL">
              <span></span>
              <span></span>
              <span></span>
              <span></span>
              Sign In
            </a>
            <a @click="toVisitor">
              <span></span>
              <span></span>
              <span></span>
              <span></span>
              Visitor
            </a>
          </div>
        </form>
      </div>

      <!-- Overlay -->
      <div class="container__overlay">
        <div class="overlay">
          <div class="overlay__panel overlay--left">
            <button class="btn" id="signIn" @click="changeClass()">Sign In</button>
          </div>
          <div class="overlay__panel overlay--right">
            <button class="btn" id="signUp" @click="changeClass()">Sign Up</button>
          </div>
        </div>
      </div>
    </div>
    <Forget v-show="dialogFormVisible" @child-msg="getChildMsg" />
  </div>
</template>

<script>
import Vue from "vue";
import Forget from "@/components/ForgetPassword.vue";

export default {
  name: "Login",
  data() {
    return {
      isOK: false,
      inUsername: "",
      inPassword: "",
      upUsername: "",
      upPassword: "",
      upEmail: "",
      users: [],
      dialogFormVisible: false,
      form: {
        name: "",
        old: "",
        new: "",
      },
      formLabelWidth: "120px",
    };
  },
  methods: {
    changeClass: function() {
      this.isOK = !this.isOK;
    },
    toURL: function() {
      const qs = require("qs");
      if (this.inUsername == "" || this.inPassword == "") {
        this.$message({
          showClose: true,
          message: "用户名或密码不能为空",
          type: "warning",
        });
      } else {
        this.$http({
          url: this.$url + "api/login",
          method: "post",
          data: qs.stringify({
            username: this.inUsername,
            password: this.inPassword,
          }),
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
            Vue.prototype.$userMsg = userMsg;
            sessionStorage.setItem("userMsg", JSON.stringify(userMsg));

            // 开始登录
            this.$http({
              url: this.$url + "api/genusersig",
              method: "get",
              params: { username: userMsg.username },
            })
            .then((Res) => {
              sessionStorage.setItem("userSig", Res.data.sig);
              this.$tim.login({ userID: userMsg.username, userSig: Res.data.sig });
            })
            .catch((error) => {});

            // 获取全局参数
            this.$http({
              url: this.$url + "api/admin/sendsysparam",
              method: "get",
            })
            .then((Res) => {
              const tmp = Res.data.doc;
              Vue.prototype.$Usersysparam = tmp;
              sessionStorage.setItem('sysparam_lowest_prices', Res.data.doc.lowest_prices);
              sessionStorage.setItem('sysparam_top_prices', Res.data.doc.top_prices);
              sessionStorage.setItem('sysparam_wait_answer', Res.data.doc.wait_answer);
              sessionStorage.setItem('sysparam_wait_receive', Res.data.doc.wait_receive);
              sessionStorage.setItem('sysparam_times_AQ', Res.data.doc.times_AQ);
              sessionStorage.setItem('sysparam_time_service', Res.data.doc.time_service);

              let obj = {
                data: res.data.doc.username,
                time: Date.now(),
                expire: 2 * 60 * 60 * 1000,
              };
              localStorage.setItem("username", JSON.stringify(obj));
              if (this.$route.query.redirect) {
                let redirect = this.$route.query.redirect;
                this.$router.push(redirect);
              } else {
                this.$router.push({ path: "/main" });
              }
            })
            .catch(() => {});

          })
          .catch((error) => {
            console.log(error);
            if (error.response.status == 401) {
              this.$message({
                showClose: true,
                message: "用户名或密码错误",
                type: "error",
              });
            }
          });
      }
    },
    addUser: function() {
      const qs = require("qs");
      var reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
      if (this.upUsername == "" || this.upPassword == "" || this.upEmail == "") {
        this.$message({
          showClose: true,
          message: "用户名、密码或邮箱不能为空",
          type: "warning",
        });
      } else if (!reg.test(this.upEmail)) {
        this.$message({
          showClose: true,
          message: "邮箱格式错误",
          type: "error",
        });
      } else {
        var image = {
          /* 将图片（路径）转换为Base64 */
          getBase64FromImageURL(url, callback) {
            var canvas = document.createElement("canvas"),
              ctx = canvas.getContext("2d"),
              img = new Image();
            img.crossOrigin = "Anonymous";
            img.onload = function() {
              canvas.height = img.height;
              canvas.width = img.width;
              ctx.drawImage(img, 0, 0);
              var base64URL = canvas.toDataURL("image/jpeg");
              callback(base64URL);
              canvas = null;
            };
            img.src = url;
          },
          /* 将base64转换为file类型 */
          getFileFromBase64(base64URL, filename) {
            var arr = base64URL.split(","),
              mime = arr[0].match(/:(.*?);/)[1],
              bstr = atob(arr[1]),
              n = bstr.length,
              u8arr = new Uint8Array(n);
            while (n--) {
              u8arr[n] = bstr.charCodeAt(n);
            }
            return new File([u8arr], filename, { type: mime });
          },
        };
        /* 图片路径转文件类型 */
        const photoURL = require("../assets/photo.jpg");
        let formData = new FormData();
        let imageFile = new File([""], "");
        image.getBase64FromImageURL(photoURL, (base64URL) => {
          imageFile = image.getFileFromBase64(base64URL, "imgName");
          formData.append("username", this.upUsername);
          formData.append("password", this.upPassword);
          formData.append("email", this.upEmail);
          formData.append("photo", imageFile);
          this.$http({
            url: this.$url + "api/register",
            method: "post",
            data: formData,
          })
            .then((res) => {
              this.$message({
                showClose: true,
                message: "注册成功",
                type: "success",
                time: 1000,
                onClose: () => {
                  this.$router.go(0);
                },
              });
            })
            .catch((error) => {
              if (error.response.status == 403) {
                if (error.response.data.state == "邮箱已存在") {
                  this.$message({
                    showClose: true,
                    message: "邮箱已存在",
                  });
                } else {
                  this.$message({
                    showClose: true,
                    message: "用户名已存在",
                  });
                }
              }
            });
        });
      }
    },
    toChangePass() {
      const qs = require("qs");
      if (this.form.name == "" || this.form.old == "" || this.form.new == "") {
        this.$message({
          showClose: true,
          message: "用户名、密码不能为空",
          type: "warning",
        });
      } else {
        this.$http({
          url: this.$url + "api/modifypassword",
          method: "post",
          data: qs.stringify({
            newpassword: this.form.new,
            originpassword: this.form.old,
            username: this.form.name,
          }),
        })
          .then((res) => {
            this.$message({
              showClose: true,
              message: "修改成功",
              type: "success",
              time: 1000,
            });
            this.dialogFormVisible = false;
          })
          .catch((error) => {
            if (error.response.status == 400) {
              if (error.response.data.state == "密码错误") {
                this.$message({
                  showClose: true,
                  message: "邮箱已存在",
                });
              } else {
                this.$message({
                  showClose: true,
                  message: "用户名不存在",
                });
              }
            }
          });
      }
    },
    toVisitor() {
      this.$http({
        url: this.$url + "api/sendansinfo",
        method: "get",
      })
        .then((res) => {
          const ansList = res.data.res;
          Vue.prototype.$ansList = ansList;
          sessionStorage.setItem("ansList", JSON.stringify(ansList));
          this.$router.push({ path: "/visitor" });
        })
        .catch((error) => {});
    },
    getChildMsg(val) {
      this.dialogFormVisible = val;
    },
  },
  components: {
    Forget,
  },
  watch: {},
};
</script>

<style scoped>
.mainbody {
  align-items: center;
  position: absolute;
  top: 0;
  left: 0;
  overflow-y: hidden;
  background: linear-gradient(#141e30, #243b55);
  background-attachment: fixed;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  display: grid;
  height: 100%;
  width: 100%;
  place-items: center;
  font-family: Arial, Helvetica, sans-serif;
}

.title {
  font-size: 30px;
  letter-spacing: 20px;
  color: #fff;
}

.form__title {
  font-weight: 300;
  margin: 0;
  margin-bottom: 2rem;
}

.link {
  color: rgb(99, 99, 99);
  font-size: 0.9rem;
  font-size: 12px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  margin-top: 15px;
  transition: 0.5s;
  letter-spacing: 4px;
}

.container {
  background: rgba(0, 0, 0, 0.5);
  box-sizing: border-box;
  box-shadow: 0, 15px, 25px, rgba(0, 0, 0, 0.6);
  border-radius: 10px;
  height: 420px;
  max-width: 758px;
  overflow: hidden;
  position: relative;
  width: 100%;
}

.container__form {
  height: 100%;
  position: absolute;
  top: 0;
  transition: all 0.6s ease-in-out;
}

.container--signin {
  left: 0;
  width: 50%;
  z-index: 2;
}

.container.right-panel-active .container--signin {
  transform: translateX(100%);
}

.container--signup {
  left: 0;
  opacity: 0;
  width: 50%;
  z-index: 1;
}

.container.right-panel-active .container--signup {
  animation: show 0.6s;
  opacity: 1;
  transform: translateX(100%);
  z-index: 5;
}

.container__overlay {
  height: 100%;
  left: 50%;
  overflow: hidden;
  position: absolute;
  top: 0;
  transition: transform 0.6s ease-in-out;
  width: 50%;
  z-index: 100;
}

.container.right-panel-active .container__overlay {
  transform: translateX(-100%);
}

h2 {
  margin: 0 0 30px;
  padding: 0;
  color: #fff;
  text-align: center;
}
.user-box {
  position: relative;
  width: 100%;
}
.user-box input {
  width: 100%;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  margin-bottom: 30px;
  border: none;
  border-bottom: 1px solid #fff;
  outline: none;
  background: transparent;
}
.user-box label {
  position: absolute;
  top: 0;
  left: 0;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  pointer-events: none;
  transition: 0.5s;
}
.user-box input:focus ~ label,
.user-box input:valid ~ label {
  top: -20px;
  left: 0;
  color: #03e9f4;
  font-size: 12px;
}

.overlay {
  background: linear-gradient(#141e30, #243b55);
  background-attachment: fixed;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  height: 100%;
  left: -100%;
  position: relative;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
  width: 200%;
}

.container.right-panel-active .overlay {
  transform: translateX(50%);
}

.overlay__panel {
  align-items: center;
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: center;
  position: absolute;
  text-align: center;
  top: 0;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
  width: 50%;
}

.overlay--left {
  transform: translateX(-20%);
}

.container.right-panel-active .overlay--left {
  transform: translateX(0);
}

.overlay--right {
  right: 0;
  transform: translateX(0);
}

.container.right-panel-active .overlay--right {
  transform: translateX(20%);
}

.btn {
  background-color: #0367a6;
  background-image: linear-gradient(90deg, #0367a6 0%, #008997 74%);
  border-radius: 20px;
  border: 1px solid #0367a6;
  color: #616060;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: bold;
  letter-spacing: 0.1rem;
  padding: 0.9rem 4rem;
  text-transform: uppercase;
  transition: transform 80ms ease-in;
}

a {
  position: relative;
  display: inline-block;
  padding: 10px 20px;
  color: #03e9f4;
  font-size: 12px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  margin-top: 40px;
  transition: 0.5s;
  letter-spacing: 4px;
  background: #202020;
}
.btn {
  position: relative;
  display: inline-block;
  padding: 10px 20px;
  color: #03e9f4;
  font-size: 12px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  margin-top: 40px;
  transition: 0.5s;
  letter-spacing: 4px;
}
.form > .btn {
  margin-top: 1.5rem;
}
.form > a {
  margin-top: 1.5rem;
}

.btn:active {
  transform: scale(0.95);
}

.btn:focus {
  outline: none;
}

a:hover {
  background: #03e9f4;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #03e9f4, 0 0 25px #03e9f4, 0 0 50px #03e9f4, 0 0 100px #03e9f4;
}

.form {
  background-color: #202020;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 3rem;
  height: 100%;
  text-align: center;
}

.btngroup {
  display: flex;
  flex-direction: row;
  width: 300px;
  justify-content: space-around;
}

a span {
  position: absolute;
  display: block;
}
a span:nth-child(1) {
  top: 0;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #03e9f4);
  animation: btn-anim1 1s linear infinite;
}
a span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #03e9f4);
  animation: btn-anim2 1s linear infinite;
  animation-delay: 0.25s;
}
a span:nth-child(3) {
  bottom: 0;
  right: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #03e9f4);
  animation: btn-anim3 1s linear infinite;
  animation-delay: 0.5s;
}
a span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #03e9f4);
  animation: btn-anim4 1s linear infinite;
  animation-delay: 0.75s;
}
@keyframes btn-anim1 {
  0% {
    left: -100%;
  }
  50%,
  100% {
    left: 100%;
  }
}
@keyframes btn-anim2 {
  0% {
    top: -100%;
  }
  50%,
  100% {
    top: 100%;
  }
}
@keyframes btn-anim3 {
  0% {
    right: -100%;
  }
  50%,
  100% {
    right: 100%;
  }
}
@keyframes btn-anim4 {
  0% {
    bottom: -100%;
  }
  50%,
  100% {
    bottom: 100%;
  }
}

@keyframes show {
  0%,
  49.99% {
    opacity: 0;
    z-index: 1;
  }

  50%,
  100% {
    opacity: 1;
    z-index: 5;
  }
}
</style>
