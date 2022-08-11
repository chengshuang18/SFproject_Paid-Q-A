/*
 * @Author: hjj 
 * @Date: 2021-10-23 13:58:32 
 * @Last Modified by: hjj
 * @Last Modified time: 2021-11-14 16:58:47
 */

<template>
    <div class="mainbody">
    <div class="container clearfix">
    <div class="people-list" id="people-list">
      <ul class="list">
        <li class="clearfix" v-for="(answer,k) in Answerer" :key="k" :class="{bg: k == isactive}" @click="fn(k)">
          <img :src="answer.src" alt="avatar" />
          <div class="about">
            <div class="name">{{answer.username}}</div>
            <div class="status">
              <i class="el-icon-edit"></i> {{answer.status}}
            </div>
          </div>
          <span v-show="unreadList[k]" class="rad-badge">
              {{unreadList[k]}}
          </span>
        </li>
      </ul>
    </div>
    
    <div class="chat">
      <div class="chat-header clearfix">
        <img :src="Answerer[isactive].src" alt="avatar" />
        
        <div class="chat-about">
          <div class="chat-with">Chat with {{Answerer[isactive].username}}</div>
          <div class="chat-num-messages">already {{Answerer[isactive].message.length}} messages</div>
        </div>
        <i class="fa fa-star"></i>
      </div>
      
      <div class="chat-history" ref="box">
        <ul>
          <li class="clearfix" v-for="(msg,r) in Answerer[isactive].message" :key="r">
            <div v-if="msg.id == userMsg.username" class="message-data align-right">
              <span class="message-data-time" >{{new Date(parseInt(msg.time) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日/g, " ")}}</span> &nbsp; &nbsp;
              <span class="message-data-name" >{{msg.id}}</span>
            </div>
            <div v-else class="message-data">
              <span class="message-data-name">{{msg.id}}</span>
              <span class="message-data-time">{{new Date(parseInt(msg.time) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日/g, " ")}}</span>
            </div>
            <div v-if="msg.id == userMsg.username" class="message other-message float-right">
              {{msg.content}}
            </div>
            <div v-else class="message my-message">
              {{msg.content}}
            </div>
          </li>
        </ul>
        
      </div>
      
      <div class="chat-message clearfix">
        <textarea v-model="textMessage" id="message-to-send" rows="3"></textarea>

        <i @click="showMessage(Answerer[isactive].username)" class="el-icon-chat-line-round"></i>

        <button @click="send(Answerer[isactive].username)">发送</button>

      </div>
      
    </div>
    
  </div>
  <el-drawer
    class="drawer"
    :visible.sync="drawer"
    :with-header="false">
    <div class="chat-history">
        <ul>
          <li class="clearfix" v-for="(msg,r) in msgRecord" :key="r">
            <div v-if="msg.id == userMsg.username" class="message-data align-right">
              <span class="message-data-time" >{{new Date(parseInt(msg.time) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日/g, " ")}}</span> &nbsp; &nbsp;
              <span class="message-data-name" >{{msg.id}}</span>
            </div>
            <div v-else class="message-data">
              <span class="message-data-name">{{msg.id}}</span>
              <span class="message-data-time">{{new Date(parseInt(msg.time) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日/g, " ")}}</span>
            </div>
            <div v-if="msg.id == userMsg.username" class="message other-message float-right">
              {{msg.content}}
            </div>
            <div v-else class="message my-message">
              {{msg.content}}
            </div>
          </li>
        </ul>
    </div>
    <button @click="fetch(Answerer[isactive].username)">查看更多</button>
  </el-drawer>
    </div>
</template>

<script>
export default {
  name: "Chat",
  data() {
    return {
      isactive: 0,
      textMessage: "",
      AnswererID: [],
      Answerer: [],
      msgRecord: [],
      drawer: false,
      nextReqMessageID: '',
      isCompleted: false,
      unreadList: [],
      userMsg: {},

      //当前订单id
      now_order_id: 0,
    };
  },
  created() {
    this.fetchResData();
  },
  mounted() {
    var that = this;
    let onMessageReceived = function(event) {
        that.Answerer.forEach((item, index)=>{
            event.data.forEach((Item, Index)=>{
              if(item.username == Item.from){
                let obj = {
                    id: item.username,
                    content: Item.payload.text,
                    time: Item.time,
                }
                item.message.push(obj);
                if(index == that.isactive){
                    setTimeout(()=>{
                        that.$refs.box.scrollTop = that.$refs.box.scrollHeight;
                    },0)
                }else{
                    setTimeout(()=>{
                        let tmp = that.unreadList;
                        tmp[index] += event.data.length;
                        that.unreadList = tmp;
                        console.log("更新未读");
                    },0)
                }
              }  
            })
        })
    };
    this.$tim.on(this.$TIM.EVENT.MESSAGE_RECEIVED, onMessageReceived);
  },
  methods: {
      fn(index) {
          this.isactive = index;
      },
      send(people) {
          if(this.textMessage == ""){
              this.$message({
                showClose: true,
                message: "内容不能为空",
                type: "warning",
                time: 1000,
              });
          }else{
            var that = this;
            let message = this.$tim.createTextMessage({
                to: people,
                conversationType: this.$TIM.TYPES.CONV_C2C,
                payload: {
                    text: this.textMessage
                },
            });
            let promise = this.$tim.sendMessage(message);
            promise.then(function(imResponse) {
                that.Answerer.forEach((item, index)=>{
                    if(item.username == imResponse.data.message.to){
                        let obj = {
                            id: that.userMsg.username,
                            content: imResponse.data.message.payload.text,
                            time: imResponse.data.message.time,
                        }
                        item.message.push(obj);
                        that.textMessage = "";
                        setTimeout(()=>{
                            that.$refs.box.scrollTop = that.$refs.box.scrollHeight;
                        },0)
                    }
                })
                that.$http({
                  url: that.$url + "api/firstanswer",
                  method: "get",
                  params: { 
                    order_id: that.now_order_id,
                    questioner: people,
                    answerer: that.userMsg.username,
                  },
                })
            }).catch(function(imError) {
                console.warn('sendMessage error:', imError);
            });
          }
      },
      showMessage(people){
        if(this.msgRecord.length == 0){
            var that = this;
            var M = [];
            let promise = this.$tim.getMessageList({conversationID: 'C2C' + people, count: 5});
            promise.then(function(imResponse) {
                const messageList = imResponse.data.messageList; // 消息列表。
                const nextReqMessageID = imResponse.data.nextReqMessageID; // 用于续拉，分页续拉时需传入该字段。
                const isCompleted = imResponse.data.isCompleted; // 表示是否已经拉完所有消息。
                for(var k = 0;k < messageList.length;k++){
                    let obj = {
                        id: messageList[k].from,
                        content: messageList[k].payload.text,
                        time: messageList[k].time,
                    };
                    M.push(obj);
                }
                that.nextReqMessageID = nextReqMessageID;
                that.isCompleted = isCompleted;
                that.msgRecord = M;
                that.drawer = true;
            });
        }else{
            this.drawer = true;
        }
      },
      fetch(people) {
        if(this.msgRecord.length > 5){
            this.$message({
                showClose: true,
                message: "无更多记录"
            });
        }else{
            this.$http({
                url: this.$url + "api/genusersig",
                method: "get",
                params: { username: "ad" },
            }).then((Res)=>{
                this.$http({
                    url: "https://console.tim.qq.com/v4/openim/admin_getroammsg",
                    method: "post",
                    params: {
                        sdkappid: 1400581926,
                        identifier: "ad",
                        usersig: Res.data.sig,
                        random: 99999999,
                        contenttype: "json",
                    },
                    headers: {
                        "Content-Type": "application/json;"
                    },
                    data: {
                        "From_Account":this.userMsg.username,
                        "To_Account":people,
                        "MaxCnt":100,
                        "MinTime":parseInt(new Date().setDate( new Date().getDate() - 7 )/1000),
                        "MaxTime":Date.parse(new Date())/1000
                    }
                }).then((res=>{
                    if(res.data.ErrorCode == 0){
                        var MM = [];
                        for(let i = 0;i < res.data.MsgList.length;i++){
                            let obj = {
                                id: res.data.MsgList[i].From_Account,
                                content: res.data.MsgList[i].MsgBody[0].MsgContent.Text,
                                time: res.data.MsgList[i].MsgTimeStamp,
                            };
                            MM.push(obj)
                        }
                        this.msgRecord = MM;
                    }
                    else{
                        this.$message({
                            showClose: true,
                            message: "拉取记录失败",
                            type: "error",
                        });
                    }
                })).catch((Error) => {
                    this.$message({
                        showClose: true,
                        message: "拉取记录失败",
                        type: "error",
                    });
                });
            }).catch((error) => {});
        }
      },
      fetchResData() {
        //从缓存中获取userMsg
        if(sessionStorage.getItem('userMsg')){
          let userMsg = sessionStorage.getItem('userMsg');
          this.userMsg = JSON.parse(userMsg);
        }
        else{
          this.userMsg = this.$userMsg;
        }

        this.isactive = $isActive;
        if(sessionStorage.getItem('$List')){
          let list = sessionStorage.getItem('$List');
          this.Answerer = JSON.parse(list);
        }
        else{
          this.Answerer = $List;
        }

        //从缓存中获取当前订单id
        if(sessionStorage.getItem('now_order_id'))
          this.now_order_id = sessionStorage.getItem('now_order_id');
        
        var tmp = [];
        var unread = [];
        if(sessionStorage.getItem('$unreadList')){
          let list = sessionStorage.getItem('$unreadList');
          unread = JSON.parse(list);
        }
        else{
          unread = $unreadList;
        }
        for(var i = 0;i < unread.length;i++){
            for(var j = 0;j < this.Answerer.length;j++){
                if(this.Answerer[j].username == unread[i].username){
                    tmp[j] = unread[i].num;
                    break;
                }
            }
        }
        this.unreadList = tmp;
        
        var that = this;
        setTimeout(function(){
          let sig = sessionStorage.getItem('userSig');
          that.$tim.login({userID: that.userMsg.username, userSig: sig});
        },1000);
      },
  },
  watch: {
      isactive(newVal, oldVal){
        var that = this;
        let promise = this.$tim.setMessageRead({conversationID: "C2C" + this.Answerer[newVal].username});
        promise.then(function(imResponse) {
            // 已读上报成功，指定 ID 的会话的 unreadCount 属性值被置为0
            let tmp = that.unreadList;
            tmp[newVal] = 0;
            that.unreadList = tmp;
        }).catch(function(imError) {
            // 已读上报失败
            console.warn('setMessageRead error:', imError);
        });
      }
  }
};
</script>

<style lang="scss" scoped>

$green: #86BB71;
$blue: #94C2ED;
$orange: #E38968;
$gray: #92959E;

*, *:before, *:after {
  box-sizing: border-box;
}

.mainbody {
  align-items: center;
  position: absolute;
  top: 0;
  left: 0;
  display: grid;
  width: 100%;
  place-items: center;
  background: #C5DDEB;
  font: 14px/20px "Lato", Arial, sans-serif;
  padding: 20px 0;
  color: white;
}

.container {
  margin: 0 auto;
  width: 750px;
  background: #444753;
  border-radius: 5px;
}

.people-list {
  width:260px;
  float: left;
  overflow-y: scroll;

  ul {
    padding: 10px;
    height: 600px;
    
    li {
      padding-top: 10px;
      padding-bottom: 10px;
    }

    li::marker{
        color:greenyellow;
        font-size: 0em;
    }
  }
  
  img {
    float: left;
    height: 50px;
    width: 50px;
  }
  
  .about {
    float: left;
    margin-top: 8px;
    padding-left: 8px;
  }

  .rad-badge{
    min-width:20px;
    min-height:20px;	
    line-height:20px;
    margin-left: 90px;
    margin-top: 15px;
    font-weight:bold;
    color: white;
    border-radius:100%;
    font-size:12px;
    background:#E94B3B;
    box-shadow:.5px .2px 1px rgba(#000,.5);
    display:inline-block;
    text-align:center;
    z-index:1;
  }
  
  .status {
    color: $gray;
  }
  
}

.chat {
  width: 490px;
  float:left;
  background: #F2F5F8;
  border-top-right-radius: 5px;
  border-bottom-right-radius: 5px;
  
  color: #434651;
  
  .chat-header {
    padding: 20px;
    border-bottom: 2px solid white;
    
    img {
      float: left;
      height: 50px;
      width: 50px;
    }
    
    .chat-about {
      float: left;
      padding-left: 10px;
      margin-top: 6px;
    }
    
    .chat-with {
      font-weight: bold;
      font-size: 16px;
    }
    
    .chat-num-messages {
      color: $gray;
    }
    
    .fa-star {
      float: right;
      color: #D8DADF;
      font-size: 20px;
      margin-top: 12px;
    }
  }
  
  .chat-history {
    padding-top: 10px;
    padding-left: 20px;
    padding-right: 20px;
    border-bottom: 2px solid white;
    overflow-y: scroll;
    height: 400px;
    
    ul{
        padding-left: 10px;
        padding-right: 10px;
        margin-bottom: 0px;
        li::marker{
            font-size: 0em;
        }
    }
    .message-data {
      margin-bottom: 15px;
    }
    
    .message-data-time {
      color: lighten($gray, 8%);
      padding-left: 6px;
    }
    
    .message {      
      color: white;
      padding: 18px 20px;
      line-height: 26px;
      font-size: 16px;
      border-radius: 7px;
      margin-bottom: 30px;
      width: 90%;
      position: relative;
      
      &:after {
        bottom: 100%;
        left: 7%;
        border: solid transparent;
        content: " ";
        height: 0;
        width: 0;
        position: absolute;
        pointer-events: none;
        border-bottom-color: $green;
        border-width: 10px;
        margin-left: -10px;
      }
    }
    
    .my-message {
      background: $green;
    }
    
    .other-message {
      background: $blue;
      
      &:after {
        border-bottom-color: $blue;
        left: 93%;
      }
    }
    
  }
  
  .chat-message {
    padding: 30px;
    
    textarea {
      width: 100%;
      border: none;
      padding: 10px 20px;
      font: 14px/22px "Lato", Arial, sans-serif;
      margin-bottom: 10px;
      border-radius: 5px;
      resize: none;
      
    }
    
    .el-icon-chat-line-round {
      font-size: 20px;
      color: gray;
      cursor: pointer;
    }
    
    button {
      float: right;
      color: $blue;
      font-size: 16px;
      text-transform: uppercase;
      border: none;
      cursor: pointer;
      font-weight: bold;
      background: #F2F5F8;
      
      &:hover {
        color: darken($blue, 7%);
      }
    }
  }
}

/*
.online, .offline, .me {
    margin-right: 3px;
    font-size: 10px;
  }
  
.online {
  color: $green;
}
  
.offline {
  color: $orange;
}

.me {
  color: $blue;
}
*/
.align-left {
  text-align: left;
}

.align-right {
  text-align: right;
}

.float-right {
  float: right;
}

.clearfix:after {
	visibility: hidden;
	display: block;
	font-size: 0;
	content: " ";
	clear: both;
	height: 0;
}

.bg {
    background-color: rgb(23, 20, 27);
}

.drawer {
    color: rgb(23, 20, 27);
    .chat-history {
        padding-top: 10px;
        padding-left: 20px;
        padding-right: 20px;
        border-bottom: 2px solid white;
        overflow-y: scroll;
        height: 650px;
    
    ul{
        padding-left: 10px;
        padding-right: 10px;
        margin-bottom: 0px;
        li::marker{
            font-size: 0em;
        }
    }
    .message-data {
      margin-bottom: 15px;
    }
    
    .message-data-time {
      color: lighten($gray, 8%);
      padding-left: 6px;
    }
    
    .message {      
      color: white;
      padding: 18px 20px;
      line-height: 26px;
      font-size: 16px;
      border-radius: 7px;
      margin-bottom: 30px;
      width: 90%;
      position: relative;
      
      &:after {
        bottom: 100%;
        left: 7%;
        border: solid transparent;
        content: " ";
        height: 0;
        width: 0;
        position: absolute;
        pointer-events: none;
        border-bottom-color: $green;
        border-width: 10px;
        margin-left: -10px;
      }
    }
    
    .my-message {
      background: $green;
    }
    
    .other-message {
      background: $blue;
      
      &:after {
        border-bottom-color: $blue;
        left: 93%;
      }
    }
    }

    button {
      float: right;
      color: $blue;
      font-size: 17px;
      text-transform: uppercase;
      border: none;
      cursor: pointer;
      font-weight: bold;
      background: #fff;
      padding: 15px;
      
      &:hover {
        color: darken($blue, 7%);
      }
    }
}
</style>
