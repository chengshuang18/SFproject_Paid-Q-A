// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VCharts from 'v-charts'
import App from './App'
import router from './router'
import axios from 'axios'
import ElementUI from 'element-ui';
import TIM from 'tim-js-sdk';
import TIMUploadPlugin from 'tim-upload-plugin';
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);
Vue.use(VCharts);
Vue.prototype.$http = axios;
Vue.prototype.$url = "https://pai-q-a-autoeng.app.secoder.net/";
//Vue.prototype.$url = "http://127.0.0.1:8888/";
window.$List = [];
window.$isActive = 0;
window.$unreadList = [];
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireAuth)){ // 判断该路由是否需要登录权限
    if (localStorage.getItem('username')) { // 判断当前的token是否存在 ； 登录存入的token
    //localStorage.removeItem('username');
    let val = localStorage.getItem('username');
    val = JSON.parse(val);
    if (Date.now() - val.time > val.expire) {
        localStorage.removeItem('username');
    }
    next();
   }
   else {
    next({
     path: '/',
     query: {redirect: to.fullPath} // 将跳转的路由path作为参数，登录成功后跳转到该路由
    })
   }
  }
  else {
   next();
  }
 })

let options = {
  SDKAppID: 1400581926 // 接入时需要将 0 替换为您的云通信应用的 SDKAppID，类型为 Number
};
// 创建 SDK 实例，`TIM.create()`方法对于同一个 `SDKAppID` 只会返回同一份实例
let tim = TIM.create(options); // SDK 实例通常用 tim 表示

Vue.prototype.$tim = tim;
Vue.prototype.$TIM = TIM;

// 设置 SDK 日志输出级别，详细分级请参见 setLogLevel 接口的说明
tim.setLogLevel(0); // 普通级别，日志量较多，接入时建议使用
// tim.setLogLevel(1); // release级别，SDK 输出关键信息，生产环境时建议使用

// 注册腾讯云即时通信 IM 上传插件
tim.registerPlugin({'tim-upload-plugin': TIMUploadPlugin});

// 监听事件，例如：
tim.on(TIM.EVENT.SDK_READY, function(event) {
  // 收到离线消息和会话列表同步完毕通知，接入侧可以调用 sendMessage 等需要鉴权的接口
  // event.name - TIM.EVENT.SDK_READY
});
tim.on(TIM.EVENT.MESSAGE_RECEIVED, function(event) {
// 收到推送的单聊、群聊、群提示、群系统通知的新消息，可通过遍历 event.data 获取消息列表数据并渲染到页面
// event.name - TIM.EVENT.MESSAGE_RECEIVED
// event.data - 存储 Message 对象的数组 - [Message]
});
tim.on(TIM.EVENT.MESSAGE_REVOKED, function(event) {
// 收到消息被撤回的通知
// event.name - TIM.EVENT.MESSAGE_REVOKED
// event.data - 存储 Message 对象的数组 - [Message] - 每个 Message 对象的 isRevoked 属性值为 true
});
tim.on(TIM.EVENT.MESSAGE_READ_BY_PEER, function(event) {
// SDK 收到对端已读消息的通知，即已读回执。使用前需要将 SDK 版本升级至 v2.7.0 或以上。仅支持单聊会话。
// event.name - TIM.EVENT.MESSAGE_READ_BY_PEER
// event.data - event.data - 存储 Message 对象的数组 - [Message] - 每个 Message 对象的 isPeerRead 属性值为 true
});
tim.on(TIM.EVENT.CONVERSATION_LIST_UPDATED, function(event) {
// 收到会话列表更新通知，可通过遍历 event.data 获取会话列表数据并渲染到页面
// event.name - TIM.EVENT.CONVERSATION_LIST_UPDATED
// event.data - 存储 Conversation 对象的数组 - [Conversation]
});
tim.on(TIM.EVENT.GROUP_LIST_UPDATED, function(event) {
// 收到群组列表更新通知，可通过遍历 event.data 获取群组列表数据并渲染到页面
// event.name - TIM.EVENT.GROUP_LIST_UPDATED
// event.data - 存储 Group 对象的数组 - [Group]
});
tim.on(TIM.EVENT.PROFILE_UPDATED, function(event) {
// 收到自己或好友的资料变更通知
// event.name - TIM.EVENT.PROFILE_UPDATED
// event.data - 存储 Profile 对象的数组 - [Profile]
});
tim.on(TIM.EVENT.BLACKLIST_UPDATED, function(event) {
// 收到黑名单列表更新通知
// event.name - TIM.EVENT.BLACKLIST_UPDATED
// event.data - 存储 userID 的数组 - [userID]
});
tim.on(TIM.EVENT.ERROR, function(event) {
// 收到 SDK 发生错误通知，可以获取错误码和错误信息
// event.name - TIM.EVENT.ERROR
// event.data.code - 错误码
// event.data.message - 错误信息
});
tim.on(TIM.EVENT.SDK_NOT_READY, function(event) {
// 收到 SDK 进入 not ready 状态通知，此时 SDK 无法正常工作
// event.name - TIM.EVENT.SDK_NOT_READY
});
tim.on(TIM.EVENT.KICKED_OUT, function(event) {
// 收到被踢下线通知
// event.name - TIM.EVENT.KICKED_OUT
// event.data.type - 被踢下线的原因，例如:
//    - TIM.TYPES.KICKED_OUT_MULT_ACCOUNT 多实例登录被踢
//    - TIM.TYPES.KICKED_OUT_MULT_DEVICE 多终端登录被踢
//    - TIM.TYPES.KICKED_OUT_USERSIG_EXPIRED 签名过期被踢 （v2.4.0起支持）。 
});
tim.on(TIM.EVENT.NET_STATE_CHANGE, function(event) { 
//  网络状态发生改变（v2.5.0 起支持）。 
// event.name - TIM.EVENT.NET_STATE_CHANGE 
// event.data.state 当前网络状态，枚举值及说明如下： 
//     \- TIM.TYPES.NET_STATE_CONNECTED - 已接入网络 
//     \- TIM.TYPES.NET_STATE_CONNECTING - 连接中。很可能遇到网络抖动，SDK 在重试。接入侧可根据此状态提示“当前网络不稳定”或“连接中” 
//    \- TIM.TYPES.NET_STATE_DISCONNECTED - 未接入网络。接入侧可根据此状态提示“当前网络不可用”。SDK 仍会继续重试，若用户网络恢复，SDK 会自动同步消息  
});
// 开始登录 
//tim.login({userID: Vue.prototype.$userMsg.username, userSig: 'your userSig'});
