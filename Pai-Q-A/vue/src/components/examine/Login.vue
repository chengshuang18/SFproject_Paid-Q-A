/*
 * @Author: hjj 
 * @Date: 2021-10-30 08:39:15 
 * @Last Modified by: hjj
 * @Last Modified time: 2021-11-04 11:05:38
 */

<template>
    <div class="mainbody">
        <div class="login-box">
            <h2>Sign in</h2>
            <form>
                <div class="user-box">
                    <input type="text" name="" required="" v-model="inUsername">
                    <label>Username</label>
                </div>
                <div class="user-box">
                    <input type="password" name="" required="" v-model="inPassword">
                    <label>Password</label>
                </div>
                <a href="#" @click="toMain()">
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    Sign In
                </a>
            </form>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
export default {
  name: "ExamineLogin",
  data() {
    return {
        inUsername: '',
        inPassword: '',
    };
  },
  methods: {
    toMain: function() {
      const qs = require("qs");
      if (this.inUsername == "" || this.inPassword == "") {
        this.$message({
          showClose: true,
          message: "用户名或密码不能为空",
          type: "warning",
        });
      } else {
        this.$http({
          url: this.$url + "api/admin/login",
          method: "post",
          data: qs.stringify({
            username: this.inUsername,
            password: this.inPassword,
          }),
        })
        .then((res) => {
            this.$http({
                url: this.$url + "api/admin/sendsysparam",
                method: "get",
            })
            .then((Res) => {
                const sysparam = Res.data.doc;
                sessionStorage.setItem('sysparam_lowest_prices', sysparam.lowest_prices);
                sessionStorage.setItem('sysparam_top_prices', sysparam.top_prices);
                sessionStorage.setItem('sysparam_wait_answer', sysparam.wait_answer);
                sessionStorage.setItem('sysparam_wait_receive', sysparam.wait_receive);
                sessionStorage.setItem('sysparam_times_AQ', sysparam.times_AQ);
                sessionStorage.setItem('sysparam_time_service', sysparam.time_service);
                Vue.prototype.$sysparam = sysparam;
            })
            .catch((error) => {
                console.log(error);
            })
            this.$http({
                url: this.$url + "api/admin/sendadmininfo",
                method: "get",
            })
            .then((Res) => {
                const manageList = Res.data.userList;
                let management = 0;
                let confirmed_at = "";
                for(let i = 0;i < manageList.length;i++){
                    if(manageList[i].username == this.inUsername){
                        management = manageList[i].management;
                        confirmed_at = manageList[i].confirmed_at;
                    }
                }
                const manageMsg = {
                    username: this.inUsername,
                    management: management,
                    confirmed_at: confirmed_at,
                };

                sessionStorage.setItem('manageMsg', JSON.stringify(manageMsg));
                sessionStorage.setItem('manageList', JSON.stringify(manageList));

                Vue.prototype.$manageMsg = manageMsg;
                Vue.prototype.$manageList = manageList;

                let myfield = 100;
                if(this.inUsername != "root"){
                    myfield = management;
                }
                this.$http({
                    url: this.$url + "api/checkorderlist",
                    method: "get",
                    params: { field: myfield },
                })
                .then((RES) => {
                    const checkorderList = RES.data.userList;
                    sessionStorage.setItem('checkorderList', JSON.stringify(checkorderList));
                    Vue.prototype.$checkorderList = checkorderList;
                    this.$router.push({ path: "/examine/main" });
                })
                .catch((error) => {
                    console.log(error);
                })
            })
            .catch((error) => {
                console.log(error);
            })
        })
        .catch((error) => {
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
  },
  components: {},
  watch: {},
}
</script>

<style scoped>
.mainbody {
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    overflow-y: hidden;
    display: grid;
    height: 100%;
    width: 100%;
    font-family: Arial, Helvetica, sans-serif;
    background: linear-gradient(#cad7f0,#5393db);
}

.login-box{
    position: absolute;
    top: 50%;
    left: 50%;
    width: 400px;
    padding: 40px;
    transform: translate(-50%,-50%);
    background: rgba(188, 118, 231, 0.5);
    box-sizing: border-box;
    box-shadow: 0,15px,25px,rgba(0, 0, 0, 0.6);
    border-radius: 10px;
}

.login-box h2 {
    margin: 0 0 30px;
    padding: 0;
    color: #fff;
    text-align: center;
}

.login-box .user-box {
    position: relative;
}

.login-box .user-box input {
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

.login-box .user-box label {
    position: absolute;
    top: 0;
    left: 0;
    padding: 10px 0;
    font-size: 16px;
    color: #fff;
    pointer-events: none;
    transition: .5s;
}

.login-box .user-box input:focus ~ label,
.login-box .user-box input:valid ~ label {
    top: -20px;
    left: 0;
    color: #fff;
    font-size: 12px;
}

.login-box form a{
    position: relative;
    display: inline-block;
    padding: 10px 20px;
    color: #fff;
    font-size: 12px;
    text-decoration: none;
    text-transform: uppercase;
    overflow: hidden;
    margin-top: 40px;
    margin-left: 107px;
    transition: .5s;
    letter-spacing: 4px;
}

.login-box a:hover {
    background: #fff;
    color: #fff;
    border-radius: 5px;
    box-shadow: 0 0 5px #fff,
                0 0 25px #fff,
                0 0 50px #fff,
                0 0 100px #fff;
}

.login-box a span {
    position: absolute;
    display: block;
}

.login-box a span:nth-child(1){
    top: 0;
    left: -100%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg,transparent,#fff);
    animation: btn-anim1 1s linear infinite;
}

.login-box a span:nth-child(2){
    top: -100%;
    right: 0;
    width: 2px;
    height: 100%;
    background: linear-gradient(180deg,transparent,#fff);
    animation: btn-anim2 1s linear infinite;
    animation-delay: .25s;
}

.login-box a span:nth-child(3){
    bottom: 0;
    right: -100%;
    width: 100%;
    height: 2px;
    background: linear-gradient(270deg,transparent,#fff);
    animation: btn-anim3 1s linear infinite;
    animation-delay: .5s;
}

.login-box a span:nth-child(4){
    bottom: -100%;
    left: 0;
    width: 2px;
    height: 100%;
    background: linear-gradient(360deg,transparent,#fff);
    animation: btn-anim4 1s linear infinite;
    animation-delay: .75s;
}

@keyframes btn-anim1{
    0%{
        left: -100%;
    }
    50%,100%{
        left: 100%;
    }
}
@keyframes btn-anim2{
    0%{
        top: -100%;
    }
    50%,100%{
        top: 100%;
    }
}
@keyframes btn-anim3{
    0%{
        right: -100%;
    }
    50%,100%{
        right: 100%;
    }
}
@keyframes btn-anim4{
    0%{
        bottom: -100%;
    }
    50%,100%{
        bottom: 100%;
    }
}
</style>
